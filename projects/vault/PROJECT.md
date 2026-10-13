---
name: vault
description: >-
  Vault's project documentation, task tools, catalogue, maintenance rules and
  writing guidance. Use for work on Vault or its shared documentation workflow.
aliases: [agent-docs, shared-docs, docs-repo]
repositories: [https://github.com/expiracy/vault]
---

# Vault

Owns the shared documentation/task-tool system. Other subjects, including work without a code repo, use their own project descriptors.

| Document | Owns |
| --- | --- |
| [CURRENT.md](../../CURRENT.md) | Observed state and evidence. |
| [Maintained design](../../planning/docs-repo-design.md) | Layout/contracts and historical checkpoints. |
| [Research](../../research/existing-approaches.md) | Dated source comparisons. |
| [AGENTS.md](../../AGENTS.md) | Maintenance and coordination rules. |
| [Writing guide](guides/markdown-style.md) | Prose, structure and media. |
| [Task tools guide](guides/task-tools.md) | Utility storage and execution. |

Task records:

- [Setup remediation](tasks/setup-remediation/context.md): six findings repaired; original checks and publication.
- [File metadata](tasks/file-metadata/context.md): optional YAML design; parsing/removal and webpage sync remain unimplemented.
- [Remove skills](tasks/remove-skills/context.md): packaged skills/installer removed; guides and checks retained.
- [External document skills](tasks/external-document-skills/context.md): writing-guide consolidation, concise repository docs and external UML skill; no packaged Vault skills.

Reuse matching task contexts and maintained designs. Create separate records only for distinct authorised scope needing a home.
