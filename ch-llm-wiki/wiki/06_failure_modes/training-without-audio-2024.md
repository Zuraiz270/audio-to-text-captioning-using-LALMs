---
title: "Training Audio Captioning Models without Audio"
type: source-note
status: draft
created: 2026-04-21
updated: 2026-04-21
source_ids: [IEEE-10448115]
source_files: []
source_tier: tier-a
canonical_url: https://ieeexplore.ieee.org/document/10448115/
tags: [source-note, matrix-section-3, text-only, contrastive, data-scarcity]
---

# Training Audio Captioning Models without Audio

| Field | Value |
|:---|:---|
| **Year** | 2024 |
| **Venue** | IEEE ICASSP 2024 |
| **Source ID** | IEEE-10448115 |
| **URL** | https://ieeexplore.ieee.org/document/10448115/ |
| **Matrix Section** | 3 — Alignment, Strategy & Fine-Tuning |

## Abstract Summary

Proposes training AAC systems using **only text** — no audio training data required. Leverages multimodal contrastive embedding spaces to bridge text training to audio inference. Addresses the critical **data scarcity** bottleneck: manual creation of audio-caption pairs is costly.

(Source: IEEE Xplore abstract, IEEE-10448115)

## Key Contributions

- Text-only training for AAC — radical approach to data scarcity.
- Uses contrastive multimodal spaces (e.g., CLAP) for cross-modal transfer.
- Eliminates need for manually curated audio-caption pairs during training.

## Datasets Used

<!-- To be confirmed on full PDF read -->

## Metrics Reported

<!-- To be confirmed on full PDF read -->

## Relevance to RQs

- **RQ0 (Contamination):** If models can train without audio, contamination manifests in text space only.
- **RQ3 (Hallucination):** Text-only training may amplify text prior hallucination.

## Limitations / Gotchas

- Models trained without audio may have weaker acoustic grounding.
- Relies heavily on quality of contrastive embeddings.

## Links

- [AudioSetCaps](audiosetcaps-2024.md)
- [RQ0: Contamination](../02_research_questions/rq0-contamination.md)
- [RQ3: Hallucination](../02_research_questions/rq3-hallucination.md)
