---
title: SPIDEr-FL
type: metric
status: seed
created: 2026-04-21
updated: 2026-04-21
source_ids: []
source_files: []
source_tier: generated
canonical_url:
tags: [metric, spider-fl, primary, evaluation]
---

# SPIDEr-FL

## Purpose

Primary captioning metric for the project. Composite of SPICE and CIDEr with fluency penalty.

## Key Points

- SPIDEr = (SPICE + CIDEr) / 2.
- SPIDEr-FL adds a fluency penalty term.
- DCASE 2024 Task 6 baseline: 29.6% SPIDEr-FL.
- Reference-based metric requiring ground-truth captions.

## Evidence

<!-- To be filled on ingest -->

## Open Questions

- Whether SPIDEr-FL correlates well with human judgment for AAC specifically.
- Known failure cases of this metric.

## Links

- [CLAPScore](clapscore.md)
- [CLAPScore vs SPIDEr](../09_comparisons/clapscore-vs-spider.md)
- [RQ1: Baseline Parity](../02_research_questions/rq1-baseline-parity.md)
