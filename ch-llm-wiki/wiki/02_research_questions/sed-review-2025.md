---
title: "A Systematic Literature Review on Sound Event Detection and Classification"
type: source-note
status: draft
created: 2026-04-21
updated: 2026-04-22
source_ids: [IEEE-10988199]
source_files: []
source_tier: tier-a
canonical_url: https://ieeexplore.ieee.org/document/10988199/
tags: [source-note, matrix-section-1, sed, slr, classification, polyphony]
---

# A Systematic Literature Review on Sound Event Detection and Classification

| Field | Value |
|:---|:---|
| **Year** | 2025 |
| **Venue** | IEEE Conference |
| **Source ID** | IEEE-10988199 |
| **URL** | https://ieeexplore.ieee.org/document/10988199/ |
| **Matrix Section** | 1 — Surveys & Benchmarks |

## Abstract Summary

Systematic literature review on Sound Event Detection (SED) and classification. SED is the backbone task for identifying and localising sound events in audio recordings — the prerequisite for audio captioning. Covers detection methods, classification taxonomies, evaluation protocols, and polyphonic sound handling.

(Source: IEEE Xplore introduction context)

## Key Contributions

- Systematic literature review following PRISMA or equivalent SLR methodology.
- Covers SED methods from traditional to deep learning approaches.
- Addresses polyphonic sound event detection — critical for understanding concurrent events.
- Provides classification taxonomy for sound events.

## Datasets Used

- Survey covering SED datasets (DCASE challenge datasets, UrbanSound, etc.)

## Metrics Reported

- Survey of SED evaluation metrics (F1, ER, segment-based, event-based)

## Relevance to RQs

- **RQ2 (Polyphony):** SED is the foundation for detecting concurrent events. If SED fails, captioning cannot describe polyphonic scenes.
- **RQ4 (Temporal):** Event-based SED provides onset/offset timing for temporal grounding.

## Links

- [Polyphony Under-Description](../06_failure_modes/polyphony-under-description.md)
- [RQ2: Polyphony](../02_research_questions/rq2-polyphony.md)
- [Beyond the Status Quo](beyond-status-quo-2023.md)
