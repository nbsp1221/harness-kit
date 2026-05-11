# npm packaging CLI setup Plan

## Overview

Prepare `harness-kit` for later npm publication as `@retn0/harness-kit` without publishing it yet.
This adds npm package metadata, a native Node CLI, package content controls, documentation, and packaging tests while replacing the existing Python implementation of `bootstrap`, `adopt`, and `doctor`.

The implementation should make the npm package the real CLI product surface.
There should be no Python runtime dependency for core `harness-kit` commands after this work is complete.

## Requirements Trace

| Spec ID | Requirement | Plan Coverage | Verification |
| --- | --- | --- | --- |
| R1 | Package name `@retn0/harness-kit` | Unit 1 `package.json` | Package metadata test |
| R2 | Public scoped publishing config | Unit 1 `publishConfig.access` | Package metadata test |
| R3 | Global `harness-kit` binary | Unit 1 bin map, Unit 2 Node CLI | Package metadata and CLI help tests |
| R4 | Fallback `hks` alias | Unit 1 bin map, Unit 2 Node CLI | Package metadata and CLI help tests |
| R5 | Support `bootstrap`, `adopt`, `doctor` | Unit 2 implements commands natively in Node | CLI behavior tests |
| R6 | Preserve command behavior and JSON shape | Unit 2 ports current behavior into Node | CLI behavior tests |
| R7 | Include CLI and starter files | Unit 1 `files` allowlist | `npm pack --dry-run --json` test |
| R8 | Exclude caches/git/temp/research | Unit 1 `files` allowlist | Tarball contents test |
| R9-R10 | Complete package metadata | Unit 1 | Package metadata test |
| R11-R12 | Package scripts and tarball inspection | Unit 1 scripts | `npm run package:check` |
| R13 | No publishing | Unit 1 scripts omit publish automation | Manual inspection, no publish command run |
| R14-R15 | Native Node CLI with no Python delegation | Unit 2 | Code inspection and CLI tests |
| R16 | Document install/usage | Unit 4 root README | README test or inspection |
| R17 | Version ownership explicit | Unit 1 version field | Package metadata test |
| R18 | Remove replaced Python CLI implementation | Unit 3 | Filesystem/package tests |
| R19-R21 | Packaging tests | Unit 5 | Focused test suite |
| R22 | Leave login/publish/release automation later | Unit 1/4 out-of-scope docs | Manual inspection |

## Scope

In scope:

- Create root `package.json`.
- Create npm-facing Node CLI, likely `bin/harness-kit.js`.
- Optionally create root `README.md` for npm package usage.
- Add packaging tests, likely `tests/test_npm_package.py`.
- Add npm scripts for local package inspection and test dispatch.
- Remove the existing Python CLI scripts once the Node CLI covers their behavior.

Out of scope:

- `npm publish`
- release workflow automation
- npm provenance/trusted publishing
- adding new commands beyond `bootstrap`, `adopt`, `doctor`
- adding external runtime dependencies

## Context

Relevant current files:

- `scripts/harness-kit/bootstrap`
- `scripts/harness-kit/adopt`
- `scripts/harness-kit/doctor`
- `scripts/harness-kit/_lib/starter.py`
- `tests/test_starter_scripts.py`
- `template/`
- `template/README.md`

Current conventions:

- Tests are currently Python `unittest`, normally run through `uvx pytest` or `python -m unittest discover -s tests`.
- Existing CLI behavior lives in Python scripts with shebangs and direct execution, but this spec migrates that behavior to Node.
- The starter template source of truth is `template/`.
- There is no root `package.json`, root `README.md`, or npm release configuration yet.

External registry context:

- `@retn0/harness-kit` returned npm 404 on 2026-05-02.
- `@harness-kit/cli` exists and exposes a `harness-kit` binary.
- The package should therefore use scoped package ownership while still providing `harness-kit` and `hks` binaries.

## Decisions

