---
type: source-card
status: draft
last_reviewed: 2026-04-20
---

# Tang et al. 2023 — SALMONN

**Raw file:** [tang-2023-salmonn-abstract.md](../../raw/01_primary_sources/tang-2023-salmonn-abstract.md)
**External:** arXiv 2310.13289 (https://arxiv.org/abs/2310.13289)
**Venue / Level:** ICLR 2024 — L2
**Confidence / Applicability:** HIGH / HIGH

## Claim

A pre-trained text LLM (Vicuna-13B) can be augmented with paired speech (Whisper) and audio (BEATs) encoders via a window-level Q-Former adapter to achieve generic "hearing" — competitive performance across ASR, audio QA, audio captioning, plus emergent cross-modal abilities.

## Method

Dual-encoder architecture: Whisper (speech) + BEATs (audio events/music) → window-level Q-Former → Vicuna-13B. Activation tuning to recover emergent abilities suppressed by instruction tuning.

## Key numbers

- Backbone: Vicuna-13B
- Adapter: window-level Q-Former

(Quantitative benchmark numbers omitted from this snapshot pending venue-PDF re-fetch — to avoid restating from memory.)

## Threat to validity

- Q-Former is the candidate adapter-layer bottleneck for polyphony — but the *mechanism* claim (Q-Former cannot represent concurrent events) is hypothesised, not yet proven; the project softened phrasing in literature_review.md §3.2 accordingly.

## Feeds

- RQ2 (polyphony hypothesis: adapter compression)
- literature_review.md §3 (architectural pillar)
- Comparator model alongside AF3 and Qwen2.5-Omni

## One-sentence reservation

Q-Former bottleneck for polyphony is a project hypothesis, not a SALMONN-paper finding.

## Cross-links

- [salmonn.md](../03_models/salmonn.md)
- [paper-summaries-legacy.md](paper-summaries-legacy.md) — earlier bridge, now superseded
