#!/usr/bin/env python3
"""Small, local-only catalogue and bounded Markdown consistency helper."""

from __future__ import annotations

import argparse
import html
from html.parser import HTMLParser
import os
from pathlib import Path, PureWindowsPath
import re
import sys
from urllib.parse import quote, unquote, urlsplit

import yaml


DEFAULT_ROOT = Path(__file__).resolve().parents[1]
IGNORED_DIRS = {".git", ".venv", "venv", "__pycache__", "node_modules"}
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
LINK_START = re.compile(r"!?\[(?:\\.|[^\]\\\n])*\]\(")
REFERENCE = re.compile(r"!?\[((?:\\.|[^\]\\\n])*)\]\[([^\]\n]*)\]")
DEFINITION = re.compile(r"^ {0,3}\[([^\]\n]+)\]:\s*(<[^>\n]*>|(?:\\.|[^\s])+)", re.M)
MARKDOWN_ESCAPE = re.compile(r"\\([!\"#$%&'()*+,\-./:;<=>?@\[\\\]^_`{|}~])")
HTML_TAG = re.compile(r"</?[a-zA-Z](?:[^\"'>]|\"[^\"]*\"|'[^']*')*>")
BACKTICKS = re.compile(r"`+")


class Invalid(ValueError):
    """Invalid repository input, reported without a traceback."""


def bounded(root: Path, path: Path) -> Path:
    resolved = path.resolve()
    if not resolved.is_relative_to(root):
        raise Invalid(f"path escapes repository: {path}")
    return resolved


def read_text(root: Path, path: Path) -> str:
    bounded(root, path)
    return path.read_text(encoding="utf-8-sig")


def frontmatter(text: str, path: Path) -> str:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise Invalid(f"{path}: expected YAML frontmatter starting with ---")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise Invalid(f"{path}: unclosed YAML frontmatter") from exc
    return "\n".join(lines[1:end])


def reject_duplicate_keys(node: yaml.Node | None, active: set[int] | None = None) -> None:
    if not isinstance(node, (yaml.MappingNode, yaml.SequenceNode)):
        return
    active = set() if active is None else active
    if id(node) in active:
        raise Invalid("recursive YAML aliases are not supported")
    active.add(id(node))
    try:
        if isinstance(node, yaml.MappingNode):
            seen = set()
            for key, value in node.value:
                if not isinstance(key, yaml.ScalarNode) or key.value in seen:
                    raise Invalid("duplicate or non-scalar YAML key")
                seen.add(key.value)
                reject_duplicate_keys(value, active)
        else:
            for value in node.value:
                reject_duplicate_keys(value, active)
    finally:
        active.remove(id(node))


def descriptors(root: Path) -> list[dict]:
    projects = root / "projects"
    if not projects.exists():
        return []
    bounded(root, projects)
    result = []
    routes: dict[str, str] = {}
    for directory in sorted(projects.iterdir(), key=lambda p: p.name):
        if not directory.is_dir() or directory.name in IGNORED_DIRS:
            continue
        bounded(root, directory)
        path = directory / "PROJECT.md"
        if not path.is_file():
            raise Invalid(f"{directory.relative_to(root)}: missing PROJECT.md")
        try:
            metadata = frontmatter(read_text(root, path), path.relative_to(root))
            # safe_load rejects executable/object tags; compose additionally detects
            # duplicate keys, which ordinary safe_load would silently overwrite.
            reject_duplicate_keys(yaml.compose(metadata, Loader=yaml.SafeLoader))
            data = yaml.safe_load(metadata)
        except yaml.YAMLError as exc:
            raise Invalid(f"{path.relative_to(root)}: invalid safe YAML: {exc}") from exc
        if not isinstance(data, dict):
            raise Invalid(f"{path.relative_to(root)}: frontmatter must be a mapping")
        name, description = data.get("name"), data.get("description")
        if not isinstance(name, str) or not SLUG.fullmatch(name):
            raise Invalid(f"{path.relative_to(root)}: name must be a lowercase slug")
        if not isinstance(description, str) or not description.strip():
            raise Invalid(f"{path.relative_to(root)}: description must be a nonempty string")
        for field in ("aliases", "repositories"):
            values = data.get(field, [])
            if not isinstance(values, list) or any(
                not isinstance(value, str) or not value.strip() or value != value.strip()
                for value in values
            ):
                raise Invalid(f"{path.relative_to(root)}: {field} must be an array of nonempty strings")
            if len({value.casefold() for value in values}) != len(values):
                raise Invalid(f"{path.relative_to(root)}: duplicate {field}")
            data[field] = values
        for route in [name, *data["aliases"]]:
            key = route.casefold()
            if key in routes:
                raise Invalid(f"{path.relative_to(root)}: duplicate name/alias {route!r} (also {routes[key]})")
            routes[key] = str(path.relative_to(root))
        data["path"] = path.relative_to(root).as_posix()
        result.append(data)
    return sorted(result, key=lambda item: (item["name"], item["path"]))


