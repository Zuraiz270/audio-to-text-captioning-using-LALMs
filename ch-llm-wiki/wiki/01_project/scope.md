---
title: Project Scope
type: project
status: seed
created: 2026-04-21
updated: 2026-04-21
source_ids: []
source_files: [PROJECT_GUIDE.md]
source_tier: tier-b
canonical_url:
tags: [scope, boundaries]
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
- Course deliverables: ~15-page term paper (Jul 6), 15-minute talk (Jul 13).

### Out of Scope

- Training new models or fine-tuning LALMs.
- Speech recognition (ASR) or music transcription.
- Real-time or streaming audio captioning.
- Proposing new metrics.

### Two-Layer Structure

| Layer | Purpose | Risk Profile |
|:---|:---|:---|
| **Course-Safe Core** | RQ0 (contamination) + RQ1 (baseline parity) | Low — comparison study |
| **Research-Grade Extension** | RQ2–RQ5 (failure modes + cultural bias) | Higher — novel characterisation |

## Evidence

(Source: PROJECT_GUIDE.md §Problem Statement, §What This Project Does)

## Open Questions

- Exact scope boundary for RQ5 cultural-bias testing.
- Whether SALMONN and Qwen2.5-Omni comparisons are course-safe or extension-only.

## Links

- [Phase Map](phase-map.md)
- [RQ0](../02_research_questions/rq0-contamination.md)
- [RQ1](../02_research_questions/rq1-baseline-parity.md)
