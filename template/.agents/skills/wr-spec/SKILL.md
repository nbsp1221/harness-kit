---
name: wr-spec
description: "Use when starting or creating a new wayrail spec item from a feature idea, bug, research task, or workflow change. Scaffolds specs/<YYYYMMDD-HHMM-short-slug>/ with spec.md, plan.md, verification.md, and review.md, then authors the spec-stage problem, scope, requirements, success criteria, assumptions, and planning handoff. Do not use for implementation planning, code execution, verification, review, or editing an existing spec item."
---

# wr-spec

Start a new wayrail spec item.

## Use When

- The user asks to start, create, scaffold, open, or draft a new spec.
- The input is a feature idea, bug, research task, workflow change, or unclear work item that needs spec-stage framing.
- The user directly invokes `$wr-spec`.

## Do Not Use When

- The user asks to plan implementation; use the plan stage instead.
- The user asks to implement code.
- The user asks to verify, review, or complete later lifecycle stages.
- The user asks to edit an existing spec item unless they explicitly want a new spec item.

## Compatibility

This is a repo-local wayrail skill. Use it only in repositories that contain the wayrail starter structure, including `specs/_templates/`. If that structure is missing, stop and report that the project has not been initialized for wayrail instead of inventing files by hand.

## Workflow

1. Determine a clear spec title and a short lower-case slug from the user request.
2. Run `scripts/new-spec-item` before writing prose.
3. Prefer `--json`; pass `--slug`, `--root`, and `--timezone` when the values are known.
4. Read the JSON output and open the generated `spec.md`.
5. Fill only `spec.md` with spec-stage content.
6. Leave `plan.md`, `verification.md`, and `review.md` as stubs for later lifecycle stages.

## Spec Authoring Rules

- Capture the problem, why now, scope, non-goals, requirements, success criteria, assumptions, and planning handoff.
- Make reasonable defaults explicit.
- Ask the user only for decisions that materially change scope, product behavior, or success criteria.
- Classify open questions as blocking before planning or deferred to planning.
- Do not include implementation plans, code changes, test commands, or review conclusions.

## Completion

Report the created spec path and recommend the plan stage as the next action.
