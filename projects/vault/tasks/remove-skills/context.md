# Remove Vault skills

Task: `remove-skills`. Started: 12 October 2026. Completed: 13 October 2026. Status: complete.

Deliverable: remove Vault's skills/installer; retain documentation, task tools, catalogue and writing guidance, including the [accepted metadata design](../../../../planning/docs-repo-design.md#change-file-metadata). Root owned code/shared docs and this context. This supersedes the [setup task's](../setup-remediation/context.md) installation component; its evidence remains historical.

## Implementation plan

Completed with existing Python 3.10+/PyYAML and Markdown, without new dependencies or global configuration changes:

- [x] Baseline: 49 tests, 35 passed, 14 Windows installer skips on macOS.
- [x] Regression first failed when integration replay omitted `.agents`.
- [x] Move both guides to `projects/vault/guides/`; remove skill manifests, `scripts/install-local.ps1` and installation tests. Revise harness, seed instructions and tests to consume ordinary guidance.
- [x] Update operating docs, indexes, catalogue and design; preserve historical checkpoints and exact removed-source commit links.
- [x] Run unit, catalogue/link, offline replay and whitespace checks; record scope/limits below.

## Progress and next action

All 34 remaining tests, including nine integration tests, passed. Guides matched their source bytes at removal; no Vault user-skill links were present on this Mac. Independent review found two stale descriptions, both corrected, with no remaining actionable findings. Removal is complete; the publication follow-up is below. Fresh live-agent/browser runs were excluded.

## Completion checkpoint: remove-skills

Recorded: 13 October 2026. Delivered: removal of `.agents/skills/`, the empty `.agents/` directory, `scripts/install-local.ps1` and its installation-only tests. Writing and task-tool references moved unchanged to `projects/vault/guides/`. Operating guidance, current summaries, project index and catalogue now describe ordinary documents. The integration harness and seed fixture consume those guides; installed-file and skill-bootstrap checks are removed.

Design basis: Vault is a central repository for documentation and task tools, with no packaged skills or skill installer. Existing discovery and consistency helpers remain. The earlier accepted optional YAML metadata description is preserved, with parsing/removal and webpage syncing still pending. Historical delivery records and hashes remain intact; links to removed sources use GitHub paths at baseline commit `0001181ef771face3a4c2a7e4287bfc304e6b603`. At this checkpoint the edits were local and uncommitted.

Checks: 34 tests passed with no skips, after a regression test first failed on the obsolete skill-directory dependency and then passed. Catalogue consistency, descriptors, supported local links, offline routing/history, the JSON task tool, media-source portability and Git whitespace checks passed. Review confirmed both guides match their baseline bytes and found no remaining runtime blockers.

Run from the Vault root with Python 3.10+ and PyYAML from `requirements.txt`:

```sh
python -m unittest discover -s tests -v
python scripts/docs_repo.py catalog --check
python scripts/docs_repo.py check
python scripts/test_integration.py --output /tmp/vault-without-skills-integration.json
git diff --check
```

The actual local checks used bundled Python 3.12.14 and PyYAML 6.0.3 from `/private/tmp/vault-metadata-check-libs` through `PYTHONPATH`. The compact report at `/private/tmp/vault-without-skills-integration.json` records current input hashes and checked scopes; older reports remain historical.

Limits: fresh live-agent and browser checks were not rerun. Metadata parsing/removal and webpage syncing were not implemented. No global configuration or installations on other machines were changed; former user-skill links elsewhere may need cleanup when those checkouts are updated. At the original completion checkpoint, no commit or push had been requested or performed.

## Publication follow-up

13 October 2026: the user authorised committing and pushing the removal and metadata documentation to `origin/master`. All 34 remaining tests and the descriptor/catalogue/local-link check passed again before publication. This follow-up reuses the completed task context and preserves its original delivery checkpoint.