def markdown_field(value: str) -> str:
    value = html.escape(" ".join(value.split()), quote=False)
    for character in "\\|`*_[]":
        value = value.replace(character, f"&#{ord(character)};")
    return value


def catalogue(items: list[dict]) -> str:
    lines = [
        "# Project catalogue", "",
        "Generated from project frontmatter. Regenerate with `python scripts/docs_repo.py catalog`.",
        "", "| Project | Description | Aliases | Repositories |", "| --- | --- | --- | --- |",
    ]
    for item in items:
        target = quote(item["path"], safe="/")
        fields = [
            f'[{item["name"]}]({target})', markdown_field(item["description"]),
            markdown_field(", ".join(sorted(item["aliases"]))),
            markdown_field(", ".join(sorted(item["repositories"]))),
        ]
        lines.append("| " + " | ".join(fields) + " |")
    return "\n".join(lines) + "\n"


def without_examples(text: str) -> str:
    """Preserve line positions while excluding frontmatter, comments and fences."""
    lines = text.splitlines(keepends=True)
    front = bool(lines and lines[0].strip() == "---")
    fence = None
    output = []
    for index, line in enumerate(lines):
        if front:
            output.append("\n" if line.endswith("\n") else "")
            if index and line.strip() == "---":
                front = False
            continue
        match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            if match and match[1][0] == fence[0] and len(match[1]) >= len(fence) and not match[2].strip():
                fence = None
            output.append("\n" if line.endswith("\n") else "")
        elif match:
            fence = match[1]
            output.append("\n" if line.endswith("\n") else "")
        else:
            output.append(line)
    return re.sub(r"<!--[\s\S]*?-->", lambda m: "\n" * m[0].count("\n"), "".join(output))


class HTMLReferences(HTMLParser):
    """Tokenise actual attributes, ignoring data-src/data-id and quoted prose."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, int]] = []
        self.anchor_ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if value is None:
                continue
            if name in {"href", "src"}:
                self.links.append((value, self.getpos()[0]))
            elif name == "id" or (name == "name" and tag == "a"):
                self.anchor_ids.add(value)


def html_references(text: str) -> HTMLReferences:
    parser = HTMLReferences()
    parser.feed(text)
    parser.close()
    return parser


def anchors(text: str) -> set[str]:
    text = without_examples(text)
    result = html_references(text).anchor_ids
    headings = []
    previous = ""
    for line in text.splitlines():
        atx = re.match(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if atx:
            headings.append(atx[1])
        elif previous.strip() and re.fullmatch(r" {0,3}(?:=+|-+)\s*", line):
            headings.append(previous.strip())
        previous = line
    used_slugs = set()
    for heading in headings:
        heading = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", heading)
        heading = REFERENCE.sub(r"\1", heading)
        heading = html.unescape(re.sub(r"<[^>]*>", "", heading))
        heading = MARKDOWN_ESCAPE.sub(r"\1", heading)
        heading = re.sub(r"(?<!\w)_{1,2}(.+?)_{1,2}(?!\w)", r"\1", heading)
        heading = re.sub(r"[*~`]", "", heading).lower()
        slug = re.sub(r"[^\w\- ]", "", heading, flags=re.UNICODE).replace(" ", "-")
        candidate, suffix = slug, 1
        while candidate in used_slugs:
            candidate = f"{slug}-{suffix}"
            suffix += 1
        used_slugs.add(candidate)
        result.add(candidate)
    return result


def inline_link(text: str, offset: int) -> tuple[str, int] | None:
    """Read a destination and the full link's end after an opening (."""
    def finishes_link(index: int) -> int | None:
        while index < len(text) and text[index].isspace():
            index += 1
        if index < len(text) and text[index] in "\"'(":
            closing = ")" if text[index] == "(" else text[index]
            index += 1
            while index < len(text):
                if text[index] == "\\" and index + 1 < len(text):
                    index += 2
                elif text[index] == closing:
                    index += 1
                    break
                else:
                    index += 1
            else:
                return None
            while index < len(text) and text[index].isspace():
                index += 1
        return index + 1 if index < len(text) and text[index] == ")" else None

    index = offset
    while index < len(text) and text[index].isspace():
        index += 1
    if index < len(text) and text[index] == "<":
        end = text.find(">", index + 1)
        closing = finishes_link(end + 1) if end != -1 else None
        return (text[index + 1:end], closing) if closing is not None else None
    start, depth = index, 0
    while index < len(text):
        char = text[index]
        if char == "\\" and index + 1 < len(text):
            index += 2
            continue
        if char == "(":
            depth += 1
        elif char == ")":
            if not depth:
                return text[start:index], index + 1
            depth -= 1
        elif char.isspace() and not depth:
            closing = finishes_link(index)
            return (text[start:index], closing) if closing is not None else None
        index += 1
    return None


