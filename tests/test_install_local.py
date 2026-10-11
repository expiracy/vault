"""Exercise local installation against temporary user profiles, never the real one."""

import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


INSTALLER = Path(__file__).resolve().parents[1] / "scripts" / "install-local.ps1"
POWERSHELL = shutil.which("pwsh") or shutil.which("powershell")


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

    def install(self):
        return subprocess.run([
            POWERSHELL, "-NoProfile", "-File", str(INSTALLER),
            "-DocsRoot", str(self.docs), "-UserDirectory", str(self.user),
        ], text=True, capture_output=True)

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


if __name__ == "__main__":
    unittest.main()
