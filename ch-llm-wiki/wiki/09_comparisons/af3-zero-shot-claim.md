---
title: "AF3 zero-shot framing — author claim vs. project-tested premise"
type: comparison
tags: [comparison, af3, zero-shot, validity]
status: draft
last_reviewed: 2026-04-20
sources: [../08_sources/goel-2025-af3.md, ../08_sources/project-guide-legacy.md]
---

## AF3 "zero-shot" — claim vs. project-tested premise

The AF3 paper and the project's framing differ on the epistemic status of "zero-shot."

| Position | Source | Confidence | Applicability |
|:---------|:-------|:-----------|:--------------|
| **A — author claim:** AF3 demonstrates zero-shot captioning on benchmarks not seen in training. | [goel-2025-af3](../08_sources/goel-2025-af3.md) — abstract; "trained on only open-source audio data" + claimed SOTA on 20+ benchmarks framed as out-of-domain. | HIGH (single-team author claim) | MED (depends on full training-corpus disclosure) |
| **B — project framing:** "Zero-shot" is a property RQ0 *tests*, not a premise we accept. The headline result is reported as zero-shot only if RQ0's contamination audit finds < 5% eval-set overlap with the disclosed training manifest. | [project-guide-legacy](../08_sources/project-guide-legacy.md) — `PROJECT_GUIDE.md` §Central Thesis (rewritten 2026-04-20 to hypothesis form); RQ0 dedicated page [rq0-contamination.md](../02_research_questions/rq0-contamination.md). | HIGH (project-internal pre-registration) | HIGH (this project) |

**Resolution per CLAUDE.md §10:**

- Hierarchy: A is from a preprint (L3); B is project-internal methodology (not a competing source — it's the *protocol* under which A's claim is evaluated). Not a true source-vs-source conflict, but a **claim-vs-protocol** asymmetry.
- Resolution: keep both. Position A is reported as the author claim (with the † preprint qualifier). Position B is the operational rule under which A is verified or qualified. Any wiki or root-doc text that asserts "AF3 is zero-shot" without flagging RQ0 dependence should be edited.

**Status:** Open until RQ0 runs. After RQ0 either H0_RQ0 is rejected (project re-asserts zero-shot with qualifier "verified on eval-set residual after manifest cross-reference") or it is not rejected (project reports "partial-train-leak result"). Either way, the page remains as a record of why the project took this stance.

### Cross-links

- [rq0-contamination.md](../02_research_questions/rq0-contamination.md)
- [audio-flamingo-3.md](../03_models/audio-flamingo-3.md)
- [`PROJECT_GUIDE.md`](../../../PROJECT_GUIDE.md) §Central Thesis
