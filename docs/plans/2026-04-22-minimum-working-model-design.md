---
status: draft
phase: "Phase 1: Starter Foundation"
last_reviewed: 2026-04-27
owner: repository maintainer
---

# Minimum Working Model Design

This document defines the first draft of the `wayrail` working layer.

It exists to answer one question before starter installation is designed in detail:

What is the minimum operating model that an agent should follow inside a `wayrail` repository?

This is not yet the final file layout or starter implementation plan.
It is the contract design that later shapes:

- `AGENTS.md`
- repository docs structure
- starter outputs
- thin commands such as `bootstrap`, `adopt`, and later `doctor`
- reusable skills or scripts

## Why This Comes Before Installation

Installation is a delivery mechanism.
The working model is the thing being delivered.

If `wayrail` defines installation first, it risks producing a visible but empty starter:

- folders without a clear operating meaning
- agent instructions without a real workflow behind them
- setup commands that create files but not a standard way of working

The community projects studied for `wayrail` all converge on the same pattern:

- install or setup the workflow
- define the work before implementation
- execute against a visible plan
- verify and review with fresh context
- record learnings so later work improves

This design makes that pattern explicit for `wayrail`.

## Best-Practice Basis

This draft is grounded in two inputs:

1. internal research already captured in this repository
2. external primary sources and public documentation

Relevant internal documents:

- [Research overview](../research/comparisons/overview.md)
- [Adoption notes](../research/comparisons/adoption-notes.md)
- [Phase 1 starter foundation](../roadmap/phases/phase-1-starter-foundation.md)

Relevant external sources:

- Every's public guide frames the core loop as `plan -> work -> review -> compound`, and treats plan plus review as the highest-leverage parts of the process: [Compound Engineering](https://every.to/guides/compound-engineering)
- `oh-my-codex` centers a repo-local operating layer with setup, doctor, state authority, and durable local files: [Oh My Codex docs](https://oh-my-codex.dev/docs.html)
- `superpowers` publicly emphasizes brainstorming, plan writing, execution, review, and verification-oriented skills as the core usage path: [Superpowers repository](https://github.com/obra/superpowers)
- `Archon` emphasizes explicit workflows, validation, and lifecycle gates rather than ad hoc conversational drift: [Archon repository](https://github.com/coleam00/Archon)
- docs-as-code guidance favors repository-local, navigable documentation that evolves with the codebase: [GitHub README guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes), [Write the Docs principles](https://www.writethedocs.org/guide/writing/docs-principles/)

## Design Summary

`wayrail` should treat the working layer as a minimum contract with six parts:

1. `stage model`
2. `artifact model`
3. `verification model`
4. `memory model`
5. `authority model`
6. `escalation model`

The recommended core lifecycle is:

`spec -> plan -> implement -> verify -> review`

This is the smallest model that still captures what the benchmark projects repeatedly protect:

- explicit problem framing
- plan-first execution
- evidence before completion
- independent review with fresh context

`compound` remains part of the broader harness, but the initial core workflow treats it as a lightweight supported layer rather than a mandatory stage.

## Non-Goals

This document does not define:

- a full multi-agent runtime
- long-running orchestration
- hook plumbing as a default mechanism
- final CLI syntax
- final docs directory names for every artifact
- host-specific prompt wording
- a plugin or marketplace strategy

Those come later.
This document only defines the minimum operating contract that installation should eventually deliver.

## Working Model Principles

### 1. Work Starts From A Visible Problem Definition

A repository should not jump from user request directly into code.
There must be a visible artifact that records what is being solved, why it matters, and what is out of scope.

### 2. Plan Before Code

Implementation should follow a written plan rather than rely on one session's hidden reasoning.
The plan is the handoff surface between design and execution.

### 3. Verification Is Separate From Review

Verification answers "does the code work against explicit checks?"
Review answers "does this solution make sense, and did we miss problems?"

Both are necessary.
They should not collapse into a single vague "looks good" step.

### 4. Review Needs Fresh Context

The implementation agent should not be the only judge of completion.
A separate reviewer, ideally with no hidden execution context, should inspect the result from the outside.

### 5. Learnings Must Outlive The Session

If the same mistake or insight must be rediscovered in the next repository, the harness has failed to compound.

### 6. The Local Repository Must Explain Itself

An agent should be able to infer how to work from repository files, not from private chat history or remembered rituals.

## The Six Contract Axes

### 1. Stage Model

The minimum recommended stage model is:

### Stage 1: `spec`

Purpose:
- define the problem
- record intent, scope, constraints, and non-goals
- prevent immediate drift into implementation details

Why this stage exists:
- `superpowers` and similar systems strongly separate discovery from execution
- Every's public workflow treats planning as the highest-leverage act, which assumes the problem is already clarified

Entry condition:
- there is a user request or project need worth changing

Exit condition:
- the repository has a visible spec-level artifact describing:
  - problem statement
  - why now
  - constraints
  - success criteria
  - non-goals

### Stage 2: `plan`

Purpose:
- translate the spec into an implementation approach
- identify file impact, sequencing, risks, and validation commands

Why this stage exists:
- plans are the control document for later implementation and review
- this is the point where tradeoffs should be made before code exists

Entry condition:
- a spec artifact exists and is judged coherent enough to execute

Exit condition:
- there is a plan artifact that is specific enough for a fresh engineer or agent to execute

### Stage 3: `implement`

Purpose:
- change the repository according to the approved plan

Why this stage exists:
- implementation should be a bounded execution phase, not a place where requirements are silently rewritten

Entry condition:
- a plan artifact exists

Exit condition:
- code or content changes are present
- implementation notes, if needed, make deviations from the plan visible

### Stage 4: `verify`

Purpose:
- establish whether the implementation satisfies explicit checks

Why this stage exists:
- benchmark projects repeatedly distrust agent self-report
- `verify` is the point where tests, lint, typecheck, build, or other explicit checks produce evidence

Entry condition:
- implementation changes exist

Exit condition:
- the defined verification commands have been run or a justified exception has been recorded
- evidence is available in a visible artifact or command summary

### Stage 5: `review`

Purpose:
- inspect the solution from fresh context
- catch design mistakes, missed edge cases, policy drift, and weak assumptions

Why this stage exists:
- Every's review stage and the review-heavy `superpowers` workflows treat independent review as a first-class step
- this is where "same-agent completion bias" gets corrected

Entry condition:
- verification evidence exists

Exit condition:
- review findings are either resolved, explicitly accepted, or explicitly deferred

### Supported Layer: `compound`

Purpose:
- preserve reusable insight from completed work

Why this layer exists:
- compounding is the difference between one-off agent help and a learning working system
- benchmark projects repeatedly store lessons, wiki updates, or retros so later work gets easier

Initial policy:
- `compound` is supported from the beginning through lightweight memory artifacts
- it is not part of the first mandatory completion gate
- it should become stronger only after real use shows what is worth preserving

### 2. Artifact Model

Each stage should produce or update a visible artifact class.

This draft intentionally defines artifact types before final folder names.
The goal is to establish responsibility first and path naming second.

### `spec` artifact

Should capture:

- problem statement
- why it matters
- constraints
- success criteria
- non-goals

This is a `what/why` document.
It should avoid implementation sequencing where possible.

### `plan` artifact

Should capture:

- affected files or systems
- approach
- sequencing
- validation commands
- risks or open questions

This is a `how` document.

### `implementation` artifact

Primary artifact:
- the actual code or content change

Optional supporting artifact:
- a short implementation note only when plan deviations need explanation

### `verification` artifact

Should capture:

- which checks were run
- their outcomes
- any justified skips

This can be lightweight, but it must be visible.

### `review` artifact

Should capture:

- reviewer identity or role
- findings
- severity or priority
- resolution state

This artifact matters because review should survive the session, not disappear into transient chat.

### `compound` artifact

Should capture:

- reusable lesson
- trigger or failure mode
- future guardrail or rule implication
- links back to the solved work when useful

This should stay concise.
The goal is retrieval and reuse, not narrative journaling.

### Default Spec Item File Shape

The initial file shape for a single cycle should be:

```text
specs/<YYYYMMDD-HHMM-short-slug>/
  spec.md
  plan.md
  verification.md
  review.md
```

Responsibilities:

- `spec.md`: what and why, plus minimal metadata such as `spec_id`, `status`, `stage`, `created_at`, and `timezone`
- `plan.md`: implementation design, affected work units, verification plan, and known risks
- `verification.md`: evidence from commands, checks, manual validation, and skipped checks
- `review.md`: fresh-context review findings and resolution state

The spec item directory name should follow:

```text
specs/<YYYYMMDD-HHMM-short-slug>/
```

Example:

```text
specs/20260427-2015-bootstrap-entrypoint/
```

Phase 1 should not require a separate `status.md`. Lightweight status belongs in `spec.md` frontmatter at first. If repeated use shows a need for machine-owned workflow state, add a dedicated runtime state artifact later instead of inventing one before the workflow proves it needs it.

Recommended minimum `spec.md` frontmatter:

```yaml
---
spec_id: 20260427-2015-bootstrap-entrypoint
title: Bootstrap Entrypoint
status: draft
stage: spec
created_at: 2026-04-27 20:15
timezone: Asia/Seoul
---
```

Initial allowed values:

- `status`: `draft`, `active`, `blocked`, `completed`, `abandoned`
- `stage`: `spec`, `plan`, `implement`, `verify`, `review`

Do not include `owner` in the Phase 1 minimum. Add ownership metadata later only if multi-operator use creates a real need.

Recommended minimum `spec.md` body after frontmatter:

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
```

`spec.md` is a requirements and scope-control artifact. It should capture the problem, current importance, concrete requirements, success criteria, scope boundaries, constraints, assumptions, and open questions. For non-trivial work, requirements should use stable IDs such as `R1`, `R2`, and `R3` so `plan.md`, `verification.md`, and `review.md` can refer back to them unambiguously.

User stories, acceptance scenarios, and edge cases may be added when they materially clarify a user-facing feature, but they are not required for every Phase 1 spec item.

Recommended minimum `plan.md` sections:

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

`plan.md` is an implementation design artifact. It should explain the approach, relevant context, technical decisions, coarse work units, expected verification, and risks. It should not duplicate lifecycle state; `spec.md` frontmatter remains the single source of truth for `status` and `stage`.

Recommended minimum `verification.md` sections:

```markdown
# <Title> Verification

## Summary

## Planned Checks

## Results

## Manual Validation

## Skipped Checks

## Remaining Risk
```

`verification.md` is an evidence summary. It should record the checks from the plan, actual command or method results, concise evidence, skipped checks with reasons, and remaining risk. It should not become a raw terminal log or substitute for fresh-context review.

Per-check results should initially use `pass`, `fail`, `skipped`, or `blocked`.

Recommended minimum `review.md` sections:

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

`review.md` is a fresh-context findings and resolution record. It should capture the review scope, reviewers or review roles, findings with severity and evidence, how actionable findings were resolved, residual risk, and final verdict. If there are no findings, it should say so explicitly rather than omit the section.

Initial severity labels should be `P0`, `P1`, `P2`, and `P3`. Initial resolution labels should be `fixed`, `accepted`, `deferred`, `rejected`, and `open`.

### 3. Verification Model

The minimum verification model should be:

- command-backed where possible
- explicit before completion
- recorded when skipped

Recommended rules:

1. no completion claim without named verification evidence
2. verification commands belong in the plan before implementation begins
3. skipped checks require a reason
4. review does not substitute for verification
5. verification should prefer repository-native commands over agent opinion

Initial gate policy:

- `spec` is created by default unless the human explicitly says to skip it
- `plan` is created by default unless the human explicitly says to skip it
- skipped `spec` or `plan` artifacts must be recorded in the current spec item's metadata or in the relevant artifact
- `verification` is required before any completion claim
- without verification, the agent can only report an unverified result

Typical command classes:

- tests
- lint
- typecheck
- build
- targeted runtime or manual checks when automation does not exist

This follows the common pattern seen in Every, `superpowers`, and Archon-style validated workflows:
execution is not done when code exists, but when explicit checks have been satisfied.

### 4. Memory Model

The minimum memory model should be file-first and lightweight.

Recommended baseline:

- a durable learnings file for cross-session memory
- optional local notes for active work if needed later
- no hidden dependency on external state for core understanding

Why this baseline is correct:

- `oh-my-codex` shows the value of repo-local state authority
- `gstack` and Every-style compounding both reinforce that retros and learnings need to remain available
- a file-first model keeps early adoption simpler than a database or service layer

Recommended minimum rule:

- only record a learning if it would plausibly change future work

Avoid:

- dumping raw transcripts into memory files
- duplicating plan content into learnings
- turning memory into a second roadmap

### 5. Authority Model

The authority model answers: where does the repository say how work should happen here?

Recommended authority order:

1. repository-local contract files
2. repository-local plans and specs for the current change
3. starter defaults shipped by `wayrail`
4. host-specific behavior or global defaults

Implications:

- local repository files outrank global tool conventions
- `AGENTS.md` should summarize and route, not become the entire contract
- a repo-local config anchor is required later because precedence must be visible

This follows the same pressure seen in `oh-my-codex` and Archon:
local authority must be explicit, and precedence should be understandable without guesswork.

### 6. Escalation Model

The working model should explicitly tell the agent when to stop and ask for human judgment.

Recommended escalation cases:

- unclear or conflicting problem statements
- competing design directions with meaningful product tradeoffs
- risky destructive operations
- policy, legal, privacy, or security ambiguity
- plan invalidation discovered mid-implementation
- verification failure that changes the intended scope

The rule should be simple:

- agents own execution within the contract
- humans own ambiguous intent and consequential tradeoffs

## Recommended Minimum Lifecycle

The preferred core lifecycle for `wayrail` is:

`spec -> plan -> implement -> verify -> review`

This is the recommendation because it balances:

- clarity
- repeatability
- lightness
- compatibility with the benchmark projects

`compound` remains a supported memory layer rather than a mandatory initial lifecycle stage.

## Why `spec` Is Separate From `plan`

This separation should be preserved.

If `spec` and `plan` are merged too early:

- problem framing gets mixed with solution preference
- alternative approaches receive less scrutiny
- implementation details leak into what should be a stable statement of intent

`spec` is about the change being justified.
`plan` is about the change being executable.

That is a useful boundary and should remain visible in the harness.

## Why `verify` And `review` Are Separate

This separation should also be preserved.

`verify` checks whether the implementation passes explicit gates.
`review` checks whether the implementation is actually good, safe, and aligned.

If they are merged:

- passing tests gets mistaken for sound design
- same-agent reasoning bias survives to completion
- review findings become harder to preserve and track

The benchmark projects repeatedly reinforce this distinction.

## Consequences For Repository Shape

If this working model is accepted, the later repository structure should support at least these artifact classes:

- specs
- plans
- verification records or summaries
- reviews
- durable learnings

This does not yet force final path names, but it does imply that a future starter cannot stop at:

- `README.md`
- `AGENTS.md`
- `wayrail.yaml`

Those are only entry surfaces.
The working model requires homes for stage artifacts.

The current preferred artifact root is `specs/`, with one directory per spec item.

## Consequences For `AGENTS.md`

If this design is accepted, `AGENTS.md` should be a thin entrypoint that tells an agent:

- which stage model exists
- where the current change artifacts live
- where verification rules live
- where durable learnings live
- when escalation is required

It should not duplicate the full operating contract.

The accepted operating model is table-of-contents style:

- root `AGENTS.md` stays roughly under 100 lines
- `docs/` and workflow artifacts are the system of record
- specialized local rules should live in nested `AGENTS.md` or `AGENTS.override.md` only when a subdirectory needs them
- large templates, review standards, and memory policy should be linked, not copied into `AGENTS.md`

## Consequences For Skills

If this design is accepted, skills should reinforce stage transitions rather than replace them.

Examples of valid skill responsibilities later:

- help write a spec
- help draft an implementation plan
- execute a plan in bounded tasks
- run or summarize verification
- request independent review
- capture a learning after completion

Examples of invalid skill responsibilities:

- hide the stage model inside a prompt
- bypass visible artifacts
- silently collapse verify and review
- encode private conventions that are not reflected in repository files

## What This Still Leaves Open

This draft has been superseded by the Phase 1 foundation decision record for several concrete file-layout questions.
The remaining open questions are:

- how the starter entrypoints should mature after the initial script-backed workflow
- how much global configuration should exist relative to repo-local configuration
- how workflow skills should be packaged and installed across hosts

The exact starter artifact shapes, initial memory model, and script-backed spec item scaffolding are now covered in [2026-04-23 Phase 1 Foundation Decisions](./2026-04-23-phase-1-foundation-decisions.md).

## Recommendation

Adopt this draft as the current `wayrail` minimum working model for Phase 1 design work.

Then use it to drive the next two decisions in order:

1. define the artifact-to-path mapping for repository structure
2. define the starter installation surface that creates that structure

## Proposed Next Step

Write the next design document around:

`artifact layout and docs structure for the minimum working model`

That document should take the artifact classes defined here and turn them into a concrete, minimal repository shape.
