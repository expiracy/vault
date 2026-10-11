# Vault setup remediation

Task: `setup-remediation`. Started: 11 October 2026. Status: in progress.

Requested deliverable: fix the six findings from the Vault setup review, test the setup again, and commit the existing and new authorised changes. The maintained design remains [Vault design](../../../../planning/docs-repo-design.md).

## Scope and ownership

Root coordinates this task and is the sole writer of the maintained design, current-state record, README, project index, and this context. The installer agent owns `scripts/install-local.ps1` and `tests/test_install_local.py`; the helper agent owns `scripts/docs_repo.py` and `tests/test_docs_repo.py`; the integration agent owns new reusable test fixtures and the integration harness. Contributions to shared documents go to root by message. Subagents do not stage or commit files; root owns Git operations.

The six findings are: relocated Python launchers retaining the old path; installer write failures leaving inconsistent links and configuration; obsolete desktop project and stale current-state text; uncommitted setup changes; false link-check failures for escaped Markdown; and temporary-only integration evidence.

Existing style, relocation, and task-tool changes must be preserved. The unrelated `.ultracode/` directory is outside this task's commit. The user authorised creating a private GitHub repository named `vault`. [expiracy/vault](https://github.com/expiracy/vault) has been created and verified private; `origin` points to it. Commit and push verification remain pending.

## Progress and next action

The relocated environment, helper and installer are repaired. The live installer passed twice and retained unrelated startup instructions. The final integrated suite ran 49 tests: 48 passed and one Windows file-symlink test was skipped for missing privilege. Both skill manifests, catalogue consistency, supported links and dependency checks passed.

The original setup chat's saved folder now points to Vault, with its original archive state restored and no turn started. The verified empty former directory has been removed. The user confirmed the obsolete `docs` desktop entry is gone from the sidebar; the subsequent project-list API check also returned Vault without the obsolete entry.

The retained browser run passed. Five fresh isolated design, recovery, contributor, integration and handoff sessions completed successfully. An independent aggregate final-fixture audit passed the strengthened state and file-scope checks, and the current helper passed against their output. Root independently confirmed that both retained reports match all 23 relevant current input hashes. Root will commit only the authorised files, replay a clean checkout, push the private backup, and verify the remote revision.

## Tools and checks

Vault infrastructure is kept in root `scripts/`; these tools support the maintained repository rather than a task-only utility. Run the following from `C:/Users/james/Documents/repos/vault` with Python 3.14.3 and PyYAML 6.0.3:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe scripts/docs_repo.py catalog --check
.\.venv\Scripts\python.exe scripts/docs_repo.py check
.\.venv\Scripts\pip.exe check
.\.venv\Scripts\python.exe scripts/test_integration.py --installed-user-dir C:/Users/james --output "$env:TEMP\vault-integration.json"
```

The [consistency helper](../../../../scripts/docs_repo.py) reads descriptors and supported links; `catalog` without `--check` rewrites only the generated catalogue. The [installer](../../../../scripts/install-local.ps1) updates the selected user directory's managed startup block, root pointer and skill links. Its [tests](../../../../tests/test_install_local.py) use isolated temporary directories and simulate failed writes, late file locks, fresh-install cleanup and dangling-link rollback. The real installation was rerun idempotently in this task.

The [integration harness](../../../../scripts/test_integration.py) copies [retained synthetic fixtures](../../../../tests/fixtures/integration/) into isolated temporary directories, runs the helper and the fixture's JSON tool, and writes a JSON result. It does not edit live documentation or global installation. Optional agent sessions consume account usage and require network access; optional browser rendering requires Node, Playwright, marked, Chrome and the pinned Mermaid CDN. Omitted scopes remain `not-checked`. Raw diagnostic transcripts and temporary absolute paths are not required for offline replay.

Optional checks used these installed runtime paths; update them if the local runtime changes. Run from the same Vault working directory:

```powershell
$vaultCodex = 'C:\Users\james\AppData\Local\OpenAI\Codex\bin\2e5e00daee91c61d\codex.exe'
$vaultNode = 'C:\Users\james\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe'
$vaultModules = 'C:\Users\james\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules'
$vaultChrome = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
.\.venv\Scripts\python.exe scripts/test_integration.py --installed-user-dir C:/Users/james --agents --codex-bin $vaultCodex --output "$env:TEMP\vault-agents.json"
.\.venv\Scripts\python.exe scripts/test_integration.py --installed-user-dir C:/Users/james --browser --node $vaultNode --node-modules $vaultModules --browser-executable $vaultChrome --output "$env:TEMP\vault-browser.json"
```

The checked CLI is `0.162.0-alpha.17.2`; browser dependencies are Node 24.19.0, Playwright 1.62.1, marked 17.0.5, Chrome 155.0.8059.39 and Mermaid 12.1.0. Add `--keep-workdir` with a new, nonexistent directory only when retaining the synthetic output is useful; the default cleans its scratch directory and retains the requested JSON report.

Retained results: [offline, installed files and browser](../../../../tests/fixtures/integration/results/offline-browser.json), [fresh agents](../../../../tests/fixtures/integration/results/fresh-agents.json), and [browser screenshot](../../../../tests/fixtures/integration/results/workflow.png). Source hashes in each result establish its checked inputs independently of later document edits.

The five live sessions ran the earlier loaded harness and an earlier copied helper. Their original checks covered recovery equality, contributor preservation of shared files, protected source/history and the completed filter context. A separate post-run comparison checked the whole final fixture, both explicit proposal states and the current helper. The report preserves used-source hashes and current audit hashes. The new per-role allowlists were tested with negative cases; they were not retroactively executed inside the already-running sessions.

The synthetic sessions' default Python lacked PyYAML, so agent-authored contexts record fallback structural checks and that limitation. Driver and post-run checks used the repaired Vault environment and passed. Future fixture startup guidance identifies the harness's PyYAML-capable interpreter. This does not establish arbitrary viewers, agents or permission configurations.

[Git attributes](../../../../.gitattributes) keep canonical text at LF and preserve retained fixture bytes. This prevents Windows checkout conversion from invalidating the historical hash manifest; the original tool and JSON fixture retain their recorded CRLF bytes. A clean-checkout replay will verify this before delivery.
