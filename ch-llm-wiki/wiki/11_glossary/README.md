---
title: Glossary
type: glossary-entry
tags: [glossary, terms]
status: stable
last_reviewed: 2026-04-20
sources: [../08_sources/project-guide-legacy.md]
---

## Canonical glossary

The **canonical 20-term short glossary** lives in [`PROJECT_GUIDE.md` §Glossary](../../../PROJECT_GUIDE.md). It is the single source of truth for project-wide terminology (AAC, AudioSet, BCa bootstrap, bf16, CHAIR-audio, CLAPScore, Clotho v2.1, Cohen's κ, Contamination audit, DCASE, Ekphrasis, FENSE, Hallucination, Holm-Bonferroni, LALM, MDE, Polyphony, Q-Former, Soundmark, SPIDEr-FL, Zero-shot).

This wiki **does not duplicate** that list.

## Per-term pages — when to add one

Per [`CLAUDE.md` §13.1](../../CLAUDE.md), `wiki/11_glossary/` may grow lightweight per-term entry pages over time. Add a per-term page when a term is:

- **heavily cross-linked** across multiple wiki pages (it deserves a stable target);
- **contested between sources** (and therefore typically paired with a `wiki/09_comparisons/` page);
- in need of **extended discussion** beyond the one-line glossary entry — e.g., a humanities concept whose nuance does not fit a single sentence.

Each per-term page uses the `glossary-entry` schema from [`CLAUDE.md` §4](../../CLAUDE.md) and cites the raw sources behind the term.

## Per-term pages — current

*None yet. The wiki will accumulate them organically as terms warrant their own page.*

Candidates likely to be added first (based on cross-link density):

- `keynote-sound.md`, `soundmark.md`, `signal-sound.md` — tied to [soundscape-schafer](../07_humanities/soundscape-schafer.md).
- `q-former.md` — tied to all three [failure modes](../06_failure_modes/) as the structural mechanism.
- `spider-fl.md` — already exists as the metric card at [../05_metrics/spider-fl.md](../05_metrics/spider-fl.md); a glossary version would be a one-paragraph sibling.
- `contamination-audit.md` — tied to RQ0.

When adding, also add a row to [`index.md`](../../index.md) under §11 and a `CREATE` line in [`log.md`](../../log.md).

## Sources

- [project-guide-legacy](../08_sources/project-guide-legacy.md) — owns the canonical 20-term short glossary referenced above. This page is a stub pointer; the long list lives in `PROJECT_GUIDE.md` §Glossary.
