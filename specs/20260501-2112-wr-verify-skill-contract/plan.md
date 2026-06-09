# wr-verify Skill Contract Plan

## Overview

Implement `wr-verify` as the third repo-local wayrail lifecycle skill.
It should consume an implemented spec item, read `spec.md` and `plan.md`, run or classify the planned verification checks, and write the corresponding `verification.md` as a concise evidence handoff.

This plan keeps Phase 1 intentionally light: `wr-verify` is a `SKILL.md` workflow plus minimal agent metadata, not a deterministic verification runner, QA subsystem, or code-fixing tool.

## Requirements Trace

| Spec ID | Requirement | Plan Coverage | Verification |
| --- | --- | --- | --- |
| R1 | Starter contains `template/.agents/skills/wr-verify/` | Unit 1 creates skill directory | File existence tests |
| R2 | Agent Skills frontmatter | Unit 1 writes `SKILL.md` frontmatter | Contract tests parse text |
| R3 | Narrow trigger | Unit 1 writes description | Contract tests assert trigger/negative scope |
| R4 | Explicit or unambiguous spec item | Unit 1 inputs section | Contract tests assert path requirement |
| R5 | Read `spec.md` and `plan.md` first | Unit 1 workflow | Contract tests assert required inputs |
| R6-R7 | Check `Implementation Handoff`; stop when not ready | Unit 1 readiness gate | Contract tests assert handoff and stop rules |
| R8 | Extract planned checks and expected outcomes | Unit 1 workflow | Contract tests assert extraction rules |
| R9-R14 | Fresh planned command execution, substitution, skipped/blocked handling | Unit 1 verification workflow | Contract tests assert freshness and substitution rules |
| R15-R16 | Per-check and overall labels | Unit 1 result model | Contract tests assert labels |
| R17-R19 | Write only `verification.md`; no fixes/review/waivers | Unit 1 boundaries | Contract tests assert write boundary |
| R20-R21 | Recommend return to implementation or continue to review | Unit 1 completion rules | Contract tests assert next-action language |
| R22 | Required `verification.md` sections | Unit 1 authoring rules | Contract tests assert section list |
| R23 | Avoid raw transcript dumping | Unit 1 evidence rules | Contract tests assert concise-evidence rule |
| R24-R25 | Skipped/blocked/manual validation details | Unit 1 authoring rules | Contract tests assert required fields |
| R26-R27 | Missing checks and command derivation order | Unit 1 workflow | Contract tests assert derivation order |
| R28-R29 | No required Phase 1 script | Unit 1 and Unit 3 | Contract tests assert no script dependency |
| R30 | Test coverage | Unit 3 adds tests | `uvx pytest` and unittest |

## Scope

In scope for this implementation pass:

- `template/.agents/skills/wr-verify/SKILL.md`
- `template/.agents/skills/wr-verify/agents/openai.yaml`
- starter inventory updates so bootstrap/adopt install `wr-verify`
- dedicated `wr-verify` skill contract tests
- updating this spec item's verification/review artifacts later in the lifecycle

Out of scope for this pass:

- `template/.agents/skills/wr-verify/scripts/`
- deterministic verification runner scripts
- code implementation or repair tooling
- browser QA automation setup
- separate evidence artifact directories
- `tasks.md` verification
- `wr-review`
- public plugin packaging
- global user skill installation
- changing the existing `verification.md` template section set

## Context

Relevant source files:

- `specs/20260501-2112-wr-verify-skill-contract/spec.md`
- `template/.agents/skills/wr-plan/SKILL.md`
- `template/.agents/skills/wr-plan/agents/openai.yaml`
- `template/.agents/skills/wr-spec/SKILL.md`
- `scripts/wayrail/_lib/starter.py`
- `tests/test_starter_scripts.py`
- `tests/test_wr_plan_skill.py`
- `tests/test_wr_spec_skill.py`
- `template/specs/_templates/verification.md`
- `specs/_templates/verification.md`
- `template/AGENTS.md`

