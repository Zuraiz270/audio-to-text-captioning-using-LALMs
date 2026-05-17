---
title: Glossary
type: glossary
status: active
created: 2026-04-21
updated: 2026-05-13
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
| **Falcon3-Audio** | Primary LALM under evaluation. IEEE ASRU 2025, doc 11434596. Single-stage training on fully-public data, so its training manifest can be audited for contamination. |
| **Audio Flamingo (2/3/Next)** | NVIDIA cross-attention LALM family. *Historical architectural context only* — not a primary target per PROJECT_GUIDE.md. |
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
| **FAIR data** | Findable, Accessible, Interoperable, Reusable. Open-data principle from Lecture 04 — Clotho v2.1 on Zenodo with a DOI + CC-BY 4.0 satisfies all four. |
| **GSP** | Good Scientific Practice. Lecture 04 names it specifically to mean strict integrity in data handling, *e.g.* avoiding "data leakage" between train/test splits. The vocabulary anchor for our contamination audit. |
| **Data leakage** | Train/test contamination — a clip (or a near-duplicate, an "augmented twin") appears in both. Empirical proof + audit methodology in [data-leakage-benchmark-2026.md](../04_datasets/data-leakage-benchmark-2026.md). |
| **Weak labels** | Clip-level annotation with no time-stamps (audio tagging-style). Clotho's captions are weak labels — they describe the whole 15–30 s clip without saying *when* events happen. |
| **Strong labels** | Segment-level annotation with start/end times (sound event detection-style). DCASE Task 4 corpora use strong labels; we *derive* pseudo-strong labels via PaSST/PANNs SED on Clotho dev for the polyphony split. |
| **Device mismatch** | Systematic acoustic difference between recording devices (studio mics vs. MEMS phones). Lecture 04 calls it out as a generalisation hazard; Clotho inherits it because FreeSound contributors use varied gear. |
| **PETs** | Privacy-Enhancing Technologies. Lecture 04 examples: audio pseudonymisation (pitch shift, voice masking), differential privacy against speaker re-identification, "privacy-by-design". Not relevant to Clotho (no speech retained). |
| **CC-BY 4.0** | Creative Commons Attribution 4.0 — requires credit to the original creator. Clotho v2.1's licence. Per Lecture 04 the standard for open-science datasets. |
| **MIT licence** | Permissive software licence — Lecture 04's "gold standard" for scripts, scrapers, processing code. We will release `figures.py` / `spectrogram_demo.py` under MIT. |
| **License splitting** | Dual-licence pattern: CC-BY on raw audio data + MIT on code. Recommended in Lecture 04 slide 14. |
| **Audiomentations** | Python data-augmentation library named in Lecture 04 slide 8. *Out of scope for this project* (zero-shot eval, no training). |
| **`librosa.stft`** | Short-time Fourier transform function in `librosa`. Lecture 04 slide 17 names it explicitly as the tool to use for P2's spectrogram examples. We use it with `n_fft=1024`, `hop=512`, then log-mel-spectrogram + power_to_db. |
