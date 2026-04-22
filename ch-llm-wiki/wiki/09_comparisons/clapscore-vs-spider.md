---
title: CLAPScore vs SPIDEr
type: comparison
status: seed
created: 2026-04-21
updated: 2026-04-21
source_ids: []
source_files: []
source_tier: generated
canonical_url:
tags: [comparison, clapscore, spider, metrics]
---

# CLAPScore vs SPIDEr

## Purpose

Compare reference-free (CLAPScore) and reference-based (SPIDEr-FL) evaluation approaches.

## Key Points

| Dimension | CLAPScore | SPIDEr-FL |
|:---|:---|:---|
| **Type** | Reference-free | Reference-based |
| **Requires GT captions** | No | Yes |
| **Basis** | CLAP embedding similarity | SPICE + CIDEr |
| **Human correlation** | TBD | TBD |
| **Known biases** | TBD | TBD |

## Evidence

<!-- To be filled on ingest of MACE and CLAIRA papers -->

## Open Questions

- Which metric better captures polyphony and hallucination failures.
- Whether both should be reported or one preferred.

## Links

- [SPIDEr-FL](../05_metrics/spider-fl.md)
- [CLAPScore](../05_metrics/clapscore.md)
- [MACE](../08_sources/mace-2025.md)
- [CLAIRA](../08_sources/claira-2026.md)
