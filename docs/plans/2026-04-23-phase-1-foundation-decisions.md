---
status: draft
phase: "Phase 1: Starter Foundation"
last_reviewed: 2026-04-27
owner: repository maintainer
---

# Phase 1 Foundation Decisions

This document records the major design decisions already agreed during `harness-kit` Phase 1 discussions.

It exists so these decisions do not remain trapped in one session.
It is a decision record for current direction, not a final implementation plan.

Detailed implementation can be designed later.
For now, this document captures what has already been decided strongly enough to guide later work.

## Purpose

The purpose of this record is to freeze the current answers to these questions:

- what `harness-kit` is trying to be
- what it is explicitly not trying to be
- what must be designed before installation work begins
- what the minimum workflow should be
- how repository artifacts should be organized
- how the `harness-kit` repository itself should be separated from downstream installed assets

## Product Direction

### Decision: `harness-kit` is a repo-local starter and contract system

`harness-kit` is not being designed as:

- a full agent runtime platform
- a dashboard or control plane
- a pure skill pack
- a large multi-agent orchestration shell

It is being designed as:

- a repo-local starter
- a local contract system
- a standard working model installer
- a lightweight verification and compounding scaffold

The product goal is to let one operator run multiple agent-first repositories with the same working contract, instead of rebuilding the harness from scratch every time.

### Decision: internal-first, public-readable

The repository is public, but internal repeated use is the planning authority.

That means:

- internal usability comes first
- public readability still matters
- public adoption is welcome
- public packaging is not the immediate optimization target

## Phase Direction

### Decision: roadmap remains phase-based

The roadmap should stay phase-based rather than date-based.

Current canonical roadmap:

- [Harness Kit Roadmap](../roadmap/README.md)

### Decision: Phase 1 must define the working layer before the installation layer

Installation is a delivery mechanism.
The working layer is what gets delivered.

Therefore Phase 1 should not jump directly into `bootstrap` or `adopt` implementation.
It must first define the minimum operating model that a repository should follow once the harness exists.

This means the order for Phase 1 is:

1. define the minimum working model
2. map that model to repository artifacts and paths
3. design the installation surface that creates those artifacts

## Core Workflow Direction

### Decision: the initial core workflow is `spec -> plan -> implement -> verify -> review`

This is the current recommended minimum workflow for `harness-kit`.

It reflects the shared pressure observed in benchmark projects:

- visible problem framing before code
- written planning before execution
- explicit verification before completion
- independent review with fresh context

### Why this workflow was chosen

`spec`
- captures the problem, success criteria, and non-goals
- protects the work from drifting immediately into solution bias

`plan`
- turns the problem into an executable approach
- creates a handoff surface between design and implementation

`implement`
- executes the approved plan
- keeps implementation separate from hidden requirement rewriting

`verify`
- requires explicit checks such as tests, lint, build, or other validation commands
- prevents completion from being based on self-report alone

`review`
- introduces a fresh-context judgment step
- is considered one of the strongest harness differentiators
- should not collapse into self-review by the same execution context

### Decision: use soft process gates with hard completion gates

The initial gate model is:

- `spec`: created by default, unless the human explicitly says to skip it
- `plan`: created by default, unless the human explicitly says to skip it
- `implement`: proceeds from the plan or from a recorded human override
- `verification`: required before any completion claim
- `review`: required before any completion claim

This keeps the workflow lightweight enough for real use while still preventing the weakest agent failure mode: claiming completion without evidence and fresh-context review.

If the human explicitly skips `spec` or `plan`, the override must be recorded in the spec item metadata or in the relevant artifact.

If verification or review is not done, the agent may report an unverified or unreviewed result, but it must not call the work complete.

### Decision: `review` is core earlier than `compound`

`review` should be treated as part of the initial core workflow.

`compound` remains important, but it can begin as a lightweight supported layer instead of a fully enforced core stage.

Reason:

- the main immediate risk in agent work is same-context overconfidence
- independent review addresses this earlier and more directly than elaborate compounding systems

## Working Model Direction

### Decision: the minimum working model is defined by six contract axes

The current working model should be understood through these six axes:

1. `stage model`
2. `artifact model`
3. `verification model`
4. `memory model`
5. `authority model`
6. `escalation model`

Current draft:

- [2026-04-22 Minimum Working Model Design](./2026-04-22-minimum-working-model-design.md)

### Decision: `AGENTS.md` must remain thin

`AGENTS.md` should be a thin entrypoint, not the whole operating constitution.

This follows OpenAI's Harness Engineering guidance: treat `AGENTS.md` as a table of contents, not an encyclopedia. The repository knowledge base should live in structured repo-local documents, while `AGENTS.md` gives the agent a small stable map to those documents.

It should tell an agent:

- which workflow exists
- where the relevant artifacts live
- where verification expectations live
- where durable learnings live
- when escalation is required

It should not become:

- the full workflow specification
- the full review standard
- the full memory store
- a prompt dump

Target size:

- keep the downstream starter `AGENTS.md` roughly under 100 lines
- prefer links and pointers over duplicated rules
- split specialized guidance into nested `AGENTS.md` or `AGENTS.override.md` files only when a subdirectory genuinely needs local rules

Required starter behavior:

- root `AGENTS.md` is installed as the visible agent entrypoint
- existing `AGENTS.md` files in adopted repositories are preserved by default
- adoption should report that the harness entrypoint needs manual or explicit merge integration when `AGENTS.md` already exists
- long-lived policy details belong in structured docs, not in the root instruction file

## Artifact and Documentation Direction

### Decision: workflow artifacts should be grouped by spec item, not only by document type

The team discussed two models:

1. type-based folders such as `docs/specs/` and `docs/plans/`
2. spec-item folders that group one cycle together

Current direction is the second model for workflow artifacts.

Reason:

- `spec`, `plan`, `verification`, and `review` belong to one cycle
- grouping them together makes a single spec item easier to reconstruct
- this is more legible for both humans and agents