| Decision | Rationale | Alternatives Considered | Requirements Served |
| --- | --- | --- | --- |
| Use `@retn0/harness-kit` as package name | Matches owner namespace and avoids unscoped/third-party brand collision | unscoped `harness-kit`, `harness-kit-starter` | R1, R2 |
| Replace Python CLI with native Node CLI | npm is the target distribution channel, and core commands should not require a second runtime | Python package via PyPI/uv, Node wrapper delegating to Python | R5, R6, R14, R15, R18 |
| Use dependency-free JavaScript for the first Node CLI | Current behavior is file copying, conflict checks, JSON output, and basic arg parsing; this does not require a build step yet | TypeScript build, external CLI framework | R3-R6, R10, R15 |
| Provide both `harness-kit` and `hks` bins | Natural command plus fallback for binary conflicts | only `harness-kit`, only `hks` | R3, R4 |
| Use `files` allowlist in `package.json` | More auditable than `.npmignore` for small package | `.npmignore` only, both | R7, R8, R12 |
| Add root README for npm usage | npm package needs install/usage docs separate from starter README | only template README | R16 |
| Keep tests in Python for this pass | Fits existing test conventions and can test the Node CLI as a subprocess | JS test runner | R19-R21 |
| No publish script | Avoid accidental publication in this setup-only pass | add `release`/`publish` scripts now | R13, R22 |

## Implementation Units

- [ ] Unit 1: Add npm package metadata
  - Requirements: R1, R2, R3, R4, R7, R8, R9, R10, R11, R12, R13, R17, R22
  - Files:
    - Create `package.json`
  - Depends on: none
  - Approach:
    - Set `name` to `@retn0/harness-kit`.
    - Set initial version to `0.0.0` or `0.1.0` based on implementation choice; prefer `0.1.0` if package checks pass and no publish occurs.
    - Set `private` to `false` or omit it; set `publishConfig.access` to `public`.
    - Set `bin` to map `harness-kit` and `hks` to `./bin/harness-kit.js`.
    - Set `files` allowlist to include `bin/`, `template/`, `README.md`, and package metadata.
    - Add scripts such as:
      - `test`: run the repository test suite
      - `package:dry-run`: run `npm pack --dry-run --json`
      - `package:check`: run packaging-focused tests and dry-run pack
    - Do not add a publish script.
  - Verification:
    - Metadata tests parse `package.json`.
    - `npm pack --dry-run --json` returns expected package file list.

- [ ] Unit 2: Add native npm CLI
  - Requirements: R3, R4, R5, R6, R14, R15, R18, R21
  - Files:
    - Create `bin/harness-kit.js`
  - Depends on: Unit 1
  - Approach:
    - Use a Node shebang entrypoint.
    - Parse the first argument as command.
    - Support `bootstrap`, `adopt`, `doctor`.
    - Support `--help` and `-h` at the top level and command level.
    - Port the existing starter behavior into Node:
      - required template file list
      - `bootstrap` and `adopt` target handling
      - `--dry-run`
      - `--json`
      - conflict detection for files, directories, and symlink parents
      - identical-file skip behavior
      - README preservation for `adopt`
      - `doctor` checks and JSON output
    - Forward all remaining args unchanged.
    - Preserve the existing command output contract where tests rely on it.
    - Print a clear error for unknown commands.
    - Avoid external npm dependencies.
  - Verification:
    - CLI help command exits `0`.
    - Unknown command exits non-zero.
    - CLI can run command help, e.g. `node bin/harness-kit.js bootstrap --help`.
    - CLI behavior tests cover bootstrap/adopt/doctor.

- [ ] Unit 3: Remove replaced Python CLI implementation
  - Requirements: R15, R18, SC5
  - Files:
    - Delete `scripts/harness-kit/bootstrap`
    - Delete `scripts/harness-kit/adopt`
    - Delete `scripts/harness-kit/doctor`
    - Delete `scripts/harness-kit/_lib/starter.py`
    - Remove empty `scripts/harness-kit/_lib/` if applicable
  - Depends on: Unit 2
  - Approach:
    - Remove the Python implementation after Node tests cover the same behavior.
    - Update references in tests and docs from `scripts/harness-kit/` to npm CLI paths.
    - Do not keep Python as a reference/test oracle.
  - Verification:
    - Tests assert the removed Python CLI files no longer exist.
    - `npm pack --dry-run --json` does not include `scripts/harness-kit/`.