Existing conventions:

- Repo-local skills live under `template/.agents/skills/<name>/`.
- Each skill has `SKILL.md` and `agents/openai.yaml`.
- Deterministic scripts are added only when the stage has a deterministic operation that benefits from tooling.
- Starter inventory is duplicated in `scripts/wayrail/_lib/starter.py` and `tests/test_starter_scripts.py`.
- Skill-specific contract tests live in dedicated `tests/test_wr_<stage>_skill.py` files.
- Current tests use Python `unittest`, with `uvx pytest` as the normal runner.

Local design context:

- `wr-plan` already records expected verification commands and outcomes in `plan.md`.
- `wr-verify` should consume those expectations and record evidence in `verification.md`.
- `template/AGENTS.md` already instructs agents not to silently skip verification or review before completion claims.

## Decisions

| Decision | Rationale | Alternatives Considered | Requirements Served |
| --- | --- | --- | --- |
| Implement `wr-verify` as skill prose plus metadata only | Verification requires command execution and evidence judgment, not scaffolding | Add a command runner script now | R8-R29 |
| Keep trigger narrow | Avoid accidental use for implementation fixes or review | Broad "finish work" skill | R3, R17-R19 |
| Require explicit or unambiguous spec item | Prevents verifying the wrong spec in a repo with many active specs | Auto-pick latest spec | R4 |
| Gate on `Implementation Handoff` | Ensures verification starts only after a plan is ready and implementation is present | Verify directly from `spec.md` | R5-R8 |
| Use planned checks as primary source | Keeps verification tied to the plan instead of random broad test suites | Always run all discoverable tests | R8-R14, R26-R27 |
| Allow safe independent checks after failure | Gives a fuller evidence picture without hiding failure | Stop after first failed command | R11, SC2 |
| Keep raw logs out of `verification.md` by default | Keeps the artifact readable and reviewable | Paste full terminal transcripts | R23 |
| Separate verify from review and waiver approval | Preserves lifecycle boundaries and human risk ownership | Let verify approve completion | R18-R21 |
| Add dedicated tests | Makes the skill contract regressions visible | Only starter inventory tests | R30 |

## Implementation Units

- [ ] Unit 1: Add `wr-verify` skill source
  - Requirements: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29
  - Files:
    - Create `template/.agents/skills/wr-verify/SKILL.md`
    - Create `template/.agents/skills/wr-verify/agents/openai.yaml`
  - Depends on: none
  - Approach:
    - Mirror the concise structure of `wr-plan`.
    - Put `name: wr-verify` and a narrow description in frontmatter.
    - Include sections for Use When, Do Not Use When, Inputs, Readiness Gate, Workflow, Result Labels, Verification Authoring Rules, Boundaries, and Completion.
    - State that the skill reads `spec.md` and `plan.md`, checks `Implementation Handoff`, runs planned checks fresh, records concise evidence, and writes only `verification.md`.
    - State per-check labels: `pass`, `fail`, `skipped`, `blocked`.
    - State overall verdicts: `pass`, `fail`, `partial`, `blocked`.
    - State that failed/skipped/blocked checks require reason and residual risk.
    - State that the skill does not edit code, approve waivers, or write review conclusions.
    - State that Phase 1 has no required script.
  - Verification:
    - Dedicated tests inspect frontmatter and required body rules.

- [ ] Unit 2: Add `wr-verify` to starter inventory
  - Requirements: R1, R30
  - Files:
    - Modify `scripts/wayrail/_lib/starter.py`
    - Modify `tests/test_starter_scripts.py`
  - Depends on: Unit 1
  - Approach:
    - Add `.agents/skills/wr-verify/SKILL.md` and `.agents/skills/wr-verify/agents/openai.yaml` to both required template file lists.
    - Do not add executable-bit assertions because `wr-verify` has no script in Phase 1.
  - Verification:
    - Starter template file test passes.
    - Bootstrap fixture creates the `wr-verify` files.

