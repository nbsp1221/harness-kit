# wr-plan Skill Contract Verification

## Summary

`wr-plan` implementation has been verified with focused skill/starter tests, full unittest discovery, and Python compilation checks.

The implementation adds the repo-local `wr-plan` skill to the starter template, includes it in starter inventory, and covers the skill contract with dedicated tests.

## Planned Checks

- `uvx pytest tests/test_wr_plan_skill.py tests/test_starter_scripts.py`
- `python -m unittest discover -s tests`
- `python -m py_compile scripts/wayrail/_lib/starter.py tests/test_wr_plan_skill.py tests/test_starter_scripts.py`
- Manual inspection of `template/.agents/skills/wr-plan/SKILL.md`

## Results

| Check | Result | Evidence |
| --- | --- | --- |
| Focused pytest | Pass | `22 passed in 0.58s` |
| Full unittest discovery | Pass | `Ran 35 tests in 0.985s` / `OK` |
| Python compilation | Pass | command exited `0` |
| Starter inventory | Pass | `tests/test_starter_scripts.py` includes wr-plan files and focused pytest passes |
| Skill contract | Pass | `tests/test_wr_plan_skill.py` checks frontmatter, readiness gate, research rules, write boundary, no `tasks.md`, and no required script |

## Manual Validation

- `template/.agents/skills/wr-plan/SKILL.md` has `name: wr-plan`.
- The description is narrow: it triggers on converting a ready wayrail `spec.md` into `plan.md`.
- The body requires an explicit spec item path or an unambiguous current spec item.
- The readiness gate stops on `Blocked before wr-plan` and unresolved `Resolve Before Planning` questions.
- The workflow requires bounded repository research before writing.
- The boundary says to write only `plan.md` and not edit code, collect verification evidence, write review conclusions, or create `tasks.md`.
- No `template/.agents/skills/wr-plan/scripts/` directory was added.

## Skipped Checks

- Live Codex runtime invocation of `$wr-plan` was not executed in this verification pass.
  The skill is validated as a starter artifact and contract text, matching the existing `wr-spec` test strategy.

## Remaining Risk

- Contract tests validate the skill instructions, not the quality of every future plan an agent writes from those instructions.
- A future helper script may become useful if repeated planning mistakes appear, but Phase 1 intentionally does not add one.

## Review Handoff

Status: Ready for review
Spec path: specs/20260501-0302-wr-plan-skill-contract/spec.md
Plan path: specs/20260501-0302-wr-plan-skill-contract/plan.md
Implementation files:

- template/.agents/skills/wr-plan/SKILL.md
- template/.agents/skills/wr-plan/agents/openai.yaml
- scripts/wayrail/_lib/starter.py
- tests/test_wr_plan_skill.py
- tests/test_starter_scripts.py

Verification evidence:

- `uvx pytest tests/test_wr_plan_skill.py tests/test_starter_scripts.py` => 22 passed
- `python -m unittest discover -s tests` => 35 passed
- `python -m py_compile scripts/wayrail/_lib/starter.py tests/test_wr_plan_skill.py tests/test_starter_scripts.py` => exit 0

Recommended next action: review this implementation.
