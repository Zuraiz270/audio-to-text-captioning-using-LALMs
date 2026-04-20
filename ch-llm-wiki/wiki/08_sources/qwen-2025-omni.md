---
type: source-card
status: draft
last_reviewed: 2026-04-20
---

# Qwen Team 2025 — Qwen2.5-Omni

**Raw file:** [qwen-2025-omni-abstract.md](../../raw/01_primary_sources/qwen-2025-omni-abstract.md)
**External:** arXiv 2503.20215 (https://arxiv.org/abs/2503.20215)
**Venue / Level:** Technical report — L3 preprint
**License:** CC BY 4.0
**Confidence / Applicability:** HIGH / MED — author-self-reported

## Claim

End-to-end multimodal model perceiving text, image, audio, video and emitting text + speech in streaming mode; first open-source model whose end-to-end speech-instruction-following matches its text-input capability.

## Method

- Block-wise streaming encoders (audio + visual)
- TMRoPE = Time-aligned Multimodal RoPE — synchronises audio/video timestamps via interleaved sequence
- Thinker-Talker dual-track: Thinker (LLM, text) + Talker (autoregressive on Thinker hiddens, audio tokens)

## Key numbers

- SOTA on Omni-Bench (multimodal fine-grained understanding) — author-self-reported

## Threat to validity

- Single-team report, no third-party replication referenced as of 2026-04-20.
- TMRoPE temporal-alignment claim is structural, not benchmarked against TAC-style temporal-grounding probes.

## Feeds

- Comparator model alongside AF3 and SALMONN
- RQ4 (temporal grounding) — TMRoPE design is structurally relevant
- [qwen2-5-omni.md](../03_models/qwen2-5-omni.md) — populates a previously 33%-dense card

## One-sentence reservation

Streaming + TMRoPE design is promising for temporal grounding, but Qwen2.5-Omni has not been benchmarked against TAC-style probes in any source we cite.

## Cross-links

- [qwen2-5-omni.md](../03_models/qwen2-5-omni.md)
- [paper-summaries-legacy.md](paper-summaries-legacy.md) — earlier bridge, now superseded
