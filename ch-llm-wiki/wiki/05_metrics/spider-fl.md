---
title: SPIDEr-FL
type: metric
status: seed
created: 2026-04-21
updated: 2026-05-25
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
- Project baseline (DCASE 2023 Task 6A, CNN14+BART): 26.1% SPIDEr-FL (reproduced locally 25.9%). For reference, the DCASE 2024 ConvNeXt-Tiny baseline scores 29.6% — a different, stronger model not used as our baseline.
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
