# hk-plan Skill Contract Plan

## Overview

Implement `hk-plan` as the second repo-local harness-kit lifecycle skill.
It should consume a ready `spec.md`, perform bounded repository research, and write the corresponding `plan.md` as an implementation-design handoff.

This plan keeps Phase 1 deliberately light: `hk-plan` is a `SKILL.md` workflow plus minimal agent metadata, not a deterministic script or task generator.

## Requirements Trace

| Spec ID | Requirement | Plan Coverage | Verification |
| --- | --- | --- | --- |
| R1 | Starter contains `template/.agents/skills/hk-plan/` | Unit 1 creates skill directory | File existence tests |
| R2 | Agent Skills frontmatter | Unit 1 writes `SKILL.md` frontmatter | Contract tests parse text |
| R3 | Narrow trigger | Unit 1 writes description | Contract tests assert trigger/negative scope |
| R4 | Explicit or unambiguous spec item | Unit 1 workflow step | Contract tests assert path requirement |
| R5 | Read selected `spec.md` first | Unit 1 workflow step | Contract tests assert ordering language |
| R6 | Check `Planning Handoff` | Unit 1 readiness section | Contract tests assert handoff rule |
| R7 | Stop when blocked | Unit 1 readiness section | Contract tests assert blocked behavior |
| R8 | Read core spec sections | Unit 1 workflow step | Contract tests assert required sections |
| R9-R10 | Bounded repository research | Unit 1 research section | Contract tests assert research targets |
| R11-R12 | Write only `plan.md`; no code/verify/review | Unit 1 boundaries | Contract tests assert write boundary |
| R13 | Required `plan.md` sections | Unit 1 plan authoring rules | Contract tests assert section list |
| R14-R16 | Trace and coarse units | Unit 1 plan authoring rules | Contract tests assert trace/unit fields |
| R17-R20 | Unknown classification | Unit 1 decision rules | Contract tests assert human-vs-technical split |
| R21 | No `tasks.md` | Unit 1 boundaries | Contract tests assert prohibition |
| R22-R23 | No Phase 1 script requirement | Unit 1 and Unit 3 | Contract tests assert no script dependency |
| R24 | Test coverage | Unit 3 adds tests | `uvx pytest` and unittest |

## Scope

In scope for this implementation pass:

- `template/.agents/skills/hk-plan/SKILL.md`
- `template/.agents/skills/hk-plan/agents/openai.yaml`
- starter inventory updates so bootstrap/adopt install `hk-plan`
- dedicated `hk-plan` skill contract tests
- updating this spec item's verification/review artifacts later in the lifecycle

Out of scope for this pass:

- `template/.agents/skills/hk-plan/scripts/`
- deterministic plan-generation scripts
- `tasks.md`
- implementation execution tooling
- `hk-verify` or `hk-review`
- public plugin packaging
- global user skill installation
- changing the existing `plan.md` template section set

## Context

Relevant source files:

- `specs/20260501-0302-hk-plan-skill-contract/spec.md`
- `template/.agents/skills/hk-spec/SKILL.md`
- `template/.agents/skills/hk-spec/agents/openai.yaml`
- `scripts/harness-kit/_lib/starter.py`
- `tests/test_starter_scripts.py`
- `tests/test_hk_spec_skill.py`
- `template/specs/_templates/plan.md`
- `specs/_templates/plan.md`

Existing conventions:

- Repo-local skills live under `template/.agents/skills/<name>/`.
- Starter inventory is duplicated in `scripts/harness-kit/_lib/starter.py` and `tests/test_starter_scripts.py`.
- Skill-specific tests should live in a dedicated test file.
- Current tests use Python `unittest`, with `uvx pytest` as the normal runner.
- `hk-spec` includes a script because scaffolding is deterministic. `hk-plan` should not copy that pattern unless a deterministic need exists.

Dogfooding note:

- Running `hk-spec` inside this source repo exposed that root `specs/_templates/` was missing while downstream `template/specs/_templates/` existed.
- Root `specs/_templates/` now exists so harness-kit can use its own repo-level skill contract against itself.

## Decisions

| Decision | Rationale | Alternatives Considered | Requirements Served |
| --- | --- | --- | --- |
| Implement `hk-plan` as skill prose plus metadata only | Planning is judgment-heavy and repo-context-dependent | Add a plan writer script now | R9-R23 |
| Keep trigger narrow | Avoid accidental use for implementation, verification, or review | Broad lifecycle assistant skill | R3, R11-R12 |
| Require explicit or unambiguous spec path | Prevents planning the wrong spec item in a repo with many specs | Auto-pick latest spec | R4 |
| Stop on blocked specs | Preserves the spec-to-plan readiness gate | Plan around unresolved blockers | R6-R7 |
| Require bounded repository research | Makes plans actionable against actual files and tests | Write plan from spec alone | R9-R10, SC3 |
| Use coarse implementation units | Keeps `plan.md` as implementation design, not task database | Generate patch-level checklist or `tasks.md` | R15-R16, R21 |
| Add dedicated tests | Keeps skill contract regressions visible | Only starter inventory tests | R24 |

