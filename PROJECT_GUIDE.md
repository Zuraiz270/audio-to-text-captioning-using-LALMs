# Audio-to-Text Captioning using LALMs — Project Guide

*Master's Project · CH-Proj-M · SS 2026 · Zuraiz (2177213)*
*Prof. Dr.-Ing. Jakob Abeßer · Computational Humanities · Uni Bamberg*
*Last updated: April 2026*

---

## Executive Summary

This semester project investigates whether current state-of-the-art Large Audio-Language Models (LALMs) can accurately describe **overlapping sound events (polyphony)** compared to traditional audio tagging baselines. The primary evaluation targets all available LALMs — including **Falcon3-Audio**, **SALMONN**, and **Qwen2.5-Omni** — benchmarked against multiple traditional models like the DCASE CNN14 and EnCLAP on Clotho v2.1. 

The project delivers three graded presentations and a Term Paper, grounded in a fully mapped 49-paper evidence matrix.

---

## Problem Statement

**What is audio captioning?** Automated Audio Captioning (AAC) translates a raw audio waveform into a free-text natural-language description. Unlike audio tagging (`{dog, traffic, wind}`), captioning produces grammatical sentences encoding event identities, spatial cues, and temporal relations: *"A dog barks in the distance as cars pass on a wet road while wind rustles nearby leaves."*

**What is the core problem?** When multiple sound events overlap in the same audio clip (polyphony), current state-of-the-art LALMs tend to under-describe the scene, hallucinate entities not present, or default to text-prior biases. The course assignment (T6) explicitly asks us to evaluate this failure mode compared to traditional systems.

---

## Research Questions

| RQ | Question | Primary Metric |
|:---|:---------|:-------|
| **RQ1** | Do LALMs match or exceed traditional tagging baselines on standard captioning metrics? | SPIDEr-FL, CIDEr |
| **RQ2 (Core)** | **How accurately can LALMs describe overlapping sound events compared to traditional tagging?** | Δ MACE (polyphony subset − monophony subset) |
| **RQ3** | What is the entity hallucination rate of LALMs on polyphonic audio? | CHAIR-audio / MACE Precision |

---

## Models Under Evaluation

We utilize all available baseline paradigms and State-of-the-Art LALMs, utilizing pre-trained weights to avoid training costs.

### The Traditional Baselines
| Model | Type | Reason for Evaluation |
|:------|:-----|:-------|
| **CNN14 (DCASE 2024 Baseline)** | Supervised Tagging/Encoder | The official IEEE/DCASE gold standard for tagging parity. |
| **AST (Audio Spectrogram Transformer)**| Transformers Tagging | SOTA pure-audio attention architecture. |
| **EnCLAP (2024)** | Non-LLM CAP | Bleeding-edge contrastive audio-text without an LLM decoder footprint. |

### The SOTA LALMs
| Model | Source | Reason for Evaluation |
|:------|:-------|:-------|
| **Falcon3-Audio (2026)** | IEEE ICASSP (Peer-reviewed) | Primary model (Clean public data, single-stage). |
| **SALMONN (2024)** | ArXiv | Widely surveyed baseline standard. |
| **Qwen2.5-Omni (2026)** | ArXiv | Bleeding-edge multi-modal integration. |

*(Note: Audio Flamingo models are retained purely as historical architectural context, not as primary targets).*

---

## 4-Step Evidence Execution Matrix

The project leverages exactly 49 pieces of verified literature, logically divided across the four operational blocks of the course timeline.

### Step 1: Literature Review & State of the Art [15%]
**Deliverable**: P1 Presentation (May 4th).
**Purpose**: Establish the historical context of AAC and introduce the SOTA models.
**Presentation Strategy (5 Minutes)**:
- *The Broad Sweep (1 Min)*: Present a single-slide taxonomy of the entire 49-paper corpus to prove academic rigor.
- *The Deep Dive (4 Min)*: Focus heavily on the architectural evolution to justify our chosen baselines. 
**Deep-Dive Literature**:
- *Historical Context Models*: `audio-flamingo-2.md`, `audio-flamingo-3.md`, `audio-flamingo-next.md`, `acoustic-prompt-tuning-2025.md`.
- *Comparison Context*: `clapscore-vs-spider.md`.

