# Research Notes: Audio-to-Text Captioning using LALMs (T6)
*Master's Project — CH-Proj-M | SS 2026 | Zuraiz (2177213)*  
*Prof. Dr.-Ing. Jakob Abeßer · Computational Humanities · Uni Bamberg*  
*Last updated: April 2026 — Definitive Merged version (v5 + CC v6)*

---

## § 1. Task Definition & Humanities Framing

**Automated Audio Captioning (AAC)** is an *inter-modal translation* task: raw audio waveform → free-text natural-language description of the acoustic scene.

| Task | Output | Example |
|:-----|:-------|:--------|
| Audio Tagging | Multi-label class set | `{dog, traffic, wind}` |
| ASR (Speech-to-Text) | Transcript of words *spoken* | *"Hello, how are you?"* |
| **AAC (our task)** | Free-text scene description | *"A dog barks in the distance as cars pass on a wet road while wind rustles nearby leaves."* |

The defining difference is **description** — a grammatical sentence capturing event identities, acoustic texture, spatial cues, and temporal relations. Traditional classifier-based taggers fundamentally fail here. LALMs offer a step-change.

### Why this is a *Computational Humanities* project, not an Engineering project

This distinction matters for the grading criteria. The humanistic anchor for AAC is **ekphrasis** — the rhetorical tradition of verbal description of non-verbal experience (cf. Homer's Shield of Achilles, *Iliad* 18). In musicology and sound studies, AAC is the machine-listening counterpart to descriptive criticism.

Three humanities-adjacent use cases frame why this research matters beyond leaderboard chasing:

1. **Soundscape studies.** R. Murray Schafer's *The Tuning of the World* (1977) defines "keynote sounds," "soundmarks," and "sound signals" as objects of cultural analysis — the same objects a well-functioning AAC system must describe. This is the direct intellectual lineage from T1 (Bamberg church bells) and T2 (ERBA-Insel ecoacoustics) to T6.
2. **Accessibility.** Audio captions for cultural heritage recordings (oral history, radio archives, folk music fieldwork) enable blind and low-vision access to sound collections.
3. **Digital archives & search.** Free-text captions enable semantic retrieval over sound archives (British Library, Europeana Sounds, BBC Sound Effects) — an explicit goal of the DARIAH-EU digital humanities infrastructure.

This framing is **the humanities contribution** of the thesis and distinguishes it from a routine DCASE replication study.

> **Extended humanities lineage.** Schafer 1977 is the working-notes anchor; the full critical apparatus (Heffernan 1993 on ekphrasis; Truax 1984 on listening modes; Augoyard & Torgue 2006 on sonic effects; Sterne 2012 on post-humanities sound; Born 2013 on spatialisation; Mitchell 1986 on sister-arts iconology) is developed in `literature_review.md` §13.

---

## § 2. Three Failure Modes — The Research Gap

> [!IMPORTANT]
> These three failure modes are the *research gap*. They are structurally related: polyphonic scenes trigger hallucination (the model falls back on its text prior rather than audio evidence), and the fallback also corrupts temporal structure. A strong thesis argues they share a root cause — audio-encoder information bottleneck.

### 2.1 Polyphony Under-Description
Real-world audio is rarely monophonic. Standard encoder-decoder AAC models describe only the *dominant* event, systematically dropping concurrent secondary events. Even LALMs exhibit this bias when one sound is acoustically louder than another.

### 2.2 Entity Hallucination
LALMs *confabulate* sounds not present in the audio. Documented by Kuan et al. (*Understanding Sounds, Missing the Questions*, Interspeech 2024) and operationalized as the **CMM-Hallucination benchmark** (Audio Flamingo 3 reports 86.7% on this benchmark). Root cause: the text-decoder has strong priors over plausible sentence patterns and completes them even without audio support. Mitigation work: *Semantic-Aware Confidence Calibration for AAC* (arxiv 2512.10170).

### 2.3 Temporal Grounding Loss
LALMs default to **canonical orderings** learned from training text rather than actual onset order in the audio. **TAC — Timestamped Audio Captioning** (Kumar et al., Adobe/Northwestern, arxiv 2602.15766, Feb 2026) is the first model to directly address this, producing captions of the form *"At 2.1s a dog begins to bark. At 5.4s a car horn overlaps."* It uses a synthetic-mixture training pipeline and reports measurably lower hallucination rates.

---

## § 3. The LALM Landscape — 2023 → 2026 Timeline

All LALMs share one architectural blueprint:

```
[ Audio Waveform ]
      ↓
[ Audio Encoder ]     ← Whisper | BEATs | PANNs | AST | CLAP | AF-CLAP (custom)
      ↓
[ Adapter / Q-Former ] ← bridges audio-embedding space to LLM token space
      ↓
[ LLM Decoder ]       ← Vicuna | LLaMA-3.1 | Qwen-2.5 | BART | custom transformer
      ↓
[ Generated Caption ]
```

### 3.1 Extended LALM Timeline (parameter count + training scale + encoder status)

| Year–Mo | Model | Params (total) | Audio encoder | Encoder frozen? | Training audio hours | Evidence |
|:--------|:------|:--------------:|:--------------|:---------------:|:---------------------:|:---------|
| 2023-10 | SALMONN | 13B | Whisper-L + BEATs | ✅ both frozen | ~680k (Whisper) + AudioSet | `[Tang 2023; L2]` |
| 2023-11 | Qwen-Audio | ~8B | Whisper-L (modified) | ❌ fine-tuned | ~280k ~estimate | `[Chu 2023; L3]` |
| 2024    | DCASE 2024 baseline (CNext-trans) | ~50M | ConvNeXt | ❌ supervised end-to-end | Clotho-train only | `[Labbeti 2024; L1]` |
| 2025-03 | Audio Flamingo 2 | 3B / 7B | AF-CLAP (custom) | ❌ AF-CLAP trained in-house | ~8M clips ~estimate | `[Ghosh 2025a; L3]` |
| 2025-03 | Qwen2.5-Omni | 7B | Whisper-based | ❌ end-to-end multimodal | undisclosed; likely ~1M hr | `[Qwen 2025; L3]` |
| 2025-07 | **Audio Flamingo 3** ⭐ | 8B | Unified AF-CLAP | ❌ contrastive pretrain + end-to-end FT | ~10M clips ~estimate | `[Ghosh 2025b, arxiv 2507.08128; L3]` |
| 2026-02 | TAC | ~200M ~estimate | PANNs-based | ❌ trained with temporal head | synthetic mixtures + AudioCaps | `[Kumar 2026; L3]` |

`~estimate` flags cells populated from L3/L4 evidence (training-data disclosures on GitHub or HF cards). Report as ranges in the term paper if the exact figure is material.

**Why this matters.** Parameter count and training-data scale are confounders in RQ1 (lit-review threat I1). A fair comparison at the architecture level would require matched compute; that is out of scope. The paper Discussion explicitly frames RQ1 as descriptive (which wins) not causal (why).

### Critical architectural comparison

```
SALMONN (2023):
  [Whisper-L (speech)] ──┐
                          ├──→ [Q-Former] ──→ [Vicuna-13B] ──→ caption
  [BEATs (events)] ──────┘
  → Dual encoder is an explicit hedge against polyphony; doubles compute

Audio Flamingo 3 (2025):
  [Unified AF-CLAP encoder + long-context adapter] ──→ [AF LLM 8B] ──→ caption/QA/reasoning
  → Single unified encoder trained at massive scale beats dual-encoder SALMONN

TAC (2026):
  [PANNs-based encoder + temporal grounding head] ──→ timestamped caption
  → Argues LLM-decoder is the wrong architecture for temporal description
```

> **Key insight for your thesis:** AF3 demonstrates that *scale + unified representation* beats *architectural hedging* (SALMONN's dual encoder). TAC goes further and argues that the LLM-decoder paradigm itself is wrong for temporal grounding. Positioning your work on this axis is the foundation of a strong discussion section.

---

## § 4. Datasets

A critical and common mistake: treating all audio-caption datasets as interchangeable. They are not.

### Evaluation datasets — use for reporting final results

| Dataset | Size | Duration | Captions/clip | Source | Notes |
|:--------|:-----|:---------|:-------------|:-------|:------|
| **Clotho v2.1** ⭐ | 6,974 clips | 15–30s | 5 human | Freesound | [Zenodo 4783391](https://zenodo.org/records/4783391) · canonical eval set |
| **AudioCaps** | ~46k clips | 10s | 1 human | YouTube/AudioSet | [audiocaps.github.io](https://audiocaps.github.io/) · shorter, noisier |
| **MACS** | Small | — | Multiple | Urban soundscapes | Good for humanities framing |

> [!WARNING]
> Clotho v2.1 is at Zenodo record **4783391**, NOT 3490684 (that is v1). Prior drafts had this wrong. Using v1 will give you different splits and non-comparable numbers.

### Pre-training / scale datasets — NOT for final evaluation

| Dataset | Size | Notes |
|:--------|:-----|:------|
| **WavCaps** | ~400k clips | ChatGPT-assisted weakly-labeled |
| **AudioSetCaps** | ~6.1M clips | YouTube-scale |
| **Sound-VECaps** | Large | Visual-enriched captions |

### LALM benchmark datasets — for model capability evaluation beyond AAC

| Dataset | AF3 Score | What it measures |
|:--------|:----------|:----------------|
| **MMAU** [Sakshi et al. 2024](https://sakshi113.github.io/mmau_homepage/) | 72.28 | Massive Multi-task Audio Understanding — de facto LALM benchmark |
| **ClothoAQA** | 91.1% | QA over Clotho clips |
| **CMM-Hallucination** | 86.7% | Confabulation rate (lower is better hallucination, higher = better accuracy) |
| **Clotho-Entailment** | 92.9% | Logical entailment over audio–caption pairs |

### Humanities domain-shift bonus (RQ5)
- **Bamberg church-bell recordings** from T1 classmates (if shareable)
- **BBC Sound Effects Archive** (CC-BY-NC 4.0, educational use)
- **Europeana Sounds** — pan-European cultural heritage audio

### 4.1 Dataset Licence Heterogeneity

Clotho v2.1 is distributed under CC-BY 4.0 as a *collection*, but the individual FreeSound clips inside carry **per-clip licences** assigned by original uploaders — most CC-BY or CC0, a minority CC-BY-NC or CC-BY-SA. Drossos 2020 §3.2 `[L2; HIGH/HIGH]` notes the collection maintains compatibility with the most restrictive per-clip licence (CC-BY-NC) for derivative uses.

**Practical implications:**
1. **Research use (our project): no change.** Academic research is permitted under all per-clip licences present in Clotho.
2. **Derivative distribution: licence-audit required.** If the thesis or a future paper redistributes *transformed* clips (e.g., synthetic A-then-B mixes used in RQ4), the per-clip licences of the source clips must be checked individually; CC-BY-SA requires share-alike propagation.
3. **RQ4 synthesis caveat:** the 50 synthesised mixtures in `08_temporal_ordering.ipynb` must retain per-clip licence attribution in their metadata JSON. Drop clips whose source licences prohibit derivatives.

**Additional source audit:**
- AudioCaps → YouTube ToS (research-only; never redistribute raw audio)
- BBC Sound Effects → CC-BY-NC 4.0 (non-commercial; educational use permitted with attribution)
- Bamberg bells → T1-group consent; no public redistribution

---

## § 5. Metrics — The Complete 2026 Stack

> [!IMPORTANT]
> **SPIDEr-FL is the official headline metric** (DCASE 2024 Task 6). But reporting only SPIDEr-FL hides the hallucination problem. A strong paper reports at least one hallucination-specific measure alongside it.

### 5.1 Classical n-gram and structural metrics

| Metric | Measures | Status |
|:-------|:---------|:-------|
| BLEU-1..4 | N-gram precision | Quick sanity check only |
| METEOR | Alignment + synonyms + recall | Better than BLEU; handles paraphrase |
| ROUGE-L | Longest common subsequence | Captures sentence structure |
| CIDEr | TF-IDF-weighted n-gram consensus | Rewards discriminative dataset-specific terms |
| SPICE | Scene-graph overlap (objects/relations/attributes) | Best classical semantic metric |

### 5.2 Primary DCASE metric: SPIDEr-FL
```
SPIDEr    = (SPICE + CIDEr) / 2
SPIDEr-FL = SPIDEr × Fluency_Error_Penalty
```
The FL term penalises ungrammatical or looping captions. This is the headline number.  
**Implementation:** [`aac-metrics`](https://github.com/Labbeti/aac-metrics) (Labbeti) — requires Java 11+.  
**DCASE 2024 baseline:** 29.6% SPIDEr-FL on Clotho-eval.

### 5.3 Learned / embedding-based metrics (higher human correlation)

| Metric | Description |
|:-------|:------------|
| **BERTScore** | Contextual-embedding similarity; catches semantic paraphrase |
| **FENSE** (Zhou et al.) | Fluency- and Error-aware Sentence Embedding Score; designed specifically for AAC; highest reported correlation to human judgement. `pip install fense` |
| **CLAPScore** | Uses contrastive audio-language model to score caption *directly against the audio* (reference-free) — measures actual audio grounding, not just text similarity |

### 5.4 Hallucination-specific metrics

| Metric | Method |
|:-------|:-------|
| **CMM-Hallucination accuracy** | The AF3 benchmark measure |
| **CHAIR-style entity precision** | spaCy NER over caption → check AudioSet ontology membership → hallucination rate = ungrounded entities / total mentions |
| **Audio-grounding precision** | CLAPScore of individual entity mentions above a threshold |

### 5.5 Temporal grounding metrics (for RQ4)

| Metric | Source |
|:-------|:-------|
| **tIoU** | Temporal intersection-over-union between predicted and ground-truth event spans |
| **Onset/offset F1** | From TAC (arxiv 2602.15766) |

### 5.6 Reporting recommendation
**Minimum set:** SPIDEr-FL · METEOR · CIDEr · SPICE · FENSE · one hallucination measure.  
Report two measures capturing two different failure modes; do not just SPICE-cap one metric.

### 5.7 Metric Variance Envelope

For every metric reported in the thesis, we need a published variance estimate to interpret point scores responsibly.

| Metric | σ (typical on AAC tasks) | Source | Notes |
|:-------|:------------------------:|:-------|:------|
| SPIDEr-FL | ~12 pp across seeds / splits | Martin-Morato et al. 2024 `[L2; HIGH/MED]` | Drives MDE in lit-review §10 |
| FENSE | ~4 pp | Zhou 2022 Table 4 `[L2; HIGH/HIGH]` | Lower variance — learned metric |
| CLAPScore | ~0.03 (cosine) | Wu 2023 `[L2; HIGH/HIGH]` | Report to 3 decimals |
| CIDEr | ~8 pp | Mei 2022 §5 `[L2; HIGH/HIGH]` | Higher variance on short clips |
| BLEU-4 | ~3 pp | Papineni 2002 | Reported for historical comparison only |

**BCa bootstrap example** (RQ1 AF3 point score):
```
Observed SPIDEr-FL(AF3) = 35.2%
BCa 95% CI = [33.1%, 37.0%]  (n_resamples=1000, seed=42)
29.6% baseline: CI lower bound 33.1% > 29.6% → H1 supported
```
Every point score in the term paper is reported with this CI format. Plain percentile bootstrap is **not** used — under-coverage on skewed AAC-score distributions per Efron & Tibshirani 1993 ch. 14.

---

## § 6. Research Questions — Operationalised

The official T6 slide asks one question. Five tightly-scoped RQs that collectively answer it and exceed the rubric:

**RQ1 (PRIMARY — Frontier comparison):** On Clotho v2.1 eval split, does **Audio Flamingo 3** (zero-shot) outperform SALMONN (zero-shot) and the DCASE 2024 CNext-trans baseline (supervised) on SPIDEr-FL, FENSE, and CIDEr? *(Publishable contribution: no published comparison places AF3 head-to-head with CNext-trans on SPIDEr-FL on Clotho-eval.)*

**RQ2 (SECONDARY — Polyphony):** On a manually-curated polyphonic subset (≥2 concurrent event types, verified by ≥3-of-5 references mentioning ≥2 entity classes), is the AF3-minus-baseline SPIDEr-FL gap *larger* than on monophonic clips?

**RQ3 (SECONDARY — Hallucination):** On AudioCaps single-event clips (verified by AudioSet metadata), what is the entity hallucination rate of AF3 vs. SALMONN vs. baseline? Method: spaCy NER → AudioSet ontology resolution → CHAIR-style precision.

**RQ4 (OPTIONAL — Temporal ordering):** On synthetic *A-then-B* mixtures (5s gap), does AF3 or SALMONN correctly order events in the caption? Compare to TAC as oracle if weights release by May 18.

**RQ5 (OPTIONAL — Humanities, thesis-distinguishing):** Do LALMs generalise to culturally-grounded audio out-of-distribution from Freesound? Qualitative case study of ≤20 clips (Bamberg bells or BBC archive). This is the RQ that makes this project Computational Humanities, not MIR.

### 6.1 RQ Experiment-Design Matrix (Wohlin 2012 §6)

One row per RQ. Every cell is populated before Phase 2 begins — empty cells signal a design gap.

| RQ | Metric | Statistical test | Data source | n | MDE / power | Threats axis | Falsifier |
|:---|:-------|:-----------------|:------------|:-:|:------------|:-------------|:----------|
| RQ0 | contamination % | descriptive | FreeSound IDs cross-ref vs WavCaps + Clotho-AQA + AudioSetCaps | 1,045 | n/a | Construct (C4) | 0% overlap → null result |
| RQ1 | SPIDEr-FL | one-sided BCa (Holm-adj) | Clotho-eval CLEAN | ≤1,045 | 0.73 pp | Internal (I1), External (E1), Conclusion (V1,V2) | CI lower ≤ 29.6% |
| RQ2 | Δ SPIDEr-FL (poly−mono) | paired BCa (Holm-adj) | Clotho-eval subset | 100 | 1.04 pp | Construct (C3), Conclusion (V3) | Δ > −3.5 pp OR p ≥ 0.05 |
| RQ3 | CHAIR-audio rate | two-sample BCa | AudioCaps single-event | 500 | 1.5 pp | Construct (C2) | Rate(AF3) − rate(SALMONN) < 5 pp OR CIs overlap |
| RQ4 | correct-ordering rate | descriptive + BCa CI | Synthetic A-then-B | 50 | — | Construct (C3), External (E2) | Rate > 60% |
| RQ5 | CLAPScore | descriptive | Bamberg bells / BBC archive | ≤ 20 | — | Construct (C1), External (E1) | Δ < 0.05 vs in-dist baseline |
| **Neg-control** | CHAIR-audio rate | descriptive + BCa CI | Silence / white / pink / tones | 30 | — | Construct (C1) | Rate < 50% → weakening of §5.2 mechanism |

**Method sources.** MDE derivation (`MDE ≈ 2.8 × SE`, with `SE = σ / √n`) per Cohen 1988; see `literature_review.md` §10.2 for full derivation and σ table. BCa 95% CI construction per Efron & Tibshirani 1993, ch. 14 (seed=42, n=1000 resamples). Variance floors (σ≈12 pp SPIDEr-FL, ≈4 pp FENSE, ≈0.03 CLAPScore) per Martin-Morato 2024 as adopted in `literature_review.md` §10.1.

### 6.2 Null-Hypothesis Phrasings

Per-RQ H₀ statements (cross-ref to `hypotheses_preregistered.yml` and lit-review §11):
- **H₀(RQ0):** WavCaps ∩ Clotho-eval = ∅ (no contamination)
- **H₀(RQ1):** μ(SPIDEr-FL, AF3, Clotho-eval-CLEAN) ≤ 29.6%
- **H₀(RQ2):** μ(Δ SPIDEr-FL, poly) = μ(Δ SPIDEr-FL, mono)
- **H₀(RQ3):** μ(CHAIR-rate, AF3) = μ(CHAIR-rate, SALMONN)
- **H₀(RQ4):** P(correct-order \| mix) = 1.0
- **H₀(RQ5):** μ(CLAPScore, cultural) ≥ μ(CLAPScore, Clotho-eval sample)
- **H₀(Neg-control):** μ(hallucination-rate \| silence) < 50%

Rejection of H₀ uses BCa 95% CI (+Holm for the H1–H3 family).

---

## § 7. Reading Order with Confidence/Applicability Ratings

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

## § 8. Software Stack

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
- ⭐ Primary: [`nvidia/audio-flamingo-3`](https://huggingface.co/nvidia/audio-flamingo-3) — 8B params, ~20GB VRAM bf16 / ~10GB int4
- Secondary: [`tsinghua-ee/SALMONN`](https://huggingface.co/tsinghua-ee/SALMONN) — 13B, ~24GB bf16 / ~14GB int4
- Optional: [Qwen2.5-Omni](https://github.com/QwenLM/Qwen2.5-Omni)
- TAC: weights not yet released as of Apr 2026; monitor [sonalkum.github.io/tacmodel/](https://sonalkum.github.io/tacmodel/)

### § 8.1 Determinism Requirements (reproducibility pins)

Every run of the inference + scoring pipeline must set the following BEFORE model load. Implementation and assertion lives in `implementation_plan.md` Phase 1 (`environment.yml` + `setup_check.py`); this section documents them as a *requirement*, not as code.

| Pin | Value | Rationale |
|:----|:------|:----------|
| `PYTHONHASHSEED` | `42` | Dict/set iteration order stable across runs (Python built-in randomisation defeats BCa seeding otherwise). |
| `CUBLAS_WORKSPACE_CONFIG` | `:4096:8` | CUDA cuBLAS workspace fixed — required precondition for `torch.use_deterministic_algorithms(True)` on A100+. |
| `torch.use_deterministic_algorithms(True, warn_only=False)` | enforced | Hard-fails any non-deterministic kernel; pair with `torch.manual_seed(42)` + `numpy.random.seed(42)`. |
| GPU compute capability | **SM ≥ 8.0** (Ampere or newer) | Required for deterministic bf16 matmul on the AF3 / SALMONN stack; `setup_check.py` asserts this and exits otherwise. |
| BCa bootstrap seed | `42` (n = 1000 resamples) | Matches `hypotheses_preregistered.yml`; any drift invalidates pre-registration. |

These pins jointly ensure that re-running the pipeline on a fresh clone reproduces published SPIDEr-FL / FENSE / CLAPScore numbers bit-exactly on the canary check (DCASE 2024 baseline 29.6% ± 1%) — which is itself a Phase 2 gate.

---

## § 9. May-4 Talk Branching by RQ0 Outcome

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
- Scope pivot: project reframes around hallucination (RQ3) and temporal grounding (RQ4) — both of which are orthogonal to training-data leakage.
- RQ1 demoted to a descriptive benchmark comparison without the "zero-shot" label.

---

## § 10. Glossary for Humanities Examiners

A CH examiner will need these 20 terms. Definitions are written for a humanities MA but no ML background.

| Term | Definition |
|:-----|:-----------|
| **AAC** | Automated Audio Captioning — a ML task that outputs free-text descriptions of what a sound recording contains. |
| **AudioSet** | A 632-class hierarchical taxonomy of everyday sounds, developed by Google, with 2M+ labelled YouTube clips. |
| **bf16 / fp16** | Numeric precision formats for neural network computation; bf16 (16-bit brain-float) allows larger models to fit in GPU memory. |
| **BCa bootstrap** | Bias-Corrected-accelerated bootstrap: a statistical method for computing confidence intervals when data is skewed. |
| **BERTScore / FENSE** | Metrics that compare machine captions to human captions using learned sentence embeddings rather than word overlap. |
| **CLAP / CLAPScore** | Contrastive Language-Audio Pretraining; produces a similarity score between an audio clip and a text description without needing human reference captions. |
| **CHAIR** | A hallucination metric originally for image captioning: counts entities mentioned that are not actually present. |
| **Clotho / Clotho-eval** | A benchmark AAC dataset; *Clotho-eval* is the 1,045-clip evaluation split at Zenodo record 4783391. |
| **DCASE** | Detection and Classification of Acoustic Scenes and Events — an annual challenge; Task 6 is audio captioning. |
| **FreeSound** | A large community-curated sound repository (freesound.org); the upstream source for Clotho. |
| **Holm-Bonferroni** | A statistical correction applied when multiple hypotheses are tested to prevent false positives. |
| **Hypothesis pre-registration** | Committing a hypothesis in writing (with git SHA) before running the experiment — anti-cheating against the HARKing fallacy. |
| **LALM** | Large Audio-Language Model; a LLM augmented with an audio encoder so it can "hear." |
| **LLM / decoder** | Large Language Model; the text-generating component that produces the caption. |
| **MDE** | Minimum Detectable Effect — the smallest true difference a statistical test can reliably detect given sample size and variance. |
| **Polyphony** | Multiple sound events occurring simultaneously in the same clip. |
| **Q-Former** | "Querying-transformer"; a small neural module that compresses audio features into a fixed number of tokens the LLM can consume. |
| **SPIDEr-FL** | The official DCASE 2024 AAC metric — a combination of SPICE and CIDEr, further multiplied by a fluency penalty. |
| **Zero-shot** | The model produces captions for a dataset it was never explicitly trained on for the captioning task. |
| **κ (Cohen's kappa)** | An inter-annotator agreement statistic correcting for chance; ≥ 0.6 is "substantial" agreement. |

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
