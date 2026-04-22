---
title: "Competitive Audio-Language Models with Data-Efficient Single-Stage Training on Public Data"
type: source-note
status: active
created: 2026-04-21
updated: 2026-04-22
source_ids: [IEEE-11434596]
source_files: [raw/01_primary_sources/Competitive_Audio-Language_Models_with_Data-Efficient_Single-Stage_Training_on_Public_Data.pdf]
source_tier: tier-b
canonical_url: https://ieeexplore.ieee.org/document/11434596
tags: [source-note, matrix-section-2, falcon3-audio, single-stage, public-data, rq1, af3]
---

# Falcon3-Audio: Competitive Audio-Language Models with Data-Efficient Single-Stage Training on Public Data

| Field | Value |
|:---|:---|
| **Year** | 2025 |
| **Venue** | IEEE ASRU 2025, 7 pages |
| **Source ID** | IEEE-11434596 |
| **URL** | https://ieeexplore.ieee.org/document/11434596 |
| **Matrix Section** | 2 — Core LALM Architectures & Engines |
| **Downloaded via** | Universität Bamberg institutional access |

## Architecture

```
Audio → Whisper-large-v3 encoder → Linear projection → Falcon3 LLM (1B/3B/7B)
```

- **Audio encoder:** Whisper-large-v3 (frozen)
- **Projector:** Lightweight linear projection (no cross-attention, no complex fusion)
- **LLM backbone:** Falcon3 instruction-tuned (1B, 3B, 7B variants)
- **Training:** Single-stage end-to-end (no multi-stage curriculum)

## Key Design Decisions (from ablations)

1. **Base vs. Instruct LLM:** Instruction-tuned Falcon3 used as backbone
2. **Audio encoder choice:** Whisper-large-v3 selected over alternatives
3. **Sequence length:** Explored to find optimal balance
4. **Projection design:** Simple linear > complex MLP or cross-attention
5. **Data mixture:** Careful audio-type balancing (speech, environmental, music)

## Training Data

- **<30K hours** of public audio data only
- No proprietary data
- All datasets open-source and inspectable
- This is the **key differentiator** — most competitors use 500K+ hours of private data

## Results

- **MMAU benchmark:** Matches SOTA among open-weight models
- **AIR-Bench Foundational:** Strong performance
- **AIR-Bench Chat:** Strong performance
- Competitive with Qwen2-Audio-7B (which uses >500K hours of non-public data)

## Concurrent Works Comparison (from paper)

| Model | Data | Params | Stages | Public Data? |
|:---|:---|:---:|:---:|:---:|
| **Falcon3-Audio-7B** | <30K hrs | 7B | 1 | ✅ Yes |
| Qwen2-Audio | >500K hrs | 8.4B | Multi | ❌ No |
| Qwen2.5-Omni | Undisclosed | 10.7B | Multi | ❌ No |
| R1-AQA | 38K samples (fine-tune of Qwen2-Audio) | 8.4B | Multi+GRPO | ❌ No |
| Audio Flamingo 2 | Various | 3B | Cross-attn | Partial |
| Phi-4 Mini | 2M+ hrs private | 5.6B | Multi | ❌ No |

## Relevance to RQs

- **RQ1 (Baseline Parity):** ★★★ THE benchmark zero-shot model for Clotho evaluation. Simple, reproducible, public-data-only.
- **Data Leakage Context:** Public-data-only = audit-friendly. Training data is inspectable for Clotho overlap.
- **Architecture:** Proves that simple projection + single-stage training is sufficient — complexity is not the answer.

## Critical Insight for This Project

Falcon3-Audio is the ideal baseline for this project because:
1. All training data is public → contamination can be audited
2. Simple architecture → results are interpretable
3. Single-stage training → no confounding multi-stage effects
4. Competitive with 10x more data models → the "sufficient" baseline

## Limitations / Gotchas

- No AAC-specific evaluation reported (MMAU is QA, AIR-Bench is Chat/Foundational)
- Clotho captioning scores not in paper — would need to run inference
- 7B is still large for edge deployment

## Links

- [Audio Flamingo 3](../03_models/audio-flamingo-3.md)
- [SALMONN](../03_models/salmonn.md)
- [Qwen2.5-Omni](../03_models/qwen25-omni.md)
- [RQ1: Baseline Parity](../02_research_questions/rq1-baseline-parity.md)
- [AF3 vs DCASE](../09_comparisons/af3-vs-dcase.md)
- [SLAM-LLM](slam-llm-2025.md)

