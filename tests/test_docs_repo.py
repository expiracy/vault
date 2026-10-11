"""Independent temporary-repository tests for the local documentation helper."""

from contextlib import redirect_stderr, redirect_stdout
import importlib.util
import io
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "docs_repo.py"
SPEC = importlib.util.spec_from_file_location("docs_repo", SCRIPT)
helper = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(helper)


class DocsRepoTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "repo"
        self.root.mkdir()

    def write(self, relative, contents):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents, encoding="utf-8")
        return path

    def project(self, folder="search", name="search", description="Keyword search", extra=""):
        return self.write(f"projects/{folder}/PROJECT.md", f"---\nname: {name}\ndescription: {description}\n{extra}---\n# Project\n")

    def run_helper(self, *arguments):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            status = helper.main(["--root", str(self.root), *arguments])
        return status, out.getvalue(), err.getvalue()

    def assert_ok(self, *arguments):
        status, output, error = self.run_helper(*arguments)
        self.assertEqual(status, 0, error)
        return output

    def assert_bad(self, fragment, *arguments):
        status, _, error = self.run_helper(*arguments)
        self.assertNotEqual(status, 0)
        self.assertIn(fragment, error)

    def test_multiline_metadata_and_deterministic_catalogue(self):
        self.project("zeta", "zeta", ">-\n  Search records across\n  multiple projects.", "aliases: [finder, lookup]\nrepositories: ['https://example.test/zeta.git']\n")
        self.project("alpha", "alpha", "Search and reporting")
        self.assert_ok("catalog")
        catalogue = (self.root / "CATALOG.md").read_text(encoding="utf-8")
        self.assertLess(catalogue.index("[alpha]"), catalogue.index("[zeta]"))
        self.assertIn("Search records across multiple projects.", catalogue)
        self.assertIn("finder, lookup", catalogue)
        self.assert_ok("catalog", "--check")
        self.assert_ok("check")
        self.write("projects/zeta/tasks/sample/context.md", "# Task\nOrdinary progress update.\n")
        self.assert_ok("catalog", "--check")
        self.assert_ok("catalog")
        self.assertEqual(catalogue, (self.root / "CATALOG.md").read_text(encoding="utf-8"))

    def test_add_change_remove_requires_regeneration(self):
        self.project()
        self.assert_bad("missing or stale", "catalog", "--check")
        self.assertFalse((self.root / "CATALOG.md").exists())
        self.assert_ok("catalog")
        self.project(description="New description")
        self.assert_bad("stale", "check")
        self.assert_ok("catalog")
        self.project("other", "other", "Another project")
        self.assert_bad("stale", "catalog", "--check")
        self.assert_ok("catalog")
        shutil.rmtree(self.root / "projects" / "other")
        self.assert_bad("stale", "catalog", "--check")
        self.assert_ok("catalog")
        self.assert_ok("check")

    def test_invalid_metadata(self):
        cases = [
            ("name: Not A Slug\ndescription: okay\n", "lowercase slug"),
            ("name: 12\ndescription: okay\n", "lowercase slug"),
            ("name: valid\ndescription: []\n", "nonempty string"),
            ("name: valid\ndescription: ''\n", "nonempty string"),
            ("name: valid\ndescription: okay\naliases: scalar\n", "array"),
            ("name: valid\ndescription: okay\naliases: [42]\n", "array"),
            ("name: valid\ndescription: okay\nrepositories: [null]\n", "array"),
            ("name: valid\ndescription: okay\naliases: [same, Same]\n", "duplicate aliases"),
            ("name: valid\nname: other\ndescription: okay\n", "duplicate"),
            ("name: [\n", "invalid safe YAML"),
            ("- valid\n- okay\n", "mapping"),
        ]
        for metadata, message in cases:
            with self.subTest(metadata=metadata):
                self.write("projects/example/PROJECT.md", f"---\n{metadata}---\n# Example\n")
                self.assert_bad(message, "catalog")

    def test_duplicate_names_aliases_and_missing_descriptor(self):
        self.project("first", "same")
        self.project("second", "same")
        self.assert_bad("duplicate name/alias", "catalog")
        self.project("second", "second", extra="aliases: [same]\n")
        self.assert_bad("duplicate name/alias", "catalog")
        self.project("second", "second")
        (self.root / "projects" / "empty").mkdir()
        self.assert_bad("missing PROJECT.md", "catalog")

    def test_dangerous_yaml_is_not_executed(self):
        sentinel = self.root / "executed.txt"
        payload = "!!python/object/apply:builtins.open\n" + helper.yaml.safe_dump([str(sentinel), "w"])
        self.write("projects/unsafe/PROJECT.md", f"---\n{payload}---\n")
        self.assert_bad("invalid safe YAML", "catalog")
        self.assertFalse(sentinel.exists())

    def test_recursive_yaml_alias_is_rejected_clearly(self):
        self.project(extra="extra: &x {self: *x}\n")
        self.assert_bad("recursive YAML aliases", "catalog")

    def test_safe_fields_and_encoded_special_paths(self):
        folder = "odd [folder] # 100% (draft)"
        self.project(folder, "odd", "'A | B <img src=\"evil\"> [fake](missing.md) `code` *bold*'", "aliases: ['a|b', '[odd]']\nrepositories: ['https://example.test/a|b']\n")
        self.assert_ok("catalog")
        output = (self.root / "CATALOG.md").read_text(encoding="utf-8")
        self.assertIn("projects/odd%20%5Bfolder%5D%20%23%20100%25%20%28draft%29/PROJECT.md", output)
        self.assertIn("&#124;", output)
        self.assertIn("&lt;img", output)
        self.assertNotIn("[fake](missing.md)", output)
        self.assert_ok("check")

    def test_links_assets_and_anchors(self):
        self.project()
        self.write("docs/feature.md", "# Search `filters`\n## Repeated\n## Repeated\nOther heading\n-------------\n<a id='custom'></a>\n")
        self.write("docs/diagram (draft).svg", "<svg/>")
        self.write("README.md", "[feature](docs/feature.md#search-filters)\n[second](docs/feature.md#repeated-1)\n[setext](docs/feature.md#other-heading)\n[explicit](docs/feature.md#custom)\n![diagram](<docs/diagram (draft).svg> \"Diagram title\")\n[reference][feature]\n[feature]: docs/feature.md#repeated\n<img src='docs/diagram%20%28draft%29.svg'>\n[remote](https://example.invalid/no-check)\n")
        self.assert_ok("catalog")
        self.assert_ok("check")
        self.write("README.md", "![missing](docs/missing.svg)\n[bad](docs/feature.md#missing)\n[bad ref][unknown]\n")
        self.assert_bad("missing local target", "check")
        self.assert_bad("missing anchor", "check")
        self.assert_bad("undefined reference", "check")

    def test_heading_collisions_and_basic_inline_formatting(self):
        self.project()
        self.write("feature.md", "# Foo\n# Foo\n# Foo-1\n## _Visible_ [label][ref] and field_name\n[ref]: feature.md#foo\n")
        self.write("README.md", "[collision](feature.md#foo-1-1)\n[formatted](feature.md#visible-label-and-field_name)\n")
        self.assert_ok("catalog")
        self.assert_ok("check")

    def test_html_attribute_names_and_quoted_values_are_not_links_or_anchors(self):
        self.project()
        self.write("feature.md", "# Feature\n<div data-src='absent.md' data-id='fake' title=\"href='also-absent.md'\"></div>\n<a name='real'></a>\n")
        self.write("README.md", "[real](feature.md#real)\n")
        self.assert_ok("catalog")
        self.assert_ok("check")
        self.write("README.md", "[fake](feature.md#fake)\n")
        self.assert_bad("missing anchor", "check")

    def test_html_character_references_are_decoded_once(self):
        self.project()
        self.write("a&amp;b.svg", "<svg/>")
        self.write("README.md", '<img src="a&amp;amp;b.svg">\n')
        self.assert_ok("catalog")
        self.assert_ok("check")

    def test_balanced_and_escaped_destination_parentheses(self):
        self.project()
        self.write("docs/a(b).md", "# Target\n")
        self.write("README.md", "[balanced](docs/a(b).md#target)\n[escaped](docs/a\\(b\\).md#target \"title\")\n")
        self.assert_ok("catalog")
        self.assert_ok("check")

    def test_malformed_simple_inline_links_are_rejected(self):
        self.project()
        self.write("target.md", "# Target\n")
        self.assert_ok("catalog")
        for link in ("[broken](<target.md>", "[broken](target.md \"unclosed)"):
            with self.subTest(link=link):
                self.write("README.md", link)
                self.assert_bad("malformed inline link", "check")

    def test_examples_and_dependency_directories_are_ignored(self):
        self.project()
        self.write("README.md", "# Intro\n```markdown\n[example](missing.md)\n```\nInline `[example](also-missing.md)`.\n<!-- [comment](absent.md) -->\n")
        for folder in (".git", ".venv", "venv", "node_modules"):
            self.write(f"{folder}/bad.md", "[broken](does-not-exist.md)\n")
        self.assert_ok("catalog")
        self.assert_ok("check")

    def test_escaped_opening_brackets_are_literal_with_odd_backslash_counts(self):
        self.project()
        self.assert_ok("catalog")
        for count in (1, 3, 5):
            with self.subTest(backslashes=count):
                prefix = "\\" * count
                self.write("README.md", f"{prefix}[literal](absent.md)\n!{prefix}[literal image](absent.svg)\n{prefix}[literal][missing]\n")
                self.assert_ok("check")

        self.write("README.md", "\\[literal](absent.md)\n[actual](actual-missing.md)\n")
        status, _, error = self.run_helper("check")
        self.assertNotEqual(status, 0)
        self.assertIn("actual-missing.md", error)
        self.assertNotIn("absent.md", error)

    def test_even_backslash_counts_keep_real_links_and_references(self):
        self.project()
        self.write("target.md", "# Target\n")
        self.assert_ok("catalog")
        for count in (0, 2, 4):
            with self.subTest(backslashes=count):
                prefix = "\\" * count
                self.write("README.md", f"{prefix}[actual](target.md)\n{prefix}[actual][valid]\n[valid]: target.md\n")
                self.assert_ok("check")
                self.write("README.md", f"{prefix}[actual](absent.md)\n")
                self.assert_bad("missing local target", "check")
                self.write("README.md", f"{prefix}[actual][missing]\n")
                self.assert_bad("undefined reference", "check")
        # Escaping an image's ! still leaves an ordinary, active link.
        self.write("README.md", "\\![actual](absent.md)\n")
        self.assert_bad("missing local target", "check")

    def test_inline_code_spans_use_matching_runs_and_unescaped_openers(self):
        self.project()
        self.assert_ok("catalog")
        self.write("README.md", '`[example](absent.md)`\n``[example](absent.md) and ` text``\n`[reference][missing] <img src="absent.svg">`\n')
        self.assert_ok("check")
        for count in (0, 1, 2, 3, 4):
            with self.subTest(backslashes=count):
                prefix = "\\" * count
                self.write("README.md", f"{prefix}`[actual](absent.md){prefix}`\n")
                if count % 2:
                    self.assert_bad("missing local target", "check")
                else:
                    self.assert_ok("check")
        self.write("README.md", "`[actual](absent.md)``\n")
        self.assert_bad("missing local target", "check")
        self.write("README.md", "`unclosed\n[actual](absent.md)\nclosing`\n")
        self.assert_bad("missing local target", "check")

    def test_backticks_in_destinations_and_html_attributes_are_preserved(self):
        self.project()
        self.write("docs/a`b`.md", "# Target\n")
        self.write("docs/a`b`.svg", "<svg/>\n")
        self.write("README.md", '[bare](docs/a`b`.md#target)\n[angle](<docs/a`b`.md> "title `code`")\n[`label`](docs/a`b`.md)\n[reference][feature]\n[feature]: docs/a`b`.md#target\n<img src="docs/a`b`.svg">\n``[example](absent`part`.md)``\n')
        self.assert_ok("catalog")
        self.assert_ok("check")
        self.write("README.md", "[actual](absent`part`.md)\n")
        self.assert_bad("missing local target", "check")

    def test_link_syntax_in_code_labels_does_not_hide_the_outer_destination(self):
        self.project()
        self.write("target.md", "# Target\n")
        self.write("a`b`.md", "# Target\n")
        self.assert_ok("catalog")
        for label in ("`[example](absent.md)`", "outer `[example](absent.md)` label", "``[example](absent`part`.md)``"):
            with self.subTest(label=label):
                self.write("README.md", f"[{label}](target.md)\n[{label}](a`b`.md)\n")
                self.assert_ok("check")
                self.write("README.md", f"[{label}](actual-missing.md)\n")
                status, _, error = self.run_helper("check")
                self.assertNotEqual(status, 0)
                self.assertIn("actual-missing.md", error)
                self.assertNotIn("absent.md", error)

    def test_unc_and_ambiguous_protocol_relative_links_remain_rejected(self):
        self.project()
        self.assert_ok("catalog")
        for link in (
            "[ambiguous](//example.com/docs)\n",
            r"[unc](<\\\\server\share\absent.md>)" + "\n",
            "[encoded](%5C%5Cserver%5Cshare%5Cabsent.md)\n",
            "[file](file://server/share/absent.md)\n",
        ):
            with self.subTest(link=link):
                self.write("README.md", link)
                self.assert_bad("absolute local link", "check")

    def test_find_all_matches_and_repository_filter_without_writes(self):
        self.project("first", "first", "Search product records", "aliases: [products]\nrepositories: ['https://example.test/first.git']\n")
        self.project("second", "second", "Search research records", "repositories: ['https://example.test/second']\n")
        before = sorted(p.relative_to(self.root).as_posix() for p in self.root.rglob("*"))
        status, output, error = self.run_helper("find", "search")
        self.assertEqual(status, 0)
        self.assertEqual(output.splitlines(), ["projects/first/PROJECT.md", "projects/second/PROJECT.md"])
        self.assertIn("Multiple projects", error)
        self.assertEqual(self.assert_ok("find", "products").strip(), "projects/first/PROJECT.md")
        self.assertEqual(self.assert_ok("find", "search", "--repository", "https://EXAMPLE.test/first/").strip(), "projects/first/PROJECT.md")
        self.assertEqual(self.assert_ok("find", "example.test/second").strip(), "projects/second/PROJECT.md")
        self.assert_bad("No matching", "find", "absent")
        self.assertEqual(before, sorted(p.relative_to(self.root).as_posix() for p in self.root.rglob("*")))

    def test_find_matches_multiline_description_words(self):
        self.project(description="|\n  Search records\n  across projects.")
        self.assertEqual(self.assert_ok("find", "records across").strip(), "projects/search/PROJECT.md")

    def test_relocated_script_runs_from_unrelated_working_directory(self):
        self.project()
        copied = self.root / "scripts" / "docs_repo.py"
        copied.parent.mkdir()
        shutil.copyfile(SCRIPT, copied)
        unrelated = Path(self.temporary.name) / "outside"
        unrelated.mkdir()
        generated = subprocess.run([sys.executable, str(copied), "catalog"], cwd=unrelated, text=True, capture_output=True)
        self.assertEqual(generated.returncode, 0, generated.stderr)
        self.assertTrue((self.root / "CATALOG.md").is_file())
        self.assertFalse((unrelated / "CATALOG.md").exists())
        checked = subprocess.run([sys.executable, str(copied), "check"], cwd=unrelated, text=True, capture_output=True)
        self.assertEqual(checked.returncode, 0, checked.stderr)
        found = subprocess.run([sys.executable, str(copied), "find", "keyword"], cwd=unrelated, text=True, capture_output=True)
        self.assertEqual(found.returncode, 0, found.stderr)
        self.assertEqual(found.stdout.strip(), "projects/search/PROJECT.md")

    def test_parent_escape_and_absolute_links_are_rejected(self):
        self.project()
        (self.root.parent / "outside.md").write_text("# Outside", encoding="utf-8")
        self.write("README.md", "[escape](../outside.md)\n[encoded](%2e%2e/outside.md)\n[absolute](file:///outside.md)\n")
        self.assert_ok("catalog")
        self.assert_bad("escapes repository", "check")
        self.assert_bad("absolute local link", "check")

    def test_outside_symlinks_are_rejected_if_available(self):
        self.project()
        outside = self.root.parent / "outside.md"
        outside.write_text("# Outside", encoding="utf-8")
        try:
            (self.root / "linked.md").symlink_to(outside)
        except OSError as exc:
            self.skipTest(f"symlinks unavailable: {exc}")
        self.assert_ok("catalog")
        self.assert_bad("escapes repository", "check")


if __name__ == "__main__":
    unittest.main()
