# Vault

Vault is a central repository for project documentation and task tools used across projects. Documents use Markdown with local images and diagrams. Useful task scripts can live here when they have no suitable home in another repository.

Current records:

- [Documentation maintenance rules](AGENTS.md)
- [Writing style guide](projects/vault/guides/markdown-style.md)
- [Task tools: storage and run instructions](projects/vault/guides/task-tools.md)
- [Current state and evidence](CURRENT.md)
- [Existing approaches and sources](research/existing-approaches.md)
- [Project catalogue](CATALOG.md)
- [Maintained design and historical checkpoints](planning/docs-repo-design.md)

Project frontmatter owns discovery metadata; the helper generates the catalogue. Read `CATALOG.md`, confirm the relevant project through its `PROJECT.md`, and follow its document and task indexes. Supply Vault's location through the session when working from another repository. Vault contains no packaged agent skills or local skill installer.

The repository is public at [expiracy/vault](https://github.com/expiracy/vault). Current-state records distinguish delivered behaviour from accepted designs and preserve the scope of earlier checks. Optional file metadata is described in [Change file-metadata](planning/docs-repo-design.md#change-file-metadata); general parsing/removal and webpage syncing remain unimplemented.

## Repository checks

The optional helper scripts need Python 3.10 or later and PyYAML, as listed in `requirements.txt`. From the repository root, use a Python environment with those dependencies:

```sh
python scripts/docs_repo.py catalog --check
python scripts/docs_repo.py check
python -m unittest discover -s tests -v
```

Invoke the helper by its absolute path from another working directory. `find QUERY` returns candidate projects; `--repository ID` can narrow the search. `catalog --check` detects stale routing metadata; `catalog` regenerates it after authorised descriptor edits. `check` validates descriptors, the generated catalogue and supported local Markdown/HTML links and anchors. These checks do not verify remote URLs, rendering or implementation claims.

## Integration checks

The [integration harness](scripts/test_integration.py) and [fixtures](tests/fixtures/integration/) replay discovery, relocated links, saved design/recovery states, task history, task-tool behaviour and diagram-source consistency in an isolated scratch repository:

```sh
python scripts/test_integration.py --output /tmp/vault-integration.json
```

Optional `--agents --codex-bin PATH` runs fresh Codex sessions using ordinary workspace instructions and copied guides. It needs authentication and network access and consumes account usage. Optional `--browser` requires `--node`, `--node-modules` containing Playwright and marked, and `--browser-executable`; its custom viewer loads Mermaid from the existing pinned CDN URL.

Results record the checked scopes and input hashes. Omitted live-agent and browser checks remain `not-checked`. Historical results in the fixtures describe their original revisions, including the former skill installation. [Remove-skills context](projects/vault/tasks/remove-skills/context.md) records the revised scope and checks.
