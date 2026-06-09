---
spec_id: 20260501-2250-wr-review-skill-contract
title: wr-review Skill Contract
status: active
stage: spec
created_at: 2026-05-01 22:50
timezone: Asia/Seoul
---

# wr-review Skill Contract

## Problem

`wayrail` now has `wr-spec`, `wr-plan`, and `wr-verify`, but the lifecycle still lacks a repeatable review stage.
After verification evidence exists, a human or agent still needs to decide whether the implementation matches the spec and plan, whether the evidence is strong enough, which findings matter, and whether remaining risk blocks completion.

Without `wr-review`, review tends to collapse into one of three weaker patterns:

- a vague "looks good" statement with no durable finding record
- a second verification pass that only repeats command results
- inline implementation fixes with no independent review handoff

`wr-review` should close the lifecycle loop by reading the artifacts and current implementation, producing a fresh-context findings and resolution record in `review.md`.

## Why Now

The previous lifecycle items established the first three repo-local skills:

- `wr-spec` starts a spec item and authors only `spec.md`
- `wr-plan` consumes a ready `spec.md` and authors only `plan.md`
- `wr-verify` consumes an implemented item and authors only `verification.md`

The final Phase 1 lifecycle skill is `wr-review`.
It is needed before wayrail can complete the basic `spec -> plan -> implement -> verify -> review` loop without relying on chat memory.

The `wr-verify` dogfooding pass also showed why review must be its own stage.
Independent reviewers found contract gaps around unsafe commands, evidence preservation, and test coverage.
Those findings were fixed, re-verified, and recorded in `review.md`.
That is exactly the behavior `wr-review` should standardize.

## Research Basis

Local project decisions already define the intended `wr-review` shape:

- `docs/plans/2026-04-23-phase-1-foundation-decisions.md` says `review.md` should be a fresh-context findings and resolution record.
- The same document says `wr-review` should be a read-only fresh-context quality gate.
- `template/AGENTS.md` defines the workflow as `spec -> plan -> implement -> verify -> review`.
- `template/specs/_templates/review.md` defines the target artifact sections: Summary, Scope, Reviewers, Findings, Resolutions, Residual Risk, and Verdict.
- `specs/20260501-2112-wr-verify-skill-contract/review.md` is a recent dogfooding example of review fan-out, finding synthesis, resolution tracking, and final verdict.
- Third-party subagent review of this spec before planning identified contract gaps around resolution authority, Review Handoff completeness, read-only diff inspection, delegated reviewer boundaries, existing review preservation, severity meaning, and verdict policy.

External comparison supports the same boundaries:

- `spec-kit-review` orchestrates specialized review agents for code, tests, comments, errors, types, and simplification, then aggregates findings.
- Spec Kit's review extension is post-implementation and read-oriented; it does not replace verification evidence or implementation.
- Prior comparison of agent workflows showed a common pattern: review should run from fresh context, group findings by severity, require evidence, and record residual risk.

## Requirements

