---
title: "OpenBEATs: A Fully Open-Source General-Purpose Audio Encoder"
type: source-note
status: draft
created: 2026-04-21
updated: 2026-04-21
source_ids: [IEEE-11230965]
source_files: []
source_tier: tier-a
canonical_url: https://ieeexplore.ieee.org/document/11230965
tags: [source-note, matrix-section-1, encoder, beats, open-source, masked-prediction]
---

# OpenBEATs: A Fully Open-Source General-Purpose Audio Encoder

| Field | Value |
|:---|:---|
| **Year** | 2025 |
| **Venue** | IEEE Conference (2025) |
| **Source ID** | IEEE-11230965 |
| **URL** | https://ieeexplore.ieee.org/document/11230965 |
| **Matrix Section** | 1 — Surveys & Benchmarks |

## Abstract Summary

Addresses the gap that BEATs (the only notable masked token prediction model for general audio) has no open-source pretraining code and was trained only on AudioSet. **OpenBEATs** provides fully open-source pretraining, enabling broader downstream applications. Masked token prediction unifies pre-training across language, vision, speech, and audio.

(Source: IEEE Xplore abstract, IEEE-11230965)

## Key Contributions

- Fully open-source BEATs alternative.
- Open-source pretraining code (bridging a critical gap).
- Extends BEATs beyond AudioSet-only training.
- Demonstrates masked token prediction for general audio understanding.

## Datasets Used

- AudioSet + additional datasets (expanding beyond original BEATs)

## Metrics Reported

<!-- To be confirmed -->

## Relevance to RQs

- **Architecture:** BEATs is used as encoder in SALMONN (Whisper + BEATs). OpenBEATs could be a transparent replacement.
- **Data Leakage Context:** Open-source training allows full audit of training data.

## Links

- [SALMONN](../03_models/salmonn.md)
- [SLAM-LLM](slam-llm-2025.md)