### Decision: use `specs/` for workflow artifact folders

The workflow artifact root should be `specs/`, not `docs/work/`.

Reason:

- `specs/` is a real convention in spec-driven tools such as `spec-kit` and `agent-os`
- `work/` is more generic and has weaker convention behind it
- the folder represents a spec-driven work cycle, not just arbitrary current work

### Decision: use a hybrid documentation structure

Not everything should be grouped by spec item.

The current direction is:

- keep durable top-level documentation by type
- group workflow artifacts by spec item

Recommended high-level shape:

```text
docs/
  roadmap/
  research/
specs/
  <YYYYMMDD-HHMM-short-slug>/
    spec.md
    plan.md
    verification.md
    review.md
memory/
  learnings.md
```

### Implication

This means:

- `roadmap` and `research` remain stable, long-lived document systems
- `spec`, `plan`, `verification`, and `review` become cycle-local artifacts
- `compound` can start as a simple durable file under `memory/`

### Decision: use timestamped spec item directories

Spec item directories should use this format:

```text
specs/<YYYYMMDD-HHMM-short-slug>/
```

Example:

```text
specs/20260427-2015-bootstrap-entrypoint/
```

Reason:

- timestamp prefixes sort naturally in file listings
- minute-level precision avoids collisions when several agent-driven cycles start on the same day
- the slug keeps the directory recognizable without requiring a separate task or issue registry
- this matches the current agent-heavy operating model better than date-only names

The timestamp should use the operator's local project timezone. Store the exact timezone in artifact frontmatter when it matters.

### Decision: use the initial four-file spec item shape

Each spec item should start with this default file shape:

```text
specs/<YYYYMMDD-HHMM-short-slug>/
  spec.md
  plan.md
  verification.md
  review.md
```

File responsibilities:

- `spec.md`: what and why, plus minimal metadata such as `spec_id`, `status`, `stage`, `created_at`, and `timezone`
- `plan.md`: implementation design, affected work units, verification plan, and known risks
- `verification.md`: commands, results, skipped checks, and remaining verification risk
- `review.md`: fresh-context review findings and resolution state

`verification.md` is preferred over `verify.md` because this is a document artifact, not a command name.

### Decision: scaffold the full spec item, but only author `spec.md` during `hk-spec`

`hk-spec` should not rely on the agent to manually create timestamped directories or lifecycle artifact files.
Those mechanics should be handled by a deterministic script shipped with the skill.

The `hk-spec` skill should split responsibilities this way:

- a co-located script creates `specs/<YYYYMMDD-HHMM-short-slug>/`
- the script creates `spec.md`, `plan.md`, `verification.md`, and `review.md`
- the script initializes frontmatter and path-derived values such as `spec_id`, `created_at`, and `timezone`
- the agent writes meaningful content only into `spec.md`
- `plan.md`, `verification.md`, and `review.md` remain minimal stubs until `hk-plan`, `hk-verify`, and `hk-review` run

The stub files should be intentionally thin, for example:

```markdown
# <Title> Plan

Not started. Run hk-plan.
```

This keeps the lifecycle directory complete from the beginning without pretending that later stages have already been performed.
It also keeps path, timestamp, and template creation out of the model's judgment loop.

This matches the useful part of `spec-kit`'s approach: deterministic tooling creates the feature directory and seed files, while the agent performs the semantic requirements work.
Phase 1 should not copy heavier state machinery such as a current-feature registry or checklist system until repeated use shows that the workflow needs it.

### Decision: make the `hk-spec` scaffold script agent-readable and conservative

The scaffold script should have a small, explicit interface.
The skill-facing command can be named `scripts/new-spec-item` inside the `hk-spec` skill; a future CLI wrapper can expose the same behavior under a public command name.

Recommended interface:

```text
new-spec-item [--json] [--dry-run] [--slug SLUG] [--root PATH] [--timezone TZ] -- TITLE
```

Behavior:

- `TITLE` is required and may be a quoted multi-word title or feature description
- `--slug` optionally overrides the generated short slug
- `--root` defaults to the git root when available, then the current directory
- `--timezone` defaults to the operator's local project timezone and writes the resolved value into `spec.md` frontmatter
- `--json` makes stdout a single machine-readable JSON object and sends diagnostics to stderr
- `--dry-run` computes IDs and paths without writing files
- empty input fails with a clear usage error
- an existing target directory fails by default
- no branch is created
- no current-spec state file, registry, lock file, or task database is written
- no `--force` or automatic overwrite mode exists in Phase 1

The `--json` output should include every path later steps need:

```json
{
  "spec_id": "20260428-1342-bootstrap-entrypoint",
  "spec_dir": "/repo/specs/20260428-1342-bootstrap-entrypoint",
  "spec_file": "/repo/specs/20260428-1342-bootstrap-entrypoint/spec.md",
  "plan_file": "/repo/specs/20260428-1342-bootstrap-entrypoint/plan.md",
  "verification_file": "/repo/specs/20260428-1342-bootstrap-entrypoint/verification.md",
  "review_file": "/repo/specs/20260428-1342-bootstrap-entrypoint/review.md",
  "slug": "bootstrap-entrypoint",
  "created_at": "2026-04-28 13:42",
  "timezone": "Asia/Seoul"
}
```

Template resolution should stay simple:

1. repo-local override: `specs/_templates/<name>.md`
2. skill-local template asset
3. built-in fallback stub

This borrows the useful conventions from `spec-kit`'s scaffold scripts, especially required description input, `--json`, `--dry-run`, slug override, and conservative collision handling.
It intentionally avoids `spec-kit`'s branch creation, sequential numbering, persisted current-feature state, and preset or extension template resolver because those are too heavy for `harness-kit` Phase 1.

The preferred implementation target is Python 3 with only the standard library.
That keeps JSON output, path handling, slug normalization, timestamp formatting, and tests portable without maintaining parallel Bash and PowerShell implementations.
If later distribution constraints make Python unavailable, the same contract can be implemented in another runtime without changing the skill behavior.

