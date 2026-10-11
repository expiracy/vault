"""Checks for retained integration fixtures and honest optional-scope reporting."""
from contextlib import redirect_stderr, redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("vault_integration", ROOT / "scripts/test_integration.py")
integration = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(integration)


class IntegrationTests(unittest.TestCase):
    def test_offline_replay_reports_unchecked_live_scopes_and_preserves_fixtures(self):
        before = integration.snapshot(integration.FIXTURES)
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "result.json"
            with redirect_stdout(io.StringIO()):
                status = integration.main(["--output", str(output)])
            self.assertEqual(status, 0)
            report = json.loads(output.read_text(encoding="utf-8"))
        self.assertTrue(report["requested_checks_passed"])
        self.assertEqual(report["scopes"]["fresh-agents"]["status"], "not-checked")
        self.assertEqual(report["scopes"]["browser-rendering"]["status"], "not-checked")
        self.assertEqual(report["scopes"]["installed-user-files"]["status"], "not-checked")
        self.assertEqual(before, integration.snapshot(integration.FIXTURES))

    def test_bad_historical_design_state_fails_instead_of_inheriting_old_pass(self):
        with tempfile.TemporaryDirectory() as temporary:
            workdir = Path(temporary)
            fixtures = workdir / "fixtures"
            shutil.copytree(integration.FIXTURES, fixtures)
            feature = fixtures / "historical/projects/delivery-board/features/dashboard.md"
            feature.write_text(feature.read_text(encoding="utf-8").replace("`not-started`", "`implemented`"), encoding="utf-8")
            original = integration.FIXTURES
            self.addCleanup(setattr, integration, "FIXTURES", original)
            integration.FIXTURES = fixtures
            root, _ = integration.prepare(workdir / "run")
            with self.assertRaisesRegex(AssertionError, "incorrectly claims implementation"):
                integration.check_offline(root)

    def test_optional_checks_require_explicit_runtime_paths(self):
        for arguments in (["--agents"], ["--browser"]):
            with self.subTest(arguments=arguments):
                with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as result:
                    integration.main(arguments)
                self.assertEqual(result.exception.code, 2)

    def test_bootstrap_accepts_single_message_and_message_array(self):
        text = "<!-- agent-docs:begin -->\n- docs-context: fixture\n- write-project-doc: fixture\n"
        message = {"content": [{"text": text, "type": "text"}]}
        for payload in (message, [message]):
            with self.subTest(payload_type=type(payload).__name__):
                with patch.object(integration, "run", return_value=json.dumps(payload)):
                    self.assertIn("exactly once", integration.check_bootstrap(Path("codex"), Path("outside")))

    def test_existing_keep_directory_is_never_reused_or_deleted(self):
        with tempfile.TemporaryDirectory() as temporary:
            marker = Path(temporary) / "keep.txt"
            marker.write_text("preserve", encoding="utf-8")
            with self.assertRaisesRegex(AssertionError, "must not already exist"):
                integration.main(["--keep-workdir", temporary])
            self.assertEqual(marker.read_text(encoding="utf-8"), "preserve")

    def test_role_guards_reject_unrelated_edits_and_new_implementation(self):
        before = {"projects/delivery-board/features/dashboard.md": "original", "projects/unrelated/PROJECT.md": "same"}
        allowed = ["projects/delivery-board/features/dashboard.md"]
        for extra, value in (("projects/unrelated/PROJECT.md", "changed"),
                             ("projects/delivery-board/app.py", "new code")):
            with self.subTest(extra=extra):
                after = dict(before)
                after[extra] = value
                with self.assertRaisesRegex(AssertionError, "outside its role"):
                    integration.assert_allowed_changes(before, after, allowed, "design")
        self.assertEqual(integration.assert_allowed_changes(before, {**before, allowed[0]: "updated"}, allowed, "design"), allowed)

    def test_readonly_and_completed_context_guards_reject_mutations(self):
        path = "projects/delivery-board/tasks/dashboard-filters/context.md"
        before, after = {path: "checkpoint"}, {path: "rewritten"}
        for role, allowed in (("recovery", []), ("handoff", ["projects/delivery-board/tasks/dashboard-ranking/context.md"])):
            with self.subTest(role=role), self.assertRaisesRegex(AssertionError, "outside its role"):
                integration.assert_allowed_changes(before, after, allowed, role)

    def test_proposal_state_checks_are_scoped_and_reject_wrong_final_states(self):
        good = "## Change dashboard-ranking\n\n| State | Value |\n| --- | --- |\n| Decision | `proposed` |\n| Implementation | `not-started` |\n| Verification | `not-checked` |\n\n### History\nPreviously mentioned proposed/not-started/not-checked.\n"
        self.assertEqual(integration.check_change_states(good, "dashboard-ranking")["decision"], "proposed")
        for original, changed in (("`proposed`", "`accepted`"), ("`not-started`", "`implemented`"), ("`not-checked`", "`passed`")):
            with self.subTest(changed=changed), self.assertRaisesRegex(AssertionError, "Incorrect current states"):
                integration.check_change_states(good.replace(original, changed), "dashboard-ranking")
        horizontal = "## Change dashboard-filters\n| Decision | Implementation | Verification |\n| --- | --- | --- |\n| `proposed` | `not-started` | `not-checked` |\n"
        self.assertEqual(integration.check_change_states(horizontal, "dashboard-filters")["verification"], "not-checked")

    def test_duplicate_conflicting_horizontal_states_are_rejected(self):
        rows = "| Decision | Implementation | Verification |\n| --- | --- | --- |\n"
        body = ("## Change dashboard-ranking\n" + rows + "| `accepted` | `implemented` | `passed` |\n\n"
                + rows + "| `proposed` | `not-started` | `not-checked` |\n")
        with self.assertRaisesRegex(AssertionError, "Conflicting"):
            integration.check_change_states(body, "dashboard-ranking")

    def test_change_identity_cannot_be_shadowed_by_longer_identifier(self):
        rows = "| Decision | Implementation | Verification |\n| --- | --- | --- |\n"
        body = ("## Change dashboard-ranking-old\n" + rows + "| `proposed` | `not-started` | `not-checked` |\n\n"
                + "## Change dashboard-ranking: current\n" + rows + "| `accepted` | `implemented` | `passed` |\n")
        with self.assertRaisesRegex(AssertionError, "Incorrect current states"):
            integration.check_change_states(body, "dashboard-ranking")


if __name__ == "__main__":
    unittest.main()
