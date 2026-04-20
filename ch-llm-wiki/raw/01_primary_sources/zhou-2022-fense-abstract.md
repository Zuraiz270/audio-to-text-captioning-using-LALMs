---
type: abstract-snapshot
source: arXiv 2110.04684
retrieved: 2026-04-20
status: abstract-only
---

# FENSE — Abstract Snapshot

**Title:** Can Audio Captions Be Evaluated With Image Caption Metrics?
**Authors:** Zelin Zhou, Zhiling Zhang, Xuenan Xu, Zeyu Xie, Mengyue Wu, Kenny Q. Zhu
**arXiv ID:** 2110.04684 (Oct 2021)
**Venue:** ICASSP 2022
**Source URL:** https://arxiv.org/abs/2110.04684

## Abstract (verbatim, condensed)

Automated evaluation of audio captioning is challenging. Existing metrics, e.g., BLEU, METEOR, ROUGE-L, CIDEr, SPICE, SPIDEr, were originally proposed for image captioning and have been directly migrated. However, these metrics may have limited correlation with human judgments on audio captions because of the modality gap. We thus propose a new evaluation metric, called FENSE (Fluency ENhanced Sentence-bert Evaluation), that combines the strengths of Sentence-BERT for capturing semantic similarities and a fluency error penalty for catching common grammatical errors. Experiments on two human-judgment audio caption corpora (AudioCaps-Eval and Clotho-Eval) show that FENSE achieves significantly stronger correlation with human evaluation than current metrics.

## Key facts

- Combines Sentence-BERT cosine + fluency penalty
- Released two benchmark corpora: AudioCaps-Eval, Clotho-Eval
- Outperforms BLEU/METEOR/ROUGE-L/CIDEr/SPICE/SPIDEr on human-correlation

## Project notes

- Used as a complementary metric to SPIDEr-FL across RQ1–RQ3.
- Implementation: official FENSE repo (Sentence-BERT all-mpnet-base-v2).
- Citation chain: previously bridged via paper-summaries-legacy; now sourced.
