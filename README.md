# Vault

Vault stores shared project documentation and task utilities in Markdown with local media. It contains no packaged skills or skill installer. Repository: [expiracy/vault](https://github.com/expiracy/vault).

## Find and update context

Read [AGENTS.md](AGENTS.md), then [CATALOG.md](CATALOG.md). Confirm the subject in `PROJECT.md` and follow its document/task indexes. Resume matching tasks and update owning documents. From another repository, supply Vault's location and suitable filesystem access.

| Document | Purpose |
| --- | --- |
| [Writing guide](projects/vault/guides/markdown-style.md) | Prose, structure and media conventions. |
| [Task tools guide](projects/vault/guides/task-tools.md) | Utility ownership and run instructions. |
| [CURRENT.md](CURRENT.md) | Observed state, evidence and limits. |
| [Maintained design](planning/docs-repo-design.md) | Layout, contracts and historical checkpoints. |
| [Research](research/existing-approaches.md) | Dated sources and comparisons. |

[Optional file metadata](planning/docs-repo-design.md#change-file-metadata) is designed; general parsing/removal and webpage syncing remain unimplemented.

## Repository checks

Use Python 3.10+ and PyYAML from `requirements.txt`. From the repository root:

```sh
python scripts/docs_repo.py catalog --check
python scripts/docs_repo.py check
python -m unittest discover -s tests -v
python scripts/test_integration.py --output /tmp/vault-integration.json
```

`catalog` without `--check` regenerates routing metadata after descriptor edits. `find QUERY` returns candidate projects; `--repository ID` narrows them. From another working directory, invoke the helper by absolute path. The bounded checker covers descriptors, catalogue and supported local Markdown/HTML links and anchors; remote URLs, rendering and implementation claims need separate checks.

## Integration checks

The [harness](scripts/test_integration.py) replays [isolated fixtures](tests/fixtures/integration/) for discovery, relocated links, design/recovery/history, task tools and diagram-source consistency. Results include checked scopes and input hashes; omitted scopes remain `not-checked`.

Optional live runs:

- `--agents --codex-bin PATH`: fresh Codex sessions; requires authentication/network and consumes account usage.
- `--browser --node PATH --node-modules PATH --browser-executable PATH`: requires Playwright and marked; its viewer loads Mermaid from the pinned CDN.

Fixture reports retain their original revisions and former installation evidence. See the [removal checkpoint](projects/vault/tasks/remove-skills/context.md) for the revised scope.
