# Task tools in Vault

Vault can hold useful scripts and small utilities produced for a task when they have no suitable home in another repository. Keep application code and its utilities in the owning code repo where one exists. Root `scripts/` is reserved for Vault's infrastructure.

## Location and ownership

- Put a task-only tool under `projects/<project-id>/tasks/<task-id>/tools/`. Create the folder only when there is a tool to retain.
- Reuse the existing task context and canonical tool. A revision does not need a new task, script copy, or separate tool document.
- Save useful deliverables rather than every temporary command or debugging experiment.
- A project can exist without a code repo. Choose its descriptor by the task's subject; do not place unrelated work in the Vault system project to manufacture a match. A requested standalone task can establish an appropriate project when it needs a new home.
- When several tasks need the same tool, link to its existing source. Move it to `projects/<project-id>/tools/` only when shared ownership is justified. Update current links and preserve historical commit references.

Suggested layout, with optional entries created only when needed:

```text
projects/<project-id>/tasks/<task-id>/
  context.md
  tools/
    build-report.py
    requirements.txt     Tool dependencies, if required
    tests/               Meaningful checks, if required
  outputs/               Regenerated results, ignored by default
  assets/                Results or fixtures deliberately retained
```

## Discover and run

Follow `CATALOG.md` to `PROJECT.md`, then its task index to the existing `context.md`. The context owns a **Tools** section with relative source links and run instructions. No separate tool catalogue, manifest, or README per script is required.

Record the details needed to use each tool:

| Detail | Required information |
| --- | --- |
| Purpose and source | What it does and a relative link to the canonical script. |
| Invocation | Exact command and working directory; include a dry-run option when the tool has one. |
| Dependencies | Runtime and packages or dependency-file link. State “standard library only” where applicable. |
| Inputs and outputs | Expected paths or formats and where results are written. |
| Effects | Files or external state it reads or changes; state “none” for effects that do not apply. |
| Evidence | Whether it is saved, executed, or checked; actual checks, date, environment, and revision where available. |

Keep entries brief. A small tool can use one table row and a short command block. Use paths relative to a stated working directory, or resolve resources relative to the script and accept input/output arguments. Avoid machine-specific paths in maintained run instructions.

Use the task's existing authorisation and session permissions when executing a tool. Inspect its source when behaviour or effects are unclear. Saving a script or documenting its command does not establish successful execution or correct results.

## Results and maintenance

- Link useful results from task context. Keep regenerated output under `outputs/`; retain material deliverables or small fixtures deliberately under `assets/` when they belong in Git.
- Keep dependency environments and bulky generated files out of maintained source. List tool-specific dependencies near the tool rather than adding them to Vault's infrastructure requirements.
- After changing a tool, run checks appropriate to its behaviour. Update the same context with observed results and remaining limits. Recheck affected claims rather than inheriting an earlier pass.
- Preserve the delivered tool contract and relevant source/check revisions in the existing completion checkpoint. Follow Vault's coordinated-writer rule when a tool is shared across tasks.
