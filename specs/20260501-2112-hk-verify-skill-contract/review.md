# hk-verify Skill Contract Review

## Summary

Reviewed the `hk-verify` implementation against `spec.md`, `plan.md`, and the starter template conventions.

The implementation matches the agreed Phase 1 direction: `hk-verify` is a repo-local evidence-writing skill, not a code fixer, waiver approver, review stage, or deterministic runner.

Initial review fan-out found contract clarity gaps around unsafe command handling, preserving existing `verification.md` evidence, and test coverage for core behavior rules.
Those findings were addressed and re-verified.

## Scope

Reviewed files:

- `template/.agents/skills/hk-verify/SKILL.md`
- `template/.agents/skills/hk-verify/agents/openai.yaml`
- `scripts/harness-kit/_lib/starter.py`
- `tests/test_hk_verify_skill.py`
- `tests/test_starter_scripts.py`
- `specs/20260501-2112-hk-verify-skill-contract/spec.md`
- `specs/20260501-2112-hk-verify-skill-contract/plan.md`
- `specs/20260501-2112-hk-verify-skill-contract/verification.md`

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
| F1 | P2 | `hk-verify` did not define unsafe command classes, so a planned check could trigger destructive, credentialed, production, install, migration, deletion, or broad-write actions during an evidence-only phase. | Added `Command Safety Gate` to `SKILL.md`; added contract test coverage for local-only default, unsafe command classes, and explicit human authorization. |
| F2 | P2 | `hk-verify` did not instruct agents to preserve existing meaningful `verification.md` content even though the spec assumption requires no overwrite without an explicit replace/revise request. | Added workflow rule to read existing `verification.md` before writing and avoid overwriting non-stub content unless explicitly requested; added contract test coverage. |
| F3 | P2 | Contract tests did not directly cover command derivation order, no silent replacement, substitution rationale, blocked/skipped classification, or missing planned-check risk. | Added targeted assertions in `tests/test_hk_verify_skill.py`; focused and full test suites pass. |

Advisory findings:

| ID | Severity | Finding | Decision |
| --- | --- | --- | --- |
| A1 | P3 | Contract tests still use substring assertions and could be made more structural by parsing Markdown sections. | Accepted as residual risk for Phase 1. This matches existing `hk-plan`/`hk-spec` test style and remains adequate for current contract regression coverage. |

## Resolutions

Implemented during review:

- Updated `template/.agents/skills/hk-verify/SKILL.md` with:
  - existing `verification.md` preservation rule
  - command derivation/substitution clarity
  - explicit `Command Safety Gate`
- Updated `tests/test_hk_verify_skill.py` with:
  - command derivation/substitution assertions
  - unsafe command boundary assertions
  - existing evidence preservation assertions
  - missing/incomplete planned-check risk assertion
- Re-ran planned verification after the review fixes.

## Residual Risk

- Live Codex runtime invocation of `$hk-verify` was not executed in this pass.
- Tests validate skill instructions and starter inventory, not the quality of every future `verification.md` written by an agent.
- Contract tests are intentionally lightweight substring checks, consistent with current lifecycle skill tests; a future parser-based test helper may be worthwhile if skill text grows.

## Verdict

Approved.

Verification evidence:

- `uvx pytest tests/test_hk_verify_skill.py tests/test_starter_scripts.py` => 28 passed
- `python -m unittest discover -s tests` => 49 passed
- `python -m py_compile scripts/harness-kit/_lib/starter.py tests/test_hk_verify_skill.py tests/test_starter_scripts.py` => exit 0

Recommended next action: start the next lifecycle skill spec, `hk-review`.
