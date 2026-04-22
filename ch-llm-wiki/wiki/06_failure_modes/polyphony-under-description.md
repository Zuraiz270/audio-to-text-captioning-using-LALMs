---
title: "Polyphony Under-Description"
type: failure-mode
status: seed
created: 2026-04-21
updated: 2026-04-21
source_ids: []
source_files: [PROJECT_GUIDE.md]
source_tier: tier-b
canonical_url:
tags: [failure-mode, polyphony, rq2]
---

# Polyphony Under-Description

## Purpose

Define and track the first core failure mode: LALMs describe the dominant sound and silently drop concurrent secondary events.

## Key Points

- When multiple sounds overlap, models tend to caption only the loudest or most salient source.
- This is a structural limitation, not a random error — driven by how audio encoders compress polyphonic scenes.
- Relevant to any real-world audio with concurrent events (traffic + birds + speech).

## Evidence

<!-- To be filled on ingest -->

## Open Questions

- Relationship between encoder architecture and polyphony sensitivity.
- Whether attention visualisation can reveal which events are dropped.

## Links

- [RQ2: Polyphony](../02_research_questions/rq2-polyphony.md)
- [SED Review](../08_sources/sed-review-2025.md)
