---
spec_id: 20260430-0200-wr-spec-skill-contract
title: wr-spec Skill Contract
status: active
stage: spec
created_at: 2026-04-30 02:00
timezone: Asia/Seoul
---

# wr-spec Skill Contract

## Problem

`wayrail` has a repo-local starter contract, but it does not yet have the first workflow skill that starts a new spec item in a repeatable way.

Without `wr-spec`, humans and agents must manually create `specs/<YYYYMMDD-HHMM-short-slug>/`, copy lifecycle files, remember frontmatter fields, and decide how much of `spec.md` should be generated versus authored. That leaves the most important entry point of the workflow dependent on chat memory.

## Why Now

The previous starter contract closed the downstream repository shape:

- workflow artifacts live under `specs/`
- each work cycle uses a timestamped spec item directory
- every spec item contains `spec.md`, `plan.md`, `verification.md`, and `review.md`
- only `spec.md` receives meaningful authored content at the spec stage
- later files start as stubs owned by their later skills

The next natural product step is to make the first workflow skill concrete.

## Research Basis

### Local Comparison Findings

`oh-my-codex` keeps skills as direct source folders under `skills/<name>/SKILL.md`.
Its skill-management skill scans user and project scopes, parses frontmatter, and creates/edit/search/remove workflows around skill directories. The useful lesson is that direct skill folders are easy to author and inspect, but the older `.codex/skills` path and extra fields such as `triggers` do not fully match the current Codex skill documentation.

`compound-engineering-plugin` treats skills as plugin source. It stores skills under `plugins/compound-engineering/skills/<name>/SKILL.md`, separates agents under `agents/`, and uses an installer/converter for Codex and other hosts. Its README says Codex installs generated plugin skills under `~/.codex/skills/<plugin>/` and warns not to double-register skills through overlapping install paths. The useful lesson is to separate canonical skill source from installed copies.

`gstack` keeps many command-like skills as top-level folders with `SKILL.md`, validates skill references in tests, and uses host adapters/scripts to convert or discover skills. Its discovery code scans root plus one level of subdirectories for `SKILL.md` and templates. The useful lesson is that skills should be testable artifacts, not just prose.

### Official Skill Findings

OpenAI Codex documentation defines skills as the authoring format for reusable workflows and plugins as the installable distribution unit. A skill directory contains required `SKILL.md` and optional `scripts/`, `references/`, `assets/`, and `agents/openai.yaml`.

Codex uses progressive disclosure: it initially sees each skill's name, description, and path, and loads the full `SKILL.md` only when the skill is selected. Therefore the `description` field carries most of the trigger burden and must be concise, explicit, and scoped.

The Agent Skills specification requires `SKILL.md` YAML frontmatter with `name` and `description`. The `name` must be lowercase, hyphenated, and match the parent directory. It also recommends focused `references/`, static `assets/`, executable `scripts/`, and keeping `SKILL.md` under roughly 500 lines.

The Agent Skills best-practices guide emphasizes:

- start from real project expertise, not generic LLM-generated workflow text
- spend context only on what the agent would otherwise get wrong
- design one coherent skill per unit of work
- provide defaults rather than menus
- use scripts when deterministic, repeatable, or stateful behavior matters
- design scripts for agents with non-interactive flags, `--help`, helpful errors, structured output, dry-run support, idempotency, and meaningful exit codes

## Recommended Direction

`wr-spec` should be a Codex-first Agent Skill installed by the starter template under the downstream repository's repo-local skill discovery path:

```text
template/
  .agents/
    skills/
      wr-spec/
        SKILL.md
        scripts/
          new-spec-item
        agents/
          openai.yaml
```

When this template is applied to a target repository, the target repository receives:

```text
.agents/skills/wr-spec/
```

This matches Codex's current repo-local skill discovery path.

Decision: Phase 1 starter includes `wr-spec` at `template/.agents/skills/wr-spec/`.
Without this, `wr-spec` would depend on global user state, an external CLI, plugin packaging, or docs-only manual behavior. Those alternatives weaken the repo-local starter goal because a target repository would no longer contain the workflow skill needed to start its own spec cycle.

