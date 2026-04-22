---
title: "SLAM-LLM: A Modular, Open-Source Multimodal Large Language Model Framework"
type: source-note
status: draft
created: 2026-04-21
updated: 2026-04-21
source_ids: [IEEE-11346946]
source_files: []
source_tier: tier-a
canonical_url: https://ieeexplore.ieee.org/document/11346946
tags: [source-note, matrix-section-2, framework, modular, open-source]
---

# SLAM-LLM: A Modular, Open-Source Multimodal Large Language Model Framework

| Field | Value |
|:---|:---|
| **Year** | 2025 |
| **Venue** | IEEE/ACM Trans. Audio, Speech, and Language Processing, pp. 63–76 |
| **Source ID** | IEEE-11346946 |
| **URL** | https://ieeexplore.ieee.org/document/11346946 |
| **Matrix Section** | 2 — Core LALM Architectures & Engines |

## Abstract Summary

Presents **SLAM-LLM**, an open-source framework for training customised MLLMs focused on speech, language, audio, and music. Provides modular configuration of different encoders, projectors, LLMs, and PEFT plugins. Includes training/inference recipes for mainstream tasks including **Automated Audio Captioning (AAC)** and Music Captioning. Some recipes have reached or are nearing SOTA performance. Addresses the gap that most MLLM frameworks (e.g., LLaVA, OpenFlamingo) prioritise vision over audio.

(Source: IEEE Xplore abstract, IEEE-11346946)

## Key Contributions

- Universal modular framework: plug-and-play encoders, projectors, LLMs, PEFT.
- Explicit AAC recipe included — directly relevant to this project.
- Open-source with high-performance checkpoints.
- Standardises the audio MLLM training stack.
- CC-BY licensed.

## Datasets Used

<!-- Multiple tasks — specific AAC datasets in paper -->

## Metrics Reported

- Near-SOTA on AAC and Music Captioning (specific scores in paper)

## Relevance to RQs

- **RQ1 (Baseline Parity):** SLAM-LLM's AAC recipe could serve as an alternative baseline.
- **Architecture:** Demonstrates that modular design (encoder + projector + LLM) is the dominant paradigm.

## Limitations / Gotchas

- Framework paper — individual task performance depends on configuration.
- Rapid development may make specific checkpoints outdated.

## Links

- [Falcon3-Audio](falcon3-audio-2026.md)
- [DeSTA2.5-Audio](desta25-audio-2026.md)
- [Audio Flamingo 3](../03_models/audio-flamingo-3.md)