### Step 2: Data Strategy [15%]
**Deliverable**: P2 Presentation (May 18th).
**Purpose**: Defend the dataset selection (Clotho) and define the Polyphony isolation strategies and Contamination/Leakage risks.
**Leveraged Literature**:
- *Dataset & Leakage Evidences*: `alm-datasets-survey-2025.md`, `data-leakage-benchmark-2026.md`, `audiocaps.md`, `audiopedia-2025.md`, `audiosetcaps-2024.md`, `cacophony-2024.md`, `clotho-v21.md`, `clotho.md`, `clotho-aqa.md`, `wavcaps-2024.md`, `improving-aac-mixup-2024.md`.

### Step 3: Code Architecture & Implementation [Ungraded Milestone]
**Deliverable**: Early June Pipeline Construction.
**Purpose**: Implementing the evaluation loop, calculating SPIDEr-FL and MACE.
**Leveraged Literature**:
- *Metric Validation*: `mace-2025.md`, `spider-fl.md`, `beyond-status-quo-2023.md`, `cat-plus-2025.md`, `claira-2026.md`, `clapscore.md`.
- *Target Model Architecture Logic*: `falcon3-audio-2026.md`, `salmonn.md`, `qwen25-omni.md`, `enclap-2024.md`, `conette-2024.md`, `openbeats-2025.md`.

### Step 4: The Term Paper & Final Defense [35% + 35%]
**Deliverable**: July 6th Term Paper Submit and July 13th Defense.
**Purpose**: Reviewing literature to scientifically explain *why* LALMs fail at polyphony and how hallucination occurs.
**Leveraged Literature**:
- *Polyphony & Hallucination Diagnostics*: `omni-r1-2025.md`, `audio-cot-2025.md`, `audio-cot-2026.md`, `entity-hallucination.md`, `polyphony-under-description.md`, `reducing-hallucination-2026.md`, `distillcaps-2024.md`, `fd-decap-2025.md`, `rag-low-resource-2025.md`, `temporal-grounding-loss.md`, `training-without-audio-2024.md`.
- *Alternative Mitigation Strategies*: `crab-av-2025.md`, `desta25-audio-2026.md`, `extending-llms-aac-2024.md`, `lavcap-2025.md`, `parameter-efficient-ac-2024.md`, `prefix-tuning-aac-2023.md`, `recap-2024.md`, `slam-llm-2025.md`, `transfer-learning-aac-2025.md`, `sed-review-2025.md`.

*(The first priority for all decisions falls to IEEE/ACM papers, with ArXiv utilized only as worst-case gap fillers).*

---

## Grading Structure & Deliverables

| Deliverable | Date | Weight | Content |
|:------------|:-----|:-------|:--------|
| **P1** | 04.05.2026 | **15%** | Topic definition + Literature review (5 min + 5 min Q/A) |
| **P2** | 18.05.2026 | **15%** | Dataset / data acquisition strategy (5 min + 5 min Q/A) |
| **Term Paper** | 06.07.2026 | **35%** | 4–6 pages, structure & requirements per course spec |
| **P3** | 13.07.2026 | **35%** | Final project presentation (10 min + 5 min Q/A) |

---

## Glossary & Metrics

| Term | Definition |
|:-----|:-----------|
| **AAC** | Automated Audio Captioning — outputs free-text descriptions of audio recordings. |
| **CHAIR-audio** | Counts entities in a caption not grounded in the audio. Adapted from image captioning. |
| **Clotho v2.1** | Canonical AAC evaluation benchmark. 6,974 FreeSound clips, 5 human captions each. |
| **DCASE** | Detection and Classification of Acoustic Scenes and Events. Task 6 = audio captioning. |
| **LALM** | Large Audio-Language Model. An LLM augmented with an audio encoder for audio understanding. |
| **MACE** | Metric for evaluating Audio Captioning Entities. Measures entity-level precision/recall. |
| **Polyphony** | Multiple sound events occurring simultaneously in the same audio clip. |
| **SPIDEr-FL** | Official DCASE 2024 metric. `(SPICE + CIDEr) / 2 × Fluency_Error_Penalty`. |
