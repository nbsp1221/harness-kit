# wr-review Skill Contract Plan

## Overview

Implement `wr-review` as the fourth repo-local wayrail lifecycle skill.
It should consume a verified spec item, read `spec.md`, `plan.md`, `verification.md`, existing `review.md`, and the current implementation diff, then write `review.md` as a fresh-context findings, resolutions, residual-risk, and verdict artifact.

This plan keeps Phase 1 intentionally light: `wr-review` is a `SKILL.md` workflow plus minimal agent metadata, not a deterministic review runner, PR tool, waiver engine, or code-fixing tool.

## Requirements Trace

| Spec ID | Requirement | Plan Coverage | Verification |
| --- | --- | --- | --- |
| R1 | Starter contains `template/.agents/skills/wr-review/` | Unit 1 creates skill directory | File existence tests |
| R2 | Agent Skills frontmatter | Unit 1 writes `SKILL.md` frontmatter | Contract tests parse text |
| R3 | Narrow trigger | Unit 1 writes description | Contract tests assert trigger/negative scope |
| R4 | Explicit or unambiguous spec item | Unit 1 inputs section | Contract tests assert path requirement |
| R5 | Read spec, plan, verification, existing review | Unit 1 workflow | Contract tests assert artifact reads |
| R6-R8 | Review Handoff completeness and readiness | Unit 1 readiness gate | Contract tests assert required handoff fields and blocking behavior |
| R9 | Fresh-context artifact intent | Unit 1 workflow | Contract tests assert hidden-session-memory prohibition |
| R10-R13 | Read-only diff inspection and untracked files | Unit 1 diff inspection section | Contract tests assert safe git commands and forbidden mutating commands |
| R14-R17 | Compare against spec/plan/verification evidence | Unit 1 review workflow | Contract tests assert comparison targets and verification-as-evidence rule |
| R18-R22 | Delegated reviewer trigger, boundaries, and synthesis | Unit 1 delegated review section | Contract tests assert relevant roles, no edits, no waivers, parent verdict |
| R23 | Finding schema | Unit 1 findings section | Contract tests assert required fields |
| R24-R25 | Severity labels and definitions | Unit 1 severity section | Contract tests assert P0-P3 meanings |
| R26-R32 | Resolution labels and authority | Unit 1 resolution section | Contract tests assert human-owned risk acceptance and no invented waivers |
| R33-R34 | Required `review.md` sections and no-findings handling | Unit 1 authoring rules | Contract tests assert section list and no-findings rule |
| R35-R40 | Verdict labels and verdict policy | Unit 1 verdict section | Contract tests assert ready/not-ready/residual-risk policy |
| R41 | No human approval claim | Unit 1 boundaries/completion | Contract tests assert approval boundary |
| R42-R44 | Existing `review.md` preservation | Unit 1 workflow/boundaries | Contract tests assert append/explicit replace rule |
| R45-R47 | Write only review; no fixes/merge/waiver/scope changes | Unit 1 boundaries | Contract tests assert lifecycle boundary |
| R48-R49 | No required Phase 1 script | Unit 1 and Unit 3 | Contract tests assert no script dependency |
| R50-R51 | Test coverage expectations | Unit 3 adds tests | `uvx pytest` and unittest |

## Scope

In scope for this implementation pass:

- `template/.agents/skills/wr-review/SKILL.md`
- `template/.agents/skills/wr-review/agents/openai.yaml`
- starter inventory updates so bootstrap/adopt install `wr-review`
- dedicated `wr-review` skill contract tests
- updating this spec item's verification/review artifacts later in the lifecycle

Out of scope for this pass:

- `template/.agents/skills/wr-review/scripts/`
- deterministic review runner scripts
- code implementation or repair tooling
- verification command execution
- PR, commit, merge, or release tooling
- waiver approval or risk acceptance automation
- public plugin packaging
- global user skill installation
- changing the existing `review.md` template section set

## Context

Relevant source files:

- `specs/20260501-2250-wr-review-skill-contract/spec.md`
- `template/.agents/skills/wr-verify/SKILL.md`
- `template/.agents/skills/wr-verify/agents/openai.yaml`
- `template/.agents/skills/wr-plan/SKILL.md`
- `scripts/wayrail/_lib/starter.py`
- `tests/test_starter_scripts.py`
- `tests/test_wr_verify_skill.py`
- `tests/test_wr_plan_skill.py`
- `tests/test_wr_spec_skill.py`
- `template/specs/_templates/review.md`
- `specs/_templates/review.md`
- `template/AGENTS.md`

