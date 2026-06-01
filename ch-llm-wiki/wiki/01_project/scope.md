---
title: Project Scope
type: project
status: active
created: 2026-04-21
updated: 2026-05-17
source_ids: []
source_files: [PROJECT_GUIDE.md]
source_tier: tier-b
canonical_url:
tags: [scope, boundaries, zero-shot]
---

# Project Scope

## Purpose

Define what this project does and does not do.

(Source: PROJECT_GUIDE.md)

## Key Points

### Course Assignment Scope
- **Topic:** T6: Audio-to-Text Captioning using Large Audio-Language Models (LALMs)
- **Definition:** Moving beyond simple classification, sound event captioning describes complex acoustic scenes in natural language.
- **Task:** Utilize state-of-the-art LALMs to "write" descriptions of audio clips.
- **Primary Research Question:** How accurately can LALMs describe overlapping sound events compared to traditional tagging?
- **Target Dataset:** Clotho or AudioCaps (typical for these models).

### In Scope

- Pre-registered head-to-head comparison: AF3 vs DCASE 2024 baseline on Clotho v2.1.
- Contamination audit of AF3 training data against Clotho/AudioCaps.
- Structured characterisation of three failure modes: polyphony under-description, entity hallucination, temporal grounding loss.
- Bootstrap confidence intervals (BCa) for metric comparisons.
- Humanities framing via ekphrasis and soundscape studies.
- Course deliverables: 4–6 page IEEE two-column Term Paper (Jul 6) requiring an AI Transparency Statement and Code Repository Link, plus a 15-minute talk (Jul 13).

### Out of Scope

- Training new models or fine-tuning LALMs.
- Speech recognition (ASR) or music transcription.
- Real-time or streaming audio captioning.
- Proposing new metrics.

### Why zero-shot — rationale

The decision to evaluate **only with pretrained weights, no fine-tuning** is a deliberate methodological choice. It is *not* mandated by any specific paper in our 49-source corpus; rather, it is the consequence of the project's research question and constraints.

**1. The research question itself.** RQ2 asks *"how accurately do LALMs describe overlapping sound events compared to traditional tagging?"* The interesting thing to measure is the **baseline behaviour** of these pretrained models — what the world actually deploys — not their potential after task-specific adaptation. Fine-tuning would change the thing we are studying.

**2. Model-vs-model comparison cleanliness.** Falcon3-Audio, SALMONN, and Qwen2.5-Omni differ in scale (3 B vs. 13 B vs. ~11 B parameters), training corpus, and architectural choices. Adding a fine-tuning stage would introduce yet another degree of freedom — learning rate, schedule, data subset — and confound the model-level comparison.

**3. Field convention.** Falcon3-Audio [IEEE ASRU 2025, doc 11434596], SALMONN [ICLR 2024], and Qwen2.5-Omni [2025 tech report] all report their Clotho/AudioCaps SPIDEr scores as the pretrained model's **out-of-the-box behaviour**. Reporting zero-shot cross-corpus performance is the field default for AAC evaluation papers. This is convention, not a mandate.

**4. Reproducibility.** Zero-shot runs are deterministic given seed and weights — anyone with the public model checkpoint can re-execute them. Fine-tuning runs depend on GPU model, data shard order, mixed-precision settings, and dozens of other implementation details. The project's [AI Transparency Statement requirement](PROJECT_GUIDE.md) is materially easier to satisfy for zero-shot evaluation.

**5. Compute and time constraints.** Fine-tuning a 3 B+ parameter LALM on Clotho dev requires GPU resources outside a one-semester student-project budget. Zero-shot inference fits on a single 24 GB GPU for Falcon3-3B and on a university-cluster A100 for Qwen2.5-Omni.

#### Acknowledged asymmetry

The DCASE 2023 Task 6A reference baseline — **CNN14 at SPIDEr-FL ≈ 26.1%** (reproduced locally at 25.9%) — *is* fine-tuned on Clotho dev. So we are comparing zero-shot LALMs against a fine-tuned tagger. This is not apples-to-apples, but the comparison is still informative:

- If LALMs **match or exceed** the fine-tuned CNN14 zero-shot, that is a *stronger* claim than match-after-fine-tuning.
- If LALMs **fall short**, that is also informative — it characterises the cost of using these models off-the-shelf.

#### Why this is *not* in tension with the "zero-shot illusion"

The [ALM Datasets Survey 2025](../04_datasets/alm-datasets-survey-2025.md) argues that zero-shot claims for LALMs are often **unverified** because pretraining corpora (e.g., AudioSet) silently overlap evaluation sets (e.g., AudioCaps, AudioSet-derived). That paper is a *critique* of unverified zero-shot, not a prescription against zero-shot evaluation. It is precisely **the motivation for our contamination audit** (P2 slide 5) — to make our zero-shot claim defensible rather than assumed.

Inference: zero-shot is the correct evaluation protocol for this project, *provided* the contamination audit confirms the test data does not appear in the LALMs' training manifests. The audit is the verification step; the protocol is the choice.

### Two-Layer Structure

| Layer | Purpose | Risk Profile |
|:---|:---|:---|
| **Course-Safe Core** | data-leakage (contamination) + RQ1 (baseline parity) | Low — comparison study |
| **Research-Grade Extension** | RQ2–RQ5 (failure modes + cultural bias) | Higher — novel characterisation |

## Evidence

(Source: PROJECT_GUIDE.md §Problem Statement, §What This Project Does)

## Open Questions

- Exact scope boundary for RQ5 cultural-bias testing.
- Whether SALMONN and Qwen2.5-Omni comparisons are course-safe or extension-only.

## Links

- [Phase Map](phase-map.md)
- [RQ1](../02_research_questions/rq1-baseline-parity.md)

