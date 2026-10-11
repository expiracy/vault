# Vault

Vault is one central repository for project documentation and task tools used by agents across projects. Documents use Markdown with local images and diagrams. Useful task scripts can live here when they have no suitable home in another repo. [CURRENT.md](CURRENT.md) records the implementation and verification scope.

Current records:

- [Agent documentation maintenance rules](AGENTS.md)
- [Writing style guide](.agents/skills/write-project-doc/references/markdown-style.md)
- [Task tools: storage and run instructions](.agents/skills/docs-context/references/task-tools.md)
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

The installer adds a managed block to `~/.codex/AGENTS.md`, stores the local root in `~/.agents/agent-docs.json`, and links the two user skills to their canonical repo directories. The configuration filename, `docs_root` key, and skill names are retained for compatibility. It preserves unrelated instructions and configuration and refuses conflicting skill destinations. `-UserDirectory PATH` supports isolated installation tests. The Windows installer uses directory junctions; other platforms can create symlinks in their user skill directory and the equivalent pointer/configuration.

The installer stages new files and junctions before publishing them and restores the previous files and links if a runtime operation fails. Read-only destination files are rejected before mutation. Abrupt termination or power loss is outside this guarantee; if rollback itself fails, the error identifies retained recovery backups.

After an authorised folder move, run the installer from the new location with `-PreviousDocsRoot PATH` set to the exact former root. This retargets the matching configuration and managed skill links; it does not move the checkout or update Codex's saved project path.

Recreate the Python environment at the new path after a checkout move. Activation scripts and package launchers can retain the former interpreter path even when `python.exe` still works. Keep `requirements.txt` as the dependency source rather than treating a moved `.venv` as portable.

From any working directory, invoke the helper using its absolute path. `find QUERY` returns candidate projects; use `--repository ID` when useful. `catalog --check` detects stale routing metadata without rewriting files. `check` validates descriptors, the generated catalogue, and supported local Markdown/HTML links and anchors. It does not verify remote URLs, rendering, or implementation claims; `--help` describes the syntax scope.

The startup pointer and user skills expose the repository to agents. Each session still needs filesystem access to read or edit it. For a CLI session, grant the central repo through the supported `--add-dir` option when needed. Do not assume discovery creates permission. [Codex instruction loading](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [user skill discovery](https://learn.chatgpt.com/docs/build-skills).

## Repeat integration checks

The retained [integration harness](scripts/test_integration.py) and [fixtures](tests/fixtures/integration/) replay project discovery, relocated links, saved design and recovery states, task history, task-tool behaviour, and diagram-source consistency in an isolated scratch repository:

```powershell
.\.venv\Scripts\python.exe scripts/test_integration.py --output "$env:TEMP\vault-integration.json"
```

Add `--installed-user-dir` with the intended user directory to inspect the actual pointer and skill links without editing them. `--agents --codex-bin` with an executable path runs five fresh Codex sessions for startup, design, recovery, contributions, integration and writer handoff. It requires authentication and network access and uses account usage. `--browser` also requires `--node`, `--node-modules` containing Playwright and marked, and `--browser-executable`; its custom viewer loads Mermaid 12.1.0 from a pinned CDN URL.

Each result records the checked scopes and source hashes. Optional checks remain `not-checked` when omitted. The default fixture replay does not establish fresh-agent behaviour or viewer rendering. [Setup remediation context](projects/vault/tasks/setup-remediation/context.md) records commands, retained results, and the final validation scope.
