---
title: SPIDEr-FL — DCASE 2024 official AAC metric
type: metric-card
tags: [metric, spider-fl, dcase, headline, l1]
status: stub
last_reviewed: 2026-04-20
sources: [../08_sources/paper-summaries-legacy.md, ../08_sources/implementation-plan-legacy.md]
---

## SPIDEr-FL

| Field | Value |
|:------|:------|
| Formula / definition | `SPIDEr = (SPICE + CIDEr) / 2`; `SPIDEr-FL = SPIDEr × Fluency_Error_Penalty` |
| Range | [0, 1] (typically reported × 100) |
| Reference-based? | yes — requires reference captions (Clotho v2.1 has 5 per clip) |
| Implementation | `aac-metrics` library |
| Best for | Multi-reference captioning evaluation; the official DCASE 2024 Task 6 score |
| Known limitations | Inherits CIDEr's n-gram dependence; less robust under heavy paraphrase than embedding metrics |

### Role in this project

**Headline metric for RQ1 and RQ2.** All AF3-vs-baseline comparisons are reported in SPIDEr-FL with BCa bootstrap CIs.

- **DCASE 2024 baseline:** **29.6% SPIDEr-FL** on Clotho-eval (Labbeti 2024). Used as the canary for metric-pipeline correctness — if the canary deviates by > 2 pp, the pipeline is broken (red line per [phase-map](../01_project/phase-map.md)).
- **RQ1 success criterion:** AF3 SPIDEr-FL BCa CI lower bound > 29.6% — see [rq-index](../02_research_questions/rq-index.md).

### Sources

- [paper-summaries-legacy](../08_sources/paper-summaries-legacy.md) — Paper 5 (Labbeti 2024, DCASE 2024 baseline & 29.6% SPIDEr-FL number). `[UNSOURCED-PRIMARY: Labbeti 2024]` — pending ingest of the DCASE 2024 technical report (github.com/Labbeti/dcase2024-task6-baseline) into [`raw/01_primary_sources/`](../../raw/01_primary_sources/). Citation downgrades to `[Labbeti 2024; L4-via-legacy; MED/HIGH]` until DCASE TR is ingested.
- [implementation-plan-legacy](../08_sources/implementation-plan-legacy.md) — DCASE 29.6% canary as red-line stop condition (> 2 pp deviation = pipeline broken); BCa CI protocol (n = 1000, seed = 42); SPIDEr-FL as headline metric across RQ1 / RQ2; σ ≈ 12 pp variance budget per Labbeti 2024.

> Legacy synthesis context: [`paper_summaries.md`](../../../paper_summaries.md) Paper 5, [`literature_review.md` §3.2](../../../literature_review.md), [`implementation_plan.md` §Metric Pipeline](../../../implementation_plan.md).
