# Optional file metadata

Task: `file-metadata`. Started and completed: 12 October 2026. Status: complete.

Requested deliverable: describe support for optional YAML metadata about an individual file, including an associated webpage, with straightforward parsing and removal. This is documentation work; implementation was not requested.

Maintained design: [Change file-metadata](../../../../planning/docs-repo-design.md#change-file-metadata). Root is the sole writer of this context, the maintained design and the project index. This extends the system documented by the completed [setup-remediation task](../setup-remediation/context.md) without changing its historical scope.

## Progress and next action

The requirement and example are recorded in the maintained design and linked from the [project index](../../PROJECT.md). Decision: `accepted`; implementation: `not-started`; verification: `not-checked`. No remaining documentation work; implement parsing/removal or webpage syncing only when requested.

## Completion checkpoint: file-metadata

Recorded: 12 October 2026. Delivered: the requested design description in `planning/docs-repo-design.md`, its project-index entry, and this task record. The source baseline was Vault commit `0001181`; at this checkpoint the documentation edits were local and uncommitted.

Design basis: the user accepted frontmatter for file metadata, including a webpage association, and requested support when present with easy parsing and removal. The description keeps ordinary document frontmatter optional, retains mandatory project descriptors, requires safe YAML parsing, preserves the body exactly when stripping metadata, and reports malformed or unclosed blocks instead of discarding content. It records sync intent without claiming an implemented sync mechanism.

Checks: `scripts/docs_repo.py --root /Users/jgray/Documents/vault check` passed for descriptors, catalogue and supported local links. The check used bundled Python 3.12 and PyYAML 6.0.3 installed temporarily under `/private/tmp/vault-metadata-check-libs`, supplied through `PYTHONPATH`; the checkout has no local Python environment. Whitespace checks passed before this checkpoint and are repeated for the final files.

Limits: documentation consistency does not verify parsing/removal behaviour, webpage sync, remote URLs or rendering. Those behaviours remain unimplemented and unchecked.

## Publication follow-up

13 October 2026: the user authorised committing and pushing this description together with the [skills removal](../remove-skills/context.md). Publication does not change the metadata change's implementation or verification states.
