---
title: CH-Proj-M 00 — Topics (Course Topic Catalog T1–T10)
type: source-card
tags: [course, topic-catalog, t6, lalm, captioning, primary-origin]
status: stable
last_reviewed: 2026-04-20
sources: []
---

## CH-Proj-M 00 — Topics (Course Topic Catalog)

- **Raw file:** [`raw/00_course/CH-Proj-M-00-Topics.pdf`](../../raw/00_course/CH-Proj-M-00-Topics.pdf) ← primary basis
- **Venue / Level:** Course slide deck, CH-Proj-M, Computational Humanities, Uni Bamberg · **L1** (course-issued material) · **Year:** SS 2026 (Apr 2026) · **Link:** [https://www.uni-bamberg.de/ch/](https://www.uni-bamberg.de/ch/)
- **Author:** Prof. Dr.-Ing. Jakob Abeßer, Professur für Computational Humanities
- **Confidence / Applicability:** HIGH / HIGH (definitive for the project's official scope and dataset framing)

**Claim:** The course offers ten candidate Master-project topics (T1–T10) under the umbrella *Master Project — Machine Listening (CH-Proj-M)*. Topic **T6 — *Audio-to-Text Captioning using Large Audio-Language Models (LALMs)*** is the topic chosen for this project.

**Method:** Slide-deck enumeration (21 slides), one or two slides per topic, each with a Description, a Dataset, and a Tasks / Research Questions list. T6 occupies slides 12–13.

**Key numbers:**

- 10 candidate topics: T1 Bamberg church bells; T2 ERBA-Insel ecoacoustics; T3 bird activity detection; T4 cross-domain mosquito species classification; T5 few-shot rare bioacoustic event detection; **T6 Audio-to-Text Captioning using LALMs** *(chosen)*; T7 acoustic traffic monitoring; T8 music genre classification; T9 music chord recognition; T10 industrial sound analysis.
- T6 dataset stipulated as: **Clotho or AudioCaps** (typical for LALM captioning) — confirms [clotho-v2-1](../04_datasets/clotho-v2-1.md) and [audiocaps](../04_datasets/audiocaps.md) as in-scope.
- T6 originating research question (verbatim): *"How accurately can LALMs describe overlapping sound events compared to traditional tagging?"* — this is the seed of [polyphony-under-description](../06_failure_modes/polyphony-under-description.md) (RQ2) and motivates the broader failure-mode taxonomy.

**Threat to validity:** Slide deck — concise prose only, no methodological depth. Cannot be cited for *how* to do the work, only for *what* the course defines as in-scope. Operationalisation belongs to the 5 root synthesis docs.

**Feeds:**

- **RQ2** — the originating polyphony question is verbatim from this slide.
- Implicitly all RQs (the project itself derives from T6).
- Wiki pages currently citing this source card:
  - [scope](../01_project/scope.md) — for "T6 is the chosen topic" + L1/L2 split origin.
  - [phase-map](../01_project/phase-map.md) — for course-issued topic origin (deadlines come from the Intro deck, not Topics).

**One-sentence reservation:** Do not cite this source for technical details about LALM architectures, metrics, or failure mechanisms — those require ingest of peer-reviewed primary sources (AF3, SALMONN, Drossos 2020, etc.).

### Notes

The slide deck also catalogues 9 alternative topics that were **not** chosen — these are useful as context for why T6 was selected (it is the only deeply Computational-Humanities-flavoured topic in the catalog: it requires inter-modal translation rather than classification or detection).

T6 description (verbatim from slide 12):
> *"Moving beyond simple classification, sound event captioning describes complex acoustic scenes in natural language. This project utilizes state-of-the-art Large Audio-Language Models (LALMs) to 'write' descriptions of audio clips."*

### Cross-links

- **Cited by:**
  - [`wiki/01_project/scope.md`](../01_project/scope.md)
  - [`wiki/01_project/phase-map.md`](../01_project/phase-map.md)
- **Legacy synthesis context:** the chosen topic is operationalised in [`PROJECT_GUIDE.md`](../../../PROJECT_GUIDE.md) and the 4 sibling root docs.
