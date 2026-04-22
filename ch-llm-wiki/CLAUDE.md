# CLAUDE.md — LLM Wiki Operating Schema

This file defines the operating rules for any LLM maintaining this wiki.
It is the authoritative schema. All wiki operations must comply with it.

---

## 1. Purpose

This repository is a **persistent LLM-maintained wiki** for mastering the literature and producing project outputs on:

**Audio-to-Text Captioning using Large Audio-Language Models (LALMs)**

It serves a Computational Humanities Master's project (CH-Proj-M, SS 2026, Uni Bamberg).

The wiki sits between raw sources and answers. It accumulates structured knowledge over time. It is not notes. It is a compounding artifact.

---

## 2. Source Hierarchy and Evidence Rules

### Tier A — Canonical Registry

- `Credible Literature/info.txt`
- `Credible Literature/LALM_Synthesis_Matrix.md`

**Purpose:**
- Source-of-truth list of included papers.
- Source-of-truth thematic grouping seed.

### Tier B — Primary Source Documents

- Local PDFs in `raw/01_primary_sources/`
- Course slides or official course documents in `raw/00_course/`
- Other explicitly added official research documents.

### Tier C — Secondary / Supporting Materials

- Materials in `raw/02_secondary_sources/`
- Future notes, ancillary references, supplemental docs.

### Tier D — Generated Wiki Pages

- All markdown files in `wiki/`
- `index.md`
- `log.md`

### Rules

- Tier A defines the canonical source universe.
- Tier B contains the actual research evidence.
- Tier C may support context but not override primary evidence.
- Tier D must always cite back to Tier A, B, or C.
- No unsupported claim is allowed.
- If a paper exists in the wiki but not in `info.txt`, flag it as an error.
- If a paper exists in `info.txt` but lacks a source page in `wiki/08_sources/`, flag the wiki as incomplete.

---

## 3. Seed vs Ingest Distinction

This distinction is mandatory.

### Seed Page

A structural placeholder page created from canonical registry data only.

It may contain:
- title
- year
- venue
- URL
- source ID
- matrix section
- placeholder sections

It **must not** claim methodology, metrics, or findings unless those are read from an actual source document.

### Ingested Page

A source page that has been created or updated after reading the actual PDF / full text / official abstract.

It may contain:
- abstract summary
- method
- datasets
- metrics
- limitations
- RQ relevance
- cross-source synthesis

### Rules

- Do not pretend a seed is a full ingest.
- Log seed and ingest separately.
- A project can begin with all canonical papers seeded and only some papers fully ingested.

---

## 4. Page Model

Every wiki page must use frontmatter with this minimum schema:

```yaml
---
title:
type:
status:
created:
updated:
source_ids:
source_files:
source_tier:
canonical_url:
tags:
---
```

### Allowed `type` values

- `overview`
- `project`
- `research-question`
- `model`
- `dataset`
- `metric`
- `failure-mode`
- `humanities`
- `source-note`
- `comparison`
- `output`
- `glossary`

### Allowed `status` values

- `seed`
- `draft`
- `active`
- `reviewed`
- `final`
- `needs-review`
- `superseded`

### Allowed `source_tier` values

- `tier-a`
- `tier-b`
- `tier-c`
- `mixed`
- `generated`

---

## 5. Page Structure Rules

Each page should normally contain these sections unless clearly not needed:

- `## Purpose`
- `## Key Points`
- `## Evidence`
- `## Open Questions`
- `## Links`

### Rules

- One page = one main topic.
- Do not dump multiple topics into giant notes.
- Split pages when they become multi-topic.
- Prefer updating existing pages over creating duplicates.
- Use explicit internal links between relevant pages.

---

## 6. Citation Rules

Use simple inline repo-style citations:

- `(Source: Credible Literature/info.txt)`
- `(Source: Credible Literature/LALM_Synthesis_Matrix.md)`
- `(Source: raw/01_primary_sources/<file>.pdf)`
- `(Source: raw/00_course/<file>.pdf)`
- `(Source Page: wiki/08_sources/<paper>.md)`

For source-note pages, include short citation keys:
- `[Kim 2024; IEEE 10446672]`
- `[Smith 2025; ACM DOI ...]`

### Rules

- Claims about methods, metrics, results, and limitations must cite actual source documents when available.
- Registry metadata may cite Tier A.
- If a statement is inferred, label it `Inference:`.
- If unresolved, label it `Unresolved:`.
- If two sources disagree, label it `[CONFLICT]`.

---

## 7. Ingest Workflow

### For a new canonical source (seed)

1. Read `Credible Literature/info.txt`.
2. Identify paper metadata.
3. Create a seed source-note page in `wiki/08_sources/`.
4. Update `index.md`.
5. Append a `seed` entry to `log.md`.

### For a full source ingest

1. Read the actual PDF / full text / official abstract.
2. Update the corresponding `wiki/08_sources/` page.
3. Extract datasets, metrics, method, limitations, and RQ relevance.
4. Update affected thematic pages.
5. Update `index.md` if needed.
6. Append an `ingest` entry to `log.md`.

---

## 8. Query Workflow

When asked a question:

1. Read `index.md` first.
2. Identify the relevant wiki pages.
3. Read those pages.
4. Only go back to raw files when:
   - the wiki is missing evidence,
   - a contradiction must be resolved,
   - the question targets exact wording or numeric claims.
5. Answer from the wiki with citations.
6. If the answer creates durable value, update or create a wiki page.
7. Append a `query` or `revise` entry to `log.md`.

---

## 9. Lint Workflow

Periodically check for:

- Duplicate source pages.
- Stale claims.
- Unsupported statements.
- Orphan pages.
- Dead links.
- Papers in `info.txt` missing source pages.
- Source pages with no actual citations.
- Thematic pages with no supporting source pages.
- Pages mixing registry metadata with paper findings without labeling.
- Pages marked `ingested` without evidence of real ingest.

---

## 10. File-Boundary Rules

### Do not

- Modify raw sources.
- Store key findings only in `log.md`.
- Bury important synthesis only inside output pages.
- Duplicate the same content across many pages without purpose.

### Do

- Keep stable knowledge in thematic pages.
- Keep per-paper notes in `wiki/08_sources/`.
- Keep chronology only in `log.md`.
- Keep navigation current in `index.md`.

---

## 11. Logging Rules

`log.md` is append-only.

Every entry must begin with this heading format:

```
## [YYYY-MM-DD] action | item
```

### Allowed actions

- `setup`
- `seed`
- `ingest`
- `query`
- `revise`
- `lint`
- `cleanup-report`
- `cleanup-approved`

### Each entry must include

- What changed.
- Which files were touched.
- Why.
- Which sources justified the change.

---

## 12. Style Rules

- Plain, precise English.
- No motivational fluff.
- No generic AI filler.
- No uncited claims.
- Prefer compact reusable structure.
- Be explicit about uncertainty.
- Keep pages maintainable.
