---
status: active
phase: "Phase 1: Starter Foundation"
last_reviewed: 2026-04-27
owner: repository maintainer
---

# Phase 1: Starter Foundation

This document expands [the canonical roadmap](../README.md) for `Phase 1`.

It defines what `starter foundation` means for `wayrail`, what should be standardized first, and which project shape should become the default base for later phases.

This is a phase design document, not an implementation plan.
Concrete build steps should later move into [docs/plans/](../../plans/).

## Goal

Make `wayrail` capable of putting a repository onto one visible starter path.

At the end of this phase, a new or existing repository should be able to enter the `wayrail` system without relying on remembered setup rituals or hidden chat conventions.

## Why Phase 1 Exists

Without a starter foundation, every later phase floats on unstable ground.

If repository entry is inconsistent, then:

- agent instructions drift before work begins
- verification rules are bolted on too late
- learnings have no obvious home
- existing repositories require bespoke interpretation
- future upgrades cannot distinguish core files from project-specific files

Phase 1 solves the first problem in the chain: how a repository becomes a `wayrail` repository.

## Scope

Phase 1 is responsible for:

- defining the first canonical repository shape
- defining the first starter entry points
- distinguishing `bootstrap` from `adopt`
- identifying required versus optional starter artifacts
- defining where later contract, verification, and compounding layers will live
- keeping the starter file-first and inspectable

Phase 1 is not responsible for fully specifying:

- the final agent working contract
- hard verification gates
- hooks as a default mechanism
- long-running runtime features
- database-backed state
- broad multi-host packaging

## Best-Practice Basis

The design choices in this phase follow two main inputs:

1. `wayrail` research conclusions:

- [research overview](../../research/comparisons/overview.md)
- [adoption notes](../../research/comparisons/adoption-notes.md)

2. External best practices:

- internal platform guidance favors a clear golden path and reduced setup burden rather than maximum flexibility: [AWS Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/internal-developer-platform/principles.html)
- software templates should include documentation and policy surfaces, not only code skeletons: [Red Hat Developer Hub](https://docs.redhat.com/en/documentation/red_hat_developer_hub/1.9/html/customizing_red_hat_developer_hub/assembly-creating-templates_customizing-rhdh)
- repository documentation should be addressable, navigable, and maintained with the code: [GitHub README guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes), [Write the Docs principles](https://www.writethedocs.org/guide/writing/docs-principles/)

## Design Decisions

### 1. The Starter Must Be Repo-Local

The starter should install files inside the target repository instead of depending on a hidden external control plane.

Reason:

- agents need to infer the local rules from repository files
- projects must stay legible even when tooling changes
- future public users should be able to inspect the system without private infrastructure

### 2. `Bootstrap` and `Adopt` Are Different Paths

`bootstrap` means starting a new repository on the standard shape.
`adopt` means bringing an existing repository under the same standard with minimal disruption.

They should share the same target model, but not the same operational assumptions.

Reason:

- new repositories can accept a cleaner baseline
- existing repositories need a migration-oriented path
- conflating the two leads to brittle starter logic and bad defaults

### 3. The Starter Should Standardize Documents Before Behavior

Phase 1 should first create visible structure and named homes for later rules before it tries to enforce detailed workflow behavior.

Reason:

- structure makes later contract and verification work easier
- file placement and ownership must be settled before stronger rules are layered on top
- this keeps the phase within starter scope instead of drifting into runtime scope

### 4. The Entry Point Should Stay Thin

Phase 1 should define one canonical starter entry point, but it does not need to prematurely commit to a heavy CLI.

Acceptable early forms:

- a thin CLI
- a scripted entry point
- a task runner entry point with a documented contract

Unacceptable early form:

- multiple overlapping ways to install the starter with different results

### 5. Required Artifacts Must Stay Small

The starter should install the minimum set of files needed to make the repository legible and extensible.

Reason:

- too much surface too early recreates prompt-pack sprawl
- future adoption into existing repositories becomes harder as the required footprint grows

## Recommended Project Shape

This is the recommended Phase 1 target shape for a repository using `wayrail`.

```text
<repo>/
  README.md
  AGENTS.md
  wayrail.yaml
  docs/
    roadmap/
    research/          # optional for downstream projects unless they do product research
    adr/               # optional, but reserved
  specs/
    _templates/
      spec.md
      plan.md
      verification.md
      review.md
    <YYYYMMDD-HHMM-short-slug>/
      spec.md
      plan.md
      verification.md
      review.md
  memory/
    learnings.md
  scripts/
    wayrail/
      bootstrap
      adopt
      doctor           # optional in Phase 1, but the location is reserved
```

This is a target shape, not a mandatory all-at-once install set.
Some paths are required immediately and some are reserved for later phases.

When `wr-spec` starts a new spec item, it should create the full lifecycle directory immediately.
The scaffolding step should create `spec.md`, `plan.md`, `verification.md`, and `review.md`, but only `spec.md` should receive meaningful authored content at the spec stage.
The later lifecycle files should start as minimal stubs that point to their owning skills.
This keeps artifact paths predictable without implying that planning, verification, or review already happened.

## Canonical Starter Artifacts

### Required in Phase 1

- `README.md`
  Reason: every repository needs a human-facing entry point.
- `AGENTS.md`
  Reason: the repository needs a visible local agent entry document early.
  It should be a thin table-of-contents style entrypoint, not the whole operating constitution.
  The starter should route agents to `specs/<id>/`, docs, and nested `AGENTS.md` files; it should not duplicate the full harness method.
  For non-trivial work, it should point to the `spec -> plan -> implement -> verify -> review` lifecycle and the `wr-spec`, `wr-plan`, `wr-verify`, and `wr-review` skills when available.
  "Non-trivial" means work that changes behavior, public interface, repository structure, data, security posture, dependencies, workflow rules, or more than one tightly scoped file.
- `wayrail.yaml`
  Reason: later phases need one explicit repo-local configuration anchor.
- `docs/roadmap/`
  Reason: the project needs a place for direction-setting documents.
- `specs/`
  Reason: workflow artifacts should be grouped by spec item so a full work cycle is reconstructable from one directory.

### Spec Item Naming

Phase 1 should use this spec item directory format:

```text
specs/<YYYYMMDD-HHMM-short-slug>/
```

Example:

```text
specs/20260427-2015-bootstrap-entrypoint/
```

Reason:

- timestamp prefixes keep spec items sortable without a separate registry
- minute-level precision avoids same-day collisions during agent-heavy work
- a short slug keeps the directory understandable to humans
- this stays lighter than introducing issue numbers or a task database in Phase 1

The timestamp should use the operator's local project timezone. When exact timezone matters, record it in the spec artifact frontmatter instead of expanding the directory name.

### Spec Item Spec Shape

The default `spec.md` should define WHAT is being solved and WHY it matters before planning begins.

Recommended minimum body sections after frontmatter:

```markdown
# <Title>

## Problem

## Why Now

## Requirements

## Success Criteria

## Scope

## Constraints

## Assumptions

## Open Questions

## Planning Handoff
```

Requirements should use stable IDs for non-trivial work, such as `R1`, `R2`, and `R3`, so later planning, verification, and review can trace decisions back to the spec.
Use `SC1`, `A1`, and `Q1` style IDs only when success criteria, assumptions, or open questions need explicit traceability.

User stories or acceptance scenarios may be added for user-facing features, but they should not be mandatory starter ceremony.

`wr-spec` should ask at most three critical human questions during initial spec creation.
Questions are reserved for choices that materially affect scope, user behavior, success criteria, non-goals, security or privacy posture, acceptable risk, or planning readiness.
Low-impact defaults should become visible assumptions instead of conversational blockers.

The spec is ready for `wr-plan` only when requirements are concrete, success criteria are objectively reviewable, scope boundaries are explicit, assumptions are visible, and no `Resolve Before Planning` questions remain.
The `Planning Handoff` section should say whether the spec is ready for `wr-plan`, list remaining blockers if any, and include the spec path for a fresh agent.

### Spec Item Plan Shape

The default `plan.md` should stay compact and implementation-design oriented.

Recommended minimum sections:

```markdown
# <Title> Plan

## Overview

## Requirements Trace

## Scope

## Context

## Decisions

## Implementation Units

## Verification

## Risks
```

This keeps `plan.md` focused on HOW the spec item will be implemented: requirements trace, scope, relevant context, technical decisions, coarse implementation units, verification expectations, and risks.

`plan.md` should not own lifecycle state in Phase 1. Spec item `status` and `stage` belong in `spec.md` frontmatter.

`wr-plan` should stop when `spec.md` is not ready for planning or still has `Resolve Before Planning` questions.
It should do bounded repository research, name relevant files and test conventions, and translate requirements into coarse implementation units.
Implementation units may use checkboxes, but they should stay larger than patch-level tasks.
Phase 1 should not create a separate `tasks.md` or task-generation skill.
`wr-plan` defines expected verification evidence; `wr-verify` records actual evidence.

### Spec Item Verification Shape

The default `verification.md` should summarize verification evidence without becoming a raw terminal log.

Recommended minimum sections:

```markdown
# <Title> Verification

## Summary

## Planned Checks

## Results

## Manual Validation

## Skipped Checks

## Remaining Risk
```

Each check should record the command or method, result, and concise evidence. Initial per-check result labels are `pass`, `fail`, `skipped`, and `blocked`.

Skipped checks require a reason. Any residual uncertainty belongs in `Remaining Risk`.

`wr-verify` should be a fresh-evidence writer.
It should run planned checks from `plan.md`, record exact command or method evidence, and avoid source edits.
Missing or unsafe checks should be recorded as `blocked` or `skipped`, not treated as passing.
The overall verdict may be `pass`, `fail`, `partial`, or `blocked`.
Human approval is required to accept skipped checks, waive failed checks, or proceed with incomplete evidence.
`verification.md` should end with a review handoff that points `wr-review` at failed, blocked, skipped, or manually validated areas.

### Spec Item Review Shape

The default `review.md` should preserve fresh-context review findings and their resolution state.

Recommended minimum sections:

```markdown
# <Title> Review

## Summary

## Scope

## Reviewers

## Findings

## Resolutions

## Residual Risk

## Verdict
```

Findings should include severity, location when applicable, evidence, and recommendation. Initial severity labels are `P0`, `P1`, `P2`, and `P3`; initial resolution labels are `fixed`, `accepted`, `deferred`, `rejected`, and `open`.

If no findings are raised, the artifact should state that explicitly and still record the scope, reviewer, and verdict.

`wr-review` should be a read-only fresh-context review.
It should read `spec.md`, `plan.md`, `verification.md`, and the current diff, then write only `review.md`.
It should not fix issues or approve release.
For non-trivial or risky work, it may use fresh read-only reviewer roles such as correctness, testing/evidence, maintainability/scope, and conditional security/API/data/reliability reviewers.
Open `P0` or `P1` findings block a ready verdict.
Verdicts should be `ready`, `ready-with-residual-risk`, or `not-ready`.
Human approval is still separate from the review artifact.

### Strongly Recommended in Phase 1

- `memory/learnings.md`
  Reason: even before a fuller compounding model exists, the repository should have a visible home for durable learnings.
- `scripts/wayrail/`
  Reason: reserving one location for starter entry points keeps the install surface legible.

### Minimal Configuration

`wayrail.yaml` should use a small versioned schema in Phase 1:

```yaml
schema_version: 1
timezone: local
workflow:
  artifact_root: specs
  spec_id_format: YYYYMMDD-HHMM-short-slug
  lifecycle:
    - spec
    - plan
    - implement
    - verify
    - review
memory:
  learnings: memory/learnings.md
```

This records the working contract without introducing host-specific keys, hook configuration, runtime state, or tool installation metadata.
Through Phase 2, this repo-local file should remain the only authoritative shared config contract.
Do not add a global config file or local override file yet.
Future global config may hold personal preferences or machine paths, but it must not silently change lifecycle stages, artifact layout, spec ID format, memory policy, or verification gates for an existing repo.

### Product Template Source

The `wayrail` product repository should keep one Phase 1 template source:

```text
template/
  README.md
  AGENTS.md
  wayrail.yaml
  docs/
    roadmap/
      README.md
  specs/
    .gitkeep
    _templates/
      spec.md
      plan.md
      verification.md
      review.md
  memory/
    learnings.md
```

`README.md` is bootstrap-oriented and should not overwrite an existing README during adoption. `specs/_templates/` is not a spec item; it is a visible source for creating future spec item artifacts.

The first spec-stage automation should live in `wr-spec` as a small scaffold script plus templates.
The script is responsible for timestamped directory creation, slug normalization, frontmatter seed values, and stub file creation.
The agent is responsible for discussing and writing the actual `spec.md` contents.
The script should expose an agent-readable interface:

```text
new-spec-item [--json] [--dry-run] [--slug SLUG] [--root PATH] [--timezone TZ] -- TITLE
```

`--json` should print a single object containing `spec_id`, every created file path, `slug`, `created_at`, and `timezone`.
The default behavior should fail on an existing spec item directory and should not create branches, force-overwrite files, or write a current-spec state file in Phase 1.
Template lookup should prefer `specs/_templates/`, then skill-local templates, then built-in fallback stubs.
The preferred implementation target is Python 3 standard library so the same script can handle JSON, paths, timestamps, and slug validation without separate Bash and PowerShell versions.

### Reserved for Later Phases

- `docs/research/`
  Use when a project performs durable research work.
- `docs/adr/`
  Use when the project needs architecture decision records.
- `docs/plans/`
  Use for product or architecture planning documents that are not part of one spec item lifecycle.
- `tasks/` or `docs/tasks/`
  Reserve until the task model is explicitly designed.
- hooks, runtime folders, or host-specific config trees
  Do not make these default starter requirements in Phase 1.

## Required vs Optional Philosophy

Phase 1 should separate three categories.

### Required

Files that every repository needs in order to be recognized as a `wayrail` repository.

### Recommended

Files that improve clarity and future growth, but whose absence should not block early adoption.

### Reserved

Paths intentionally kept open for later phases without forcing them into every repository now.

This matters because adoption into existing repositories should remain viable.
If too many files are marked required too early, the starter becomes a migration tax instead of a standardization tool.

## Starter Entry Points

Phase 1 should define exactly two starter actions.
These should be scripts-first entrypoints with CLI-shaped contracts, not a packaged public CLI yet.
Scripts should support bounded output, meaningful exit codes, `--help`, `--dry-run`, and `--json` where useful.
Structured output belongs on stdout in JSON mode; diagnostics belong on stderr.
A future `hk` or `wayrail` CLI can wrap the same behavior after the workflow and distribution needs are stable.

### `bootstrap`

Use when the repository is new and the standard shape can be installed directly.

Expected behavior:

- create the Phase 1 template artifacts
- write `README.md` only when absent
- create `AGENTS.md`, `wayrail.yaml`, `docs/roadmap/README.md`, `specs/`, `specs/_templates/`, and `memory/learnings.md`
- avoid creating a timestamped spec item by default
- stop on conflicting existing files unless an explicit future force or merge mode is selected
- avoid adding hooks, host-specific config, runtime state, or task databases

### `adopt`

Use when the repository already exists and needs to be brought under the same standard.

Expected behavior:

- inspect the repository against the target shape
- create missing non-conflicting harness artifacts
- preserve existing `README.md`
- preserve existing `AGENTS.md`; report that the harness entrypoint needs manual or explicit merge integration
- preserve existing `docs/`, `specs/`, and `memory/` contents
- avoid destructive rewrites of existing project structure
- report what was created, what already existed, and what still needs manual integration

Phase 1 should not automatically deep-merge existing Markdown files. Merge behavior can be added later as an explicit, separately tested mode.
Phase 1 should also avoid broad `--force`.
Instead, `bootstrap` and `adopt` should support `--dry-run` conflict reports that list planned creates, preserved files, identical files, conflicts, and suggested manual actions.
If conflicts exist, non-interactive runs should exit non-zero without partial mutation.
Future force or merge modes should be scoped to harness-owned files or marked blocks and should use backups by default.

### Deferred Entry Point: `doctor`

`doctor` is not the center of Phase 1, but the location and intent should be reserved.
If shipped in Phase 1, it should be a read-only starter contract validator.

Intended future role:

- distinguish starter install health from later execution readiness
- validate that the repository still satisfies the local starter contract

Initial checks should cover environment facts, required starter files, `wayrail.yaml`, lifecycle template shape, workflow artifact readiness, and optional integration visibility.
It should not run project tests, install dependencies, merge docs, repair files, or claim runtime readiness by default.

Exit behavior should be simple:

- `0`: pass or warnings only
- `1`: contract failures
- `2`: invalid invocation or internal error

`doctor --json` should be stable from the beginning.
Warnings should not fail by default; a future strict mode can be added for CI.
Network checks should require an explicit future `--online` mode.

## `Bootstrap` vs `Adopt`

The difference should be explicit in both code and docs.

### `bootstrap` assumptions

- repository is early enough to accept a cleaner baseline
- starter can create structure proactively
- fewer compatibility accommodations are needed

### `adopt` assumptions

- repository may already contain conventions worth preserving
- starter must avoid broad rewrites
- install should prefer additive, inspectable changes

### Shared target model

Both paths should converge on:

- the same required starter artifacts
- the same config anchor
- the same visible local contract starting point

The paths differ in migration behavior, not in final identity.

## Configuration Model

Phase 1 should introduce one repo-local configuration anchor:

- `wayrail.yaml`

Initial use should stay narrow and versioned.

Phase 1 contents:

```yaml
schema_version: 1
timezone: local
workflow:
  artifact_root: specs
  spec_id_format: YYYYMMDD-HHMM-short-slug
  lifecycle:
    - spec
    - plan
    - implement
    - verify
    - review
memory:
  learnings: memory/learnings.md
```

This is enough structure to make repo-local authority visible without turning configuration into a broad runtime schema.

## Customization Boundaries

Phase 1 should allow limited customization, but only in controlled places.

### Allowed early variation

- project stack metadata
- optional document creation
- starter profile selection if it remains narrow

### Not allowed in Phase 1 core

- project-specific role catalogs
- host-specific runtime behavior in the core starter
- many alternative directory layouts
- broad plugin or extension points

Reason:

Phase 1 exists to reduce startup variance, not to encode every variance up front.

## File Ownership Model

The starter should make file ownership legible.

Recommended ownership rule:

- files created by `wayrail` should be clearly documented as starter-managed
- files intended for ongoing project editing should stay editable and human-readable
- reserved paths should be documented even if empty

This will matter later for upgrades.
If the repository cannot tell which artifacts belong to the starter, standard evolution becomes risky.

## Phase 1 Validation Questions

Before Phase 1 is considered complete, the following questions should have clear answers:

- Can a new repository enter the system through one canonical starter path?
- Can an existing repository be evaluated and adopted without bespoke redesign?
- Are the required starter artifacts few enough to keep adoption realistic?
- Can an agent locate the local starter boundary from repository files alone?
- Is the starter still clearly separate from a runtime platform?

## Phase 1 Success Signals

Phase 1 is working if:

- starting another repository no longer requires reconstructing the same starter shape from memory
- different repositories begin to share the same visible starter anchors
- adoption into an existing repository looks like bounded standardization rather than reinvention
- later Phase 2 and Phase 3 decisions have obvious homes in the repository layout

## Phase 1 Exit Criteria

Phase 1 should be considered complete when:

- one canonical starter path exists for new repositories
- one canonical adoption path exists for existing repositories
- the required starter artifact set is explicitly defined
- the repo-local configuration anchor exists
- the starter-managed versus project-edited artifact boundary is documented
- the recommended repository shape is written down and stable enough to design against

## Phase 2 Revisit Items

These questions now have initial answers in the Phase 1 foundation decision record, but they should be revisited when Phase 2 starts:

- root `AGENTS.md` exact wording may need adjustment after real adoption
- global configuration should remain deferred unless personal defaults become necessary
- workflow skills should use host-agnostic source under `skills/` with a Codex-first adapter

## Immediate Handoff

The next step after this phase document is not implementation yet.
The next step is to write one or more concrete plans in [docs/plans/](../../plans/) for the first starter artifact set and the first starter entry point.
