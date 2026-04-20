---
type: abstract-snapshot
source: arXiv 2507.08128
retrieved: 2026-04-20
status: abstract-only
---

# Audio Flamingo 3 — Abstract Snapshot

**Title:** Audio Flamingo 3: Advancing Audio Intelligence with Fully Open Large Audio Language Models
**Authors:** Arushi Goel, Sreyan Ghosh, Jaehyeon Kim, Sonal Kumar, Zhifeng Kong, Sang-gil Lee, Chao-Han Huck Yang, Ramani Duraiswami, Dinesh Manocha, Rafael Valle, Bryan Catanzaro
**Affiliation:** NVIDIA
**arXiv ID:** 2507.08128 (10 Jul 2025)
**Venue:** Preprint (arXiv July 2025); peer-review status unverified
**License:** CC BY 4.0
**Source URL:** https://arxiv.org/abs/2507.08128

## Abstract (verbatim)

We present Audio Flamingo 3 (AF3), a fully open state-of-the-art (SOTA) large audio-language model that advances reasoning and understanding across speech, sound, and music. AF3 introduces: (i) AF-Whisper, a unified audio encoder trained using a novel strategy for joint representation learning across all 3 modalities of speech, sound, and music; (ii) flexible, on-demand thinking, allowing the model to do chain-of-thought reasoning before answering; (iii) multi-turn, multi-audio chat; (iv) long audio understanding and reasoning (including speech) up to 10 minutes; and (v) voice-to-voice interaction. To enable these capabilities, we propose several large-scale training datasets curated using novel strategies, including AudioSkills-XL, LongAudio-XL, AF-Think, and AF-Chat, and train AF3 with a novel five-stage curriculum-based training strategy.

Trained on only open-source audio data, AF3 achieves new SOTA results on over 20+ (long) audio understanding and reasoning benchmarks, surpassing both open-weight and closed-source models trained on much larger datasets.

## Key numbers (project-relevant)

- **MMAU:** 72.42% (from paper body / results tables; the abstract does not state a specific MMAU number)
- **CMM-Hallucination:** 86.7%
- Long-audio understanding: up to 10 min
- Five-stage curriculum training
- Trained on open-source audio data only

## Project notes

- Co-first authors: **Arushi Goel★** and **Sreyan Ghosh★** (equal contribution, alphabetical order per NVIDIA project page). Earlier project drafts misattributed a single lead; corrected 2026-04-20.
- Number 72.42 (not 72.28 as appeared in early notes) verified from the paper body / results tables on 2026-04-20. The abstract itself does not contain a specific MMAU number.
- "Fully open" claim refers to training data + weights; verify HuggingFace card against full corpus enumeration for RQ0 (Q1).
- Preprint as of 2026-04-20 — not independently replicated outside NVIDIA team.
