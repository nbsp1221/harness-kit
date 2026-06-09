---
spec_id: 20260501-2112-wr-verify-skill-contract
title: wr-verify Skill Contract
status: active
stage: spec
created_at: 2026-05-01 21:12
timezone: Asia/Seoul
---

# wr-verify Skill Contract

## Problem

`wayrail` now has `wr-spec` and `wr-plan`, but the lifecycle still has no repeatable verification stage.
After implementation, an agent can say that checks passed, but there is no repo-local contract for what evidence must be collected, where it must be written, or what to do when checks fail, are skipped, or cannot run.

Without `wr-verify`, completion claims are vulnerable to three failure modes:

- stale or implied evidence: the agent relies on prior context instead of running fresh checks
- mixed responsibilities: the agent fixes code, reviews quality, and verifies behavior in one blurred step
- missing audit trail: later reviewers cannot tell which commands ran, what passed, what failed, and what risk remains

`wr-verify` should close that gap by turning the planned verification section of `plan.md` into fresh, legible evidence in `verification.md`.

## Why Now

The previous lifecycle items established the first two repo-local skills:

- `wr-spec` scaffolds a spec item and authors only `spec.md`
- `wr-plan` consumes a ready `spec.md` and authors only `plan.md`

The next lifecycle boundary is implementation-to-review.
Before `wr-review` exists, the workflow needs a clear evidence writer that can say what was actually checked.

Comparable systems separate this responsibility:

- Spec Kit's `verify` extension validates implementation against spec artifacts and is read-only/idempotent.
- Spec Kit's `verify-tasks` extension independently verifies completion claims and explicitly warns about confirmation bias from the implementing agent.
- Spec Kit's `qa` extension records browser or CLI evidence against acceptance criteria.
- Spec Kit's `review` extension keeps code-quality review separate from verification.
- `speckit-gates` has an `implementation-verify` skill focused on fulfillment metrics after implementation.

The shared insight is that verification should produce evidence and next-step recommendations, not silently repair work or grant approval.

## Research Basis

Local project decisions already define the intended `wr-verify` shape:

- `docs/plans/2026-04-23-phase-1-foundation-decisions.md` says `verification.md` is an evidence summary, not a raw log.
- The same document says `wr-verify` should be a fresh-evidence writer, not a fixer or reviewer.
- `template/AGENTS.md` defines the workflow as `spec -> plan -> implement -> verify -> review`.
- `template/specs/_templates/verification.md` defines the target artifact sections: Summary, Planned Checks, Results, Manual Validation, Skipped Checks, Remaining Risk, and Review Handoff.

External comparison supports the same boundaries:

- `spec-kit-verify` checks task completion, file existence, requirement coverage, scenario/test coverage, spec intent alignment, constitution alignment, and design consistency, while remaining read-only and idempotent.
- `spec-kit-qa` emphasizes evidence-backed pass/fail determinations.
- `spec-kit-verify-tasks` shows that completion claims need independent evidence and that ambiguous evidence should not become a confident pass.
- `spec-kit-review` separates review concerns such as tests, errors, types, comments, simplification, and general code quality.

## Requirements

- `R1`: `wr-verify` MUST be present in the starter template at `template/.agents/skills/wr-verify/`.
- `R2`: `template/.agents/skills/wr-verify/SKILL.md` MUST use Agent Skills-compatible frontmatter with `name: wr-verify`.
- `R3`: The skill description MUST trigger only when converting an implemented wayrail spec item into `verification.md` evidence.
- `R4`: The skill MUST require an explicit spec item path or an unambiguous current spec item from the conversation.
- `R5`: `wr-verify` MUST read the selected `spec.md` and `plan.md` before writing `verification.md`.
- `R6`: `wr-verify` MUST check the `Implementation Handoff` section of `plan.md` before verifying.
- `R7`: `wr-verify` MUST stop without writing successful verification when the plan is not ready for implementation or when implementation has not been reported or observed.
- `R8`: `wr-verify` MUST extract planned checks, expected outcomes, requirement links, implementation-unit links, and any manual validation expectations from `plan.md`.
- `R9`: `wr-verify` MUST run planned verification commands fresh from the current workspace unless the command is unsafe, unavailable, or blocked.
- `R10`: `wr-verify` MUST record command, working directory, result label, exit status when available, concise evidence, and relevant artifact paths for each command-backed check.
- `R11`: `wr-verify` MUST keep running independent checks after a failure when doing so is safe and useful.
- `R12`: `wr-verify` MUST NOT silently replace a planned check with a different command.
- `R13`: If `wr-verify` substitutes an equivalent repo-native check, it MUST record the substitution and rationale.
- `R14`: If no safe equivalent exists for a planned check, `wr-verify` MUST mark that check as `blocked` or `skipped` with a reason.
- `R15`: `wr-verify` MUST classify per-check results as `pass`, `fail`, `skipped`, or `blocked`.
- `R16`: `wr-verify` MUST classify overall verification as `pass`, `fail`, `partial`, or `blocked`.
- `R17`: `wr-verify` MUST write only the selected spec item's `verification.md` in Phase 1.
- `R18`: `wr-verify` MUST NOT edit source code, tests, `spec.md`, `plan.md`, or `review.md`.
- `R19`: `wr-verify` MUST NOT approve waivers, accept risk on behalf of the human, or declare review complete.
- `R20`: `wr-verify` MAY recommend returning to implementation when checks fail or evidence is missing.
- `R21`: `wr-verify` MAY recommend continuing to `wr-review` only when the evidence is legible enough for a fresh reviewer to assess.
- `R22`: `verification.md` MUST include Summary, Planned Checks, Results, Manual Validation, Skipped Checks, Remaining Risk, and Review Handoff.
- `R23`: `verification.md` MUST avoid full raw terminal transcripts by default and use concise excerpts, counts, exit status, or artifact paths instead.
- `R24`: Skipped or blocked checks MUST include reason, whether the check was required for pass, residual risk, and owner or next step when knowable.
- `R25`: Manual validation entries MUST record scenario or method, expected result, observed result, observer when known, and evidence.
- `R26`: `wr-verify` MUST treat missing or incomplete planned checks as a planning/verification risk, not invent a broad unrelated test suite by default.
- `R27`: Command derivation order MUST be explicit: planned checks from `plan.md`, then repo guidance such as `AGENTS.md`, then standard project scripts only when they verify the same claim.
- `R28`: Phase 1 `wr-verify` MUST NOT require a deterministic script; verification is command execution plus evidence judgment.
- `R29`: If a future helper script is added, it MUST be scoped to formatting, parsing, or evidence capture and must not replace verification judgment.
- `R30`: Tests MUST verify the starter includes the `wr-verify` skill and that its skill contract contains freshness, evidence, result labels, write-boundary, no-fix, no-review, and handoff rules.