### Decision: keep `spec.md` focused on problem, scope, and requirements

`spec.md` should define WHAT is being solved and WHY it matters.
It should not contain implementation sequencing, detailed file plans, or validation command transcripts.

Comparable systems show a consistent split:

- `spec-kit` uses a detailed feature specification with user scenarios, functional requirements, edge cases, success criteria, and assumptions
- `compound-engineering` uses a lightweight PRD-style requirements document with problem frame, stable requirement IDs, success criteria, scope boundaries, decisions, assumptions, and outstanding questions
- `agent-os` separates shaping notes from implementation planning and keeps shaping lightweight
- `superpowers` treats the spec/design stage as the place to clarify purpose, constraints, success criteria, and scope before planning

Phase 1 should follow a compact requirements-document shape. User stories or acceptance scenarios are useful for user-facing features, but they should not be mandatory for every spec item.

Recommended minimum `spec.md` body after frontmatter:

```markdown
# <Title>

## Problem

## Why Now

## Requirements

## Success Criteria

## Scope

## Constraints

## Assumptions

## Open Questions
```

Section responsibilities:

- `Problem`: the user, project, or workflow problem being addressed
- `Why Now`: why this work matters in the current project context
- `Requirements`: concrete intended behavior, preferably with stable IDs such as `R1`, `R2`, and `R3` for non-trivial work
- `Success Criteria`: observable outcomes that show the work solved the right problem
- `Scope`: explicit inclusions and non-goals
- `Constraints`: known limits that planning and implementation must respect
- `Assumptions`: defaults being accepted because they are not yet proven or specified
- `Open Questions`: unresolved items, separated where useful into questions that block planning and questions deferred to planning

Implementation details belong in `plan.md` unless the spec item itself is about choosing a product or architecture direction.

### Decision: make `hk-spec` a clarification and readiness gate, not a planning shortcut

`hk-spec` should produce a self-contained spec that a fresh agent can use without chat history.
It should not produce implementation sequencing, file-by-file plans, technical design, or validation command recipes.

Recommended `hk-spec` procedure:

1. Start from a title or short feature description.
2. Run the scaffold script with `--json` and use the returned `spec_file`.
3. Read only enough local context to avoid writing false claims or asking questions already answered by repository docs.
4. Clarify product intent.
5. Write `spec.md`.
6. Run a lightweight readiness check.
7. End with a planning handoff.

Clarification policy:

- ask the human only when the answer materially changes scope, user behavior, success criteria, non-goals, security or privacy posture, acceptable risk, or planning readiness
- ask at most three critical questions during initial spec creation
- ask one question at a time
- prefer a recommended option with short tradeoff notes when choices are clear
- make reasonable assumptions for low-impact defaults and record them
- do not ask about implementation mechanics unless they are explicit product constraints
- do not hide product decisions as technical assumptions

Phase 1 should not introduce a separate `hk-clarify` skill.
If a spec is not ready for planning, unresolved issues stay in `Open Questions` under `Resolve Before Planning`.

Recommended lightweight ID policy:

- `R1`, `R2`, `R3` for requirements
- `SC1`, `SC2`, `SC3` for success criteria when useful
- `A1`, `A2`, `A3` for assumptions when risk needs to be tracked
- `Q1`, `Q2`, `Q3` for open questions

Do not require separate user-story, functional, non-functional, edge-case, and acceptance-scenario ID families in Phase 1.
Those are valid for heavier spec-driven systems, but they add bookkeeping before `harness-kit` has proven that it needs that detail.

Readiness criteria before handoff to `hk-plan`:

- requirements are concrete enough to plan from
- success criteria are measurable or objectively reviewable
- scope and non-goals are explicit
- assumptions are visible
- no `Resolve Before Planning` questions remain
- planning would not need to invent product behavior, scope boundaries, or success criteria
- implementation details have not leaked into the spec except as explicit constraints

The spec should end with a compact handoff block:

```markdown
## Planning Handoff

Status: Ready for hk-plan
Spec path: specs/<YYYYMMDD-HHMM-short-slug>/spec.md
Open questions: none
Key assumptions: A1
Requirement index: R1, R2, R3
Recommended next action: hk-plan
```

If the spec is blocked, `Status` should be `Blocked before hk-plan`, and `Recommended next action` should describe the human decision needed.

### Decision: keep `plan.md` compact and implementation-design oriented

`plan.md` should be the design surface for how a spec item will be implemented.
It should not become a separate status document, a full task database, or a command transcript.

Comparable systems point in different directions:

- `spec-kit` uses a highly structured implementation plan with technical context and project structure
- `superpowers` uses very detailed execution plans with task checkboxes, file lists, commands, and expected output
- `agent-os` keeps a lightweight `plan.md` and splits shaping context into sibling artifacts
- `compound-engineering` treats planning as the HOW document: requirements trace, scope, research, decisions, implementation units, verification, and risks
- `archon` emphasizes affected files, existing patterns, and validation commands before implementation

Phase 1 should follow a compact `compound-engineering`-style subset.

Recommended minimum `plan.md` sections:

```markdown
# <Title> Plan

## Overview

## Requirements Trace

## Scope

## Context

## Decisions

## Implementation Units

## Verification

## Risks
```

Section responsibilities:

- `Overview`: short implementation summary
- `Requirements Trace`: links the plan back to the relevant spec requirements or success criteria
- `Scope`: what is in and out for this implementation pass
- `Context`: relevant files, existing patterns, constraints, and references
- `Decisions`: meaningful technical choices and rationale
- `Implementation Units`: coarse work units with expected files and sequencing
- `Verification`: commands, checks, or manual validation expected before completion
- `Risks`: uncertainty, rollback concerns, or known weak assumptions

`plan.md` should not own lifecycle frontmatter in Phase 1. The single source of truth for spec item `status` and `stage` remains `spec.md` frontmatter.

### Decision: make `hk-plan` a design-and-handoff skill, not a task generator

