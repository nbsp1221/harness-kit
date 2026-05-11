# hk-spec Skill Contract Verification

## Summary

Status: pass
Verified at: 2026-05-01 02:16 Asia/Seoul

The `hk-spec` skill implementation was verified with the dedicated `hk-spec` tests, starter script tests, test discovery under `tests/`, and a manual dry-run JSON smoke check.

## Planned Checks

- Run the focused test set for `hk-spec` and starter scripts.
- Run repository test discovery under `tests/`.
- Run Python syntax compilation for changed Python files and executable scripts.
- Run `new-spec-item --dry-run --json` against a copied starter template.
- Run `new-spec-item --json` normal creation against a copied starter template.
- Confirm dry-run output is a single JSON object with lifecycle paths and no writes.

## Results

Passed:

```bash
uvx pytest tests/test_hk_spec_skill.py tests/test_starter_scripts.py
```

Result: 27 tests passed.

Passed:

```bash
python -m unittest tests.test_hk_spec_skill tests.test_starter_scripts
```

Result: 27 tests passed.

Passed:

```bash
python -m unittest discover -s tests
```

Result: 27 tests passed.

Passed:

```bash
python -m py_compile template/.agents/skills/hk-spec/scripts/new-spec-item scripts/harness-kit/_lib/starter.py tests/test_hk_spec_skill.py tests/test_starter_scripts.py
```

Result: exit code 0.

Passed:

```bash
rm -rf /tmp/hk-smoke
cp -R template /tmp/hk-smoke
template/.agents/skills/hk-spec/scripts/new-spec-item --root /tmp/hk-smoke --slug sample-feature --timezone Asia/Seoul --dry-run --json -- "Sample Feature"
```

Result: exit code 0, `status: planned`, `safe_to_apply: true`, `created_paths: []`, and all four lifecycle paths present in `planned_paths`.

Passed:

```bash
rm -rf /tmp/hk-create
cp -R template /tmp/hk-create
template/.agents/skills/hk-spec/scripts/new-spec-item --root /tmp/hk-create --slug created-feature --timezone Asia/Seoul --json -- "Created Feature"
```

Result: exit code 0, `status: created`, `safe_to_apply: true`, and all four lifecycle files created.

## Manual Validation

- Confirmed `template/.agents/skills/hk-spec/scripts/new-spec-item` is executable.
- Confirmed starter copy logic preserves executable mode with `shutil.copy2`.
- Confirmed Q4, Q5, Q6, and Q7 are no longer listed as deferred questions in `spec.md`.
- Confirmed JSON-mode errors now return a parseable envelope instead of stderr-only output.
- Confirmed dry-run validates rendered `spec.md` frontmatter before reporting `safe_to_apply: true`.
- Confirmed `new-spec-item` works in a minimal repository that has only `specs/_templates/`, preserving the boundary between creation preflight and `doctor`.

## Skipped Checks

- A real Codex runtime skill invocation test was skipped because the agreed contract only requires normal repository tests for Phase 1.

## Remaining Risk

- The generated timestamp is intentionally real-time; tests assert behavior and shape rather than exact IDs.
- The script uses simple YAML line parsing for `artifact_root` instead of a YAML parser to avoid adding dependencies.

## Review Handoff

Status: Reviewed; issues addressed
Spec path: specs/20260430-0200-hk-spec-skill-contract/spec.md
Plan path: specs/20260430-0200-hk-spec-skill-contract/plan.md
Verification path: specs/20260430-0200-hk-spec-skill-contract/verification.md
Recommended next action: decide whether to commit this hk-spec implementation or proceed to the next lifecycle skill.
