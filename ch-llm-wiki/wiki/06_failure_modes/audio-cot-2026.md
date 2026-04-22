---
title: "Audio-CoT: Exploring Chain-of-Thought Reasoning in Large Audio Language Model"
type: source-note
status: draft
created: 2026-04-21
updated: 2026-04-21
source_ids: [IEEE-11434628]
source_files: []
source_tier: tier-a
canonical_url: https://ieeexplore.ieee.org/document/11434628/
tags: [source-note, matrix-section-3, cot, reasoning, icassp-2025]
---

# Audio-CoT: Exploring Chain-of-Thought Reasoning in Large Audio Language Model

| Field | Value |
|:---|:---|
| **Year** | 2026 |
| **Venue** | ICASSP 2025, Honolulu, HI |
| **Source ID** | IEEE-11434628 |
| **URL** | https://ieeexplore.ieee.org/document/11434628/ |
| **Matrix Section** | 3 — Alignment, Strategy & Fine-Tuning |

## Abstract Summary

First exploration of Chain-of-Thought (CoT) reasoning in LALMs. Evaluates representative CoT methods across sound, music, and speech domains. Finds: CoT significantly improves easy/medium tasks but can **confuse the model on hard tasks**, where reasoning chains degrade rather than improve accuracy. Identifies positive correlation between reasoning path length and accuracy.

(Source: IEEE Xplore abstract, IEEE-11434628)

## Key Contributions

- First systematic study of CoT in audio LLMs (sound, music, speech).
- Demonstrates CoT improves performance on easy/medium tasks.
- Reveals a critical failure: CoT hurts hard tasks — reasoning chains confuse the model.
- Shows positive correlation between reasoning path length and accuracy.
- Provides inference-scaling perspective for audio modality.

## Datasets Used

<!-- To be confirmed on full PDF read — covers sound, music, speech domains -->

## Metrics Reported

<!-- Task-specific accuracy across difficulty levels -->

## Relevance to RQs

- **RQ2 (Polyphony):** CoT may help models enumerate concurrent events — or confuse them.
- **RQ3 (Hallucination):** Longer reasoning chains could either reduce or amplify hallucination.
- Methodological: directly competes with Omni-R1's RL approach.

## Limitations / Gotchas

- CoT hurts hard tasks — this is a significant caveat for complex AAC scenes.
- Not tested on captioning directly.

## Links

- [Omni-R1](omni-r1-2026.md)
- [RQ2: Polyphony](../02_research_questions/rq2-polyphony.md)
