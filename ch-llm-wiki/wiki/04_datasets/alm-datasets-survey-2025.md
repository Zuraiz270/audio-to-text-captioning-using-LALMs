---
title: "Audio-Language Datasets of Scenes and Events: A Survey"
type: source-note
status: active
created: 2026-04-21
updated: 2026-04-22
source_ids: [IEEE-10874676]
source_files: [raw/01_primary_sources/Audio-Language_Datasets_of_Scenes_and_Events_A_Survey.pdf]
source_tier: tier-b
canonical_url: https://ieeexplore.ieee.org/document/10874676/
tags: [source-note, matrix-section-1, survey, datasets, data-leakage, zero-shot, rq0]
---

# Audio-Language Datasets of Scenes and Events: A Survey

| Field | Value |
|:---|:---|
| **Year** | 2025 |
| **Venue** | IEEE Access (Vol 13) |
| **Source ID** | IEEE-10874676 |
| **URL** | https://ieeexplore.ieee.org/document/10874676/ |
| **Matrix Section** | 1 — Surveys & Benchmarks |
| **Downloaded via** | Universität Bamberg institutional access |

## Abstract Summary

Comprehensive survey of 69 audio-language datasets for scenes and events (excluding speech/music). Exposes critical flaws in evaluation methodologies, highlighting how **data leakage between datasets invalidates many zero-shot learning claims**. Argues that recognizing a dog bark in a test set is not "zero-shot" if the model was pretrained on AudioSet dog barks.

(Source: Full PDF, IEEE-10874676)

## Key Findings

### 1. The Zero-Shot Illusion
- True "zero-shot" learning is rare in practice.
- Models pretrained on massive datasets (like AudioSet) have seen almost all common audio concepts.
- When evaluated down-stream, performance on overlapping categories does not represent genuine generalization.

### 2. Dataset Overlap (Data Leakage)
- The paper conducts a thorough data leak analysis across audio datasets.
- Current audio datasets heavily recycle source materials (YouTube, Freesound).
- If Test Set B shares sources with Training Set A, models pre-trained on A will perform artificially well on B.

### 3. Emergence of LLM Data Generation
- Recent trend: Using LLMs to annotate, clean, or augment audio captions (e.g., WavCaps).
- While this solves scale issues, it risks "model collapse" and introduces LLM priors into the audio datasets.

## Relevance to RQs

- **RQ0 (Contamination):** ★★★ Core evidence for the contamination hypothesis. This survey proves that datasets overlap significantly and zero-shot claims must be audited for data leakage.
- **RQ1 (Baseline Parity):** Performance on Clotho/AudioCaps might just be measuring how much of Freesound/YouTube the model memorized during pre-training.

## Methodological Warning for Project

- **AudioCaps** tests are highly compromised if the model's base encoder was pretrained on **AudioSet**, because AudioCaps is derived directly from AudioSet.
- **Clotho** uses Freesound. If the model was pretrained on Freesound data (like LAION-Audio-630K or WavCaps), Clotho evaluation is contaminated.
- To prove whether AF3 or SALMONN are actually better, we MUST trace their pretraining data lineages.

## Links

- [RQ0: Contamination](../02_research_questions/rq0-contamination.md)
- [WavCaps](wavcaps-2024.md)
- [Data Leakage Benchmark](data-leakage-benchmark-2026.md)