## Success Criteria

- `SC1`: A user or agent can invoke `wr-verify` against an implemented spec item and receive a useful `verification.md` without remembering the verification checklist.
- `SC2`: `verification.md` clearly shows what checks ran, what passed, what failed, what was skipped, and what risk remains.
- `SC3`: Verification evidence is fresh from the current session/workspace, not copied from prior discussion.
- `SC4`: Failed, skipped, or blocked checks do not become successful completion claims.
- `SC5`: The skill keeps verification separate from implementation fixes and review approval.
- `SC6`: A fresh reviewer can use `verification.md` to decide where `wr-review` should focus.
- `SC7`: `wr-verify` can recommend return-to-implementation or continue-to-review without granting human waivers.
- `SC8`: The skill body stays concise and suitable for progressive disclosure.
- `SC9`: The implementation can be tested without requiring Codex itself to execute the skill.

## Scope

In scope:

- starter-template `wr-verify` skill layout
- `SKILL.md` trigger and verification workflow instructions
- readiness checks against `plan.md`
- fresh command execution and evidence recording rules
- `verification.md` authoring rules
- result label and overall verdict definitions
- skipped/blocked/manual validation handling
- review handoff expectations
- starter inventory and skill-contract tests

Out of scope:

- implementing `wr-review`
- implementation execution or code fixing
- automatic waiver approval
- raw log management beyond concise evidence references
- browser automation framework integration as a Phase 1 requirement
- separate QA report directories
- `tasks.md` verification
- public plugin packaging
- global user installation
- deterministic verification runner script

## Constraints

- `wr-verify` must preserve the existing artifact model: `specs/<YYYYMMDD-HHMM-short-slug>/verification.md`.
- `wr-verify` must treat `plan.md` verification expectations as the primary source of planned checks.
- `wr-verify` must treat `spec.md` requirements and success criteria as the source of what the checks are meant to prove.
- `wr-verify` must keep `verification.md` readable by humans.
- `wr-verify` must be repo-local and installed through the starter template in Phase 1.
- The implementation should avoid introducing a task database, CI orchestrator, browser testing harness, or general-purpose QA subsystem.
- Verification should be conservative: ambiguous or missing evidence should become `partial`, `blocked`, or `skipped`, not `pass`.

## Assumptions

- `A1`: `template/.agents/skills/wr-verify/` is the canonical Phase 1 repo-local installation source.
- `A2`: The existing `template/specs/_templates/verification.md` section set is sufficient for Phase 1.
- `A3`: A script is not necessary for Phase 1 because the hard part is selecting and interpreting evidence, not scaffolding files.
- `A4`: Existing repository tests can validate skill presence and contract wording without a live Codex runtime.
- `A5`: If `verification.md` already contains meaningful non-stub content, `wr-verify` should avoid overwriting it unless the user explicitly asks to replace or revise it.
- `A6`: Optional evidence artifacts may become useful later, but Phase 1 can start with `verification.md` only.

## Open Questions

### Resolve Before Planning

None.

### Deferred to wr-plan

None.

## Planning Handoff

Status: Ready for wr-plan
Spec path: specs/20260501-2112-wr-verify-skill-contract/spec.md
Open questions: none blocking planning
Key assumptions: A1, A2, A3, A4, A5, A6
Requirement index: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30
Recommended next action: wr-plan

## Sources

- Local: `docs/plans/2026-04-23-phase-1-foundation-decisions.md`
- Local: `template/AGENTS.md`
- Local: `template/specs/_templates/verification.md`
- Local: `specs/20260501-0302-wr-plan-skill-contract/spec.md`
- Local: `specs/20260501-0302-wr-plan-skill-contract/plan.md`
- External: `github/spec-kit` community extension catalog
- External: `ismaelJimenez/spec-kit-verify`
- External: `datastone-inc/spec-kit-verify-tasks`
- External: `arunt14/spec-kit-qa`
- External: `ismaelJimenez/spec-kit-review`
- External: `drillan/speckit-gates` implementation-verify skill