`hk-plan` should consume `spec.md` and write `plan.md`.
It should not implement code, run verification, or create a separate task database in Phase 1.

Recommended `hk-plan` procedure:

1. Load an explicit spec path or the current spec item path provided by the user or previous handoff.
2. Check `Planning Handoff`.
3. Stop if the spec is not ready for `hk-plan` or if `Resolve Before Planning` questions remain.
4. Read the spec sections that define problem, requirements, success criteria, scope, constraints, assumptions, and open questions.
5. Do bounded repository research before writing:
   - inspect relevant docs and likely target files
   - search for local implementation and test conventions
   - identify existing commands, scripts, or checks likely to verify the work
   - avoid source edits and implementation-time experiments
6. Classify unknowns:
   - product, scope, behavior, quality bar, security, privacy, or risk tolerance questions require human judgment
   - technical convention questions should be resolved from repo context or focused research
   - execution-time uncertainties should be recorded under `Risks`
7. Write `plan.md` using the compact section set.
8. End with an implementation handoff.

`Implementation Units` may use checkboxes, but they should be coarse units rather than patch-level task lists.

Recommended unit shape:

```markdown
- [ ] Unit 1: Add scaffold command contract
  - Requirements: R1, R2
  - Files: `path/to/file`
  - Depends on: none
  - Approach: concise technical direction
  - Verification: command or manual check expected later
```

Do not create `tasks.md` in Phase 1.
Spec Kit's separate task-generation stage is useful evidence that task breakdown can be valuable, but `harness-kit` should first prove the lighter spec-to-plan contract before adding another artifact or skill.

Readiness criteria before implementation:

- every relevant requirement or success criterion is traced to at least one decision, implementation unit, or verification item
- scope says what this pass will not do
- relevant repo files, docs, conventions, and test locations are named
- decisions include rationale and alternatives when the choice is not obvious
- implementation units are ordered by dependency where order matters
- each implementation unit has expected file targets or artifact targets
- verification lists concrete commands, checks, or manual validation and expected observable outcomes
- remaining unknowns are either implementation-time risks or explicit human-owned blockers
- the implementer should not need to invent product behavior

Verification planning belongs in `hk-plan`, but verification evidence does not.
Actual command execution, results, skipped checks, and remaining verification risk belong in `hk-verify`.

### Decision: make `verification.md` an evidence summary, not a raw log

`verification.md` should record what was checked, what happened, what was skipped, and what risk remains.
It should not duplicate the plan, store full terminal transcripts by default, or replace review.

Comparable systems emphasize the same rule in different forms:

- `archon` writes a validation artifact with summary status, per-check commands, results, fixes made during validation, and remaining warnings
- `superpowers` requires fresh command evidence before any completion claim
- `compound-engineering` puts verification expectations in the plan and treats them as task completion signals during execution
- `spec-kit` includes validation expectations in plans and task acceptance, but does not require a separate heavyweight log artifact

Phase 1 should keep `verification.md` short, but specific enough that a reviewer can tell what evidence supports the completion claim.

Recommended minimum `verification.md` sections:

```markdown
# <Title> Verification

## Summary

## Planned Checks

## Results

## Manual Validation

## Skipped Checks

## Remaining Risk
```

Section responsibilities:

- `Summary`: overall verification status and timestamp
- `Planned Checks`: checks copied or summarized from `plan.md`
- `Results`: command or method, exit/result, and concise evidence for each check
- `Manual Validation`: human-observed checks when command-backed verification is insufficient or unavailable
- `Skipped Checks`: any checks not run, with explicit reason
- `Remaining Risk`: what is still unproven after verification

Allowed per-check result labels should start small:

- `pass`
- `fail`
- `skipped`
- `blocked`

Full logs should stay out of `verification.md` unless they are short and necessary. Prefer concise excerpts, counts, command names, exit status, and links or paths to external artifacts when they exist.

### Decision: make `hk-verify` a fresh-evidence writer, not a fixer or reviewer

`hk-verify` should read `spec.md` and `plan.md`, inspect the implemented workspace, run the planned verification checks, and write `verification.md`.
It should not edit source code, update tests, change plans, approve work, or decide whether remaining risk is acceptable.

Recommended `hk-verify` procedure:

1. Read `spec.md` and `plan.md`.
2. Extract planned checks, expected outcomes, requirement links, and implementation-unit links.
3. Assign check IDs such as `V1`, `V2`, and `V3` when the plan does not already provide them.
4. Run each planned command fresh from the intended working directory.
5. Record command, cwd, exit status, concise output evidence, duration when useful, and any artifact paths.
6. For manual validation, record scenario, method, observer, expected result, observed result, and evidence.
7. Keep running independent checks after a failure when it is safe, so the report gives a full evidence picture.
8. Write `verification.md`.
9. Hand off to `hk-review` only when the evidence is legible enough for a fresh reviewer to assess.

Command derivation order:

1. explicit checks from `plan.md`
2. repo guidance such as `AGENTS.md`
3. standard project scripts only when the plan is incomplete and the script verifies the same claim

Do not silently replace a planned check with a different one.
If an equivalent repo-native check is substituted, record the substitution and rationale.
If no safe equivalent exists, mark the check as `blocked`.

Overall verification verdicts should use:

- `pass`: all required checks passed and evidence matches expectations
- `fail`: one or more required checks ran and contradicted expectations
- `partial`: some evidence is valid, but required evidence is missing, skipped, or manual-only
- `blocked`: verification could not run enough required checks to support a completion claim

Per-check labels remain:

- `pass`
- `fail`
- `skipped`
- `blocked`

Skipped or blocked checks require:

- reason
- whether the check was required for pass
- residual risk
- owner or next step

`hk-verify` should allow writes only to `verification.md` and optional evidence artifacts such as log files or screenshots.
Operational setup or cleanup may run if it is required for a planned check and is recorded, but implementation changes must route back to the implementation step and then be verified again from fresh evidence.