- `R1`: `wr-review` MUST be present in the starter template at `template/.agents/skills/wr-review/`.
- `R2`: `template/.agents/skills/wr-review/SKILL.md` MUST use Agent Skills-compatible frontmatter with `name: wr-review`.
- `R3`: The skill description MUST trigger only when reviewing an implemented and verified wayrail spec item into `review.md`.
- `R4`: The skill MUST require an explicit spec item path or an unambiguous current spec item from the conversation.
- `R5`: `wr-review` MUST read the selected `spec.md`, `plan.md`, `verification.md`, and existing `review.md` before writing `review.md`.
- `R6`: `wr-review` MUST check that `verification.md` has a Review Handoff before producing a ready verdict.
- `R7`: `wr-review` MUST treat Review Handoff as complete only when it identifies verification status, commands or checks run, pass/fail/blocked/skipped results, manual evidence when applicable, known gaps, residual risks, and recommended next action.
- `R8`: Missing or incomplete Review Handoff content MUST block a ready verdict and be recorded as a review finding.
- `R9`: `wr-review` MUST reconstruct intent from lifecycle artifacts, not hidden implementation-session memory.
- `R10`: `wr-review` MUST inspect the current implementation diff, including untracked files when relevant.
- `R11`: Diff inspection MUST be read-only and SHOULD use safe commands such as `git status --short`, `git diff --no-ext-diff --no-textconv`, and `git diff --cached --no-ext-diff --no-textconv`.
- `R12`: `wr-review` MUST NOT run `git add`, `git stash`, `git checkout`, `git clean`, `git reset`, commit, merge, push, or any command that mutates repository or filesystem state.
- `R13`: Untracked files MUST be listed first and read only when relevant to the selected spec item or review scope.
- `R14`: `wr-review` MUST compare implementation and evidence against `spec.md` requirements, success criteria, scope, constraints, assumptions, and open questions.
- `R15`: `wr-review` MUST compare implementation and evidence against `plan.md` implementation units, decisions, expected files, and planned verification.
- `R16`: `wr-review` MUST treat `verification.md` as evidence, not truth.
- `R17`: `wr-review` MUST flag failed, skipped, blocked, missing, weak, or manual-only verification evidence when it affects completion confidence.
- `R18`: `wr-review` SHOULD use delegated fresh-context reviewers when the diff is large, touches security, data, external APIs, filesystem, shell, network, permissions, or changes shared lifecycle behavior; otherwise it MAY perform a single-reviewer pass.
- `R19`: When delegating, `wr-review` SHOULD select only relevant roles from correctness, testing/evidence, maintainability/scope, and security.
- `R20`: Delegated reviewers MUST receive the selected spec item path, the same read-only/no-fix/no-approval boundaries, and an instruction to return findings only.
- `R21`: Delegated reviewers MUST NOT edit files, run mutating commands, grant waivers, approve release, or produce the final verdict.
- `R22`: The parent `wr-review` MUST synthesize delegated or human findings into one deduplicated finding set and remains responsible for the final verdict.
- `R23`: Findings MUST include stable ID, severity, resolution state, reviewer/source, location when applicable, artifact reference when applicable, evidence, behavioral risk, recommendation, and decision authority: `human-required` or `parent-decidable`.
- `R24`: Severity labels MUST be `P0`, `P1`, `P2`, and `P3`.
- `R25`: Severity definitions MUST be: `P0` invalidates lifecycle artifacts, corrupts data/security, or makes review impossible; `P1` blocks declared requirements, success criteria, required evidence, or lifecycle safety; `P2` is a meaningful correctness, coverage, maintainability, or scope issue that should be fixed or explicitly deferred; `P3` is minor clarity, polish, or non-blocking improvement.
- `R26`: Resolution labels MUST be `fixed`, `human-accepted-risk`, `deferred`, `rejected`, and `open`.
- `R27`: New findings produced by `wr-review` MUST default to `open`.
- `R28`: `wr-review` MAY mark a finding `fixed` only when current artifacts or diff provide evidence the issue has been resolved.
- `R29`: `human-accepted-risk` MUST only be used when an explicit human decision is present in current user instructions or reviewed lifecycle artifacts, and `wr-review` MUST record the source of that decision.
- `R30`: `deferred` MUST only be used when an explicit human or owner decision with rationale and follow-up target is present in current user instructions or reviewed lifecycle artifacts.
- `R31`: `wr-review` MAY mark a finding `rejected` when concrete evidence shows the finding is invalid, duplicate, out of scope, or already disproven, and MUST record that rationale.
- `R32`: `wr-review` MUST NOT invent acceptance, deferment, waiver, or risk approval decisions.
- `R33`: `review.md` MUST include Summary, Scope, Reviewers, Findings, Resolutions, Residual Risk, and Verdict.
- `R34`: If there are no findings, `review.md` MUST say so explicitly and still record scope, reviewers, residual risk, and verdict.
- `R35`: Open `P0` and `P1` findings MUST block a ready verdict.
- `R36`: `P0` and `P1` findings marked `human-accepted-risk` or `deferred` MUST produce `not-ready` unless the reviewed artifacts or current user instructions explicitly approve proceeding despite that risk.
- `R37`: `P2` findings SHOULD be fixed when straightforward or intentionally deferred with rationale.
- `R38`: `P3` findings MUST NOT block by default.
- `R39`: Verdicts MUST be `ready`, `ready-with-residual-risk`, or `not-ready`.
- `R40`: Verdict rules MUST be: `not-ready` for any open `P0`/`P1`, incomplete Review Handoff, missing required artifact or diff review, failed required verification, or missing core requirement; `ready-with-residual-risk` for no blocking findings but notable `human-accepted-risk`, `deferred`, skipped, blocked, weak, manual-only, or P2 residual risk remains; `ready` only when all material findings are `fixed` or evidence-backed `rejected`, required evidence is strong, and residual risk is none or routine.
- `R41`: `wr-review` MAY say "ready for human approval", but MUST NOT claim human approval.
- `R42`: If `review.md` is missing or stub-only, `wr-review` MAY create or replace it.
- `R43`: If `review.md` contains meaningful non-stub content, `wr-review` MUST preserve it and either append a new dated review section or stop and require explicit user instruction to replace or revise the existing review.
- `R44`: `wr-review` MUST NOT silently overwrite prior findings, resolutions, residual risk, or verdicts.
- `R45`: `wr-review` MUST write only the selected spec item's `review.md` in Phase 1.
- `R46`: `wr-review` MUST NOT edit source code, tests, `spec.md`, `plan.md`, or `verification.md`.
- `R47`: `wr-review` MUST NOT fix findings, grant waivers, merge, commit, approve release, or change scope.
- `R48`: Phase 1 `wr-review` MUST NOT require a deterministic script; review requires judgment and synthesis.
- `R49`: If a future helper script is added, it MUST be scoped to read-only diff detection, formatting, or finding normalization and must not replace review judgment.
- `R50`: Tests MUST verify the starter includes the `wr-review` skill and that its skill contract contains artifact reads, Review Handoff completeness, fresh-context review, safe read-only diff inspection, delegated reviewer boundaries, finding schema, severity/resolution/verdict labels, resolution authority, existing review preservation, write-boundary, no-fix, no-approval, and no-script rules.
- `R51`: Tests SHOULD include contract checks for incomplete Review Handoff blocking ready, open `P0`/`P1` blocking ready, residual non-blocking findings producing `ready-with-residual-risk`, no-findings still recording residual risk and verdict, existing non-stub `review.md` requiring append or explicit replace/revise instruction, and every documented finding field appearing in review authoring instructions.

