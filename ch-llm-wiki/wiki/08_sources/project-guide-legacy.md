---
title: PROJECT_GUIDE.md — Legacy Synthesis (project entry point)
type: source-card
tags: [legacy-synthesis, project-internal, project-guide, scope, phase-map, glossary]
status: stable
last_reviewed: 2026-04-20
sources: []
---

## PROJECT_GUIDE.md — Legacy Synthesis (project entry point)

- **Raw file:** [`raw/03_legacy_synthesis/PROJECT_GUIDE.md`](../../raw/03_legacy_synthesis/PROJECT_GUIDE.md) ← primary basis
- **Venue / Level:** Project-internal synthesis document, CH-Proj-M, Uni Bamberg · **L4** (project codebase / synthesis artefact, not peer-reviewed) · **Year:** SS 2026 (Apr 2026 rebuild) · **Author:** Zuraiz under supervision of Prof. Abeßer
- **Confidence / Applicability:** MED (synthesis, not primary) / HIGH (canonical project entry point — owns scope, phase map, glossary)

**Claim:** The project entry-point document. Owns the L1 (course-safe) / L2 (research-grade) cut ladder, the RQ0–RQ5 table with primary metrics and falsification criteria, the Phase 0–4 timeline with hard gates and red lines, the deliverable list (term paper Jul 6, talk Jul 13), the document boundary rules, and the canonical 20-term glossary.

**Method:** Author synthesis pulling together the project's normative structure from its peer-reviewed literature (developed in `literature_review.md`) and operational decisions (developed in `implementation_plan.md`). Every section is a one-page-or-less summary that cross-references the deeper file. The two-layer structure (L1/L2) and four-cut ladder (Cut 1 Qwen2.5-Omni → Cut 4 RQ5 cultural) is the document's load-bearing scope mechanism.

**Key numbers (verbatim per legacy synthesis):**

- **6 research questions** — RQ0 contamination · RQ1 vs DCASE · RQ2 polyphony · RQ3 hallucination · RQ4 temporal · RQ5 cultural.
- **4-cut ladder:** Cut 1 = Qwen2.5-Omni (drops first), Cut 4 = RQ5 (drops last — humanities identity).
- **DCASE 2024 baseline:** 29.6% SPIDEr-FL on Clotho-eval (RQ1 floor).
- **Phases:** Phase 0 → Apr 19 · Phase 1 Apr 19 → May 4 · Phase 2 May 4 → May 18 · Phase 3 May 18 → Jul 1 · Phase 4 Jul 1 → Jul 13.
- **Deliverables:** term paper ~15 pages Jul 6; 15-min talk + Q&A Jul 13.
- **Clotho v2.1 Zenodo:** record **4783391** (NOT 3490684 = v1).
- **Glossary:** 20 canonical terms (AAC, AudioSet, BCa bootstrap, bf16, CHAIR-audio, CLAPScore, Clotho v2.1, Cohen's κ, Contamination audit, DCASE, Ekphrasis, FENSE, Hallucination, Holm-Bonferroni, LALM, MDE, Polyphony, Q-Former, Soundmark, SPIDEr-FL, Zero-shot).
- **Hard gates:** `setup_check.py` exits 0 (Phase 0) · canary 29.6% ± 1% (Phase 1) · κ ≥ 0.6 polyphony annotation (Phase 2).
- **Red lines:** DCASE canary > 2 pp deviation → metric pipeline broken · SM < 8.0 → bf16 invalid · `hypotheses_preregistered.yml` modified after Phase 2 → HARKing.

**Threat to validity:** L4 project-internal synthesis. Owns scope and timeline decisions but contains no primary empirical evidence — every cited number (29.6% baseline, 1.04 pp MDE, 24 GB VRAM bf16) traces back to other documents (`literature_review.md` for evidence, `implementation_plan.md` for protocols). Specific architectural claims (e.g., Q-Former bottleneck as unified root cause) need re-verification against primaries when AF3, SALMONN, TAC papers are ingested. Per [`CLAUDE.md` §5](../../CLAUDE.md), this card may be cited as primary basis for **scope, phase, deliverables, and glossary** claims (which it owns), but must NOT be cited as primary basis for empirical numbers — those belong to peer-reviewed primaries.

**Feeds:**

- **Scope** ([scope](../01_project/scope.md)) — L1/L2 split, cut ladder, in-scope / out-of-scope.
- **Phase map** ([phase-map](../01_project/phase-map.md)) — Phase 0–4 timeline, hard gates, red lines.
- **RQs** ([rq-index](../02_research_questions/rq-index.md)) — RQ0–RQ5 table, solved-if / falsified-if criteria.
- **Glossary** ([11_glossary/README](../11_glossary/README.md)) — canonical 20-term short glossary.
- Wiki pages currently citing this card: see "Cited by" below.

**One-sentence reservation:** This card owns *project-structural* decisions (scope, phase, RQ list, glossary), but owns no *empirical claim* — every quantitative number (29.6%, 1.04 pp MDE, 8B parameters) belongs to its primary source and must be cited from there once ingested.

### Notes

PROJECT_GUIDE.md is the entry point in the 5-file documentation ecosystem. It is the only file a new reader (examiner, supervisor, future Claude session) is expected to read first to understand what the project is. The wiki preserves this role: [scope](../01_project/scope.md) and [phase-map](../01_project/phase-map.md) are atomized summaries of PROJECT_GUIDE.md's scope and phase sections, and [11_glossary/README](../11_glossary/README.md) points back to PROJECT_GUIDE.md as the canonical glossary.

When PROJECT_GUIDE.md is updated (e.g., a new cut is added to the L2 ladder, or a deadline shifts), the wiki pages citing this card must have their `last_reviewed` bumped and their content checked against the new version. The drift rule ([`CLAUDE.md` §13](../../CLAUDE.md)) applies: PROJECT_GUIDE.md wins on conflict.

### Cross-links

- **Cited by:** [scope](../01_project/scope.md), [phase-map](../01_project/phase-map.md), [rq-index](../02_research_questions/rq-index.md), [11_glossary/README](../11_glossary/README.md).
- **Sibling legacy-synthesis cards:** [paper-summaries-legacy](paper-summaries-legacy.md), [literature-review-legacy](literature-review-legacy.md), [implementation-plan-legacy](implementation-plan-legacy.md), [research-notes-legacy](research-notes-legacy.md).
- **Live working copy at repo root:** [`PROJECT_GUIDE.md`](../../../PROJECT_GUIDE.md) (the immutable copy is in [`raw/03_legacy_synthesis/`](../../raw/03_legacy_synthesis/PROJECT_GUIDE.md)).
