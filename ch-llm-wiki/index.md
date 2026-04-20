# Wiki Index — CH-Proj-M

*Audio-to-Text Captioning using Large Audio-Language Models · SS 2026 · Zuraiz · Uni Bamberg · Prof. Abeßer*

> **Read first:** [`CLAUDE.md`](CLAUDE.md) — schema and conventions. Every session starts there.
> **Audit trail:** [`log.md`](log.md) — append-only history.
> **Root synthesis:** [`PROJECT_GUIDE.md`](../PROJECT_GUIDE.md) · [`implementation_plan.md`](../implementation_plan.md) · [`literature_review.md`](../literature_review.md) · [`paper_summaries.md`](../paper_summaries.md) · [`research_notes.md`](../research_notes.md)

---

## 00 — Overview

| Page | Hook |
|:-----|:-----|
| [README](wiki/00_overview/README.md) | What this wiki is, how to read it, how to extend it. |

## 01 — Project

| Page | Hook |
|:-----|:-----|
| [scope](wiki/01_project/scope.md) | L1 course-safe core / L2 research-grade extension; cut order. |
| [phase-map](wiki/01_project/phase-map.md) | Phase 0–4 timeline with hard gates and red-line stop conditions. |

## 02 — Research questions

| Page | Hook |
|:-----|:-----|
| [rq-index](wiki/02_research_questions/rq-index.md) | RQ0–RQ5 one-liners, primary metric, layer (L1/L2). |
| [rq0-contamination](wiki/02_research_questions/rq0-contamination.md) | Validity-gate RQ: training-data overlap audit. |

## 03 — Models

| Page | Hook |
|:-----|:-----|
| [audio-flamingo-3](wiki/03_models/audio-flamingo-3.md) | Primary LALM under test. NVIDIA, Jul 2025. |
| [salmonn](wiki/03_models/salmonn.md) | Secondary LALM, comparison baseline (Tang 2023). |
| [qwen2-5-omni](wiki/03_models/qwen2-5-omni.md) | Tertiary LALM, conditional Layer-2 cut. |
| [af-clap](wiki/03_models/af-clap.md) | Audio-Flamingo unified encoder (AF-CLAP / AF-Whisper) — naming hygiene + lineage. |

## 04 — Datasets

| Page | Hook |
|:-----|:-----|
| [clotho-v2-1](wiki/04_datasets/clotho-v2-1.md) | Canonical AAC eval benchmark. 1,045 eval clips. Zenodo 4783391. |
| [audiocaps](wiki/04_datasets/audiocaps.md) | RQ3 hallucination stimulus set. ~46k AudioSet-derived clips. |

## 05 — Metrics

| Page | Hook |
|:-----|:-----|
| [fense](wiki/05_metrics/fense.md) | Fluency- and Error-aware Sentence Embedding Score. |
| [spider-fl](wiki/05_metrics/spider-fl.md) | DCASE 2024 official metric. Baseline: 29.6%. |

## 06 — Failure modes

| Page | Hook |
|:-----|:-----|
| [polyphony-under-description](wiki/06_failure_modes/polyphony-under-description.md) | Concurrent secondary events silently dropped. |
| [entity-hallucination](wiki/06_failure_modes/entity-hallucination.md) | Sounds asserted that aren't in the audio. |
| [temporal-grounding-loss](wiki/06_failure_modes/temporal-grounding-loss.md) | Events ordered by text prior, not actual onset. |

## 07 — Humanities

| Page | Hook |
|:-----|:-----|
| [ekphrasis](wiki/07_humanities/ekphrasis.md) | Verbal description of non-verbal aesthetic experience. |
| [soundscape-schafer](wiki/07_humanities/soundscape-schafer.md) | Keynote / soundmark / signal — Schafer 1977. |
| [accessibility](wiki/07_humanities/accessibility.md) | Audio captions for blind / low-vision users. |
| [digital-archives](wiki/07_humanities/digital-archives.md) | British Library, BBC SFX, Europeana Sounds. |

## 08 — Sources

| Page | Hook |
|:-----|:-----|
| [INDEX](wiki/08_sources/INDEX.md) | Source-card index — every raw file → its source card. |
| [ch-proj-m-00-topics](wiki/08_sources/ch-proj-m-00-topics.md) | Course topic catalog T1–T10; T6 is this project. |
| [ch-proj-m-00-intro](wiki/08_sources/ch-proj-m-00-intro.md) | Course intro deck — logistics, deliverables, deadlines. |
| [paper-summaries-legacy](wiki/08_sources/paper-summaries-legacy.md) | Legacy synthesis (L4) — 26-paper structured catalogue; bridge citation for 14 stub concept pages. |
| [project-guide-legacy](wiki/08_sources/project-guide-legacy.md) | Legacy synthesis (L4) — project entry point owning scope, phase map, RQ table, glossary. |
| [literature-review-legacy](wiki/08_sources/literature-review-legacy.md) | Legacy synthesis (L4) — EBSE evidence narrative, 15 sections (humanities + unified RCA + DARIAH/BL/BBC). |
| [implementation-plan-legacy](wiki/08_sources/implementation-plan-legacy.md) | Legacy synthesis (L4) — operational playbook (determinism pins, hardware gate, Makefile, risk register). |
| [research-notes-legacy](wiki/08_sources/research-notes-legacy.md) | Legacy synthesis (L4) — strategy, evidence-expansion ops, reading order, May-4 talk branching. |
| [goel-2025-af3](wiki/08_sources/goel-2025-af3.md) | Primary card for Audio Flamingo 3 (arXiv 2507.08128, NeurIPS 2025 spotlight). |
| [tang-2023-salmonn](wiki/08_sources/tang-2023-salmonn.md) | Primary card for SALMONN (ICLR 2024 / arXiv 2310.13289). |
| [qwen-2025-omni](wiki/08_sources/qwen-2025-omni.md) | Primary card for Qwen2.5-Omni (arXiv 2503.20215). |
| [drossos-2020-clotho](wiki/08_sources/drossos-2020-clotho.md) | Primary card for Clotho v1 (ICASSP 2020 / arXiv 1910.09387). |
| [zhou-2022-fense](wiki/08_sources/zhou-2022-fense.md) | Primary card for FENSE (ICASSP 2022 / arXiv 2110.04684). |
| [kumar-2026-tac](wiki/08_sources/kumar-2026-tac.md) | Primary card for TAC — Timestamped Audio Captioning (arXiv 2602.15766, Feb 2026). |
| [polybench-2026](wiki/08_sources/polybench-2026.md) | Primary card for PolyBench polyphony benchmark (arXiv 2603.05128, Mar 2026). |

## 09 — Comparisons

| Page | Hook |
|:-----|:-----|
| [af3-zero-shot-claim](wiki/09_comparisons/af3-zero-shot-claim.md) | AF3 author "zero-shot" claim vs. project's RQ0-tested premise. |
| [clapscore-threshold-0-25](wiki/09_comparisons/clapscore-threshold-0-25.md) | The 0.25 hallucination threshold as a free parameter with sensitivity analysis. |

## 10 — Outputs

*Empty. Created when first experiment runs.*

## 11 — Glossary

| Page | Hook |
|:-----|:-----|
| [README](wiki/11_glossary/README.md) | Stub pointing to the canonical 20-term glossary in `PROJECT_GUIDE.md`. Per-term pages may be added over time. |
