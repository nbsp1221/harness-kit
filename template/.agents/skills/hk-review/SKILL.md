---
name: hk-review
description: "Use when reviewing an implemented and verified harness-kit spec item into review.md. Reads a selected spec item, checks Review Handoff readiness, inspects the current diff read-only, synthesizes findings, resolutions, residual risk, and a verdict, and writes only review.md. Do not use for implementation, verification command execution, fixing findings, waiver approval, merge, commit, release approval, or editing spec.md/plan.md/verification.md."
---

# hk-review

Create a fresh-context review record for an implemented and verified harness-kit spec item.

## Use When

- The user asks to run `hk-review`, review a completed harness-kit spec item, or move a verified item into review.
- The input includes an explicit spec item path or an unambiguous current spec item from the conversation.
- The target spec item has `spec.md`, `plan.md`, and `verification.md`; missing `review.md` is allowed and handled by the authoring rules.

## Do Not Use When

- The user asks to start a new spec item; use `hk-spec`.
- The user asks to create an implementation plan; use `hk-plan`.
- The user asks to run verification checks or write verification evidence; use `hk-verify`.
- The user asks for implementation, code fixes, test fixes, waiver approval, merge, commit, or release approval.
- The review cannot identify the selected spec item.

## Inputs

Prefer an explicit spec item path such as `specs/<id>/spec.md`.
If the conversation has exactly one unambiguous current spec item, use that path and state it.
If neither is available, ask for the spec path.

## Readiness Gate

Read `spec.md`, read `plan.md`, and read `verification.md` before writing anything.
Read existing `review.md` when present before writing anything.
Check `verification.md` for a `Review Handoff`.
Treat the handoff as complete only when it identifies verification status, commands or checks run, pass/fail/blocked/skipped results, manual evidence when applicable, known gaps, residual risks, and recommended next action.
Missing or incomplete Review Handoff content blocks a `ready` verdict and must record a finding.

## Context Reconstruction

Perform a fresh-context review from lifecycle artifacts and current workspace state, not hidden implementation-session memory.
Reconstruct intent from the selected `spec.md`, `plan.md`, `verification.md`, existing `review.md` when present, and the current implementation diff.

## Diff Inspection

Inspect the current implementation diff read-only.
Use safe commands such as:

- `git status --short`
- `git diff --no-ext-diff --no-textconv`
- `git diff --cached --no-ext-diff --no-textconv`

Always list untracked files first and read only relevant untracked files for the selected spec item or review scope.
Do not run mutating commands such as `git add`, `git stash`, `git checkout`, `git clean`, `git reset`, commit, merge, push, or commands that mutate repository or filesystem state.

## Review Workflow

1. Identify the target spec item.
2. Read `spec.md`.
3. Read `plan.md`.
4. Read `verification.md`.
5. Read existing `review.md` when present.
6. Apply the readiness gate.
7. Inspect the current implementation diff read-only.
8. Compare implementation and evidence against `spec.md` requirements, success criteria, scope, constraints, assumptions, and open questions.
9. Compare implementation and evidence against `plan.md` implementation units, decisions, expected files, and planned verification.
10. Always treat `verification.md` as evidence, not truth.
11. Flag failed, skipped, blocked, missing, weak, or manual-only verification evidence when it affects completion confidence.
12. Synthesize findings, resolutions, residual risk, and verdict into `review.md`.

## Delegated Reviewers

Use delegated fresh-context reviewers when the diff is large, touches security, data, external APIs, filesystem, shell, network, permissions, or changes shared lifecycle behavior.
Otherwise a single-reviewer pass is acceptable.
Select only relevant roles from correctness, testing/evidence, maintainability/scope, and security.

When delegating, give each reviewer the selected spec item path, the same read-only/no-fix/no-approval boundaries, and an instruction to return findings only.
Delegated reviewers MUST NOT edit files, MUST NOT run mutating commands, MUST NOT grant waivers, MUST NOT approve release, and MUST NOT produce the final verdict.
The parent `hk-review` synthesizes delegated or human findings into one deduplicated finding set and owns the final verdict.

## Finding Schema

Each finding must include:

- stable ID
- severity
- resolution state
- reviewer/source
- location when applicable
- artifact reference when applicable
- evidence
- behavioral risk
- recommendation
- decision authority: `human-required` or `parent-decidable`

## Severity Labels

- `P0`: invalidates lifecycle artifacts, corrupts data/security, or makes review impossible.
- `P1`: blocks declared requirements, success criteria, required evidence, or lifecycle safety.
- `P2`: meaningful correctness, coverage, maintainability, or scope issue that should be fixed or explicitly deferred.
- `P3`: minor clarity, polish, or non-blocking improvement.

## Resolution Labels

- `open`: unresolved finding. New findings default to `open`.
- `fixed`: current artifacts or diff provide evidence that the issue has been resolved.
- `human-accepted-risk`: explicit human decision exists in current user instructions or reviewed lifecycle artifacts; record the source.
- `deferred`: explicit human or owner decision with rationale and follow-up target exists in current user instructions or reviewed lifecycle artifacts.
- `rejected`: concrete evidence shows the finding is invalid, duplicate, out of scope, or already disproven; record the rationale.

MUST NOT invent acceptance, deferment, waiver, or risk approval decisions.

## Verdicts

Use only these verdicts:

- `not-ready`
- `ready-with-residual-risk`
- `ready`

Verdict policy:

- `not-ready`: any open `P0` or `P1`, incomplete Review Handoff, missing required artifact or diff review, failed required verification, or missing core requirement.
- `not-ready`: `P0` or `P1` findings marked `human-accepted-risk` or `deferred` unless the reviewed artifacts or current user instructions explicitly approve proceeding despite that risk.
- `ready-with-residual-risk`: no blocking findings, but notable `human-accepted-risk`, `deferred`, skipped, blocked, weak, manual-only, or `P2` residual risk remains.
- `ready`: all material findings are `fixed` or evidence-backed `rejected`, required evidence is strong, and residual risk is none or routine.

`P3` findings do not block by default.
`P2` findings should be fixed when straightforward or intentionally deferred with rationale.
You may say "ready for human approval"; do not claim human approval.

## Review Authoring Rules

Write `review.md` with these sections:

- Summary
- Scope
- Reviewers
- Findings
- Resolutions
- Residual Risk
- Verdict

If there are no findings, say so explicitly and still record scope, reviewers, residual risk, and verdict.
If existing `review.md` is missing or stub-only, create or replace it.
If existing `review.md` contains meaningful non-stub content, preserve it and append a new dated review section, or stop and require explicit user instruction to replace or revise it.
MUST NOT silently overwrite prior findings, resolutions, residual risk, or verdicts.

## Boundaries

Write only `review.md`.
Do not edit source code.
Do not edit tests.
Do not edit `spec.md`.
Do not edit `plan.md`.
Do not edit `verification.md`.
Do not fix findings.
Do not approve waivers.
Do not claim human approval.
Do not merge.
Do not commit.
Do not approve release.
Do not change scope.

Phase 1 does not require a script; review requires judgment and synthesis.
If a future helper script is added, it may help with read-only diff detection, formatting, or finding normalization, but it must not replace review judgment.

## Completion

Report the written `review.md` path and verdict.
If the verdict is `not-ready`, recommend returning to implementation or verification with the blocking finding IDs.
If the verdict is `ready-with-residual-risk`, summarize the residual risks and any human-owned decisions.
If the verdict is `ready`, state that the item is ready for human approval.
