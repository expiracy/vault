"""Exercise local installation against temporary user profiles, never the real one."""

import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import unittest


INSTALLER = Path(__file__).resolve().parents[1] / "scripts" / "install-local.ps1"
POWERSHELL = shutil.which("pwsh") or shutil.which("powershell")
WINDOWS_POWERSHELL = shutil.which("powershell")


@unittest.skipUnless(POWERSHELL, "PowerShell is needed for Windows local installation")
@unittest.skipUnless(__import__("sys").platform == "win32", "Junction installation is Windows-specific")
class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="agent-docs-install-test-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.docs = self.base / "central docs"
        self.user = self.base / "user profile"
        for relative in (
            "AGENTS.md", "CATALOG.md",
            ".agents/skills/docs-context/SKILL.md",
            ".agents/skills/write-project-doc/SKILL.md",
        ):
            destination = self.docs / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text("fixture\n", encoding="utf-8")
        self.agents = self.user / ".codex" / "AGENTS.md"
        self.agents.parent.mkdir(parents=True)
        self.agents.write_text("Keep this unrelated instruction.\n", encoding="utf-8")

    def install(self, docs_root=None, previous_docs_root=None, engine=None):
        arguments = [
            engine or POWERSHELL, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(INSTALLER),
            "-DocsRoot", str(docs_root or self.docs), "-UserDirectory", str(self.user),
        ]
        if previous_docs_root is not None:
            arguments.extend(["-PreviousDocsRoot", str(previous_docs_root)])
        return subprocess.run(arguments, text=True, capture_output=True)

    @staticmethod
    def source_files(root):
        return {
            str(path.relative_to(root)): path.read_bytes()
            for path in root.rglob("*") if path.is_file()
        }

    def skill_targets(self):
        return {
            skill: (self.user/".agents"/"skills"/skill).resolve()
            for skill in ("docs-context", "write-project-doc")
        }

    def assert_no_transaction_files(self):
        self.assertEqual(
            [path for path in self.user.rglob("*") if ".agent-docs-" in path.name],
            [],
        )

    def install_with_late_file_lock(self, docs_root=None, previous_docs_root=None, engine=None):
        """Lock AGENTS after preflight/staging, so its final publication fails.

        The wrapper intercepts New-Item only within this child process. The real
        installer still performs file replacement and rollback without mocks.
        """
        wrapper = self.base / "lock-installation-destination.ps1"
        wrapper.write_text("""param($Installer, $DocsRoot, $UserDirectory, $FaultPath, $PreviousDocsRoot)
$global:InstallerTestFaultPath = $FaultPath
$global:InstallerTestLock = $null
function global:New-Item {
    [CmdletBinding()]
    param($ItemType, $Path, $Target, [switch]$Force)
    Microsoft.PowerShell.Management\\New-Item @PSBoundParameters
    if ($ItemType -eq 'Junction' -and (Split-Path -Leaf $Target) -eq 'write-project-doc') {
        $global:InstallerTestLock = [IO.File]::Open(
            $global:InstallerTestFaultPath, [IO.FileMode]::Open,
            [IO.FileAccess]::Read, [IO.FileShare]::Read)
        Write-Host 'Late file lock armed after junction staging.'
    }
}
try {
    $parameters = @{ DocsRoot = $DocsRoot; UserDirectory = $UserDirectory }
    if ($PreviousDocsRoot) { $parameters.PreviousDocsRoot = $PreviousDocsRoot }
    & $Installer @parameters
} finally {
    if ($null -ne $global:InstallerTestLock) { $global:InstallerTestLock.Dispose() }
}
""", encoding="utf-8")
        arguments = [
            engine or POWERSHELL, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(wrapper),
            "-Installer", str(INSTALLER), "-DocsRoot", str(docs_root or self.docs),
            "-UserDirectory", str(self.user), "-FaultPath", str(self.agents),
        ]
        if previous_docs_root is not None:
            arguments.extend(["-PreviousDocsRoot", str(previous_docs_root)])
        return subprocess.run(arguments, text=True, capture_output=True)

    def test_install_is_idempotent_and_preserves_unrelated_content(self):
        first = self.install()
        self.assertEqual(first.returncode, 0, first.stderr)
        config = self.user / ".agents" / "agent-docs.json"
        first_body = self.agents.read_text(encoding="utf-8")
        self.assertIn("Keep this unrelated instruction.", first_body)
        self.assertEqual(first_body.count("<!-- agent-docs:begin -->"), 1)
        self.assertEqual(Path(json.loads(config.read_text())["docs_root"]), self.docs)
        for skill in ("docs-context", "write-project-doc"):
            self.assertEqual((self.user/".agents"/"skills"/skill/"SKILL.md").read_text(), "fixture\n")
        data = json.loads(config.read_text())
        data["unrelated_setting"] = {"keep": True}
        config.write_text(json.dumps(data), encoding="utf-8")
        second = self.install()
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(self.agents.read_text(encoding="utf-8"), first_body)
        self.assertEqual(json.loads(config.read_text())["unrelated_setting"], {"keep": True})
        self.assert_no_transaction_files()

    def test_conflicting_skill_is_not_overwritten_and_preflight_is_complete(self):
        conflict = self.user/".agents"/"skills"/"write-project-doc"
        conflict.mkdir(parents=True)
        (conflict/"SKILL.md").write_text("another skill", encoding="utf-8")
        original = self.agents.read_bytes()
        result = self.install()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((conflict/"SKILL.md").read_text(), "another skill")
        self.assertEqual(self.agents.read_bytes(), original)
        self.assertFalse((self.user/".agents"/"agent-docs.json").exists())
        self.assertFalse((self.user/".agents"/"skills"/"docs-context").exists())

    def test_malformed_startup_block_is_rejected_without_changes(self):
        self.agents.write_text("before\n<!-- agent-docs:begin -->\nafter", encoding="utf-8")
        original = self.agents.read_bytes()
        result = self.install()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.agents.read_bytes(), original)
        self.assertFalse((self.user/".agents"/"agent-docs.json").exists())

    def test_different_existing_docs_root_is_preserved(self):
        config = self.user/".agents"/"agent-docs.json"
        config.parent.mkdir(parents=True)
        config.write_text(json.dumps({"docs_root": str(self.base/"other docs")}), encoding="utf-8")
        original = config.read_bytes()
        result = self.install()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(config.read_bytes(), original)
        self.assertFalse((self.user/".agents"/"skills").exists())

    def test_explicit_relocation_preserves_settings_and_both_canonical_sources(self):
        first = self.install()
        self.assertEqual(first.returncode, 0, first.stderr)
        config = self.user/".agents"/"agent-docs.json"
        data = json.loads(config.read_text(encoding="utf-8"))
        nested = {"keep": "deep value"}
        for _ in range(20):
            nested = {"nested": nested}
        data["unrelated_setting"] = {"keep": [True, "unchanged"], "nested": nested}
        config.write_text(json.dumps(data), encoding="utf-8")
        self.agents.write_text(
            self.agents.read_text(encoding="utf-8") + "Keep this trailing instruction.\n",
            encoding="utf-8",
        )
        for skill in ("docs-context", "write-project-doc"):
            (self.docs/".agents"/"skills"/skill/"source-marker.txt").write_text(
                f"Preserve the old {skill} source.\n", encoding="utf-8",
            )
        old_source = self.source_files(self.docs)
        relocated = self.base/"vault"
        shutil.copytree(self.docs, relocated)
        for skill in ("docs-context", "write-project-doc"):
            (relocated/".agents"/"skills"/skill/"SKILL.md").write_text(
                "relocated fixture\n", encoding="utf-8",
            )
        new_source = self.source_files(relocated)

        result = self.install(relocated, self.docs)
        self.assertEqual(result.returncode, 0, result.stderr)
        updated = json.loads(config.read_text(encoding="utf-8"))
        self.assertEqual(Path(updated["docs_root"]), relocated)
        self.assertEqual(updated["unrelated_setting"], data["unrelated_setting"])
        instructions = self.agents.read_text(encoding="utf-8")
        self.assertTrue(instructions.startswith("Keep this unrelated instruction.\n"))
        self.assertTrue(instructions.endswith("Keep this trailing instruction.\n"))
        self.assertEqual(instructions.count("<!-- agent-docs:begin -->"), 1)
        self.assertEqual(instructions.count("<!-- agent-docs:end -->"), 1)
        self.assertIn("Shared Vault documentation and tools", instructions)
        self.assertIn("existing task context to task-owned tools and instructions", instructions)
        for skill, target in self.skill_targets().items():
            self.assertEqual(target, (relocated/".agents"/"skills"/skill).resolve())
            self.assertEqual(
                (self.user/".agents"/"skills"/skill/"SKILL.md").read_text(),
                "relocated fixture\n",
            )
        self.assertEqual(self.source_files(self.docs), old_source)
        self.assertEqual(self.source_files(relocated), new_source)
        repeated = self.install(relocated)
        self.assertEqual(repeated.returncode, 0, repeated.stderr)
        self.assertEqual(self.agents.read_text(encoding="utf-8"), instructions)

    def test_relocation_without_exact_previous_root_leaves_every_destination_unchanged(self):
        first = self.install()
        self.assertEqual(first.returncode, 0, first.stderr)
        relocated = self.base/"vault"
        shutil.copytree(self.docs, relocated)
        config = self.user/".agents"/"agent-docs.json"
        original_config = config.read_bytes()
        original_instructions = self.agents.read_bytes()
        original_targets = self.skill_targets()
        old_source = self.source_files(self.docs)
        for previous in (None, self.base/"wrong previous root"):
            with self.subTest(previous=previous):
                result = self.install(relocated, previous)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(config.read_bytes(), original_config)
                self.assertEqual(self.agents.read_bytes(), original_instructions)
                self.assertEqual(self.skill_targets(), original_targets)
                self.assertEqual(self.source_files(self.docs), old_source)

    def test_relocation_conflicting_second_skill_is_rejected_before_retargeting_first(self):
        first = self.install()
        self.assertEqual(first.returncode, 0, first.stderr)
        relocated = self.base/"vault"
        shutil.copytree(self.docs, relocated)
        conflict = self.user/".agents"/"skills"/"write-project-doc"
        self.assertEqual(conflict.resolve(), (self.docs/".agents"/"skills"/"write-project-doc").resolve())
        conflict.rmdir()  # Remove the temporary junction entry, not its source.
        conflict.mkdir()
        (conflict/"SKILL.md").write_text("unrelated skill", encoding="utf-8")
        config = self.user/".agents"/"agent-docs.json"
        original_config = config.read_bytes()
        original_instructions = self.agents.read_bytes()
        old_source = self.source_files(self.docs)
        new_source = self.source_files(relocated)

        result = self.install(relocated, self.docs)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(config.read_bytes(), original_config)
        self.assertEqual(self.agents.read_bytes(), original_instructions)
        self.assertEqual(
            (self.user/".agents"/"skills"/"docs-context").resolve(),
            (self.docs/".agents"/"skills"/"docs-context").resolve(),
        )
        self.assertEqual((conflict/"SKILL.md").read_text(), "unrelated skill")
        self.assertEqual(self.source_files(self.docs), old_source)
        self.assertEqual(self.source_files(relocated), new_source)

    def test_relocation_retargets_dangling_links_after_temporary_checkout_move(self):
        first = self.install()
        self.assertEqual(first.returncode, 0, first.stderr)
        original_source = self.source_files(self.docs)
        relocated = self.base/"vault"
        self.assertEqual(self.docs.resolve().parent, self.base.resolve())
        self.assertEqual(relocated.resolve().parent, self.base.resolve())
        self.docs.rename(relocated)
        self.assertFalse(self.docs.exists())

        result = self.install(relocated, self.docs)
        self.assertEqual(result.returncode, 0, result.stderr)
        config = self.user/".agents"/"agent-docs.json"
        self.assertEqual(Path(json.loads(config.read_text())["docs_root"]), relocated)
        for skill, target in self.skill_targets().items():
            self.assertEqual(target, (relocated/".agents"/"skills"/skill).resolve())
        self.assertEqual(self.source_files(relocated), original_source)

    def test_unserializable_config_depth_is_refused_before_relocation_changes(self):
        first = self.install()
        self.assertEqual(first.returncode, 0, first.stderr)
        relocated = self.base/"vault"
        shutil.copytree(self.docs, relocated)
        config = self.user/".agents"/"agent-docs.json"
        data = json.loads(config.read_text(encoding="utf-8"))
        nested = {"keep": "do not truncate"}
        for _ in range(110):
            nested = {"nested": nested}
        data["unrelated_setting"] = nested
        config.write_text(json.dumps(data), encoding="utf-8")
        original_config = config.read_bytes()
        original_instructions = self.agents.read_bytes()
        original_targets = self.skill_targets()

        result = self.install(relocated, self.docs)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(config.read_bytes(), original_config)
        self.assertEqual(self.agents.read_bytes(), original_instructions)
        self.assertEqual(self.skill_targets(), original_targets)

    def test_read_only_destinations_are_refused_before_relocation_changes(self):
        first = self.install()
        self.assertEqual(first.returncode, 0, first.stderr)
        relocated = self.base / "vault"
        shutil.copytree(self.docs, relocated)
        config = self.user / ".agents" / "agent-docs.json"
        original_config = config.read_bytes()
        original_instructions = self.agents.read_bytes()
        original_targets = self.skill_targets()
        for destination in (config, self.agents):
            with self.subTest(destination=destination.name):
                os.chmod(destination, stat.S_IREAD)
                try:
                    result = self.install(relocated, self.docs)
                finally:
                    os.chmod(destination, stat.S_IREAD | stat.S_IWRITE)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("read-only", result.stderr)
                self.assertEqual(config.read_bytes(), original_config)
                self.assertEqual(self.agents.read_bytes(), original_instructions)
                self.assertEqual(self.skill_targets(), original_targets)
                self.assert_no_transaction_files()

    def test_late_publication_failure_restores_relocated_files_and_junctions(self):
        first = self.install()
        self.assertEqual(first.returncode, 0, first.stderr)
        config = self.user / ".agents" / "agent-docs.json"
        data = json.loads(config.read_text(encoding="utf-8"))
        data["unrelated_setting"] = {"label": "na\u00efve r\u00e9sum\u00e9", "keep": [True, 7]}
        config.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        original_config = config.read_bytes()
        original_instructions = self.agents.read_bytes()
        original_targets = self.skill_targets()
        old_source = self.source_files(self.docs)
        relocated = self.base / "vault"
        shutil.copytree(self.docs, relocated)
        new_source = self.source_files(relocated)
        for engine in dict.fromkeys(filter(None, (POWERSHELL, WINDOWS_POWERSHELL))):
            with self.subTest(engine=engine):
                result = self.install_with_late_file_lock(relocated, self.docs, engine)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Late file lock armed", result.stdout)
                self.assertIn("were restored", result.stderr)
                self.assertEqual(config.read_bytes(), original_config)
                self.assertEqual(self.agents.read_bytes(), original_instructions)
                self.assertEqual(self.skill_targets(), original_targets)
                self.assertEqual(self.source_files(self.docs), old_source)
                self.assertEqual(self.source_files(relocated), new_source)
                self.assert_no_transaction_files()
        retried = self.install(relocated, self.docs)
        self.assertEqual(retried.returncode, 0, retried.stderr)

    def test_late_failure_restores_original_dangling_junction_entries(self):
        first = self.install()
        self.assertEqual(first.returncode, 0, first.stderr)
        config = self.user / ".agents" / "agent-docs.json"
        original_config = config.read_bytes()
        original_instructions = self.agents.read_bytes()
        original_targets = self.skill_targets()
        original_source = self.source_files(self.docs)
        relocated = self.base / "vault"
        self.assertEqual(self.docs.resolve().parent, self.base.resolve())
        self.assertEqual(relocated.resolve().parent, self.base.resolve())
        self.docs.rename(relocated)
        result = self.install_with_late_file_lock(relocated, self.docs)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("were restored", result.stderr)
        self.assertEqual(config.read_bytes(), original_config)
        self.assertEqual(self.agents.read_bytes(), original_instructions)
        self.assertEqual(self.skill_targets(), original_targets)
        for skill in original_targets:
            destination = self.user / ".agents" / "skills" / skill
            self.assertTrue(os.path.lexists(destination))
            self.assertFalse(destination.exists())
        self.assertEqual(self.source_files(relocated), original_source)
        self.assert_no_transaction_files()
        retried = self.install(relocated, self.docs)
        self.assertEqual(retried.returncode, 0, retried.stderr)

    def test_late_fresh_install_failure_removes_created_files_and_links(self):
        original_instructions = self.agents.read_bytes()
        original_source = self.source_files(self.docs)
        result = self.install_with_late_file_lock()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Late file lock armed", result.stdout)
        self.assertIn("were restored", result.stderr)
        self.assertEqual(self.agents.read_bytes(), original_instructions)
        self.assertFalse((self.user / ".agents").exists())
        self.assertEqual(self.source_files(self.docs), original_source)
        self.assert_no_transaction_files()
        retried = self.install()
        self.assertEqual(retried.returncode, 0, retried.stderr)

    @unittest.skipUnless(WINDOWS_POWERSHELL, "Windows PowerShell is needed for the UTF-8 compatibility check")
    def test_windows_powershell_relocation_preserves_unicode_paths_and_settings(self):
        unicode_docs = self.base/"central caf\u00e9 docs"
        self.assertEqual(self.docs.resolve().parent, self.base.resolve())
        self.assertEqual(unicode_docs.resolve().parent, self.base.resolve())
        self.docs.rename(unicode_docs)
        self.docs = unicode_docs
        first = self.install(engine=WINDOWS_POWERSHELL)
        self.assertEqual(first.returncode, 0, first.stderr)
        config = self.user/".agents"/"agent-docs.json"
        data = json.loads(config.read_text(encoding="utf-8"))
        data["unrelated_setting"] = {"label": "na\u00efve r\u00e9sum\u00e9"}
        config.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        self.agents.write_text(
            self.agents.read_text(encoding="utf-8") + "Keep the caf\u00e9 instruction.\n",
            encoding="utf-8",
        )
        relocated = self.base/"vault \u00e9tude"
        shutil.copytree(self.docs, relocated)

        result = self.install(relocated, self.docs, engine=WINDOWS_POWERSHELL)
        self.assertEqual(result.returncode, 0, result.stderr)
        updated = json.loads(config.read_text(encoding="utf-8"))
        self.assertEqual(Path(updated["docs_root"]), relocated)
        self.assertEqual(updated["unrelated_setting"], data["unrelated_setting"])
        self.assertTrue(self.agents.read_text(encoding="utf-8").endswith("Keep the caf\u00e9 instruction.\n"))
        repeated = self.install(relocated, engine=WINDOWS_POWERSHELL)
        self.assertEqual(repeated.returncode, 0, repeated.stderr)
        self.assertEqual(json.loads(config.read_text(encoding="utf-8")), updated)


if __name__ == "__main__":
    unittest.main()