- [ ] Unit 3: Add dedicated `wr-verify` contract tests
  - Requirements: R2-R30
  - Files:
    - Create `tests/test_wr_verify_skill.py`
  - Depends on: Unit 1
  - Approach:
    - Assert skill files exist.
    - Assert frontmatter has `name: wr-verify`.
    - Assert trigger text mentions implemented wayrail spec item and `verification.md` evidence.
    - Assert body requires explicit or unambiguous spec item path.
    - Assert body requires reading `spec.md` and `plan.md`.
    - Assert body checks `Implementation Handoff`.
    - Assert body requires fresh planned checks and command evidence fields.
    - Assert body defines per-check and overall labels.
    - Assert body requires skipped/blocked/manual validation details.
    - Assert body says to write only `verification.md`.
    - Assert body prohibits code edits, test edits, spec/plan/review edits, waiver approval, and review completion.
    - Assert body says no Phase 1 script is required.
  - Verification:
    - `uvx pytest tests/test_wr_verify_skill.py tests/test_starter_scripts.py`

- [ ] Unit 4: Verify and update lifecycle artifacts
  - Requirements: R30, SC1-SC9
  - Files:
    - Modify `specs/20260501-2112-wr-verify-skill-contract/verification.md`
    - Later modify `specs/20260501-2112-wr-verify-skill-contract/review.md`
  - Depends on: Units 1-3
  - Approach:
    - Run focused pytest checks.
    - Run full unittest discovery if focused checks pass.
    - Run Python compilation for touched Python test/source files.
    - Record skipped live Codex invocation if not executed.
  - Verification:
    - `uvx pytest tests/test_wr_verify_skill.py tests/test_starter_scripts.py`
    - `python -m unittest discover -s tests`
    - `python -m py_compile scripts/wayrail/_lib/starter.py tests/test_wr_verify_skill.py tests/test_starter_scripts.py`

## Verification

Planned checks:

- `uvx pytest tests/test_wr_verify_skill.py tests/test_starter_scripts.py`
- `python -m unittest discover -s tests`
- `python -m py_compile scripts/wayrail/_lib/starter.py tests/test_wr_verify_skill.py tests/test_starter_scripts.py`
- Manual inspection of `template/.agents/skills/wr-verify/SKILL.md`
- Manual inspection that no `template/.agents/skills/wr-verify/scripts/` is required or referenced as required

Expected evidence:

- focused pytest run passes
- full unittest discovery passes
- Python compilation exits `0`
- starter bootstrap/adopt inventory includes `wr-verify`
- `wr-verify` skill contract remains verification-only
- `verification.md` requirements are represented in the skill text

## Risks

- Trigger wording could be too broad and cause the skill to activate for implementation repair or review.
  - Mitigation: contract tests should assert negative-scope wording.
- Agents may still treat failed checks as something to fix inline.
  - Mitigation: make no-fix and return-to-implementation boundaries explicit and tested.
- No script means evidence formatting depends on the acting agent.
  - Mitigation: keep `verification.md` required sections and evidence fields explicit in the skill contract.
- Planned checks may be incomplete.
  - Mitigation: require missing checks to be recorded as planning/verification risk instead of inventing unrelated broad checks.
- Live Codex runtime behavior is not validated by tests.
  - Mitigation: Phase 1 tests validate starter artifacts and contract text; future dogfooding can reveal runtime selection issues.

## Implementation Handoff

Status: Ready for implementation
Plan path: specs/20260501-2112-wr-verify-skill-contract/plan.md
Spec path: specs/20260501-2112-wr-verify-skill-contract/spec.md
Implementation order: Unit 1, Unit 2, Unit 3, Unit 4
Recommended next action: implement Units 1-3, then run planned verification and record results.
