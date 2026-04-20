# CLAUDE.md — LLM Wiki Schema for CH-Proj-M

*Master's Project · CH-Proj-M · SS 2026 · Zuraiz · Uni Bamberg · Prof. Abeßer*
*This file governs every Claude session that touches `ch-llm-wiki/`.*

---

## 0. First action of every new session

Before writing or editing anything in this wiki, every Claude session **must** in this exact order:

1. Read this file (`ch-llm-wiki/CLAUDE.md`) end-to-end.
2. Read `ch-llm-wiki/index.md` to map what already exists.
3. Read the **last 20 lines** of `ch-llm-wiki/log.md` to see what changed recently.

Only then act. This is non-negotiable. The schema is load-bearing.

---

## 1. Purpose & non-goals

**This wiki is** a persistent, compounding markdown knowledge base for the CH-Proj-M project (*Audio-to-Text Captioning using Large Audio-Language Models*). It sits **between raw sources and answers**: one file per concept, per source, per model, per dataset, per failure mode, per humanities frame. Every claim is traceable to a source card; every source card is traceable to a raw file in `raw/`.

**This wiki is NOT:**

- A chatbot or scratchpad.
- A replacement for the 5 root synthesis docs (`PROJECT_GUIDE.md`, `implementation_plan.md`, `literature_review.md`, `paper_summaries.md`, `research_notes.md`) — those remain the canonical synthesis.
- A generic notes folder. Every file follows the schema in §4.
- A place for ephemeral state. If something belongs to one session only, it belongs in conversation, not here.

---

## 2. Three-layer architecture

```
┌─────────────────────────────────────────────────────────┐
│  raw/       — IMMUTABLE source files (LLM read-only)    │
│              PDFs, papers, course slides, datasets,     │
│              experiment logs. Never edit. Never delete. │
└─────────────────────────────────────────────────────────┘
                           ▲
                           │  cited primary
                           │
┌─────────────────────────────────────────────────────────┐
│  wiki/      — LLM-MAINTAINED markdown graph             │
│              Per-concept pages, source cards, glossary, │
│              comparisons. Edit freely under the schema. │
└─────────────────────────────────────────────────────────┘
                           ▲
                           │  governed by
                           │
┌─────────────────────────────────────────────────────────┐
│  CLAUDE.md  — SCHEMA / RULES (this file)                │
│  index.md   — navigable map of every wiki page          │
│  log.md     — append-only audit trail                   │
└─────────────────────────────────────────────────────────┘
```

**Immutability rule:** files under `raw/` are read-only to every Claude session. To add a raw source, the user places the file there manually, or the LLM may copy a file into `raw/` *only* during a documented ingest (§7). The LLM **never** edits or deletes anything in `raw/`.

---

## 3. Folder conventions

### `raw/` — immutable inputs

| Folder | Holds | Examples |
|:-------|:------|:---------|
| `raw/00_course/` | Course-issued material | `CH-Proj-M-00-Topics.pdf`, syllabus, lecture slides |
| `raw/01_primary_sources/` | Peer-reviewed papers, primary research | Drossos 2020 PDF, AF3 paper |
| `raw/02_secondary_sources/` | Surveys, blog posts, technical reports, official docs | Mei 2022 survey, NVIDIA AF3 model card |
| `raw/03_legacy_synthesis/` | Pre-existing synthesis from outside this wiki | Dropped-in earlier draft notes (rare) |
| `raw/04_experiments/` | Raw experiment outputs (logs, JSON, CSV) | `results/contamination_audit.json`, model output dumps |
| `raw/assets/` | Figures, audio clips, supplementary media | Spectrograms, .wav samples |

### `wiki/` — LLM-maintained graph

