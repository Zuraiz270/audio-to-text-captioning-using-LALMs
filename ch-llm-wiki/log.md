# Wiki Change Log

This file is append-only. Every structural change to the wiki is recorded here.

---

## [2026-04-21] setup | wiki initialization

- Created directory tree under `ch-llm-wiki/`.
- Created `CLAUDE.md` (operating schema).
- Created `index.md` (master table of contents).
- Created `log.md` (this file).
- Files touched: `CLAUDE.md`, `index.md`, `log.md`, all directory `.gitkeep` files.
- Why: Initial wiki build per LLM Wiki Agent implementation plan.
- Source: User instruction, 2026-04-21.

## [2026-04-21] seed | thematic seed pages

- Created project, RQ, model, dataset, metric, failure-mode, humanities, comparison, and glossary seed pages.
- Files touched: 24 wiki pages across `wiki/00_overview/` through `wiki/11_glossary/`.
- Why: Structural scaffolding for the wiki knowledge base.
- Source: `PROJECT_GUIDE.md`, `LALM_Synthesis_Matrix.md`.

## [2026-04-21] seed | canonical paper registry seeding

- Read `Credible Literature/info.txt` (39 lines).
- **Duplicate detected:** Lines 7 and 38 both reference "Soundscape Captioning Using Sound Affective Quality Network and Large Language Model" (IEEE 11329491). Duplicate not removed — reported only.
- Created 38 seed source-note pages in `wiki/08_sources/` (one per unique paper).
- Files touched: 38 files in `wiki/08_sources/`.
- Why: Seed the wiki with one structural page per canonical paper from the registry.
- Source: `Credible Literature/info.txt`, `Credible Literature/LALM_Synthesis_Matrix.md`.

## [2026-04-21] cleanup-approved | PDF migration to raw

- Copied 11 PDFs from `Literature/` subdirectories into `raw/01_primary_sources/`.
- Files: AudioCaps.pdf, Audio Flamingo 2.pdf, Audio Flamingo 3.pdf, Audio Flamingo Next.pdf, Automated Audio Captioning.pdf, Clotho-AQA.pdf, Description and Discussion on DCASE 2026.pdf, Qwen2.5-Omni Technical Report.pdf, SALMONN.pdf, TAC Timestamped Audio Captioning.pdf, Clotho_an_Audio_Captioning_Dataset.pdf.
- Why: Preserve primary source documents in the wiki's raw layer before deleting the legacy directory.
- Source: User instruction, 2026-04-21.

## [2026-04-21] cleanup-approved | duplicate fix in info.txt

- Removed duplicate entry for IEEE-11329491 (Soundscape Captioning) from line 38 of `Credible Literature/info.txt`.
- Original entry on line 7 preserved.
- Canonical unique paper count: **38**.
- Why: Duplicate detected during lint. User approved cleanup.
- Source: Lint report, user approval.

## [2026-04-21] cleanup-approved | legacy directory removal

- Deleted `_archive/` (old wiki, old literature_review.md, old paper_summaries.md).
- Deleted `Literature/` (old PDFs — contents already migrated to `raw/01_primary_sources/`).
- Deleted `implementation_plan.md` (root-level legacy artifact).
- Deleted `research_notes.md` (root-level legacy notes).
- Why: All content superseded by the new wiki. PDFs preserved in raw layer.
- Source: User instruction, 2026-04-21.

## [2026-04-21] ingest | first abstract batch (14 papers)

- Fetched abstracts from IEEE Xplore for 14 papers and upgraded source-note pages from `seed` → `draft`.
- Papers ingested: reducing-hallucination-2026, claira-2026, omni-r1-2026, audio-cot-2026, falcon3-audio-2026, desta25-audio-2026, avqacl-plus-2026, soundscape-captioning-2025, fd-decap-2025, mace-2025, data-leakage-benchmark-2026, slam-llm-2025, crab-av-2025, cat-plus-2025.
- Each page now contains: abstract summary, key contributions, RQ relevance, cross-links, and identified limitations.
- Why: Phase 4 ingest — upgrade seed pages with evidence from IEEE Xplore abstracts.
- Source: IEEE Xplore abstracts (Tier A metadata + partial Tier B content).

## [2026-04-22] ingest | second abstract batch (24 papers — ingest complete)

- Fetched abstracts via IEEE Xplore, DuckDuckGo search, and arXiv for remaining 24 seed papers.
- All 38 source-note pages are now `status: draft`. Zero seeds remaining.
- Papers ingested: acoustic-prompt-tuning-2025, parameter-efficient-ac-2024, audiosetcaps-2024, training-without-audio-2024, enclap-2024, prefix-tuning-aac-2023, recap-2024, audiopedia-2025, openbeats-2025, alm-datasets-survey-2025, transfer-learning-aac-2025, improving-aac-mixup-2024, extending-llms-aac-2024, beyond-status-quo-2023, conette-2024, wavcaps-2024, cacophony-2024, distillcaps-2024, lavcap-2025, avcl-survey-2024, sed-review-2025, dual-layer-video-2025, ecoacoustic-soundscapes-2024, rag-low-resource-2025.
- Coverage: all pages now contain abstract summary, key contributions, RQ relevance mapping, cross-links, and limitations.
- Why: Complete Phase 4 ingest — all canonical papers at draft quality.
- Source: IEEE Xplore, DuckDuckGo, arXiv (Tier A registry metadata).
