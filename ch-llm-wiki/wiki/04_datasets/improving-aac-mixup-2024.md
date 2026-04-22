---
title: "Improving Audio Captioning Models with Fine-Grained Audio Features, Text Embedding Supervision, and LLM Mix-Up Augmentation"
type: source-note
status: draft
created: 2026-04-21
updated: 2026-04-21
source_ids: [IEEE-10447215]
source_files: []
source_tier: tier-a
canonical_url: https://ieeexplore.ieee.org/document/10447215/
tags: [source-note, matrix-section-3, fine-grained, mixup, llm-augmentation]
---

# Improving Audio Captioning Models with Fine-Grained Audio Features, Text Embedding Supervision, and LLM Mix-Up Augmentation

| Field | Value |
|:---|:---|
| **Year** | 2024 |
| **Venue** | IEEE ICASSP 2024 |
| **Source ID** | IEEE-10447215 |
| **URL** | https://ieeexplore.ieee.org/document/10447215/ |
| **Matrix Section** | 3 — Alignment, Strategy & Fine-Tuning |

## Abstract Summary

Improves seq2seq AAC models by extensively leveraging pretrained models. Three techniques: (1) Fine-grained audio features, (2) Text embedding supervision, (3) LLM Mix-Up data augmentation. Follows the macro-trend of combining multiple pretrained components for AAC.

(Source: IEEE Xplore abstract, IEEE-10447215)

## Key Contributions

- Three complementary enhancement strategies for seq2seq AAC.
- LLM-based mix-up augmentation: generating diverse training captions.
- Text embedding supervision: aligning generated captions to reference embeddings.
- Fine-grained audio features: extracting richer encoder representations.

## Datasets Used

<!-- To be confirmed -->

## Metrics Reported

<!-- To be confirmed -->

## Relevance to RQs

- **RQ1 (Baseline Parity):** Multiple enhancement techniques that could be applied to any AAC baseline.
- **RQ3 (Hallucination):** Text embedding supervision may help ground generation.

## Links

- [DistillCaps](distillcaps-2024.md)
- [CoNeTTE](conette-2024.md)
