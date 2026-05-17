---
title: Clotho v2.1
type: dataset
status: active
created: 2026-04-21
updated: 2026-05-13
source_ids: [ICASSP-2020-Drossos-Clotho]
source_files: [raw/01_primary_sources/clotho.pdf]
source_tier: mixed
canonical_url: https://zenodo.org/record/4783391
tags: [dataset, clotho, primary, evaluation, p2, freesound, cc-by-4.0]
---

# Clotho v2.1

## Purpose

Primary evaluation dataset for all RQs in this project. Canonical AAC benchmark from DCASE Task 6.

## Key Points

### Origin and acquisition

- **Source**: [Freesound](https://freesound.org/) audio clips, uploaded by community contributors.
- **Curators**: Drossos, Lipping, Virtanen at Tampere University Audio Research Group.
- **Captions crowdsourced** via Amazon Mechanical Turk from English-speaking annotators.
- **No original recording** by the dataset team — all audio is community-contributed, which means **heterogeneous recording devices** (mobile phones, field recorders, studio gear). This is the honest answer to the prof's "which mics?" question on the P2 brief: there is no single mic profile. Device mismatch (per Lecture 04 slides 6–7) is a built-in caveat of FreeSound-derived corpora.

### Audio properties

| Property | Value |
|:---|:---|
| Sample rate | 44.1 kHz |
| Channels | 1 (mono) |
| Bit depth | 16-bit |
| Format | WAV (PCM) |
| Clip duration | 15 to 30 seconds |
| Total clips (v2.1) | ~6,974 across development/validation/evaluation splits |
| Total captions | ~34,870 (5 captions × clips) |
| Vocabulary | open — no fixed class taxonomy |

(Values from Drossos+ 2020 abstract for v1; v2.1 adds the official DCASE evaluation split. Verify exact split sizes from `clotho_metadata_*.csv` after Step 0 download.)

### Annotation

- **Type**: **weak** — clip-level, no temporal grounding. (Per Lecture 04 slide 10 vocabulary: this is *audio tagging*-style annotation in scope, even though the captions are sentences.)
- **5 human-written captions per clip**.
- **8 to 20 words per caption**.
- AMT crowdworkers from English-speaking countries.
- Post-processing: removes unique words, named entities, and speech transcription — the dataset is *not* a speech corpus.

### Splits (DCASE 2024 Task 6 convention)

- **Development** (training) — bulk of clips.
- **Validation** (held-out tuning).
- **Evaluation** (test, used for scoring).

Exact counts confirmed from `clotho_metadata_*.csv` after local download.

### License and FAIR compliance

- **License**: CC-BY 4.0 (per Lecture 04 slide 13).
- **Zenodo record**: 4783391 (v2.1) — DOI assigned, fully **FAIR-compliant** (Findable: Zenodo DOI · Accessible: free direct download · Interoperable: standard WAV + CSV · Reusable: CC-BY 4.0).

## Justification over AudioCaps (P1 / P2 defence)

While AudioCaps is larger, Clotho v2.1 is strictly preferred for this project's evaluation due to:

1. **DCASE Baseline Parity (RQ1)**: Clotho is the canonical benchmark for DCASE Task 6. Using it ensures a direct, apples-to-apples comparison against the official CNN14 baseline (SPIDEr-FL ≈ 29.6%).
2. **Mitigating Data Leakage (RQ0)**: AudioCaps is built on AudioSet. Almost all LALMs are pre-trained on AudioSet, creating massive data contamination risks that invalidate zero-shot claims. Clotho (sourced from Freesound) provides a safer out-of-domain evaluation. **Empirical wedge**: FD-DeCap (IEEE TASLP 2025, doc 11333308) reports SPIDEr 0.282 on Clotho vs. 0.429 on AudioCaps — even with causal-inference debiasing, the contaminated corpus scores ~50% higher.
3. **Caption Density (RQ2 + RQ3)**: Clotho provides 5 human-written captions per clip (compared to 1 in the AudioCaps training set). This dense annotation is critical for evaluating polyphony under-description and hallucination accurately. The 5-caption union is our **`E_ref` set** in the under-description formula `card(E_model) < card(E_ref ∩ E_audio)`.

## P2 deck mapping

| Slide | Clotho fact used |
|:---|:---|
| Slide 1 | Zenodo DOI + CC-BY 4.0 badges; FAIR alignment per Lecture 04 |
| Slide 2 | Heterogeneous FreeSound mics → device mismatch (Lecture 04 slides 6–7) |
| Slide 3 | Audio properties table (sr · format · channels · duration · captions/clip · vocab · CC-BY · Zenodo); weak annotation type |
| Slide 4 | Top-20 AudioSet classes derived by SED tagging over dev split; mono vs. poly example panels with waveform + log-mel spectrogram |
| Slide 5 | Risk of LALM training-data contamination (Falcon3-Audio's manifest is public → file-ID audit possible; SALMONN / Qwen2.5-Omni → Chromaprint fingerprint + caption n-gram) |

## Evidence

- Drossos, Lipping, Virtanen — *Clotho: An Audio Captioning Dataset*, IEEE ICASSP 2020. Source: `raw/01_primary_sources/clotho.pdf`. Abstract extracts at [clotho.md](clotho.md).
- Zenodo record 4783391 — canonical distribution of v2.1.
- Lecture 04 (Prof. Abeßer) — *Data in Machine Listening*, CH-Proj-M SS 2026. Source: `raw/00_course/CH-Proj-M-04-Audio_Datasets_Editing_Annotation.pdf`.
- FD-DeCap — Dixit/Khare et al., IEEE TASLP 2025, doc 11333308. SPIDEr 0.282 (Clotho) vs. 0.429 (AudioCaps) reported. Source page: [fd-decap-2025.md](../06_failure_modes/fd-decap-2025.md).

## Open Questions

- Exact split counts and total v2.1 clip count — to be filled in after local `clotho_metadata_*.csv` is read post-download.
- Whether any Clotho clip IDs appear in Falcon3-Audio's published training manifest — the contamination audit (Step 5 of pipeline) will answer this.

## Links

- [Drossos+ 2020 abstract / paper notes](clotho.md)
- [AudioCaps (rejected corpus)](audiocaps.md)
- [ALM Datasets Survey 2025 — zero-shot illusion](alm-datasets-survey-2025.md)
- [Data Leakage Benchmark 2026 — audit methodology](data-leakage-benchmark-2026.md)
- [Lecture 04 — Data in Machine Listening](../01_project/lecture-04-data-in-machine-listening.md)
- [RQ0 — Contamination](../02_research_questions/rq0-contamination.md)
- [RQ2 — Polyphony](../02_research_questions/rq2-polyphony.md)