Decision: `new-spec-item` lives inside `template/.agents/skills/wr-spec/scripts/`.
This script is the deterministic execution tool of the `wr-spec` skill itself, not a starter-wide command. Shared scripts remain reserved for starter-level commands such as `bootstrap`, `adopt`, and `doctor`, or for logic reused by multiple skills. If later `wr-plan`, `wr-verify`, or `wr-review` need the same implementation logic, it can be extracted after that duplication exists.

Decision: `wr-spec` is a project-bound `wayrail` skill, not a standalone skill pack.
Lifecycle file templates remain under `template/specs/_templates/` as repo-level artifact templates. The `wr-spec` skill owns the workflow instructions and `new-spec-item` command that instantiate those templates, but it does not duplicate the lifecycle templates under skill `assets/`.
This follows the Spec Kit pattern: repo-local templates live under `.specify/templates/`, while repo-local skills under `.agents/skills/speckit-*` invoke those templates and require the project structure to exist.

Decision: `new-spec-item --json` uses a stable lower-case wayrail envelope rather than Spec Kit's minimal uppercase field set.
The envelope extends existing starter script conventions with `schema_version`, `command`, `status`, `dry_run`, `safe_to_apply`, `repo_root`, `actions`, `conflicts`, and `error`.
It also includes a `spec` object with `spec_id`, `title`, `slug`, `created_at`, `timezone`, `spec_dir`, and the four lifecycle file paths.
Dry-run output keeps the same shape and moves intended writes to `planned_paths`; successful writes use `created_paths`; conflicts return `status: conflict`, `safe_to_apply: false`, no writes, a populated `conflicts` array, and a machine-readable `error.code`.

Decision: `SKILL.md` uses a narrow trigger.
The description should trigger only when starting or creating a new wayrail spec item from a feature idea, bug, research task, or workflow change.
It must explicitly avoid planning, implementation, verification, review, and editing an existing spec item.
The project-bound compatibility requirement belongs in the body so the trigger description stays focused.

Decision: tests for `wr-spec` get a dedicated file.
`tests/test_wr_spec_skill.py` owns skill layout, frontmatter, script behavior, dry-run JSON, lifecycle creation, repo-template use, conflict safety, and missing-template failures.
`tests/test_starter_scripts.py` should only be extended enough to prove starter install/adopt includes the new skill files.

Decision: validation is split by responsibility.
`new-spec-item` validates only creation-time preconditions needed to write safely: invocation, title, slug, timezone, root resolution, target collision, unsafe paths, required repo templates, and generated `spec.md` frontmatter fields.
`doctor` owns whole-repository validation: starter files, lifecycle templates, existing spec items, existing frontmatter shape, and wayrail config health.

The skill should not ask an agent to hand-roll the directory structure. The skill should instruct the agent to run `scripts/new-spec-item` first, then author `spec.md` from the current conversation and repository context.

The script should own deterministic scaffolding:

- generate `specs/<YYYYMMDD-HHMM-short-slug>/`
- create `spec.md`, `plan.md`, `verification.md`, and `review.md`
- write frontmatter and base sections into `spec.md`
- write minimal stubs into later lifecycle files
- support dry-run and JSON output
- fail safely on conflicts rather than overwriting

The agent should own judgment:

- identify the problem frame
- extract requirements and success criteria
- separate scope from non-goals
- record assumptions
- classify blocking versus deferred questions
- ask the human only when a decision is genuinely product- or preference-dependent

## Requirements

