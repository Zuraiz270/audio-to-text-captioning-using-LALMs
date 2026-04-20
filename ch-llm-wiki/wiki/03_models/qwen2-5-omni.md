---
title: Qwen2.5-Omni
type: model-card
tags: [lalm, qwen, alibaba, l2, ablation]
status: draft
last_reviewed: 2026-04-20
sources: [../08_sources/qwen-2025-omni.md, ../08_sources/paper-summaries-legacy.md, ../08_sources/implementation-plan-legacy.md]
---

## Qwen2.5-Omni

| Field | Value |
|:------|:------|
| Family | LALM (end-to-end multimodal: text, image, audio, video) |
| Released | March 2025 (arXiv 2503.20215) by Alibaba — CC BY 4.0 |
| Audio encoder | Block-wise streaming audio encoder |
| Adapter | TMRoPE (Time-aligned Multimodal RoPE) position embedding for audio/video sync |
| LLM decoder | Qwen2.5 family — Thinker (text-generation core) |
| Speech generator | Talker — dual-track autoregressive on Thinker hidden states (audio tokens) |
| Parameters | varies by released checkpoint (refetch HF model card for exact figures) |
| Training data | per-paper enumeration deferred to PDF re-fetch |
| Open weights | yes (CC BY 4.0) |

### Role in this project

**Tertiary model (L2).** Conditional ablation — used only if compute / time permit. First in the L2 cut order (drops first under pressure), per [scope](../01_project/scope.md). Of structural interest for RQ4 because TMRoPE is explicitly designed to align audio/video timestamps — relevant to temporal grounding.

### Known failure modes

- [polyphony-under-description](../06_failure_modes/polyphony-under-description.md)
- [entity-hallucination](../06_failure_modes/entity-hallucination.md)
- [temporal-grounding-loss](../06_failure_modes/temporal-grounding-loss.md) — TMRoPE is *hypothesised* to mitigate; not yet benchmarked against TAC-style probes.

### Sources

- [qwen-2025-omni](../08_sources/qwen-2025-omni.md) — primary source card (arXiv 2503.20215 abstract retrieved 2026-04-20). `[Qwen Team 2025; L3-preprint; HIGH/MED]`.
- [paper-summaries-legacy](../08_sources/paper-summaries-legacy.md) — legacy synthesis context (Paper 9).
- [implementation-plan-legacy](../08_sources/implementation-plan-legacy.md) — operational context: L2 ablation slot, first to drop under compute / time pressure per cut order in [scope](../01_project/scope.md).

> Legacy synthesis context: [`research_notes.md`](../../../research_notes.md), [`literature_review.md`](../../../literature_review.md).
