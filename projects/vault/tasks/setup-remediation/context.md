# Vault setup remediation

Task: `setup-remediation`. Started/completed: 11 October 2026. Status: complete. Historical setup; its skills/installer were superseded by the [removal task](../remove-skills/context.md). GitHub visibility changed to public separately on 12 October 2026.

Deliverable: fix six setup-review findings, repeat checks and commit authorised changes. [Maintained design](../../../../planning/docs-repo-design.md); original delivery/evidence remains below.

## Scope and ownership

Root owned shared docs and Git. Installer agent: `scripts/install-local.ps1`, `tests/test_install_local.py`; helper agent: `scripts/docs_repo.py`, `tests/test_docs_repo.py`; integration agent: fixtures/harness. Contributors used messages for shared-doc changes and did not stage/commit.

Findings: relocated launchers, partial installer writes, stale desktop/current-state paths, uncommitted setup, escaped-Markdown false link failures and temporary-only evidence. Existing style/relocation/tool work was preserved; `.ultracode/` was excluded. The user authorised the original private `expiracy/vault` backup; `origin/master` matched the implementation revision at that delivery.

## Progress and next action

All six repairs were delivered. Original result: 49 tests, 48 passed, one Windows symlink-privilege skip. Live installer passed twice; browser and five isolated agent roles passed with the recorded audit/runtime limitations. Chats and sidebar paths were corrected, original archive state preserved, empty old root removed. Clean-checkout replay and all 23 relevant input-hash comparisons passed. No original repair work remains; recheck affected scopes when sources/environments change.

## Tools and checks

Vault infrastructure is kept in root `scripts/`; these tools support the maintained repository rather than a task-only utility. Run the following from `C:/Users/james/Documents/repos/vault` with Python 3.14.3 and PyYAML 6.0.3:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe scripts/docs_repo.py catalog --check
.\.venv\Scripts\python.exe scripts/docs_repo.py check
.\.venv\Scripts\pip.exe check
.\.venv\Scripts\python.exe scripts/test_integration.py --installed-user-dir C:/Users/james --output "$env:TEMP\vault-integration.json"
```

The [consistency helper](../../../../scripts/docs_repo.py) reads descriptors and supported links; `catalog` without `--check` rewrites only the generated catalogue. The [historical installer](https://github.com/expiracy/vault/blob/0001181ef771face3a4c2a7e4287bfc304e6b603/scripts/install-local.ps1) updates the selected user directory's managed startup block, root pointer and skill links. Its [historical tests](https://github.com/expiracy/vault/blob/0001181ef771face3a4c2a7e4287bfc304e6b603/tests/test_install_local.py) use isolated temporary directories and simulate failed writes, late file locks, fresh-install cleanup and dangling-link rollback. The real installation was rerun idempotently in this task.

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

[Git attributes](../../../../.gitattributes) keep canonical text at LF and preserve retained fixture bytes. This prevents Windows checkout conversion from invalidating the historical hash manifest; the original tool and JSON fixture retain their recorded CRLF bytes. A clean-checkout replay verified this with `core.autocrlf=true`.

## Completion checkpoint: setup-remediation

Recorded: 11 October 2026. Delivered: all six review findings, the fresh setup checks and the requested commit. The user additionally authorised the private backup; the implementation commit and prior history have been pushed.

| Finding | Delivered result and verification |
| --- | --- |
| Moved Python launchers | Regenerated activation scripts and pip launchers at Vault's path, using CPython 3.14.3 and bundled pip 25.3; PyYAML 6.0.3 remains available and `pip check` passes. The ignored environment is local; tracked requirements and setup instructions support recreation. |
| Installer partial failure | Staged publication with rollback restores files and both skill links after late failures, including dangling links. Fourteen installer tests pass; the live installation passed twice with unrelated startup content and canonical sources preserved. |
| Stale desktop paths | Current and original setup chats use Vault. The original chat remained archived and no turn started. The verified empty old root was deleted. User confirmation and a subsequent API list establish removal of the obsolete desktop entry. |
| Uncommitted setup and no remote | Prior writing-style, relocation and task-tool changes are preserved in the implementation commit. Private GitHub `origin` and tracking branch are configured; the remote implementation hash matches local Git. |
| Escaped Markdown false positives | Escaped brackets, code in link labels and literal destination backticks are handled within the documented syntax scope. Twenty-four helper tests pass; the privileged file-symlink test is skipped. |
| Temporary-only integration evidence | A resettable fixture, replay harness, historical hash manifest, current compact reports and screenshot are retained. Ten harness tests, current-source browser/installation checks, five live roles with a later aggregate audit, and clean-checkout replay pass within their recorded scopes. |

Implementation and initial documentation revision: [7e5ffc3716c360e6e1d1641e0904418df056e5cd](https://github.com/expiracy/vault/commit/7e5ffc3716c360e6e1d1641e0904418df056e5cd). Code paths: `scripts/docs_repo.py`, `scripts/install-local.ps1`, `scripts/test_integration.py` and `tests/`. Documentation paths: `planning/docs-repo-design.md`, `CURRENT.md`, `projects/vault/PROJECT.md` and the canonical skills. This checkpoint is a later documentation update; earlier completed checkpoints remain intact.

Final unit result: 49 tests run, 48 passed, one privilege skip. Both manifests validate; catalogue, supported links, dependencies and staged whitespace checks pass. A clean local Git clone at the exact implementation revision, checked out with `core.autocrlf=true`, passed catalogue, supported links and offline integration using the documented Python/PyYAML runtime and no untracked fixture or source files; all relevant input hashes remain identical. GitHub privacy and default branch were verified separately, and `git ls-remote` matched the pushed implementation hash.

Material decisions: retain configuration and skill names for compatibility; use reversible installer staging rather than changes to global permissions; preserve historical fixture bytes; retain scoped evidence rather than treating design delivery as runtime implementation. The earlier in-flight driver and copied helper are distinguished from the later current-source audit in the retained report.

Limits: the Windows file-symlink privilege remains unavailable. Installer rollback does not cover abrupt termination or independently failed rollback. Agent coordination is cooperative. The media check covers the custom Chrome viewer; Codex/GitHub rendering and other hosts are unverified. The live fixture's PyYAML limitation and the final guard scope are described above. These limits do not leave any of the six authorised repairs unfinished.

Next action: no remaining task work. Recheck affected scopes when source or environment changes; future project work adds appropriate descriptors and reuses maintained documents.
