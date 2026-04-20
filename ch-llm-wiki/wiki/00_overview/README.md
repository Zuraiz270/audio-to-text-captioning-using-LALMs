---
title: Wiki Overview
type: concept
tags: [overview, orientation, how-to-use]
status: stable
last_reviewed: 2026-04-20
sources: []
---

## What this wiki is

A persistent, compounding markdown knowledge base for the CH-Proj-M Master's project on **Audio-to-Text Captioning using Large Audio-Language Models (LALMs)**. It sits between raw sources (`raw/`) and answers, atomizing the project's knowledge into per-concept pages with strict citation discipline.

It is **not** a replacement for the 5 root synthesis docs ([`PROJECT_GUIDE.md`](../../../PROJECT_GUIDE.md), [`implementation_plan.md`](../../../implementation_plan.md), [`literature_review.md`](../../../literature_review.md), [`paper_summaries.md`](../../../paper_summaries.md), [`research_notes.md`](../../../research_notes.md)). Those remain the canonical synthesis. The wiki summarizes, atomizes, and cross-links them — and absorbs new sources via a disciplined ingest workflow.

## How to read it

1. Start at [`index.md`](../../index.md) to see the map.
2. Follow the folder you need: project scope, models, datasets, metrics, failure modes, humanities frames, sources, comparisons, outputs, glossary.
3. Every claim cites a source card under [`wiki/08_sources/`](../08_sources/INDEX.md). Every source card cites a raw file under `raw/`. Trust the chain.
4. If a page is `status: stub`, it exists as a cross-link target but has not yet been backed by a real source ingest.

## How to extend it

1. Read [`CLAUDE.md`](../../CLAUDE.md) end-to-end — it is the schema.
2. To add a new source: place the file in the right `raw/NN_*/` folder, then run the ingest workflow ([`CLAUDE.md` §7](../../CLAUDE.md)).
3. To answer a question: run the query workflow ([`CLAUDE.md` §8](../../CLAUDE.md)).
4. To validate the wiki state: run the lint workflow ([`CLAUDE.md` §9](../../CLAUDE.md)).
5. Every change appends one line to [`log.md`](../../log.md).

## Boundaries

- **Read** anything.
- **Write** only inside [`wiki/`](../), [`index.md`](../../index.md), [`log.md`](../../log.md).
- **Never edit** anything in [`raw/`](../../raw/) or any of the 5 root docs without explicit per-session approval.

Full file boundaries: [`CLAUDE.md` §12](../../CLAUDE.md).
