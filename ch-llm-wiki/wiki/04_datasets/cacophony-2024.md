---
title: "Cacophony: An Improved Contrastive Audio-Text Model"
type: source-note
status: draft
created: 2026-04-21
updated: 2026-04-22
source_ids: [ACM-10.1109/TASLP.2024.3485170]
source_files: []
source_tier: tier-a
canonical_url: https://dl.acm.org/doi/10.1109/TASLP.2024.3485170
tags: [source-note, matrix-section-2, contrastive, clap, large-scale, 13k-hours]
---

# Cacophony: An Improved Contrastive Audio-Text Model

| Field | Value |
|:---|:---|
| **Year** | 2024 |
| **Venue** | IEEE/ACM Trans. Audio, Speech, and Language Processing |
| **Source ID** | ACM-10.1109/TASLP.2024.3485170 |
| **URL** | https://dl.acm.org/doi/10.1109/TASLP.2024.3485170 |
| **Matrix Section** | 2 — Core LALM Architectures & Engines |

## Abstract Summary

Audio-text models lag behind image-text counterparts in scale and performance. Cacophony improves both **data scale** (13,000 hours of text-labelled audio) and **training procedure** for contrastive audio-text models. Uses pretrained language models to process noisy text descriptions into cleaner training signals.

(Source: arXiv:2402.06986 / IEEE Xplore)

## Key Contributions

- 13,000 hours of text-labelled audio: significant scale-up over prior CLAP models.
- Improved training procedure for contrastive audio-text learning.
- Addresses the gap between audio-text and image-text model performance.
- Uses LLMs to clean noisy text labels.

## Datasets Used

- 13K hours of text-labelled audio (curated from multiple sources)

## Metrics Reported

<!-- To be confirmed -->

## Relevance to RQs

- **RQ1 (Baseline Parity):** Better CLAP-style embeddings improve CLAPScore and contrastive evaluation.
- **Architecture:** Contrastive models are the backbone of reference-free evaluation (CLAPScore).

## Links

- [CLAPScore](../05_metrics/clapscore.md)
- [EnCLAP](enclap-2024.md)
- [WavCaps](wavcaps-2024.md)
