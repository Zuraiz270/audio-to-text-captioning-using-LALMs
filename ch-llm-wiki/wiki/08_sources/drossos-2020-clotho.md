---
type: source-card
status: draft
last_reviewed: 2026-04-20
---

# Drossos et al. 2020 — Clotho

**Raw file:** [drossos-2020-clotho-abstract.md](../../raw/01_primary_sources/drossos-2020-clotho-abstract.md)
**External:** arXiv 1910.09387 (https://arxiv.org/abs/1910.09387)
**Venue / Level:** ICASSP 2020 — L2
**Confidence / Applicability:** HIGH / HIGH

## Claim

Clotho is a 4,981-clip audio-captioning dataset (15–30 s, 5 captions per clip, 8–20 words, no speech, gender-balanced annotation) built via a documented three-step caption-crafting framework.

## Method

- Source audio: Freesound
- Three-step caption crafting (diversity + content + accuracy)
- Five captions per clip
- No speech in audio (forces non-speech sound description)

## Key numbers

- v1: 4,981 clips, 24,905 captions
- v2.1 (project-relevant): Zenodo DOI **4783391** (NOT 3490684 — earlier draft error)
- DCASE 2024 Task 6 baseline on v2.1 eval split: SPIDEr-FL 29.6 (per Labbeti 2024)

## Threat to validity

- v1 paper does not enumerate v2.1's eval split; that information lives in the DCASE-2021/2024 task descriptions and Labbeti 2024 baseline.
- Annotation language English-only.

## Feeds

- RQ0 (contamination check on eval IDs)
- RQ1 (DCASE baseline target)
- RQ2 (200-clip polyphony subset is derived from Clotho v2.1 eval split)
- RQ4 (Clotho clips form the A/B sources for synthetic A-then-B mixtures)

## One-sentence reservation

The v1 paper documents the original release; v2.1 specifics (split, hash) are pinned in implementation_plan.md §11 and depend on Zenodo record 4783391, not on this paper.

## Cross-links

- [clotho-v2-1.md](../04_datasets/clotho-v2-1.md)
- [paper-summaries-legacy.md](paper-summaries-legacy.md) — earlier bridge, now superseded
