# Proposed central documentation repository

Status: revised design draft. Updated: 11 October 2026.

Present-state evidence is recorded separately in [CURRENT.md](../CURRENT.md). At this point, the project contains research and planning documents. The catalogue, project descriptors, skills, helper scripts, and cross-project discovery integration are proposed. They have not been implemented by this project.

Confirmed requirements:

- One central docs repository with subfolders accessible to agents working across projects.
- Folder descriptions that help agents find relevant context, similar to skill descriptions.
- Readable records of current task context and progress for user audit.
- Skills for producing documents in the user's preferred style.
- Markdown documents with images and diagrams.
- Update appropriate existing documents to reflect new information by default. Create a new document only when explicitly requested or when requested work or an agreed workflow needs a document with no appropriate existing home.

The five reviewed issues are now resolved in the document roles and workflow below. Their operating rules are recorded in [AGENTS.md](../AGENTS.md) for this workspace. The wider repository structure, catalogue, skills, and cross-project integration still require implementation and a pilot. Resolving a design issue does not establish that the corresponding runtime capability exists.

## Document maintenance rule

The default is to update the appropriate existing document. Read the relevant files first, integrate new information into the maintained account, and correct outdated statements throughout the affected document. Update its status, evidence, and links consistently. Appending a correction while leaving a conflicting claim elsewhere does not make the document correct.

Create a new document only when the user explicitly requests one, or when requested work or an agreed workflow needs a document with no appropriate existing home. A changed requirement, new finding, or revision ordinarily belongs in the existing document. Avoid dated replacements, numbered copies, and supplementary files created solely for updates. Supporting images and diagram assets can still be added when needed.

The future `docs-context` and `write-project-doc` skills must follow this rule. Their templates describe a document's shape when one is needed, rather than requiring a new file for every invocation. A distinct authorised task may need one context record; subsequent messages, findings, and revisions update that record. Extending a feature reuses its maintained design.

## Recommended approach

