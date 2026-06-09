# wr-verify Skill Contract Verification

## Summary

Verdict: pass
Verified at: 2026-05-01 21:12 Asia/Seoul

`wr-verify` implementation has been verified with focused skill/starter tests, full unittest discovery, and Python compilation checks.

The implementation adds the repo-local `wr-verify` skill to the starter template, includes it in starter inventory, and covers the skill contract with dedicated tests.
After review fan-out, the verification contract was tightened for unsafe command handling, existing `verification.md` preservation, and more explicit contract test coverage.

## Planned Checks

- `uvx pytest tests/test_wr_verify_skill.py tests/test_starter_scripts.py`
- `python -m unittest discover -s tests`
- `python -m py_compile scripts/wayrail/_lib/starter.py tests/test_wr_verify_skill.py tests/test_starter_scripts.py`
- Manual inspection of `template/.agents/skills/wr-verify/SKILL.md`
- Manual inspection that no `template/.agents/skills/wr-verify/scripts/` is required or referenced as required

## Results

| Check | Result | Evidence |
| --- | --- | --- |
| Focused pytest | pass | `28 passed in 0.53s` |
| Full unittest discovery | pass | `Ran 49 tests in 0.938s` / `OK` |
| Python compilation | pass | command exited `0` |
| Starter inventory | pass | `scripts/wayrail/_lib/starter.py` and `tests/test_starter_scripts.py` include `wr-verify` files; focused pytest passes |
| Skill contract | pass | `tests/test_wr_verify_skill.py` checks frontmatter, explicit spec path, `spec.md`/`plan.md` reads, `Implementation Handoff`, fresh evidence, command derivation/substitution, safety gate, result labels, `verification.md` sections, skipped/blocked/manual details, existing evidence preservation, write boundary, no fixes/review/waivers, and no required script |

## Manual Validation

- `template/.agents/skills/wr-verify/SKILL.md` has `name: wr-verify`.
- The description is narrow: it triggers on converting an implemented wayrail spec item into `verification.md` evidence.
- The body requires an explicit spec item path or an unambiguous current spec item.
- The readiness gate requires reading `spec.md` and `plan.md`, then checking `Implementation Handoff`.
- The workflow requires planned verification checks to run fresh from the current workspace unless unsafe, unavailable, or blocked.
- The command safety gate blocks destructive, production, credentialed, dependency-installing, migration, deletion, and broad-write commands without explicit human authorization.
- Existing meaningful `verification.md` content must not be overwritten unless the user explicitly asks to replace or revise it.
- The result labels are defined as `pass`, `fail`, `skipped`, and `blocked` per check, and `pass`, `fail`, `partial`, and `blocked` overall.
- The authoring rules require Summary, Planned Checks, Results, Manual Validation, Skipped Checks, Remaining Risk, and Review Handoff.
- The boundary says to write only `verification.md` and not edit code, tests, `spec.md`, `plan.md`, `review.md`, approve waivers, declare review complete, or create `tasks.md`.
- No `template/.agents/skills/wr-verify/scripts/` directory was added.

## Skipped Checks

- Live Codex runtime invocation of `$wr-verify` was not executed in this verification pass.
  The skill is validated as a starter artifact and contract text, matching the existing `wr-spec` and `wr-plan` test strategy.

## Remaining Risk

- Contract tests validate the skill instructions, not the quality of every future verification artifact an agent writes from those instructions.
- Live runtime skill selection may still reveal wording issues; dogfooding the next implemented item should exercise that path.

## Review Handoff

Status: Ready for review
Spec path: specs/20260501-2112-wr-verify-skill-contract/spec.md
Plan path: specs/20260501-2112-wr-verify-skill-contract/plan.md
Implementation files:

- template/.agents/skills/wr-verify/SKILL.md
- template/.agents/skills/wr-verify/agents/openai.yaml
- scripts/wayrail/_lib/starter.py
- tests/test_wr_verify_skill.py
- tests/test_starter_scripts.py

Verification evidence:

- `uvx pytest tests/test_wr_verify_skill.py tests/test_starter_scripts.py` => 28 passed
- `python -m unittest discover -s tests` => 49 passed
- `python -m py_compile scripts/wayrail/_lib/starter.py tests/test_wr_verify_skill.py tests/test_starter_scripts.py` => exit 0

Recommended next action: review this implementation.
