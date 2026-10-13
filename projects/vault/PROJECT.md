---
name: vault
description: >-
  Vault's shared project documentation, discovery, task context, writing guidance,
  and task-tool conventions. Consult when building or using Vault, its catalogue,
  documentation conventions, or storage for standalone task utilities.
aliases: [agent-docs, shared-docs, docs-repo]
repositories: [https://github.com/expiracy/vault]
---

# Vault

This project owns Vault's documentation and task-tool system. Other subjects have their own project descriptors, including work with no code repository.

- Current capabilities and evidence: [CURRENT.md](../../CURRENT.md)
- Maintained system design and historical checkpoints: [docs repo design](../../planning/docs-repo-design.md)
- Research: [existing approaches](../../research/existing-approaches.md)
- Local maintenance rules: [AGENTS.md](../../AGENTS.md)
- Writing style: [style guide](guides/markdown-style.md)
- Task-owned utilities: [task tools guide](guides/task-tools.md)

Task records:

- [Setup remediation](tasks/setup-remediation/context.md): repair the six setup-review findings, repeat the setup checks, and commit the authorised changes.
- [File metadata](tasks/file-metadata/context.md): completed design description for optional YAML frontmatter; parsing/removal support and webpage syncing remain unimplemented.
- [Remove skills](tasks/remove-skills/context.md): remove packaged skills and the installer while retaining ordinary guides and repository checks.
- [External document skills](tasks/external-document-skills/context.md): documentation writing style and canonical UML diagram assets through external skills; Vault stays Markdown and contains no packaged skills.

Use those documents for current work on this system. Additional feature documents and task contexts are created only when separate authorised scope needs an appropriate home. Follow-ups to the existing system design update it in place.
