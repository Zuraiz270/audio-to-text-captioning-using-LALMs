---
title: "Entity Hallucination"
type: failure-mode
status: seed
created: 2026-04-21
updated: 2026-04-21
source_ids: []
source_files: [PROJECT_GUIDE.md]
source_tier: tier-b
canonical_url:
tags: [failure-mode, hallucination, rq3]
---

# Entity Hallucination

## Purpose

Define and track the second core failure mode: LALMs mention sounds not present in the audio, driven by LLM text priors.

## Key Points

- The LLM component generates text from learned co-occurrence patterns, not exclusively from acoustic input.
- Example: model outputs "birds chirping" because "park" appears in the prompt context, regardless of audio content.
- Measurement requires comparing generated entities against ground-truth event labels.

## Evidence

<!-- To be filled on ingest -->

## Open Questions

- Adaptation of CHAIR metric from vision to audio.
- Whether hallucination correlates with caption length or complexity.

## Links

- [RQ3: Hallucination](../02_research_questions/rq3-hallucination.md)
- [Reducing Hallucination](../08_sources/reducing-hallucination-2026.md)
- [FD-DeCap](../08_sources/fd-decap-2025.md)
- [CLAIRA](../08_sources/claira-2026.md)
