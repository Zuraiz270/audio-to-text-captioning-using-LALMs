---
title: Accessibility — Audio Captions for Blind / Low-Vision Users
type: humanities-frame
tags: [humanities, accessibility, blv, wcag]
status: stub
last_reviewed: 2026-04-20
sources: [../08_sources/paper-summaries-legacy.md, ../08_sources/literature-review-legacy.md]
---

## Accessibility

**Tradition.** Disability studies / web accessibility / inclusive design.
**Originating context.** WCAG 2.1 AA "non-text content" requirements; sound-archives accessibility advocacy.

**Definition.** For blind and low-vision (BLV) users, audio collections are first-class cultural artefacts that are nonetheless gated by **the absence of textual description**. Image collections have ALT text; audio collections largely do not. AAC at deployable quality would close this gap.

**Why it matters here.** This frame supplies one of the project's two non-engineering motivations (the other being [ekphrasis](ekphrasis.md)). It also disciplines the failure-mode analysis: a BLV user **cannot independently verify** a hallucinated entity ([entity-hallucination](../06_failure_modes/entity-hallucination.md)) or a mis-ordered event ([temporal-grounding-loss](../06_failure_modes/temporal-grounding-loss.md)) — so the failure modes are not abstract metric quirks, they are **harm vectors**.

This argument:

- Promotes [entity-hallucination](../06_failure_modes/entity-hallucination.md) from "metric curiosity" to "safety concern."
- Connects [polyphony-under-description](../06_failure_modes/polyphony-under-description.md) to lost information that a sighted user could partially recover from context but a BLV user cannot.
- Justifies the project's choice to characterise failure modes structurally, not just to chase headline scores.

### See also

- [digital-archives](digital-archives.md) — collections that benefit when AAC is deployable.

### Sources

- [paper-summaries-legacy](../08_sources/paper-summaries-legacy.md) — covers humanities tier (S4–S12) but contains **no dedicated card** for WCAG 2.1 AA or BLV sound-archive accessibility. `[UNSOURCED-PRIMARY: WCAG 2.1 AA]` `[UNSOURCED-PRIMARY: BLV sound-archive accessibility literature]` — pending direct ingest into [`raw/02_secondary_sources/`](../../raw/02_secondary_sources/) (W3C WCAG 2.1 spec is L1 standards-track and should be primary). This page therefore remains thinly-cited even via legacy — flagged for explicit raw-file deposit.
- [literature-review-legacy](../08_sources/literature-review-legacy.md) — §1.2 mentions BLV access in passing as one of the project's two non-engineering motivations, but **does not contain a dedicated WCAG / BLV evidence card** either. Citation status remains thin: explicit raw-file deposit (W3C WCAG 2.1 spec + BLV sound-archive literature) is still required for L1-grade primary citations.

> Legacy synthesis context: [`PROJECT_GUIDE.md` §Why This Matters → Accessibility](../../../PROJECT_GUIDE.md), [`literature_review.md`](../../../literature_review.md).
