---
name: hk-plan
description: "Use when converting a ready harness-kit spec.md into an implementation plan.md. Reads a selected spec item, checks Planning Handoff readiness, performs bounded repository research, and writes only plan.md. Do not use for code implementation, verification evidence, review conclusions, creating tasks.md, or editing spec.md."
---

# hk-plan

Create the implementation plan for a ready harness-kit spec item.

## Use When

- The user asks to run `hk-plan`, create a plan, or move a ready harness-kit spec item from spec stage to plan stage.
- The input includes an explicit spec item path or an unambiguous current spec item from the conversation.
- The target spec item has `spec.md` and `plan.md`.

## Do Not Use When

- The user asks to start a new spec item; use `hk-spec`.
- The user asks to implement code.
- The user asks to verify completed work.
- The user asks to review an implementation.
- The spec is blocked before planning.
- The request would create `tasks.md`.

## Inputs

Prefer an explicit spec item path such as `specs/<id>/spec.md`.
If the conversation has exactly one unambiguous current spec item, use that path and state it.
If neither is available, ask for the spec path.

## Readiness Gate

Read `spec.md` before writing anything.
Check `Planning Handoff`.
Stop without writing when the handoff says `Blocked before hk-plan`.
Stop without writing when `Resolve Before Planning` contains unresolved questions.

## Workflow

1. Identify the target spec item.
2. Read `spec.md`.
3. Confirm the readiness gate.
4. Read the problem, requirements, success criteria, scope, constraints, assumptions, and open questions.
5. Do bounded repository research:
   - inspect relevant docs
   - inspect likely target files
   - identify local implementation and test conventions
   - identify likely verification commands
6. Classify unknowns before asking the human.
7. Write only `plan.md`.
8. Report the plan path and recommend implementation as the next action.

## Plan Authoring Rules

Write `plan.md` with these sections:

- Overview
- Requirements Trace
- Scope
- Context
- Decisions
- Implementation Units
- Verification
- Risks
- Implementation Handoff

Trace every relevant requirement or success criterion to plan coverage, or explicitly mark it out of scope with rationale.
Use coarse implementation units, not patch-level tasks.
Each implementation unit should include:

- Requirements:
- Files:
- Depends on:
- Approach:
- Verification:

## Unknown Handling

Classify unknowns before asking the human.
Human judgment is required for product behavior, scope, quality bar, security, privacy, or risk-tolerance decisions that cannot be resolved from the repository.
Technical convention questions should be resolved from repository context or focused research.
Execution-time uncertainties belong under `Risks`.

## Boundaries

Write only `plan.md`.
Do not edit source code.
Do not run implementation.
Do not collect verification evidence.
Do not write review conclusions.
Do not create `tasks.md`.
Phase 1 does not require a script for `hk-plan`; planning is judgment-heavy.

## Completion

Report the written `plan.md` path.
State whether implementation can begin.
Do not claim verification or review has happened.
