---
title: Glossary
type: glossary
status: seed
created: 2026-04-21
updated: 2026-04-21
source_ids: []
source_files: [PROJECT_GUIDE.md]
source_tier: mixed
canonical_url:
tags: [glossary, definitions]
---

# Glossary

| Term | Definition |
|:---|:---|
| **AAC** | Automated Audio Captioning — inter-modal translation from raw audio waveform to free-text natural-language description. |
| **LALM** | Large Audio-Language Model — combines a pre-trained audio encoder, a lightweight adapter, and an LLM decoder. |
| **Clotho v2.1** | Canonical AAC benchmark dataset. Freesound audio clips with crowd-sourced captions. |
| **AudioCaps** | AAC dataset derived from AudioSet 10-second clips with human-written captions. |
| **Audio Flamingo 3** | Primary model under evaluation. NVIDIA, Jul 2025. Claims emergent zero-shot captioning. |
| **SALMONN** | Secondary comparison LALM. Dual encoder (Whisper + BEATs) + Q-Former + LLM. |
| **Qwen2.5-Omni** | Secondary comparison model. General-purpose multimodal LLM (Alibaba). |
| **SPIDEr-FL** | Primary captioning metric. (SPICE + CIDEr) / 2 with fluency penalty. |
| **CLAPScore** | Reference-free metric. Cosine similarity between audio and text embeddings in CLAP space. |
| **FENSE** | Fluency ENhanced Sentence-level Evaluation. Adds fluency penalty to sentence embeddings. |
| **Polyphony** | Multiple simultaneous sound events in a single audio clip. |
| **Entity hallucination** | Model fabricates sound events not present in the audio, driven by LLM text priors. |
| **Temporal grounding** | Preserving the true chronological order of sound events in the generated caption. |
| **Ekphrasis** | Classical rhetorical genre of verbal description of non-verbal aesthetic experience. |
| **Soundscape** | The acoustic environment as perceived by humans. Term from R. Murray Schafer (1977). |
| **Soundmark** | Culturally-specific, geographically-anchored sound (e.g., specific church bells). Schafer's term. |
| **Accessibility** | In this project: enabling BLV users to access sound collections via text captions. |
| **Cultural heritage audio** | Recordings in archives (British Library, BBC, Europeana) that lack textual description layers. |
| **Q-Former** | Querying Transformer — lightweight adapter bridging encoder and LLM in multimodal architectures. |
| **BCa** | Bias-corrected and accelerated bootstrap — statistical method for confidence intervals. |
| **CHAIR** | Caption Hallucination Assessment with Image Relevance — hallucination metric adapted from vision. |
| **PEFT** | Parameter-Efficient Fine-Tuning — methods like LoRA, prefix tuning, adapters. |
| **RAG** | Retrieval-Augmented Generation — augmenting LLM output with retrieved external knowledge. |
| **SED** | Sound Event Detection — identifying and localising sound events in audio recordings. |
| **DCASE** | Detection and Classification of Acoustic Scenes and Events — annual challenge and workshop. |
