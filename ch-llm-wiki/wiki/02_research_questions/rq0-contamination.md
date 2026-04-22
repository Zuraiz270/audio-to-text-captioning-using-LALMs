---
title: "data-leakage: Contamination Audit"
type: research-question
status: seed
created: 2026-04-21
updated: 2026-04-21
source_ids: []
source_files: [PROJECT_GUIDE.md]
source_tier: tier-b
canonical_url:
tags: [data-leakage, contamination, zero-shot]
---

# data-leakage: Contamination Audit

## Purpose

Determine whether AF3's training data overlaps with Clotho v2.1 or AudioCaps test splits, which would invalidate zero-shot claims.

## Key Points

- AF3 claims emergent zero-shot captioning. This project treats that as testable, not a premise.
- Contamination audit must precede all other RQs — if the test set leaks into training, baseline parity results are meaningless.
- Audit method: compare AF3 training data manifest against Clotho/AudioCaps file IDs, audio fingerprints, and caption overlaps.

## Evidence

<!-- To be filled on ingest of relevant papers -->

## Open Questions

- Is AF3's full training data manifest publicly available?
- What level of overlap constitutes disqualifying contamination?
- How to handle indirect contamination (e.g., AudioSet overlap)?

## Links

- [Data Leakage Benchmark](../08_sources/data-leakage-benchmark-2026.md)
- [ALM Datasets Survey](../08_sources/alm-datasets-survey-2025.md)
- [Clotho v2.1](../04_datasets/clotho-v21.md)
- [AudioCaps](../04_datasets/audiocaps.md)

