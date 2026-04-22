---
title: AF3 vs DCASE Baseline
type: comparison
status: seed
created: 2026-04-21
updated: 2026-04-21
source_ids: []
source_files: [PROJECT_GUIDE.md]
source_tier: generated
canonical_url:
tags: [comparison, af3, dcase, baseline, rq1]
---

# AF3 vs DCASE Baseline

## Purpose

Head-to-head comparison table for the central RQ1 question.

## Key Points

| Dimension | AF3 | DCASE 2024 Baseline |
|:---|:---|:---|
| **Training** | Unresolved: zero-shot claim | Supervised on Clotho |
| **SPIDEr-FL** | TBD | 29.6% |
| **Encoder** | AF-Whisper | TBD |
| **LLM** | TBD | N/A (encoder-decoder) |
| **Contamination Status** | TBD (RQ0) | Clean by construction |

## Evidence

<!-- To be filled after contamination audit and baseline replication -->

## Open Questions

- AF3 exact scores on Clotho v2.1.
- Bootstrap CI methodology details.

## Links

- [RQ1: Baseline Parity](../02_research_questions/rq1-baseline-parity.md)
- [Audio Flamingo 3](../03_models/audio-flamingo-3.md)
- [SPIDEr-FL](../05_metrics/spider-fl.md)
