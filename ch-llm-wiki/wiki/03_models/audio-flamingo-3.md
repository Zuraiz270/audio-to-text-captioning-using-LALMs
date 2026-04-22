---
title: Audio Flamingo 3
type: model
status: seed
created: 2026-04-21
updated: 2026-04-21
source_ids: []
source_files: []
source_tier: generated
canonical_url:
tags: [model, af3, primary, lalm]
---

# Audio Flamingo 3

## Purpose

Primary model under evaluation. AF3 is claimed to perform emergent zero-shot audio captioning.

## Key Points

- Developer: NVIDIA (Jul 2025).
- Architecture: unified AF-Whisper encoder + LLM decoder.
- Role in project: primary model for RQ0–RQ5.
- The zero-shot claim is treated as testable, not as a premise.

## Evidence

<!-- To be filled on ingest of AF3 paper -->

## Open Questions

- Full training data manifest availability for contamination audit.
- Exact encoder architecture details.
- Published benchmark scores on Clotho v2.1.

## Links

- [RQ0: Contamination](../02_research_questions/rq0-contamination.md)
- [RQ1: Baseline Parity](../02_research_questions/rq1-baseline-parity.md)
- [AF3 vs DCASE Baseline](../09_comparisons/af3-vs-dcase-baseline.md)
- [SALMONN](salmonn.md)
- [Qwen2.5-Omni](qwen25-omni.md)
