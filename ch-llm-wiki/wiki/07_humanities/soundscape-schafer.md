---
title: Soundscape — Keynote / Soundmark / Signal (Schafer 1977)
type: humanities-frame
tags: [humanities, soundscape, schafer, keynote, soundmark, rq5]
status: stub
last_reviewed: 2026-04-20
sources: [../08_sources/paper-summaries-legacy.md, ../08_sources/literature-review-legacy.md]
---

## Soundscape studies — Schafer's tripartite ontology

**Tradition.** Acoustic ecology / sound studies.
**Originating thinker.** R. Murray Schafer, *The Tuning of the World* (1977) — extended by Barry Truax (1984), Augoyard & Torgue (2006), Jonathan Sterne (2012), Georgina Born (2013).

**Definition.** Schafer 1977 partitions the soundscape into three categories of cultural-acoustic object:

| Category | Definition | Example |
|:---------|:-----------|:--------|
| **Keynote sound** | The continuous, often unattended background sound of a place — its acoustic ground. | Wind, traffic hum, surf. |
| **Sound signal** | A foreground sound consciously listened to — informational, often functional. | Sirens, alarms, whistles. |
| **Soundmark** | A community-specific sound of cultural identity — a "sonic landmark." | Bamberg Martinskirche bells; Big Ben; specific muezzin call. |

**Why it matters here.** A LALM trained on web-scraped audio (FreeSound + AudioSet derivatives) has structurally **uneven priors** across these three categories:

- **Strong priors for sound signals** (sirens, alarms — over-represented in safety / urban training corpora).
- **Moderate priors for keynote sounds** (wind, traffic — common but unattended in training).
- **Structurally absent priors for soundmarks** — they are by definition local and culturally-specific, so they do not appear in geographically-flat web training corpora.

This asymmetry is the **mechanism behind RQ5**: when AF3 is asked to caption a recording of Bamberg's Martinskirche bells, it should default to a generic "church bells ringing" rather than identifying the soundmark, because the soundmark is structurally absent from training. Measuring this gap is how the project gets a humanistic conclusion out of a quantitative ML benchmark.

**RQ5 success criterion:** qualitative soundmark gaps are visible in captions of culturally-grounded audio. **Falsified if** CLAPScore Δ < 0.05 vs. in-distribution audio (gap is not measurable).

### See also

- [ekphrasis](ekphrasis.md) — the rhetorical-tradition complement to Schafer's ontology.
- [digital-archives](digital-archives.md) — where soundmarks live (British Library, Europeana Sounds).

### Sources

- [paper-summaries-legacy](../08_sources/paper-summaries-legacy.md) — Paper S4 (Schafer 1977 ⭐), Paper S8 (Truax 1984), Paper S9 (Augoyard & Torgue 2006), Paper S10 (Sterne 2012), Paper S11 (Born 2013). `[UNSOURCED-PRIMARY: Schafer 1977]` `[UNSOURCED-PRIMARY: Truax 1984]` `[UNSOURCED-PRIMARY: Sterne 2012]` `[UNSOURCED-PRIMARY: Augoyard 2006]` `[UNSOURCED-PRIMARY: Born 2013]` — pending ingest of monographs into [`raw/02_secondary_sources/`](../../raw/02_secondary_sources/). Schafer 1977 = primary anchor (T1 priority).
- [literature-review-legacy](../08_sources/literature-review-legacy.md) — §13 establishes Schafer's keynote / soundmark / signal as the canonical RQ5 frame; §1.2 names DARIAH-EU 2023, British Library, BBC SFX, and Europeana Sounds as the soundmark archives the deployment horizon depends on.

> Legacy synthesis context: [`literature_review.md` §13](../../../literature_review.md), [`PROJECT_GUIDE.md` §Why Computational Humanities](../../../PROJECT_GUIDE.md).
