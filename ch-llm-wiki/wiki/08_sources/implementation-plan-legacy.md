---
title: implementation_plan.md — Legacy Synthesis (operational playbook, 11 sections)
type: source-card
tags: [legacy-synthesis, project-internal, implementation-plan, determinism, hardware-gate, makefile, risk-register]
status: stable
last_reviewed: 2026-04-20
sources: []
---

## implementation_plan.md — Legacy Synthesis (operational playbook)

- **Raw file:** [`raw/03_legacy_synthesis/implementation_plan.md`](../../raw/03_legacy_synthesis/implementation_plan.md) ← primary basis
- **Venue / Level:** Project-internal synthesis document, CH-Proj-M, Uni Bamberg · **L4** · **Year:** SS 2026 (Apr 2026 rebuild) · **Author:** Zuraiz
- **Confidence / Applicability:** MED (synthesis, not primary) / HIGH (canonical operational playbook — owns determinism pins, hardware gates, hypotheses YAML, risk register, Makefile)

**Claim:** Owns every *how* decision in the project. Determinism pins (§1.1: PYTHONHASHSEED=42, CUBLAS_WORKSPACE_CONFIG=:4096:8, torch.use_deterministic_algorithms=True), hardware gate (§1.2: SM ≥ 8.0, ≥ 24 GB VRAM bf16), `setup_check.py` spec (§1.3), `hypotheses_preregistered.yml` schema (§1.4 — Family-1 SPIDEr / Family-2 CHAIR / descriptive_only RQ4-5), Phase 0–4 protocols including code stubs for contamination_audit / canary_baseline / af3_hello_world / run_inference / rq1_comparison / rq2_polyphony_differential / rq3_hallucination (CHAIR-audio dual criterion implementation) / rq4_temporal / rq5_cultural_heritage / negative_controls (§§2–6), Makefile (§7 — `make all` pipeline), risk register R1–R10 with likelihood/impact/mitigation/layer (§8), verification gates G0–G7 (§9), cut ladder (§10 — same as PROJECT_GUIDE.md but operational), full directory layout (§11).

**Method:** Code-stub-driven planning. Each protocol section embeds a fully-typed Python skeleton showing inputs, outputs, kill criteria, and where artefacts land (e.g., `results/contamination_audit.json`). Risk and gate tables make every planned failure mode explicit before Phase 1 begins.

**Key numbers (verbatim per legacy synthesis):**

- **Determinism pins:** `PYTHONHASHSEED=42` · `CUBLAS_WORKSPACE_CONFIG=:4096:8` · `torch.manual_seed(42)` · `torch.use_deterministic_algorithms(True)` · `cudnn.benchmark=False`.
- **Hardware:** SM ≥ 8.0 (Ampere+) · bf16 ≥ 24 GB VRAM · int4 fallback ≥ 12 GB · Java 11+ for `aac-metrics` SPICE · Python 3.11.
- **AF3:** 8B params · ~20 GB bf16 / ~10 GB int4. **SALMONN:** 13B · ~24 GB / ~14 GB. **Qwen2.5-Omni:** ~7B · Apache-2.0.
- **Bootstrap:** BCa method · n=1000 resamples · seed=42 · confidence_level=0.95.
- **Holm-Bonferroni:** Family-1 (RQ1, RQ2, RQ3-SPIDEr) k=3 strictest α'=0.0167 · Family-2 (RQ3-CHAIR) k=1 α'=0.05.
- **DCASE canary tolerance:** 29.6% ± 1% SPIDEr-FL (kill if > 2 pp deviation).
- **Polyphony annotation:** Cohen's κ ≥ 0.6 gate; AudioSet tag-count proxy as fallback.
- **CHAIR-audio sensitivity:** primary 0.25 CLAPScore threshold; sweep at {0.20, 0.30}.
- **Negative-control battery:** 30 clips (10 silence + 10 white-noise + 10 pure tones) · expected hallucination rate ≥ 80%.
- **RQ4 stimulus:** 50 synthetic A-then-B mixtures · MDE 4.76 pp.
- **RQ5 stimulus:** ≤ 20 culturally-grounded clips (Bamberg bells if T1 consent + BBC SFX) · `[DESCRIPTIVE_ONLY]`.
- **Risk register:** 10 risks (R1–R10) tagged L1/L2 with mitigations.
- **Verification gates:** 8 gates (G0–G7) from setup → paper compilation.

**Threat to validity:** L4 internal plan. Code stubs are *intended* implementations — none have yet been executed against real Clotho-eval data as of the wiki bootstrap (2026-04-20). The 29.6% canary number is taken from Labbeti 2024 (L1) but reproducibility on this project's hardware is not yet verified — that is exactly the Phase 1 canary check. Risk likelihoods (LOW/MED/HIGH) in the §8 register are subjective author estimates, not measured. Per CLAUDE.md §5, this card may be cited as primary basis for **operational decisions** (determinism pins, hardware gate, BCa parameters, Makefile structure) which it owns, but must NOT be cited as primary basis for empirical numbers (e.g., the 29.6% baseline → cite Labbeti 2024).

**Feeds:**

- **Metrics** ([fense](../05_metrics/fense.md), [spider-fl](../05_metrics/spider-fl.md)) — `aac-metrics` library + canary protocol from §3.2.
- **Models** ([audio-flamingo-3](../03_models/audio-flamingo-3.md), [salmonn](../03_models/salmonn.md), [qwen2-5-omni](../03_models/qwen2-5-omni.md)) — VRAM budgets, inference protocols, decoding pins from §1.2 + §4.1.
- All RQ-related code stubs — referenced by `wiki/02_research_questions/` if per-RQ pages are added.
- Wiki pages currently citing this card: see "Cited by" below.

**One-sentence reservation:** This card owns *operational* decisions; cite it for "how the project runs" (BCa seed=42, bf16 gate, `make all`), but never as primary basis for "how the world is" (the 29.6% baseline number, the AF3 architecture) — those belong to peer-reviewed/preprint primaries.

### Notes

implementation_plan.md is the project's *operational truth*. When a wiki model-card or metric-card needs to know what hardware/precision/library/seed is in use, this card is where the chain leads. The Makefile in §7 is the single source of truth for the `make all` pipeline that must exit 0 on a fresh clone (verification gate G6).

### Cross-links

- **Cited by:** [fense](../05_metrics/fense.md), [spider-fl](../05_metrics/spider-fl.md), [audio-flamingo-3](../03_models/audio-flamingo-3.md), [salmonn](../03_models/salmonn.md), [qwen2-5-omni](../03_models/qwen2-5-omni.md).
- **Sibling legacy-synthesis cards:** [paper-summaries-legacy](paper-summaries-legacy.md), [project-guide-legacy](project-guide-legacy.md), [literature-review-legacy](literature-review-legacy.md), [research-notes-legacy](research-notes-legacy.md).
- **Live working copy:** [`implementation_plan.md`](../../../implementation_plan.md).