## Implementation Units

- [ ] Unit 1: Add `hk-plan` skill source
  - Requirements: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23
  - Files:
    - Create `template/.agents/skills/hk-plan/SKILL.md`
    - Create `template/.agents/skills/hk-plan/agents/openai.yaml`
  - Depends on: none
  - Approach:
    - Mirror the concise style of `hk-spec`.
    - Put `name: hk-plan` and a narrow description in frontmatter.
    - Include sections for Use When, Do Not Use When, Inputs, Readiness Gate, Workflow, Plan Authoring Rules, Unknown Handling, Boundaries, and Completion.
    - State that the skill writes only `plan.md`.
    - State that it must not create `tasks.md`.
    - State that Phase 1 has no required script.
  - Verification:
    - Dedicated tests inspect frontmatter and required body rules.

- [ ] Unit 2: Add `hk-plan` to starter inventory
  - Requirements: R1, R24
  - Files:
    - Modify `scripts/harness-kit/_lib/starter.py`
    - Modify `tests/test_starter_scripts.py`
  - Depends on: Unit 1
  - Approach:
    - Add `.agents/skills/hk-plan/SKILL.md` and `.agents/skills/hk-plan/agents/openai.yaml` to both required template file lists.
    - Do not add executable-bit assertions because `hk-plan` has no script in Phase 1.
  - Verification:
    - Starter template file test passes.
    - Bootstrap fixture creates the `hk-plan` files.

- [ ] Unit 3: Add dedicated `hk-plan` contract tests
  - Requirements: R2-R24
  - Files:
    - Create `tests/test_hk_plan_skill.py`
  - Depends on: Unit 1
  - Approach:
    - Assert skill files exist.
    - Assert frontmatter has `name: hk-plan`.
    - Assert trigger text mentions converting a ready harness-kit `spec.md` into `plan.md`.
    - Assert body requires explicit or unambiguous spec path.
    - Assert body requires checking `Planning Handoff` and stopping on blocked specs.
    - Assert body requires bounded repository research.
    - Assert body says to write only `plan.md`.
    - Assert body prohibits implementation, verification evidence, review conclusions, and `tasks.md`.
    - Assert body says no Phase 1 script is required.
  - Verification:
    - `uvx pytest tests/test_hk_plan_skill.py tests/test_starter_scripts.py`

- [ ] Unit 4: Verify and update lifecycle artifacts
  - Requirements: R24, SC1-SC8
  - Files:
    - Modify `specs/20260501-0302-hk-plan-skill-contract/verification.md`
    - Later modify `specs/20260501-0302-hk-plan-skill-contract/review.md`
  - Depends on: Units 1-3
  - Approach:
    - Run focused pytest checks.
    - Run full unittest discovery if focused checks pass.
    - Record skipped live Codex invocation if not executed.
  - Verification:
    - `uvx pytest tests/test_hk_plan_skill.py tests/test_starter_scripts.py`
    - `python -m unittest discover -s tests`

## Verification

Planned checks:

- `uvx pytest tests/test_hk_plan_skill.py tests/test_starter_scripts.py`
- `python -m unittest discover -s tests`
- Manual inspection of `template/.agents/skills/hk-plan/SKILL.md`
- Manual inspection that no `template/.agents/skills/hk-plan/scripts/` is required or referenced as required

Expected evidence:

- focused pytest run passes
- full unittest discovery passes
- starter bootstrap/adopt inventory includes `hk-plan`
- `hk-plan` skill contract remains planning-only

## Risks

- Trigger wording could be too broad and make the skill activate for implementation work.
  - Mitigation: contract tests should assert negative-scope wording.
- The skill may become too long and violate progressive-disclosure discipline.
  - Mitigation: keep `SKILL.md` under a small section set and avoid examples that are not needed every run.
- No script means less machine-enforced behavior.
  - Mitigation: Phase 1 tests enforce the workflow contract; future validation helper can be added if repeated failures appear.
- A plan can still be low quality if the agent skips repo research.
  - Mitigation: make bounded research a required workflow step and completion condition.

## Implementation Handoff

Status: Ready for implementation
Plan path: specs/20260501-0302-hk-plan-skill-contract/plan.md
Spec path: specs/20260501-0302-hk-plan-skill-contract/spec.md
Implementation order: Unit 1, Unit 2, Unit 3, Unit 4
Recommended next action: implement Units 1-3, then run planned verification and record results.
