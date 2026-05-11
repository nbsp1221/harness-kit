# hk-spec Skill Contract Plan

## Overview

Implement the first repo-local harness-kit workflow skill: `hk-spec`.
The starter template will install `.agents/skills/hk-spec/` into downstream repositories.
The skill will run a deterministic `scripts/new-spec-item` helper before any prose authoring, then guide the agent to fill only `spec.md`.

The implementation should stay small and local:

- no public plugin packaging
- no global user skill install path
- no standalone skill-pack support
- no broad `doctor` rewrite beyond starter inventory coverage

## Requirements Trace

- Skill layout: R1, R2, R3, R12, R13, R14, R15, R16, R17, R20
- Script behavior: R4, R5, R6, R7, R8, R9, R10, R11, R18, R19, R22
- Tests: R21, SC1, SC2, SC3, SC4, SC8
- Artifact quality: SC5, SC6, SC7

## Scope

In this plan:

- Add `template/.agents/skills/hk-spec/SKILL.md`.
- Add `template/.agents/skills/hk-spec/agents/openai.yaml`.
- Add executable `template/.agents/skills/hk-spec/scripts/new-spec-item`.
- Ensure starter inventory installs/adopts the new skill files.
- Add `tests/test_hk_spec_skill.py`.
- Extend `tests/test_starter_scripts.py` only for template inventory coverage.

Not in this plan:

- `hk-plan`, `hk-verify`, or `hk-review`.
- Codex runtime invocation tests.
- Plugin packaging.
- Claude Code adapter.
- `doctor --fix` or full repository repair.

## Context

Research closed the four planning questions:

- Spec Kit keeps repo-level templates under `.specify/templates/` and has skills/commands instantiate them rather than duplicating templates inside each skill.
- OpenAI Codex and Agent Skills guidance put trigger responsibility on `name` and `description`, so `hk-spec` must have a narrow description and body-level compatibility guard.
- Existing harness-kit starter scripts already use lower-case structured JSON with `dry_run`, `safe_to_apply`, `actions`, and explicit conflicts.
- `doctor` patterns in harness-kit, Spec Kit, npm, Flutter, and Homebrew treat health checks as diagnostic commands, separate from create/scaffold commands.

## Decisions

### JSON Contract

`new-spec-item --json` returns one stdout JSON object.
Diagnostics go to stderr.

Successful creation:

```json
{
  "schema_version": 1,
  "command": "new-spec-item",
  "status": "created",
  "dry_run": false,
  "safe_to_apply": true,
  "repo_root": "/repo",
  "spec": {
    "spec_id": "20260501-1530-example-title",
    "title": "Example title",
    "slug": "example-title",
    "created_at": "2026-05-01 15:30",
    "timezone": "Asia/Seoul",
    "spec_dir": "/repo/specs/20260501-1530-example-title",
    "files": {
      "spec": "/repo/specs/20260501-1530-example-title/spec.md",
      "plan": "/repo/specs/20260501-1530-example-title/plan.md",
      "verification": "/repo/specs/20260501-1530-example-title/verification.md",
      "review": "/repo/specs/20260501-1530-example-title/review.md"
    }
  },
  "created_paths": [
    "specs/20260501-1530-example-title/spec.md",
    "specs/20260501-1530-example-title/plan.md",
    "specs/20260501-1530-example-title/verification.md",
    "specs/20260501-1530-example-title/review.md"
  ],
  "planned_paths": [],
  "actions": [
    {
      "path": "specs/20260501-1530-example-title/spec.md",
      "action": "create",
      "applied": true,
      "source": "repo-template"
    }
  ],
  "conflicts": [],
  "error": null,
  "next_action": "write_spec"
}
```

Dry-run keeps the same envelope with `status: planned`, `dry_run: true`, `created_paths: []`, intended writes in `planned_paths`, and `actions[].applied: false`.

Conflict keeps the same envelope with `status: conflict`, `safe_to_apply: false`, no writes, populated `conflicts`, a machine-readable `error.code`, and exit code `1`.

### Skill Wording

`SKILL.md` frontmatter:

```yaml
---
name: hk-spec
description: "Use when starting or creating a new harness-kit spec item from a feature idea, bug, research task, or workflow change. Scaffolds specs/<YYYYMMDD-HHMM-short-slug>/ with spec.md, plan.md, verification.md, and review.md, then authors the spec-stage problem, scope, requirements, success criteria, assumptions, and planning handoff. Do not use for implementation planning, code execution, verification, review, or editing an existing spec item."
---
```

The body must include:

