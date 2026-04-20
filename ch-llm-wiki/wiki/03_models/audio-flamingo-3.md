---
title: Audio Flamingo 3 (AF3)
type: model-card
tags: [lalm, audio-flamingo, nvidia, primary-model, l1]
status: draft
last_reviewed: 2026-04-20
sources: [../08_sources/goel-2025-af3.md, ../08_sources/paper-summaries-legacy.md, ../08_sources/implementation-plan-legacy.md]
---

## Audio Flamingo 3

| Field | Value |
|:------|:------|
| Family | LALM (Large Audio-Language Model) |
| Released | Jul 2025 by NVIDIA (co-first authors: Arushi Goel★, Sreyan Ghosh★) |
| Audio encoder | AF-Whisper — unified encoder over speech, sound, music |
| Adapter | Q-Former-style |
| LLM decoder | NVIDIA Nemotron-derived (per AF3 abstract) |
| Parameters | undisclosed in abstract — refetch HuggingFace card to confirm |
| Training data | AudioSkills-XL, LongAudio-XL, AF-Think, AF-Chat (open-source audio only) — completeness flagged Q1 WAITING-ON-REFETCH |
| Open weights | yes (per "fully open" claim — pending HF data-card verification) |

### Role in this project

**Primary model under test (L1).** AF3 is the LALM whose **claimed-zero-shot** captioning is benchmarked against the supervised DCASE 2024 baseline on Clotho v2.1. The "zero-shot" framing is itself a project-tested claim (RQ0), not a premise.

- Feeds RQ0 (contamination audit), RQ1 (vs. baseline), RQ2 (polyphony), RQ3 (hallucination), RQ4 (temporal — L2), RQ5 (cultural — L2).

### Headline numbers (preprint)

- **MMAU:** 72.42 † (corrected from earlier draft 72.28)
- **CMM-Hallucination:** 86.7 †
- Long-audio understanding: ≤ 10 min

† Preprint, single-team result, not independently replicated as of 2026-04-20.

### Known failure modes

- [polyphony-under-description](../06_failure_modes/polyphony-under-description.md)
- [entity-hallucination](../06_failure_modes/entity-hallucination.md)
- [temporal-grounding-loss](../06_failure_modes/temporal-grounding-loss.md)

### Sources

- [goel-2025-af3](../08_sources/goel-2025-af3.md) — primary source card (arXiv 2507.08128 abstract retrieved 2026-04-20). `[Goel 2025; L3-preprint; HIGH/MED]`.
- [paper-summaries-legacy](../08_sources/paper-summaries-legacy.md) — legacy synthesis context (Papers 7, 8). Retained for back-compatibility; superseded by goel-2025-af3 for AF3-specific claims.
- [implementation-plan-legacy](../08_sources/implementation-plan-legacy.md) — operational context: AF3 hardware gate (SM ≥ 8.0, ≥ 24 GB VRAM bf16); determinism pins; 4-cut model ladder; canonical RQ0–RQ5 entry points.

> Legacy synthesis context: AF3 lineage and architectural details summarized in [`paper_summaries.md`](../../../paper_summaries.md) §P8 and [`literature_review.md` §4.3](../../../literature_review.md).
