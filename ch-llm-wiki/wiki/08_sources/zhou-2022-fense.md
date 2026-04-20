---
type: source-card
status: draft
last_reviewed: 2026-04-20
---

# Zhou et al. 2022 — FENSE

**Raw file:** [zhou-2022-fense-abstract.md](../../raw/01_primary_sources/zhou-2022-fense-abstract.md)
**External:** arXiv 2110.04684 (https://arxiv.org/abs/2110.04684)
**Venue / Level:** ICASSP 2022 — L2
**Confidence / Applicability:** HIGH / HIGH

## Claim

Image-caption metrics (BLEU, METEOR, ROUGE-L, CIDEr, SPICE, SPIDEr) correlate weakly with human judgement on audio captions due to the modality gap. FENSE (Sentence-BERT cosine + fluency-error penalty) achieves significantly stronger correlation on AudioCaps-Eval and Clotho-Eval.

## Method

- Sentence-BERT cosine similarity (semantics)
- Rule-based fluency-error penalty (grammar)
- Validated against two newly released human-judgement corpora (AudioCaps-Eval, Clotho-Eval)

## Key numbers

- Human-correlation results presented for both eval corpora vs. all classical image-caption metrics (specific Spearman/Pearson values omitted to avoid restating from memory).

## Threat to validity

- Sentence-BERT model choice (all-mpnet-base-v2) inherits any biases of the underlying transformer.
- Human-judgement corpora are sized in low thousands — limited statistical power.

## Feeds

- RQ1, RQ2, RQ3 — FENSE is the project's complementary semantic metric to SPIDEr-FL
- implementation_plan.md §6 (metric stack)

## One-sentence reservation

Validated only on AudioCaps-Eval and Clotho-Eval — extrapolation to other-domain audio captions is by analogy.

## Cross-links

- [fense.md](../05_metrics/fense.md)
- [paper-summaries-legacy.md](paper-summaries-legacy.md) — earlier bridge, now superseded