- `R1`: `wr-spec` MUST be present in the starter template at `template/.agents/skills/wr-spec/`.
- `R2`: `template/.agents/skills/wr-spec/SKILL.md` MUST use Agent Skills-compatible frontmatter with `name: wr-spec` and a description that clearly triggers on creating or starting a new wayrail spec item.
- `R3`: `wr-spec` MUST include a deterministic scaffolding script at `template/.agents/skills/wr-spec/scripts/new-spec-item`.
- `R4`: The script MUST support `--json`, `--dry-run`, `--slug SLUG`, `--root PATH`, `--timezone TZ`, and `-- TITLE`.
- `R5`: The script MUST create a full lifecycle directory containing `spec.md`, `plan.md`, `verification.md`, and `review.md`.
- `R6`: `new-spec-item` MUST use the target repository's `specs/_templates/` files as the canonical source templates for generated lifecycle files.
- `R7`: Generated `spec.md` frontmatter MUST include `spec_id`, `title`, `status`, `stage`, `created_at`, and `timezone`.
- `R8`: Newly generated spec items SHOULD default to `status: active` and `stage: spec`.
- `R9`: The script MUST be non-interactive and safe for agents to run in a shell.
- `R10`: The script MUST not overwrite an existing spec item or existing lifecycle file unless a separately specified future force mode exists.
- `R11`: The script MUST return structured output in JSON mode with enough information for an agent to report the created path and next action.
- `R12`: `SKILL.md` MUST tell the agent to run the script before writing the spec content.
- `R13`: `SKILL.md` MUST tell the agent to fill `spec.md` after scaffolding, using current context and repository files.
- `R14`: `SKILL.md` MUST keep detailed examples or templates out of the main body unless they are essential on every run.
- `R15`: Phase 1 MUST install `wr-spec` into downstream repositories through the starter template, not through a global user skill path.
- `R16`: Phase 1 MUST NOT package `wr-spec` as a public plugin.
- `R17`: `wr-spec` MUST declare that it requires a `wayrail` project structure with `specs/_templates/`.
- `R18`: `new-spec-item --json` MUST use a stable top-level envelope with `schema_version`, `command`, `status`, `dry_run`, `safe_to_apply`, `repo_root`, `spec`, `created_paths`, `planned_paths`, `actions`, `conflicts`, `error`, and `next_action`.
- `R19`: `new-spec-item` exit codes MUST be `0` for success or safe dry-run, `1` for expected user-correctable creation blockers, and `2` for invalid invocation, unreadable configuration, or internal errors.
- `R20`: `SKILL.md` MUST use a narrow description equivalent to: "Use when starting or creating a new wayrail spec item from a feature idea, bug, research task, or workflow change. Scaffolds specs/<YYYYMMDD-HHMM-short-slug>/ with spec.md, plan.md, verification.md, and review.md, then authors the spec-stage problem, scope, requirements, success criteria, assumptions, and planning handoff. Do not use for implementation planning, code execution, verification, review, or editing an existing spec item."
- `R21`: The implementation MUST add dedicated `wr-spec` behavior tests in `tests/test_wr_spec_skill.py` and update starter inventory tests only for installation coverage.
- `R22`: `new-spec-item` MUST NOT perform whole-repository health validation; that responsibility remains with `doctor`.

## Success Criteria

- `SC1`: A user or agent can start a new spec item by invoking `wr-spec` without remembering the directory naming convention.
- `SC2`: `--dry-run --json` reports the intended spec item path and actions without writing files.
- `SC3`: A normal run creates the full lifecycle directory with valid files.
- `SC4`: Re-running with the same slug or computed spec id fails safely with a clear conflict message.
- `SC5`: The generated `spec.md` is immediately usable as a spec-stage artifact.
- `SC6`: The later lifecycle stubs make the workflow visible without implying that plan, verification, or review has happened.
- `SC7`: The skill body stays concise enough for progressive disclosure and routes optional detail to bundled assets or scripts.
- `SC8`: The implementation can be tested without requiring Codex itself to run the skill.

## Scope

In scope:

- starter-template `wr-spec` skill layout
- `SKILL.md` trigger and workflow instructions
- deterministic spec item scaffolding script
- generated `spec.md` shape
- use of `specs/_templates/` as the lifecycle template source
- script contract and tests
- decision handoff from spec stage to plan stage

Out of scope:

- `wr-plan`, `wr-verify`, and `wr-review` implementation
- public plugin packaging
- global user installation
- Claude Code `.claude/skills/wr-spec/` adapter
- broad `--force`
- automatic Markdown merge
- runtime databases, dashboards, hooks, or long-running daemons

## Constraints

- The skill must follow the already-decided `specs/<YYYYMMDD-HHMM-short-slug>/` artifact model.
- The implementation should prefer Python 3 stdlib for the scaffolding script unless planning finds a stronger reason not to.
- The skill should stay Codex-first while avoiding avoidable lock-in to a private runtime.
- The skill should use scripts for deterministic file creation and prose instructions for judgment-heavy spec authoring.
- The generated artifact must remain readable and editable by humans.

## Assumptions

- `A1`: `template/.agents/skills/wr-spec/` is the canonical Phase 1 repo-local installation source.
- `A2`: `agents/openai.yaml` is useful enough to include in the canonical skill source, but it can stay minimal.
- `A3`: `template/specs/_templates/` is the canonical source of lifecycle file templates.
- `A4`: The first implementation can validate script behavior with normal repository tests without requiring a full Codex skill invocation test.

## Open Questions

### Resolve Before Planning

None.

### Deferred to wr-plan

None.

## Closed Planning Decisions

- `Q4`: JSON schema is closed as the stable lower-case envelope described in `R18`; success uses `status: created`, dry-run uses `status: planned`, and conflicts use `status: conflict`.
- `Q5`: `SKILL.md` trigger wording is closed as the narrow `R20` description, with compatibility documented in the body rather than frontmatter.
- `Q6`: Test layout is closed as dedicated `tests/test_wr_spec_skill.py` behavior tests plus minimal starter inventory updates in `tests/test_starter_scripts.py`.
- `Q7`: Validation boundary is closed: `new-spec-item` handles creation-time preflight and generated output sanity; `doctor` handles whole-repository health.

## Planning Handoff

Status: Ready for wr-plan
Spec path: specs/20260430-0200-wr-spec-skill-contract/spec.md
Open questions: none blocking planning
Requirement index: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22
Recommended next action: wr-plan

## Sources

- Local: `/tmp@retn0/wayrail-research/oh-my-codex/skills/skill/SKILL.md`
- Local: `/tmp@retn0/wayrail-research/oh-my-codex/skills/plan/SKILL.md`
- Local: `/tmp@retn0/wayrail-research/compound-engineering-plugin/README.md`
- Local: `/tmp@retn0/wayrail-research/compound-engineering-plugin/plugins/compound-engineering/skills/ce-plan/SKILL.md`
- Local: `/tmp@retn0/wayrail-research/compound-engineering-plugin/plugins/compound-engineering/skills/ce-work/SKILL.md`
- Local: `/tmp@retn0/wayrail-research/gstack/docs/skills.md`
- Local: `/tmp@retn0/wayrail-research/gstack/scripts/discover-skills.ts`
- Local: `/tmp@retn0/wayrail-research/gstack/test/skill-validation.test.ts`
- Web: https://developers.openai.com/codex/skills
- Web: https://agentskills.io/specification
- Web: https://agentskills.io/skill-creation/best-practices
- Web: https://agentskills.io/skill-creation/optimizing-descriptions
- Web: https://agentskills.io/skill-creation/using-scripts
- Local: `/tmp@retn0/wayrail-extra/spec-kit/scripts/bash/create-new-feature.sh`
- Local: `/tmp@retn0/wayrail-extra/spec-kit/tests/integrations/test_integration_base_skills.py`
- Local: `/tmp@retn0/wayrail-extra/spec-kit/tests/integrations/test_integration_codex.py`
- Web: https://cli.github.com/manual/gh_help_formatting
- Web: https://developer.hashicorp.com/terraform/internals/machine-readable-ui
- Web: https://docs.npmjs.com/cli/v10/commands/npm-doctor/
- Web: https://docs.flutter.dev/reference/flutter-cli