Existing conventions:

- Repo-local skills live under `template/.agents/skills/<name>/`.
- Each skill has `SKILL.md` and `agents/openai.yaml`.
- Deterministic scripts are added only when the stage has a deterministic operation that benefits from tooling.
- Starter inventory is duplicated in `scripts/wayrail/_lib/starter.py` and `tests/test_starter_scripts.py`.
- Skill-specific contract tests live in dedicated `tests/test_wr_<stage>_skill.py` files.
- Current tests use Python `unittest`, with `uvx pytest` as the normal runner.

Local design context:

- `wr-verify` now writes `verification.md` with Review Handoff expectations.
- `wr-review` should consume that handoff, challenge evidence quality, and produce a final review artifact.
- `template/AGENTS.md` already instructs agents not to silently skip verification or review before completion claims.

## Decisions

| Decision | Rationale | Alternatives Considered | Requirements Served |
| --- | --- | --- | --- |
| Implement `wr-review` as skill prose plus metadata only | Review requires judgment, evidence synthesis, and prioritization | Add a review runner script now | R5-R49 |
| Keep trigger narrow | Avoid accidental use for implementation, verification, PR, or release work | Broad "finish and approve" skill | R3, R41-R47 |
| Require explicit or unambiguous spec item | Prevents reviewing the wrong spec in a repo with many active specs | Auto-pick latest spec | R4 |
| Gate on `verification.md` Review Handoff | Ensures review starts from verification evidence rather than chat memory | Review directly after implementation | R5-R8 |
| Define read-only diff inspection | Avoids git mutation and unsafe broad reads during review | Let reviewers choose arbitrary git commands | R10-R13 |
| Keep risk acceptance human-owned | Prevents `wr-review` from becoming a waiver engine | Let review mark accepted risks | R26-R32, R41 |
| Define verdict policy explicitly | Makes review outcome predictable and testable | Leave verdict to free-form judgment | R35-R40 |
| Preserve existing `review.md` | Prevents accidental loss of prior findings and human decisions | Always overwrite review output | R42-R44 |
| Add dedicated tests | Makes the skill contract regressions visible | Only starter inventory tests | R50-R51 |

## Implementation Units

- [ ] Unit 1: Add `wr-review` skill source
  - Requirements: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49
  - Files:
    - Create `template/.agents/skills/wr-review/SKILL.md`
    - Create `template/.agents/skills/wr-review/agents/openai.yaml`
  - Depends on: none
  - Approach:
    - Mirror the concise structure of `wr-verify`.
    - Put `name: wr-review` and a narrow description in frontmatter.
    - Include sections for Use When, Do Not Use When, Inputs, Readiness Gate, Diff Inspection, Workflow, Delegated Reviewers, Finding Schema, Severity Labels, Resolution Labels, Verdicts, Review Authoring Rules, Boundaries, and Completion.
    - State that the skill reads `spec.md`, `plan.md`, `verification.md`, and existing `review.md` before writing.
    - State Review Handoff completeness fields and ready-verdict blocking behavior.
    - State safe read-only diff commands and forbidden mutating commands.
    - State delegated reviewer boundaries and parent synthesis ownership.
    - State finding fields, severity definitions, resolution authority, and verdict policy.
    - State existing `review.md` preservation.
    - State that the skill writes only `review.md` and does not fix, verify, approve waivers, merge, commit, or release.
    - State that Phase 1 has no required script.
  - Verification:
    - Dedicated tests inspect frontmatter and required body rules.

- [ ] Unit 2: Add `wr-review` to starter inventory
  - Requirements: R1, R50
  - Files:
    - Modify `scripts/wayrail/_lib/starter.py`
    - Modify `tests/test_starter_scripts.py`
  - Depends on: Unit 1
  - Approach:
    - Add `.agents/skills/wr-review/SKILL.md` and `.agents/skills/wr-review/agents/openai.yaml` to both required template file lists.
    - Do not add executable-bit assertions because `wr-review` has no script in Phase 1.
  - Verification:
    - Starter template file test passes.
    - Bootstrap fixture creates the `wr-review` files.

