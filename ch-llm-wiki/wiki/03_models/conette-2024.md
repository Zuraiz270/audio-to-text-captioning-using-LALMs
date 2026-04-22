---
title: "CoNeTTE: An Efficient Audio Captioning System Leveraging Multiple Datasets With Task Embedding"
type: source-note
status: draft
created: 2026-04-21
updated: 2026-04-22
source_ids: [ACM-10.1109/TASLP.2024.3430813]
source_files: []
source_tier: tier-a
canonical_url: https://dl.acm.org/doi/10.1109/TASLP.2024.3430813
tags: [source-note, matrix-section-3, multi-dataset, task-embedding, efficient]
---

# CoNeTTE: An Efficient Audio Captioning System Leveraging Multiple Datasets With Task Embedding

| Field | Value |
|:---|:---|
| **Year** | 2024 |
| **Venue** | IEEE/ACM Trans. Audio, Speech, and Language Processing |
| **Source ID** | ACM-10.1109/TASLP.2024.3430813 |
| **URL** | https://dl.acm.org/doi/10.1109/TASLP.2024.3430813 |
| **Matrix Section** | 3 — Alignment, Strategy & Fine-Tuning |

## Abstract Summary

Efficient AAC system that trains on **multiple datasets simultaneously** using a **Task Embedding (TE) token** to identify the source dataset for each input. Mitigates performance gaps between datasets by conditioning generation on dataset identity. Provides insights into how TEs affect vocabulary (form) and sound event types described (content).

(Source: IEEE Xplore / DuckDuckGo search, IEEE-10603439)

## Key Contributions

- Multi-dataset training for AAC with task embedding tokens.
- Task Embedding mitigates cross-dataset domain shift.
- Analysis of TE impact on vocabulary and content of generated captions.
- Open-source: https://github.com/Labbeti/conette-audio-captioning

## Datasets Used

- Multiple AAC datasets (Clotho, AudioCaps, likely others)

## Metrics Reported

<!-- To be confirmed on full PDF read -->

## Relevance to RQs

- **RQ1 (Baseline Parity):** Multi-dataset training may improve baseline scores.
- **Data Leakage Context:** TE tokens make dataset provenance explicit — useful for contamination analysis.

## Links

- [Improving AAC Mixup](improving-aac-mixup-2024.md)
- [DistillCaps](distillcaps-2024.md)
- [Clotho v2.1](../04_datasets/clotho-v21.md)

