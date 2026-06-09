---
spec_id: 20260501-0302-wr-plan-skill-contract
title: wr-plan Skill Contract
status: active
stage: spec
created_at: 2026-05-01 03:02
timezone: Asia/Seoul
---

# wr-plan Skill Contract

## Problem

`wayrail` can now create a spec item through `wr-spec`, but the next lifecycle transition is still manual.
After `spec.md` is ready, a human or agent must decide how to convert requirements, success criteria, constraints, and open questions into an implementation-oriented `plan.md`.

Without `wr-plan`, the workflow has a repeatable entry point but no repeatable planning contract.
That leaves implementation plans vulnerable to two failure modes:

- plans that jump straight into patch-level task lists without checking whether the spec is ready
- plans that are generic prose rather than a concrete handoff grounded in repository files, tests, and implementation constraints

## Why Now

The previous `wr-spec` item closed and implemented the first lifecycle skill.
It also established the pattern that each lifecycle skill should own one stage:

- `wr-spec` starts a new item and authors only `spec.md`
- `wr-plan` should consume a ready `spec.md` and author only `plan.md`
- later skills own verification and review artifacts

The next product step is therefore to define `wr-plan` before implementing `wr-verify` or `wr-review`.
This keeps the workflow usable in sequence and lets wayrail dogfood its own lifecycle on the next changes.

## Research Basis

Local project documents already contain a closed planning direction:

- `docs/plans/2026-04-23-phase-1-foundation-decisions.md` says `wr-plan` should be a design-and-handoff skill, not a task generator.
- `docs/roadmap/phases/phase-1-starter-foundation.md` says `wr-plan` should stop when `spec.md` is not ready, do bounded repository research, name relevant files and test conventions, and translate requirements into coarse implementation units.
- Existing plan artifacts such as `specs/20260429-0045-repo-local-starter-contract/plan.md` and `specs/20260430-0200-wr-spec-skill-contract/plan.md` show the target shape: overview, requirements trace, scope, context, decisions, implementation units, verification expectations, risks, and implementation handoff.

The key product insight is that `wr-plan` should not create another task system in Phase 1.
It should produce a single implementation design artifact that is good enough for a fresh agent or human to execute.

## Requirements

- `R1`: `wr-plan` MUST be present in the starter template at `template/.agents/skills/wr-plan/`.
- `R2`: `template/.agents/skills/wr-plan/SKILL.md` MUST use Agent Skills-compatible frontmatter with `name: wr-plan`.
- `R3`: The skill description MUST trigger only when converting a ready wayrail `spec.md` into an implementation `plan.md`.
- `R4`: The skill MUST require an explicit spec item path or an unambiguous current spec item from the conversation.
- `R5`: `wr-plan` MUST read the selected `spec.md` before writing `plan.md`.
- `R6`: `wr-plan` MUST check the `Planning Handoff` section before planning.
- `R7`: `wr-plan` MUST stop without writing a plan when the spec is marked blocked before `wr-plan` or when `Resolve Before Planning` contains unresolved questions.
- `R8`: `wr-plan` MUST read the spec sections that define problem, requirements, success criteria, scope, constraints, assumptions, and open questions.
- `R9`: `wr-plan` MUST perform bounded repository research before writing the plan.
- `R10`: Bounded repository research MUST include relevant docs, likely target files, local conventions, and likely verification commands or test locations.
- `R11`: `wr-plan` MUST write only the selected spec item's `plan.md`.
- `R12`: `wr-plan` MUST NOT edit source code, run implementation, run verification evidence collection, or write review conclusions.
- `R13`: `plan.md` MUST include overview, requirements trace, scope, context, decisions, implementation units, verification, risks, and implementation handoff.
- `R14`: Requirements and success criteria from `spec.md` MUST be traced to plan coverage or explicitly marked out of scope with rationale.
- `R15`: Implementation units MUST be coarse enough to guide execution without becoming patch-level task lists.
- `R16`: Implementation units SHOULD include requirement references, expected files or areas, dependencies, approach, and expected verification.
- `R17`: `wr-plan` MUST classify unknowns rather than immediately asking the user.
- `R18`: Human questions are required only for product behavior, scope, quality bar, security, privacy, or risk-tolerance decisions that cannot be resolved from the repo.
- `R19`: Technical convention questions SHOULD be resolved through repository context or focused research.
- `R20`: Execution-time uncertainties SHOULD be recorded under `Risks`.
- `R21`: Phase 1 `wr-plan` MUST NOT create `tasks.md` or a separate task-generation artifact.
- `R22`: Phase 1 `wr-plan` MUST NOT require a deterministic script; planning is judgment-heavy and can be implemented as a concise `SKILL.md` workflow.
- `R23`: If a future helper script is added, it MUST be scoped to validation or formatting and must not replace plan authoring judgment.
- `R24`: Tests MUST verify the starter includes the `wr-plan` skill and that its skill contract contains the readiness, research, write-boundary, and no-`tasks.md` rules.

