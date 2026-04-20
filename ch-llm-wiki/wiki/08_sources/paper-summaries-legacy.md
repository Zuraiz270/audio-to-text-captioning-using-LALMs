---
title: paper_summaries.md — Legacy Synthesis (26-paper structured catalogue)
type: source-card
tags: [legacy-synthesis, project-internal, paper-catalogue, t1, t2, t3, papers, structured-cards]
status: stable
last_reviewed: 2026-04-20
sources: []
---

## paper_summaries.md — Legacy Synthesis (26-paper structured catalogue)

- **Raw file:** [`raw/03_legacy_synthesis/paper_summaries.md`](../../raw/03_legacy_synthesis/paper_summaries.md) ← primary basis
- **Venue / Level:** Project-internal synthesis document, CH-Proj-M, Uni Bamberg · **L4** (project codebase / synthesis artefact, not peer-reviewed) · **Year:** SS 2026 (Apr 2026 rebuild) · **Author:** Zuraiz (matrikel 2177213) under supervision of Prof. Abeßer
- **File size:** 24,366 bytes (24 KB)
- **Confidence / Applicability:** MED (synthesis, not primary) / HIGH (project-internal authoritative tier-priority and reading queue)

**Claim:** A structured per-paper catalogue covering 26 sources for T6 (Audio-to-Text Captioning with LALMs): 11 numbered primary/method papers + 15 supplementary (S1–S15) covering metrics, baselines, statistics, humanities. Each paper carries a fixed-format card: Venue/Level, Confidence/Applicability, Claim, Method, Key numbers, Threat to validity, Feeds (RQ tags + lit-review section), One-sentence reservation, optional `[YOUR NOTES]` slot. Defines tier convention (T1 = read before Phase 1 May 4; T2 = read before Phase 2 May 18; T3 = supplementary).

**Method:** Author-curated synthesis. Each card pre-fills the verifiable sections (venue, year, link, key numbers from abstracts/READMEs) and reserves space for post-reading notes. Card format is the body skeleton later adopted verbatim into [`CLAUDE.md` §4 source-card schema](../../CLAUDE.md). Reading-progress tracker table at end (lines 412–442) tracks per-paper reading status across three checkpoints (summary read, critical appraisal, notes done).

**Key numbers (paper roster — verbatim per legacy synthesis):**

- **T1 (Phase 1 priority, 6 papers):** Drossos 2020 (Clotho), Mei 2022 (AAC survey), Labbeti 2024 (DCASE baseline), Ghosh 2025b (AF3) ⭐, Kuan 2024 (hallucination mechanism), Schafer 1977 (soundscape ontology) ⭐.
- **T2 (Phase 2 priority, 6 papers):** Tang 2023 (SALMONN), Zhou 2022 (FENSE), Wu 2023 (LAION-CLAP), Rohrbach 2018 (CHAIR), Kumar 2026 (TAC), Heffernan 1993 (Museum of Words), Lipping 2022 (Clotho-AQA), Wohlin 2012 (Experimentation in SE).
- **T3 (supplementary, 13 papers):** Gemmeke 2017 (AudioSet), Kim 2019 (AudioCaps), Ghosh 2025a (AF2), Qwen Team 2025, Holm 1979, Efron & Tibshirani 1993, Truax 1984, Augoyard & Torgue 2006, Sterne 2012, Born 2013, Mitchell 1986, Kerr 1998.
- **Single most cited paper:** Ghosh 2025b — AF3 (PRIMARY MODEL, feeds RQ0–RQ4).
- **Verbatim T6 baseline number:** Labbeti 2024 reports **29.6% SPIDEr-FL** on Clotho-eval — the comparison floor for RQ1.
- **AF3 benchmark numbers (per legacy synthesis):** MMAU 72.28, ClothoAQA 91.1%, CMM-Hallucination 86.7%, Clotho-Entailment 92.9% — but explicitly flagged as conditional on RQ0 contamination audit outcome.

**Threat to validity:** This is **L4 project-internal synthesis**, not peer-reviewed primary literature. Cards are pre-filled from abstracts, READMEs, and the author's prior reading — they are **secondary descriptions**. Specific numerical claims (e.g., AF3's 72.28 MMAU score, Labbeti's 29.6% SPIDEr-FL) need to be re-verified against the raw papers when those are ingested. Per [`CLAUDE.md` §5](../../CLAUDE.md), this source card may be cited by concept pages **only as `[UNSOURCED-PRIMARY]` placeholder backing** until the primary paper is ingested into [`raw/01_primary_sources/`](../../raw/01_primary_sources/) and gets its own source card. At that point, concept-page citations should migrate from this legacy card to the primary-paper card, and this card's role reduces to "tier-priority and reading-queue index."

