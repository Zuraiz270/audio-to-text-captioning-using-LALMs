---
title: "CLAPScore 0.25 hallucination threshold — free parameter with sensitivity analysis"
type: comparison
tags: [comparison, clapscore, threshold, hallucination, free-parameter]
status: draft
last_reviewed: 2026-04-20
sources: [../08_sources/implementation-plan-legacy.md, ../08_sources/paper-summaries-legacy.md]
---

## CLAPScore ≤ 0.25 as the hallucination threshold

The project uses a CLAPScore cutoff to flag candidate hallucinations in the CHAIR-audio dual criterion (RQ3 / H4: AF3 vs SALMONN gap). The cutoff value is a free parameter — recorded here per CLAUDE.md §10 because the project chose a value without a directly empirical grounding for *that specific value*.

| Position | Source | Confidence | Applicability |
|:---------|:-------|:-----------|:--------------|
| **A — chosen value 0.25:** matches the order of magnitude of the Rohrbach 2018 CHAIR default mapped onto the LAION-CLAP empirical score distribution; treated as a project convention. | [paper-summaries-legacy](../08_sources/paper-summaries-legacy.md) — Rohrbach 2018 CHAIR card; CLAPScore card. | MED (analogy from image-captioning CHAIR) | LOW (LAION-CLAP empirical score distribution on audio captions has not been independently calibrated for this project) |
| **B — sensitivity analysis at {0.20, 0.25, 0.30}:** per [`implementation_plan.md` §6 (Free Parameter)](../../../implementation_plan.md), all three thresholds are pre-registered and reported equally. The H4 (AF3 vs SALMONN) decision is INDETERMINATE if 2/3 thresholds disagree on the rejection of H4. | [implementation-plan-legacy](../08_sources/implementation-plan-legacy.md) — operational protocol. | HIGH (project pre-registration, EBSE-compliant) | HIGH (this project) |

**Resolution per CLAUDE.md §10:**

- A is an analogy across modalities and is honestly low-applicability.
- B converts a free-parameter problem into a **honest parameterization**: the project does not depend on 0.25 being correct; it depends on H4's verdict being *robust across* the threshold range. If H4 flips between 0.20 and 0.30, the project reports "INDETERMINATE — threshold-sensitive" rather than picking one and writing up a story.
- Citation badge to use anywhere CLAPScore-0.25 appears: `[FREE-PARAMETER; sensitivity {0.20, 0.25, 0.30}; INDETERMINATE rule on disagreement]`.

**Status:** Open until H4 is run and the sensitivity sweep is reported. If H4 is INDETERMINATE under the sweep, this is itself a finding worth recording (free-parameter sensitivity = a real result, not a methodological failure).

### Cross-links

- [entity-hallucination.md](../06_failure_modes/entity-hallucination.md)
- [`implementation_plan.md` §6](../../../implementation_plan.md)
- [`research_notes.md` Q5](../../../research_notes.md)
