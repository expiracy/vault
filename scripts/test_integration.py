#!/usr/bin/env python3
"""Replay bounded Vault integration checks without changing the real installation.

Default checks are offline fixture checks, not proof of agent or viewer behaviour.
--agents starts fresh Codex sessions against an isolated fixture; --browser renders
the current workflow diagram in a local viewer. Both are opt-in and report scope.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import platform
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "integration"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(root):
    return {p.relative_to(root).as_posix(): digest(p) for p in root.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts}


def assert_allowed_changes(before, after, allowed, role):
    removed = sorted(set(before) - set(after))
    changed = sorted(name for name in set(before) | set(after)
                     if before.get(name) != after.get(name))
    require(not removed, f"{role} deleted fixture files: {removed}")
    unexpected = sorted(set(changed) - set(allowed))
    require(not unexpected, f"{role} changed files outside its role: {unexpected}")
    return changed


def section(text, title):
    heading = re.search(r"^(#{1,6})\s+" + re.escape(title) + r"(?=\s|:|$)[^\n]*$", text, re.M)
    require(heading, f"Missing document section: {title}")
    tail = text[heading.end():]
    next_heading = re.search(r"^#{1," + str(len(heading.group(1))) + r"}\s+", tail, re.M)
    return tail[:next_heading.start()] if next_heading else tail


def check_change_states(text, change_id):
    body = section(text, "Change " + change_id)
    # Current state declarations precede the detailed child sections. Historical
    # state words elsewhere must not satisfy the current proposal's assertions.
    next_heading = re.search(r"^#{1,6}\s+", body, re.M)
    body = body[:next_heading.start()] if next_heading else body
    expected = {"decision": "proposed", "implementation": "not-started", "verification": "not-checked"}
    observed = {}
    def record(key, value):
        require(key not in observed or observed[key] == value, f"Conflicting {change_id} {key} states")
        observed[key] = value
    for line in body.splitlines():
        cells = [cell.strip().casefold() for cell in line.strip().strip("|").split("|")]
        if cells[:3] == list(expected):
            continue
        vertical = re.match(r"^\|\s*(Decision|Implementation|Verification)\s*\|\s*`?([a-z-]+)`?\s*\|", line, re.I)
        plain = re.match(r"^(?:-\s*)?(Decision|Implementation|Verification):\s*`?([a-z-]+)`?\b", line, re.I)
        match = vertical or plain
        if match:
            key, value = match.group(1).casefold(), match.group(2).casefold()
            record(key, value)
    lines = body.splitlines()
    for index, line in enumerate(lines):
        cells = [cell.strip().casefold() for cell in line.strip().strip("|").split("|")]
        if cells[:3] == list(expected) and index + 2 < len(lines):
            values = [cell.strip().strip("`") for cell in lines[index + 2].strip().strip("|").split("|")]
            for key, value in zip(expected, values[:3]):
                record(key, value)
    require(observed == expected, f"Incorrect current states for {change_id}: {observed}; expected {expected}")
    return observed


def source_hashes():
    paths = [ROOT / "scripts/test_integration.py", ROOT / "scripts/docs_repo.py",
             ROOT / "planning/assets/docs-workflow.mmd", ROOT / "planning/assets/docs-workflow.svg",
             FIXTURES / "browser.cjs", FIXTURES / "provenance.json"]
    paths.extend(p for p in (ROOT / ".agents/skills").rglob("*") if p.is_file())
    for folder in ("seed", "historical"):
        paths.extend(p for p in (FIXTURES / folder).rglob("*") if p.is_file())
    hashes = {p.relative_to(ROOT).as_posix(): digest(p) for p in sorted(paths)}
    design = (ROOT / "planning/docs-repo-design.md").read_text(encoding="utf-8")
    fence = re.search(r"```mermaid\s*\n(.*?)```", design, re.S)
    require(fence, "Maintained design lacks its Mermaid fence")
    hashes["planning/docs-repo-design.md#mermaid-fence"] = hashlib.sha256(
        fence.group(1).strip().encode("utf-8")).hexdigest()
    return hashes


def run(command, cwd, timeout=60):
    result = subprocess.run([str(x) for x in command], cwd=cwd, text=True,
                            encoding="utf-8", errors="replace", capture_output=True,
                            timeout=timeout)
    require(result.returncode == 0,
            f"Command failed ({result.returncode}): {command[0]}\n"
            + result.stderr[-1500:] + result.stdout[-1500:])
    return result.stdout


def helper(root, *arguments):
    return run([sys.executable, root / "scripts/docs_repo.py", "--root", root,
                *arguments], root)


def prepare(workdir):
    central = workdir / "original" / "vault"
    shutil.copytree(FIXTURES / "seed", central)
    shutil.copytree(ROOT / ".agents/skills", central / ".agents/skills")
    (central / "scripts").mkdir()
    shutil.copy2(ROOT / "scripts/docs_repo.py", central / "scripts/docs_repo.py")
    media = central / "media"
    media.mkdir()
    for name in ("docs-workflow.mmd", "docs-workflow.svg"):
        shutil.copy2(ROOT / "planning/assets" / name, media / name)
    source = (media / "docs-workflow.mmd").read_text(encoding="utf-8").strip()
    (media / "workflow.md").write_text(
        "# Documentation workflow\n\n"
        "![Catalogue, project, design, context and checkpoint flow](docs-workflow.svg)\n\n"
        "[Editable source](docs-workflow.mmd)\n\n```mermaid\n" + source + "\n```\n",
        encoding="utf-8")
    helper(central, "catalog")
    before = snapshot(central)
    moved = workdir / "relocated" / "vault"
    moved.parent.mkdir()
    shutil.move(str(central), moved)
    require(before == snapshot(moved), "Fixture relocation changed content")
    outside = workdir / "outside"
    outside.mkdir()
    # Scope override belongs to this isolated startup file. The live user pointer
    # and canonical installation remain untouched.
    (outside / "AGENTS.md").write_text(
        "# Isolated integration session\n\n"
        f"For this test, the central Vault is `{moved.as_posix()}`. This explicit "
        "test-root instruction overrides the installed docs_root value. Read its "
        "AGENTS.md and copied docs-context/write-project-doc skills, then discover "
        "the relevant project through its CATALOG.md. Work only in this synthetic "
        "Vault. Do not edit the live Vault or global user files. Do not spawn or contact "
        "subagents for this fixture run; complete the assigned single-writer or read-only "
        "role yourself.\n\n"
        f"Use `{Path(sys.executable).as_posix()}` for helper commands; this interpreter "
        "has the harness's PyYAML dependency. There is no copied environment in the "
        "fixture.\n", encoding="utf-8")
    return moved, outside


def check_offline(root):
    helper(root, "check")
    require(helper(root, "find", "delivery-board").strip()
            == "projects/delivery-board/PROJECT.md", "Discovery selected wrong project")
    baseline = snapshot(root / "projects/delivery-board")
    historical = FIXTURES / "historical/projects/delivery-board"
    feature = (historical / "features/dashboard.md").read_text(encoding="utf-8")
    context = (historical / "tasks/dashboard-filters/context.md").read_text(encoding="utf-8")
    require("`proposed` | `not-started` | `not-checked`" in feature,
            "Historical design incorrectly claims implementation")
    require("Status: complete (design deliverable)." in context,
            "Historical design delivery is incomplete")
    require("Confirm the proposed delivery-date source" in context,
            "Recovery evidence lost the unresolved date-source question")
    require("Next action: review the proposal" in context,
            "Recovery evidence lost its next action")
    # This deterministic replay checks state/history invariants in saved agent
    # output. It is deliberately reported separately from fresh-agent execution.
    target = root / "projects/delivery-board"
    shutil.copy2(historical / "features/dashboard.md", target / "features/dashboard.md")
    shutil.copytree(historical / "tasks/dashboard-filters", target / "tasks/dashboard-filters")
    with (target / "PROJECT.md").open("a", encoding="utf-8") as output:
        output.write("\n- Filter design: [filters](tasks/dashboard-filters/context.md)\n")
    protected = "tasks/delivery-list/context.md"
    require(digest(target / protected) == baseline[protected], "Original history changed")
    require(not list(target.rglob("design.md")), "Competing task design appeared")
    require(not list(target.glob("features/*.py")), "Design replay introduced code")
    provenance = json.loads((FIXTURES / "provenance.json").read_text(encoding="utf-8"))
    for relative, expected in provenance["sha256"].items():
        require(digest(FIXTURES / relative) == expected,
                f"Retained historical fixture changed: {relative}")
    helper(root, "check")
    return {"routing": "matching descriptor and relocated links passed",
            "lifecycle": "saved design-only output retains change states, history and recovery facts",
            "scope": "deterministic replay; fresh agents were not exercised by this check"}


def check_task_tool(root):
    task = root / "projects/delivery-board/tasks/count-json-items"
    source = task / "tools/count_items.py"
    inputs = task / "inputs/items.json"
    before = digest(inputs)
    output = task / "outputs/count-report.json"
    for flags, expected in (([], 3), (["--active-only"], 2)):
        run([sys.executable, "tools/count_items.py", "--input", "inputs/items.json",
             "--output", "outputs/count-report.json", *flags], task)
        result = json.loads(output.read_text(encoding="utf-8"))
        require(result["count"] == expected and result["input_count"] == 3,
                f"Incorrect task-tool result for {flags}")
    require(digest(inputs) == before, "Task tool changed input")
    invalid = task / "outputs/invalid.json"
    invalid.write_text("{}", encoding="utf-8")
    preserved = digest(output)
    result = subprocess.run([sys.executable, str(source), "--input", str(invalid),
                             "--output", str(output)], capture_output=True, text=True)
    require(result.returncode != 0 and digest(output) == preserved,
            "Invalid input succeeded or replaced the existing report")
    return "default=3, active-only=2, input preserved, invalid input rejected without report replacement"


def check_media(root):
    design = (ROOT / "planning/docs-repo-design.md").read_text(encoding="utf-8")
    match = re.search(r"```mermaid\s*\n(.*?)```", design, re.S)
    editable = (root / "media/docs-workflow.mmd").read_text(encoding="utf-8").strip()
    require(match and match.group(1).strip() == editable,
            "Current maintained Mermaid fence differs from editable source")
    import xml.etree.ElementTree as ET
    svg = ET.parse(root / "media/docs-workflow.svg").getroot()
    require(svg.tag.endswith("svg") and svg.attrib.get("viewBox"), "Invalid SVG fallback")
    helper(root, "check")
    return "current fence matches editable source; SVG parses; relocated media links resolve (rendering unchecked)"


def check_installation(user_directory):
    configured = json.loads((user_directory / ".agents/agent-docs.json").read_text(encoding="utf-8-sig"))
    require(Path(configured["docs_root"]).resolve() == ROOT, "Installed docs_root points elsewhere")
    instructions = (user_directory / ".codex/AGENTS.md").read_text(encoding="utf-8-sig")
    require(instructions.count("<!-- agent-docs:begin -->") == 1
            and instructions.count("<!-- agent-docs:end -->") == 1,
            "Startup pointer is missing or duplicated")
    for name in ("docs-context", "write-project-doc"):
        installed = user_directory / ".agents/skills" / name / "SKILL.md"
        require(installed.resolve() == ROOT / ".agents/skills" / name / "SKILL.md",
                f"Installed {name} does not resolve to canonical source")
        require(installed.read_bytes() == (ROOT / ".agents/skills" / name / "SKILL.md").read_bytes(),
                f"Installed {name} content differs")
    return "actual user pointer and both canonical skill links inspected read-only"


def check_bootstrap(binary, outside):
    output = run([binary, "debug", "prompt-input",
                  "Find shared project documentation before designing a feature change."], outside)
    data = json.loads(output)
    messages = data if isinstance(data, list) else [data]
    body = "\n".join(block.get("text", "") for message in messages
                     for block in message.get("content", []))
    require("agent-docs:begin" in body, "Fresh startup did not load the managed pointer")
    for name in ("docs-context", "write-project-doc"):
        require(len(re.findall(r"^- " + re.escape(name) + r":", body, re.M)) == 1,
                f"Fresh startup must expose exactly one {name} description")
    return "fresh CLI startup loaded managed guidance and both skill descriptions exactly once"


def agent(binary, outside, root, prompt, schema=None):
    command = [binary, "--ask-for-approval", "never", "exec", "--cd", outside,
               "--sandbox", "workspace-write", "--add-dir", root,
               "--skip-git-repo-check", "--ephemeral", "--json"]
    if schema:
        command.extend(["--output-schema", schema])
    command.append(prompt + " Do not spawn or contact subagents for this fixture run; "
                   "complete the assigned single-writer or read-only role yourself.")
    output = run(command, outside, timeout=420)
    events = []
    for line in output.splitlines():
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    messages = [x["item"]["text"] for x in events
                if x.get("item", {}).get("type") == "agent_message"]
    require(any(x.get("type") == "turn.completed" for x in events), "Fresh agent did not complete")
    require(messages, "Fresh agent returned no final message")
    # Raw prompts, events and stderr are not saved into the repository.
    return messages[-1]


def check_agents(binary, workdir):
    root, outside = prepare(workdir)
    used_source_hashes = source_hashes()
    phases = {}
    before = snapshot(root)
    def phase(name, allowed):
        nonlocal before
        after = snapshot(root)
        changes = assert_allowed_changes(before, after, allowed, name)
        phases[name] = {"before": before, "after": after, "allowed_changes": changes}
        (workdir / "phase-hashes.json").write_text(json.dumps(phases, indent=2) + "\n", encoding="utf-8")
        before = after
    startup = check_bootstrap(binary, outside)
    print("Integration: installed startup passed; running fresh design writer.", file=sys.stderr, flush=True)
    target = root / "projects/delivery-board"
    old_history = digest(target / "tasks/delivery-list/context.md")
    old_source = digest(target / "tasks/count-json-items/tools/count_items.py")
    initial_feature = (target / "features/dashboard.md").read_text(encoding="utf-8")
    agent(binary, outside, root,
          "For Delivery Board, design optional status and inclusive from/to date filters on the existing "
          "dashboard. Combine supplied conditions with AND and preserve default list fields and order. "
          "Deliver a reviewable design only. You are sole shared-document writer named design-writer. "
          "Use existing feature and one context tasks/dashboard-filters/context.md, change dashboard-filters. "
          "Record writer assignment, completion checkpoint, unresolved date-source question and next action. "
          "Do not implement, accept, commit, or edit other project records. Run relevant structural checks.")
    feature = (target / "features/dashboard.md").read_text(encoding="utf-8")
    context = (target / "tasks/dashboard-filters/context.md").read_text(encoding="utf-8")
    phase("design", ["projects/delivery-board/features/dashboard.md", "projects/delivery-board/PROJECT.md",
                     "projects/delivery-board/tasks/dashboard-filters/context.md"])
    check_change_states(feature, "dashboard-filters")
    for state in ("proposed", "not-started", "not-checked"):
        require(state in feature and state in context, f"Design lost {state} state")
    require("completion checkpoint" in context.casefold(), "Design delivery lacks checkpoint")
    require(digest(target / "tasks/delivery-list/context.md") == old_history,
            "Fresh design writer changed historical task")
    require(digest(target / "tasks/count-json-items/tools/count_items.py") == old_source,
            "Fresh design writer changed source")
    require("There are no filters." in feature and "input" in initial_feature,
            "Fresh design writer erased baseline current facts")
    require(section(feature, "Current design").strip() == section(initial_feature, "Current design").strip(),
            "Fresh design writer changed the baseline current design")
    helper(root, "check")
    print("Integration: design state/history passed; running fresh read-only recovery.", file=sys.stderr, flush=True)
    protected = snapshot(root)
    schema = workdir / "recovery-schema.json"
    schema.write_text(json.dumps({"type": "object", "additionalProperties": False,
        "properties": {"delivered": {"type": "string"}, "implemented": {"type": "boolean"},
                       "runtime_verified": {"type": "boolean"}, "next_action": {"type": "string"},
                       "open_issue": {"type": "string"}},
        "required": ["delivered", "implemented", "runtime_verified", "next_action", "open_issue"]}),
        encoding="utf-8")
    recovery = json.loads(agent(binary, outside, root,
        "Resume Delivery Board filter-design work. Recover its delivered scope, implementation and runtime "
        "verification, open issue and next action from shared project context. Read only; edit nothing. "
        "Return the requested JSON fields.", schema))
    require(not recovery["implemented"] and not recovery["runtime_verified"],
            "Recovery confused design delivery with implementation")
    require("date" in recovery["open_issue"].casefold()
            and "review" in recovery["next_action"].casefold(), "Recovery missed date issue or review action")
    require(protected == snapshot(root), "Read-only recovery changed fixture files")
    phase("recovery", [])
    print("Integration: recovery passed; running restricted contributor.", file=sys.stderr, flush=True)
    # An actual contributor writes only its task; a separately started writer
    # integrates it; explicit handoff authorises a third fresh writer to refine.
    feature_hash = digest(target / "features/dashboard.md")
    index_hash = digest(target / "PROJECT.md")
    agent(binary, outside, root,
        "Contribute a design for optional title-only ranking to Delivery Board. You are ranking-contributor, "
        "not a shared writer: design-writer owns features/dashboard.md and PROJECT.md. Write only "
        "tasks/dashboard-ranking/context.md, propose change dashboard-ranking with rank disabled by default, "
        "stable ties and title-only relevance, and preserve list/filter behaviour. Record contributor role. "
        "Do not change shared files, implement or commit. Finish your contribution for integration.")
    require(digest(target / "features/dashboard.md") == feature_hash
            and digest(target / "PROJECT.md") == index_hash, "Contributor edited shared files")
    phase("contributor", ["projects/delivery-board/tasks/dashboard-ranking/context.md"])
    print("Integration: contributor preserved shared files; running assigned integration writer.", file=sys.stderr, flush=True)
    agent(binary, outside, root,
        "You are assigned sole writer design-writer for the shared Delivery Board feature and project index. "
        "Integrate the existing ranking-contributor task into the maintained feature as change dashboard-ranking. "
        "Retain dashboard-filters, original history and the earlier completed design checkpoint. Link the ranking "
        "context from PROJECT.md. Both proposals remain proposed/not-started/not-checked. Record that coordinator "
        "has ended your writer assignment after this delivery and explicitly handed the feature/index to "
        "ranking-contributor for a follow-up. Do not implement or commit; run structural checks.")
    phase("integration", ["projects/delivery-board/features/dashboard.md", "projects/delivery-board/PROJECT.md",
                          "projects/delivery-board/tasks/dashboard-ranking/context.md"])
    integrated_feature = (target / "features/dashboard.md").read_text(encoding="utf-8")
    for change_id in ("dashboard-filters", "dashboard-ranking"):
        check_change_states(integrated_feature, change_id)
    filters_checkpoint = digest(target / "tasks/dashboard-filters/context.md")
    print("Integration: proposals integrated; running explicit writer handoff.", file=sys.stderr, flush=True)
    agent(binary, outside, root,
        "Coordinator explicitly hands the Delivery Board feature and project index to you, ranking-contributor, "
        "as sole writer after design-writer's completed integration. Refine the existing dashboard-ranking proposal "
        "and its same context: title-only relevance excludes status/date weights, ties preserve input order, ranking "
        "is default off. Record the explicit handoff and a completion checkpoint. Preserve dashboard-filters and "
        "its completed context. Create no new task or competing design, implement nothing, commit nothing. Run checks.")
    phase("handoff", ["projects/delivery-board/features/dashboard.md", "projects/delivery-board/PROJECT.md",
                      "projects/delivery-board/tasks/dashboard-ranking/context.md"])
    final_feature = (target / "features/dashboard.md").read_text(encoding="utf-8")
    ranking = (target / "tasks/dashboard-ranking/context.md").read_text(encoding="utf-8")
    require("dashboard-filters" in final_feature and "dashboard-ranking" in final_feature,
            "Shared writer lost one proposal")
    for change_id in ("dashboard-filters", "dashboard-ranking"):
        check_change_states(final_feature, change_id)
    require("handoff" in ranking.casefold(), "New writer omitted handoff record")
    require(digest(target / "tasks/dashboard-filters/context.md") == filters_checkpoint,
            "Handoff changed completed filter task")
    require(digest(target / "tasks/delivery-list/context.md") == old_history
            and digest(target / "tasks/count-json-items/tools/count_items.py") == old_source,
            "Shared writers changed protected history or source")
    require(sorted(p.parent.name for p in (target / "tasks").glob("*/context.md"))
            == ["count-json-items", "dashboard-filters", "dashboard-ranking", "delivery-list"],
            "Agent created additional task records")
    require(not list(target.rglob("design.md")), "Agent created competing task design")
    helper(root, "check")
    return {"startup": startup, "design": "fresh design-only writer passed state/history/structure checks",
            "recovery": recovery, "shared_writer": "fresh contributor, integration writer and explicit handoff passed",
            "role_changes": {name: data["allowed_changes"] for name, data in phases.items()},
            "used_source_sha256": used_source_hashes,
            "scope": "actual installed startup inspected; synthetic root selected through isolated startup guidance"}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write a compact JSON result, without raw agent events")
    parser.add_argument("--installed-user-dir", type=Path, help="Inspect actual user installation read-only")
    parser.add_argument("--agents", action="store_true", help="Run five fresh Codex sessions (requires network/auth; uses account usage)")
    parser.add_argument("--codex-bin", type=Path, help="Codex executable for --agents")
    parser.add_argument("--browser", action="store_true", help="Render Markdown, SVG and Mermaid in a local browser viewer")
    parser.add_argument("--node", type=Path)
    parser.add_argument("--node-modules", type=Path, help="Directory containing playwright and marked")
    parser.add_argument("--browser-executable", type=Path)
    parser.add_argument("--keep-workdir", type=Path, help="New empty directory for fixture outputs/screenshots; default is temporary")
    args = parser.parse_args(argv)
    if args.agents and not args.codex_bin:
        parser.error("--agents requires --codex-bin")
    if args.browser and not all((args.node, args.node_modules, args.browser_executable)):
        parser.error("--browser requires --node, --node-modules and --browser-executable")
    report = {"recorded_at_utc": datetime.now(timezone.utc).isoformat(),
              "environment": {"python": platform.python_version(), "platform": platform.system()},
              "source_sha256": source_hashes(),
              "fixture": "synthetic Delivery Board; no live documentation or installation mutation",
              "scopes": {}}
    cleanup = None
    if args.keep_workdir:
        require(not args.keep_workdir.exists(), "--keep-workdir must not already exist")
        workdir = args.keep_workdir.resolve()
        workdir.mkdir(parents=True)
    else:
        cleanup = tempfile.TemporaryDirectory(prefix="vault-integration-")
        workdir = Path(cleanup.name)
    def check(name, function=None):
        if function is None:
            report["scopes"][name] = {"status": "not-checked"}
            return
        try:
            report["scopes"][name] = {"status": "passed", "evidence": function()}
        except Exception as error:
            report["scopes"][name] = {"status": "failed", "error": str(error)}
    try:
        root, _ = prepare(workdir)
        check("offline-routing-lifecycle", lambda: check_offline(root))
        check("task-tool", lambda: check_task_tool(root))
        check("media-source-portability", lambda: check_media(root))
        check("installed-user-files", (lambda: check_installation(args.installed_user_dir.resolve()))
              if args.installed_user_dir else None)
        if args.agents:
            agents_workdir = workdir / "agents"
            agents_workdir.mkdir()
            check("fresh-agents", lambda: check_agents(args.codex_bin.resolve(), agents_workdir))
        else:
            check("fresh-agents")
        if args.browser:
            check("browser-rendering", lambda: json.loads(run([args.node.resolve(),
                FIXTURES / "browser.cjs", "--root", root, "--modules", args.node_modules.resolve(),
                "--browser", args.browser_executable.resolve(), "--output", workdir / "browser"],
                workdir, timeout=180)))
        else:
            check("browser-rendering")
    except Exception as error:
        report["scopes"]["fixture-preparation"] = {"status": "failed", "error": str(error)}
    finally:
        if cleanup:
            cleanup.cleanup()
    report["requested_checks_passed"] = all(x["status"] != "failed" for x in report["scopes"].values())
    if args.keep_workdir:
        report["retained_workdir"] = str(workdir)
    body = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(body, encoding="utf-8")
    print(body, end="")
    return 0 if report["requested_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