| Folder | Holds | Page `type` field |
|:-------|:------|:------------------|
| `wiki/00_overview/` | Wiki orientation, how-to-use | `concept` |
| `wiki/01_project/` | Project scope, phase map, deliverables, deadlines | `concept` |
| `wiki/02_research_questions/` | RQ index + per-RQ pages | `concept` |
| `wiki/03_models/` | Model cards (one file per model) | `model-card` |
| `wiki/04_datasets/` | Dataset cards (one file per dataset) | `dataset-card` |
| `wiki/05_metrics/` | Metric cards (one file per metric) | `metric-card` |
| `wiki/06_failure_modes/` | Failure-mode pages | `failure-mode` |
| `wiki/07_humanities/` | Humanities framings (ekphrasis, soundscape, etc.) | `humanities-frame` |
| `wiki/08_sources/` | Source cards — one card per raw file in `raw/` | `source-card` |
| `wiki/09_comparisons/` | Pages reconciling contradictions between sources | `comparison` |
| `wiki/10_outputs/` | Per-experiment result pages | `output` |
| `wiki/11_glossary/` | Glossary stub (see §13) + per-term pages for high-value terms | `glossary-entry` |

**File naming:** all wiki files use `kebab-case.md`. INDEX files in a folder are `INDEX.md` (uppercase) and list every page in that folder.

---

## 4. Page schema

Every wiki page **must** open with YAML frontmatter, followed by a body that follows the skeleton for its `type`.

### Frontmatter (mandatory on every page)

```yaml
---
title: <human-readable title>
type: <one of: concept | model-card | dataset-card | metric-card | failure-mode | humanities-frame | source-card | comparison | output | glossary-entry>
tags: [<short, lowercase, hyphenated tags>]
status: <stub | draft | stable>
last_reviewed: YYYY-MM-DD
sources: [<relative paths to wiki/08_sources/*.md cards that back this page>]
---
```

`status` discipline:
- **stub** — page exists for cross-linking but body is mostly placeholders. May lack citations.
- **draft** — body is written but not yet verified against sources or peer-reviewed.
- **stable** — body is sourced, cross-linked, and reviewed within the last 90 days.

### Body skeletons by `type`

#### `source-card` (paper card format from `paper_summaries.md`)

```markdown
## <Title of source>

- **Raw file:** [`raw/NN_*/<filename>`](../../raw/NN_*/<filename>) ← primary basis
- **Venue / Level:** <venue> · **L1–L5** · **Year:** YYYY · **Link:** <DOI/URL>
- **Confidence / Applicability:** HIGH/MED/LOW / HIGH/MED/LOW

**Claim:** <one-sentence claim>
**Method:** <one-sentence method>
**Key numbers:** <numbers that future pages will cite>
**Threat to validity:** <known weakness>
**Feeds:** <list of RQs this source feeds — RQ0…RQ5 — and which wiki pages cite it>
**One-sentence reservation:** <what NOT to cite this source for>

### Notes
<extended notes; optional>

### Cross-links
- Cited by: [list of wiki pages that cite this source card]
- Legacy synthesis: [optional pointer to the relevant root-doc section]
```

#### `model-card`

```markdown
## <Model name>

| Field | Value |
|:------|:------|
| Family | <e.g., LALM, supervised AAC> |
| Released | <month YYYY by org> |
| Audio encoder | … |
| Adapter | … |
| LLM decoder | … |
| Parameters | … |
| Training data | … |
| Open weights | yes/no |

### Role in this project
<L1 / L2 / not used; what RQs it feeds>

### Known failure modes
<links to wiki/06_failure_modes/*.md pages>

### Sources
<bullet list of source-card links>
```

#### `dataset-card`

```markdown
## <Dataset name>

| Field | Value |
|:------|:------|
| Purpose | <captioning / tagging / retrieval / …> |
| Size | <clips × captions> |
| Splits | <train / dev / eval> |
| Sample rate | … |
| License | … |
| Canonical record | <Zenodo / DOI / URL> |

### Role in this project
<which RQ uses this dataset and how>

### Known issues
<contamination risk, label noise, etc.>

### Sources
<bullet list of source-card links>
```

#### `metric-card`

```markdown
## <Metric name>

| Field | Value |
|:------|:------|
| Formula / definition | … |
| Range | … |
| Reference-based? | yes/no |
| Implementation | <library + version> |
| Best for | … |
| Known limitations | … |

### Role in this project
<which RQ uses this metric and how>

### Sources
<bullet list of source-card links>
```

