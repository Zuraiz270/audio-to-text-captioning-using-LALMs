---
title: literature_review.md — Legacy Synthesis (EBSE evidence narrative, 15 sections)
type: source-card
tags: [legacy-synthesis, project-internal, literature-review, ebse, evidence-narrative, humanities-lineage, unified-rca]
status: stable
last_reviewed: 2026-04-20
sources: []
---

## literature_review.md — Legacy Synthesis (EBSE evidence narrative)

- **Raw file:** [`raw/03_legacy_synthesis/literature_review.md`](../../raw/03_legacy_synthesis/literature_review.md) ← primary basis
- **Venue / Level:** Project-internal synthesis document, CH-Proj-M, Uni Bamberg · **L4** · **Year:** SS 2026 (Apr 2026 rebuild) · **Author:** Zuraiz
- **Confidence / Applicability:** MED (synthesis, not primary) / HIGH (canonical evidence narrative — owns Schafer/ekphrasis framing, unified RCA, metric protocol)

**Claim:** EBSE-compliant evidence narrative for T6 across 15 sections. Owns: AAC task definition (§1), humanities framing (§1.2 — ekphrasis + Schafer + DARIAH/British Library/BBC archive case for accessibility), dataset hierarchy (§2 — Tier-1 Clotho v2.1, Tier-2 AudioCaps, Tier-3 contamination corpora), DCASE 2024 baseline floor (§3 — 29.6% SPIDEr-FL), LALM architectural shift (§4 — SALMONN dual-encoder → AF3 unified-encoder), the **unified root-cause analysis** (§5 — Q-Former bottleneck → polyphony + hallucination + temporal loss as one mechanism), metric protocol (§6 — SPIDEr-FL/FENSE/CLAPScore/CHAIR-audio), research gap matrix (§7 — six empty cells filled), intellectual lineage diagram (§8 — 1977→2026), Wohlin's 4-axis threats (§9), MDE per RQ (§10), evidence hierarchy (§11), pre-registration (§12), competing explanations (§13), broadened humanities lineage (§14 — Truax/Augoyard/Sterne/Born/Mitchell), integrity gate (§15).

**Method:** Per-claim EBSE evidence badges `[Author Year; Lx; CONF/APPLIC]` on every empirical statement; per-section evidence-trail tables; explicit STALE-VALID flagging for sources > 10 years old; explicit conflict-resolution disclosure (e.g., SALMONN L2 vs AF3 L3 → recency rule). Reading time: 30–45 min.

**Key numbers (verbatim per legacy synthesis):**

- **DCASE 2024 baseline:** 29.6% SPIDEr-FL on Clotho-eval (Labbeti 2024, L1).
- **AF3 SOTA benchmarks:** MMAU 72.28 · ClothoAQA 91.1% · CMM-Hallucination 86.7% · Clotho-Entailment 92.9% (Ghosh 2025b, L3 preprint).
- **Metric variance** (Martin-Morato 2024, L2/MED): σ ≈ 12 pp SPIDEr-FL · σ ≈ 4 pp FENSE · σ ≈ 0.03 CLAPScore · σ ≈ 8 pp CIDEr · σ ≈ 3 pp BLEU-4.
- **Per-RQ MDE table** (§10.2): RQ1 1.04 pp · RQ2 1.50 pp · RQ3 1.25 pp · RQ4 4.76 pp · RQ5 0.019 (descriptive).
- **Schafer's tripartite ontology:** keynote / soundmark / signal — conceptual vocabulary for RQ5.
- **DARIAH-EU Strategic Plan (2023, L1)** — automated AV captioning of cultural heritage = priority capability.
- **British Library Sound Archive** > 6.5M recordings; **BBC Sound Effects Archive** > 33,000 CC-licensed clips — both lack systematic free-text caption layer.
- **Holm-Bonferroni families:** Family-1 SPIDEr-FL k=3 strictest α' = 0.0167 · Family-2 CHAIR k=1 α' = 0.05.
- **CHAIR-audio dual criterion:** entity hallucinated iff (a) ∉ AudioSet tags AND (b) CLAPScore < 0.25.

**Threat to validity:** L4 internal synthesis, not peer-reviewed. Many cited preprints are L3 (AF3, AF2, Qwen2.5-Omni, TAC, AF-Next) — confidence is HIGH only because of institutional credibility (NVIDIA, Adobe/Northwestern) and public code, not because of independent replication. The unified-RCA claim (§5) is the project's central theoretical claim and is supported by mechanism reasoning + author synthesis but is **not yet empirically validated** in this project — RQ2/RQ3/RQ4 are the falsification tests. The humanities lineage (§14) cites monographs (Schafer 1977, Truax 1984, Augoyard 2006, Sterne 2012, Born 2013, Mitchell 1986) all flagged STALE-VALID; per CLAUDE.md §5, primary monograph ingest is still pending.

**Feeds:**

- **All 3 failure-mode pages** ([polyphony-under-description](../06_failure_modes/polyphony-under-description.md), [entity-hallucination](../06_failure_modes/entity-hallucination.md), [temporal-grounding-loss](../06_failure_modes/temporal-grounding-loss.md)) — unified RCA from §5.
- **All 4 humanities-frame pages** ([ekphrasis](../07_humanities/ekphrasis.md), [soundscape-schafer](../07_humanities/soundscape-schafer.md), [accessibility](../07_humanities/accessibility.md), [digital-archives](../07_humanities/digital-archives.md)) — humanities framing from §1.2 + §14.
- **RQ0 / RQ1 / RQ2 / RQ3 / RQ4 / RQ5** — research-gap matrix from §7; pre-registered nulls from §12.
- Wiki pages currently citing this card: see "Cited by" below.

**One-sentence reservation:** This card synthesizes 26+ peer-reviewed primaries — never cite it as primary basis for any specific empirical claim (e.g., "29.6% baseline" belongs to Labbeti 2024; "Q-Former bottleneck" belongs to Mei 2022 + Ghosh 2025b; "soundmark" belongs to Schafer 1977); migrate to those primaries as soon as they are ingested.

### Notes

literature_review.md is the project's *evidence narrative* — it tells the story that turns 26 papers into a coherent thesis. The wiki's per-concept pages (failure modes, humanities frames) are the atomized form of this narrative, and they cite this legacy card as bridge until peer-reviewed primaries are deposited. Notable for accessibility / digital-archives stubs: §1.2 of literature_review.md adds DARIAH-EU 2023, British Library, BBC, and Europeana as named sources — strengthening those previously thinly-cited stubs beyond what paper-summaries-legacy alone provided.

### Cross-links

- **Cited by:** [polyphony-under-description](../06_failure_modes/polyphony-under-description.md), [entity-hallucination](../06_failure_modes/entity-hallucination.md), [temporal-grounding-loss](../06_failure_modes/temporal-grounding-loss.md), [ekphrasis](../07_humanities/ekphrasis.md), [soundscape-schafer](../07_humanities/soundscape-schafer.md), [accessibility](../07_humanities/accessibility.md), [digital-archives](../07_humanities/digital-archives.md).
- **Sibling legacy-synthesis cards:** [paper-summaries-legacy](paper-summaries-legacy.md), [project-guide-legacy](project-guide-legacy.md), [implementation-plan-legacy](implementation-plan-legacy.md), [research-notes-legacy](research-notes-legacy.md).
- **Live working copy:** [`literature_review.md`](../../../literature_review.md).
