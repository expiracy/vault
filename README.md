# Shared agent documentation

This project is being planned as one central documentation repository that agents can use across projects. Documents will use Markdown with local images and diagrams.

Current records:

- [Agent documentation maintenance rules](AGENTS.md)
- [Current state and evidence](CURRENT.md)
- [Existing approaches and sources](research/existing-approaches.md)
- [Proposed repository and skills](planning/docs-repo-design.md)

The revised design defines maintained feature documents, change states, task completion checkpoints, and coordination for shared edits. Local operating rules are recorded in `AGENTS.md`. The catalogue, skills, helper scripts, and cross-project discovery configuration described in the design have not been implemented.

The documentation is now committed to local Git history. An isolated agent pilot exercised in-place design updates, acceptance without implementation, scoped partial results, historical retrieval, and recovery by a fresh agent. The [current-state record](CURRENT.md) links to the evidence and remaining setup gaps. These tests used manually routed fixture documents, without installed documentation skills or automatic discovery.

The current-state record describes what exists and what has been checked. The design describes possible future behaviour. Accepting a design would settle the intended direction but would not establish that it had been implemented or verified.
