# Wiki Index

Master table of contents for the CH-Proj-M LLM Wiki.

**Canonical source registry:** `Credible Literature/info.txt` (38 unique papers)
**Thematic mapping:** `Credible Literature/LALM_Synthesis_Matrix.md`
**Schema:** [CLAUDE.md](CLAUDE.md)
**Change log:** [log.md](log.md)

---

## 00 — Overview

- [README](wiki/00_overview/README.md) — Project summary and wiki navigation guide.

## 01 — Project

- [Scope](wiki/01_project/scope.md) — Task definition, in/out of scope, course-safe vs research-grade.
- [Phase Map](wiki/01_project/phase-map.md) — Execution phases and deliverable timeline.

## 02 — Research Questions

- [RQ0: Contamination Audit](wiki/02_research_questions/rq0-contamination.md)
- [RQ1: Baseline Parity](wiki/02_research_questions/rq1-baseline-parity.md)
- [RQ2: Polyphony](wiki/02_research_questions/rq2-polyphony.md)
- [RQ3: Hallucination](wiki/02_research_questions/rq3-hallucination.md)
- [RQ4: Temporal Grounding](wiki/02_research_questions/rq4-temporal.md)
- [RQ5: Cultural Bias](wiki/02_research_questions/rq5-cultural-bias.md)

## 03 — Models

- [Audio Flamingo 3](wiki/03_models/audio-flamingo-3.md) — Primary model.
- [SALMONN](wiki/03_models/salmonn.md) — Secondary model.
- [Qwen2.5-Omni](wiki/03_models/qwen25-omni.md) — Secondary model.

## 04 — Datasets

- [Clotho v2.1](wiki/04_datasets/clotho-v21.md) — Primary evaluation dataset.
- [AudioCaps](wiki/04_datasets/audiocaps.md) — Auxiliary dataset.

## 05 — Metrics

- [SPIDEr-FL](wiki/05_metrics/spider-fl.md) — Primary captioning metric.
- [CLAPScore](wiki/05_metrics/clapscore.md) — Reference-free metric.

## 06 — Failure Modes

- [Polyphony Under-Description](wiki/06_failure_modes/polyphony-under-description.md) — Failure mode 1.
- [Entity Hallucination](wiki/06_failure_modes/entity-hallucination.md) — Failure mode 2.
- [Temporal Grounding Loss](wiki/06_failure_modes/temporal-grounding-loss.md) — Failure mode 3.

## 07 — Humanities

- [Ekphrasis](wiki/07_humanities/ekphrasis.md) — Rhetorical tradition.
- [Soundscape Studies](wiki/07_humanities/soundscape-studies.md) — Acoustic ecology.
- [Accessibility & Archives](wiki/07_humanities/accessibility-archives.md) — Cultural heritage audio.

## 08 — Source Notes (38 papers)

### Section 1: Datasets, Encoders & Baselines
- [Beyond the Status Quo (2023)](wiki/08_sources/beyond-status-quo-2023.md)
- [Prefix Tuning for AAC (2023)](wiki/08_sources/prefix-tuning-aac-2023.md)
- [WavCaps (2024)](wiki/08_sources/wavcaps-2024.md)
- [AudioSetCaps (2024)](wiki/08_sources/audiosetcaps-2024.md)
- [OpenBEATs (2025)](wiki/08_sources/openbeats-2025.md)
- [Transfer Learning for AAC (2025)](wiki/08_sources/transfer-learning-aac-2025.md)
- [AVCL Survey (2024)](wiki/08_sources/avcl-survey-2024.md)
- [SED Review (2025)](wiki/08_sources/sed-review-2025.md)

### Section 2: Core LALM Architectures & Engines
- [EnCLAP (2024)](wiki/08_sources/enclap-2024.md)
- [Cacophony (2024)](wiki/08_sources/cacophony-2024.md)
- [Extending LLMs for AAC (2024)](wiki/08_sources/extending-llms-aac-2024.md)
- [SLAM-LLM (2025)](wiki/08_sources/slam-llm-2025.md)
- [CAT+ (2025)](wiki/08_sources/cat-plus-2025.md)
- [Falcon3-Audio (2026)](wiki/08_sources/falcon3-audio-2026.md)
- [DeSTA2.5-Audio (2026)](wiki/08_sources/desta25-audio-2026.md)

### Section 3: Alignment, Strategy & Fine-Tuning
- [Training without Audio (2024)](wiki/08_sources/training-without-audio-2024.md)
- [CoNeTTE (2024)](wiki/08_sources/conette-2024.md)
- [Parameter Efficient AC (2024)](wiki/08_sources/parameter-efficient-ac-2024.md)
- [Improving AAC Mixup (2024)](wiki/08_sources/improving-aac-mixup-2024.md)
- [Recap (2024)](wiki/08_sources/recap-2024.md)
- [DistillCaps (2024)](wiki/08_sources/distillcaps-2024.md)
- [Acoustic Prompt Tuning (2025)](wiki/08_sources/acoustic-prompt-tuning-2025.md)
- [LAVCap (2025)](wiki/08_sources/lavcap-2025.md)
- [Audiopedia (2025)](wiki/08_sources/audiopedia-2025.md)
- [RAG Low-Resource (2025)](wiki/08_sources/rag-low-resource-2025.md)
- [Omni-R1 (2026)](wiki/08_sources/omni-r1-2026.md)
- [Audio-CoT (2026)](wiki/08_sources/audio-cot-2026.md)
- [AVQACL++ (2026)](wiki/08_sources/avqacl-plus-2026.md)

### Section 4: Evaluation Metrics & Bias Mitigation
- [FD-DeCap (2025)](wiki/08_sources/fd-decap-2025.md)
- [MACE (2025)](wiki/08_sources/mace-2025.md)
- [CLAIRA (2026)](wiki/08_sources/claira-2026.md)
- [Reducing Hallucination (2026)](wiki/08_sources/reducing-hallucination-2026.md)
- [Data Leakage Benchmark (2026)](wiki/08_sources/data-leakage-benchmark-2026.md)

### Section 5: Domain Extensions (Heritage, Accessibility, Temporal)
- [Dual-Layer Video (2025)](wiki/08_sources/dual-layer-video-2025.md)
- [Crab AV (2025)](wiki/08_sources/crab-av-2025.md)
- [Soundscape Captioning (2025)](wiki/08_sources/soundscape-captioning-2025.md)
- [Ecoacoustic Soundscapes (2024)](wiki/08_sources/ecoacoustic-soundscapes-2024.md)

### Section 6: Dataset Acquisition, Annotation & Licensing
- [ALM Datasets Survey (2025)](wiki/08_sources/alm-datasets-survey-2025.md)

## 09 — Comparisons

- [AF3 vs DCASE Baseline](wiki/09_comparisons/af3-vs-dcase-baseline.md)
- [CLAPScore vs SPIDEr](wiki/09_comparisons/clapscore-vs-spider.md)

## 10 — Outputs

(Empty — future experiment outputs.)

## 11 — Glossary

- [Glossary](wiki/11_glossary/README.md)
