# Shared agent documentation

This is one central documentation repository for agents working across projects. Documents use Markdown with local images and diagrams. The core catalogue and skills are implemented; [CURRENT.md](CURRENT.md) records their verification scope.

Current records:

- [Agent documentation maintenance rules](AGENTS.md)
- [Current state and evidence](CURRENT.md)
- [Existing approaches and sources](research/existing-approaches.md)
- [Project catalogue](CATALOG.md)
- [Maintained repository design and checkpoints](planning/docs-repo-design.md)

The design defines maintained feature documents, separate change states, task completion checkpoints, and coordination for shared edits. Local operating rules are in `AGENTS.md`. Project frontmatter owns discovery metadata; the helper generates the catalogue. The two skills are maintained in `.agents/skills/` and can be linked into user scope for other projects.

The initial documentation and first isolated pilot are committed to local Git history. That earlier pilot tested the rules before the catalogue and skills existed. The current-state record distinguishes it from the subsequent full integration tests.

The current-state record describes what exists and what has been checked. Maintained designs distinguish current behaviour from identified changes. Accepting a design does not establish implementation or verification.

## Set up and check

Use Python 3.10 or later. On Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts/docs_repo.py catalog
.\.venv\Scripts\python.exe scripts/docs_repo.py check
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\scripts\install-local.ps1
```

The installer adds a managed block to `~/.codex/AGENTS.md`, stores the local root in `~/.agents/agent-docs.json`, and links the two user skills to their canonical repo directories. It preserves unrelated instructions and configuration and refuses conflicting skill destinations. `-UserDirectory PATH` supports isolated installation tests. The Windows installer uses directory junctions; other platforms can create symlinks in their user skill directory and the equivalent pointer/configuration.

From any working directory, invoke the helper using its absolute path. `find QUERY` returns candidate projects; use `--repository ID` when useful. `catalog --check` detects stale routing metadata without rewriting files. `check` validates descriptors, the generated catalogue, and supported local Markdown/HTML links and anchors. It does not verify remote URLs, rendering, or implementation claims; `--help` describes the syntax scope.

The startup pointer and user skills expose the repository to agents. Each session still needs filesystem access to read or edit it. For a CLI session, grant the central repo through the supported `--add-dir` option when needed. Do not assume discovery creates permission. [Codex instruction loading](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [user skill discovery](https://learn.chatgpt.com/docs/build-skills).
