---
status: active
audience: internal-first
last_reviewed: 2026-04-22
current_phase: "Phase 1: Starter Foundation"
roadmap_owner: repository maintainer
update_when: phase-start, phase-end, boundary-change, research-shift
---

# Harness Kit Roadmap

> Internal-first, public-readable roadmap for `harness-kit`.
>
> This is a phase-based product roadmap, not a release plan and not a task backlog.
> Detailed feature design belongs in [docs/plans/](../plans/).
> Research evidence belongs in [docs/research/](../research/).

## Related Docs

- [Phase details](./phases/README.md)
- [Research overview](../research/comparisons/overview.md)
- [Adoption notes](../research/comparisons/adoption-notes.md)
- [Research archive](../research/README.md)
- [Implementation plans](../plans/)

## Roadmap Status

- Status: active
- Current phase: `Phase 1: Starter Foundation`
- Owner: repository maintainer
- Review cadence: at phase start, at phase end, and during monthly maintenance review
- Update triggers: product-boundary change, research-driven direction change, or phase transition

## North Star

`harness-kit` should let one person run many agent-driven projects with the same working contract, verification discipline, and compounding loop, without rebuilding the harness from scratch each time.

In its mature form, `harness-kit` should make a new or existing repository immediately legible to both humans and coding agents by installing:

- a repo-local agent contract
- a standard workflow with named stage boundaries
- explicit verification gates
- lightweight durable state and learnings
- a narrow adapter layer for host-specific integration

## Outcome Signals

The roadmap is succeeding if these outcomes become true in practice:

- new repositories no longer require re-explaining the same harness rules from scratch
- existing repositories can be adopted into the same working model without bespoke redesign
- agents can determine how to work from repository files instead of hidden session context
- completion claims become easier to verify and harder to bluff
- useful learnings survive long enough to improve later work across multiple repositories

These are operating outcomes, not date promises and not a feature checklist.

## Problem Statement

The problem is not that coding agents are unavailable. The problem is that the surrounding working system drifts from project to project.

Today, the same person may run several repositories with:

- different startup structure
- different agent instructions
- different completion criteria
- different verification commands
- different documentation expectations
- different ways of preserving learnings

That creates recurring waste:

- strong patterns must be manually reintroduced into each new project
- project quality depends too much on remembered setup rituals
- agent behavior varies because the local contract varies
- session learnings do not reliably compound across projects
- existing repositories are hard to standardize after they have already drifted

`harness-kit` exists to standardize the working model around the agent, not to compete with the model itself.

## Product Definition

`harness-kit` is a repo-local starter and contract system.

Its core job is to install, validate, and evolve a standard agent working model across many repositories.

At minimum, the product should be able to:

- bootstrap a new repository into the `harness-kit` working model
- adopt an existing repository into that same model
- make the local contract visible and inspectable in files
- validate whether the repository still satisfies the contract
- preserve lightweight state and learnings that improve later work

The product should remain internal-first in decision making, while staying clean enough that an outside user can read the repository and understand how to use it.

## Current Planning Posture

This is an internal roadmap for a public repository.

That means:

- internal repeated use is the planning authority
- public readability is required
- public adoption is welcome but not the optimization target
- a future public-friendly packaging story can emerge only after the internal system is dependable

## Who It Is For

### Primary User

The primary user is one operator managing multiple agent-first software projects who wants the same standards, stage boundaries, and verification rules everywhere.

### Primary Agent

The primary agent is a coding agent operating inside one repository at a time and needing a clear answer to:

- how work begins
- which stage the repository is in
- what artifact each stage produces
- what evidence is required before claiming completion
- where state and learnings live
- which rules are local to the repository versus inherited defaults

### Secondary Audience

The repository is public, so a secondary audience exists:

- collaborators
- curious users
- future adopters

But their needs are secondary to the internal product goal. Public readability matters. Public-driven scope does not.

## Non-Goals

The roadmap intentionally does not target the following in the early system:

- a full multi-agent runtime platform
- a dashboard or control-plane UI
- database-backed workflow execution history
- long-running background orchestration as a core requirement
- a huge built-in role catalog
- broad host compatibility before the core local contract is stable
- a generic marketplace or plugin ecosystem
- replacing existing coding agents with a new model-facing shell

## Design Principles

### 1. Internal First, Public Readable

The system should be optimized for real repeated use across the owner's projects.
Because the repository is public, the artifacts should still be understandable without private context.

### 2. Repo-Local Authority

The repository should contain the canonical local contract.
Global defaults may exist, but the local repository must remain the place where an agent can determine how to work here.

### 3. Stage Boundaries Must Be Explicit

Work should move through named stages with different expected artifacts.
The system should prefer explicit handoffs over conversational drift.

### 4. Verification Before Completion