Raw logs should not be pasted into `verification.md` by default.
Use short excerpts that prove the result or explain a failure, and link to raw artifacts when they exist.

`verification.md` should end with a review handoff:

```markdown
## Review Handoff

Verdict: partial
Evidence artifacts:
- verification.md
Failed or blocked checks:
- V2
Suggested review focus:
- areas with manual-only or missing evidence
Recommended next action: return to implementation or continue to hk-review
```

Humans decide whether to accept skipped checks, waive failed or blocked checks, accept remaining risk, or proceed to review with incomplete evidence.
`hk-verify` may recommend, but it should not grant those waivers.

### Decision: make `review.md` a fresh-context findings and resolution record

`review.md` should record what was reviewed, who or what reviewed it, what findings were raised, how they were resolved, and whether any residual risk remains.
It should not collapse into verification, and it should not only say "looks good."

Comparable systems again converge on a findings-oriented shape:

- `superpowers` requests review from a fresh context and requires acting on critical or important feedback before proceeding
- `compound-engineering` groups findings by severity, records reviewer, confidence, route, residual risks, testing gaps, and final verdict
- `archon` synthesizes multiple review artifacts into a consolidated report with severity groups, summary, statistics, and verdict
- `spec-kit` supports review-oriented extensions but does not make review a separate mandatory artifact in the base template

Phase 1 should keep one `review.md` per spec item, with room to paste or summarize findings from human or agent reviewers.

Recommended minimum `review.md` sections:

```markdown
# <Title> Review

## Summary

## Scope

## Reviewers

## Findings

## Resolutions

## Residual Risk

## Verdict
```

Section responsibilities:

- `Summary`: short review outcome
- `Scope`: what diff, files, commit range, or artifact set was reviewed
- `Reviewers`: human reviewers, agent reviewers, or review roles used
- `Findings`: issues grouped or listed with severity, location, evidence, and recommendation
- `Resolutions`: what happened to each actionable finding
- `Residual Risk`: concerns not fully proven or intentionally deferred
- `Verdict`: whether the work is ready, needs changes, or needs discussion

Initial severity labels should use the same simple scale as common review systems:

- `P0`: critical, must fix before completion
- `P1`: high-impact, should fix before completion unless explicitly accepted
- `P2`: meaningful issue, fix if straightforward or defer intentionally
- `P3`: low-impact suggestion or cleanup

Initial resolution labels should stay small:

- `fixed`
- `accepted`
- `deferred`
- `rejected`
- `open`

If there are no findings, `review.md` should say that explicitly and still record scope, reviewer, and verdict.

### Decision: make `hk-review` a read-only fresh-context quality gate

`hk-review` should read the lifecycle artifacts and the current implementation diff, then write `review.md`.
It should not fix implementation issues, waive verification gaps, merge, approve release, or change scope.

Recommended `hk-review` procedure:

1. Read `spec.md`, `plan.md`, `verification.md`, and the current workspace diff, including untracked files when relevant.
2. Reconstruct intent from artifacts, not from the implementer's hidden session history.
3. Review against three contracts:
   - `spec.md`: requirements, success criteria, scope, constraints, assumptions, and open questions
   - `plan.md`: implementation units, decisions, expected files, and expected verification
   - `verification.md`: actual evidence, failed checks, skipped checks, blocked checks, manual validation, and residual risk
4. Inspect changed files and relevant surrounding code or documents.
5. For non-trivial or risky work, use fresh read-only reviewer roles.
6. Synthesize findings into one deduplicated finding set.
7. Write or update only `review.md` in Phase 1.

Useful reviewer roles:

- correctness
- testing and evidence
- maintainability and scope
- security when auth, user input, secrets, filesystem, shell, network, or permissions are touched
- API, data, or reliability when those surfaces are touched

Finding records should be stable and evidence-backed:

```markdown
### F1: Missing failed-check handling in review handoff

Severity: P1
Resolution: open
Reviewer: testing/evidence
Location: path/to/file:12
References: R2, V3
Evidence: concise observed issue
Recommendation: specific action
```

Each finding should include:

- ID such as `F1`
- severity `P0` through `P3`
- resolution state
- reviewer or source
- location when applicable
- reference to requirement, plan unit, verification check, or evidence when applicable
- concrete evidence
- specific recommendation

Resolution policy:

- `fixed`: the implementation or artifact changed and refreshed verification or review evidence supports the fix
- `accepted`: a human explicitly accepted the risk as-is
- `deferred`: a human or owner intentionally moved the issue out of scope with rationale and follow-up target
- `rejected`: the finding is invalid, duplicate, out of scope, or disproven with concrete evidence
- `open`: unresolved

Open `P0` and `P1` findings block a ready verdict.
`P2` findings should be fixed when straightforward or intentionally deferred.
`P3` findings do not block by default.

`hk-review` should treat `verification.md` as evidence, not truth.
It should flag planned checks not run, failed checks marked acceptable without rationale, weak manual validation, evidence that does not map to requirements, and risky changed areas with no verification coverage.

Verdicts should use:

- `ready`: no open `P0` or `P1`, and residual lower-priority risk is fixed, accepted, deferred, or non-blocking
- `ready-with-residual-risk`: no blocking findings, but notable accepted, deferred, skipped, blocked, or manual-only evidence remains
- `not-ready`: open `P0` or `P1`, missing core requirement, failed required verification, or unresolved human decision

If there are no findings, `review.md` must still state the reviewed scope, reviewers, verification evidence considered, residual risk, and verdict.
`hk-review` may say "ready for human approval", but it must not claim human approval.

### Decision: use minimal `spec.md` frontmatter for Phase 1 status

`spec.md` should carry the initial spec item metadata in YAML frontmatter.

Recommended Phase 1 minimum:

```yaml
---
spec_id: 20260427-2015-bootstrap-entrypoint
title: Bootstrap Entrypoint
status: draft
stage: spec
created_at: 2026-04-27 20:15
timezone: Asia/Seoul
---
```

Field meanings:

