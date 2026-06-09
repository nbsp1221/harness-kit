# Research Archive

This directory stores durable research for `wayrail`.

The goal is not to collect loose notes. The goal is to build a reusable decision archive that answers:

- which existing harness projects matter
- how each project works
- what `wayrail` should copy
- what `wayrail` should avoid

## Structure

```text
docs/research/
  README.md
  process/
  passes/
  summaries/
  dossiers/
  comparisons/
```

- `summaries/`: quick judgment reports for each target
- `dossiers/`: source-grounded deep reports for long-term reuse
- `comparisons/`: cross-project synthesis for faster decisions
- `passes/`: immutable snapshot notes for each research pass
- `process/`: templates and research contracts

## Current Target Set

- [compound-engineering-plugin summary](./summaries/compound-engineering-plugin.md)
- [gstack summary](./summaries/gstack.md)
- [superpowers summary](./summaries/superpowers.md)
- [oh-my-codex summary](./summaries/oh-my-codex.md)
- [Archon summary](./summaries/archon.md)
- [OpenHarness summary](./summaries/openharness.md)

## Deep Dossiers

- [compound-engineering-plugin dossier](./dossiers/compound-engineering-plugin.md)
- [gstack dossier](./dossiers/gstack.md)
- [superpowers dossier](./dossiers/superpowers.md)
- [oh-my-codex dossier](./dossiers/oh-my-codex.md)
- [archon dossier](./dossiers/archon.md)
- [openharness dossier](./dossiers/openharness.md)

## Process Docs

- [summary template](./process/summary-template.md)
- [dossier template](./process/dossier-template.md)
- [research pass contract](./process/research-pass-contract.md)
- [deep research contract](./process/deep-research-contract.md)

## Comparison Docs

- [Overview](./comparisons/overview.md)
- [Feature Matrix](./comparisons/feature-matrix.md)
- [Adoption Notes](./comparisons/adoption-notes.md)

## Research Passes

- [2026-04-21 First Pass](./passes/2026-04-21-first-pass.md)

## Research Rules

- Prefer stable file paths over date-stamped filenames for target reports.
- Keep summary and dossier layers separate.
- Put dates in frontmatter, not filenames.
- Treat each target report as an updateable working document.
- Record evidence explicitly so future re-analysis is cheap.
- Pin each research pass to upstream commit refs.
- End each target report with `What To Steal` and `What Not To Steal`.
- Keep comparisons opinionated, but keep target reports evidence-heavy.

## Update Workflow

1. Update the relevant file in `summaries/` when quick judgment changes.
2. Update the relevant file in `dossiers/` when source reconstruction deepens.
3. Update `comparisons/feature-matrix.md` if the change affects comparative judgment.
4. Update `comparisons/overview.md` if the ranking or recommended direction changes.
5. Update `comparisons/adoption-notes.md` when a new design implication for `wayrail` becomes clear.

## Scope

This research archive is focused on open harness systems, workflow plugins, orchestration layers, and agent-development methodologies that materially inform `wayrail`.
