# Agent Guide

This file is the repository entrypoint for agents. Keep it short: it is a map to the working contract, not the full contract.

## Source Of Truth

Use repository files over chat memory when they conflict.

- Active work lives in `specs/<id>/`.
- Each non-trivial work item should use:
  - `spec.md` - problem, scope, success criteria, non-goals
  - `plan.md` - implementation approach, affected files, risks, checks
  - `verification.md` - commands run, results, gaps
  - `review.md` - independent review findings and outcome
- Long-lived project docs live in `docs/` or the repository's existing documentation structure.
- Directory-specific rules belong in the nearest nested `AGENTS.md`.
- Temporary or branch-local overrides may live in `AGENTS.override.md` only when this repository explicitly uses that convention.

## Workflow

For non-trivial changes, follow:

`spec -> plan -> implement -> verify -> review`

Use harness skills when available:

- `wr-spec` to create or update `specs/<id>/spec.md`
- `wr-plan` to create or update `specs/<id>/plan.md`
- `wr-verify` to create or update `specs/<id>/verification.md`
- `wr-review` to create or update `specs/<id>/review.md`

If the human explicitly skips `spec` or `plan`, record that override in the relevant artifact.
Do not silently skip verification or review before a completion claim.

## Working Rules

- Preserve existing user work and repository instructions.
- Keep changes scoped to the requested work and the approved plan.
- Prefer existing project patterns over new abstractions.
- Do not add dependencies, broad rewrites, or new workflows unless the plan calls for them.
- Ask before destructive actions, production actions, credential use, or materially changing scope.
- When touching a subdirectory with its own `AGENTS.md`, follow that file in addition to this one.

## Verification And Completion

- Define verification in `plan.md` or `verification.md` before claiming completion.
- Run the most direct relevant checks: tests, lint, typecheck, build, smoke test, or documented project-specific commands.
- Record commands and outcomes in `specs/<id>/verification.md`.
- If a check cannot be run, record why and what risk remains.
- Do not call work complete until verification and review are done, or clearly report it as unverified or unreviewed.

## Repo Map

Update these links after adoption:

- Project overview: `README.md`
- Architecture or design docs: `docs/`
- Active specs: `specs/`
- Local agent guidance: nested `AGENTS.md` files