def inline_destination(text: str, offset: int) -> str | None:
    parsed = inline_link(text, offset)
    return parsed[0] if parsed is not None else None


def escaped(text: str, offset: int) -> bool:
    """Markdown punctuation is escaped by an odd number of backslashes."""
    start = offset
    while start and text[start - 1] == "\\":
        start -= 1
    return (offset - start) % 2 == 1


def code_span_end(text: str, offset: int) -> int | None:
    opener = BACKTICKS.match(text, offset)
    line_end = text.find("\n", opener.end())
    for closing in BACKTICKS.finditer(text, opener.end(), len(text) if line_end == -1 else line_end):
        if len(closing[0]) == len(opener[0]):
            return closing.end()
    return None


def inline_link_start(text: str, offset: int) -> tuple[int, list[tuple[int, int]]] | None:
    """Find ]( outside label code spans, retaining their masking ranges."""
    bracket = offset + (1 if text[offset:offset + 1] == "!" else 0)
    if text[bracket:bracket + 1] != "[" or escaped(text, bracket):
        return None
    index, depth = bracket + 1, 1
    code_spans = []
    while index < len(text) and text[index] != "\n":
        char = text[index]
        if char == "\\":
            index += 2
            continue
        if char == "`":
            end = code_span_end(text, index)
            if end is not None:
                code_spans.append((index, end))
                index = end
                continue
            index = BACKTICKS.match(text, index).end()
            continue
        if char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
            if not depth:
                return (index + 2, code_spans) if text[index + 1:index + 2] == "(" else None
        index += 1
    return None


def without_inline_code(text: str) -> str:
    """Mask code spans, preserving line positions and actual link destinations."""
    output = list(text)
    index = 0
    while index < len(text):
        # A destination or HTML attribute is parsed as part of its enclosing
        # construct; its backticks do not start a Markdown code span.
        definition = DEFINITION.match(text, index)
        if definition:
            index = definition.end()
            continue
        link = inline_link_start(text, index)
        if link is not None:
            parsed = inline_link(text, link[0])
            if parsed is not None:
                for start, end in link[1]:
                    output[start:end] = " " * (end - start)
                index = parsed[1]
                continue
        tag = HTML_TAG.match(text, index)
        if tag:
            index = tag.end()
            continue
        if text[index] == "`" and not escaped(text, index):
            end = code_span_end(text, index)
            if end is not None:
                output[index:end] = " " * (end - index)
                index = end
            else:
                index = BACKTICKS.match(text, index).end()
            continue
        index += 1
    return "".join(output)


def link_targets(text: str) -> tuple[list[tuple[str, int]], list[str]]:
    text = without_inline_code(without_examples(text))
    found, errors = [], []
    references = set()
    def markdown_destination(value: str) -> str:
        return html.unescape(MARKDOWN_ESCAPE.sub(r"\1", value))

    for match in DEFINITION.finditer(text):
        references.add(" ".join(match[1].split()).casefold())
        found.append((markdown_destination(match[2].strip("<>")), text.count("\n", 0, match.start()) + 1))
    for match in LINK_START.finditer(text):
        bracket = match.start() + (1 if match[0].startswith("!") else 0)
        if escaped(text, bracket):
            continue
        target = inline_destination(text, match.end())
        if target is None:
            errors.append(f"line {text.count(chr(10), 0, match.start()) + 1}: malformed inline link")
        else:
            found.append((markdown_destination(target), text.count("\n", 0, match.start()) + 1))
    for match in REFERENCE.finditer(text):
        bracket = match.start() + (1 if match[0].startswith("!") else 0)
        if escaped(text, bracket):
            continue
        reference = " ".join((match[2] or match[1]).split()).casefold()
        if reference not in references:
            errors.append(f"line {text.count(chr(10), 0, match.start()) + 1}: undefined reference {reference!r}")
    found.extend(html_references(text).links)
    return found, errors


def markdown_files(root: Path) -> list[Path]:
    found = []
    for directory, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(name for name in dirs if name not in IGNORED_DIRS)
        for name in dirs:
            bounded(root, Path(directory) / name)
        for name in sorted(files):
            if Path(name).suffix.lower() in {".md", ".markdown"}:
                path = Path(directory) / name
                bounded(root, path)
                found.append(path)
    return found


