---
title: "FD-DeCap: A Front-Door Causal Inference-Based Framework for Debiasing Automatic Audio Captioning"
type: source-note
status: draft
created: 2026-04-21
updated: 2026-04-21
source_ids: [IEEE-11333308]
source_files: []
source_tier: tier-a
canonical_url: https://ieeexplore.ieee.org/abstract/document/11333308/
tags: [source-note, matrix-section-4, causal-inference, debiasing, clotho, audiocaps]
---

# FD-DeCap: A Front-Door Causal Inference-Based Framework for Debiasing Automatic Audio Captioning

| Field | Value |
|:---|:---|
| **Year** | 2025 |
| **Venue** | IEEE/ACM Trans. Audio, Speech, and Language Processing, pp. 6029–6042 |
| **Source ID** | IEEE-11333308 |
| **URL** | https://ieeexplore.ieee.org/abstract/document/11333308/ |
| **Matrix Section** | 4 — Evaluation Metrics & Bias Mitigation |

## Abstract Summary

Addresses latent confounders and spurious co-occurrence patterns that cause bias in AAC. Proposes **FD-DeCap** using front-door causal inference with three components: (1) **AudioAug** — noise perturbation for robustness; (2) **MedGate** — explicit mediator variable satisfying front-door criterion to disentangle effects; (3) **MSeCE** — consistency loss optimizing cross-entropy + MSE to avoid spurious correlations. Achieves SPIDEr scores of **0.282 (Clotho)** and **0.429 (AudioCaps)**.

(Source: IEEE Xplore abstract, IEEE-11333308)

## Key Contributions

- First application of front-door causal inference to AAC.
- Breaks spurious audio-text correlations that drive hallucination.
- Reports concrete SPIDEr scores on Clotho (0.282) and AudioCaps (0.429).
- Multi-perspective causal validation with similarity distributions, feature analysis, case studies.
- After debiasing: generated captions shift closer to references, mediator features become more dispersed.

## Datasets Used

- Clotho (SPIDEr: 0.282)
- AudioCaps (SPIDEr: 0.429)

## Metrics Reported

- SPIDEr: 0.282 (Clotho), 0.429 (AudioCaps)

## Relevance to RQs

- **RQ3 (Hallucination):** Directly addresses the causal mechanism behind spurious co-occurrence hallucination.
- **RQ1 (Baseline Parity):** SPIDEr scores provide comparison baselines.
- **RQ0 (Contamination):** Highlights selection bias in dataset distributions.

## Limitations / Gotchas

- Front-door criterion requires specific structural assumptions about the causal graph.
- Mediator variable design is architecture-specific.

## Links

- [Entity Hallucination](../06_failure_modes/entity-hallucination.md)
- [RQ3: Hallucination](../02_research_questions/rq3-hallucination.md)
- [Reducing Hallucination](reducing-hallucination-2026.md)
- [CLAIRA](claira-2026.md)
