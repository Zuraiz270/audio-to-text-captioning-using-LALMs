---
title: "EnCLAP: Combining Neural Audio Codec and Audio-Text Joint Embedding for Automated Audio Captioning"
type: source-note
status: draft
created: 2026-04-21
updated: 2026-04-21
source_ids: [IEEE-10446672]
source_files: []
source_tier: tier-a
canonical_url: https://ieeexplore.ieee.org/document/10446672/
tags: [source-note, matrix-section-2, enclap, encodec, clap, bart]
---

# EnCLAP: Combining Neural Audio Codec and Audio-Text Joint Embedding for Automated Audio Captioning

| Field | Value |
|:---|:---|
| **Year** | 2024 |
| **Venue** | IEEE ICASSP 2024 |
| **Source ID** | IEEE-10446672 |
| **URL** | https://ieeexplore.ieee.org/document/10446672/ |
| **Matrix Section** | 2 — Core LALM Architectures & Engines |

## Abstract Summary

Proposes **EnCLAP**: combines **EnCodec** (neural audio codec) + **CLAP** (audio-text joint embedding) + **BART** (pretrained language model). Introduces **masked codec modeling** training objective to improve acoustic awareness of the pretrained LM. Surpasses baselines on AudioCaps and Clotho.

(Source: IEEE Xplore abstract, IEEE-10446672)

## Key Contributions

- Dual-representation approach: EnCodec for acoustic fidelity + CLAP for semantic alignment.
- Masked codec modeling: novel training objective improving acoustic awareness.
- BART as language model backbone — not an LLM, but a pretrained encoder-decoder.
- SOTA on AudioCaps and Clotho at time of publication.
- Open-source code available.

## Datasets Used

- AudioCaps (training/evaluation)
- Clotho (training/evaluation)

## Metrics Reported

- Surpasses baselines on both AudioCaps and Clotho (specific scores in paper)

## Relevance to RQs

- **RQ1 (Baseline Parity):** Provides pre-LALM baseline with competitive scores on Clotho.
- **Architecture:** EnCodec + CLAP = alternative encoder paradigm to Whisper-only.

## Limitations / Gotchas

- BART is not an LLM — this is a generation before LALMs.
- Masked codec modeling may be architecture-specific.

## Links

- [Cacophony](cacophony-2024.md)
- [CLAPScore](../05_metrics/clapscore.md)
- [Clotho v2.1](../04_datasets/clotho-v21.md)
