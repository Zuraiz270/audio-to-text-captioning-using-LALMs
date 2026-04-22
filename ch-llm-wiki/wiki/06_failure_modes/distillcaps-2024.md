---
title: "DistillCaps: Enhancing Audio-Language Alignment in Captioning via Retrieval-Augmented Knowledge Distillation"
type: source-note
status: draft
created: 2026-04-21
updated: 2026-04-22
source_ids: [ACM-10.1145/3746252.3761269]
source_files: []
source_tier: tier-a
canonical_url: https://dl.acm.org/doi/abs/10.1145/3746252.3761269
tags: [source-note, matrix-section-3, rag, knowledge-distillation, training-time]
---

# DistillCaps: Enhancing Audio-Language Alignment in Captioning via Retrieval-Augmented Knowledge Distillation

| Field | Value |
|:---|:---|
| **Year** | 2024 |
| **Venue** | ACM Multimedia 2024 |
| **Source ID** | ACM-10.1145/3746252.3761269 |
| **URL** | https://dl.acm.org/doi/abs/10.1145/3746252.3761269 |
| **Matrix Section** | 3 — Alignment, Strategy & Fine-Tuning |

## Abstract Summary

AAC benefits from external context via RAG, but inference-time RAG is infeasible due to data availability, latency, and complexity. **DistillCaps** uses RAG at **training time** to guide knowledge distillation — the model learns from retrieval-augmented contexts but doesn't need them at inference. This "distills" retrieval knowledge into the model weights.

(Source: ACM DL abstract)

## Key Contributions

- Training-time RAG: retrieval-augmented knowledge distillation (not inference-time RAG).
- Eliminates inference-time datastore dependency.
- Knowledge distillation from RAG teacher to student model.
- Combines benefits of RAG (context) with benefits of standalone models (inference speed).

## Datasets Used

<!-- To be confirmed -->

## Metrics Reported

<!-- To be confirmed -->

## Relevance to RQs

- **RQ1 (Baseline Parity):** DistillCaps may improve captioning quality without inference overhead.
- **RQ3 (Hallucination):** Distilled retrieval knowledge may reduce hallucination by grounding in real examples.

## Links

- [RECAP](recap-2024.md)
- [RAG Low-Resource](rag-low-resource-2025.md)
- [Improving AAC Mixup](improving-aac-mixup-2024.md)
