# npm packaging CLI setup Review

## Summary

Review date: 2026-05-02 Asia/Seoul

The npm packaging CLI implementation satisfies the core spec direction: `@retn0/harness-kit` is package-shaped, exposes `harness-kit` and `hks`, implements `bootstrap`, `adopt`, and `doctor` directly in Node.js, and removes the previous Python CLI implementation under `scripts/harness-kit/`.

Verification evidence is complete for the declared package checks, CLI behavior checks, tarball contents, and Python CLI removal.
No actual publish occurred.

## Scope

- Reviewed lifecycle artifacts:
  - `specs/20260502-0026-npm-packaging-cli/spec.md`
  - `specs/20260502-0026-npm-packaging-cli/plan.md`
  - `specs/20260502-0026-npm-packaging-cli/verification.md`
- Reviewed implementation files:
  - `package.json`
  - `README.md`
  - `bin/harness-kit.js`
  - `tests/test_npm_package.py`
  - `tests/test_starter_scripts.py`
- Reviewed removal evidence:
  - `scripts/harness-kit/bootstrap`
  - `scripts/harness-kit/adopt`
  - `scripts/harness-kit/doctor`
  - `scripts/harness-kit/_lib/starter.py`

## Reviewers

- Primary reviewer: Codex parent reviewer, fresh-context `hk-review` pass.
- Delegated reviewers: not used. The current environment only allows spawned subagents when explicitly requested in the active turn; this review was performed directly against the lifecycle artifacts, untracked workspace state, implementation files, and verification evidence.

## Findings

- `F1`
  - Severity: `P3`
  - Resolution: `deferred`
  - Reviewer/source: primary reviewer
  - Location: `package.json`
  - Artifact reference: `verification.md` Remaining Risk
  - Evidence: `package.json` declares `license: MIT`, but there is no root `LICENSE` file in the reviewed package setup.
  - Behavioral risk: This does not block local packaging or the current no-publish spec, but the first public npm publish should not rely on an implicit license decision.
  - Recommendation: Before actual publication, add or confirm the intended root license file and make sure it matches `package.json`.
  - Deferral source: owner instruction on 2026-05-02: the license file will be added later.
  - Decision authority: `human-required`

## Resolutions

- Core package metadata is present and verified:
  - `name: @retn0/harness-kit`
  - `version: 0.1.0`
  - `publishConfig.access: public`
  - `bin.harness-kit` and `bin.hks`
  - `files` allowlist
- Native Node CLI requirement is met:
  - `bin/harness-kit.js` implements core command behavior directly.
  - No Python subprocess delegation is present.
- Python CLI removal requirement is met:
  - Former `scripts/harness-kit/*` Python entrypoints and `_lib/starter.py` are absent.
  - Tests assert the removed paths do not exist.
- Package content requirement is met:
  - `npm pack --dry-run --json` includes package runtime files and starter template files.
  - Tests assert `specs/`, `tests/`, caches, research docs, and `scripts/harness-kit/` are excluded.
- Verification handoff is complete:
  - Focused pytest, full unittest discovery, py_compile, Node help commands, npm pack dry run, package check, executable shebang check, and removal evidence are recorded.

## Residual Risk

- `F1`: The license metadata says MIT, and the owner has deferred adding the root license file until later before first public publication.
- The CLI is currently dependency-free JavaScript. That is appropriate for the current small command surface, but future command growth may justify a TypeScript build or shared module extraction.

## Verdict

`ready-with-residual-risk`

The implementation is ready for human approval for this no-publish packaging step.
The only material residual item is the owner-deferred license file before a future actual npm publication.