- `spec_id`: matches the spec item directory name
- `title`: human-readable title
- `status`: overall spec item state
- `stage`: current workflow stage
- `created_at`: local creation timestamp
- `timezone`: timezone used for the timestamp

Initial allowed values:

- `status`: `draft`, `active`, `blocked`, `completed`, `abandoned`
- `stage`: `spec`, `plan`, `implement`, `verify`, `review`

`owner` is intentionally not part of the Phase 1 minimum. The system is internal-first and single-operator by default; ownership can be added later if repeated use shows a real need.

### Decision: do not require `status.md` in Phase 1

`status.md` should not be part of the required Phase 1 spec item shape.

Reason:

- comparable spec-driven tools usually keep lightweight status inside the spec document or task checklist, not in a separate status document
- a separate `status.md` can become duplicate state that drifts from `spec.md`, `plan.md`, `verification.md`, and `review.md`
- Phase 1 should keep the artifact set small and add state surfaces only after repeated use proves the need

Initial status should live in `spec.md` frontmatter. Runtime-oriented state such as resume data, active phase transitions, or machine-owned progress can be introduced later as a dedicated machine-readable artifact if the need becomes concrete.

## Repository Structure Direction

### Decision: separate `harness-kit` product files from downstream installed files

The repository needs to distinguish between:

1. files used to build `harness-kit` itself
2. files that `harness-kit` will install into other repositories

This separation is necessary because their responsibilities differ.

Examples of product-side files:

- roadmap docs
- research docs
- design docs
- install logic
- tests

Examples of downstream installed files:

- `AGENTS.md`
- `harness-kit.yaml`
- workflow artifact scaffolding
- memory scaffolding

### Decision: avoid premature variant layering

At the current stage, variants such as `base`, `codex`, or `claude` overlays are not required.

This means a structure like `template/base/` is considered premature for now.

Current direction:

- use a single `template/` directory if template assets are needed
- introduce variant layering only when real usage pressure appears

### Decision: introduce a minimal `harness-kit.yaml` schema in Phase 1

`harness-kit.yaml` is already part of the required starter surface, so it should have a minimal schema from the beginning.
The schema should be versioned, but it should not try to model every future host, hook, runtime, or policy option.

Recommended Phase 1 minimum:

```yaml
schema_version: 1
timezone: local
workflow:
  artifact_root: specs
  spec_id_format: YYYYMMDD-HHMM-short-slug
  lifecycle:
    - spec
    - plan
    - implement
    - verify
    - review
memory:
  learnings: memory/learnings.md
```

Field responsibilities:

- `schema_version`: allows later migration without guessing file meaning
- `timezone`: records whether timestamps use local operator time or a specific project timezone
- `workflow.artifact_root`: points to the spec item root
- `workflow.spec_id_format`: documents the directory naming contract
- `workflow.lifecycle`: records the active stage model
- `memory.learnings`: points to the initial durable learning artifact

Do not add host-specific keys, hook configuration, runtime state, or tool installation metadata in Phase 1.

### Decision: keep repo-local config authoritative; defer global config

`harness-kit.yaml` should be the only authoritative shared configuration contract through Phase 2.
Do not introduce `~/.harness-kit/config.yaml`, `$XDG_CONFIG_HOME/harness-kit/config.yaml`, or `harness-kit.local.yaml` yet.

Effective configuration order for the near term:

1. built-in defaults
2. repo-local `harness-kit.yaml`
3. explicit one-shot invocation overrides, if a script or future CLI exposes them

This is intentionally simpler than a mature CLI precedence stack.
The repo should be able to explain its harness contract from committed files alone.

Committed `harness-kit.yaml` may contain:

- schema version
- artifact roots and lifecycle paths
- spec ID format
- workflow lifecycle
- memory artifact path
- repo-native verification command declarations when those are designed
- template locations or names when those become configurable
- project-wide conventions that should survive across machines

It must not contain:

- secrets, API keys, tokens, or credentials
- absolute home-directory paths
- personal model, provider, or account choices
- per-developer sandbox, approval, or host safety preferences
- generated runtime state
- "current active task" state
- machine-local binary paths

Future global or user config may be added only for personal or machine preferences that do not change an existing repository's workflow contract, such as verbosity, editor/opener preference, cache or state directory, or default timezone before repository initialization.
Global config must not silently change lifecycle stages, artifact layout, spec ID format, memory policy, or verification gates for an existing repo.

Environment variables should be reserved for secrets, CI flags, ephemeral run identifiers, and explicit one-run automation overrides.
They should not silently disable workflow gates or rewrite repository artifact locations.

Nested `AGENTS.md` files remain the mechanism for local prose instructions.
Do not add nested structured config files until there is clear pressure that prose instructions cannot handle.

### Decision: keep `template/` as one non-variant downstream starter source

`template/` should contain the files that `bootstrap` or `adopt` can install into downstream repositories.
It should stay single-layered in Phase 1.

Recommended product-side template source:

```text
template/
  README.md
  AGENTS.md
  harness-kit.yaml
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
```

Installation notes:

- `README.md` is bootstrap-oriented and must not overwrite an existing README during adoption
- `AGENTS.md` is the thin agent entrypoint
- `harness-kit.yaml` is the repo-local configuration anchor
- `docs/roadmap/README.md` gives downstream projects a direction-setting home without copying this product repo's roadmap
- `specs/.gitkeep` preserves the artifact root before any spec item exists
- `specs/_templates/` gives humans and agents visible artifact templates without creating a fake spec item
- `memory/learnings.md` provides the initial compounding surface

Do not add `template/base/`, host-specific overlays, runtime folders, hooks, generated state, or task databases in Phase 1.

### Decision: make `bootstrap` and `adopt` non-destructive by default

Phase 1 should define two starter entry points with the same target model but different safety assumptions.

Comparable systems show the main risk clearly:

