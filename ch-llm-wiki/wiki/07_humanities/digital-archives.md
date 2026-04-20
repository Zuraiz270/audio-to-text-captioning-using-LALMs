---
title: Digital Archives & Cultural Heritage Audio
type: humanities-frame
tags: [humanities, archives, british-library, bbc, europeana, cultural-heritage]
status: stub
last_reviewed: 2026-04-20
sources: [../08_sources/paper-summaries-legacy.md, ../08_sources/literature-review-legacy.md]
---

## Digital archives & cultural heritage audio

**Tradition.** Library and archival science / digital humanities / sound studies.

**Definition.** Major national and trans-national sound archives hold millions of recordings — oral histories, broadcast material, field recordings, sound effects — but **lack a systematic free-text caption layer**. The recordings are findable by title and metadata only, not by content.

| Archive | Holdings | Free-text captions? |
|:--------|:---------|:--------------------|
| British Library Sound Archive | > 6.5M recordings | No systematic layer |
| BBC Sound Effects Archive | > 33,000 CC-licensed clips | No systematic layer |
| Europeana Sounds | Trans-national aggregator | No systematic layer |

**Why it matters here.** This frame supplies the project's **deployment horizon**. AAC is not just a benchmark task — it is the technical precondition for semantic search and retrieval over these collections. RQ5 is the project's small-scale rehearsal of that deployment: applying AF3 to culturally-grounded audio (Bamberg soundmarks per [soundscape-schafer](soundscape-schafer.md)) and observing where it fails when the audio is **outside** the FreeSound / AudioSet training distribution.

The connection is direct:

- Cultural-heritage archives contain a high density of [soundmarks](soundscape-schafer.md) — by definition local, named, culturally-anchored.
- LALM training corpora are geographically flat and culturally-thin.
- Therefore, deploying current LALMs on these archives without measurement risks systematically erasing culturally-specific content from the auto-generated description layer.

### See also

- [soundscape-schafer](soundscape-schafer.md) — the ontological frame for what gets erased.
- [accessibility](accessibility.md) — who is harmed when description fails.

### Sources

- [paper-summaries-legacy](../08_sources/paper-summaries-legacy.md) — covers academic humanities (S4–S12) but contains **no dedicated card** for archive-side documentation. `[UNSOURCED-PRIMARY: British Library Sound Archive documentation]` `[UNSOURCED-PRIMARY: BBC Sound Effects Archive]` `[UNSOURCED-PRIMARY: Europeana Sounds]` — pending direct ingest into [`raw/02_secondary_sources/`](../../raw/02_secondary_sources/) (institutional documentation pages are L1 official docs and should be primary). This page remains thinly-cited even via legacy — flagged for explicit raw-file deposit.
- [literature-review-legacy](../08_sources/literature-review-legacy.md) — **substantial improvement over paper-summaries-legacy coverage:** §1.2 names DARIAH-EU 2023, British Library Sound Archive (> 6.5M recordings), BBC Sound Effects (> 33,000 CC-licensed clips), and Europeana Sounds as the deployment-horizon archives lacking systematic free-text caption layers. Direct ingest of institutional documentation pages still recommended for L1-grade primary citations.

> Legacy synthesis context: [`PROJECT_GUIDE.md` §Why This Matters → Cultural Archiving](../../../PROJECT_GUIDE.md), [`literature_review.md` §13](../../../literature_review.md).
