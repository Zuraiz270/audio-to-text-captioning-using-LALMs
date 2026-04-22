---
title: "DeSTA2.5-Audio: Toward General-Purpose Large Audio Language Model With Self-Generated Cross-Modal Alignment"
type: source-note
status: draft
created: 2026-04-21
updated: 2026-04-21
source_ids: [IEEE-11447408]
source_files: []
source_tier: tier-a
canonical_url: https://ieeexplore.ieee.org/document/11447408/
tags: [source-note, matrix-section-2, desta, catastrophic-forgetting, alignment]
---

# DeSTA2.5-Audio: Toward General-Purpose Large Audio Language Model With Self-Generated Cross-Modal Alignment

| Field | Value |
|:---|:---|
| **Year** | 2026 |
| **Venue** | IEEE/ACM Transactions on Audio, Speech, and Language Processing |
| **Source ID** | IEEE-11447408 |
| **URL** | https://ieeexplore.ieee.org/document/11447408/ |
| **Matrix Section** | 2 — Core LALM Architectures & Engines |

## Abstract Summary

Introduces DeSTA2.5-Audio, a general-purpose LALM addressing **catastrophic forgetting** — the critical challenge where audio training degrades the LLM's original language abilities. Proposes a **self-generated cross-modal alignment strategy** where the backbone LLM generates its own training targets ("DeSTA" approach). This preserves native language proficiency and enables zero-shot generalization. Constructs **DeSTA-AQA5M**, a 5M-sample task-agnostic dataset from 7,000 hours across 50 diverse datasets.

(Source: IEEE Xplore abstract, IEEE-11447408)

## Key Contributions

- Solves catastrophic forgetting via self-generated cross-modal alignment.
- DeSTA-AQA5M: 5M training samples, 7K hours, 50 datasets (speech, environmental, music).
- SOTA or competitive on Dynamic-SUPERB, MMAU, SAKURA, Speech-IFEval, VoiceBench.
- Self-generated strategy outperforms existing training strategies in comparative studies.
- General-purpose: not task-specific, enables zero-shot transfer.

## Datasets Used

- DeSTA-AQA5M (training — 50 source datasets)
- Dynamic-SUPERB, MMAU, SAKURA, Speech-IFEval, VoiceBench (evaluation)

## Metrics Reported

- SOTA on multiple benchmarks (specific scores in paper, pp. 2062–2076)

## Relevance to RQs

- **RQ1 (Baseline Parity):** Self-generated alignment may explain why some LALMs outperform others on captioning without explicit AAC training.
- **Architecture:** Demonstrates that alignment strategy matters more than scale.

## Limitations / Gotchas

- 5M samples / 7K hours is still substantial compute.
- Zero-shot generalization claim needs testing on Clotho specifically.

## Links

- [Falcon3-Audio](falcon3-audio-2026.md)
- [SLAM-LLM](slam-llm-2025.md)
- [AVQACL++](avqacl-plus-2026.md)
