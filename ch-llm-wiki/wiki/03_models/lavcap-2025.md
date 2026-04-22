---
title: "LAVCap: LLM-based Audio-Visual Captioning using Optimal Transport"
type: source-note
status: draft
created: 2026-04-21
updated: 2026-04-22
source_ids: [IEEE-10888241]
source_files: []
source_tier: tier-a
canonical_url: https://ieeexplore.ieee.org/document/10888241/
tags: [source-note, matrix-section-3, audio-visual, optimal-transport, llm]
---

# LAVCap: LLM-based Audio-Visual Captioning using Optimal Transport

| Field | Value |
|:---|:---|
| **Year** | 2025 |
| **Venue** | IEEE ICASSP 2025 |
| **Source ID** | IEEE-10888241 |
| **URL** | https://ieeexplore.ieee.org/document/10888241/ |
| **Matrix Section** | 3 — Alignment, Strategy & Fine-Tuning |

## Abstract Summary

LLM-based audio-visual captioning framework that uses **optimal transport-based alignment loss** to bridge the modality gap between audio and visual features. Proposes an **optimal transport attention module** for audio-visual fusion using transport assignment maps. Achieves SOTA on AudioCaps benchmark.

(Source: arXiv:2501.09291)

## Key Contributions

- Optimal transport for audio-visual modality alignment: mathematically principled fusion.
- Audio-visual captioning: visual context improves audio caption quality.
- OT attention module: transport assignment maps guide cross-modal attention.
- SOTA on AudioCaps.

## Datasets Used

- AudioCaps (evaluation)

## Metrics Reported

- SOTA on AudioCaps (specific scores in paper)

## Relevance to RQs

- **RQ2 (Polyphony):** Visual context may help disambiguate concurrent audio events.
- **RQ4 (Temporal):** Visual temporal cues may improve temporal grounding in captions.

## Limitations / Gotchas

- Requires paired audio-visual data (not applicable to audio-only scenarios).
- AudioCaps-centric evaluation — Clotho v2.1 performance unknown.

## Links

- [Crab AV](crab-av-2025.md)
- [CAT+](cat-plus-2025.md)
- [Dual-Layer Video](dual-layer-video-2025.md)