- `spec-kit` supports force-style initialization and warns that template files may be merged or overwritten
- `agent-os` separates base installation from project installation so project installs can be self-contained
- `oh-my-codex` preserves existing `AGENTS.md` unless force or interactive approval is used
- `compound-engineering` setup diagnoses first, then asks before creating or deleting local project files

`harness-kit` should default to the conservative side because adoption into existing repositories is a first-class use case.

`bootstrap` behavior:

- intended for a new or empty repository
- creates the Phase 1 template artifacts
- writes `README.md` only when absent
- creates `AGENTS.md`, `harness-kit.yaml`, `docs/roadmap/README.md`, `specs/`, `specs/_templates/`, and `memory/learnings.md`
- does not create a timestamped spec item by default
- does not install hooks, host-specific config, runtime state, or task databases
- stops on conflicting existing files unless the later CLI provides an explicit force or merge mode

`adopt` behavior:

- intended for an existing repository
- inspects the target shape before writing
- creates missing non-conflicting harness artifacts
- preserves existing `README.md`
- preserves existing `AGENTS.md`; if it exists, report that a harness entrypoint should be merged manually or through an explicit merge mode
- preserves existing `docs/`, `specs/`, and `memory/` contents
- never rewrites project-specific documentation by default
- reports what was created, what already existed, and what still needs manual integration

Phase 1 should not include automatic deep merges into existing Markdown files. If merge behavior is added later, it should be explicit and separately tested.

### Decision: defer `--force` and `--merge`; ship dry-run and conflict reporting first

Phase 1 should not include broad `--force`, smart Markdown merge, or automatic deep merge behavior.
The safe default is:

- inspect target repository first
- create missing harness files only when no conflicting write is required
- treat identical existing files as already satisfied
- report divergent existing files as conflicts
- abort without partial mutation when conflicts are found
- preserve existing `README.md`, `AGENTS.md`, `CLAUDE.md`, `docs/`, `specs/`, and memory files

`bootstrap` and `adopt` should support `--dry-run`.
Dry-run output should report:

- files that would be created
- files already present and preserved
- files that are identical to the starter template
- files that conflict
- suggested manual actions

JSON mode should expose the same actions for agents:

```json
{
  "actions": [
    {"path": "AGENTS.md", "action": "conflict", "reason": "file exists and differs"},
    {"path": "specs/_templates/spec.md", "action": "create"}
  ],
  "safe_to_apply": false
}
```

Do not add prompts as a required Phase 1 path.
Agent-driven and scripted usage should be non-interactive and should fail clearly on conflicts.

Future overwrite or merge modes should be scoped rather than global:

- `--force-managed`: overwrite only harness-owned generated files or marked blocks
- `--backup`: required or default-on for any overwrite
- `--append-agent-block`: append or update a managed block in `AGENTS.md`
- `--replace-agent-file`: separate explicit mode for full replacement, if ever allowed
- `--merge-json`: allowed for configuration only after a polite merge policy is specified

Do not add `--merge-markdown` until the project has stable markers, provenance, or a three-way update model.
A broad force flag would make it unclear whether the tool means "skip prompts", "overwrite managed files", "replace user docs", or "merge content", which is too risky for the adoption use case.

### Decision: use scripts-first entrypoints with CLI-shaped contracts

Phase 1 should keep scripts as the executable surface and avoid introducing a packaged CLI too early.
The scripts should still be designed as if a thin CLI wrapper may call them later.

Phase 1 entrypoint policy:

- starter operations live under `scripts/harness-kit/`
- skill-local deterministic tools live inside the relevant skill, such as `hk-spec/scripts/new-spec-item`
- scripts provide `--help`, `--dry-run`, and `--json` where useful
- structured machine-readable data goes to stdout in JSON mode
- diagnostics go to stderr
- commands are non-destructive by default
- exit codes are meaningful and tested
- command output stays bounded and agent-readable

Do not introduce a packaged `hk` or `harness-kit` CLI in Phase 1.
The future CLI should be a thin wrapper over the same script contracts once the workflow has proven stable.

Introduce a CLI later only when one or more of these become true:

- `bootstrap`, `adopt`, and `doctor` need shared option parsing, config loading, version checks, or migrations
- public distribution needs a one-command install or update path
- multiple hosts need the same stable binary entrypoint
- Windows support needs to be first-class rather than best-effort through Python scripts
- command behavior is stable enough to version as a public API

This follows the strongest pattern from comparable systems: keep repo-local scripts inspectable and easy for agents to call, while leaving room for a CLI once packaging and distribution become real product concerns.
The future binary name, package channel, and public distribution timing remain product decisions, not Phase 1 engineering prerequisites.

### Decision: make `doctor` a read-only starter contract validator

`doctor` should validate whether a repository satisfies the visible `harness-kit` contract.
It should not claim full runtime readiness, run project verification commands by default, install tools, repair files, or approve work.

Phase 1 may ship `scripts/harness-kit/doctor` as a small read-only checker.
If it does not ship immediately, the reserved path and contract should still be documented.

Initial check categories:

- `environment`: git availability, repo root detection, supported OS note, and basic path facts
- `starter_integrity`: required starter files and directories exist
- `config`: `harness-kit.yaml` exists, parses, and has the minimum Phase 1 keys
- `artifact_shape`: `specs/`, `specs/_templates/`, and the four lifecycle templates are recognizable
- `workflow_readiness`: repository can host `spec -> plan -> implement -> verify -> review` artifacts
- `agent_readiness`: `AGENTS.md` exists and appears to be a thin entrypoint, without requiring host-specific config
- `integration_readiness`: optional tools or host files are reported as present, missing, or skipped, but do not block by default

Required starter contract failures should be `fail`.
Optional integrations, reserved paths, or missing later-phase directories should be `warn` or `skip`.

Status labels:

- `pass`
- `warn`
- `fail`
- `skip`
- `error`

Exit codes:

- `0`: no `fail` or `error`; warnings are allowed
- `1`: one or more contract failures
- `2`: invalid invocation, unreadable config, or doctor internal error

