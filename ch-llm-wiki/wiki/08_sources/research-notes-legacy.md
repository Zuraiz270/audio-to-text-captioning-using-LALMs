---
title: research_notes.md — Legacy Synthesis (strategy + evidence-expansion playbook)
type: source-card
tags: [legacy-synthesis, project-internal, research-notes, strategy, open-questions, reading-order, evidence-expansion]
status: stable
last_reviewed: 2026-04-20
sources: []
---

## research_notes.md — Legacy Synthesis (strategy + evidence-expansion playbook)

- **Raw file:** [`raw/03_legacy_synthesis/research_notes.md`](../../raw/03_legacy_synthesis/research_notes.md) ← primary basis
- **Venue / Level:** Project-internal synthesis document, CH-Proj-M, Uni Bamberg · **L4** · **Year:** SS 2026 (Apr 2026 rebuild) · **Author:** Zuraiz
- **Confidence / Applicability:** MED (strategy, not primary) / HIGH (canonical strategic anchor — owns thesis-axis positioning, open questions, RQ design matrix, May-4 talk branching)

**Claim:** Strategic anchor + evidence-expansion operations. Owns the thesis-positioning argument on the architecture axis (§1: SALMONN dual-encoder → AF3 unified-encoder → TAC explicit temporal head; the project sits at the AF3 position testing whether TAC's critique applies to AF3 captioning), the seven open questions tracked across the project (§2: AF3 training-data disclosure / scoop risk / TAC weight release / Bamberg consent / CHAIR threshold sensitivity / Clotho-AQA attribution / Martin-Morato variance applicability), the Wohlin §6 RQ experiment-design matrix (§4: per-RQ metric / test / data / n / MDE / threats axis / falsifier), the evidence expansion strategy A–H (§5: source hierarchy 1–5, search locations, seed queries, refresh checkpoints, inclusion rules, evidence logging template, contradiction handling protocol, emergent-query log), the conceptual links between RQs (§6: polyphony↔hallucination↔temporal as one root cause; soundmark↔domain shift; ekphrasis↔inter-modal translation loss; contamination↔zero-shot framing), the reading order (§8: 18-paper queue across phases), the software stack (§9), and the May-4 talk branching by RQ0 outcome (§10: Branch A clean = standard narrative · Branch B partial = lead with finding · Branch C 0% clean = pivot to negative result).

**Method:** Strategy-document format. Tables make decision-relevant variables explicit (open questions × status, RQ × design matrix, source hierarchy × trust level). The May-4 branching protocol (§10) is a pre-committed decision tree that removes talk-day judgement-call risk.

**Key numbers (verbatim per legacy synthesis):**

- **7 open questions** (§2) — Q1 AF3 data disclosure · Q2 scoop risk · Q3 TAC weights · Q4 Bamberg consent · Q5 CHAIR threshold sensitivity · Q6 Clotho-AQA attribution · Q7 Martin-Morato variance applicability.
- **RQ design matrix** (§4): RQ0 n=1,045 descriptive · RQ1 n≤1,045 MDE 1.04 pp · RQ2 n~500 MDE 1.50 pp · RQ3 n=500 MDE 1.25 pp · RQ4 n=50 (no MDE) · RQ5 n≤20 descriptive · Neg-ctrl n=30.
- **Source hierarchy** (§5A): 5 priority tiers (official → peer-reviewed → challenge baselines → preprints → secondary commentary).
- **Refresh checkpoints** (§5D): 4 (pre-lit-review-lock May 4 · pre-impl-lock May 4 · pre-experiment May 18 · pre-discussion-write Jul 1).
- **Reading order** (§8): 18 papers (10 numbered + 7 supplementary + 1 humanities anchor).
- **May-4 talk branches** (§10): A (clean=100%) standard · B (0 < clean < 100%) lead with finding · C (clean=0%) pivot to negative result.

**Threat to validity:** L4 strategy document. Open questions are *unresolved* — Q1–Q7 require future ingest or experiments to close. The "scoop risk" (Q2) cannot be assessed from inside this document; it requires periodic external search per §5D. The Martin-Morato variance applicability (Q7) directly affects RQ1 MDE — the conservative σ ≈ 12 pp estimate is used, but the sensitivity floor (σ ≈ 8 pp → MDE ≈ 0.73 pp) is documented as alternative. Reading order is author-curated, not validated. Per CLAUDE.md §5, this card may be cited as primary basis for **strategic decisions** (RQ design matrix structure, talk-branching protocol, evidence-expansion operations) which it owns, but must NOT be cited as primary basis for empirical claims.

**Feeds:**

- **RQ design matrix** ([rq-index](../02_research_questions/rq-index.md)) — per-RQ n / MDE / falsifier from §4.
- **Conceptual links** — supports the unified-RCA argument (links polyphony↔hallucination↔temporal) developed in [literature-review-legacy](literature-review-legacy.md) §5.
- **Reading order** — informs which primary papers should be ingested next (currently: T1 paper rosters per [paper-summaries-legacy](paper-summaries-legacy.md)).
- Wiki pages currently citing this card: see "Cited by" below.

**One-sentence reservation:** This card owns *strategy and process* decisions; it does not own empirical claims, and any citation that requires an empirical number should chain through to literature-review-legacy → primary paper.

### Notes

research_notes.md is the document that prevents the project from going rigid in the face of Phase 1 surprises. The May-4 branching protocol (§10) is its most operationally important contribution: it pre-commits to three different talk narratives depending on RQ0's outcome, eliminating the need for a high-stakes mid-talk judgment call. As the project executes, the open questions in §2 will be progressively closed; future EDIT log entries on this card will track closures.

### Cross-links

- **Cited by:** [rq-index](../02_research_questions/rq-index.md).
- **Sibling legacy-synthesis cards:** [paper-summaries-legacy](paper-summaries-legacy.md), [project-guide-legacy](project-guide-legacy.md), [literature-review-legacy](literature-review-legacy.md), [implementation-plan-legacy](implementation-plan-legacy.md).
- **Live working copy:** [`research_notes.md`](../../../research_notes.md).
