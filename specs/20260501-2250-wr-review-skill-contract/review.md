# wr-review Skill Contract Review

## Summary

Status: not-ready

Fresh-context review found two parent-decidable issues: one contract contradiction around missing `review.md`, and one weak test assertion around `ready-with-residual-risk` verdict policy.

## Scope

- Spec item: `specs/20260501-2250-wr-review-skill-contract`
- Reviewed artifacts:
  - `spec.md`
  - `plan.md`
  - `verification.md`
  - existing `review.md`
- Reviewed implementation files:
  - `template/.agents/skills/wr-review/SKILL.md`
  - `template/.agents/skills/wr-review/agents/openai.yaml`
  - `scripts/wayrail/_lib/starter.py`
  - `tests/test_wr_review_skill.py`
  - `tests/test_starter_scripts.py`

## Reviewers

- Parent `wr-review` synthesis
- Correctness/lifecycle contract reviewer
- Testing/evidence reviewer
- Maintainability/scope reviewer

## Findings

- `WRR-001`
  - Severity: `P2`
  - Resolution state: `open`
  - Reviewer/source: correctness/lifecycle contract reviewer and maintainability/scope reviewer
  - Location: `template/.agents/skills/wr-review/SKILL.md`
  - Artifact reference: `spec.md` `R42`, `R43`
  - Evidence: `SKILL.md` says the target item has `spec.md`, `plan.md`, `verification.md`, and `review.md`, and says to read existing `review.md` before writing. The same skill later says missing or stub-only `review.md` may be created or replaced.
  - Behavioral risk: an agent may refuse to run `wr-review` for a valid verified spec item whose `review.md` is missing, even though the spec allows creating it.
  - Recommendation: require `spec.md`, `plan.md`, and `verification.md`; read `review.md` when present; keep the missing/stub creation rule.
  - Decision authority: `parent-decidable`
- `WRR-002`
  - Severity: `P3`
  - Resolution state: `open`
  - Reviewer/source: testing/evidence reviewer
  - Location: `tests/test_wr_review_skill.py`
  - Artifact reference: `spec.md` `R40`, `R51`, `SC5`
  - Evidence: the test asserts verdict labels and a few generic phrases, but does not assert the specific `ready-with-residual-risk` rule for no blocking findings plus human-accepted/deferred/skipped/blocked/weak/manual-only/P2 residual risk.
  - Behavioral risk: future edits could weaken the residual-risk verdict policy while keeping the label present.
  - Recommendation: add focused assertions for the `ready-with-residual-risk` policy text.
  - Decision authority: `parent-decidable`

## Resolutions

- `WRR-001`: open
- `WRR-002`: open

## Residual Risk

- The implementation should not be considered ready until `WRR-001` is fixed and re-verified.
- `WRR-002` is non-blocking by severity, but it is straightforward to fix with test assertions before final approval.

## Verdict

`not-ready`

Reason: `WRR-001` is an open P2 lifecycle contract inconsistency and should be fixed before this skill is treated as ready for human approval.

## Follow-up Review - 2026-05-01

### Summary

Status: ready-with-residual-risk

The two findings from the initial review were fixed and re-verified.
The implementation now satisfies the `wr-review` skill contract and starter inventory requirements.

### Scope

- Reviewed fixes:
  - `template/.agents/skills/wr-review/SKILL.md`
  - `tests/test_wr_review_skill.py`
  - `specs/20260501-2250-wr-review-skill-contract/verification.md`
- Verification evidence:
  - `uvx pytest tests/test_wr_review_skill.py tests/test_starter_scripts.py`: `29 passed in 0.53s`
  - `python -m unittest discover -s tests`: `Ran 64 tests in 0.949s`, `OK`
  - `python -m py_compile scripts/wayrail/_lib/starter.py tests/test_wr_review_skill.py tests/test_starter_scripts.py`: exit `0`

### Reviewers

- Parent `wr-review` synthesis

### Findings

- No new findings.

### Resolutions

- `WRR-001`: fixed
  - Evidence: `SKILL.md` now requires `spec.md`, `plan.md`, and `verification.md`, explicitly says missing `review.md` is allowed, and reads existing `review.md` only when present.
- `WRR-002`: fixed
  - Evidence: `tests/test_wr_review_skill.py` now asserts missing `review.md` handling and the concrete `ready-with-residual-risk` policy conditions.

### Residual Risk

- Fresh-session runtime skill discovery for the newly added `wr-review` skill has not been independently checked.
- The skill is instruction-only, so practical ergonomics should continue to be dogfooded.

### Verdict

`ready-with-residual-risk`

Reason: all material findings are fixed and verification passed. The remaining risk is limited to fresh-session runtime discovery and normal instruction-adherence risk for a Phase 1 skill.