## Success Criteria

- `SC1`: A user or agent can invoke `wr-review` against a verified spec item and receive a useful `review.md` without remembering the review checklist.
- `SC2`: `review.md` clearly states what was reviewed, who or what reviewed it, what findings exist, how findings were resolved, and what residual risk remains.
- `SC3`: The review can challenge weak verification evidence instead of treating `verification.md` as automatically true.
- `SC4`: Findings are evidence-backed, deduplicated, severity-labeled, and have concrete recommendations.
- `SC5`: The verdict is predictable from finding severities and resolution states.
- `SC6`: The skill keeps review separate from implementation fixes, verification evidence collection, waiver approval, and release approval.
- `SC7`: The skill body stays concise and suitable for progressive disclosure.
- `SC8`: The implementation can be tested without requiring Codex itself to execute the skill.
- `SC9`: Human-owned risk acceptance is visible as human-owned and cannot be created by `wr-review`.

## Scope

In scope:

- starter-template `wr-review` skill layout
- `SKILL.md` trigger and review workflow instructions
- readiness checks against `verification.md`
- fresh-context artifact and diff review rules
- read-only diff inspection safety rules
- reviewer role guidance
- delegated reviewer boundary rules
- finding schema
- severity, resolution, and verdict label definitions
- `review.md` authoring rules
- starter inventory and skill-contract tests

Out of scope:

- implementation fixes
- verification command execution
- waiver approval
- release approval or merge readiness automation
- PR creation, commit creation, or git staging
- public plugin packaging
- global user installation
- deterministic review runner script

## Constraints

- `wr-review` must preserve the existing artifact model: `specs/<YYYYMMDD-HHMM-short-slug>/review.md`.
- `wr-review` must treat `spec.md`, `plan.md`, and `verification.md` as required review inputs.
- `wr-review` must be able to review untracked files because this project may be pre-commit during Phase 1.
- `wr-review` must inspect diffs without mutating git or filesystem state.
- `wr-review` must keep `review.md` readable by humans.
- `wr-review` must be repo-local and installed through the starter template in Phase 1.
- The implementation should avoid introducing a review database, dashboard, persistent reviewer registry, or broad orchestration runtime.

## Assumptions

- `A1`: `template/.agents/skills/wr-review/` is the canonical Phase 1 repo-local installation source.
- `A2`: The existing `template/specs/_templates/review.md` section set is sufficient for Phase 1.
- `A3`: A script is not necessary for Phase 1 because review requires judgment, evidence synthesis, and prioritization.
- `A4`: Existing repository tests can validate skill presence and contract wording without a live Codex runtime.
- `A5`: Existing review preservation is a requirement, not merely an assumption.
- `A6`: Subagent review fan-out is useful for non-trivial work, but `wr-review` should degrade gracefully to a single reviewer when delegation is unavailable.

## Open Questions

### Resolve Before Planning

None.

### Deferred to wr-plan

None.

## Planning Handoff

Status: Ready for wr-plan
Spec path: specs/20260501-2250-wr-review-skill-contract/spec.md
Open questions: none blocking planning
Key assumptions: A1, A2, A3, A4, A5, A6
Requirement index: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49, R50, R51
Recommended next action: wr-plan

## Sources

- Local: `docs/plans/2026-04-23-phase-1-foundation-decisions.md`
- Local: `template/AGENTS.md`
- Local: `template/specs/_templates/review.md`
- Local: `specs/20260501-2112-wr-verify-skill-contract/review.md`
- Local: `specs/20260501-2112-wr-verify-skill-contract/verification.md`
- External: `ismaelJimenez/spec-kit-review`
- External: `github/spec-kit` community extension catalog
