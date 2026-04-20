---
title: RQ0 — Training-data contamination audit
type: concept
tags: [rq, rq0, contamination, validity, methodology]
status: draft
last_reviewed: 2026-04-20
sources: [../08_sources/goel-2025-af3.md, ../08_sources/drossos-2020-clotho.md, ../08_sources/implementation-plan-legacy.md]
---

## RQ0 — Training-data contamination audit

**Question:** Are the Clotho v2.1 evaluation clips on which we benchmark AF3 already present (verbatim or near-verbatim) in any disclosed AF3 training corpus, or in the training corpora of the comparator LALMs (SALMONN, Qwen2.5-Omni)?

**Why it sits before RQ1:** every other RQ's headline number ("AF3 reaches X SPIDEr-FL on Clotho v2.1, well above the supervised DCASE baseline") is conditional on the eval set not having been seen during training. A contamination overlap converts an apparent zero-shot result into a partial-train-leak result. RQ0 is therefore a *validity gate*, not a research finding.

### Hypothesis (operational form)

- **H0_RQ0:** non-trivial (≥ 5%) of Clotho v2.1 eval-split FreeSound IDs appear in at least one disclosed training manifest among {AF3 disclosed corpus, WavCaps, AudioSetCaps, Clotho-AQA}.
- **Decision rule:** if H0_RQ0 is *not* rejected (i.e., overlap is ≥ 5% on any model), the headline RQ1/RQ2/RQ3 numbers for that model are reported with an explicit "partial overlap with training" qualifier and the supervised DCASE comparison is recomputed on the eval-split residual (clips with no overlap).

### Method

1. **Manifest collection.** Fetch each model's training manifest from the official source (HuggingFace data card / paper appendix / official repo).
2. **Eval-set fingerprint.** Hash the Clotho v2.1 eval-split FreeSound IDs (1,045 clips).
3. **Set intersection.** Compute the symmetric intersection per (eval, manifest) pair.
4. **Report.** Per-model overlap percentage + per-clip overlap manifest. Highest-risk overlap candidate identified in early survey: **Clotho-AQA** (re-uses Clotho clips for QA-style annotation; if AF3 was trained on Clotho-AQA, the eval split is contaminated by construction).
5. **Threats / failure cases.** (a) Manifest is *incomplete* (the most likely failure — Q1 in [`research_notes.md`](../../../research_notes.md) is exactly this); (b) data leak via web-scraped corpora not enumerated; (c) audio identity vs. ID identity (re-encoded versions of the same clip would not match by ID).

### Failure-case fallback (when manifest disclosure is incomplete)

- Mark RQ0 **partially answerable** rather than blocked.
- Report intersection with disclosed subset; record the undisclosed portion as a formal threat-to-validity in [`literature_review.md` §9](../../../literature_review.md).
- Cross-reference the cross-corpus baseline {WavCaps, AudioSetCaps, Clotho-AQA} as a lower-bound contamination estimate.

### Why this matters for the central thesis

The project's central thesis is hypothesis-form: "we test whether AF3 *under a zero-shot protocol* matches/exceeds the supervised baseline." If RQ0 finds material contamination, the *zero-shot protocol* premise fails, and the thesis must be restated with the qualifier — not silently retracted. The honest reporting of RQ0's outcome is what distinguishes this from the AF3 paper's self-reported "fully open" framing.

### Sources

- [goel-2025-af3](../08_sources/goel-2025-af3.md) — AF3 abstract claim of open training data; HF data-card refetch is the gating dependency.
- [drossos-2020-clotho](../08_sources/drossos-2020-clotho.md) — Clotho v2.1 eval-split provenance.
- [implementation-plan-legacy](../08_sources/implementation-plan-legacy.md) — operational protocol context (manifest loaders specified as CONTRACT blocks per [`implementation_plan.md` §4](../../../implementation_plan.md)).

### Cross-links

- [rq-index.md](rq-index.md)
- [audio-flamingo-3.md](../03_models/audio-flamingo-3.md)
- [clotho-v2-1.md](../04_datasets/clotho-v2-1.md)
- [af3-zero-shot-claim.md](../09_comparisons/af3-zero-shot-claim.md)
