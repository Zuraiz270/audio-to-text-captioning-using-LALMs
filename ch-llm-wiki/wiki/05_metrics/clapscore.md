---
title: CLAPScore
type: metric
status: seed
created: 2026-04-21
updated: 2026-04-21
source_ids: []
source_files: []
source_tier: generated
canonical_url:
tags: [metric, clapscore, reference-free]
---

# CLAPScore

## Purpose

Reference-free evaluation metric. Computes cosine similarity between audio and text embeddings in CLAP space.

## Key Points

- Does not require ground-truth captions.
- Based on LAION-CLAP joint audio-text embeddings.
- Useful for evaluating captioning when reference captions are unavailable or low quality.
- Complementary to reference-based metrics like SPIDEr-FL.

## Evidence

<!-- To be filled on ingest -->

## Open Questions

- How well CLAPScore correlates with human judgment vs SPIDEr-FL.
- Known biases in CLAP embedding space.

## Links

- [SPIDEr-FL](spider-fl.md)
- [CLAPScore vs SPIDEr](../09_comparisons/clapscore-vs-spider.md)
