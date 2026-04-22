---
title: "RQ1: Baseline Parity"
type: research-question
status: seed
created: 2026-04-21
updated: 2026-04-21
source_ids: []
source_files: [PROJECT_GUIDE.md]
source_tier: tier-b
canonical_url:
tags: [rq1, baseline, dcase, comparison]
---

# RQ1: Baseline Parity

## Purpose

Can AF3 match or exceed the supervised DCASE 2024 Task 6 baseline (29.6% SPIDEr-FL) on Clotho v2.1 in a zero-shot setting?

## Key Points

- Head-to-head comparison with bootstrap confidence intervals (BCa).
- Course-safe core question — low risk, well-defined metric.
- Success criterion: AF3 SPIDEr-FL ≥ DCASE baseline SPIDEr-FL with non-overlapping 95% CIs.

## Evidence

<!-- To be filled on ingest -->

## Open Questions

- Exact DCASE 2024 baseline configuration to replicate.
- Whether to report multiple metrics (SPIDEr-FL, FENSE, CLAPScore) or focus on one.

## Links

- [AF3 vs DCASE Baseline](../09_comparisons/af3-vs-dcase-baseline.md)
- [Audio Flamingo 3](../03_models/audio-flamingo-3.md)
- [SPIDEr-FL](../05_metrics/spider-fl.md)
- [Clotho v2.1](../04_datasets/clotho-v21.md)
