# wr-verify Skill Contract Review

## Summary

Reviewed the `wr-verify` implementation against `spec.md`, `plan.md`, and the starter template conventions.

The implementation matches the agreed Phase 1 direction: `wr-verify` is a repo-local evidence-writing skill, not a code fixer, waiver approver, review stage, or deterministic runner.

Initial review fan-out found contract clarity gaps around unsafe command handling, preserving existing `verification.md` evidence, and test coverage for core behavior rules.
Those findings were addressed and re-verified.

## Scope

Reviewed files:

- `template/.agents/skills/wr-verify/SKILL.md`
- `template/.agents/skills/wr-verify/agents/openai.yaml`
- `scripts/wayrail/_lib/starter.py`
- `tests/test_wr_verify_skill.py`
- `tests/test_starter_scripts.py`
- `specs/20260501-2112-wr-verify-skill-contract/spec.md`
- `specs/20260501-2112-wr-verify-skill-contract/plan.md`
- `specs/20260501-2112-wr-verify-skill-contract/verification.md`

## Reviewers

- Security and boundary review: delegated read-only reviewer
- Correctness and testing review: delegated read-only reviewer
- Maintainability and contract-quality review: delegated read-only reviewer
- Parent synthesis: local review and final judgment

## Findings

No remaining blocking findings.

Resolved findings:

| ID | Severity | Finding | Resolution |
| --- | --- | --- | --- |
| F1 | P2 | `wr-verify` did not define unsafe command classes, so a planned check could trigger destructive, credentialed, production, install, migration, deletion, or broad-write actions during an evidence-only phase. | Added `Command Safety Gate` to `SKILL.md`; added contract test coverage for local-only default, unsafe command classes, and explicit human authorization. |
| F2 | P2 | `wr-verify` did not instruct agents to preserve existing meaningful `verification.md` content even though the spec assumption requires no overwrite without an explicit replace/revise request. | Added workflow rule to read existing `verification.md` before writing and avoid overwriting non-stub content unless explicitly requested; added contract test coverage. |
| F3 | P2 | Contract tests did not directly cover command derivation order, no silent replacement, substitution rationale, blocked/skipped classification, or missing planned-check risk. | Added targeted assertions in `tests/test_wr_verify_skill.py`; focused and full test suites pass. |

Advisory findings:

| ID | Severity | Finding | Decision |
| --- | --- | --- | --- |
| A1 | P3 | Contract tests still use substring assertions and could be made more structural by parsing Markdown sections. | Accepted as residual risk for Phase 1. This matches existing `wr-plan`/`wr-spec` test style and remains adequate for current contract regression coverage. |

## Resolutions

Implemented during review:

- Updated `template/.agents/skills/wr-verify/SKILL.md` with:
  - existing `verification.md` preservation rule
  - command derivation/substitution clarity
  - explicit `Command Safety Gate`
- Updated `tests/test_wr_verify_skill.py` with:
  - command derivation/substitution assertions
  - unsafe command boundary assertions
  - existing evidence preservation assertions
  - missing/incomplete planned-check risk assertion
- Re-ran planned verification after the review fixes.

## Residual Risk

- Live Codex runtime invocation of `$wr-verify` was not executed in this pass.
- Tests validate skill instructions and starter inventory, not the quality of every future `verification.md` written by an agent.
- Contract tests are intentionally lightweight substring checks, consistent with current lifecycle skill tests; a future parser-based test helper may be worthwhile if skill text grows.

## Verdict

Approved.

Verification evidence:

- `uvx pytest tests/test_wr_verify_skill.py tests/test_starter_scripts.py` => 28 passed
- `python -m unittest discover -s tests` => 49 passed
- `python -m py_compile scripts/wayrail/_lib/starter.py tests/test_wr_verify_skill.py tests/test_starter_scripts.py` => exit 0

Recommended next action: start the next lifecycle skill spec, `wr-review`.
