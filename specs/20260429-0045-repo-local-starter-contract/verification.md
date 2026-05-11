# Repo Local Starter Contract Verification

## Summary

Verdict: pass
Verified at: 2026-04-30 01:23 Asia/Seoul
Spec: `specs/20260429-0045-repo-local-starter-contract/spec.md`
Plan: `specs/20260429-0045-repo-local-starter-contract/plan.md`

The starter templates, starter scripts, conflict behavior, JSON output, and doctor validation were verified with focused unit tests and smoke checks.

## Planned Checks

| ID | Requirement/Unit | Planned check | Expected evidence |
| --- | --- | --- | --- |
| V1 | Unit 1, R1-R6 | Template file presence and minimal config shape | Required starter files exist; config has Phase 1 keys |
| V2 | Unit 2, R7-R9 | Script help and JSON behavior | `bootstrap`, `adopt`, `doctor` expose help and parseable JSON |
| V3 | Unit 3, R8-R9 | Bootstrap/adopt fixture behavior | Blank repo is created; existing conflicting `AGENTS.md` is preserved |
| V4 | Unit 4, R7-R9 | Doctor fixture behavior | Bootstrapped repo passes; missing required file fails |
| V5 | Unit 5, SC1-SC3 | Focused tests | Test suite passes |

## Results

| ID | Result | Command or method | Evidence |
| --- | --- | --- | --- |
| V1 | pass | `python -m unittest discover -s tests` | 14 tests ran, 0 failures |
| V2 | pass | `python -m unittest discover -s tests` | help checks and JSON parsing tests passed |
| V3 | pass | `python -m unittest discover -s tests` | bootstrap/adopt fixture tests passed, including README preserve, ancestor-file conflict, symlink-parent conflict, and file-target conflict |
| V4 | pass | `python -m unittest discover -s tests` | doctor valid, missing-file, and invalid UTF-8 config tests passed |
| V5 | pass | `python -m unittest discover -s tests` | output: `Ran 14 tests in 0.521s` and `OK` |
| V6 | pass | smoke check with temp directories | `bootstrap --dry-run --json` did not create the target directory; `bootstrap --json` and `doctor --json` succeeded |

## Manual Validation

- Inspected generated file list under `template/`, `scripts/harness-kit/`, and `tests/`.
- Confirmed no generated `__pycache__` or `.pyc` files remain after test execution.
- Confirmed smoke adoption report preserves an existing divergent `AGENTS.md` by reporting `conflict` and `safe_to_apply: false`.
- Confirmed dry-run does not create a missing target directory.
- Confirmed review-discovered blockers were fixed and covered by tests:
  - existing `README.md` no longer blocks `adopt`
  - ancestor-file conflicts are reported before mutation
  - symlink parents are conflicts and do not write outside the target
  - invalid UTF-8 config produces JSON failure output instead of a traceback

## Skipped Checks

None.

## Remaining Risk

- The scripts assume Python 3 is available.
- The current implementation validates `harness-kit.yaml` by required text snippets rather than a full YAML parser.
- Directory conflict handling is intentionally simple and file-oriented for Phase 1.

## Review Handoff

Verdict: pass
Evidence artifacts:
- `tests/test_starter_scripts.py`
- `template/`
- `scripts/harness-kit/`
- this `verification.md`

Suggested review focus:
- non-destructive conflict behavior in `scripts/harness-kit/_lib/starter.py`
- whether downstream template wording is sufficiently thin
- whether doctor should require or only report product-side starter scripts in future phases

Recommended next action: hk-review
