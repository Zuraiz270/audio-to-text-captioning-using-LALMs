---
title: "Reducing Object Hallucination in Large Audio-Language Models via Audio-Aware Decoding"
type: source-note
status: active
created: 2026-04-21
updated: 2026-04-22
source_ids: [IEEE-11434595]
source_files: [raw/01_primary_sources/Reducing_Object_Hallucination_in_Large_Audio-Language_Models_via_Audio-Aware_Decoding.pdf]
source_tier: tier-b
canonical_url: https://ieeexplore.ieee.org/document/11434595
tags: [source-note, matrix-section-6, hallucination, contrastive-decoding, inference-time, rq3]
---

# Reducing Object Hallucination in Large Audio-Language Models via Audio-Aware Decoding

| Field | Value |
|:---|:---|
| **Year** | 2025 |
| **Venue** | IEEE ASRU 2025, pp. 7 pages |
| **Source ID** | IEEE-11434595 |
| **URL** | https://ieeexplore.ieee.org/document/11434595 |
| **Matrix Section** | 6 — Failure Modes & Mitigation |
| **Downloaded via** | Universität Bamberg institutional access |

## Abstract Summary

Introduces **Audio-Aware Decoding (AAD)** — a contrastive decoding method for LALMs that reduces object hallucination at inference time without retraining. At each decoding step, compares token probabilities **with** and **without** audio context (blank audio), amplifying tokens whose probability increases with audio. Tested on SALMONN-7B, SALMONN-13B, and Qwen2-Audio-7B.

(Source: Full PDF, IEEE-11434595)

## Method: Audio-Aware Decoding (AAD)

**Core equation:**

```
p_AAD(t) = softmax[ (1+α) · logit_with_audio(t) − α · logit_without_audio(t) ]
```

- `logit_with_audio`: standard LALM output with actual audio input A
- `logit_without_audio`: LALM output with **blank audio** (all-zero audio of same length)
- `α`: hyperparameter controlling emphasis on audio context vs. model prior

**Intuition:** Tokens that become substantially more likely when audio is presented are promoted. This steers the model toward audio-grounded outputs rather than text-prior hallucination.

**Key design choices:**
- No retraining required — inference-time only
- Prefix prompt: "Focus on the given audio and answer the following question"
- Blank audio = all zeros, same length as input

## Results (Exact)

### Audio Hallucination QA Dataset

| Model | Method | Random F1 | Adversarial F1 | Popular F1 | Clotho-AQA F1 | Average F1 |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| SALMONN-7B | Default | 0.233 | 0.177 | 0.229 | 0.746 | 0.346 |
| SALMONN-7B | Prompt | 0.564 | 0.324 | 0.464 | 0.772 | 0.531 |
| SALMONN-7B | **AAD α=0.5** | **0.661** | **0.416** | **0.540** | 0.790 | **0.602** |
| SALMONN-7B | **AAD α=1.0** | **0.737** | **0.456** | **0.562** | 0.753 | **0.627** |
| SALMONN-13B | Default | 0.384 | 0.275 | 0.393 | 0.737 | 0.447 |
| SALMONN-13B | **AAD α=1.0** | **0.676** | **0.356** | **0.469** | 0.801 | **0.575** |
| Qwen2-Audio-7B | Default | 0.302 | 0.247 | 0.298 | 0.778 | 0.406 |
| Qwen2-Audio-7B | **AAD α=1.0** | **0.737** | **0.435** | **0.506** | 0.821 | **0.624** |

**Key findings:**
- AAD improves F1 from 0.046 to 0.428 across models and subsets.
- Clotho-AQA improvements: 5.4% to 10.3%.
- Works on both SALMONN (7B, 13B) and Qwen2-Audio architectures.
- α=1.0 generally best for hallucination reduction.
- Adversarial sampling is hardest — objects frequently co-occur with true objects.

## Models Tested

- **SALMONN-7B** (Whisper + BEATs + Vicuna-7B)
- **SALMONN-13B** (Whisper + BEATs + Vicuna-13B)
- **Qwen2-Audio-7B-Instruct**

## Datasets Used

- Audio Hallucination QA (from previous work, 3 sampling strategies: random, adversarial, popular)
- Clotho-AQA (audio QA dataset, not designed for hallucination eval but shows improvements)

## Relevance to RQs

- **RQ3 (Hallucination):** ★★★ Direct — THE go-to mitigation paper. Proves hallucination is caused by text-prior over-reliance.
- **RQ1 (Baseline Parity):** AAD could be applied to AF3's inference for fair Clotho evaluation.
- **Architecture:** Demonstrates that hallucination is a decoding problem, not an encoding problem.

## Critical Insight for This Project

The paper proves that **object hallucination in LALMs is a text-prior problem**: models generate tokens based on training statistics rather than audio content. This directly validates the "text prior" hypothesis in RQ3. The causal mechanism:

1. Model sees audio with bird sounds
2. Training data has frequent co-occurrence of "bird" + "dog" 
3. Without AAD: model hallucinates "dog barking" because text prior dominates
4. With AAD: contrastive decoding amplifies audio-grounded tokens

## Limitations / Gotchas

- Tested on yes/no QA, not open-ended captioning.
- α hyperparameter needs per-model tuning.
- 2x inference cost (two forward passes per step).
- Doesn't address temporal hallucination — only object-level.

## Links

- [RQ3: Hallucination](../02_research_questions/rq3-hallucination.md)
- [Entity Hallucination](../06_failure_modes/entity-hallucination.md)
- [FD-DeCap](fd-decap-2025.md)
- [SALMONN](../03_models/salmonn.md)
- [CLAIRA](claira-2026.md)
