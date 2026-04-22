---
title: "Temporal Grounding Loss"
type: failure-mode
status: seed
created: 2026-04-21
updated: 2026-04-21
source_ids: []
source_files: [PROJECT_GUIDE.md]
source_tier: tier-b
canonical_url:
tags: [failure-mode, temporal, grounding, temporal]
---

# Temporal Grounding Loss

## Purpose

Define and track the third core failure mode: LALMs describe events in canonical text-prior order rather than actual onset order.

## Key Points

- Language models have learned default event orderings from text corpora.
- When audio contains events in a non-canonical order, the model may reorder them to match text priors.
- This is distinct from hallucination — the events are real, but their temporal relationships are wrong.

## Evidence

<!-- To be filled on ingest -->

## Open Questions

- How to measure temporal accuracy systematically.
- Whether any existing LALM explicitly addresses temporal grounding.

## Links

- [Crab AV](../08_sources/crab-av-2025.md)

