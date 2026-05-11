---
spec_id: 20260429-0045-repo-local-starter-contract
title: Repo Local Starter Contract
status: completed
stage: review
created_at: 2026-04-29 00:45
timezone: Asia/Seoul
---

# Repo Local Starter Contract

## Problem

`harness-kit` needs a concrete downstream repository starter shape before implementation begins.
Without that shape, bootstrap, adoption, workflow skills, and doctor behavior remain abstract decisions rather than an installable contract.

The starter must make a repository legible to both humans and agents without turning `harness-kit` into a runtime platform.

## Why Now

The Phase 1 foundation decisions have settled the core repository model:

- `AGENTS.md` is the thin agent entrypoint.
- `harness-kit.yaml` is the repo-local structured contract.
- workflow artifacts live under `specs/<id>/`.
- durable learnings start as `memory/learnings.md`.
- starter operations are scripts-first and non-destructive.

The next implementation step should not proceed until this starter contract is captured as a spec item.

## Requirements

- `R1`: The starter MUST install or define a thin root `AGENTS.md` that routes agents to the local working contract without becoming a full project manual.
- `R2`: The starter MUST install `harness-kit.yaml` as the authoritative repo-local structured configuration contract.
- `R3`: The starter MUST provide `docs/roadmap/README.md` as the initial home for product or project direction.
- `R4`: The starter MUST create `specs/` as the workflow artifact root.
- `R5`: The starter MUST include `specs/_templates/spec.md`, `plan.md`, `verification.md`, and `review.md`.
- `R6`: The starter MUST provide `memory/learnings.md` as the initial durable learning surface.
- `R7`: The starter MUST reserve `scripts/harness-kit/bootstrap`, `adopt`, and `doctor` as the starter operation surface.
- `R8`: `bootstrap` and `adopt` MUST be non-destructive by default and MUST preserve existing user-authored files.
- `R9`: The starter MUST support agent-readable script behavior through bounded output, meaningful exit codes, and JSON mode where useful.
- `R10`: The starter MUST NOT install broad runtime infrastructure, host-specific config, hooks, databases, dashboards, or task databases in Phase 1.

## Success Criteria

- `SC1`: A fresh target repository can receive the starter structure without relying on chat memory.
- `SC2`: An existing target repository can be inspected for adoption without overwriting `README.md`, `AGENTS.md`, existing docs, specs, or memory.
- `SC3`: A coding agent can determine where instructions, config, active workflow artifacts, and learnings live from repository files alone.
- `SC4`: The starter structure is sufficient for the later `hk-spec`, `hk-plan`, `hk-verify`, and `hk-review` skills to operate against visible files.
- `SC5`: The starter remains clearly separate from a runtime platform or packaged public CLI.

## Scope

In scope:

- downstream starter file and directory shape
- required, recommended, and reserved starter artifacts
- bootstrap/adopt/doctor starter responsibilities
- non-destructive adoption behavior
- script-first entrypoint expectations
- minimal repo-local config shape
- starter relationship to workflow artifacts and skills

Out of scope:

- packaged CLI distribution
- global user configuration
- automatic Markdown merge
- broad `--force`
- host-specific runtime integration
- Codex plugin packaging
- implementation of the workflow skills themselves
- task database or dashboard behavior

## Constraints

- Root `AGENTS.md` must stay thin and routing-oriented.
- `harness-kit.yaml` must remain repo-local and must not contain secrets, personal preferences, generated state, or host-specific runtime settings.
- `specs/` is the workflow artifact root.
- Individual work items use `specs/<YYYYMMDD-HHMM-short-slug>/`.
- `bootstrap` and `adopt` must support dry-run style conflict reporting before destructive behavior is ever considered.
- Any future force or merge behavior must be explicit, scoped, and separately tested.
- `doctor` is a read-only starter contract validator, not a test runner or runtime readiness checker.

## Assumptions

- `A1`: Phase 1 users can tolerate a scripts-first interface before a packaged CLI exists.
- `A2`: A single `memory/learnings.md` file is enough for the initial compounding surface.
- `A3`: Downstream repositories should not receive copied `hk-*` workflow skills by default.
- `A4`: Exact starter wording can evolve after real adoption, as long as the structural contract remains stable.

## Open Questions

### Resolve Before Planning

None.

### Deferred to hk-plan

- `Q1`: Exact file contents for the initial starter templates.
- `Q2`: Exact JSON response shape for `bootstrap`, `adopt`, and `doctor`.
- `Q3`: Test fixture layout for validating new-repo bootstrap and existing-repo adoption.

## Planning Handoff

Status: Ready for hk-plan
Spec path: specs/20260429-0045-repo-local-starter-contract/spec.md
Open questions: none blocking planning
Key assumptions: A1, A2, A3, A4
Requirement index: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10
Recommended next action: hk-plan
