---
title: Research Questions — Index
type: concept
tags: [rq, research-questions, hypotheses]
status: stable
last_reviewed: 2026-04-20
sources: [../08_sources/project-guide-legacy.md, ../08_sources/research-notes-legacy.md]
---

## RQ0 – RQ5

| RQ | Question | Primary metric | Layer | Solved-if | Falsified-if |
|:---|:---------|:---------------|:-----:|:----------|:-------------|
| **RQ0** | Does AF3's training data overlap with Clotho-eval? ([dedicated page](rq0-contamination.md)) | Contamination % | L1 | Audit completes with disclosed overlap % | — (descriptive) |
| **RQ1** | Does AF3 (claimed-zero-shot, RQ0-tested) outperform the DCASE 2024 baseline on Clotho-eval? | [SPIDEr-FL](../05_metrics/spider-fl.md) + BCa CI | L1 | AF3 SPIDEr-FL BCa CI lower bound > 29.6% | CI lower bound ≤ 29.6% + 1.04 pp MDE |
| **RQ2** | Is the AF3-baseline gap larger on polyphonic clips than monophonic? | Δ SPIDEr-FL | L1 | Δ(poly − mono) significantly > 0 | Δ within MDE or negative |
| **RQ3** | (H3) What is AF3's absolute entity-hallucination rate? (H4) AF3 vs SALMONN gap? | CHAIR-audio dual criterion | L1 | H3: hallucination rate < pre-registered ceiling; H4: AF3 < SALMONN by ≥ 5 pp | H3 above ceiling; H4 CIs overlap or INDETERMINATE under {0.20, 0.25, 0.30} sensitivity |
| **RQ4** | Do LALMs correctly order events in synthetic A-then-B mixtures? | Correct-ordering rate | L2 | Rate ≤ 60% for LALMs | Rate > 80% (mechanism weakened) |
| **RQ5** | Do LALMs generalise to culturally-grounded audio outside FreeSound? | Descriptive (Schafer-framed qualitative audit); CLAPScore as secondary indicator [LOW–MED applicability] | L2 | Qualitative soundmark gaps visible in captions | Soundmark gaps absent in qualitative audit |

## Failure-mode mapping

- **RQ2** ↔ [polyphony-under-description](../06_failure_modes/polyphony-under-description.md)
- **RQ3** ↔ [entity-hallucination](../06_failure_modes/entity-hallucination.md)
- **RQ4** ↔ [temporal-grounding-loss](../06_failure_modes/temporal-grounding-loss.md)
- **RQ5** ↔ [soundscape-schafer](../07_humanities/soundscape-schafer.md)

## Layer assignment

- **L1 (Course-Safe Core):** RQ0, RQ1, RQ2, RQ3 — must ship.
- **L2 (Research-Grade Extension):** RQ4, RQ5 — modular ambition; cut ladder per [scope](../01_project/scope.md).

> *Canonical RQ section with rationale, hypotheses, and pre-registration:* [`PROJECT_GUIDE.md` §Research Questions](../../../PROJECT_GUIDE.md), [`research_notes.md`](../../../research_notes.md), [`implementation_plan.md` §Null Hypotheses](../../../implementation_plan.md) (legacy synthesis context).

## Sources

- [project-guide-legacy](../08_sources/project-guide-legacy.md) — canonical RQ table (RQ0–RQ5), null hypotheses, primary metric per RQ, and L1 / L2 layer assignment.
- [research-notes-legacy](../08_sources/research-notes-legacy.md) — strategic positioning of the RQs (Wohlin §6 design matrix; architecture-axis SALMONN → AF3 → TAC); 7 open questions framing the RQ design.

*This page is a structured index. Per-RQ pages with their own source cards may be added as the wiki grows.*
