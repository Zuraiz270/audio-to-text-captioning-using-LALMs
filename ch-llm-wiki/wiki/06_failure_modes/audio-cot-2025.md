---
title: "Audio-CoT: Exploring Chain-of-Thought Reasoning in Large Audio Language Model"
type: source-note
status: active
created: 2026-04-21
updated: 2026-04-22
source_ids: [IEEE-11434628]
source_files: [raw/01_primary_sources/Audio-CoT_Exploring_Chain-of-Thought_Reasoning_in_Large_Audio_Language_Model.pdf]
source_tier: tier-b
canonical_url: https://ieeexplore.ieee.org/document/11434628/
tags: [source-note, matrix-section-3, reasoning, chain-of-thought, hallucination, mitigation]
---

# Audio-CoT: Exploring Chain-of-Thought Reasoning in Large Audio Language Model

| Field | Value |
|:---|:---|
| **Year** | 2025 |
| **Venue** | IEEE ASRU 2025 |
| **Source ID** | IEEE-11434628 |
| **URL** | https://ieeexplore.ieee.org/document/11434628/ |
| **Matrix Section** | 3 — Reasoning & Hallucination Mitigation |
| **Downloaded via** | Universität Bamberg institutional access |

## Abstract Summary

First systemic exploration of Chain-of-Thought (CoT) reasoning for auditory modalities in LALMs. Compares Manual-CoT, Zero-Shot-CoT, and Desp-CoT. Finds that CoT significantly helps on easy/medium acoustic reasoning tasks but struggles with hard tasks where the "thoughts" confuse the model.

(Source: Full PDF, IEEE-11434628)

## Key Findings

- **Methodologies Tested:**
  1. Manual-CoT (few-shot with explicit reasoning paths)
  2. Zero-Shot-CoT (adding "Let's think step by step")
  3. Desp-CoT (generating a description of audio first, then reasoning)
- **Positive Correlation:** Longer reasoning paths generally correlate with higher accuracy on general multi-modal benchmarks.
- **The "Hard Task" Fallacy:** For highly complex or heavily polyphonic audio, forcing the model to generate a reasoning chain often breaks its attention, causing it to hallucinate intermediate steps and ultimately predict the wrong answer.
- **Self-Consistency:** Marginalizing over multiple reasoning paths (generating 5 CoTs and taking the majority vote) significantly improves robustness.

## Relevance to RQs

- **RQ3 (Hallucination):** ★★★ CoT is a primary strategy for reducing hallucination. By comparing Desp-CoT (Describe audio -> classify/caption) vs direct end-to-end, we can see if forcing LALMs to be explicit about what components they hear prevents object hallucination.
- **RQ2 (Polyphony):** If a model adopts CoT, does it describe concurrent sounds sequentially, or does the sequential nature of LLMs inherently bottleneck concurrent acoustic representations?

## Links

- [Reducing Hallucination via Audio-Aware Decoding](reducing-hallucination-2026.md)
- [Omni-R1 (RLHF for Reasoning)](omni-r1-2025.md)