#### `failure-mode`

```markdown
## <Failure-mode name>

**Definition:** <one paragraph>
**Mechanism:** <why it happens — bottleneck, prior, etc.>
**How we measure it:** <metric, protocol>
**Which RQ:** <RQ tag>
**Affected models:** <links to model cards>

### Sources
<bullet list of source-card links>
```

#### `humanities-frame`

```markdown
## <Humanities concept>

**Tradition:** <classical rhetoric / soundscape studies / accessibility / …>
**Originating thinker(s):** <Schafer 1977, Heffernan 1993, …>
**Definition:** <one paragraph>
**Why it matters here:** <one paragraph linking to project RQs>

### Sources
<bullet list of source-card links>
```

#### `comparison`

```markdown
## <Topic on which sources disagree>

| Position | Source | Confidence | Applicability |
|:---------|:-------|:-----------|:--------------|
| A: …     | …      | HIGH       | HIGH          |
| B: …     | …      | MED        | LOW           |

**Resolution per CLAUDE.md §10:** <how we handle the conflict in this project>
```

#### `output`

```markdown
## <Experiment name> — <date>

| Field | Value |
|:------|:------|
| RQ | RQx |
| Model | … |
| Dataset / split | … |
| Seed | … |
| Metric | value (BCa CI lower, upper) |
| Raw artefact | [`raw/04_experiments/<file>`](../../raw/04_experiments/<file>) |

### Notes
<interpretation>
```

#### `glossary-entry`

```markdown
## <Term>

**Short definition:** <one sentence>
**Extended:** <up to 3 paragraphs — used when the term is contested, heavily cross-linked, or central to a humanities frame>

### See also
<links to related wiki pages>

### Sources
<bullet list of source-card links>
```

#### `concept` (catch-all for overview / project / RQ pages)

Any heading structure that fits the topic — but the frontmatter above is still mandatory.

---

## 5. Citation rules

The evidence chain is **claim → wiki page → source card → raw file**. Never short-circuit it.

1. **Every non-trivial claim** in any wiki page cites a source card under `wiki/08_sources/<slug>.md`.
2. **Every source card** under `wiki/08_sources/` **must cite the raw file** it summarizes (a file under `raw/`) as its **primary basis**, declared in the `Raw file:` line of the source-card body. A source card with no raw file is invalid.
3. **The 5 root synthesis docs** (`PROJECT_GUIDE.md`, `implementation_plan.md`, `literature_review.md`, `paper_summaries.md`, `research_notes.md`) may be referenced **only as secondary cross-links or legacy synthesis context** — for example: *"synthesized further in [`literature_review.md`](../../literature_review.md) §4"*. They **must never** be the primary basis for a claim on a source card or a concept page. If a wiki page can only cite a root doc, it is `status: stub` until a real source is ingested.
4. **Inline EBSE evidence badges** are reused verbatim from `literature_review.md`: `[Author Year; Lx; CONF/APPLIC]` (e.g., `[Drossos 2020; L2; HIGH/HIGH]`). Levels: L1 official docs · L2 peer-reviewed · L3 standards/RFCs · L4 codebase · L5 verified community.
5. **Unsourced claims** are written verbatim with the marker `[UNSOURCED]` immediately after the claim. Lint flags these. They must be either (a) sourced via ingest, or (b) deleted.
6. **Concept pages** (models, datasets, metrics, failure modes, humanities frames) cite source cards in their `Sources` section — never raw files directly. The chain is enforced by the structure.

---

## 6. Cross-link rules

1. **Internal links** between wiki pages use **relative markdown paths** — e.g., `[Polyphony under-description](../06_failure_modes/polyphony-under-description.md)`.
2. **Source cards** are linked from the `sources:` frontmatter field *and* the body `Sources` section.
3. **Orphan pages** — any wiki page with zero inbound links from other wiki pages — are flagged by lint (§9). Either link to it or delete it.
4. **Bidirectional discoverability:** if page A cites source card S, then S's `Cross-links → Cited by` list **must** mention A.

