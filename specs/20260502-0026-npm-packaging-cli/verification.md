# npm packaging CLI setup Verification

## Summary

Status: pass
Verified at: 2026-05-02 Asia/Seoul

`@retn0/harness-kit` now has npm package metadata, a dependency-free native Node CLI, package file selection checks, and behavior tests for `bootstrap`, `adopt`, and `doctor`.
The previous Python CLI implementation under `scripts/harness-kit/` has been removed.
No publish command was run.

## Planned Checks

- `uvx pytest tests/test_npm_package.py tests/test_starter_scripts.py`
- `python -m unittest discover -s tests`
- `python -m py_compile tests/test_npm_package.py tests/test_starter_scripts.py`
- `node bin/harness-kit.js --help`
- `node bin/harness-kit.js bootstrap --help`
- `node bin/harness-kit.js adopt --help`
- `node bin/harness-kit.js doctor --help`
- `npm pack --dry-run --json`
- `npm run package:check`
- `./bin/harness-kit.js --help`
- Confirm `scripts/harness-kit/` no longer contains Python CLI files

## Results

- Pass: `uvx pytest tests/test_npm_package.py tests/test_starter_scripts.py`
  - Result: `18 passed in 0.66s`
- Pass: `python -m unittest discover -s tests`
  - Result: `Ran 68 tests in 1.073s`, `OK`
- Pass: `python -m py_compile tests/test_npm_package.py tests/test_starter_scripts.py`
  - Result: exit `0`
- Pass: `node bin/harness-kit.js --help`
  - Result: exit `0`; output listed `bootstrap`, `adopt`, `doctor`, and `hks`
- Pass: `node bin/harness-kit.js bootstrap --help`
  - Result: exit `0`
- Pass: `node bin/harness-kit.js adopt --help`
  - Result: exit `0`
- Pass: `node bin/harness-kit.js doctor --help`
  - Result: exit `0`
- Pass: `npm pack --dry-run --json`
  - Result: exit `0`
  - Package: `@retn0/harness-kit@0.1.0`
  - Entry count: `22`
  - Included: `README.md`, `package.json`, `bin/harness-kit.js`, `template/`, and repo-local `hk-*` skills
  - Excluded by test: `specs/`, `tests/`, `.pytest_cache/`, `__pycache__/`, `docs/research/`, and `scripts/harness-kit/`
- Pass: `npm run package:check`
  - Result: `Ran 68 tests in 1.050s`, `OK`, followed by successful `npm pack --dry-run --json`
- Pass: `./bin/harness-kit.js --help`
  - Result: exit `0`; executable bit is set and the shebang path works
- Pass: `find scripts -maxdepth 4 -type f -print`
  - Result: no files; the former Python CLI files are absent

## Manual Validation

- Confirmed `package.json` exposes both `harness-kit` and `hks` binaries pointing at `./bin/harness-kit.js`.
- Confirmed `package.json` has no `publish` or `release` script.
- Confirmed `package.json` uses `publishConfig.access: public`.
- Confirmed `bin/harness-kit.js` implements `bootstrap`, `adopt`, and `doctor` directly in Node.js rather than spawning Python.
- Confirmed tests exercise:
  - dry-run JSON output without writing
  - full starter bootstrap
  - adopt conflict handling without partial mutation
  - adopt README preservation
  - ancestor file conflict
  - symlink parent conflict
  - identical-file skip behavior
  - doctor pass/fail JSON output
  - invalid UTF-8 config handling
  - npm tarball contents
  - removed Python CLI implementation

## Skipped Checks

- Actual `npm publish` was intentionally skipped. Publishing, npm login, provenance, trusted publishing, and release automation are out of scope for this spec item.
- No separate JS test runner was introduced. Existing Python `unittest`/`pytest` tests invoke the Node CLI as a subprocess.

## Remaining Risk

- The Node CLI is a behavior port from the previous Python implementation. The covered starter behaviors pass, but future command growth may justify extracting shared JS helpers or adopting TypeScript.
- The package metadata uses `MIT`; the owner explicitly deferred adding the root license file until later before first public publication.

## Review Handoff

Status: Ready for hk-review
Spec path: specs/20260502-0026-npm-packaging-cli/spec.md
Plan path: specs/20260502-0026-npm-packaging-cli/plan.md
Verification path: specs/20260502-0026-npm-packaging-cli/verification.md
Implemented files: package.json, README.md, bin/harness-kit.js, tests/test_npm_package.py, tests/test_starter_scripts.py
Removed files: scripts/harness-kit/bootstrap, scripts/harness-kit/adopt, scripts/harness-kit/doctor, scripts/harness-kit/_lib/starter.py
Recommended next action: hk-review
