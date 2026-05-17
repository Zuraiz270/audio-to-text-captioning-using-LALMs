---
title: "Lecture 04 — Data in Machine Listening (Course Material)"
type: project
status: active
created: 2026-05-13
updated: 2026-05-13
source_ids: []
source_files: [raw/00_course/CH-Proj-M-04-Audio_Datasets_Editing_Annotation.pdf]
source_tier: tier-b
canonical_url:
tags: [course, lecture, data-strategy, p2, fair, gsp, licences, weak-strong-labels]
---

# Lecture 04 — Data in Machine Listening

## Purpose

Canonical course material delivered by Prof. Dr.-Ing. Jakob Abeßer in CH-Proj-M (SS 2026), Lecture 04 (file `04 – Data in Machine Listening`). Defines the **required structure of the P2 presentation** (Data Acquisition Strategy, 2026-05-18) and introduces the vocabulary the prof expects students to use when discussing datasets: device mismatch, augmentation, transfer learning, weak vs. strong annotation, FAIR data, Good Scientific Practice (GSP) and data leakage, Creative Commons / MIT licences, license splitting, Privacy-Enhancing Technologies (PETs).

(Source: raw/00_course/CH-Proj-M-04-Audio_Datasets_Editing_Annotation.pdf, 19 slides, delivered by Prof. Abeßer)

## Key Points

### Audio is a "data-scarce" domain (slides 3–5)

- Paradigm shift: earlier knowledge-driven (features + classifiers) → today data-driven (DL).
- DL methods are data-hungry, but audio is harder to scrape than text/images, slower and more expensive to annotate (labels require listening in real-time), and carries privacy risks (strict regulations create legal hurdles).
- **Scale gap vs. other domains**:
  - NLP — Common Crawl / C4: trillions of tokens.
  - Vision — ImageNet-21K / LAION: 14M to 5B+ images.
  - Audio — LibriSpeech / AudioSet: 1,000 hours speech / 2M clips.

### Device mismatch (slides 6–7)

- High-quality devices (studio mics like RØDE NTSF1) produce one kind of recording.
- Low-quality devices (MEMS microphones in cell phones) produce systematically different audio.
- Mismatch between training-time and deployment-time devices is a known generalisation hazard. **Direct implication for our project**: Clotho is FreeSound-sourced ⇒ heterogeneous recording devices ⇒ device mismatch is a *built-in caveat* of the corpus.

### Approaches against data scarcity (slides 8–9)

- **Data augmentation** — e.g., Python lib `audiomentations`.
- **Transfer learning** — re-using pretrained representations.

Both apply at *training time*. **Out of scope for our zero-shot evaluation project**, but worth knowing for term-paper framing.

### Types of annotations (slide 10)

- **Weak labels** — clip-level (audio tagging, AT). One label per whole clip.
- **Strong labels** — segment-level with start/end times (sound event detection, SED).
- DCASE Task 1 (acoustic scene classification) is weak; DCASE Task 4 (SED) is strong.
- **Clotho is weak** (one set of captions per clip, no temporal grounding). Our polyphony split derives pseudo-strong labels via PaSST/PANNs SED.

### Open data principles (slide 11)

- **Reproducibility** — standardised pre-processing pipelines, model architectures, training logs.
- **FAIR data** — Findable, Accessible, Interoperable, Reusable.
- **Good Scientific Practice (GSP)** — strict integrity in data handling. *Explicit example given: avoiding "data leakage" in train/test splits.* This is the prof's own vocabulary for the contamination audit we run on slide 5 of P2.

### Data protection / PETs (slide 12)

- Audio = personal data: speech contains biometric identifiers + PII.
- **Privacy-Enhancing Technologies (PETs)**:
  - Audio pseudonymisation (pitch shifting / voice masking)
  - Differential privacy to prevent speaker re-identification from latent space
- "Privacy-by-design" approaches.
- *Direct implication*: not a P2 concern for us (Clotho contains no speech; the original Clotho paper post-processed annotations to remove speech transcription, per Drossos+ 2020). Would apply only if we recorded our own data.

### Licences (slides 13–14)

- Creative Commons family:
  - **CC0** — Public domain dedication, no rights reserved.
  - **CC-BY** — Attribution required (standard for open science).
  - **CC-BY-NC** — Non-commercial only.
  - **CC-BY-SA** — Share-alike (derivatives must use same licence).
- **MIT licence** — permissive software licence, "gold standard" for scripts, scrapers, processing code.
- **License splitting** — dual-licence: CC-BY on the raw `.wav` files, MIT on the training/evaluation code.
- *Direct implication*: Clotho is released under **CC-BY 4.0** on Zenodo (record 4783391). Fully FAIR-compliant. Our P2 deck must name this explicitly on slide 1.

### Tools (slides 15–16)

- **Sonic Visualiser** — annotation tool.
- **Audacity** — audio editing tool.

Not P2-deck content, but useful if asked in Q&A about how strong labels are produced.

## P2 Required Structure (verbatim from slide 17)

> **5 min presentation, 5 min Q/A**
> **Dataset(s) description**:
> - Metadata, data acquisition strategy (how recorded? which mics?)
> - Which classes?, #examples/class
> - Sample rate, audio format, file duration
> - Annotation (type of annotation, weak/strong)
> - Audio examples + Spectrogram examples — `librosa.stft`
> - All team members shall present!

(Note: this project is solo per registration, so presenter = author.)

## Implications for our P2 deck

| Lecture concept | Where it appears in P2 |
|:---|:---|
| Device mismatch | Slide 2 — heterogeneous FreeSound mic profile is the honest answer to "which mics?" |
| Data scarcity scale gap | Slide 1 framing — *why* test-set choice matters when training corpora are so much smaller than NLP/vision counterparts |
| Augmentation / transfer learning | Q&A only — out of scope for zero-shot evaluation |
| Weak vs. strong labels | Slide 3 — Clotho is explicitly *weak*; slide 4 derives pseudo-strong labels via SED |
| FAIR data | Slide 1 — Zenodo DOI + CC-BY 4.0 badge |
| GSP / data leakage | Slide 5 — the prof's own term for the contamination audit |
| PETs | Q&A only — not relevant to Clotho |
| Licences | Slide 1 — CC-BY 4.0 badge; Step 3 code released MIT (license splitting per lecture) |
| `librosa.stft` | Slides 3 + 4 — log-mel spectrograms; `spectrogram_demo.py` honours the exact tool name |

## Open Questions

- Should Step 3 (pipeline) code formally adopt the dual-licence pattern (MIT for code + CC-BY for any redistributed audio)? Probably yes — flag for confirmation at P3.

## Links

- [P1 speaker script (style anchor)](../../../deliverables/p1/p1_speaker_script.md)
- [Clotho v2.1 dataset note](../04_datasets/clotho-v21.md)
- [RQ0 — Contamination](../02_research_questions/rq0-contamination.md)
- [RQ2 — Polyphony](../02_research_questions/rq2-polyphony.md)
- [Data Leakage Benchmark 2026 (audit methodology anchor)](../04_datasets/data-leakage-benchmark-2026.md)
- [ALM Datasets Survey 2025 (zero-shot illusion framing)](../04_datasets/alm-datasets-survey-2025.md)