---

## 7. Ingest workflow

When a new raw source enters the project, follow these 7 steps in order. Skipping a step breaks the wiki's evidence chain.

1. **Place the raw file** in the correct `raw/NN_*/` folder. Filename uses kebab-case where possible. The user may place it manually; the LLM may copy it during ingest if instructed.
2. **Create a source card** at `wiki/08_sources/<slug>.md` using the `source-card` schema (§4). The `Raw file:` field cites the file from step 1 as primary basis.
3. **Extract claims** from the raw source. For each non-trivial claim:
   - If a relevant concept/model/dataset/metric/failure-mode/humanities page already exists, *update* it with the new claim and a citation to the new source card.
   - Otherwise, create a new wiki page under the appropriate folder, with frontmatter and the right body skeleton.
4. **Update affected pages:** add the source card to their `sources:` frontmatter list and `Sources` body section. Bump their `last_reviewed` to today's date.
5. **Update `wiki/08_sources/INDEX.md`** with a new row for the source card.
6. **Append a log entry** to `log.md` for the ingest itself *and* one for each page created or edited.
7. **Run lint mentally** (§9): no broken links, no missing frontmatter, no orphan pages, no `[UNSOURCED]` markers introduced.

---

## 8. Query workflow

When the user asks a question that the wiki can answer:

1. Read `index.md` to find candidate pages.
2. Read those pages and follow their `sources:` to source cards.
3. Read source cards to confirm the cited raw file actually backs the claim. Trust the chain only when it holds.
4. Compose the answer **from cited content**. Inline-cite the source card(s) you used: e.g., *"per [Drossos 2020; L2; HIGH/HIGH] (`wiki/08_sources/drossos-2020.md`)"*.
5. **Never fabricate.** If a claim has no source card, mark it `[UNSOURCED]` in the answer and propose an ingest.
6. **Never paraphrase past the evidence.** If the source says "29.6% on Clotho-eval," do not generalize to "around 30%" without saying the source is exact.

---

## 9. Lint workflow

Run lint when asked, after a large ingest, or before declaring the wiki "ready for handover." Lint checks (in order):

1. **Frontmatter present and complete** on every `.md` file under `wiki/` (except `INDEX.md`, which has only `# Title` + a table).
2. **Broken internal links** — every `[text](path)` that points inside `ch-llm-wiki/` resolves.
3. **Orphan pages** — any page with zero inbound links from other wiki pages.
4. **`[UNSOURCED]` markers** — list every occurrence with file + line.
5. **Stale `last_reviewed`** — any page where `last_reviewed` > 90 days old, status `stable`. Demote to `draft` or refresh.
6. **Duplicate slugs** — any two files with the same kebab-case slug across different folders.
7. **Source-card raw-file check** — every `wiki/08_sources/*.md` has a `Raw file:` line that points to an existing file under `raw/`.
8. **Citation-rule check** — no source card has its primary basis on a root doc.

Output: a markdown report, one section per check, with file paths and line numbers. Append a `LINT` entry to `log.md`.

---

## 10. Contradiction handling

When two sources disagree on a fact relevant to this project:

1. Create or update `wiki/09_comparisons/<topic>.md` using the `comparison` body skeleton (§4).
2. Each row names a position, the source card backing it, and the Confidence/Applicability per the user's global EBSE rubric (`~/.claude/CLAUDE.md` §3.2).
3. Apply the conflict resolution order from the user's global EBSE protocol: **Hierarchy (L1 > L3) → Regulatory (Law > Performance) → Recency → Specificity**.
4. State the resolution explicitly. If unresolvable from current evidence, flag `[LOW-CONFIDENCE]` and recommend further ingest.
5. Cross-link the comparison page from every concept page that touches the disputed fact.

---

## 11. Logging behavior

Every state change appends one line to `ch-llm-wiki/log.md` in this format:

```
YYYY-MM-DD HH:MM | <ACTION> | <relative path> | <one-line summary>
```

