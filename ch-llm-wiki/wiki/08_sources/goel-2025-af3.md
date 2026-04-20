---
type: source-card
status: draft
last_reviewed: 2026-04-20
---

# Goel et al. 2025 — Audio Flamingo 3

**Raw file:** [goel-2025-af3-abstract.md](../../raw/01_primary_sources/goel-2025-af3-abstract.md)
**External:** arXiv 2507.08128 (https://arxiv.org/abs/2507.08128)
**Venue / Level:** NeurIPS 2025 spotlight (announced) — abstract retrieved as L3 preprint
**Confidence / Applicability:** HIGH / MED — author-self-reported numbers; not independently replicated as of 2026-04-20

## Claim

Audio Flamingo 3 (AF3) is a fully open large audio-language model that achieves SOTA on 20+ audio understanding/reasoning benchmarks, surpassing larger closed-source competitors when trained on open audio data only.

## Method

Five-stage curriculum training over a unified audio encoder (AF-Whisper) joining speech, sound, and music. On-demand "thinking" mode (CoT before answer), multi-turn multi-audio chat, long-audio (≤10 min), voice-to-voice. Training corpora: AudioSkills-XL, LongAudio-XL, AF-Think, AF-Chat (all author-curated).

## Key numbers (project-relevant)

- **MMAU:** 72.42 † (preprint, not independently replicated as of 2026-04-20)
- **CMM-Hallucination:** 86.7 †
- Long-audio: ≤ 10 min

† Preprint qualifier per literature_review.md §4.3.

## Threat to validity

- "Fully open" claim depends on whether the HuggingFace data card enumerates the *complete* training corpus (Q1 in research_notes.md is **WAITING-ON-REFETCH**).
- Single-team result; replication risk.
- Lead-author misattribution (project drafts said "Ghosh"; lead is **Goel**) corrected 2026-04-20 — citation hygiene flag for downstream files.

## Feeds

- RQ0 contamination check (training-manifest disclosure)
- RQ1 baseline gap claim (AF3 vs DCASE 29.6%)
- RQ2 polyphony failure mode (AF-Whisper as adapter)
- literature_review.md §4.3, paper_summaries.md §P8

## One-sentence reservation

Numbers are author-reported on a preprint and the open-data claim is contingent on a HuggingFace data card refetch that has not yet succeeded.

## Cross-links

- [audio-flamingo-3.md](../03_models/audio-flamingo-3.md)
- [paper-summaries-legacy.md](paper-summaries-legacy.md) — earlier bridge citation, now superseded for AF3 claims
