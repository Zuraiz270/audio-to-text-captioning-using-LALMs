---
title: Polyphony Under-Description
type: failure-mode
tags: [failure-mode, polyphony, rq2, l1]
status: draft
last_reviewed: 2026-04-20
sources: [../08_sources/polybench-2026.md, ../08_sources/drossos-2020-clotho.md, ../08_sources/paper-summaries-legacy.md, ../08_sources/literature-review-legacy.md]
---

## Polyphony under-description

**Definition.** When two or more sound events occur simultaneously in the same audio clip ("polyphony"), LALMs systematically describe only the dominant event and silently drop the concurrent secondary events. The output caption is grammatical and fluent, but the acoustic scene's concurrency is invisible in the text.

**Mechanism.** The Q-Former (or equivalent adapter) compresses variable-length encoder output into a small fixed token budget consumed by the LLM decoder. There is no explicit concurrent-event segregation at the adapter layer, so secondary events are squeezed out of the bottleneck. The LLM then completes the most likely caption given the dominant audio token + its language prior, which favors single-event canonical descriptions.

**How we measure it.** Δ SPIDEr-FL between polyphonic and monophonic subsets of Clotho-eval. Polyphony labels are crowdsourced; gate is Cohen's κ ≥ 0.6. Fallback: AudioSet proxy labels (clips with ≥ 2 distinct AudioSet tags marked polyphonic). See [rq-index](../02_research_questions/rq-index.md) for the RQ2 success / falsification criteria.

**Which RQ:** **RQ2** — *"Is the AF3-baseline gap larger on polyphonic clips than monophonic?"*

**Affected models:**
- [audio-flamingo-3](../03_models/audio-flamingo-3.md)
- [salmonn](../03_models/salmonn.md)
- [qwen2-5-omni](../03_models/qwen2-5-omni.md)

### Sources

- [polybench-2026](../08_sources/polybench-2026.md) — independent post-AF3 (Mar 2026) corroboration: 5-subset benchmark explicitly measuring polyphonic event-count under-description across contemporary LALMs. `[PolyBench 2026; L3-preprint; MED/HIGH]`.
- [drossos-2020-clotho](../08_sources/drossos-2020-clotho.md) — Clotho v2.1 is the project's polyphony-subset source dataset.
- [paper-summaries-legacy](../08_sources/paper-summaries-legacy.md) — Paper 4 (Mei 2022, polyphony explicitly named un-solved) and Paper 1 (Drossos 2020, Clotho's natural polyphony). `[UNSOURCED-PRIMARY: Mei 2022]` retained pending ingest of arXiv 2205.05949 into [`raw/01_primary_sources/`](../../raw/01_primary_sources/).
- [literature-review-legacy](../08_sources/literature-review-legacy.md) — §5.1, §5.2, §6.4 unified RCA: polyphony under-description is one of three encoder→adapter→LLM bottleneck failures (the structural sibling argument the project rests on); cites Mei 2022 + Drossos 2020 within that frame.

> Legacy synthesis context: [`literature_review.md` §5.1, §5.2](../../../literature_review.md), [`paper_summaries.md`](../../../paper_summaries.md) Papers 1, 4.
