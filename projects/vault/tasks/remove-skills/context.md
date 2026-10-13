# Remove Vault skills

Task: `remove-skills`. Started: 12 October 2026. Completed: 13 October 2026. Status: complete.

Requested deliverable: remove skills and their local installer from Vault. Keep project documentation, task tools, catalogue discovery and useful writing guidance. Preserve the accepted [file metadata description](../../../../planning/docs-repo-design.md#change-file-metadata).

Root is the sole writer of the implementation, maintained design, current-state record, guides, indexes and this context. The user explicitly requested that Vault contain no skills; this supersedes the installation component of the completed [setup-remediation task](../setup-remediation/context.md), whose historical evidence remains intact.

## Implementation plan

Goal: make Vault a documentation and task-tool repository without packaged skills or an installer.

Architecture: retain the existing catalogue and consistency helper. Move writing and task-tool references into ordinary project guides, remove skill installation code, and let isolated integration sessions consume normal documents.

Tech stack: existing Python 3.10+ scripts and PyYAML; Markdown guidance. No new dependency or global configuration changes.

- [x] Establish the baseline: 49 tests ran, 35 passed and 14 Windows installer tests were skipped on macOS.
- [x] Change `tests/test_integration.py` to replay a checkout without `.agents`; run it before modifying the harness and confirm the missing dependency causes failure.
- [x] Move both reference guides to `projects/vault/guides/`; delete both `SKILL.md` files, `scripts/install-local.ps1` and `tests/test_install_local.py`. Update `scripts/test_integration.py` and the seed fixture's `AGENTS.md` to use plain guidance; remove installed-file and skill-bootstrap checks and their tests.
- [x] Update `AGENTS.md`, `README.md`, `CURRENT.md`, `PROJECT.md`, the generated catalogue and the maintained design. Preserve historical checkpoints and use historical commit links for removed sources.
- [x] Run the remaining unit suite, catalogue/link checks, whitespace checks and offline replay. Record a completion checkpoint; leave browser and paid live-agent runs unchecked.

## Progress and next action

The regression check first failed because replay attempted to copy the omitted `.agents/skills` directory. After removing that dependency, all nine remaining integration tests passed. Both reference guides were preserved byte-for-byte at their new paths. No `docs-context` or `write-project-doc` user-skill links exist on this Mac. The full 34-test suite, catalogue/link checks, offline replay and whitespace checks passed. Independent read-only review found two stale descriptions; both were corrected, and the reviewer reported no remaining actionable findings. The removal work is complete; publication was subsequently authorised below.

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