- when to use
- when not to use
- compatibility: requires harness-kit starter structure and `specs/_templates/`
- workflow: run `scripts/new-spec-item` first, then author generated `spec.md`
- spec authoring rules
- completion: report created spec path and recommend `hk-plan`

### Validation Boundary

`new-spec-item` checks only what it needs to create safely:

- title is present
- slug is valid or generated safely
- timezone is valid
- root resolves to a repository directory
- artifact root resolves to `specs` unless configured later
- required repo templates exist and are readable
- target spec directory and lifecycle files do not already exist
- generated `spec.md` contains required frontmatter fields

`doctor` owns broader repository health checks and should not be duplicated inside `new-spec-item`.

## Implementation Units

1. Starter Inventory

Update starter required files to include:

- `template/.agents/skills/hk-spec/SKILL.md`
- `template/.agents/skills/hk-spec/scripts/new-spec-item`
- `template/.agents/skills/hk-spec/agents/openai.yaml`

2. Skill Body

Create `SKILL.md` with the closed frontmatter and a concise body.
Keep examples out unless needed on every run.
Point deterministic work to `scripts/new-spec-item`.
Point lifecycle source templates to `specs/_templates/`.

3. Script

Implement `new-spec-item` in Python 3 stdlib.
Use argparse for the command interface.
Use `zoneinfo` for timezone handling.
Generate `YYYYMMDD-HHMM-short-slug`.
Read `specs/_templates/{spec,plan,verification,review}.md`.
Write all four lifecycle files on normal run.
On dry-run, compute and report without writing.
On conflict, fail before writing anything.

4. Template Rendering

For `spec.md`, replace template placeholders with generated values:

- `<YYYYMMDD-HHMM-short-slug>`
- `<Title>`
- `<YYYY-MM-DD HH:MM>`
- `<Timezone>`
- `status: draft` to `status: active`

Later lifecycle files should be copied from repo templates without authored content changes unless the template has the same mechanical placeholders.

5. Tests

Add `tests/test_hk_spec_skill.py` with coverage for:

- template skill files exist
- frontmatter has `name: hk-spec` and narrow description
- skill body references script-first workflow and `specs/_templates/`
- `new-spec-item --help`
- dry-run JSON creates no files
- normal run creates all four lifecycle files
- generated `spec.md` frontmatter contains required fields
- repo templates are actually used
- conflict exits non-zero and does not overwrite
- missing templates fail cleanly

Extend `tests/test_starter_scripts.py` only to prove bootstrap/adopt include the new skill files.

## Verification

Run:

```bash
pytest tests/test_hk_spec_skill.py tests/test_starter_scripts.py
```

If the full suite is reasonably fast, also run:

```bash
pytest
```

Manual smoke check:

```bash
rm -rf /tmp/hk-smoke
cp -R template /tmp/hk-smoke
template/.agents/skills/hk-spec/scripts/new-spec-item --root /tmp/hk-smoke --slug sample-feature --timezone Asia/Seoul --dry-run --json -- "Sample Feature"
```

Expected:

- stdout is one JSON object
- dry-run writes nothing
- `safe_to_apply` is true for a clean target
- lifecycle paths are all present

## Risks

- Timestamp-dependent tests can become flaky if they assert exact IDs. Tests should assert format unless the script gets an explicit test-only clock input later.
- Template rendering can become too clever. Keep it limited to known starter placeholders.
- Missing-template fallback would blur the project-bound decision. For Phase 1, fail cleanly when required repo templates are missing.
- Broad validation inside `new-spec-item` would duplicate `doctor`; keep the boundary narrow.

## Implementation Handoff

Status: Implemented; ready for review
Spec path: specs/20260430-0200-hk-spec-skill-contract/spec.md
Plan path: specs/20260430-0200-hk-spec-skill-contract/plan.md
Open questions: none
Primary files:

- `template/.agents/skills/hk-spec/SKILL.md`
- `template/.agents/skills/hk-spec/agents/openai.yaml`
- `template/.agents/skills/hk-spec/scripts/new-spec-item`
- `scripts/harness-kit/_lib/starter.py`
- `tests/test_hk_spec_skill.py`
- `tests/test_starter_scripts.py`

Implemented files:

- `template/.agents/skills/hk-spec/SKILL.md`
- `template/.agents/skills/hk-spec/agents/openai.yaml`
- `template/.agents/skills/hk-spec/scripts/new-spec-item`
- `scripts/harness-kit/_lib/starter.py`
- `tests/test_hk_spec_skill.py`
- `tests/test_starter_scripts.py`

Recommended next action: review the implementation against this plan.