## Success Criteria

- `SC1`: A user or agent can invoke `wr-plan` against a ready spec item and receive a useful `plan.md` without remembering the planning checklist.
- `SC2`: `wr-plan` refuses to proceed when the spec handoff says planning is blocked.
- `SC3`: The resulting plan names relevant repository context instead of remaining generic.
- `SC4`: The resulting plan traces requirements to implementation units and verification expectations.
- `SC5`: The plan can be handed to a fresh implementer without rereading the full discussion history.
- `SC6`: `wr-plan` does not write code, collect verification evidence, perform review, or create `tasks.md`.
- `SC7`: The skill body stays concise and suitable for progressive disclosure.
- `SC8`: The implementation can be tested without requiring Codex itself to execute the skill.

## Scope

In scope:

- starter-template `wr-plan` skill layout
- `SKILL.md` trigger and planning workflow instructions
- readiness checks against `spec.md`
- bounded repository research rules
- `plan.md` authoring rules
- requirement trace and implementation handoff expectations
- starter inventory and skill-contract tests

Out of scope:

- implementing `wr-verify` or `wr-review`
- implementation execution
- verification evidence collection
- review conclusions
- separate `tasks.md`
- public plugin packaging
- global user installation
- automatic plan generation by deterministic script
- broad rewrite of existing plan templates

## Constraints

- `wr-plan` must preserve the existing artifact model: `specs/<YYYYMMDD-HHMM-short-slug>/plan.md`.
- `wr-plan` must treat `spec.md` as the source of truth for the current work item.
- `wr-plan` must keep `plan.md` focused on implementation design, not lifecycle state.
- `wr-plan` must be repo-local and installed through the starter template in Phase 1.
- The generated or authored plan must remain readable and editable by humans.
- The implementation should avoid introducing a task database, background runner, dashboard, or orchestration runtime.

## Assumptions

- `A1`: `template/.agents/skills/wr-plan/` is the canonical Phase 1 repo-local installation source.
- `A2`: The existing `plan.md` template section set is sufficient for Phase 1.
- `A3`: A script is not necessary for Phase 1 because the hard part is judgment, not deterministic scaffolding.
- `A4`: Existing repository tests can validate skill presence and contract wording without a live Codex runtime.
- `A5`: If a plan already contains meaningful non-stub content, `wr-plan` should avoid overwriting it unless the user explicitly asks to replace or revise it.

## Open Questions

### Resolve Before Planning

None.

### Deferred to wr-plan

None.

## Planning Handoff

Status: Ready for wr-plan
Spec path: specs/20260501-0302-wr-plan-skill-contract/spec.md
Open questions: none blocking planning
Key assumptions: A1, A2, A3, A4, A5
Requirement index: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24
Recommended next action: wr-plan

## Sources

- Local: `docs/plans/2026-04-23-phase-1-foundation-decisions.md`
- Local: `docs/roadmap/phases/phase-1-starter-foundation.md`
- Local: `specs/20260429-0045-repo-local-starter-contract/plan.md`
- Local: `specs/20260430-0200-wr-spec-skill-contract/spec.md`
- Local: `specs/20260430-0200-wr-spec-skill-contract/plan.md`
