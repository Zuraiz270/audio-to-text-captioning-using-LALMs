---
title: "Audiopedia: Audio QA with Knowledge"
type: source-note
status: draft
created: 2026-04-21
updated: 2026-04-21
source_ids: [IEEE-10889814]
source_files: []
source_tier: tier-a
canonical_url: https://ieeexplore.ieee.org/document/10889814/
tags: [source-note, matrix-section-3, aqa, knowledge, reasoning]
---

# Audiopedia: Audio QA with Knowledge

| Field | Value |
|:---|:---|
| **Year** | 2025 |
| **Venue** | IEEE ICASSP 2025 |
| **Source ID** | IEEE-10889814 |
| **URL** | https://ieeexplore.ieee.org/document/10889814/ |
| **Matrix Section** | 3 — Alignment, Strategy & Fine-Tuning |

## Abstract Summary

Introduces **Audiopedia** — Audio Question Answering with Knowledge, requiring both audio comprehension AND external knowledge reasoning. Unlike standard AQA that answers from audio alone, Audiopedia targets **knowledge-intensive questions**. Defines three sub-tasks: (i) single-audio QA (s-AQA), (ii) multi-audio QA, and additional variants requiring external world knowledge.

(Source: IEEE Xplore abstract, IEEE-10889814)

## Key Contributions

- First benchmark for knowledge-intensive audio QA.
- Three sub-task definitions for increasing complexity.
- Tests whether audio models can reason beyond pure perception.
- Bridges audio understanding and world knowledge.

## Datasets Used

- Audiopedia benchmark (constructed)

## Metrics Reported

<!-- To be confirmed -->

## Relevance to RQs

- **RQ3 (Hallucination):** Knowledge-intensive QA directly tests whether models hallucinate knowledge vs. retrieve it.
- **RQ5 (Cultural Bias):** Cultural knowledge questions may expose training data biases.

## Links

- [Audio-CoT](audio-cot-2026.md)
- [RAG Low-Resource](rag-low-resource-2025.md)
