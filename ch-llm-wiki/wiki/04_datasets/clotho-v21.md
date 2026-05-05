---
title: Clotho v2.1
type: dataset
status: seed
created: 2026-04-21
updated: 2026-04-21
source_ids: []
source_files: []
source_tier: generated
canonical_url:
tags: [dataset, clotho, primary, evaluation]
---

# Clotho v2.1

## Purpose

Primary evaluation dataset for all RQs. Canonical AAC benchmark from DCASE.

## Key Points

- Source: Freesound audio clips, crowd-sourced captions.
- Splits: development, validation, evaluation.
- Captions: 5 per audio clip, 8–20 words each.
- Duration: 15–30 seconds per clip.
- Role: primary benchmark for AF3 vs DCASE baseline comparison.

## Justification over AudioCaps (Methodology Defense)

While AudioCaps is larger, Clotho v2.1 is strictly preferred for this project's evaluation due to:
1. **DCASE Baseline Parity (RQ1)**: Clotho is the canonical benchmark for DCASE Task 6. Using it ensures a direct, apples-to-apples comparison against the official CNN14 baseline.
2. **Mitigating Data Leakage (RQ0)**: AudioCaps is built on AudioSet. Almost all LALMs are pre-trained on AudioSet, creating massive data contamination risks that invalidate zero-shot claims. Clotho (sourced from Freesound) provides a much safer out-of-domain evaluation.
3. **Caption Density (RQ2 & RQ3)**: Clotho provides 5 human-written captions per clip (compared to 1 in the AudioCaps training set). This dense annotation is critical for evaluating polyphony under-description and hallucination accurately.

## Evidence

<!-- To be filled on ingest -->

## Open Questions

- Exact version used in DCASE 2024 Task 6 baseline.
- Known annotation quality issues.
- Overlap with AudioCaps or other training sets.

## Links

- [RQ1: Baseline Parity](../02_research_questions/rq1-baseline-parity.md)
- [AudioCaps](audiocaps.md)
- [ALM Datasets Survey](../08_sources/alm-datasets-survey-2025.md)

