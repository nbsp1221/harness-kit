# Repo Local Starter Contract Plan

## Overview

Implement the first usable `wayrail` starter surface as a repo-local, scripts-first contract.
The implementation should add the product-side starter templates, starter scripts, and focused tests needed to install or inspect the downstream starter shape described in `spec.md`.

This plan intentionally stops before packaged CLI distribution, host-specific skill installation, automatic Markdown merging, broad `--force`, hooks, runtime state, or workflow skill implementation.

## Requirements Trace

| Spec ID | Requirement | Plan Coverage | Verification |
| --- | --- | --- | --- |
| R1 | Thin root `AGENTS.md` | Unit 1 creates `template/AGENTS.md` | Inspect template content and bootstrap output |
| R2 | Repo-local `wayrail.yaml` | Unit 1 creates `template/wayrail.yaml` | Parse YAML or validate expected text keys |
| R3 | `docs/roadmap/README.md` | Unit 1 creates downstream roadmap template | Inspect file exists after bootstrap/adopt |
| R4 | `specs/` artifact root | Unit 1 and Unit 2 create/preserve `specs/` | Bootstrap/adopt fixture assertions |
| R5 | Lifecycle templates under `specs/_templates/` | Unit 1 creates four templates | Assert all four files exist |
| R6 | `memory/learnings.md` | Unit 1 creates learning template | Assert file exists and is non-empty |
| R7 | `scripts/wayrail/bootstrap`, `adopt`, `doctor` | Unit 2 adds product scripts | `--help`, `--dry-run`, and fixture runs |
| R8 | Non-destructive bootstrap/adopt | Unit 3 implements conflict detection | Existing-file fixture assertions |
| R9 | Agent-readable script behavior | Unit 2 and Unit 3 define JSON output and exit codes | JSON parsing tests |
| R10 | No broad runtime/platform features | Unit 1-4 keep scope limited | Review file tree and script behavior |

## Scope

In scope for this implementation pass:

- product-side `template/` starter files
- repo-local starter scripts under `scripts/wayrail/`
- script contracts for `bootstrap`, `adopt`, and `doctor`
- non-destructive file creation and conflict reporting
- JSON output for agent/script consumption
- test fixtures for blank bootstrap, existing-repo adoption, conflict reporting, and doctor validation

Out of scope for this implementation pass:

- packaged `hk` CLI
- `wr-spec`, `wr-plan`, `wr-verify`, or `wr-review` skill implementation
- Codex plugin or host adapter installation
- automatic Markdown merge
- broad `--force`
- `doctor --fix`
- hooks, task database, dashboard, runtime state, background orchestration
- global config or local override config

## Context

Relevant source documents:

- `specs/20260429-0045-repo-local-starter-contract/spec.md`
- `docs/roadmap/phases/phase-1-starter-foundation.md`
- `docs/plans/2026-04-23-phase-1-foundation-decisions.md`
- `docs/plans/2026-04-22-minimum-working-model-design.md`

Current repository facts:

- No starter `template/` directory exists yet.
- No product-side `scripts/wayrail/` directory exists yet.
- The repository currently contains planning, roadmap, and research docs plus this first `specs/<id>/` item.
- The repository has no committed baseline yet, so test fixtures should not rely on existing git history.

Implementation runtime choice:

- Use Python 3 standard library for starter scripts.
- Keep public script entrypoints at `scripts/wayrail/bootstrap`, `scripts/wayrail/adopt`, and `scripts/wayrail/doctor`.
- The script files may be Python executables with shebangs, or thin executable wrappers around shared Python modules if that keeps tests cleaner.

Suggested product-side helper layout:

```text
template/
  README.md
  AGENTS.md
  wayrail.yaml
  docs/
    roadmap/
      README.md
  specs/
    .gitkeep
    _templates/
      spec.md
      plan.md
      verification.md
      review.md
  memory/
    learnings.md
scripts/
  wayrail/
    bootstrap
    adopt
    doctor
tests/
  fixtures/
  test_starter_scripts.py
```

