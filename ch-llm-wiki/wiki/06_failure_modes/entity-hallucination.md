---
title: Entity Hallucination
type: failure-mode
tags: [failure-mode, hallucination, chair-audio, rq3, l1]
status: stub
last_reviewed: 2026-04-20
sources: [../08_sources/paper-summaries-legacy.md, ../08_sources/literature-review-legacy.md]
---

## Entity hallucination

**Definition.** A LALM mentions sound entities in its caption that are **not present** in the actual audio. The mention is driven by the LLM's text prior (e.g., a "city street" cue in adjacent words triggers "and a car horn" even when no horn is audible) rather than by acoustic evidence in the input.

**Mechanism.** The Q-Former-compressed audio token is a weak conditioning signal compared to the LLM's autoregressive language prior. When the prior strongly predicts a co-occurring entity given the partial caption, the LLM emits it. This is a structural sibling of [polyphony-under-description](polyphony-under-description.md): both arise from the encoder-LLM bottleneck and the LLM's prior dominating insufficiently-grounded generation.

**How we measure it.** **CHAIR-audio dual criterion** (adapted from CHAIR for image captioning, Rohrbach 2018):

> An entity is hallucinated iff (a) absent from the clip's AudioSet tags **AND** (b) CLAPScore between the entity's text and the clip's audio < 0.25.

The dual criterion compensates for AudioSet's incomplete tagging (rater agreement ≈ 0.5; many audible events are un-tagged). Hallucination rate is reported per model with bootstrap CIs.

**Which RQ:** **RQ3** — *"What is AF3's entity-hallucination rate vs. SALMONN?"*

- **Solved if** AF3 hallucination rate < SALMONN by ≥ 5 pp.
- **Falsified if** CIs overlap.

**Stimulus dataset:** [audiocaps](../04_datasets/audiocaps.md) — single-event clips chosen so any extra entity is a hallucination candidate.

**Affected models:**
- [audio-flamingo-3](../03_models/audio-flamingo-3.md)
- [salmonn](../03_models/salmonn.md)
- [qwen2-5-omni](../03_models/qwen2-5-omni.md) (L2)

### Sources

- [paper-summaries-legacy](../08_sources/paper-summaries-legacy.md) — Paper S3 (Rohrbach 2018, CHAIR), Paper 2 (Gemmeke 2017, AudioSet ontology), Paper S2 (Wu 2023, LAION-CLAP), Paper 10 (Kuan 2024, hallucination = language-prior failure). `[UNSOURCED-PRIMARY: Rohrbach 2018]` `[UNSOURCED-PRIMARY: Gemmeke 2017]` `[UNSOURCED-PRIMARY: Wu 2023]` `[UNSOURCED-PRIMARY: Kuan 2024]` — pending ingest of EMNLP 2018 D18-1437, ICASSP 2017 10.1109/ICASSP.2017.7952261, ICASSP 2023 LAION-CLAP, and Interspeech 2024 Kuan paper into [`raw/01_primary_sources/`](../../raw/01_primary_sources/).
- [literature-review-legacy](../08_sources/literature-review-legacy.md) — §6.6 establishes the CHAIR-audio dual criterion (AudioSet absence ∧ CLAPScore < 0.25) and the rater-agreement ≈ 0.5 motivation for the dual gate; §5–§6 places hallucination as a structural sibling of polyphony and temporal failures (one bottleneck, three symptoms).

> Legacy synthesis context: [`literature_review.md` §6.6](../../../literature_review.md), [`paper_summaries.md` Papers 2, 3](../../../paper_summaries.md).
