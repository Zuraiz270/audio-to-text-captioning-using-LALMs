# LALM Polyphony Evidence Taxonomy

*This document categorizes all 39 canonical papers downloaded for the CH-Proj-M Master's project. It defines exactly how each paper serves the T6 course requirement (Polyphony Evaluation) and explicitly notes which papers are safely ignored.*

---

## 1. The "Code Architecture" Papers (Heavy Active Use)
*These papers are directly used to write the Python evaluation scripts, determine the model parameters, and define the mathematical metrics for the T6 Polyphony baseline.*

### Metrics & Evaluation Design
- **MACE (2025):** Provides the mathematical foundation for "Event Recall" by breaking captions down into noun/verb objects to bypass SPIDEr limitations.
- **Reducing Object Hallucination (2026):** Introduces the CHAIR-audio metric, which we inverse to measure polyphony event drops.
- **CLAIRA (2026):** Validates using an LLM-as-a-judge as a standard evaluation mechanism.
- **Benchmarking Data Leakage (2026):** The blueprint for ensuring our datasets (Clotho) are properly split and not artificially inflating zero-shot scores.

### Model Baselines
- **Falcon3-Audio (2026):** Primary LALM test subject (chosen for public-data purity).
- **SALMONN (2024):** Secondary LALM test subject (widely used dual-encoder baseline).
- **Qwen2.5-Omni (2026):** Tertiary LALM baseline.

---

## 2. The "May 4th Presentation" Data Papers
*These papers are the core evidence required for the May 4th Data Acquisition & Annotation Seminar Presentation.*

- **ALM Datasets Survey (2025):** The holy grail for the presentation. Reviews 69 audio datasets, licensing issues, and data collection methodologies.
- **AudioSetCaps (2024) / WavCaps (2024) / Clotho (2020):** Primary examples of how datasets are crowdsourced vs. scraped.
- **Benchmarking Data Leakage (2026) (Re-used):** Proves how annotation augmentation ruins downstream evaluations.

---

## 3. The "Literature Review" Papers (Used for Term Paper Draft)
*These papers are not used in the code, but they are absolutely necessary to cite in the final ~15-page term paper to explain *why* LALMs fail at overlapping sounds.*

### The Root Cause of Polyphony Failure
- **Omni-R1 (2025):** Proves that LALM "audio reasoning" gains are actually just the LLM getting better at text logic, which means they drop audio signals they don't logically expect.
- **Audio-CoT (2025 & 2026):** Proves that while Chain-of-Thought helps on simple audio, it catastrophically confuses the model on hard, highly polyphonic audio.

### Alternatives to Tagging (Contextual Citations)
- **Crab (2025) / SLAM-LLM (2025):** Current SOTA attempts to fix the LLM text-prior issue using cross-modal adapter tricks.
- **RAG for Low-Resource Audio (2025) / DistillCaps (2024):** Attempts to fix hallucination via RAG.
- **FD-DeCap (2025):** Explores debiasing models using front-door causal inference.

---

## 4. The "Baseline Context" Papers
*Historically important context for the T6 requirement to compare LALMs to "traditional tagging."*

- **Systematic Review on Sound Event Detection (2025):** The foundation for understanding what a "tagging baseline" actually is (CNNs, ASTs).
- **Audio-Visual Learning Survey (2024):** Broader multimodal context.

---

## 5. Archived "Out of Scope" Papers
*These were read, digested, and then explicitly abandoned because they do not serve the strict T6 Polyphony requirement.*

- **Ecoacoustic Soundscapes (2024) / Soundscape Captioning (2025):** Originally pulled for the Computational Humanities / Ekphrasis / Cultural frame. Now safely ignored since we stripped RQ5 from the project guide.
- **Dual-Layer Video (2025) / AVQA (2026):** Too focused on visual modalities, not purely audio captioning.
