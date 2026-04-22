---
title: "AudioSetCaps: An Enriched Audio-Caption Dataset Using Automated Generation Pipeline"
type: source-note
status: draft
created: 2026-04-21
updated: 2026-04-21
source_ids: [IEEE-11051255]
source_files: []
source_tier: tier-a
canonical_url: https://ieeexplore.ieee.org/document/11051255/
tags: [source-note, matrix-section-1, dataset, audioset, pipeline, lalm]
---

# AudioSetCaps: An Enriched Audio-Caption Dataset Using Automated Generation Pipeline

| Field | Value |
|:---|:---|
| **Year** | 2024 |
| **Venue** | IEEE/ACM Trans. Audio, Speech, and Language Processing |
| **Source ID** | IEEE-11051255 |
| **URL** | https://ieeexplore.ieee.org/document/11051255/ |
| **Matrix Section** | 1 — Surveys & Benchmarks |

## Abstract Summary

Addresses the bottleneck of constructing large-scale paired audio-language datasets. Proposes an automated pipeline integrating audio-language models to extract detailed audio information and generate enriched captions. Current synthetic caption approaches struggle to incorporate fine-grained audio details. AudioSetCaps enriches AudioSet with high-quality automated captions.

(Source: IEEE Xplore abstract, IEEE-11051255)

## Key Contributions

- Automated pipeline for large-scale audio caption generation.
- Uses audio-language models in the caption generation loop.
- Enriches AudioSet — directly relevant to data-leakage contamination questions.
- Addresses data scarcity in AAC training.

## Datasets Used

- AudioSet (base dataset for enrichment)

## Metrics Reported

<!-- To be confirmed on full PDF read -->

## Relevance to RQs

- **Data Leakage Context:** AudioSetCaps derived from AudioSet — if AF3 used this, contamination with AudioCaps (also AudioSet-derived) could occur.
- **RQ1 (Baseline Parity):** More training data → potentially better captioning.

## Limitations / Gotchas

- Automated captions may inherit biases from the generating LALM.
- AudioSet overlap with AudioCaps creates contamination risk.

## Links

- [WavCaps](wavcaps-2024.md)
- [ALM Datasets Survey](alm-datasets-survey-2025.md)