- [ ] Unit 3: Add dedicated `wr-review` contract tests
  - Requirements: R2-R51
  - Files:
    - Create `tests/test_wr_review_skill.py`
  - Depends on: Unit 1
  - Approach:
    - Assert skill files exist.
    - Assert frontmatter has `name: wr-review`.
    - Assert trigger text mentions reviewing an implemented and verified wayrail spec item into `review.md`.
    - Assert body requires explicit or unambiguous spec item path.
    - Assert body requires reading `spec.md`, `plan.md`, `verification.md`, and existing `review.md`.
    - Assert body defines Review Handoff completeness fields and blocks ready when incomplete.
    - Assert body requires fresh-context review from artifacts, not hidden implementation-session memory.
    - Assert body defines safe read-only diff inspection and forbidden mutating git commands.
    - Assert body handles untracked files by listing first and reading only relevant files.
    - Assert body treats `verification.md` as evidence, not truth.
    - Assert body defines delegated reviewer triggers, roles, boundaries, and parent verdict ownership.
    - Assert body defines every finding field, including behavioral risk and decision authority.
    - Assert body defines P0-P3 severity meanings.
    - Assert body defines resolution labels and human-owned risk acceptance.
    - Assert body defines verdict labels and policy for `ready`, `ready-with-residual-risk`, and `not-ready`.
    - Assert body preserves existing non-stub `review.md`.
    - Assert body says to write only `review.md`.
    - Assert body prohibits code/test/spec/plan/verification edits, fixes, waivers, merge, commit, release approval, and scope changes.
    - Assert body says no Phase 1 script is required.
  - Verification:
    - `uvx pytest tests/test_wr_review_skill.py tests/test_starter_scripts.py`

- [ ] Unit 4: Verify and update lifecycle artifacts
  - Requirements: R50-R51, SC1-SC9
  - Files:
    - Modify `specs/20260501-2250-wr-review-skill-contract/verification.md`
    - Later modify `specs/20260501-2250-wr-review-skill-contract/review.md`
  - Depends on: Units 1-3
  - Approach:
    - Run focused pytest checks.
    - Run full unittest discovery if focused checks pass.
    - Run Python compilation for touched Python test/source files.
    - Record skipped live Codex invocation if not executed.
  - Verification:
    - `uvx pytest tests/test_wr_review_skill.py tests/test_starter_scripts.py`
    - `python -m unittest discover -s tests`
    - `python -m py_compile scripts/wayrail/_lib/starter.py tests/test_wr_review_skill.py tests/test_starter_scripts.py`

## Verification

Planned checks:

- `uvx pytest tests/test_wr_review_skill.py tests/test_starter_scripts.py`
- `python -m unittest discover -s tests`
- `python -m py_compile scripts/wayrail/_lib/starter.py tests/test_wr_review_skill.py tests/test_starter_scripts.py`
- Manual inspection of `template/.agents/skills/wr-review/SKILL.md`
- Manual inspection that no `template/.agents/skills/wr-review/scripts/` is required or referenced as required

Expected evidence:

- focused pytest run passes
- full unittest discovery passes
- Python compilation exits `0`
- starter bootstrap/adopt inventory includes `wr-review`
- `wr-review` skill contract remains review-only
- Review Handoff, read-only diff, delegated reviewer, resolution authority, verdict, and preservation rules are represented in the skill text

## Risks

- The skill could become too long because review has more policy detail than spec/plan/verify.
  - Mitigation: keep examples short and use compact sections with explicit labels.
- Resolution policy could be misread as allowing agents to accept risk.
  - Mitigation: use `human-accepted-risk`, require source, and test the no-invented-waiver rule.
- Diff inspection could accidentally encourage unsafe git operations.
  - Mitigation: explicitly list safe read-only commands and forbidden mutating commands.
- Delegated reviewer guidance could cause over-dispatch for small changes.
  - Mitigation: define delegation triggers and allow single-reviewer pass otherwise.
- No script means tests only validate instruction contracts, not live Codex behavior.
  - Mitigation: Phase 1 tests validate starter artifacts and contract text; dogfooding can reveal runtime selection issues.

## Implementation Handoff

Status: Ready for implementation
Plan path: specs/20260501-2250-wr-review-skill-contract/plan.md
Spec path: specs/20260501-2250-wr-review-skill-contract/spec.md
Implementation order: Unit 1, Unit 2, Unit 3, Unit 4
Recommended next action: implement Units 1-3, then run planned verification and record results.