If shared logic is needed, prefer a small internal module under `scripts/wayrail/lib/` or `scripts/wayrail/_lib/` rather than introducing package metadata.

## Decisions

| Decision | Rationale | Alternatives Considered | Requirements Served |
| --- | --- | --- | --- |
| Use product-side `template/` as the single starter source | Keeps downstream installed artifacts separate from product docs | Generate templates inline from scripts | R1-R6, R10 |
| Use Python 3 standard library for scripts | Reliable JSON, path handling, comparison, and tests without packaging | Bash scripts; full CLI package | R7-R9 |
| Make scripts non-interactive | Agents and CI need predictable behavior | Prompt on conflicts | R8-R9 |
| Add `--dry-run` and `--json` from the start | Lets agents inspect changes before mutation | Human-only text output | R8-R9 |
| Abort on conflicts before mutation | Prevents partial adoption and preserves existing files | Create safe files then report conflicts | R8 |
| Treat identical existing files as satisfied | Idempotent reruns should be harmless | Fail on all pre-existing files | R8 |
| Keep `doctor` report-only | Maintains boundary between validation and repair | `doctor --fix` now | R7-R10 |

## Implementation Units

- [x] Unit 1: Add starter template files
  - Requirements: R1, R2, R3, R4, R5, R6, R10
  - Files:
    - Create `template/README.md`
    - Create `template/AGENTS.md`
    - Create `template/wayrail.yaml`
    - Create `template/docs/roadmap/README.md`
    - Create `template/specs/.gitkeep`
    - Create `template/specs/_templates/spec.md`
    - Create `template/specs/_templates/plan.md`
    - Create `template/specs/_templates/verification.md`
    - Create `template/specs/_templates/review.md`
    - Create `template/memory/learnings.md`
  - Approach:
    - Keep templates concise and downstream-oriented.
    - Use the starter `AGENTS.md` wording from the foundation decision record.
    - Make lifecycle templates match the documented sections.
    - Avoid host-specific or `wayrail` product-repo-only text in downstream templates.
  - Verification:
    - Inspect every template path.
    - Confirm `wayrail.yaml` contains only Phase 1 keys.
    - Confirm templates do not mention packaged CLI, host plugins, hooks, or runtime state as installed defaults.

- [x] Unit 2: Add shared starter script behavior
  - Requirements: R7, R8, R9, R10
  - Files:
    - Create `scripts/wayrail/bootstrap`
    - Create `scripts/wayrail/adopt`
    - Create `scripts/wayrail/doctor`
    - Optionally create `scripts/wayrail/_lib/` for shared Python helpers
  - Approach:
    - Implement `--help`, `--dry-run`, and `--json` where useful.
    - Accept an explicit target path argument or default to current working directory.
    - Resolve the product template source relative to the script location.
    - Emit JSON to stdout in JSON mode and diagnostics to stderr.
    - Use clear exit codes: `0` success or warnings-only, `1` conflicts or contract failures, `2` invalid invocation/internal error.
  - Verification:
    - Run each script with `--help`.
    - Run each script with `--json --dry-run` against a temp fixture and parse JSON.
    - Confirm no script creates runtime directories, hooks, task databases, or host config.

- [x] Unit 3: Implement bootstrap/adopt creation and conflict policy
  - Requirements: R1, R2, R3, R4, R5, R6, R8, R9
  - Files:
    - Modify `scripts/wayrail/bootstrap`
    - Modify `scripts/wayrail/adopt`
    - Modify shared helper files if introduced
    - Add tests under `tests/`
  - Approach:
    - Model file actions as `create`, `skip-identical`, `preserve`, and `conflict`.
    - Precompute all actions before writing.
    - If conflicts exist, exit non-zero and do not apply partial writes.
    - `bootstrap` and `adopt` share the same target artifact set but differ in messaging and assumptions.
    - Preserve existing `README.md`, `AGENTS.md`, `docs/`, `specs/`, and `memory/` contents.
  - Verification:
    - Blank fixture: bootstrap creates the full starter shape.
    - Rerun fixture: bootstrap/adopt reports identical files without destructive changes.
    - Existing `AGENTS.md` fixture: adopt reports conflict or manual integration without overwrite.
    - Existing unrelated docs fixture: adopt preserves existing docs.
    - JSON output includes `actions` and `safe_to_apply`.

