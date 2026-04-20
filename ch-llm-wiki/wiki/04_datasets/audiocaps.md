---
title: AudioCaps
type: dataset-card
tags: [dataset, audiocaps, audioset, hallucination-stimulus, l1]
status: stub
last_reviewed: 2026-04-20
sources: [../08_sources/paper-summaries-legacy.md]
---

## AudioCaps

| Field | Value |
|:------|:------|
| Purpose | Audio captioning (single-event focus) |
| Size | ~46,000 clips × 1 caption |
| Splits | train / val / test |
| Sample rate | per Kim 2019 (pending re-fetch of NAACL PDF) — `[UNSOURCED-PRIMARY: Kim 2019]` retained |
| Clip length | 10 s |
| Source audio | AudioSet (YouTube) |
| AudioSet tags | available per clip (used for grounding checks) |
| Canonical link | audiocaps.github.io |

### Role in this project

**RQ3 hallucination-stimulus dataset (L1).** AudioCaps is used **only** as the stimulus set for the entity-hallucination experiment ([entity-hallucination](../06_failure_modes/entity-hallucination.md)) because its per-clip AudioSet tags provide a hallucination-vocabulary anchor.

- Feeds RQ3 — single-event clips for CHAIR-audio measurement.

### Known issues

- **Single-caption metrics are annotator-dominated** — SPIDEr / CIDEr / FENSE on AudioCaps are **not** comparable to multi-reference Clotho scores. Do not report SPIDEr-FL on AudioCaps as the headline.
- **Ground truth via AudioSet tags is a lower bound:** rater agreement on AudioSet is moderate (κ ≈ 0.5 on some subsets); audible events are systematically un-tagged. Hence the dual criterion (AudioSet tags **AND** CLAPScore) for hallucination measurement.

### Sources

- [paper-summaries-legacy](../08_sources/paper-summaries-legacy.md) — Paper 3 (Kim 2019, AudioCaps) and Paper 2 (Gemmeke 2017, AudioSet — parent corpus). `[UNSOURCED-PRIMARY: Kim 2019]` `[UNSOURCED-PRIMARY: Gemmeke 2017]` — pending ingest into [`raw/01_primary_sources/`](../../raw/01_primary_sources/). Citation downgrades to `[Kim 2019; L4-via-legacy; MED/HIGH]` until NAACL paper is ingested.

> Legacy synthesis context: [`paper_summaries.md`](../../../paper_summaries.md) Paper 3, [`literature_review.md` §2.2](../../../literature_review.md).
