---
title: "CLAIRA: Leveraging Large Language Models to Judge Audio Captions"
type: source-note
status: draft
created: 2026-04-21
updated: 2026-04-21
source_ids: [IEEE-11434610]
source_files: []
source_tier: tier-a
canonical_url: https://ieeexplore.ieee.org/document/11434610
tags: [source-note, matrix-section-4, evaluation, llm-judge, icassp-2025]
---

# CLAIRA: Leveraging Large Language Models to Judge Audio Captions

| Field | Value |
|:---|:---|
| **Year** | 2026 |
| **Venue** | ICASSP 2025, Honolulu, HI |
| **Source ID** | IEEE-11434610 |
| **URL** | https://ieeexplore.ieee.org/document/11434610 |
| **Matrix Section** | 4 — Evaluation Metrics & Bias Mitigation |

## Abstract Summary

Evaluating audio caption quality is expensive via human judgment. This paper proposes CLAIRA — using LLMs as automated judges to measure semantic distance between ground-truth captions and model-generated candidates. Aims to replace or complement traditional NLP metrics (ROUGE, CIDEr) with LLM-based evaluation that better captures semantic similarity.

(Source: IEEE Xplore abstract, IEEE-11434610)

## Key Contributions

- Proposes LLM-as-judge paradigm for audio captioning evaluation.
- Addresses the known gap between automated metrics and human judgment in AAC.
- Potentially complementary to reference-based (SPIDEr-FL) and reference-free (CLAPScore) metrics.

## Datasets Used

<!-- To be confirmed on full PDF read -->

## Metrics Reported

<!-- To be confirmed on full PDF read -->

## Relevance to RQs

- **RQ1 (Baseline Parity):** Provides alternative evaluation paradigm beyond SPIDEr-FL.
- **RQ3 (Hallucination):** LLM judges may detect hallucinated content more reliably than string-matching metrics.

## Limitations / Gotchas

- LLM judges may have their own biases (e.g., preferring verbose captions).
- Cost and reproducibility of LLM-based evaluation.

## Links

- [CLAPScore vs SPIDEr](../09_comparisons/clapscore-vs-spider.md)
- [MACE](mace-2025.md)
- [SPIDEr-FL](../05_metrics/spider-fl.md)
