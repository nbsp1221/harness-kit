# Research Pass Contract

This document defines the contract for the first full research pass on the six target harness projects.

## Scope

Produce evidence-backed research for:

- `compound-engineering-plugin`
- `gstack`
- `superpowers`
- `oh-my-codex`
- `Archon`
- `OpenHarness`

The goal is not to fully reverse-engineer every repository. The goal is to gather enough structured evidence to complete the target reports and meaningfully update the comparison docs.

## Owners

- Parent agent: synthesis, document writing, final judgment
- Subagents: bounded read-only research on assigned targets
- Review subagents: bounded read-only critique of the drafted reports

## Acceptance Criteria

- Each target report contains concrete evidence for:
  - repository positioning
  - workflow model
  - bootstrap model
  - verification and control model
  - memory and compounding model
  - strengths
  - weaknesses
  - what `harness-kit` should steal
  - what `harness-kit` should avoid
- `comparisons/feature-matrix.md` is updated with less speculative ratings
- `comparisons/overview.md` reflects the current best ranking and rationale
- `comparisons/adoption-notes.md` reflects likely v1 inclusions, partial inclusions, and exclusions

## Evidence Required

Subagents must return:

- concrete file paths
- concise findings tied to those files
- why each finding matters for `harness-kit`
- unresolved questions where evidence is incomplete

Evidence should prefer:

- top-level `README.md`
- install or setup docs
- command, skill, hook, workflow, or config files
- architecture or contributor docs when they clarify the operating model

## Output Contract For Subagents

Use this exact shape:

```text
Scope:
Owner:

Findings:
- Claim:
  Evidence:
  Why it matters:

- Claim:
  Evidence:
  Why it matters:

What To Steal:
- ...

What Not To Steal:
- ...

Open Questions:
- ...

Next-step note:
```

## Next-Step Note

The parent agent uses returned evidence to populate `docs/research/summaries/*.md`, then updates the comparison docs, then runs a bounded review fan-out before final synthesis.