**Feeds:**

- **All RQs (RQ0–RQ5)** — provides the per-paper Feeds tags that map papers to RQs.
- **All concept pages with `[UNSOURCED-PRIMARY]` markers** — currently 14 stub pages: 3 model cards (AF3, SALMONN, Qwen2.5-Omni), 2 dataset cards (Clotho v2.1, AudioCaps), 2 metric cards (FENSE, SPIDEr-FL), 3 failure-mode cards (polyphony, entity-hallucination, temporal-grounding-loss), 4 humanities frames (ekphrasis, soundscape-schafer, accessibility, digital-archives).
- **Reading queue / tier prioritisation** — the single source of truth for which paper to read first (Phase 1 vs Phase 2 vs supplementary).
- Wiki pages currently citing this card: see "Cited by" below — populated as concept pages are upgraded from `status: stub` to `status: draft`.

**One-sentence reservation:** This is a **synthesis card, not a primary card** — never cite this card as the sole basis for an empirical claim that originates in a primary paper; always pair the citation with `[UNSOURCED-PRIMARY: <Author Year>]` and migrate to the primary-paper source card as soon as that paper is ingested.

### Notes

This card exists to bridge a real workflow gap: the wiki was bootstrapped with 14 concept-page stubs whose primary papers are not yet deposited in [`raw/01_primary_sources/`](../../raw/01_primary_sources/). Without this legacy-synthesis card, those stubs would have no citation chain at all (pure `[UNSOURCED]`), making them unusable for any query workflow per [`CLAUDE.md` §8](../../CLAUDE.md). With this card, each stub gets a **degraded but non-fabricated** citation: "the legacy synthesis says X about paper Y, pending primary-paper ingest."

This is exactly the partial-state pattern the schema is designed to handle gracefully — like the `status: draft` / `[UNSOURCED]` markers on [ch-proj-m-00-intro](ch-proj-m-00-intro.md) (deferred slide content), this card is the structural bridge that lets the wiki function during the bootstrap window.

**Migration policy.** When a primary paper is ingested:

1. Create its own source card (e.g., `wiki/08_sources/ghosh-2025b-af3.md`).
2. Update each concept page citing this legacy card to cite the new primary card instead.
3. Remove the `[UNSOURCED-PRIMARY: <Author Year>]` marker from the citation.
4. Update this card's "Feeds → Wiki pages currently citing" to remove the migrated page.
5. Append `EDIT` log entries per affected file.

When all 26 primary papers have been ingested, this card's role narrows to "the project's reading-queue index and tier prioritisation source," which is still a legitimate role and the card remains `status: stable`.

### Cross-links

- **Cited by (initial — to be populated as concept pages are upgraded):**
  - [audio-flamingo-3](../03_models/audio-flamingo-3.md) (pending — Ghosh 2025b)
  - [salmonn](../03_models/salmonn.md) (pending — Tang 2023)
  - [qwen2-5-omni](../03_models/qwen2-5-omni.md) (pending — Qwen Team 2025)
  - [clotho-v2-1](../04_datasets/clotho-v2-1.md) (pending — Drossos 2020)
  - [audiocaps](../04_datasets/audiocaps.md) (pending — Kim 2019)
  - [fense](../05_metrics/fense.md) (pending — Zhou 2022)
  - [spider-fl](../05_metrics/spider-fl.md) (pending — Labbeti 2024)
  - [polyphony-under-description](../06_failure_modes/polyphony-under-description.md) (pending — Mei 2022 + Drossos 2020)
  - [entity-hallucination](../06_failure_modes/entity-hallucination.md) (pending — Rohrbach 2018, Kuan 2024, Wu 2023)
  - [temporal-grounding-loss](../06_failure_modes/temporal-grounding-loss.md) (pending — Kumar 2026)
  - [ekphrasis](../07_humanities/ekphrasis.md) (pending — Heffernan 1993, Mitchell 1986)
  - [soundscape-schafer](../07_humanities/soundscape-schafer.md) (pending — Schafer 1977, Truax 1984, Augoyard 2006, Born 2013, Sterne 2012)
- **Sibling legacy-synthesis cards:** to be created — `project-guide-legacy.md`, `literature-review-legacy.md`, `implementation-plan-legacy.md`, `research-notes-legacy.md`.
- **Legacy synthesis context:** the file itself is the canonical paper catalogue, so this card *is* the legacy reference; cross-link back to [`paper_summaries.md`](../../../paper_summaries.md) at repo root for the live working copy (the raw copy in `raw/03_legacy_synthesis/` is the immutable snapshot).
