---
title: FENSE — Fluency- and Error-aware Sentence Embedding Score
type: metric-card
tags: [metric, fense, embedding, l1]
status: draft
last_reviewed: 2026-04-20
sources: [../08_sources/zhou-2022-fense.md, ../08_sources/paper-summaries-legacy.md, ../08_sources/implementation-plan-legacy.md]
---

## FENSE

| Field | Value |
|:------|:------|
| Formula / definition | SentenceBERT (all-mpnet-base-v2) cosine similarity × fluency-error penalty |
| Range | [0, 1] (fluency-penalised cosine) |
| Reference-based? | yes — requires reference captions |
| Implementation | Official FENSE repo (Zhou et al. 2022); SentenceBERT `all-mpnet-base-v2` backbone |
| Best for | Semantic similarity that penalises ungrammatical / incoherent hallucinations |
| Known limitations | Inherits SentenceBERT backbone domain biases; less interpretable than n-gram metrics; validated only on AudioCaps-Eval and Clotho-Eval human-judgement corpora |

### Role in this project

**Secondary metric for RQ1 / RQ2 / RQ3.** FENSE has the highest reported correlation with human quality judgement for audio captions (per Zhou 2022 vs. BLEU/METEOR/ROUGE-L/CIDEr/SPICE/SPIDEr), used as a complementary semantic signal to [SPIDEr-FL](spider-fl.md).

### Sources

- [zhou-2022-fense](../08_sources/zhou-2022-fense.md) — primary source card (arXiv 2110.04684 / ICASSP 2022 abstract retrieved 2026-04-20). `[Zhou 2022; L2; HIGH/HIGH]`.
- [paper-summaries-legacy](../08_sources/paper-summaries-legacy.md) — legacy synthesis context (Paper S1).
- [implementation-plan-legacy](../08_sources/implementation-plan-legacy.md) — operational use as the project's secondary metric alongside SPIDEr-FL, CIDEr, SPICE, and CLAPScore.

> Legacy synthesis context: [`paper_summaries.md`](../../../paper_summaries.md) (FENSE card), [`literature_review.md` §6](../../../literature_review.md).
