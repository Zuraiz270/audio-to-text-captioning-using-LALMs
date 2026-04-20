---
type: abstract-snapshot
source: arXiv 2503.20215
retrieved: 2026-04-20
status: abstract-only
---

# Qwen2.5-Omni — Abstract Snapshot

**Title:** Qwen2.5-Omni Technical Report
**Authors:** Qwen Team (Alibaba)
**arXiv ID:** 2503.20215 (26 Mar 2025)
**License:** CC BY 4.0
**Source URL:** https://arxiv.org/abs/2503.20215

## Abstract (verbatim, condensed)

In this report, we present Qwen2.5-Omni, an end-to-end multimodal model designed to perceive diverse modalities, including text, images, audio, and video, while simultaneously generating text and natural speech responses in a streaming manner. To enable the streaming of multimodal information inputs, both audio and visual encoders utilize a block-wise processing approach. To synchronize the timestamps of video inputs with audio, we organize the audio and video sequentially in an interleaved manner and propose a novel position embedding approach, named TMRoPE (Time-aligned Multimodal RoPE). To concurrently generate text and speech while avoiding interference between the two modalities, we propose Thinker-Talker architecture. In this framework, Thinker functions as a large language model tasked with text generation, while Talker is a dual-track autoregressive model that directly utilizes the hidden representations from the Thinker to produce audio tokens as output.

Qwen2.5-Omni performs competitively with similarly sized single-modality models and showcases state-of-the-art performance on benchmarks emphasizing fine-grained, multimodal understanding (Omni-Bench). Notably, Qwen2.5-Omni is the first open-source model to achieve a level of performance in end-to-end speech instruction following that is comparable to its capabilities with text inputs.

## Key architecture facts

- TMRoPE = Time-aligned Multimodal RoPE position embedding
- Thinker-Talker dual-track architecture
- Block-wise streaming encoders (audio + visual)
- End-to-end multimodal: text, image, audio, video → text + speech

## Project notes

- Comparator model alongside AF3 and SALMONN.
- Streaming + temporal alignment design relevant to RQ4 (temporal grounding).
- Prior wiki card was 33% dense; this snapshot enables ≥80% density refresh.
