# Research Notes: Audio-to-Text Captioning using LALMs (T6)
*Master's Project — CH-Proj-M | SS 2026 | Zuraiz (2177213)*
*Prof. Dr.-Ing. Jakob Abeßer · Computational Humanities · Uni Bamberg*
*Last updated: April 2026 — Rebuilt version (documentation system redesign)*

---

## § 1. Strategic Positioning

### Why This Is a Computational Humanities Project

The grading criteria require a humanities contribution, not just an engineering evaluation. The AAC task sits at a productive intersection:

- **Engineering side:** LALM performance benchmarking, metric validation, failure-mode characterisation.
- **Humanities side:** AAC is the computational instantiation of *ekphrasis* — the rhetorical tradition of verbal description of non-verbal experience. The three failure modes (polyphony under-description, hallucination, temporal grounding loss) are not just performance bugs; they are *semiotic failures* — the machine's inability to translate acoustic experience into verbal description faithfully.

The Schafer (1977) anchoring is strategic: keynote sounds, soundmarks, and sound signals provide a vocabulary for describing *what AAC systems systematically miss* — a humanities-grade critique not visible through SPIDEr-FL alone. The full critical apparatus (Truax 1984, Augoyard & Torgue 2006, Sterne 2012, Born 2013, Mitchell 1986) is developed in `literature_review.md` §13 — this section does NOT restate that evidence.

### Positioning the Thesis on the Architecture Axis

The Discussion chapter's central argument runs on one axis:

```
SALMONN (2023)              AF3 (2025)              TAC (2026)
dual encoder +              unified encoder +        explicit temporal
Q-Former hedge              scale beats hedge         grounding head
       ↓                          ↓                        ↓
Architectural hedging   →   Scale + unified repr   →   "LLM decoder is
against diversity            beats dual-encoder          wrong for temporal"
```

