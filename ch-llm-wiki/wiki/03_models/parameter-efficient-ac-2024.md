---
title: "Parameter Efficient Audio Captioning with Faithful Guidance Using Audio-Text Shared Latent Representation"
type: source-note
status: draft
created: 2026-04-21
updated: 2026-04-21
source_ids: [IEEE-10448154]
source_files: []
source_tier: tier-a
canonical_url: https://ieeexplore.ieee.org/document/10448154
tags: [source-note, matrix-section-3, peft, hallucination, edge-deployment]
---

# Parameter Efficient Audio Captioning with Faithful Guidance Using Audio-Text Shared Latent Representation

| Field | Value |
|:---|:---|
| **Year** | 2024 |
| **Venue** | IEEE ICASSP 2024 |
| **Source ID** | IEEE-10448154 |
| **URL** | https://ieeexplore.ieee.org/document/10448154 |
| **Matrix Section** | 3 — Alignment, Strategy & Fine-Tuning |

## Abstract Summary

Addresses two problems in pretrained transformer AAC models: **hallucination** and **large memory footprint**. Proposes a data augmentation technique for generating hallucinated audio captions to train the model to distinguish faithful vs. hallucinated content. Uses audio-text shared latent representations for parameter efficiency, enabling edge deployment.

(Source: IEEE Xplore abstract, IEEE-10448154)

## Key Contributions

- Data augmentation method for generating negative (hallucinated) training captions.
- Similarity-based hallucination detection using audio-text shared representations.
- Parameter efficient — targets edge/embedded deployment.
- Directly addresses the hallucination problem in AAC.

## Datasets Used

<!-- To be confirmed on full PDF read -->

## Metrics Reported

<!-- To be confirmed on full PDF read -->

## Relevance to RQs

- **RQ3 (Hallucination):** Directly addresses hallucination via training-time negative examples.
- **Architecture:** Parameter-efficient approach relevant to resource-constrained evaluation.

## Limitations / Gotchas

- Generated hallucinated captions may not cover all hallucination patterns seen in LALMs.
- Edge deployment constraints may limit model quality.

## Links

- [RQ3: Hallucination](../02_research_questions/rq3-hallucination.md)
- [Entity Hallucination](../06_failure_modes/entity-hallucination.md)
- [Acoustic Prompt Tuning](acoustic-prompt-tuning-2025.md)
- [Prefix Tuning for AAC](prefix-tuning-aac-2023.md)
