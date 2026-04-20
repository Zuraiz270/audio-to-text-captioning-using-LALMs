---
title: Clotho v2.1
type: dataset-card
tags: [dataset, clotho, freesound, primary-eval, l1]
status: draft
last_reviewed: 2026-04-20
sources: [../08_sources/drossos-2020-clotho.md, ../08_sources/paper-summaries-legacy.md]
---

## Clotho v2.1

| Field | Value |
|:------|:------|
| Purpose | Audio captioning evaluation |
| Size (v2.1) | 6,974 clips × 5 captions each |
| Splits | dev / val / **eval (1,045 clips)** |
| Sample rate | 44.1 kHz (per Drossos 2020 §2.2 — to be confirmed against v2.1 release notes) |
| Clip length | 15–30 s |
| Source audio | FreeSound (CC-licensed) |
| License | CC |
| Canonical record | Zenodo **4783391** (NOT 3490684, which is v1) |

### Role in this project

**Primary evaluation dataset (L1).** All headline RQ1 / RQ2 / RQ3 numbers are computed on the Clotho v2.1 eval split (1,045 clips). Also the official DCASE 2024 Task 6 evaluation set (Labbeti 2024 baseline: SPIDEr-FL 29.6).

- Feeds RQ0 (FreeSound IDs needed for contamination cross-reference), RQ1, RQ2, RQ3, RQ4 (mixture sources).

### Known issues

- **Contamination risk:** Clotho draws from FreeSound; AF3 / SALMONN / WavCaps training corpora may overlap. RQ0 audits this directly.
- **Annotation:** 5 captions per clip, AMT-crowdsourced via Drossos's three-step framework (diversity + content + accuracy), annotators gender-balanced. Inter-annotator agreement on event identification was not measured ([`paper_summaries.md` Paper 1](../../../paper_summaries.md)).
- **Acoustic-focus instruction:** annotators were asked to describe acoustic content only; this is unverifiable empirically — some captions contain inferred visual content.
- **Language:** English-only.

### Sources

- [drossos-2020-clotho](../08_sources/drossos-2020-clotho.md) — primary source card (arXiv 1910.09387 / ICASSP 2020 abstract retrieved 2026-04-20). `[Drossos 2020; L2; HIGH/HIGH]`.
- [paper-summaries-legacy](../08_sources/paper-summaries-legacy.md) — legacy synthesis context (Paper 1). Retained.

> Legacy synthesis context: [`paper_summaries.md`](../../../paper_summaries.md) Paper 1, [`literature_review.md` §1, §2](../../../literature_review.md).