- [x] Unit 4: Implement doctor starter contract validation
  - Requirements: R2, R4, R5, R6, R7, R9, R10
  - Files:
    - Modify `scripts/wayrail/doctor`
    - Add tests under `tests/`
  - Approach:
    - Validate setup health only.
    - Check required starter paths, minimal `wayrail.yaml` shape, lifecycle template presence, and starter script presence.
    - Treat optional integrations as `warn` or `skip`, not `fail`.
    - Do not run project tests, install dependencies, modify files, or perform network checks.
    - Provide stable `--json` shape with `schema_version`, `status`, `repo_root`, `checks`, and `summary`.
  - Verification:
    - Valid fixture returns exit `0` with status `pass`.
    - Missing required file fixture returns exit `1` with status `fail`.
    - Invalid invocation returns exit `2`.
    - JSON parses and contains categorized checks.
    - Warnings do not fail by default.

- [x] Unit 5: Add focused tests and documentation notes
  - Requirements: R8, R9, R10, SC1, SC2, SC3
  - Files:
    - Create or update `tests/`
    - Optionally update `docs/roadmap/phases/phase-1-starter-foundation.md` only if implementation reveals a contract mismatch
  - Approach:
    - Prefer Python standard library tests if the scripts are Python.
    - Use temporary directories instead of modifying the real repository as test targets.
    - Test both human-readable and JSON paths where practical.
    - Keep docs changes limited to implementation-discovered corrections.
  - Verification:
    - Run the focused test command for starter scripts.
    - Run direct smoke checks for `bootstrap`, `adopt`, and `doctor`.
    - Inspect generated fixture tree against the expected starter shape.

## Verification

Expected checks after implementation:

```bash
python -m pytest tests
```

If pytest is not available or no test runner is introduced, use standard library tests instead:

```bash
python -m unittest discover -s tests
```

Script smoke checks:

```bash
scripts/wayrail/bootstrap --help
scripts/wayrail/adopt --help
scripts/wayrail/doctor --help
```

Fixture checks:

```bash
scripts/wayrail/bootstrap --dry-run --json <blank-fixture>
scripts/wayrail/bootstrap --json <blank-fixture>
scripts/wayrail/adopt --dry-run --json <existing-fixture>
scripts/wayrail/doctor --json <bootstrapped-fixture>
```

Expected evidence:

- JSON output parses successfully.
- Blank bootstrap creates the required starter artifact set.
- Adoption preserves existing user-authored files.
- Conflicts produce a non-zero exit and no partial mutation.
- Doctor validates starter shape without running project tests or changing files.

Manual validation:

- Inspect a bootstrapped fixture tree.
- Inspect an adoption conflict report for an existing `AGENTS.md`.
- Confirm no generated file claims host-specific runtime support or packaged CLI availability.

## Risks

- Python 3 may not be available in every downstream environment.
  - Mitigation: document Python 3 as the Phase 1 script runtime; revisit packaging if distribution pressure appears.
- Conflict detection can become ambiguous for directories.
  - Mitigation: start with file-level action reporting and preserve existing directories by default.
- `README.md` handling may be sensitive in adoption.
  - Mitigation: never overwrite existing `README.md`; report manual action instead.
- Tests may accidentally validate product repo files rather than downstream generated files.
  - Mitigation: use temp fixtures and compare generated target trees.
- Starter templates may become too verbose.
  - Mitigation: keep root `AGENTS.md` and roadmap templates thin; move detail to docs only after real need appears.

## Implementation Handoff

Status: Ready for implementation
Spec path: `specs/20260429-0045-repo-local-starter-contract/spec.md`
Plan path: `specs/20260429-0045-repo-local-starter-contract/plan.md`
Primary implementation targets: `template/`, `scripts/wayrail/`, `tests/`
Do not implement: workflow skills, packaged CLI, force/merge modes, hooks, runtime platform, or host adapters
