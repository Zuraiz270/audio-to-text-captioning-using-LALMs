---
title: Project Scope — L1 Course-Safe / L2 Research-Grade
type: concept
tags: [scope, layers, l1, l2, cut-order]
status: stable
last_reviewed: 2026-04-20
sources: [../08_sources/ch-proj-m-00-topics.md, ../08_sources/project-guide-legacy.md]
---

## Origin

This project is the chosen instantiation of **Topic T6 — Audio-to-Text Captioning using Large Audio-Language Models (LALMs)** from the course-issued topic catalog (see [`ch-proj-m-00-topics`](../08_sources/ch-proj-m-00-topics.md)). The project is structured into two independent layers so that course-safe deliverables are protected from research-grade ambition.

> *Canonical scope statement:* [`PROJECT_GUIDE.md` §Scope](../../../PROJECT_GUIDE.md) (legacy synthesis context).

## Layer 1 — Course-Safe Core (must ship)

The minimum deliverable that stands on its own as a defensible 6 ECTS submission even if every Layer-2 extension fails.

| Component | What it covers | Page |
|:----------|:---------------|:-----|
| RQ0 — Contamination audit | FreeSound ID cross-reference | [rq-index](../02_research_questions/rq-index.md) |
| RQ1 — AF3 vs DCASE baseline | SPIDEr-FL on Clotho-eval with BCa CI | [rq-index](../02_research_questions/rq-index.md) |
| RQ2 — Polyphony differential | Δ SPIDEr-FL poly vs mono | [polyphony-under-description](../06_failure_modes/polyphony-under-description.md) |
| RQ3 — Hallucination rate | CHAIR-audio dual criterion | [entity-hallucination](../06_failure_modes/entity-hallucination.md) |
| Metric stack | [SPIDEr-FL](../05_metrics/spider-fl.md), [FENSE](../05_metrics/fense.md), CIDEr, SPICE, CLAPScore | [rq-index](../02_research_questions/rq-index.md) |
| Dataset | [Clotho v2.1 eval](../04_datasets/clotho-v2-1.md) (1,045 clips) | — |

If Layer 1 is complete, the project passes regardless of Layer 2 status.

## Layer 2 — Research-Grade Extension (modular ambition)

Each item is independent. Failure in any does not affect Layer 1.

| Cut order | Component | Cuts when |
|:---------:|:----------|:----------|
| 1 (drops first) | Qwen2.5-Omni ablation — see [qwen2-5-omni](../03_models/qwen2-5-omni.md) | Compute / time pressure |
| 2 | RQ4 — Temporal ordering — see [temporal-grounding-loss](../06_failure_modes/temporal-grounding-loss.md) | Synthetic-set construction blocked |
| 3 | Negative-control battery | Confabulation diagnostic infeasible |
| 4 (drops last) | RQ5 — Cultural heritage / Schafer — see [soundscape-schafer](../07_humanities/soundscape-schafer.md) | The humanities identity — protected |

> Operational details on cut decisions: [`implementation_plan.md`](../../../implementation_plan.md) (legacy synthesis context).

## Out of scope

- Model training, fine-tuning, or LoRA adaptation.
- Real-time / streaming inference.
- Non-English captioning.
- Proposing new metrics or architectures.
- Human evaluation study (no ethics-board approval timeline).

## Sources

- [`ch-proj-m-00-topics`](../08_sources/ch-proj-m-00-topics.md) — course topic catalog confirming T6 as the chosen topic and its dataset / RQ framing.
- [project-guide-legacy](../08_sources/project-guide-legacy.md) — canonical L1 / L2 scope split, RQ table, and cut order. Owner-authored project synthesis; this page summarises and cross-links it rather than restating.
