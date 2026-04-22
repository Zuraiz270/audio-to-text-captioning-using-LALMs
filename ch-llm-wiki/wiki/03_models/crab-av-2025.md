---
title: "Crab: A Unified Audio-Visual Scene Understanding Model with Explicit Cooperation"
type: source-note
status: draft
created: 2026-04-21
updated: 2026-04-21
source_ids: [IEEE-11093253]
source_files: []
source_tier: tier-a
canonical_url: https://ieeexplore.ieee.org/document/11093253/
tags: [source-note, matrix-section-5, audio-visual, lora, temporal, spatial, unified]
---

# Crab: A Unified Audio-Visual Scene Understanding Model with Explicit Cooperation

| Field | Value |
|:---|:---|
| **Year** | 2025 |
| **Venue** | CVPR 2025, Nashville, TN |
| **Source ID** | IEEE-11093253 |
| **URL** | https://ieeexplore.ieee.org/document/11093253/ |
| **Matrix Section** | 5 — Domain Extensions |

## Abstract Summary

Proposes a unified audio-visual model that achieves **explicit inter-task cooperation** for temporal localization, spatial localization, spatio-temporal reasoning, and pixel-level understanding. Constructs **AV-UIE** (Audio-Visual Unified Instruction-tuning with Explicit reasoning), a dataset that clarifies inter-task relationships. Uses **interaction-aware LoRA** with multiple LoRA heads to learn different aspects of audiovisual interaction. Surpasses existing unified AV models and most specialised models. Open-source.

(Source: IEEE Xplore abstract, IEEE-11093253)

## Key Contributions

- Unifies 4 AV task categories via explicit inter-task cooperation.
- AV-UIE dataset with explicit reasoning process annotations.
- Interaction-aware LoRA with multiple heads — each head develops specific AV understanding.
- Outperforms both unified and specialised models on multiple tasks.
- Open-source: https://github.com/GeWu-Lab/Crab

## Datasets Used

- AV-UIE (constructed, instruction-tuning)
- Multiple existing AV benchmarks (evaluation)

## Metrics Reported

- Outperforms existing unified AV models on temporal, spatial, spatio-temporal, and pixel tasks

## Relevance to RQs

- **Temporal Grounding Context:** Explicitly addresses spatio-temporal reasoning — the grounding problem.
- **RQ2 (Polyphony):** Multi-head LoRA may help decompose concurrent audio-visual events.
- **Architecture:** Shows how inter-task cooperation prevents the heterogeneity interference that joint training causes.

## Limitations / Gotchas

- CVPR = vision-primary venue; audio component may be secondary.
- AV-UIE dataset construction methodology needs scrutiny for audio quality.

## Links

- [Temporal Grounding Loss](../06_failure_modes/temporal-grounding-loss.md)
- [AVQACL++](avqacl-plus-2026.md)
- [CAT+](cat-plus-2025.md)

