---
type: abstract-snapshot
source: arXiv 2310.13289
retrieved: 2026-04-20
status: abstract-only
---

# SALMONN — Abstract Snapshot

**Title:** SALMONN: Towards Generic Hearing Abilities for Large Language Models
**Authors:** Changli Tang, Wenyi Yu, Guangzhi Sun, Xianzhao Chen, Tian Tan, Wei Li, Lu Lu, Zejun Ma, Chao Zhang
**Affiliation:** Tsinghua University, ByteDance
**arXiv ID:** 2310.13289 (20 Oct 2023, revised 2024)
**Venue:** ICLR 2024
**Source URL:** https://arxiv.org/abs/2310.13289

## Abstract (verbatim, condensed)

Hearing is arguably an essential ability of artificial intelligence (AI) agents in the physical world, which refers to the perception and understanding of general auditory information consisting of at least three types of sounds: speech, audio events, and music. In this paper, we propose SALMONN, a speech audio language music open neural network, built by integrating a pre-trained text-based large language model (LLM) with speech and audio encoders into a single multimodal model. SALMONN enables the LLM to directly process and understand general audio inputs and achieve competitive performances on a number of speech and audio tasks used in training, such as automatic speech recognition and translation, auditory-information-based question answering, emotion recognition, speaker verification, and music and audio captioning etc. SALMONN also has a diverse set of emergent abilities unseen in the training, which includes but is not limited to speech translation to untrained languages, speech-based slot filling, spoken-query-based question answering, audio-based storytelling, and speech audio co-reasoning etc. The presence of the cross-modal emergent abilities is studied, and a novel few-shot activation tuning approach is proposed to activate such abilities of SALMONN.

## Key architecture facts

- Dual-encoder design: Whisper (speech) + BEATs (audio events/music)
- Window-level Q-Former adapter to LLM
- Vicuna-13B as backbone LLM
- Activation tuning to recover emergent abilities

## Project notes

- Cited in literature_review.md §3 as architectural pillar (dual-encoder vs single-stream).
- Q-Former is the candidate adapter-layer bottleneck for polyphony (RQ2 hypothesis).
- Project softens "Q-Former cannot represent" → "is hypothesised to be unable" pending direct citation to AF3 architecture description.