Build a small convention around ordinary files. Reuse the central-store idea from [OpenSpec](https://github.com/Fission-AI/OpenSpec/blob/main/docs/stores-beta/user-guide.md), description-based selection from [Kiro](https://kiro.dev/docs/steering/), and current-context summaries from [Memory Bank](https://github.com/cline/cline/blob/main/docs/best-practices/memory-bank.mdx). Keep the custom work focused on discovery, task state, and writing style.

The initial project can work directly from local files. A service, semantic database, website, and full specification framework can be considered later if a demonstrated need appears.

## Proposed layout

```text
docs/
  README.md                         Human introduction
  AGENTS.md                         Instructions for working inside this repo
  CATALOG.md                        Generated project descriptions and links
  projects/
    <project-id>/
      PROJECT.md                    Project description and document/task index
      current.md                    Project-level facts and links to feature facts
      features/                     Maintained feature documents, when needed
        <feature-id>.md             Current design and separately labelled changes
        assets/<feature-id>/        Feature images and diagram sources
      tasks/
        <task-id>/
          context.md                Current state and next action
          progress.md               Milestone history, when needed
          research.md               Sources and findings, when needed
          design.md                 Only for a separately needed/requested design
          assets/                   Images and editable diagram sources
      decisions/                    Significant lasting decisions, when needed
      guides/                       Maintained project guides, when needed
  .agents/
    skills/
      docs-context/
        SKILL.md
      write-project-doc/
        SKILL.md
        references/                 Writing style and document conventions
        assets/                     Templates
  scripts/                          Catalogue generation and consistency check
```

Use existing documents when they already serve the purpose. Only create optional documents and folders when separate content warrants them or the user requests them. A small task can use one `context.md` with its requested deliverable, goal, progress, and next action. Larger work can link to existing research and design documents or create distinct ones where needed. A project can exist before any code repository exists.

These paths are defaults for documents without an existing home. Keep suitable existing documents at their current paths and index them. The current planning document remains this project's design home while it is being refined. Do not move or copy it just to match the suggested layout.

## Maintained designs and task records

Each feature has one maintained design home when it needs documentation. Prefer its existing suitable document. Otherwise use `features/<feature-id>.md`, with a stable identifier, short description, current design, and individually identified changes. A small project may keep one existing project design instead of creating separate feature files.

`PROJECT.md` links to these maintained documents and task contexts. Its feature entries identify the subject and document path; task entries identify the task, requested deliverable, and context path. Detailed facts and task status remain in their owning documents rather than being copied into the index.

| Document | Owns | Links to |
| --- | --- | --- |
| `PROJECT.md` | Project discovery, scope, and routing. | Relevant feature designs, task contexts, and project facts. |
| Maintained feature or project design | Detailed current design, evidence for feature claims, proposed changes, and material design rationale. | Originating tasks, decisions, source files, and checks. |
| `current.md` | Project-level environment or integration facts, with evidence. | Feature facts at their canonical design sections. |
| Task `context.md` | Requested deliverable, scope, progress, next action, and historical completion checkpoints. | Maintained design and stable change identifiers. |
| Existing decision records | Significant decision context, rationale, and supersession history. | Affected designs and tasks. |

Task-specific designs are optional. Use one when the user requests a separate document or the task needs a distinct design with no suitable existing home, such as a cross-project change. In that case, the task design owns the detailed proposal, and affected feature documents link to it instead of reproducing it. Once implementation is checked, integrate the resulting current facts into their maintained feature documents and retain the proposal's history through its task checkpoint.

## Folder descriptions and catalogue

Each project folder carries its own canonical descriptor in `PROJECT.md`. Use frontmatter for a stable name and a short description of the context and when to consult it. Repository identities and aliases are optional routing aids. The body is the maintained project overview, with scope, constraints, and links to relevant documents.

An illustrative descriptor for this documentation project:

```yaml
---
name: agent-docs
description: >-
  Central agent documentation, project discovery, task context, and Markdown
  writing conventions. Consult when designing or maintaining the shared docs
  repo or the skills that use it.
aliases: [shared-docs, docs-repo]
repositories: []
---
```

Derive the folder path and entry-point link from the descriptor's location. Avoid a second hand-maintained path field. Use repository URLs or stable identities where available. Machine-specific checkout paths belong in local configuration.

A small helper generates `CATALOG.md` from project frontmatter. The committed catalogue contains each project's name, description, optional routing aids, and a relative link to its `PROJECT.md`. Descriptions are edited in one place. Regenerate after adding, removing, renaming, or changing a project's routing metadata. Ordinary task updates do not change the catalogue.

An agent can read the short catalogue, select a matching project, and open its descriptor. Known repository identity should help selection, while descriptions support conceptual requests spanning several repositories. If several projects match, load their descriptors or clarify the scope before writing. Do not choose a task merely because it is the newest one.

These descriptors are a custom convention. They will not automatically appear in an agent's available context like registered skills do.

## Proposed behaviour and present state

In a maintained design, keep the observed current design separate from identified proposed changes. Record implementation gaps and contradictory observations as they are found, even when reality differs from an accepted decision. `current.md` links to the feature's current-design section and holds only project-level facts itself. Neither the project description nor the existence of a proposal establishes that a capability works.

| Record | Meaning | What it establishes |
| --- | --- | --- |
| Confirmed requirement | The user has specified a desired outcome or constraint. | What the system should support. |
| Proposed design | An approach is being considered. | Possible future behaviour. |
| Accepted decision | An approach has been chosen, with its source recorded. | The intended direction. Implementation may still be pending. |
| Implemented, unverified work | Files or code have been changed, but the relevant behaviour has not been checked. | That an implementation exists, with its remaining checks stated. |
| Verified current state | The relevant claim has supporting evidence from a stated environment or revision. | What was observed to work within that scope at the recorded checkpoint. |

A maintained document has no blanket acceptance or implementation status when it contains changes at different stages. Each proposed change has a stable identifier, its originating task, and independent states:

| State | Values | Meaning |
| --- | --- | --- |
| Decision | `proposed`, `accepted`, `rejected`, `superseded` | Whether the intended approach has been chosen. Record the source and rationale of acceptance or supersession. |
| Implementation | `not-started`, `partial`, `implemented`, `not-applicable` | What has been delivered. Use `not-applicable` only when the change itself genuinely needs no implementation. |
| Verification | `not-checked`, `passed`, `failed`, `needs-recheck` | Results of relevant checks, with their evidence and scope. |

Accepting a design changes its decision state, not its implementation or verification states. A design-only task can be complete while its change remains `not-started` and `not-checked`.

When results differ across parts of a change, record implementation and verification per required scope. The overall implementation is `partial` while requested work remains missing. Overall verification is `passed` only when relevant checks cover the full declared scope at the stated revision and environment. Otherwise record failed, stale, or unchecked scope as applicable, while preserving each subset's results. Do not narrow the declared scope merely to obtain a passed result; record any user-authorised scope change.

For the illustrative filters change, the notation would be:

| Required scope | Implementation | Verification | Evidence |
| --- | --- | --- | --- |
| Category filtering | `implemented` | `passed` | Subset check results, source revision, environment, and date. |
| Date filtering | `not-started` | `not-checked` | No implementation or check evidence yet. |
| Whole requested change | `partial` | `not-checked` for the full scope | Category results do not establish date-filter behaviour. |

These are example states, not results from a real search implementation in this repo.

For present-state claims, record supporting files or checks, the date, and the applicable scope. Scope might be a local workspace, code revision, installed skill, or agent environment. A catalogue that works in the docs workspace does not establish that agents in another project can discover it.

Update the owning document when new evidence supports a changed claim. Integrate verified changes into its current-design section and update any existing affected summaries or guides. Preserve the change's identifier, substantive delta, rationale, outcome, and relevant checkpoint rather than silently deleting its history. Revise active proposals in place. Keep superseded decision records and link their replacements where those records exist. Do not create a new document for each revision. When relevant source or environment facts change, recheck affected claims or mark their verification as needing recheck.

## Agent discovery and access

The intended reading path is:

```text
Agent's startup guidance
  -> Central docs location and CATALOG.md
  -> Relevant PROJECT.md
  -> Relevant maintained feature/project design and explicit task context
  -> Detailed documents needed for the work
```

For Codex, use a short global `AGENTS.md` pointer to make the docs location known across projects. Make the reusable skills available at user scope or through a supported plugin. Repo-local skills are useful for development in this repository but do not automatically load in unrelated code repos. [Instruction discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [skill discovery](https://learn.chatgpt.com/docs/build-skills).

The bootstrap should say where the docs live and when to consult the catalogue. Detailed operating instructions belong in the skill, and project facts belong in project documents. This avoids copying the same content into every code repository.

Configure filesystem access to the docs root for sessions that need it. An instruction or skill cannot grant that access. Validate the integration from another project's workspace during the pilot, including read and write access.

## Task context and audit

Record each distinct authorised task in one context document when this workflow is in use. Give it a stable identifier and directory. Record the requested deliverable, scope, goal, status, last update, relevant source repositories and revision where applicable, maintained design paths, and change identifiers. Include progress, unresolved assumptions, constraints, evidence links, and next action. A new message or session does not by itself create a new task.

Task completion is assessed against its requested deliverable. A design task completes when it delivers the requested coherent, reviewable design with constraints, trade-offs, status, and unresolved issues stated. A research task completes against its research scope. An implementation task needs the delivered behaviour and relevant checks. Record the actual outcome and evidence in task context. Do not require implementation to complete a design-only task, and do not start implementation merely because its design is accepted. Carry out implementation when the user's instructions include it.

Update context at meaningful checkpoints: changed scope, a significant finding, a completed phase, or a handoff. Keep a dated milestone record when reconstructing the sequence would help review. Avoid reproducing the full conversation or every tool call.

When resuming work, verify source facts relevant to the next action. A recent timestamp does not establish that the source code or external information still matches the document. Link completion claims to checks, resulting files, commits, or other appropriate evidence.

Resume or refine unfinished work in its existing task context. When reopening a completed task to finish or correct its original scope, preserve its completion checkpoint and append an amendment for the reopened work. An extension with new scope is a distinct task linked to the earlier one, while reusing the same maintained feature design. Do not reopen a completed task merely to make a later extension part of its original delivery.

Keep completed tasks addressable at their existing paths. Record a dated completion checkpoint in the existing context with delivered scope, check results and their limitations, material decisions and rationale, and a concise account of the requirements and contracts used. Link the maintained design and stable change identifier. Correct a historical claim with a dated amendment that states the correction while retaining the original delivery and understanding. Avoid moving task directories simply to mark them complete.

Before Git exists, the checkpoint prose preserves the relevant historical facts. A revision label or link to a mutable document cannot reconstruct its earlier contents. This records the design basis, not an exact copy of the whole document. Once Git is available, also record the exact docs commit and path for the design used, plus code commits for delivered implementation where applicable. Branch names alone are mutable references. Git introduced later cannot recover content already overwritten, so retain earlier prose checkpoints.

Promote lasting facts into their owning maintained documents and link back to task evidence. Preserve significant decisions in existing records or appropriate dated sections. Git history and milestone records support audit, but implementation claims still need checks within their stated scope.

## Coordinating shared edits

Separate task folders protect task records, but maintained feature designs, `current.md`, `PROJECT.md`, decision records, and the catalogue can be shared across tasks. Before overlapping edits, one coordinator assigns a single writer for each shared document. Record the assignment in existing task context and agent instructions. Assignment comes from the coordinator rather than agents independently claiming the same file.

Other agents keep contributions and evidence in their existing task records or send them to the assigned writer. The writer rereads the current document, preserves unrelated edits, reconciles conflicting proposals, and integrates the result. Handoffs identify the new writer and any pending contributions. Tasks with different IDs still follow this rule when they affect the same maintained document.

If a writer has not been coordinated while overlapping edits are active, keep contributions in the task context until the assignment is resolved. These are cooperation rules, not automatic filesystem locks. The pilot must exercise two agents working on the same feature as well as on separate task records.

## Writing skills and media

Start with two focused skills:

| Skill | Purpose | Main outputs |
| --- | --- | --- |
| `docs-context` | Find the owning project and maintained design, select or resume the task, recover context, and record meaningful checkpoints. | Project indexes, task context, evidence links, and catalogue updates when metadata changes. |
| `write-project-doc` | Revise the owning document using the chosen voice, change states, citations, and figure conventions. Create a separate document only when the maintenance rule permits it. | Maintained designs, research notes, guides, and decision records with linked media. |

Keep instructions brief. Put the selected writing style and substantial document-type guidance in references, and reusable output templates in assets. Skill frontmatter and supporting resources follow the [Agent Skills format](https://agentskills.io/specification).

The exact prose style remains open. Existing report-writing preferences offer a starting point, but general docs need a representative example before report-specific rules are adopted. The first writing exercise should be a short real design document that the user can edit. Those corrections become the style reference.

Use relative image paths inside documents. Keep feature media in `features/assets/<feature-id>/` when using the suggested layout, and task-only media in the task's `assets/` folder. Existing documents can retain their existing media locations. Link reusable media rather than copying it into every task. Use Mermaid for diagrams where the viewer renders it, with an SVG or PNG alternative when needed. Alt text explains what the image shows, and nearby prose or a caption explains its significance. [Markdown and media links](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax), [Mermaid support](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams).

Use short decision records for decisions that matter beyond one task. Record context, status, decision, and consequences. Preserve a superseded record and link its replacement. [ADR precedent](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions).

## Implementation sequence

1. Finalise the project descriptor, change-state notation, task checkpoint, and media conventions using the resolved workflow below. Use this documentation project as the first real example.
2. Create the catalogue helper and a small consistency check for descriptor identities, catalogue entries, and local document/media paths. Initialise Git when implementing the agreed repository.
3. Draft the two skills and one example design document. Refine the style from user edits to that example.
4. Configure the startup pointer, cross-project skill discovery, and filesystem access. Test with a fresh agent starting in another project.
5. Pilot separate tasks, overlapping work on the same maintained feature, and a handoff. Refine where the observed workflow fails.

Pilot acceptance checks:

- A fresh agent can identify the correct project from its description and repository identity without reading unrelated project documents.
- An agent starting outside the docs workspace can find and access the relevant docs.
- A fresh session can recover a task's state and next action, including what has and has not been verified.
- A reader can distinguish current behaviour, accepted decisions, and proposals. An accepted but unimplemented design is never presented as a working capability.
- A design-only task can complete while its change remains unimplemented, and acceptance alone does not trigger implementation.
- A feature extension updates the indexed maintained design, with no competing task design created by default.
- Documents and images remain linked after the repository is cloned elsewhere. Diagrams work in the chosen review viewer.
- Agents updating different tasks preserve each other's work.
- Agents working on the same feature share a coordinated writer and do not race to edit its maintained documents.
- A completed task retains its delivery and design basis after the maintained feature design is updated. Exact historical document retrieval is checked when Git is available.
- Editing a project's description regenerates a consistent catalogue.
- A produced document follows the agreed style and makes its proposal or implementation status clear.
- A new finding or requirement updates the appropriate existing document without creating a duplicate, and outdated claims are corrected throughout that document.
- A follow-up or resumed session reuses the same task record, and partial checks establish only the stated subset of a change.

## Worked example: extending search

This is an illustrative walkthrough, not an implemented feature in this repo. Assume an existing search document records checked keyword-search behaviour. That existing file remains the maintained design even if its path differs from the suggested layout.

| Event | Documentation action | Task outcome | Filter-change state |
| --- | --- | --- | --- |
| User asks to design search filters. | Find and check the existing design and code. Add an identified filters proposal to the same design; record its intended behaviour, interfaces, trade-offs, and open issues. Use one task context for this design work. | Complete when the requested design is delivered. Preserve a checkpoint of its scope and design basis. | `proposed` / `not-started` / `not-checked`. |
| User accepts the design. | Update that change's decision and record the source of acceptance. Keep the current keyword-search account separate from the intended filters. | The completed design task remains complete. | `accepted` / `not-started` / `not-checked`. |
| User asks to implement the filters. | Track the new implementation scope in its own task context, linked to the design task and the same filter-change identifier. Reuse the maintained design. | In progress until its requested implementation scope and checks are satisfied. | Implementation moves to `partial` or `implemented`; verification follows the checks actually performed. |
| Only category filtering is implemented and checked. | Record category and date results separately in the scoped-state table. Keep the remaining filter work pending. | Implementation task remains incomplete if its scope includes the remaining filters. | `accepted` / `partial` / `not-checked` for the whole change; category checks are `passed`. |
| The full requested filters are implemented and checked. | Integrate the resulting current behaviour, retain the change's delta and rationale, and add the implementation completion checkpoint and revision references. | Implementation task is complete. The earlier design checkpoint still describes design work only. | `accepted` / `implemented` / `passed` for the stated scope and revision. |

Follow-up questions during design reuse the design task. If another agent is concurrently designing search ranking, the coordinator assigns one writer for the shared search document and both agents contribute through their own task records. The project current-state summary links to the maintained search facts rather than duplicating them.

## Design review resolutions

Reviewed and revised: 11 October 2026. The user requested that the five identified issues be addressed. They are resolved as design definitions and local operating rules; their cross-project operation remains to be demonstrated in the pilot.

| Reviewed issue | Resolution |
| --- | --- |
| No maintained feature-design home. | One indexed existing feature or project design is authoritative. The suggested default is `features/<feature-id>.md`; task designs are optional distinct artifacts. |
| Mixed current and proposed behaviour. | Separate current design from identified changes. Each change has independent decision, implementation, and verification states, with evidence scope. Detailed facts have one owner. |
| Mutable links obscure history. | Existing task contexts preserve completion checkpoints and relevant design contracts. Git enables exact commit-and-path references later; a mutable link or revision label alone is insufficient. |
| Concurrent tasks share documents. | A coordinator assigns one writer before overlapping edits to shared documents. Contributors use task records or coordination messages; no automatic lock is claimed. |
| Completion mismatches the request. | Requested deliverables govern completion. Design-only work can finish before implementation, and acceptance alone does not authorise code changes. |

OpenSpec's maintained domain specs and separate change records provide a useful precedent for maintained facts and task history. The design adapts that separation to the user's preference for updating existing documents. [OpenSpec structure](https://github.com/Fission-AI/OpenSpec/blob/main/docs/getting-started.md).

The original ADR convention preserves superseded decisions, which supports retaining a historical account even while the maintained design changes. [ADR history convention](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions).

The catalogue, skills, and cross-project integration remain unimplemented in [CURRENT.md](../CURRENT.md). Git has now been initialised for the user's requested documentation commit. A pilot must still demonstrate discovery, access, document reuse, and recovery from a fresh session before these capabilities can be described as working.

The reviewed structural and workflow issues are now specified. Exact prose style, final template notation, and the first external project for the pilot remain open. The next implementation work is to create the catalogue and skills, configure discovery and access, and exercise these rules with real tasks.

## Completion checkpoint: docs-workflow-refinements

Recorded: 11 October 2026. Work identifier: `docs-workflow-refinements`.

Requested deliverable: address the five design-review issues. This was documentation and workflow design work. It did not include building the catalogue, installing skills, or configuring cross-project access.

Delivered: this maintained design and the existing local `AGENTS.md`, README, and current-state record were revised. The design basis at this checkpoint is:

- An existing appropriate feature or project design remains authoritative. New feature designs default to `features/<feature-id>.md` only when needed. Extensions reuse that document, and task contexts link to it.
- Current design and identified changes are separate sections. Decision, implementation, and verification are independent, with scoped results when a change is partial. Project current-state records link to detailed feature facts rather than copying them.
- Task completion follows the requested deliverable. A completed design task can leave implementation and verification pending. Follow-ups reuse task context; a distinct extension uses a new task record under the configured workflow and preserves earlier completion history.
- Completion checkpoints retain delivered scope, checks, decisions, rationale, and relevant requirements or contracts in prose. Exact commit-and-path references are added when Git is available. A link or revision label alone does not preserve overwritten content.
- A coordinator assigns one writer before overlapping edits to shared maintained documents. Other agents contribute through task context or messages. This relies on cooperation and does not implement an automatic lock.

Checks: local document links and Markdown code-fence balance were checked. An independent agent applied the written workflow to five hypothetical cases: design and acceptance, concurrent feature work, pre-Git historical references, partial filter implementation, and an explicitly requested separate design document. The cases produced consistent outcomes. Its two follow-up findings were addressed through explicit scoped-state notation and this historical checkpoint.

Limits: no code feature, catalogue, skill, shared-file locking mechanism, or cross-project integration was implemented or exercised. No Git revision is available. This checkpoint preserves the relevant design basis, not the exact earlier contents of every document.

The checkpoint is kept in this existing design while task-record infrastructure is unimplemented. It is a historical account of this revision. Preserve it when the maintained design changes and append dated corrections or amendments where needed.
