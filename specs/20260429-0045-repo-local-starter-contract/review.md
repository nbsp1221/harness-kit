# Repo Local Starter Contract Review

## Summary

Verdict: ready
Reviewed at: 2026-04-30 01:24 Asia/Seoul

The review used a three-way read-only subagent fan-out plus parent synthesis:

- security and external-contract risk
- correctness and testing
- maintainability, simplicity, and performance

The first pass found blocking issues in non-destructive adoption and stable JSON behavior.
Those issues were fixed in `scripts/wayrail/_lib/starter.py`, covered with focused tests, and re-verified.

## Findings

| ID | Severity | Status | Finding | Resolution |
| --- | --- | --- | --- | --- |
| F1 | P1 | fixed | Symlink parent paths could cause starter writes outside the target repository. | `path_conflict` now rejects symlink components in managed starter paths before writes occur. |
| F2 | P1 | fixed | Existing ancestor files such as `docs` could bypass preflight and cause partial writes. | Parent path preflight now reports conflicts before mutation. |
| F3 | P1 | fixed | `adopt` treated an existing project `README.md` as a blocking conflict. | `adopt` now preserves existing `README.md` and continues applying missing starter files. |
| F4 | P2 | fixed | `doctor --json` could traceback on invalid text files instead of returning contract JSON. | Text reads now produce normal failing checks when files are unreadable or invalid UTF-8. |
| F5 | P2 | fixed | A file passed as the target path could escape preflight and fail during apply. | Target paths that already exist as non-directories now produce conflict actions. |
| F6 | P3 | fixed | Test execution recreated `__pycache__` while verification claimed none remained. | Generated Python cache files were removed after verification. |

## Evidence

- `python -m unittest discover -s tests`
  - Result: pass
  - Evidence: `Ran 14 tests in 0.521s` and `OK`
- Smoke check:
  - `bootstrap --dry-run --json` against a missing target did not create the target
  - `bootstrap --json` created the starter shape
  - `doctor --json` passed the bootstrapped fixture
- Cleanup check:
  - `find . -name '__pycache__' -o -name '*.pyc'` returned no output after cleanup

## Residual Risk

- The scripts still assume Python 3 is available.
- `doctor` intentionally validates `wayrail.yaml` by required snippets rather than a full YAML parser.
- Directory handling remains file-oriented for Phase 1; automatic merge and repair remain out of scope.

## Handoff

Status: completed
Spec path: `specs/20260429-0045-repo-local-starter-contract/spec.md`
Implementation paths:

- `template/`
- `scripts/wayrail/`
- `tests/test_starter_scripts.py`

Recommended next action: start the next spec item or begin defining the first `wr-*` skill implementation.
