---
title: "Recap: Retrieval-Augmented Audio Captioning"
type: source-note
status: draft
created: 2026-04-21
updated: 2026-04-21
source_ids: [IEEE-10448030]
source_files: []
source_tier: tier-a
canonical_url: https://ieeexplore.ieee.org/document/10448030/
tags: [source-note, matrix-section-3, rag, clap, retrieval, domain-transfer]
---

# Recap: Retrieval-Augmented Audio Captioning

| Field | Value |
|:---|:---|
| **Year** | 2024 |
| **Venue** | IEEE ICASSP 2024 |
| **Source ID** | IEEE-10448030 |
| **URL** | https://ieeexplore.ieee.org/document/10448030/ |
| **Matrix Section** | 3 — Alignment, Strategy & Fine-Tuning |

## Abstract Summary

Presents **RECAP** — generates captions conditioned on input audio AND retrieved similar captions from a datastore. Uses **CLAP** to retrieve similar captions from a replaceable datastore. Can transfer to any domain without fine-tuning by swapping the datastore.

(Source: IEEE Xplore abstract, IEEE-10448030)

## Key Contributions

- RAG for audio captioning: retrieval-augmented generation using CLAP similarity.
- Zero-shot domain transfer by datastore replacement (no fine-tuning needed).
- Conditioning on both audio and retrieved text captions.
- Demonstrates RAG effectiveness in audio captioning domain.

## Datasets Used

<!-- To be confirmed -->

## Metrics Reported

<!-- To be confirmed -->

## Relevance to RQs

- **RQ1 (Baseline Parity):** RAG approach may improve zero-shot performance.
- **RQ3 (Hallucination):** Retrieved captions may anchor generation and reduce hallucination — or reinforce it.
- **Data Leakage Context:** Datastore contents directly affect output — if contaminated, results are invalid.

## Links

- [DistillCaps](distillcaps-2024.md)
- [RAG Low-Resource](rag-low-resource-2025.md)
- [CLAPScore](../05_metrics/clapscore.md)

