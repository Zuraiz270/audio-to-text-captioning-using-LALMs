---
title: Temporal Grounding Loss
type: failure-mode
tags: [failure-mode, temporal, ordering, rq4, l2]
status: draft
last_reviewed: 2026-04-20
sources: [../08_sources/kumar-2026-tac.md, ../08_sources/paper-summaries-legacy.md, ../08_sources/literature-review-legacy.md]
---

## Temporal grounding loss

**Definition.** When a clip contains two temporally-ordered events ("A then B"), LALMs describe them in the **canonical text-prior order** rather than the actual onset order observed in the audio. For example, given audio of "thunder, then rain," a LALM with a strong "rain → thunder" co-occurrence prior may caption "rain falls and thunder rumbles" — semantically reasonable but temporally inverted.

**Mechanism.** The audio encoder produces frame-level temporal information; the Q-Former's fixed-token bottleneck destroys temporal granularity by pooling. The LLM decoder then generates from a temporally-flattened representation and falls back on text-prior co-occurrence statistics for ordering. This is the third structural sibling of [polyphony-under-description](polyphony-under-description.md) and [entity-hallucination](entity-hallucination.md): three failures, one root cause (the encoder-LLM information bottleneck).

**How we measure it.** **Synthetic A-then-B mixtures.** Construct controlled stimuli by concatenating pairs of single-event clips at known onsets, with both event orderings (A→B and B→A). Compute correct-ordering rate per model:

- **Mechanism present (RQ4 success):** correct-ordering rate ≤ 60% — at or near chance for unordered captioning.
- **Mechanism weakened (RQ4 falsified):** correct-ordering rate > 80% — temporal information survives the bottleneck better than expected.

**Which RQ:** **RQ4** — *"Do LALMs correctly order events in synthetic A-then-B mixtures?"* (L2 — second in the cut order per [scope](../01_project/scope.md))

**Affected models:**
- [audio-flamingo-3](../03_models/audio-flamingo-3.md)
- [salmonn](../03_models/salmonn.md)
- [qwen2-5-omni](../03_models/qwen2-5-omni.md) (L2)

### Sources

- [kumar-2026-tac](../08_sources/kumar-2026-tac.md) — primary source card for the TAC protocol (arXiv 2602.15766, Feb 17 2026, CC BY 4.0). Confirmed real preprint as of 2026-04-20. `[Kumar 2026; L3-preprint; MED/HIGH]`.
- [paper-summaries-legacy](../08_sources/paper-summaries-legacy.md) — legacy synthesis context (Paper 11). Retained for back-compatibility.
- [literature-review-legacy](../08_sources/literature-review-legacy.md) — §6 places temporal grounding loss as the third structural failure of the encoder-LLM bottleneck (the unified-RCA argument); cites TAC as the L2 architectural mitigation pointing toward the project's research-grade extension.

> Legacy synthesis context: [`literature_review.md`](../../../literature_review.md), [`research_notes.md`](../../../research_notes.md), [`implementation_plan.md` §Temporal Alignment Procedure](../../../implementation_plan.md).
