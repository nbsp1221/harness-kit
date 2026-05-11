# hk-review Skill Contract Verification

## Summary

Status: pass

Implemented `hk-review` as a repo-local starter skill and verified the skill contract, starter inventory, full test suite, and Python compilation checks.
After review found two parent-decidable issues, fixed the missing-`review.md` contract contradiction and strengthened residual-risk verdict policy tests, then re-ran the planned checks successfully.

## Planned Checks

- `V1`: `uvx pytest tests/test_hk_review_skill.py tests/test_starter_scripts.py`
- `V2`: `python -m unittest discover -s tests`
- `V3`: `python -m py_compile scripts/harness-kit/_lib/starter.py tests/test_hk_review_skill.py tests/test_starter_scripts.py`
- `V4`: Manual inspection that `template/.agents/skills/hk-review/SKILL.md` remains review-only and contains the required Review Handoff, diff, delegation, finding, severity, resolution, verdict, preservation, and boundary rules.
- `V5`: Manual inspection that Phase 1 does not require `template/.agents/skills/hk-review/scripts/`.

## Results

- `V1`: pass
  - Command: `uvx pytest tests/test_hk_review_skill.py tests/test_starter_scripts.py`
  - Working directory: `/home/retn0/repositories/nbsp1221/harness-kit`
  - Exit status: `0`
  - Evidence: initial run `29 passed in 0.63s`; post-review-fix rerun `29 passed in 0.53s`
- `V2`: pass
  - Command: `python -m unittest discover -s tests`
  - Working directory: `/home/retn0/repositories/nbsp1221/harness-kit`
  - Exit status: `0`
  - Evidence: initial run `Ran 64 tests in 0.954s`, `OK`; post-review-fix rerun `Ran 64 tests in 0.949s`, `OK`
- `V3`: pass
  - Command: `python -m py_compile scripts/harness-kit/_lib/starter.py tests/test_hk_review_skill.py tests/test_starter_scripts.py`
  - Working directory: `/home/retn0/repositories/nbsp1221/harness-kit`
  - Exit status: `0`
  - Evidence: command completed with no output on initial and post-review-fix runs.
- `V4`: pass
  - Evidence: `template/.agents/skills/hk-review/SKILL.md` defines a review-only workflow that reads `spec.md`, `plan.md`, `verification.md`, existing `review.md`, inspects diff read-only, preserves existing review content, writes only `review.md`, and forbids implementation, verification, fixes, waivers, merge, commit, release approval, and scope changes.
- `V5`: pass
  - Evidence: `template/.agents/skills/hk-review/scripts/` does not exist; tests assert no scripts directory for `hk-review`.

## Manual Validation

- Confirmed the initial focused test run failed before implementation because `template/.agents/skills/hk-review/SKILL.md` and starter entries were missing.
- Confirmed the starter inventory now includes `.agents/skills/hk-review/SKILL.md` and `.agents/skills/hk-review/agents/openai.yaml`.
- Confirmed test caches created by verification were removed after the run.
- Confirmed post-review-fix tests now assert missing `review.md` is allowed and that `ready-with-residual-risk` depends on non-blocking residual risk conditions.

## Skipped Checks

- Live Codex invocation of `$hk-review` through a fresh skill registry was not run in this implementation step.
  - Reason: Phase 1 verification validates the repo-local skill contract and starter artifacts without requiring a live Codex runtime.
  - Required for pass: no.
  - Residual risk: runtime skill discovery in a fresh session remains dogfooding evidence to collect later.
  - Owner or next step: confirm fresh-session skill discovery before release packaging.

## Remaining Risk

- The skill is instruction-only; tests validate contract text and starter presence, not whether every future agent will follow the instructions perfectly.
- Fresh-session skill discovery should be checked before release packaging.

## Review Handoff

Status: Ready for review

Commands or checks run:

- `uvx pytest tests/test_hk_review_skill.py tests/test_starter_scripts.py` before and after review fixes
- `python -m unittest discover -s tests` before and after review fixes
- `python -m py_compile scripts/harness-kit/_lib/starter.py tests/test_hk_review_skill.py tests/test_starter_scripts.py` before and after review fixes
- Manual inspection of `template/.agents/skills/hk-review/SKILL.md`
- Manual inspection that no Phase 1 `hk-review/scripts/` directory exists

Results:

- pass: focused pytest, full unittest, Python compilation, manual skill inspection, no-script inspection
- fail: none
- blocked: none
- skipped: fresh-session live Codex skill discovery invocation

Manual evidence:

- `hk-review` files exist under `template/.agents/skills/hk-review/`.
- Starter bootstrap/adopt inventory includes `hk-review`.
- `tests/test_hk_review_skill.py` covers Review Handoff completeness, fresh-context review, safe read-only diff inspection, delegated reviewer boundaries, finding schema, severity/resolution/verdict labels, resolution authority, existing review preservation, write-boundary, no-fix, no-approval, and no-script rules.

Known gaps:

- No fresh-session `$hk-review` runtime discovery check yet.

Residual risks:

- The Phase 1 skill depends on agent adherence to written instructions.
- Fresh-session runtime skill discovery should be assessed before release packaging.

Recommended next action: finalize review for this spec item.