The harness should distrust self-reported completion.
Completion should require visible verification commands, checks, or artifacts.

### 5. Bootstrap and Runtime Must Stay Distinct

Project setup, validation, and upgrade concerns must not be confused with a full runtime substrate.
`harness-kit` should first standardize repository shape and working rules before it grows heavier operational features.

### 6. Compounding Must Be Lightweight and Durable

Learnings should survive across sessions and repositories, but the mechanism should stay simple enough to adopt widely.
Files beat hidden state in early phases.

### 7. Narrow Core, Thin Adapters

The core contract should stay stable and host-agnostic where possible.
Host-specific integration should be added through thin adapters, not by polluting the core model.

### 8. Roadmap Is Outcome-Based

This roadmap defines capabilities and exit criteria, not a dated promise.
Detailed implementation order belongs in plan documents once a phase or feature is chosen.

## Product Shape

The product should mature in layers.

### Canonical Layers

- `starter layer`: creates or standardizes repository structure and base documents
- `contract layer`: defines how agents should work inside the repository
- `verification layer`: defines required evidence before stage completion
- `compounding layer`: preserves useful learnings and local state
- `adapter layer`: connects the core contract to specific hosts without redefining the model

### Core Artifacts Expected Over Time

- repo-local contract files
- workflow and handoff artifacts
- standard verification commands
- durable learning or checkpoint files
- a narrow configuration file describing repository-level harness choices

## Why The Phases Are Ordered This Way

The sequence is deliberate.

- `Phase 1` comes first because repository entry and file layout must exist before anything else can be standardized
- `Phase 2` comes next because the local contract has to be legible before verification can be enforced
- `Phase 3` follows because gates and compounding only work after the contract and stage model are clear
- `Phase 4` exists because a good exemplar repository is not yet a reusable multi-project system
- `Phase 5` is last because internal completeness should be earned by repeated adoption, not declared early

If a proposed feature skips these dependencies, it probably belongs in a later phase or outside the core.

## Phase Roadmap

This roadmap is intentionally phase-based rather than date-based.
Each phase is complete when its exit criteria are met, not when a calendar target arrives.

Current working emphasis: `Phase 1` and `Phase 2`.
The system is not yet mature enough to treat later phases as commitments.

### Phase 1: Starter Foundation

Goal: make `harness-kit` capable of standardizing repository startup.

This phase should establish:

- the canonical repository-side install surface
- the first version of the repo-local file layout
- a clear distinction between new-project bootstrap and existing-project adoption
- a canonical roadmap, research, and planning document structure
- an initial command surface for installing the starter, whether that starts as a CLI or a thin scripted entry point

By the end of this phase, `harness-kit` should answer:

- how a repository enters the system
- which files are considered part of the installed harness
- what the minimum supported repository shape is

Success signals:

- Starting a new repository no longer depends on reconstructing the same harness setup from memory.
- Existing repositories can be judged against one visible starter model instead of ad hoc setup habits.

### Phase 2: Agent Contract

Goal: define the standard local working contract for agents and humans.

This phase should establish:

- canonical local instructions and ownership boundaries
- named workflow stages
- expected stage artifacts and handoff rules
- explicit distinction between inherited defaults and repo-local overrides
- a narrow configuration precedence model

By the end of this phase, an agent entering a repository should be able to determine how to work there without relying on hidden chat context.

Success signals:

- A new agent session can infer the local working model from repository files alone.
- Basic agent instructions stop drifting heavily from project to project because the local contract is explicit.

### Phase 3: Verification and Compounding

Goal: make completion claims trustworthy and learnings durable.

This phase should establish:

- required verification gates and completion evidence
- standard command contracts such as lint, test, build, and typecheck where relevant
- lightweight persistent learnings, checkpoints, or wiki-like local state
- a clear distinction between setup validation and execution readiness

By the end of this phase, `harness-kit` should no longer be just a starter. It should actively reduce quality drift over time.

Success signals:

- Completion claims without verification evidence become abnormal in repositories using the harness.
- Useful learnings survive across sessions without depending on remembered chat context.

### Phase 4: Multi-Project Adoption

Goal: make the system work across a portfolio of repositories instead of one exemplar repository.

This phase should establish:

- adoption guidance for existing repositories
- upgrade and migration discipline when the standard evolves
- minimal variability points for project type or stack
- documented patterns for where customization is allowed versus forbidden

By the end of this phase, the same owner should be able to roll the working model across multiple repositories with low manual translation cost.

Success signals:

- Adopting the harness into another repository becomes a bounded migration instead of a fresh process design exercise.
- Standard updates can move across repositories without bespoke rewriting each time.

### Phase 5: Internal Complete System

Goal: make `harness-kit` the default internal way to start, standardize, and maintain agent-first repositories.

This phase should establish:

- a stable internal product boundary
- a well-defined maintenance and upgrade story
- a strong enough contract that new project setup does not require rediscovering process decisions
- a clear position on which optional features remain outside the core

At this point, `harness-kit` should behave like a dependable internal operating standard for repositories, even though it remains implemented as a file-first public repository.

Success signals:

- New internal repositories default to the harness instead of inventing their own working model.
- Core boundary debates become less frequent because the standard is stable and legible.

## Phase Exit Criteria

The roadmap stays useful only if each phase has a clear definition of done.

### Phase 1 Exit Criteria

- A canonical starter entry point exists and can place a repository onto one starter path.
- The installed repository structure is documented well enough that setup no longer depends on remembered rituals.
- The difference between bootstrap and adoption is explicit enough to choose the right path without guesswork.
- The roadmap, research, and planning document layers are in place and usable as separate decision surfaces.

### Phase 2 Exit Criteria

- A repo-local contract format exists and is stable enough to guide routine agent work.
- Workflow stages and required artifacts are named well enough to reduce ambiguous handoffs.
- Local versus inherited configuration boundaries are documented well enough to avoid hidden authority.
- An agent can infer expected behavior from repository files alone with minimal chat-only context.

### Phase 3 Exit Criteria

- Completion gates require visible evidence and make unverified completion claims exceptional.
- Verification commands are part of the working contract and are usable during normal stage completion.
- A lightweight durable compounding mechanism exists and carries useful learnings between sessions.
- The system distinguishes setup health from runtime readiness in a way users and agents can act on.

### Phase 4 Exit Criteria

- Existing repositories can be adopted with repeatable guidance instead of bespoke interpretation.
- Standard evolution has an upgrade path that does not require manual rediscovery of the model.
- Variability points are intentionally bounded so customization does not erase the common system.
- Multi-project reuse is materially easier than ad hoc manual setup.

### Phase 5 Exit Criteria

- `harness-kit` is the default starting point for the owner's new repositories.
- The core boundary is stable enough that optional features can be judged against it.
- The system reduces repeated process design work across projects in practice.

## Decision Rules

Use these rules when choosing what to build next.

### Build Now If

- it strengthens repo-local clarity
- it reduces repeated setup work across projects
- it makes stage transitions or completion evidence more explicit
- it improves multi-project reuse without adding much runtime weight
- it makes future agent work more legible from repository files alone
- it preserves the file-first public readability of the system

### Defer If

- it mainly improves presentation rather than working discipline
- it depends on a large runtime substrate
- it introduces broad compatibility obligations before the core contract stabilizes
- it adds many roles, hooks, or integrations without improving the common model
- it solves a one-project edge case by complicating the shared core
- it assumes a packaged public product surface before internal repeated use proves the core

## Risks and Failure Modes

The main risks are strategic, not only technical.

### 1. Becoming a Platform Too Early

The project can easily overgrow into a runtime platform before the starter and contract layers are solid.

### 2. Recreating Prompt Pack Sprawl

If too many skills, roles, or project-specific exceptions enter the core too early, the same inconsistency problem returns inside `harness-kit`.

### 3. Confusing Roadmap With Backlog

If this document becomes a feature list, it will stop helping with product direction.
Detailed design and execution should stay in [docs/plans/](../plans/).

### 4. Hidden State

If important behavior depends on undocumented chat conventions or machine-local setup, the system will stop being portable across repositories.

### 5. Public Pressure Distorting Internal Priorities

Because the repository is public, there is a risk of prematurely optimizing for outside expectations.
Public readability is good. Public roadmap pressure is not the planning authority.

## How To Use This Roadmap

Use this document to decide direction, not to track day-to-day execution.

- Review this roadmap when a phase starts, when a phase ends, and whenever a major product-boundary decision is made.
- Recheck it during monthly maintenance review so it does not drift behind research or implementation plans.
- When the product boundary changes, update this roadmap first or alongside the related design change.
- When a phase needs deeper treatment, add a document under [docs/roadmap/phases/](./phases/README.md).
- When a concrete capability is chosen for implementation, write a design in [docs/plans/](../plans/).
- When a roadmap statement depends on evidence, keep that evidence in [docs/research/](../research/).

If a proposed feature cannot be explained as advancing one of the roadmap phases or protecting one of the design principles, it probably does not belong in the core yet.

## Source Basis

This roadmap is grounded in the research archive in [docs/research/](../research/), especially:

- [research overview](../research/comparisons/overview.md)
- [adoption notes](../research/comparisons/adoption-notes.md)

The roadmap also follows common roadmap best practices:

- keep roadmap and plan separate
- organize around goals, phases, and outcomes rather than a raw feature backlog
- treat the roadmap as a living document
- avoid overcommitting to rigid dates while the product boundary is still being defined
