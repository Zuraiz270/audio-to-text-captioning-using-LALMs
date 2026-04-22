---
title: "WavCaps: A ChatGPT-Assisted Weakly-Labelled Audio Captioning Dataset for Audio-Language Multimodal Research"
type: source-note
status: draft
created: 2026-04-21
updated: 2026-04-22
source_ids: [ACM-10.1109/TASLP.2024.3419446]
source_files: []
source_tier: tier-a
canonical_url: https://dl.acm.org/doi/10.1109/TASLP.2024.3419446
tags: [source-note, matrix-section-1, dataset, chatgpt, weakly-labelled, large-scale]
---

# WavCaps: A ChatGPT-Assisted Weakly-Labelled Audio Captioning Dataset

| Field | Value |
|:---|:---|
| **Year** | 2024 |
| **Venue** | IEEE/ACM Trans. Audio, Speech, and Language Processing |
| **Source ID** | ACM-10.1109/TASLP.2024.3419446 |
| **URL** | https://dl.acm.org/doi/10.1109/TASLP.2024.3419446 |
| **Matrix Section** | 1 — Surveys & Benchmarks |

## Abstract Summary

First **large-scale weakly-labelled audio captioning dataset**: ~400K audio clips with paired captions. Sourced audio clips and raw descriptions from web sources and a sound event detection dataset. Used ChatGPT to process noisy raw descriptions into usable captions. Addresses the critical data scarcity problem in audio-language research.

(Source: arXiv / IEEE Xplore, arXiv:2303.17395)

## Key Contributions

- ~400K audio-caption pairs: largest AAC dataset at time of publication.
- ChatGPT-assisted caption cleaning from noisy web descriptions.
- Enables audio-language retrieval, AAC, and zero-shot audio classification.
- Open-source metadata and code: https://github.com/XinhaoMei/WavCaps

## Datasets Used

- WavCaps (constructed — 400K clips from web + SED sources)

## Metrics Reported

<!-- Multiple tasks evaluated -->

## Relevance to RQs

- **RQ0 (Contamination):** WavCaps is a major training data source for LALMs. If AF3 used WavCaps data, and WavCaps overlaps with Clotho/AudioCaps sources, contamination is possible.
- **RQ1 (Baseline Parity):** Training data scale directly affects model performance.

## Limitations / Gotchas

- "Weakly-labelled" = ChatGPT-cleaned, not human-verified.
- Web sources may overlap with AudioCaps/Clotho test sets.

## Links

- [AudioSetCaps](audiosetcaps-2024.md)
- [ALM Datasets Survey](alm-datasets-survey-2025.md)
- [RQ0: Contamination](../02_research_questions/rq0-contamination.md)