def check_links(root: Path) -> list[str]:
    errors = []
    cached_anchors = {}
    for source in markdown_files(root):
        targets, syntax_errors = link_targets(read_text(root, source))
        label = source.relative_to(root).as_posix()
        errors.extend(f"{label}: {error}" for error in syntax_errors)
        for target, line in targets:
            raw = target
            if target.startswith("//") or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                if not target.lower().startswith("file:") and not PureWindowsPath(target).is_absolute():
                    continue
                errors.append(f"{label}:{line}: absolute local link is not portable: {raw}")
                continue
            try:
                parts = urlsplit(target)
                decoded = unquote(parts.path).replace("\\", "/")
                if decoded.startswith("/") or PureWindowsPath(decoded).is_absolute():
                    raise Invalid(f"absolute local link is not portable: {raw}")
                destination = bounded(root, source.parent / decoded) if decoded else source
                if not destination.exists():
                    raise Invalid(f"missing local target: {raw}")
                if parts.fragment and destination.suffix.lower() in {".md", ".markdown"}:
                    if destination not in cached_anchors:
                        cached_anchors[destination] = anchors(read_text(root, destination))
                    if unquote(parts.fragment) not in cached_anchors[destination]:
                        raise Invalid(f"missing anchor: {raw}")
            except (Invalid, ValueError, OSError) as exc:
                errors.append(f"{label}:{line}: {exc}")
    return errors


def repository_key(value: str) -> str:
    return value.casefold().rstrip("/").removesuffix(".git")


def parser() -> argparse.ArgumentParser:
    description = "Generate, check or search the local project catalogue; no network access."
    syntax = (
        "Link checks support inline links/images (angle destinations, balanced parentheses, optional titles), "
        "reference definitions and explicit references, quoted HTML href/src, ATX/setext headings and HTML id/name anchors. "
        "Fenced/inline code, frontmatter and comments are skipped. Heading fragments use a GitHub-style basic slug "
        "with duplicate suffixes. This is a bounded syntax checker, not a complete Markdown AST: indented code, "
        "multiline links/headings/code spans and extension-specific generated anchors are unsupported. Remote/deep links are skipped; "
        "protocol-relative //host/path links are treated as UNC paths and rejected. "
        "local paths must remain inside the repository, including symlinks."
    )
    result = argparse.ArgumentParser(description=description, epilog=syntax)
    result.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="repository root (defaults to this script's repository)")
    commands = result.add_subparsers(dest="command", required=True)
    for command in ("catalog", "check", "find"):
        child = commands.add_parser(command, epilog=syntax if command == "check" else None)
        child.add_argument("--root", type=Path, default=argparse.SUPPRESS, help="repository root")
        if command == "catalog":
            child.add_argument("--check", action="store_true", help="fail if the catalogue is missing or stale; do not write")
        elif command == "find":
            child.add_argument("query", help="case-insensitive text in names, aliases, descriptions or repositories")
            child.add_argument("--repository", help="restrict to this exact repository identity (ignores case, trailing / and .git)")
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    root = args.root.resolve()
    try:
        if not root.is_dir():
            raise Invalid(f"repository root does not exist: {root}")
        items = descriptors(root)
        expected = catalogue(items)
        path = root / "CATALOG.md"
        bounded(root, path)
        if args.command == "catalog" and not args.check:
            path.write_text(expected, encoding="utf-8", newline="\n")
            print(f"Generated CATALOG.md from {len(items)} project descriptor(s).")
            return 0
        if args.command in {"catalog", "check"}:
            errors = []
            if not path.is_file() or read_text(root, path) != expected:
                errors.append("CATALOG.md is missing or stale; run catalog to regenerate")
            if args.command == "check":
                errors.extend(check_links(root))
            for error in errors:
                print(error, file=sys.stderr)
            if errors:
                return 1
            print("Catalogue is current." if args.command == "catalog" else "Descriptors, catalogue and supported local links passed.")
            return 0
        query = " ".join(args.query.casefold().split())
        if not query:
            raise Invalid("find query must not be empty")
        matches = []
        for item in items:
            if args.repository and repository_key(args.repository) not in {
                repository_key(value) for value in item["repositories"]
            }:
                continue
            fields = [item["name"], item["description"], *item["aliases"], *item["repositories"]]
            if any(query in " ".join(value.casefold().split()) for value in fields):
                matches.append(item)
        for item in matches:
            print(item["path"])
        if len(matches) > 1:
            print("Multiple projects match; inspect these descriptors before choosing scope.", file=sys.stderr)
        if not matches:
            print("No matching project descriptors.", file=sys.stderr)
        return 0 if matches else 1
    except (Invalid, OSError, UnicodeError, RecursionError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