`--json` should be a stable script contract from the beginning:

```json
{
  "schema_version": 1,
  "status": "warn",
  "repo_root": "/repo",
  "checks": [
    {
      "id": "artifact.spec_templates",
      "category": "artifact_shape",
      "status": "pass",
      "path": "specs/_templates/spec.md",
      "message": "spec template exists"
    }
  ],
  "summary": {"pass": 8, "warn": 1, "fail": 0, "skip": 2, "error": 0}
}
```

Diagnostics should go to stderr in JSON mode.
Human output should be grouped by category and include concise remediation notes.

`doctor` should be report-only in Phase 1.
Do not add `doctor --fix` yet.
If `--fix` is added later, it should be limited to safe deterministic repairs such as creating missing directories or refreshing harness-owned generated templates.
It must not merge `AGENTS.md`, rewrite user-authored docs, choose verification commands, install dependencies, mutate host config, or perform network checks without an explicit future mode.

Network checks should be disabled by default.
If they are needed later, add an explicit `--online` mode.

Codex-specific checks should remain optional integration checks.
The core doctor contract is host-agnostic starter health, not Codex runtime validation.

### Decision: use a thin starter `AGENTS.md` routing contract

The downstream starter `AGENTS.md` should be a short root entrypoint that routes agents to the working contract.
It should not explain the whole harness, duplicate roadmap or plan documents, or encode host-specific runtime behavior.

Recommended starter template:

```markdown
# Agent Guide

This file is the repository entrypoint for agents. Keep it short: it is a map to the working contract, not the full contract.

## Source Of Truth

Use repository files over chat memory when they conflict.

- Active work lives in `specs/<id>/`.
- Each non-trivial work item should use:
  - `spec.md` — problem, scope, success criteria, non-goals
  - `plan.md` — implementation approach, affected files, risks, checks
  - `verification.md` — commands run, results, gaps
  - `review.md` — independent review findings and outcome
- Long-lived project docs live in `docs/` or the repository's existing documentation structure.
- Directory-specific rules belong in the nearest nested `AGENTS.md`.
- Temporary or branch-local overrides may live in `AGENTS.override.md` only when this repository explicitly uses that convention.

## Workflow

For non-trivial changes, follow:

`spec -> plan -> implement -> verify -> review`

Use harness skills when available:

- `hk-spec` to create or update `specs/<id>/spec.md`
- `hk-plan` to create or update `specs/<id>/plan.md`
- `hk-verify` to create or update `specs/<id>/verification.md`
- `hk-review` to create or update `specs/<id>/review.md`

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
```

For Phase 1, "non-trivial" means work that changes behavior, public interface, repository structure, data, security posture, dependencies, workflow rules, or more than one tightly scoped file.
Tiny typo fixes, formatting-only changes, and obvious one-line documentation corrections may skip `spec` and `plan`, but they still need honest verification appropriate to the change.

The starter should not make `AGENTS.override.md` a required file.
It may mention the convention only as an optional local override mechanism when a repository explicitly adopts it.

Root `AGENTS.md` target length should stay under roughly 100 lines.
If the file grows beyond that, move detail into docs or nested `AGENTS.md` files and keep root as the map.

### Decision: package workflow skills as host-agnostic source with a Codex-first adapter

The canonical workflow skills should live in the product repository under top-level `skills/`.
They should not be copied into every downstream repository by default.

Canonical product layout:

```text
harness-kit/
  skills/
    hk-spec/
      SKILL.md
      scripts/
      assets/
      references/
    hk-plan/
      SKILL.md
    hk-verify/
      SKILL.md
    hk-review/
      SKILL.md
  hosts/
    codex/
      install
      doctor
      uninstall
  scripts/
    harness-kit/
      bootstrap
      adopt
      doctor
  template/
```

Default downstream behavior:

- `bootstrap` and `adopt` install the repo-local contract and starter artifacts
- downstream repositories get `AGENTS.md`, `harness-kit.yaml`, `specs/`, templates, memory, and starter scripts
- downstream repositories do not receive copies of `hk-*` skills by default
- downstream `AGENTS.md` may say to use `hk-*` skills when available

Host adapter behavior:

- install skills only through host-specific adapters
- start with `hosts/codex/`
- keep non-Codex adapters deferred until the core workflow proves stable
- keep adapter code thin and avoid moving core workflow semantics into host-specific packages

Codex install behavior should be user-global by default for internal Phase 2.
Project-local skill installation should be an explicit option for pinned, air-gapped, or team-controlled repositories, not the default.

Managed install rules:

- namespace installed artifacts under `harness-kit`
- write a small manifest for installed skill links or files
- on update, refresh only manifest-owned artifacts
- on uninstall, remove only manifest-owned artifacts
- never delete user-authored skills by name alone
- `doctor` should report skill visibility separately from repo starter contract health

For local development, symlinks from a Codex skill discovery path to the product repo's `skills/hk-*` directories are acceptable.
For public release, copied plugin payloads or a formal Codex plugin may be safer than raw symlinks.

`harness-kit.yaml` should not require installed skills in Phase 2.
If skill visibility is checked, missing skills should be advisory or warning-level unless the user explicitly requested a skill-driven workflow.

This preserves the core design: the repository contract works from files and scripts alone, while skills improve agent ergonomics when installed.

### Current repository-structure direction

The repository is expected to grow toward something like this:

```text
harness-kit/
  README.md
  docs/
    roadmap/
    plans/
    research/
  template/
  scripts/
  tests/
```

This is not yet a final filesystem contract.
It is the current directional model.

## Recommended Next Step

The next implementation pass should harden the starter entrypoints through real use:

- run `bootstrap` against a blank fixture repository
- run `adopt` against at least one existing local repository
- refine conflict reporting only after seeing real adoption friction
- defer force, merge, and `doctor` behavior until those frictions are concrete

## Status

These decisions are current direction, not all-time immutable rules.

However, they are strong enough to guide the next step of design and should be treated as the working baseline until intentionally changed.
