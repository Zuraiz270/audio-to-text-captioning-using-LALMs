---
title: "Extending Large Language Models for Speech and Audio Captioning"
type: source-note
status: draft
created: 2026-04-21
updated: 2026-04-21
source_ids: [IEEE-10446343]
source_files: []
source_tier: tier-a
canonical_url: https://ieeexplore.ieee.org/document/10446343/
tags: [source-note, matrix-section-2, asr, aac, multimodal-llm]
---

# Extending Large Language Models for Speech and Audio Captioning

| Field | Value |
|:---|:---|
| **Year** | 2024 |
| **Venue** | IEEE ICASSP 2024 |
| **Source ID** | IEEE-10446343 |
| **URL** | https://ieeexplore.ieee.org/document/10446343/ |
| **Matrix Section** | 2 — Core LALM Architectures & Engines |

## Abstract Summary

First study achieving **both ASR and AAC** by connecting an LLM with an audio encoder. Addresses the gap that multimodal LLMs show visual capabilities but auditory tasks are under-investigated. Also addresses that ASR and AAC are typically separate systems, yielding incomplete auditory perception.

(Source: IEEE Xplore abstract, IEEE-10446343)

## Key Contributions

- First unified ASR + AAC system via LLM.
- Demonstrates that a single audio-LLM architecture handles both speech recognition and audio captioning.
- Addresses the architectural fragmentation between ASR and AAC communities.

## Datasets Used

<!-- To be confirmed -->

## Metrics Reported

<!-- To be confirmed -->

## Relevance to RQs

- **RQ1 (Baseline Parity):** early LALM approach directly doing AAC.
- **Architecture:** Precursor to SALMONN-style dual-task architectures.

## Links

- [SALMONN](../03_models/salmonn.md)
- [SLAM-LLM](slam-llm-2025.md)
- [Acoustic Prompt Tuning](acoustic-prompt-tuning-2025.md)
