---
title: "RQ1: Baseline Parity"
type: research-question
status: seed
created: 2026-04-21
updated: 2026-05-25
source_ids: []
source_files: [PROJECT_GUIDE.md]
source_tier: tier-b
canonical_url:
tags: [rq1, baseline, dcase, comparison]
---

# RQ1: Baseline Parity

## Purpose

Can AF3 match or exceed the supervised DCASE 2023 Task 6A CNN14 baseline (26.1% SPIDEr-FL) on Clotho v2.1 in a zero-shot setting?

> **Baseline correction (2026-05-25):** earlier drafts quoted "DCASE 2024 baseline, 29.6% SPIDEr-FL". That 29.6% is the DCASE **2024** ConvNeXt-Tiny baseline, **not** CNN14. The project's named traditional baseline is the DCASE **2023** Task 6A CNN14+BART system (published SPIDEr-FL 26.1%), now reproduced locally — see Evidence.

## Key Points

- Head-to-head comparison with bootstrap confidence intervals (BCa).
- Course-safe core question — low risk, well-defined metric.
- Success criterion: AF3 SPIDEr-FL ≥ DCASE baseline SPIDEr-FL with non-overlapping 95% CIs.

## Evidence

- **Baseline reproduced (2026-05-25).** DCASE 2023 Task 6A CNN14+BART run locally on full Clotho-eval (1045 clips, beam=4, CPU): SPIDEr-FL **0.2592** vs published 0.261 — every sub-metric within ~0.005 (CIDEr-D 0.416, SPICE 0.118, METEOR 0.176). Artefacts: `results/cnn14_eval.json`, `results/cnn14_eval_scores.json`, `results/cnn14_eval.manifest.json`.

## Open Questions

- ~~Exact DCASE 2024 baseline configuration to replicate.~~ **RESOLVED:** reproduced the DCASE 2023 Task 6A CNN14+BART baseline (felixgontier repo), not the 2024 ConvNeXt one.
- Whether to report multiple metrics (SPIDEr-FL, FENSE, CLAPScore) or focus on one.
- The H1 threshold (26.1%) is measured on **full** Clotho-eval, but H1 scores AF3 on the **CLEAN** subset — confirm same clip set before freezing the preregistration.

## Links

- [Audio Flamingo 3](../03_models/audio-flamingo-3.md)
- [SPIDEr-FL](../05_metrics/spider-fl.md)
- [Clotho v2.1](../04_datasets/clotho-v21.md)

