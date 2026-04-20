# Audio-to-Text Captioning using LALMs — Project Guide

*Master's Project · CH-Proj-M · SS 2026 · Zuraiz (2177213)*
*Prof. Dr.-Ing. Jakob Abeßer · Computational Humanities · Uni Bamberg*
*Last updated: April 2026*

---

## Executive Summary

This project investigates whether current-generation Large Audio-Language Models (LALMs) — specifically Audio Flamingo 3 (NVIDIA, Jul 2025) — can match or exceed the supervised DCASE 2024 baseline in automated audio captioning, and characterises the three structurally-related failure modes they exhibit: polyphonic under-description, entity hallucination, and temporal grounding loss. The project is framed as Computational Humanities, not engineering: the theoretical anchor is the rhetorical tradition of *ekphrasis* (verbal description of non-verbal experience) and R. Murray Schafer's soundscape studies.

Success means: (1) a pre-registered, contamination-audited head-to-head comparison of AF3 vs. the DCASE baseline on Clotho v2.1 with bootstrap confidence intervals, and (2) a structured characterisation of where and how LALMs fail — publishable as a DCASE 2026 workshop paper. Course deliverables are a ~15-page term paper (Jul 6) and a 15-minute talk (Jul 13).

---

## Problem Statement

**What is audio captioning?** Automated Audio Captioning (AAC) is inter-modal translation: a raw audio waveform in, a free-text natural-language description out. Unlike audio tagging (`{dog, traffic, wind}`), captioning produces grammatical sentences encoding event identities, spatial cues, acoustic texture, and temporal relations: *"A dog barks in the distance as cars pass on a wet road while wind rustles nearby leaves."*

**What are LALMs?** Large Audio-Language Models combine a pre-trained audio encoder, a lightweight adapter (Q-Former in SALMONN; unified AF-Whisper encoder in AF3), and a large language model (LLM) decoder. Neither component was trained for captioning; the adapter learns to bridge audio representations into the LLM's token space. This is reported by model authors as enabling *emergent zero-shot captioning* — a claim this project's RQ0 contamination audit treats as testable, not a premise (see §Glossary).

> **Glossary-ahead note for first-time readers.** Acronyms used below (LALM, AAC, SPIDEr-FL, BCa, CHAIR-audio, FENSE, CLAPScore, Q-Former, soundmark, ekphrasis) are defined in the §Glossary at the bottom of this document. New readers may want to skim that section before reading the Research Questions.

**What is the specific problem?** Three failure modes:
1. **Polyphony under-description** — LALMs describe the dominant sound and silently drop concurrent secondary events.
2. **Entity hallucination** — LALMs mention sounds not present in the audio, driven by the LLM's text prior rather than acoustic evidence.
3. **Temporal grounding loss** — LALMs describe events in canonical text-prior order rather than actual onset order.

**What is NOT the problem:**
- Training new models or fine-tuning LALMs.
- Speech recognition (ASR) or music transcription.
- Real-time or streaming audio captioning.
- Proposing new metrics (we evaluate existing ones).

---

## Why This Matters

### Accessibility
Audio captions enable blind and low-vision users to access sound collections — oral history archives, radio broadcasts, cultural heritage recordings — that currently have no textual description layer.

### Cultural Archiving
The British Library Sound Archive (>6.5M recordings), BBC Sound Effects Archive (>33,000 CC-licensed clips), and Europeana Sounds have no systematic free-text caption layer. AAC enables semantic search and retrieval over these collections.

### Machine Understanding
Safety-critical audio description (autonomous vehicles, surveillance, assistive devices) requires accurate captioning that does not hallucinate threats or miss concurrent events.

### Why Computational Humanities, Not Engineering
The humanistic lineage runs through two traditions that converge on this project:

- **Ekphrasis** — the classical rhetorical genre of verbal description of non-verbal aesthetic experience (Homer's Shield of Achilles → Heffernan 1993). AAC is the computational instantiation of ekphrasis for acoustic objects.
- **Soundscape studies** — R. Murray Schafer (1977) defines keynote sounds, soundmarks, and sound signals as objects of cultural analysis. A LALM trained on FreeSound has strong priors for sound signals, moderate priors for keynote sounds, and structurally absent priors for soundmarks — culturally-specific, geographically-anchored sounds like Bamberg Martinskirche bells. This is the mechanism behind RQ5.

The full critical apparatus (Truax 1984, Augoyard & Torgue 2006, Sterne 2012, Born 2013, Mitchell 1986) is developed in `literature_review.md` §13.

---

## What This Project Does

### Research Questions

| RQ | Question | Primary Metric | Layer |
|:---|:---------|:---------------|:-----:|
| **RQ0** | Does AF3's training data overlap with Clotho-eval? | Contamination % | 🟢 L1 |
| **RQ1** | Does AF3 (zero-shot) outperform the DCASE 2024 baseline on Clotho-eval? | SPIDEr-FL + BCa CI | 🟢 L1 |
| **RQ2** | Is the AF3-baseline gap larger on polyphonic clips than monophonic? | Δ SPIDEr-FL | 🟢 L1 |
| **RQ3** | What is AF3's entity hallucination rate vs. SALMONN? | CHAIR-audio dual criterion (two sub-hypotheses pre-registered: H3 = absolute rate, H4 = AF3 vs SALMONN gap — see `implementation_plan.md` §Hypotheses) | 🟢 L1 |
| **RQ4** | Do LALMs correctly order events in synthetic A-then-B mixtures? | Correct-ordering rate | 🔵 L2 |
| **RQ5** | Do LALMs generalise to culturally-grounded audio outside FreeSound? | **Primary claim is descriptive** (Schafer-framed qualitative audit). CLAPScore reported as a secondary indicator with `[LOW–MED applicability]` per LAION-CLAP training-domain mismatch on Germanic archival audio. | 🔵 L2 |

### Central Thesis

> **This project tests** whether current-generation LALMs — conditional on a passed training-set contamination audit (RQ0) — match or exceed the supervised DCASE 2024 baseline on Clotho v2.1 (the *performance* claim, RQ1), and **further hypothesises** that any such LALMs exhibit three structurally-related failure modes whose hypothesised shared root cause is the information bottleneck between the audio encoder and the LLM decoder, with no mechanism for concurrent-event segregation at the adapter layer (the *unified-mechanism* claim, RQ2–RQ4).
>
> The performance claim and the unified-mechanism claim are tested independently. Either may be falsified without the other; falsification of the unified-mechanism claim is an interesting result, not a project failure.

### What "Solved" Means per RQ

| RQ | Solved if | Falsified if |
|:---|:----------|:-------------|
| RQ0 | Contamination audit completes with disclosed overlap % | — (descriptive) |
| RQ1 | AF3 SPIDEr-FL BCa CI lower bound > 29.6% | CI lower bound ≤ 29.6% + 1.04 pp MDE |
| RQ2 | Δ(poly − mono) significantly > 0 | Δ within MDE or negative |
| RQ3 | AF3 hallucination rate < SALMONN by ≥ 5 pp | CIs overlap |
| RQ4 | Correct-ordering rate ≤ 60% for LALMs | Rate > 80% (mechanism weakened) |
| RQ5 | Qualitative soundmark gaps visible in captions | CLAPScore Δ < 0.05 vs in-distribution |

---

## Scope

### In-Scope
- Zero-shot inference with AF3, SALMONN, optionally Qwen2.5-Omni on Clotho v2.1.
- Contamination audit via FreeSound ID cross-referencing.
- Quantitative evaluation using SPIDEr-FL, CIDEr, SPICE, FENSE, CLAPScore, CHAIR-audio.
- Statistical analysis using BCa bootstrap CIs + Holm-Bonferroni correction.
- Humanities-framed qualitative analysis of cultural heritage audio (RQ5).
- Pre-registered hypotheses with per-RQ falsification criteria.

### Out-of-Scope
- Model training, fine-tuning, or LoRA adaptation.
- Real-time / streaming inference.
- Non-English captioning.
- Proposing new metrics or architectures.
- Human evaluation study (no ethics board approval timeline).

### Two-Layer Structure

#### Layer 1 — Course-Safe Core (Must Ship)

The minimum deliverable that stands on its own as a defensible 6 ECTS submission even if every ambitious extension fails.

| Component | What it covers | Kill criterion |
|:----------|:--------------|:---------------|
| **RQ0** — Contamination audit | FreeSound ID cross-reference | Must complete before any model evaluation |
| **RQ1** — AF3 vs DCASE baseline | SPIDEr-FL on Clotho-eval with BCa CI | Canary: baseline reproduces 29.6% ± 1% |
| **RQ2** — Polyphony differential | Δ SPIDEr-FL poly vs mono | κ ≥ 0.6 on annotation; if not, use AudioSet proxy |
| **RQ3** — Hallucination rate | CHAIR-audio dual criterion | AF3 + one comparison model (SALMONN or Qwen) |
| Metric stack | SPIDEr-FL, CIDEr, SPICE, FENSE, CLAPScore | `aac-metrics` reproduces known numbers |
| Dataset | Clotho v2.1 eval (1,045 clips) | Zenodo 4783391 accessible |
| Paper | ~15 pages, standard structure | Submitted Jul 6 |
| Talk | 15 min + Q&A | Delivered Jul 13 |

**If Layer 1 is complete, the project passes regardless of Layer 2 status.**

#### Layer 2 — Research-Grade Extension (Modular Ambition)

Each item is independent. Failure in any does not affect Layer 1.

| Cut | Component | Priority | Rationale |
|:---:|:----------|:---------|:----------|
| 1 | Qwen2.5-Omni ablation | Only if time | Adds model breadth but not thesis depth |
| 2 | **RQ4** — Temporal ordering | Should ship | Intellectually valuable but synthetic-only |
| 3 | Negative-control battery | Should ship | Tests confabulation mechanism directly |
| 4 | **RQ5** — Cultural heritage / Schafer | Should ship — thesis distinguisher | Last to cut — the humanities identity |

**Cut order:** When time/compute pressure forces scope reduction, cut in this exact order. Cut 1 drops first, Cut 4 drops last.

**Operational trigger for a cut.** A cut is invoked when **at least one** of the following holds at any weekly checkpoint (see §Phase Map / §Checkpoints): (a) the week's actual hours exceed **2× the phase-map estimate** for that phase; (b) any hard gate in §Checkpoints has FAILED and the documented fallback has been attempted but did not pass; (c) compute budget (RZ/Colab GPU-hours) on the active GPU profile is projected to exhaust before Phase 4 write-up begins. The decision-owner is the project author (sole operator); cuts are recorded inline in `research_notes.md` §3 (Lessons Learned) with date, trigger, and which item was cut. Full kill-criteria table lives in `implementation_plan.md` §Kill-criteria operational triggers.

**Items outside the cut ladder:**
- **Holm-Bonferroni correction** — conditional; apply automatically when ≥ 2 inferential hypotheses remain in scope.
- **DCASE 2026 workshop paper** — independent; not part of the project critical path; pursue only after Jul 13 talk.

---

## Phase Map

| Phase | Dates | Key Activities | Hard Gate |
|:------|:------|:---------------|:----------|
| **Phase 0** — Environment | → Apr 19 | Conda env, determinism pins, `setup_check.py`, `hypotheses_preregistered.yml` | `setup_check.py` exits 0 |
| **Phase 1** — Baseline + Audit | Apr 19 → May 4 | RQ0 contamination audit, data exploration, AF3 hello-world demo | Canary: DCASE baseline reproduces 29.6% ± 1% |
| **Phase 2** — Core Experiments | May 4 → May 18 | AF3 + SALMONN full eval, polyphony subset annotation, RQ1/RQ2/RQ3 | κ ≥ 0.6 on annotation; all BCa CIs computed |
| **Phase 3** — Failure Modes | May 18 → Jul 1 | RQ3 hallucination, RQ4 temporal, RQ5 humanities, negative controls | Layer-tagged; mixed 🟢/🔵 |
| **Phase 4** — Write-up | Jul 1 → Jul 13 | `make all` pipeline, paper draft, talk preparation | Paper submitted Jul 6; talk delivered Jul 13 |

Full operational details: `implementation_plan.md`.

---

## Checkpoints and Pivot Rules

| # | Date | Check | If FAIL |
|:-:|:-----|:------|:--------|
| 1 | Apr 19 | `setup_check.py` passes on RZ or Colab Pro | Fix environment — no experiments until pass |
| 2 | May 1 | RQ0 contamination audit complete | If overlap > 0: demote "zero-shot" to "audited-but-not-zero"; report clean-subset numbers |
| 3 | May 4 | DCASE canary reproduces 29.6% ± 1% | Metric pipeline broken — stop and debug |
| 4 | May 18 | κ ≥ 0.6 on polyphony annotation | Fall back to AudioSet proxy labels |
| 5 | Jun 15 | RQ1/RQ2/RQ3 results stable; CIs computed | Begin write-up on available results; cut Layer 2 if behind |
| 6 | Jul 1 | All results frozen; no new experiments | Write-up mode only |

**Red lines (stop-and-fix):**
- DCASE canary fails by > 2 pp → metric pipeline is broken.
- `setup_check.py` fails SM ≥ 8.0 gate → bf16 results invalid.
- `hypotheses_preregistered.yml` modified after Phase 2 data collection begins → HARKing violation.

---

## Dataset Strategy (Summary)

> **Mirror — canonical lives in `implementation_plan.md` §Dataset strategy.** This summary exists for orientation only; per-RQ provenance, version pins, SHA hashes, split fixes, and per-RQ data-quality gates are owned by the canonical and must not be restated here. Strategic rationale and rejected alternatives live in `research_notes.md` §Dataset-strategy rationale.

The project is **benchmark-first**. No full custom dataset collection is proposed anywhere. Only benchmark-based or derived-subset strategies are allowed unless a later evidence-backed exception is explicitly approved.

| RQ | Primary data | Strategy |
|:---|:-------------|:---------|
| RQ0 | Clotho v2.1 eval IDs × training manifests | use existing |
| RQ1 | Clotho v2.1 eval split | use existing |
| RQ2 | Clotho v2.1 eval + polyphony annotation | derived subset |
| RQ3 | AudioCaps single-event subset + AudioSet tags | derived subset |
| RQ4 | Synthetic A-then-B mixtures | derived synthetic |
| RQ5 | Cultural-archive sampling via APIs | existing via API |

Per-RQ provenance, version pins, SHA hashes, quality gates, rejected alternatives, and full rationale: see canonical in `implementation_plan.md` §11 and `research_notes.md` §5.5.

---

## Success Criteria

| Criterion | Layer | Measured by |
|:----------|:-----:|:------------|
| DCASE canary reproduced | 🟢 | 29.6% SPIDEr-FL within Labbeti 2024 reported seed-variance envelope (see `implementation_plan.md` §Canary tolerance) |
| RQ0 contamination audit complete | 🟢 | `results/contamination_audit.json` exists; per-corpus overlap % reported even if = 0 |
| RQ1 AF3 vs baseline comparison with BCa CIs | 🟢 | One-sided BCa CI lower bound reported and adjudicated against 29.6% per pre-registered falsifier |
| RQ2 polyphony differential measured | 🟢 | Δ SPIDEr-FL (poly − mono) with paired BCa CI |
| RQ3 hallucination rate measured | 🟢 | CHAIR-audio rate with BCa CI; both H3 (absolute) and H4 (AF3 vs SALMONN gap) sub-hypotheses adjudicated |
| RQ4 temporal ordering measured | 🔵 | Correct-ordering rate with BCa CI on synthetic A-then-B mixtures |
| RQ5 cultural heritage case study | 🔵 | Descriptive Schafer-framed audit (primary) + CLAPScore as secondary indicator with `[LOW–MED applicability]` qualifier |
| Paper submitted | 🟢 | Jul 6 |
| Talk delivered | 🟢 | Jul 13 |
| All code reproducible from `make all` | 🟢 | Pipeline exits 0 on fresh clone |

---

## Deliverables

| Deliverable | Deadline | Format |
|:------------|:---------|:-------|
| Term paper | Jul 6 | ~15 pages, LaTeX, standard academic structure |
| Talk | Jul 13 | 15 min presentation + Q&A |
| Repository | Jul 13 | Git repo with `Makefile`, notebooks, `environment.yml`, `hypotheses_preregistered.yml` |

---

## How the Documents Connect

```
                    ┌─────────────────────┐
                    │   PROJECT_GUIDE.md  │  ← You are here
                    │   (Entry Point)     │
                    └────────┬────────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
   ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
   │ literature_  │  │ research_    │  │ implementation_  │
   │ review.md    │  │ notes.md     │  │ plan.md          │
   │              │  │              │  │                  │
   │ Evidence     │  │ Strategy     │  │ Execution        │
   │ narrative    │  │ + evidence   │  │ + code stubs     │
   │              │  │ expansion    │  │ + kill criteria   │
   └──────┬───────┘  └──────────────┘  └──────────────────┘
          │
          ▼
   ┌──────────────┐
   │ paper_       │
   │ summaries.md │
   │              │
   │ Per-paper    │
   │ intake cards │
   └──────────────┘
```

### Boundary Rules

| Content type | Lives in | Does NOT live in |
|:-------------|:---------|:-----------------|
| Academic argument, evidence narrative, source citations | `literature_review.md` | implementation_plan, research_notes |
| Operational decisions, code stubs, environment specs, kill criteria | `implementation_plan.md` | literature_review, research_notes |
| Per-paper structured intake cards | `paper_summaries.md` | literature_review (which synthesises, not logs) |
| Strategic reasoning, open questions, evidence expansion protocol | `research_notes.md` | literature_review, implementation_plan |
| Project overview, scope, two-layer structure, glossary, document map | `PROJECT_GUIDE.md` | not duplicated elsewhere |

Where duplication is unavoidable, one file owns the canonical version and others cross-reference it with a link.

---

## Glossary

| Term | Definition |
|:-----|:-----------|
| **AAC** | Automated Audio Captioning — a machine learning task that outputs free-text descriptions of what a sound recording contains. Input: audio waveform. Output: grammatical sentence. |
| **AudioSet** | A 632-class hierarchical taxonomy of everyday sounds, developed by Google, with 2M+ labelled YouTube clips. Used in this project as the hallucination vocabulary for CHAIR-audio. |
| **BCa bootstrap** | Bias-Corrected-accelerated bootstrap — a statistical method for computing confidence intervals that corrects for bias and skewness in the sampling distribution. Preferred over plain percentile bootstrap for skewed AAC-score distributions. |
| **bf16** | Brain-float 16-bit — a numeric precision format for neural network computation that uses 8 exponent bits (same as fp32) but only 7 mantissa bits. Requires GPU compute capability SM ≥ 8.0 (Ampere or newer). |
| **CHAIR-audio** | Adapted from image captioning (Rohrbach 2018). Counts entities in a caption that are not grounded in the audio. This project uses a dual criterion: entity is hallucinated iff (a) absent from AudioSet tags AND (b) CLAPScore < 0.25. |
| **CLAPScore** | Contrastive Language-Audio Pretraining score. Cosine similarity between CLAP audio embedding and CLAP text embedding. Reference-free — does not need human captions. The only quantitative metric available for RQ5. |
| **Clotho v2.1** | The canonical AAC evaluation benchmark. 6,974 FreeSound clips with 5 human captions each. Evaluation split: 1,045 clips. Zenodo record **4783391** (not 3490684, which is v1). |
| **Cohen's κ** | Inter-annotator agreement statistic correcting for chance agreement. κ ≥ 0.6 is "substantial." Used as the gate for polyphony annotation quality in RQ2. |
| **Contamination audit** | Cross-referencing FreeSound IDs in Clotho-eval against training manifests of AF3, SALMONN, and related corpora (WavCaps, AudioSetCaps, Clotho-AQA) to check for data leakage. |
| **DCASE** | Detection and Classification of Acoustic Scenes and Events — an annual challenge series. Task 6 is audio captioning. The 2024 baseline achieves 29.6% SPIDEr-FL on Clotho-eval. |
| **Ekphrasis** | The classical rhetorical tradition of verbal description of non-verbal aesthetic experience. AAC is its computational instantiation for acoustic objects. |
| **FENSE** | Fluency- and Error-aware Sentence Embedding Score. Combines SentenceBERT similarity with a fluency penalty. Highest reported correlation with human quality judgement for audio captions. Requires reference captions. |
| **Hallucination** | A LALM mentioning sound entities not present in the audio. Driven by the LLM's text prior rather than acoustic evidence. Measured by CHAIR-audio. |
| **Holm-Bonferroni** | A statistical correction applied when testing multiple hypotheses simultaneously. Controls family-wise error rate. Uniformly more powerful than Bonferroni for k > 1. |
| **LALM** | Large Audio-Language Model. An LLM augmented with an audio encoder and adapter module so it can process audio input and generate text about it. |
| **MDE** | Minimum Detectable Effect — the smallest true difference a statistical test can reliably detect given sample size, variance, and significance level. |
| **Polyphony** | Multiple sound events occurring simultaneously in the same audio clip. The core challenge that current AAC systems fail at. |
| **Q-Former** | Querying-transformer — a small neural module that compresses audio encoder output into a fixed number of tokens the LLM decoder can consume. The information bottleneck in current LALM architectures. |
| **Soundmark** | (Schafer 1977) A community-specific sound of cultural identity — e.g., Bamberg Martinskirche bells. Structurally absent from web-scraped training corpora. Primary target of RQ5. |
| **SPIDEr-FL** | The official DCASE 2024 AAC metric. `SPIDEr = (SPICE + CIDEr) / 2`; `SPIDEr-FL = SPIDEr × Fluency_Error_Penalty`. Implemented by `aac-metrics`. DCASE 2024 baseline: 29.6%. |
| **Zero-shot** | The model produces captions for a dataset it was never explicitly trained on for the captioning task. A claim that RQ0 tests, not a premise to accept. |
