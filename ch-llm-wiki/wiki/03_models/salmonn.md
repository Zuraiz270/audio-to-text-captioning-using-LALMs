---
title: SALMONN
type: model-card
tags: [lalm, salmonn, comparison-model, l1]
status: draft
last_reviewed: 2026-04-20
sources: [../08_sources/tang-2023-salmonn.md, ../08_sources/paper-summaries-legacy.md, ../08_sources/implementation-plan-legacy.md]
---

## SALMONN

| Field | Value |
|:------|:------|
| Family | LALM |
| Released | 2023 (Tang et al.); ICLR 2024 |
| Audio encoder | Whisper-L-v2 (speech) + BEATs (events / music) — dual-encoder |
| Adapter | Window-level Q-Former |
| LLM decoder | Vicuna-13B |
| Parameters | 13B |
| Training data | per-paper enumeration deferred — refetch ICLR PDF to populate fully |
| Open weights | yes |

### Role in this project

**Comparison LALM (L1).** SALMONN is the secondary LALM used in the RQ3 hallucination comparison (H4) and as a historical LALM baseline for RQ1.

- Feeds RQ1 (historical LALM baseline), RQ2 (dual-encoder test), RQ3 (hallucination comparison vs. AF3).

### Known failure modes

- [polyphony-under-description](../06_failure_modes/polyphony-under-description.md)
- [entity-hallucination](../06_failure_modes/entity-hallucination.md)

### Sources

- [tang-2023-salmonn](../08_sources/tang-2023-salmonn.md) — primary source card (arXiv 2310.13289 abstract retrieved 2026-04-20). `[Tang 2023; L2; HIGH/HIGH]`.
- [paper-summaries-legacy](../08_sources/paper-summaries-legacy.md) — legacy synthesis context (Paper 6). Retained for back-compatibility.
- [implementation-plan-legacy](../08_sources/implementation-plan-legacy.md) — operational context: SALMONN's role as the secondary LALM in the 4-cut model ladder; canonical RQ3 (H4) hallucination comparison protocol against AF3 (CHAIR-audio dual criterion).

> Legacy synthesis context: [`paper_summaries.md`](../../../paper_summaries.md) Paper 6, [`literature_review.md` §4.2](../../../literature_review.md).
