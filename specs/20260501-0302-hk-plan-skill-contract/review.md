# hk-plan Skill Contract Review

## Summary

Reviewed the `hk-plan` implementation against `spec.md`, `plan.md`, and the starter template conventions.

The implementation matches the agreed Phase 1 direction: `hk-plan` is a repo-local skill artifact, not a script-driven task generator.
It is included in starter inventory and covered by focused contract tests.

## Scope

Reviewed files:

- `template/.agents/skills/hk-plan/SKILL.md`
- `template/.agents/skills/hk-plan/agents/openai.yaml`
- `scripts/harness-kit/_lib/starter.py`
- `tests/test_hk_plan_skill.py`
- `tests/test_starter_scripts.py`
- `specs/20260501-0302-hk-plan-skill-contract/spec.md`
- `specs/20260501-0302-hk-plan-skill-contract/plan.md`
- `specs/20260501-0302-hk-plan-skill-contract/verification.md`

## Reviewers

- Primary review: local implementation review against lifecycle spec and plan.

## Findings

No blocking findings.

Checked:

- `hk-plan` frontmatter uses `name: hk-plan`.
- Trigger wording is limited to converting a ready harness-kit `spec.md` into `plan.md`.
- Readiness gate is explicit and stops on blocked specs.
- Workflow requires bounded repository research before writing.
- Write boundary is explicit: only `plan.md`.
- Prohibitions cover source edits, implementation, verification evidence, review conclusions, and `tasks.md`.
- Phase 1 no-script decision is reflected in both skill text and tests.
- Starter inventory includes the new skill files.
- Tests cover the contract without requiring a live Codex runtime.

## Resolutions

None required.

## Residual Risk

- The tests validate skill instructions and starter inventory, not the behavior of a live Codex runtime selecting the skill.
- Future plans still depend on the acting agent following the bounded research and handoff instructions.
- If repeated misuse appears, a later validation helper may be justified, but that is intentionally out of scope for Phase 1.

## Verdict

Approved.

Verification evidence:

- `uvx pytest tests/test_hk_plan_skill.py tests/test_starter_scripts.py` => 22 passed
- `python -m unittest discover -s tests` => 35 passed
- `python -m py_compile scripts/harness-kit/_lib/starter.py tests/test_hk_plan_skill.py tests/test_starter_scripts.py` => exit 0

Recommended next action: start the next lifecycle skill spec, likely `hk-verify`, unless the user wants to refine `hk-plan` behavior first.