- [ ] Unit 4: Add npm usage documentation
  - Requirements: R9, R16, R22
  - Files:
    - Create `README.md`
  - Depends on: Unit 1
  - Approach:
    - Document package name: `@retn0/harness-kit`.
    - Document intended future install command: `npm install -g @retn0/harness-kit`.
    - Document current local usage for development.
    - Document commands:
      - `harness-kit bootstrap`
      - `harness-kit adopt`
      - `harness-kit doctor`
      - `hks` alias
    - State that publish/release automation is intentionally not part of this pass.
    - Keep template README unchanged unless package docs need to point to it.
  - Verification:
    - Packaging tests or manual inspection confirm README mentions package and commands.

- [ ] Unit 5: Add packaging and behavior tests
  - Requirements: R19, R20, R21
  - Files:
    - Create `tests/test_npm_package.py`
  - Depends on: Units 1-3
  - Approach:
    - Parse `package.json` with Python `json`.
    - Assert package name, publish config, bin map, files allowlist, script names, and absence of publish automation.
    - Run `node bin/harness-kit.js --help` and `node bin/harness-kit.js bootstrap --help`.
    - Exercise `bootstrap`, `adopt`, and `doctor` against temporary repositories.
    - Assert JSON output shape and conflict handling match the starter contract.
    - Assert the former Python CLI implementation files are absent.
    - Run `npm pack --dry-run --json` and assert expected files are included:
      - `package.json`
      - `README.md`
      - `bin/harness-kit.js`
      - key `template/` files and `hk-*` skill files
    - Assert excluded files do not appear:
      - `.git/`
      - `.pytest_cache/`
      - `__pycache__/`
      - `specs/`
      - `scripts/harness-kit/`
      - `docs/research/`
      - `tests/`
    - Keep tests deterministic and avoid publishing.
  - Verification:
    - `uvx pytest tests/test_npm_package.py tests/test_starter_scripts.py`
    - `npm run package:check`

- [ ] Unit 6: Verify and update lifecycle artifacts
  - Requirements: SC1-SC7
  - Files:
    - Modify `specs/20260502-0026-npm-packaging-cli/verification.md`
    - Later modify `specs/20260502-0026-npm-packaging-cli/review.md`
  - Depends on: Units 1-5
  - Approach:
    - Run focused packaging tests.
    - Run updated starter behavior tests through the Node CLI.
    - Run full unittest discovery.
    - Run npm package dry-run.
    - Run Python compile for touched Python tests.
    - Record that no publish occurred.
  - Verification:
    - See Verification section below.

## Verification

Planned checks:

- `uvx pytest tests/test_npm_package.py tests/test_starter_scripts.py`
- `python -m unittest discover -s tests`
- `python -m py_compile tests/test_npm_package.py tests/test_starter_scripts.py`
- `node bin/harness-kit.js --help`
- `node bin/harness-kit.js bootstrap --help`
- `node bin/harness-kit.js adopt --help`
- `node bin/harness-kit.js doctor --help`
- `npm pack --dry-run --json`
- `npm run package:check`

Expected evidence:

- package metadata has `name: @retn0/harness-kit`
- `bin.harness-kit` and `bin.hks` both point to the Node CLI
- npm tarball dry-run includes CLI/template files and excludes tests/specs/cache/git internals
- Node CLI preserves the starter command behavior expected by tests
- former Python CLI implementation files are absent
- no `npm publish` command is run

## Risks

- Porting the Python behavior to Node may miss a small edge case from the existing implementation.
  - Mitigation: port behavior tests first and cover conflict handling, JSON output, dry-run, adopt README preservation, and doctor checks.
- `harness-kit` binary may conflict with another globally installed package.
  - Mitigation: also expose `hks`.
- `files` allowlist may accidentally omit required template files.
  - Mitigation: test `npm pack --dry-run --json` against required starter files.
- Package metadata could imply public release readiness before release automation exists.
  - Mitigation: docs and scripts should say this prepares packaging but does not publish.
- Using `0.1.0` before publishing could imply semver stability.
  - Mitigation: mark README as initial/prepublish packaging setup if needed.

## Implementation Handoff

Status: Ready for implementation
Plan path: specs/20260502-0026-npm-packaging-cli/plan.md
Spec path: specs/20260502-0026-npm-packaging-cli/spec.md
Implementation order: Unit 1, Unit 2, Unit 3, Unit 4, Unit 5, Unit 6
Recommended next action: implement Units 1-5, then run planned verification and record results.