- AF3 demonstrates that *scale + unified representation* renders architectural specialisation (SALMONN's dual encoder) unnecessary.
- TAC goes further and argues that the LLM-decoder paradigm itself is wrong for temporal description.
- The project sits at the AF3 position, testing whether the TAC critique applies to AF3's captioning.

This is the axis the Discussion chapter positions on. It is not a claim — it is a framing.

---

## § 2. Open Questions

These are unresolved questions that affect project decisions. They are answered as information becomes available throughout the project lifecycle. Mark each with its resolution when answered.

| # | Question | Affects | Status |
|:-:|:---------|:--------|:------:|
| Q1 | Does AF3's HuggingFace model card disclose all training datasets, or is the data card incomplete? | RQ0 contamination audit completeness | **WAITING-ON-REFETCH** — HuggingFace card not fully retrievable on Phase 1 web fetch (April 2026); re-attempt before May 4 lock; if still incomplete, RQ0 runs on cross-reference of {WavCaps, AudioSetCaps, Clotho-AQA} and the gap is recorded as a §9 threat-to-validity in `literature_review.md`. |
| Q2 | Has anyone published AF3 zero-shot captioning results on Clotho-eval by May 2026? | RQ1 novelty claim (empty-cell status) | **OPEN** — check at pre-literature-review-lock refresh |
| Q3 | Are TAC weights released by May 18? | RQ4 oracle comparison | **OPEN** — monitor sonalkum.github.io/tacmodel/ |
| Q4 | Can we get T1-group written consent for Bamberg bell recordings? | RQ5 data availability | **OPEN** — contact T1 group coordinator |
| Q5 | Does the 0.25 CLAPScore threshold for CHAIR-audio dual criterion survive sensitivity analysis? | RQ3 hallucination measurement validity | **OPEN — flagged free parameter.** Sensitivity at {0.20, 0.25, 0.30} is pre-registered as the primary deliverable; reporting rule in `implementation_plan.md` §4.4 declares the affected hypothesis `[INDETERMINATE — threshold-sensitive]` if two of three thresholds disagree — this applies to both H3 (absolute CHAIR-audio rate) and H4 (AF3 vs SALMONN gap), since both depend on the same CLAPScore threshold in the dual criterion. Wiki page `wiki/09_comparisons/clapscore-threshold-0-25.md` records residual uncertainty. |
| Q6 | Is Clotho-AQA the correct attribution (Lipping 2022)? Is the "Kumar 2026 TAC" reference real or hallucinated? | RQ0 manifest matching + RQ4 framing | **PARTIALLY RESOLVED (April 2026 Phase 1):** TAC = arXiv 2602.15766, Feb 2026, Kumar et al. (Adobe / Northwestern), CC-BY 4.0 — **CONFIRMED REAL**, no demotion needed. Clotho-AQA = Lipping 2022 — STILL OPEN until AF3 §3 is read; verify whether AF3 disclosed manifest names it explicitly. |
| Q7 | Does Martin-Morato 2024's variance estimate (σ ≈ 12 pp SPIDEr-FL) apply to greedy-decoding LALMs, or only supervised models with seed variance? | RQ1 MDE calculation validity | **OPEN** — the conservative estimate is used; sensitivity floor (σ ≈ 8 pp → MDE ≈ 0.73 pp) documented as alternative |

---

## § 3. Lessons Learned

*Populated during execution. Each entry records what happened, what was expected, and what the discrepancy teaches.*

| Date | Phase | Lesson | Impact |
|:-----|:------|:-------|:-------|
| 2026-04-20 | Phase 1 (audit + evidence refresh) | The headline AF3 MMAU number circulating in earlier internal drafts (72.28) is a digit error; the AF3 paper body (results tables) reports **72.42** (the abstract does not contain a specific MMAU number). The earlier value had been propagated across `literature_review.md`, `paper_summaries.md`, and the wiki without ever being checked against the primary source. | Headline numbers must be web-fetched from the primary source at insertion time and on every refresh; the `[Author Year; Lx; CONF/APPLIC]` badge is necessary but not sufficient. Corrected in `literature_review.md` §4.3 and `paper_summaries.md` P8 on the same date. |
| 2026-04-20 | Phase 1 | "Kumar 2026 TAC" was at audit-time tagged as a Tier-1 risk (possible hallucination). Phase 1 verification confirmed the paper exists at arXiv 2602.15766, posted Feb 17 2026, CC-BY 4.0. | Future-dated citations require explicit verification before they enter the docs; once verified, the verification source is logged inline (here and in `paper_summaries.md` P11). RQ4 framing is unblocked. |
| 2026-04-20 | Phase 1 | RQ0 input completeness — AF3's HuggingFace model card was not fully retrievable on the Phase 1 web fetch attempt. | Q1 status moved from OPEN to **WAITING-ON-REFETCH**; RQ0 plan now has a documented fallback (cross-reference of {WavCaps, AudioSetCaps, Clotho-AQA}) and a §9 threat-to-validity entry if the gap persists. |

---

## § 4. RQ Experiment-Design Matrix (Wohlin 2012 §6)

One row per RQ. Every cell must be populated before Phase 2 begins — empty cells signal a design gap.

| RQ | Metric | Statistical test | Data source | n | MDE / power | Threats axis | Falsifier |
|:---|:-------|:-----------------|:------------|:-:|:------------|:-------------|:----------|
| RQ0 | contamination % | descriptive | FreeSound IDs cross-ref vs WavCaps + Clotho-AQA + AudioSetCaps | 1,045 | n/a | Construct (C4) | 0% overlap → null result |
| RQ1 | SPIDEr-FL | one-sided BCa (Holm-adj) | Clotho-eval CLEAN | ≤1,045 | 1.04 pp | Internal (I1), External (E1), Conclusion (V1,V2) | CI lower ≤ 29.6% |
| RQ2 | Δ SPIDEr-FL (poly−mono) | paired BCa (Holm-adj) | Clotho-eval subset | ~500 | 1.50 pp | Construct (C3), Conclusion (V3) | Δ > −3.5 pp OR p ≥ 0.05 |
| RQ3 | CHAIR-audio rate | two-sample BCa | AudioCaps single-event | 500 | 1.25 pp | Construct (C2) | Rate(AF3) − rate(SALMONN) < 5 pp OR CIs overlap |
| RQ4 | correct-ordering rate | descriptive + BCa CI | Synthetic A-then-B | 50 | — | Construct (C3), External (E2) | Rate > 60% |
| RQ5 | CLAPScore | descriptive | Bamberg bells / BBC archive | ≤ 20 | — | Construct (C1), External (E1) | Δ < 0.05 vs in-dist baseline |
| **Neg-ctrl** | CHAIR-audio rate | descriptive + BCa CI | Silence / white / pink / tones | 30 | — | Construct (C1) | Rate < 50% → weakening of §5.2 mechanism |

**Method sources.** MDE derivation (`MDE ≈ 2.8 × SE`, with `SE = σ / √n`) per Cohen 1988. BCa 95% CI construction per Efron & Tibshirani 1993 ch. 14 (seed=42, n=1000 resamples). Variance floors (σ≈12 pp SPIDEr-FL, ≈4 pp FENSE, ≈0.03 CLAPScore) per Martin-Morato 2024 — full derivation in `literature_review.md` §10.

---

## § 5. Evidence Expansion Strategy

This is the operational system for finding, evaluating, and integrating new evidence throughout the project lifecycle.

### A. Source Hierarchy

Consult sources in this priority order. Higher-priority sources override lower-priority ones on factual claims.

| Priority | Source type | Examples | Trust level |
|:--------:|:------------|:---------|:------------|
| 1 | Official benchmark pages, dataset docs, model cards, official repos | DCASE challenge page, Zenodo dataset records, HuggingFace model cards, GitHub repos for AF3/SALMONN/aac-metrics | Highest — primary source for specs, versions, licences |
| 2 | Peer-reviewed papers | Published at ACL, EMNLP, ICASSP, Interspeech, ECCV, NeurIPS, DCASE Workshop | High — claims have survived review |
| 3 | Official baselines and challenge reports | DCASE Task 6 baseline (Labbeti 2024), challenge summaries | High — community-vetted benchmarks |
| 4 | Strong recent preprints directly relevant to the question | arXiv papers from established labs (NVIDIA, Tsinghua, Alibaba) with public code | Medium — not yet peer-reviewed; use with explicit L3 disclosure |
| 5 | Secondary technical commentary | Blog posts, tutorials, technical discussions | Low — use only if it adds implementation insight not available elsewhere |

### B. Search Locations

| Location | URL | What to search for |
|:---------|:----|:-------------------|
| Google Scholar | scholar.google.com | Broad field queries, citation tracking, related work |
| arXiv | arxiv.org (cs.SD, cs.CL, cs.MM, eess.AS) | Preprints, latest model papers, emerging methods |
| ACL Anthology | aclanthology.org | NLP-side audio understanding, captioning evaluation |
| IEEE Xplore | ieeexplore.ieee.org | ICASSP papers (audio processing, metrics) |
| DCASE community | dcase.community | Challenge baselines, task descriptions, evaluation protocols |
| HuggingFace | huggingface.co/models, huggingface.co/datasets | Model cards (AF3, SALMONN, Qwen), dataset cards (WavCaps, Clotho) |
| GitHub | github.com | Official repos for: dcase2024-task6-baseline, audio-flamingo, SALMONN, aac-metrics, laion-clap |
| Semantic Scholar | semanticscholar.org | Citation graphs, influence tracking, "cited by" for core papers |
| Zenodo | zenodo.org | Dataset version records (Clotho v2.1 = record 4783391) |

### C. Seed Queries

Organised by topic. Run these at project start and at each refresh checkpoint.

**Task / field overview:**
- `"automated audio captioning survey 2024 OR 2025 OR 2026"`
- `"audio-to-text captioning large audio language models"`
- `"audio captioning benchmark Clotho v2.1 DCASE Task 6"`

**Models:**
- `"Audio Flamingo 3 audio captioning"`
- `"SALMONN audio captioning Clotho"`
- `"Qwen2.5-Omni audio understanding captioning"`
- `"timestamped audio captioning temporal grounding audio"`

**Failure modes:**
- `"audio captioning hallucination benchmark"`
- `"polyphonic audio captioning concurrent sound events"`
- `"temporal grounding audio language model captioning"`

**Metrics:**
- `"SPIDEr-FL audio captioning metric validity"`
- `"FENSE audio captioning evaluation"`
- `"CLAPScore audio-text evaluation audio captioning"`
- `"CHAIR hallucination metric audio captioning"`

**Validity / contamination / reproducibility:**
- `"Clotho WavCaps contamination Freesound"`
- `"audio captioning benchmark leakage dataset overlap"`
- `"reproducibility audio captioning evaluation metrics"`

**Humanities / impact:**
- `"soundscape studies soundmark audio archives"`
- `"cultural heritage audio captioning accessibility"`
- `"ekphrasis sound studies computational humanities"`

**Emergent queries:** (populated during execution — see §H below)

### D. Refresh Checkpoints

Re-run seed queries (§C) and check model cards / dataset pages at each of these points:

| Checkpoint | Date | What to check | Why |
|:-----------|:-----|:--------------|:----|
| Pre-literature-review lock | Before May 4 | All seed queries. New papers in cs.SD, cs.CL since project start. AF3/SALMONN model card updates. | Ensures lit review is current before Phase 2. |
| Pre-implementation lock | May 4 | Model cards for version changes. `aac-metrics` changelog. Clotho/AudioCaps dataset errata. | Catches breaking changes before experiments run. |
| Pre-experiment | May 18 | Targeted queries for failure modes + contamination. Check if anyone else has published AF3 captioning results. | Avoids scooping. Avoids replicating known bugs. |
| Pre-discussion write | Jul 1 | All seed queries. Focus on papers published May–Jun 2026 that might affect claims. | Ensures Discussion cites the latest relevant work. |

### E. Inclusion Rules

A new source is added to the project documentation only if it does **at least one** of the following:

| Criterion | Example |
|:----------|:--------|
| Strengthens a core claim | A new study confirms AF3 outperforms prior LALMs on a related benchmark |
| Challenges an existing assumption | A paper shows CHAIR-audio dual criterion misses a class of hallucinations |
| Updates an outdated comparison | AF3 v2 is released with different architecture |
| Improves a methodological decision | A better bootstrap variant for small audio samples is published |
| Exposes a real risk | Clotho v2.1 errata are announced |
| Fills a genuine conceptual gap | A humanities paper on machine ekphrasis is published |

If a source does **none** of these, it is noise. Do not add it.

### F. Evidence Logging Template

Every new source that passes the inclusion filter is logged with this structure:

```
### [Author Year] — [Short title]
- **Citation:** [full citation]
- **Year:** [year]
- **Source type:** [peer-reviewed / preprint / model card / dataset doc / challenge report / other]
- **Relevance:** [which RQ or literature_review section it feeds]
- **Key claim:** [1–2 sentences]
- **Why it matters:** [1 sentence: what changes if we use this]
- **Confidence:** [HIGH / MED / LOW]
- **Applicability:** [HIGH / MED / LOW]
- **Required action:** [update lit review §X / update implementation_plan step Y / no action — context only]
- **Changes docs/plan?** [YES — specify what changes / NO]
```

**Example (pre-filled):**

```
### Goel 2025 — Audio Flamingo 3 (project key: Ghosh 2025b retained for back-compat)
- **Citation:** Goel★, Ghosh★ et al. (co-first authors, equal contribution / alphabetical order), "Audio Flamingo 3", arXiv 2507.08128, Jul 2025. Preprint; peer-review status unverified.
- **Year:** 2025
- **Source type:** preprint (NVIDIA, public code)
- **Relevance:** RQ1 primary model, literature_review §4.3
- **Key claim:** Unified AF-Whisper encoder (lineage: AF-CLAP) achieves SOTA on MMAU (**72.42** — corrected 2026-04-20 from earlier 72.28 digit error), ClothoAQA (91.1%), CMM-Hallucination (86.7%). All numbers preprint, single-team, not independently replicated.
- **Why it matters:** AF3 is the primary model for all experiments; its architecture (unified vs dual encoder) is the central thesis thread.
- **Confidence:** HIGH
- **Applicability:** MED (Q1 OPEN — HuggingFace data card not yet refetched; full open-data claim contingent on enumeration)
- **Required action:** Already integrated. Monitor for peer-reviewed version or updated model card. Refetch HF card to close Q1.
- **Changes docs/plan?** NO — already the project's primary model.
```

### G. Contradiction Handling

When a new source appears that may conflict with existing project assumptions, answer these four questions before deciding what to do:

| # | Question | If YES |
|:-:|:---------|:-------|
| 1 | Does it support the current plan? | Log it as confirming evidence. No action needed beyond documentation. |
| 2 | Does it weaken an existing assumption? | Flag the assumption in Open Questions (§2). Assess severity: does the assumption affect Layer 1 or Layer 2 only? If Layer 1: pause and re-evaluate before proceeding. If Layer 2: note it and continue. |
| 3 | Does it force a change in scope, method, model, or metric? | Update the affected document (literature_review, implementation_plan, or both). Log the change in the evidence log with a clear before/after note. |
| 4 | Is it context-only, or execution-changing? | If context-only: add to literature_review or research_notes as background. If execution-changing: update implementation_plan and re-check downstream dependencies. |

If the contradiction cannot be resolved with available evidence, state the ambiguity explicitly in the relevant document. Do not silently pick one side.

### H. Emergent Queries

*This section starts empty. It is the only part of the evidence expansion strategy that is intentionally left open.*

New queries are added here when:
- an experiment produces a surprising result,
- a reviewer or supervisor raises a question the current evidence cannot answer,
- a new model, dataset, or metric is released that affects the project.

Each emergent query is logged with:
- **Trigger:** what caused the search
- **Query terms:** the actual search strings used
- **Results:** whether any findings changed project decisions

| Date | Trigger | Query | Result | Action |
|:-----|:--------|:------|:-------|:-------|
| | | | | |

---

## § 5.5 Dataset-Strategy Rationale (MIRROR)

> **Mirror — canonical lives in `implementation_plan.md` §11 (Dataset Strategy).** This section holds *only* what is **not** in the canonical: rejected alternatives, reasons for rejection, and residual tensions. The per-RQ table, version pins, and quality gates are owned by the canonical and **must not be restated here**. If a per-RQ choice changes, edit only the canonical; this section is then re-checked for consistency, not rewritten.

### 5.5.1 Why benchmark-first rather than custom collection

The decision rule is `benchmark-first; derived subset second; new collection forbidden without explicit evidence-backed exception`. Three reasons:

1. **Comparability.** Custom evaluation sets break direct comparability with the DCASE 2024 baseline (29.6% SPIDEr-FL on Clotho-eval). RQ1 *is* a comparison against that floor; without the same evaluation universe, the comparison is meaningless.
2. **Foolproofness.** Custom collection introduces failure modes (licensing, annotation drift, contamination of own audit) that a 12-ECTS solo project cannot reliably control. The cost-of-failure is asymmetric.
3. **Honest scope.** "I built a new audio captioning benchmark" is a different project than this one and would require its own scope, ethics review, and timeline. Layering a benchmark-construction subproject onto an evaluation thesis is the kind of scope creep the §10 cut ladder exists to prevent.

### 5.5.2 Rejected alternatives (per RQ)

| RQ | Rejected | Why rejected |
|:---|:---------|:-------------|
| RQ0 | Build a fresh contamination detector from raw FreeSound + manual cross-reference | Published training manifests are already the only ground truth; a custom detector duplicates effort and adds a new fallibility layer (false positives from filename canonicalisation). |
| RQ1 | Custom Clotho-comparable eval set | Directly breaks the 29.6% comparison. Eliminates the project's central RQ1 statement. |
| RQ2 | Use MACS or NonSpeech7k as the polyphonic dataset | MACS lacks Clotho-comparable five-caption per clip references; NonSpeech7k is a different task (event detection, not captioning). Comparing AF3's polyphonic captioning across two non-comparable evaluation universes is uninterpretable. |
| RQ2 | Skip polyphony annotation entirely; rely only on AudioSet proxy | AudioSet tags are an acknowledged under-counting label set (Gemmeke 2017 §IV); using them as the *primary* polyphony signal would itself become a methodological threat. The 200-clip κ ≥ 0.6 manual annotation is the structurally cleaner primary; AudioSet proxy is the documented fallback. |
| RQ3 | Use Clotho instead of AudioCaps for hallucination | AudioCaps single-event clips give a tractable controlled-stimulus design for CHAIR-audio dual criterion; multi-event Clotho captions make per-entity grounding ambiguous (which of five reference captions is "the" reference for the entity?). |
| RQ4 | Wait for a natural temporal-order corpus to be released | None exists with reliable ground-truth onset labels. The synthetic A-then-B pipeline (Kumar 2026 TAC) is the protocol the field uses for this question. RQ4's external-validity caveat is honestly disclosed. |
| RQ5 | Custom recording session of Bamberg bells, market sounds, etc. | Foolproofness: licence/consent overhead; recording-quality variance; no ethics-board timeline. The DARIAH/BL/BBC/Europeana API route returns curated, licensed, archive-grade audio with metadata — strictly better evidential value with strictly less risk. |
| RQ5 | LAION-CLAP-trained CLAPScore as the *primary* metric | Training-domain mismatch (web-scraped, English-leaning) makes any single number unstable on Germanic archival audio. Demoted to secondary indicator with `[LOW–MED applicability]`; primary claim is the descriptive Schafer-framed audit. |

### 5.5.3 Residual tensions accepted

- **AudioSet under-counting** raises proxy-fallback uncertainty for RQ2; acknowledged in `audioset_proxy_fallback()` contract (`implementation_plan.md` §4.3).
- **AF3 data card incompleteness** (Q1 above) means RQ0 may be partially-answerable; documented as a §9 threat in `literature_review.md`, not silently absorbed.
- **TAC weights unreleased** (Q3 above) means RQ4 may run without an oracle; documented as R6 in `implementation_plan.md` §8.

### 5.5.4 Exception clause

A custom-collection exception requires, in writing here, **before any data is gathered**:
1. The benchmark/derived-subset alternatives that have been ruled out (with reasons),
2. The specific evidence-backed reason a derived subset cannot answer the question,
3. A licence + ethics + storage plan,
4. Supervisor sign-off recorded in §3 Lessons Learned.

No exception has been invoked as of April 2026.

---

## § 6. Conceptual Links

Cross-connections between project components that don't fit in the operational plan or evidence narrative:

1. **Polyphony → Hallucination → Temporal loss = one root cause.** The Q-Former information bottleneck destroys concurrent-event separation → LLM operates under-constrained → text prior fills the gap. This chain links RQ2, RQ3, and RQ4 mechanistically. If RQ2 shows no polyphony-specific gap, the chain breaks and the Discussion chapter must weaken the unified-root-cause claim. See `literature_review.md` §5 for full RCA.

2. **Soundmark ↔ Domain shift.** Schafer's soundmark concept (§1) provides the theoretical vocabulary for the empirical observation that LALMs trained on FreeSound lack priors for culturally-specific sounds. This is the link from humanities framing to quantitative RQ5 (CLAPScore drop on Bamberg bells).

3. **Ekphrasis ↔ inter-modal translation loss.** The sister-arts tradition (Mitchell 1986) predicts that cross-modal translation is always lossy, and that the loss is theoretically interesting. AAC inherits this — the three failure modes are the *specific form* of the translation loss. This is the Discussion chapter's horizon, not an empirical claim.

4. **Contamination ↔ "zero-shot" framing.** RQ0 is not a standalone contribution — it gates the interpretation of RQ1. If contamination is found, every "zero-shot" claim in the project is reframed. This dependency is why RQ0 runs first.

---

## § 7. Emerging Ideas

*Populated during execution. Each entry captures an idea that emerged during the project and may feed future work.*

| Date | Idea | Status |
|:-----|:-----|:-------|
| 2026-04-20 | **PolyBench (Mar 2026, arXiv 2603.05128; submitted to INTERSPEECH 2026)** introduces a five-subset polyphonic benchmark (counting, classification, detection, concurrency, duration). Abstract reports "consistent performance degradation in polyphonic audio, indicating a fundamental bottleneck" for state-of-the-art LALMs. Whether AF3 is specifically included and whether the bottleneck is at the encoder-to-LLM interface requires full-paper verification. Strengthens the *motivation* for RQ2 but post-dates AF3 and does not replace it. Future-work idea: replicate PolyBench's "concurrency" subset on AF3. | NOTED — referenced in `literature_review.md` §5.1; wiki source card `wiki/08_sources/polybench-2026.md` |
| 2026-04-20 | **AF3 co-first-author correction** (Goel★ and Ghosh★ are equal-contribution, alphabetical order — not a single lead author). Future cite-checking discipline: when a project key was assigned from a citation rather than the primary source, verify authorship against the arXiv listing and project page on first ingest. | NOTED — corrected in `literature_review.md` §4.3 and `paper_summaries.md` P8 |

---

## § 8. Reading Order

| # | Paper | Read before | Conf | Applic | Role in thesis |
|:-:|:------|:------------|:----:|:------:|:---------------|
| 1 | Drossos 2020 (Clotho) | Phase 1 | HIGH | HIGH | Dataset + task definition |
| 2 | Kim 2019 (AudioCaps) | Phase 1 | HIGH | HIGH | RQ3 dataset |
| 3 | Mei 2022 (AAC survey) | Phase 1 | HIGH | HIGH | Related Work backbone |
| 4 | Labbeti 2024 (DCASE baseline) | Phase 1 | HIGH | HIGH | 29.6% floor; canary |
| 5 | Tang 2023 (SALMONN) | Phase 2 | HIGH | MED | Baseline LALM |
| 6 | Ghosh 2025a (AF2) | Phase 2 | HIGH | HIGH | AF-CLAP lineage |
| 7 | Ghosh 2025b (AF3) | Phase 1 | HIGH | HIGH | Primary model |
| 8 | Qwen 2025 (Qwen2.5-Omni) | Phase 3 (if ablation) | HIGH | HIGH | Optional ablation |
| 9 | Kuan 2024 (LALM limits) | Phase 1 | HIGH | HIGH | RQ3 theory |
| 10 | Kumar 2026 (TAC) | Phase 2 | HIGH | HIGH | RQ4 oracle |
| S1 | Zhou 2022 (FENSE) | Phase 1 | HIGH | HIGH | Primary metric pair |
| S2 | Wu 2023 (LAION-CLAP) | Phase 1 | HIGH | HIGH | RQ5 mandatory |
| S3 | Rohrbach 2018 (CHAIR) | Phase 2 | HIGH | MED | Adapted for audio |
| S4 | Schafer 1977 (Soundscape) | Phase 1 | HIGH | HIGH | Humanities anchor |
| S5 | Holm 1979 | Phase 1 | HIGH | HIGH | MTP correction |
| S6 | Efron & Tibshirani 1993 ch. 14 | Phase 1 | HIGH | HIGH | BCa bootstrap |
| S7 | Gemmeke 2017 (AudioSet) | Phase 2 | HIGH | HIGH | Ontology |

MED applicability rows flag adaptation risk — these papers' findings require domain translation (MIR → AAC, image → audio). Adaptation disclosed in Methodology.

---

## § 9. Software Stack

```bash
# 1. Environment
conda create -n t6-aac python=3.11
conda activate t6-aac

# 2. Core ML (CUDA 12.1)
pip install torch==2.4.* torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install transformers==4.44.* accelerate bitsandbytes

# 3. Audio I/O + datasets
pip install librosa==0.10.* soundfile resampy
pip install aac-datasets    # Clotho v2.1 / AudioCaps loaders

# 4. Metrics (install ALL on Day 1 — Java issue surfaces early)
pip install aac-metrics     # SPIDEr-FL, SPICE, CIDEr — requires Java 11+
pip install fense           # FENSE learned metric
pip install bert-score
pip install pycocoevalcap   # BLEU/METEOR/CIDEr fallback
# Verify Java: java -version (must be 11+)

# 5. Hallucination analysis (RQ3)
pip install spacy
python -m spacy download en_core_web_sm
# AudioSet ontology: https://github.com/audioset/ontology (download ontology.json)

# 6. Analysis + reporting
pip install jupyter pandas matplotlib seaborn
```

**Model loading (HuggingFace):**
- ⭐ Primary: `nvidia/audio-flamingo-3` — 8B params, ~20GB VRAM bf16 / ~10GB int4
- Secondary: `tsinghua-ee/SALMONN` — 13B, ~24GB bf16 / ~14GB int4
- Optional: Qwen2.5-Omni (Apache-2.0)
- TAC: weights not yet released as of Apr 2026; monitor sonalkum.github.io/tacmodel/

---

## § 10. May-4 Talk Branching by RQ0 Outcome

The May-4 talk must branch dynamically based on what the contamination audit actually reveals.

### Branch A — Clean fraction = 100%
Standard narrative: thesis as planned. Zero-shot claim fully supported. Play live AF3 demo.

### Branch B — 0 < clean fraction < 100%
**Lead with the finding, not the demo.** Reframe:
- Slide 2: *"We measured AF3's training-set overlap with Clotho-eval. Result: k/1045 (= X%)"*. This is itself a novel contribution.
- Slide 6 (RQ0) is now the highlight slide.
- RQ1 reported on clean subset with explicit note on overlap.
- Detail the derivation chain (FreeSound / WavCaps / AudioSetCaps).

### Branch C — Clean fraction = 0% (catastrophic)
**Pivot talk to a negative result with scope update.**
- Talk argues: zero-shot is an irreducibly confounded claim for frontier LALMs trained on the web-accessible audio commons.
- Scope pivot: project reframes around hallucination (RQ3) and temporal grounding (RQ4) — both orthogonal to training-data leakage.
- RQ1 demoted to a descriptive benchmark comparison without the "zero-shot" label.

---

## § 11. Glossary for Humanities Examiners

See `PROJECT_GUIDE.md` § Glossary for the full 20-term glossary.

---

## Evidence Provenance & Trail

All claims traceable to primary sources verified April 2026:

| # | Source | Level | Year | Conf | Applic | Status |
|:-:|:-------|:------|:----:|:----:|:------:|:------:|
| 1 | Clotho v2.1 (Zenodo 4783391), AudioCaps, SALMONN, AF2, AF3, Qwen2.5-Omni, TAC, DCASE 2024, aac-metrics | L1/L2 | — | HIGH | HIGH | ACCEPTED |
| 2 | Martin-Morato et al. — AAC metric variance | L2 | 2024 | HIGH | MED | ACCEPTED |
| 3 | Wohlin et al. — *Experimentation in SE* §6 (Springer 2012) | L2 | 2012 | HIGH | HIGH | ACCEPTED |
| 4 | Landis & Koch — Biometrics 33(1) (1977) | L2 | 1977 | HIGH | HIGH | STALE-VALID |
| 5 | Drossos et al. — Clotho §3.2 (ICASSP 2020) | L2 | 2020 | HIGH | HIGH | ACCEPTED |
| 6 | Efron & Tibshirani — *Intro to the Bootstrap* ch. 14 | L2 | 1993 | HIGH | HIGH | STALE-VALID |
| 7 | Audio Flamingo Next (arxiv 2604.10905), Semantic-Aware Confidence Calibration (arxiv 2512.10170) | L3 | 2025/26 | MED | MED | `[BLEEDING-EDGE]` — cite with caution |

> [!CAUTION]
> Do not cite blog posts, Medium articles, or LinkedIn posts as evidence. Per academic standards, only peer-reviewed papers (L2) and official technical reports (L1) count.
