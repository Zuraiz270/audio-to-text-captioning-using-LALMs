---
title: "Acoustic Prompt Tuning: Empowering Large Language Models With Audition Capabilities"
type: source-note
status: draft
created: 2026-04-21
updated: 2026-04-21
source_ids: [IEEE-10852359]
source_files: []
source_tier: tier-a
canonical_url: https://ieeexplore.ieee.org/document/10852359
tags: [source-note, matrix-section-3, prompt-tuning, adapter, peft]
---

# Acoustic Prompt Tuning: Empowering Large Language Models With Audition Capabilities

| Field | Value |
|:---|:---|
| **Year** | 2025 |
| **Venue** | IEEE/ACM Trans. Audio, Speech, and Language Processing |
| **Source ID** | IEEE-10852359 |
| **URL** | https://ieeexplore.ieee.org/document/10852359 |
| **Matrix Section** | 3 — Alignment, Strategy & Fine-Tuning |

## Abstract Summary

Introduces **Acoustic Prompt Tuning (APT)**, a new adapter extending LLMs and VLMs to the audio domain without compromising domain-specific capability. Addresses the gap that few LLMs/VLMs can generalise to audio. APT injects auditory capabilities via acoustic prefix prompt blocks — a PEFT approach that avoids full retraining.

(Source: IEEE Xplore abstract, IEEE-10852359)

## Key Contributions

- APT adapter: extends frozen LLMs to audio without retraining the base model.
- Preserves original language capability while adding audition.
- PEFT approach — computationally efficient.

## Datasets Used

<!-- To be confirmed on full PDF read -->

## Metrics Reported

<!-- To be confirmed on full PDF read -->

## Relevance to RQs

- **RQ1 (Baseline Parity):** APT represents a PEFT alternative to full LALM training.
- **Architecture:** Demonstrates that adapter-based audio integration is viable.

## Limitations / Gotchas

- Adapter quality depends on the frozen LLM's text-space structure.

## Links

- [Parameter Efficient AC](parameter-efficient-ac-2024.md)
- [Prefix Tuning for AAC](prefix-tuning-aac-2023.md)