Action vocabulary:
- `INGEST`  — a new raw source was added and its source card created.
- `CREATE`  — a new wiki page was created.
- `EDIT`    — an existing wiki page was modified.
- `LINT`    — lint was run; summary names the report file or "all clean".
- `RENAME`  — a wiki page was renamed (note old → new in the summary).
- `DELETE`  — a wiki page was deleted (rare; document why in the summary).

The log is append-only. Never edit or delete past lines.

---

## 12. File boundaries

The LLM, when working in this wiki:

| Action | Where |
|:-------|:------|
| **May read** | Anywhere on the user's machine (filesystem-permitting). |
| **May create / edit / delete** | Inside `ch-llm-wiki/wiki/`, plus `ch-llm-wiki/index.md` and `ch-llm-wiki/log.md`. |
| **May copy into (only during a documented ingest)** | `ch-llm-wiki/raw/NN_*/` — and only the new file being ingested. |
| **May NEVER edit, rename, or delete** | Any existing file under `ch-llm-wiki/raw/`. |
| **May NEVER edit, rename, or delete** | The 5 root docs (`PROJECT_GUIDE.md`, `implementation_plan.md`, `literature_review.md`, `paper_summaries.md`, `research_notes.md`) without explicit user approval per session. |
| **May NEVER edit** | This file (`ch-llm-wiki/CLAUDE.md`) without explicit user approval per session — it is the schema. |

If a user request would cross a "NEVER" boundary, the LLM must stop and ask for explicit permission for that specific action before proceeding.

---

## 13. Relationship to root docs

The 5 root docs are the **canonical synthesis** of the project — written and maintained by the user, EBSE-compliant, peer-review-hardened. The wiki **summarizes, atomizes, and cross-links** them; it does **not** replace them.

| Root doc | Owns | The wiki uses it for |
|:---------|:-----|:---------------------|
| `PROJECT_GUIDE.md` | Scope, two-layer split, glossary, document map | Cross-link from `wiki/01_project/`, `wiki/11_glossary/` |
| `implementation_plan.md` | Determinism pins, hardware gates, kill criteria, code stubs | Cross-link from `wiki/03_models/`, `wiki/05_metrics/`, `wiki/10_outputs/` |
| `literature_review.md` | Evidence narrative, EBSE badges, ekphrasis + Schafer §13 | Cross-link from `wiki/06_failure_modes/`, `wiki/07_humanities/` |
| `paper_summaries.md` | Per-paper structured cards (Claim/Method/...) | Card schema reused for source cards in `wiki/08_sources/` |
| `research_notes.md` | Strategic framing, open questions, expansion strategy | Cross-link from `wiki/02_research_questions/` |

**Drift rule:** if a wiki page's content disagrees with the root doc, **the root doc wins**. Correct the wiki page, log an `EDIT`, and add a cross-link to the authoritative root-doc section.

### Glossary policy (§13.1)

`PROJECT_GUIDE.md` §Glossary holds the **canonical 20-term short glossary**. `wiki/11_glossary/README.md` links to it as the source of truth and **does not duplicate** the full list.

However, `wiki/11_glossary/` is **explicitly allowed to grow** lightweight per-term entry pages over time — for example `wiki/11_glossary/keynote-sound.md`, `wiki/11_glossary/ekphrasis.md`, `wiki/11_glossary/spider-fl.md` — when a term is:

- heavily cross-linked across multiple wiki pages, or
- contested between sources (then often paired with a `wiki/09_comparisons/` page), or
- needs extended discussion beyond the one-line glossary entry.

Each per-term page uses the `glossary-entry` schema (§4) and cites the raw sources behind the term. Glossary support is **not** frozen at README-only.

---

## 14. Conventions for new sessions (recap)

1. Read `CLAUDE.md`, `index.md`, last 20 lines of `log.md` (§0).
2. When the user adds a source: run the ingest workflow (§7).
3. When the user asks a question: run the query workflow (§8).
4. Before declaring "done" on a large change: run lint (§9).
5. When two sources disagree: create or update a comparison page (§10).
6. Every change appends to `log.md` (§11).
7. Stay inside the file boundaries (§12).
8. Defer to root docs on conflicts (§13).
