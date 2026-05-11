# hk-spec Skill Contract Review

## Summary

Status: pass
Reviewed at: 2026-05-01 02:25 Asia/Seoul

The `hk-spec` implementation satisfies the accepted spec and plan after review feedback was addressed.
The implementation is ready to commit as the first repo-local harness-kit workflow skill.

## Scope

Reviewed artifacts:

- `specs/20260430-0200-hk-spec-skill-contract/spec.md`
- `specs/20260430-0200-hk-spec-skill-contract/plan.md`
- `specs/20260430-0200-hk-spec-skill-contract/verification.md`
- `template/.agents/skills/hk-spec/SKILL.md`
- `template/.agents/skills/hk-spec/agents/openai.yaml`
- `template/.agents/skills/hk-spec/scripts/new-spec-item`
- `scripts/harness-kit/_lib/starter.py`
- `tests/test_hk_spec_skill.py`
- `tests/test_starter_scripts.py`

Review focused on:

- whether Q4-Q7 were closed with implementable decisions
- whether `hk-spec` is installed through the starter template
- whether `new-spec-item` follows the JSON, dry-run, conflict, and validation contracts
- whether tests cover the machine-facing contract and important failure paths
- whether docs, implementation, and verification evidence agree

## Reviewers

- Correctness review: focused on `new-spec-item` and starter integration.
- Test coverage review: focused on requirement coverage and flaky-test risk.
- Documentation consistency review: focused on contradictions between spec, plan, verification, and implementation.

## Findings

Resolved findings:

- `P1`: JSON mode initially dropped the required error envelope on `CreationError`.
- `P2`: Dry-run initially skipped rendered `spec.md` frontmatter validation, so `safe_to_apply` could be misleading.
- `P1`: R19 invalid-invocation exit-code behavior was not covered by tests.
- `P2`: R18 JSON envelope fields were only partially asserted.
- `P2`: R22 creation-preflight versus whole-repo-validation boundary was not protected by a minimal-repo test.

No unresolved review findings remain.

## Resolutions

- Added JSON error envelopes for invalid invocation and `CreationError` paths.
- Render and validate templates during dry-run before reporting `safe_to_apply: true`.
- Added tests for invalid invocation, invalid timezone, generated-spec validation during dry-run, complete JSON envelope fields, and minimal repository operation with only `specs/_templates/`.
- Re-ran verification after the fixes.
- Updated `verification.md` to include the actual `uvx pytest` result.

## Residual Risk

- The script intentionally uses simple line parsing for `artifact_root` in `harness-kit.yaml`. This is acceptable for Phase 1 because the template contract is small and avoiding a YAML dependency keeps starter execution lightweight.
- The script has no real Codex runtime invocation test. This is acceptable for Phase 1 because the agreed acceptance criterion is repository-level testing of skill files and scripts.
- Timestamp generation is real-time. Tests assert format and behavior instead of exact spec IDs.

## Verdict

Approved.

The spec, plan, implementation, verification, and review stages for `hk-spec` are complete.
Recommended next action: commit this change, then start a new spec item for the next lifecycle skill, likely `hk-plan`.
