---
title: "Prefix Tuning for Automated Audio Captioning"
type: source-note
status: draft
created: 2026-04-21
updated: 2026-04-21
source_ids: [IEEE-10096877]
source_files: []
source_tier: tier-a
canonical_url: https://ieeexplore.ieee.org/document/10096877/
tags: [source-note, matrix-section-1, prefix-tuning, peft, frozen-lm]
---

# Prefix Tuning for Automated Audio Captioning

| Field | Value |
|:---|:---|
| **Year** | 2023 |
| **Venue** | IEEE ICASSP 2023 |
| **Source ID** | IEEE-10096877 |
| **URL** | https://ieeexplore.ieee.org/document/10096877/ |
| **Matrix Section** | 1 — Surveys & Benchmarks |

## Abstract Summary

Proposes prefix tuning for AAC to handle small-scale dataset challenge. Keeps a pretrained language model **frozen** and only learns to extract global and temporal audio features as prefix tokens. This preserves the LM's text generation expressivity while adapting it to audio.

(Source: IEEE Xplore abstract, IEEE-10096877)

## Key Contributions

- Prefix tuning: learn audio prefix tokens, freeze the language model.
- Handles data scarcity by leveraging pretrained LM knowledge.
- Global + temporal feature extraction from audio.
- Early example of PEFT for AAC (pre-LALM era).

## Datasets Used

<!-- To be confirmed -->

## Metrics Reported

<!-- To be confirmed -->

## Relevance to RQs

- **RQ1 (Baseline Parity):** Prefix tuning baseline predating LALMs.
- **Architecture:** Precursor to modern adapter/prompt-tuning approaches (APT, LoRA).

## Links

- [Acoustic Prompt Tuning](acoustic-prompt-tuning-2025.md)
- [Parameter Efficient AC](parameter-efficient-ac-2024.md)
