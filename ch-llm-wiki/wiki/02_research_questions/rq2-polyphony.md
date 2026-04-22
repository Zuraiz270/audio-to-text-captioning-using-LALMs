---
title: "RQ2: Polyphony Under-Description"
type: research-question
status: seed
created: 2026-04-21
updated: 2026-04-21
source_ids: []
source_files: [PROJECT_GUIDE.md]
source_tier: tier-b
canonical_url:
tags: [rq2, polyphony, failure-mode]
---

# RQ2: Polyphony Under-Description

## Purpose

**Primary Course Task:** "How accurately can LALMs describe overlapping sound events compared to traditional tagging?"

Do LALMs systematically under-describe concurrent sound events (polyphony), favouring dominant sources and dropping secondary ones, compared to tagging models which classify each event independently?

## Key Points

- Polyphony = multiple simultaneous sound events in a single audio clip.
- LALMs tend to describe the loudest or most salient event and silently omit others.
- Measurement: compare number of sound events in ground-truth captions vs. model output.

## Evidence

<!-- To be filled on ingest -->

## Open Questions

- Threshold for "under-description" — how many dropped events counts as failure?
- Whether SED-based event counting is reliable enough for ground truth.

## Links

- [Polyphony Under-Description](../06_failure_modes/polyphony-under-description.md)
- [SED Review](../08_sources/sed-review-2025.md)
- [Clotho v2.1](../04_datasets/clotho-v21.md)
