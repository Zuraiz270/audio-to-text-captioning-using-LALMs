# Literature Review (EBSE-Compliant) — T6: Audio-to-Text Captioning using LALMs
*Master's Project · CH-Proj-M · SS 2026 · Zuraiz (2177213)*
*Prof. Dr.-Ing. Jakob Abeßer · Computational Humanities · Uni Bamberg*

> **EBSE Protocol:** Every empirical claim carries an inline evidence badge: `[Author Year; Lx; CONF/APPLIC]` where Lx = source level (L1=official dataset/benchmark, L2=peer-reviewed, L3=preprint), CONF = confidence in evidence quality (HIGH / MED), APPLIC = applicability to this project (HIGH / MED / LOW). Staleness flagged per §3.2 (>10yr = `[STALE-VALID]` with justification). Zero unverified claims.

---

## § 1. Task Definition: What AAC Is and Is Not

### 1.1 Formal Task Boundary

Automated Audio Captioning (AAC) was formally defined as a distinct task by Drossos, Lipping, and Virtanen `[Drossos 2020; L2; HIGH/HIGH]` as *inter-modal translation*: a raw audio waveform as input, a free-text natural-language description as output.

| Task | Input | Output | Captures |
|:-----|:------|:-------|:---------|
| **Audio Tagging** | Waveform | Label set `{dog, traffic, rain}` | Identities only — no relation, order, texture |
| **ASR** | Waveform (speech) | Word transcript | Speech channel only — non-speech ignored |
| **AAC (this project)** | Any waveform | Free-text description | Identities + relations + texture + temporal order |

The linguistic surplus of AAC over Audio Tagging is not cosmetic. The tag set `{dog, traffic, wind}` carries zero information about whether the dog is near or far, whether the traffic is wet or dry, whether the wind precedes or follows. The caption *"A dog barks in the distance as cars pass on a wet road while wind rustles nearby leaves"* encodes spatial distance, surface texture, temporal concurrence, and acoustic texture. None of these can be recovered from the tag set. This is the *information gap* that makes AAC a distinct and harder problem `[Drossos 2020; L2; HIGH/HIGH]`.

### 1.2 Humanities Framing: Ekphrasis and Soundscape Studies

**Why this belongs in Computational Humanities, not MIR.** The humanistic lineage runs through two traditions that converge on this project.

**Ekphrasis** — the classical rhetorical genre of verbal description of non-verbal aesthetic experience — is most often associated with visual art (Homer's shield of Achilles, *Iliad* 18.478–608 `[STALE-VALID: foundational literary example]`; Heffernan 1993 `[Heffernan 1993; L2; HIGH/HIGH]`). AAC is the computational instantiation of ekphrasis for acoustic objects: a machine that produces verbal descriptions of acoustic experiences that resist direct verbal expression. The theoretical claim is that the same semiotic gap that makes visual ekphrasis interesting — the translation between sign systems — operates in the acoustic domain with additional difficulty, because acoustic experience is transient and lacks the stable spatial anchor of visual art.

**Soundscape Studies** was inaugurated by R. Murray Schafer's *The Tuning of the World* (1977) `[Schafer 1977; L2; HIGH/HIGH — STALE-VALID: 49yr but no replacement exists]`. Schafer defined three acoustic categories with direct implications for what an AAC system must describe:

| Schafer Category | Definition | AAC Implication |
|:-----------------|:-----------|:----------------|
| **Keynote sound** | Background tone defining an acoustic environment (e.g., city hum, ocean) | Must be described even when it carries low event salience |
| **Soundmark** | Community-specific sound of cultural identity (e.g., Bamberg Martinskirche bells) | Primary target of RQ5; likely OOD for Freesound-trained models |
| **Sound signal** | Foreground sound demanding active attention (e.g., alarm, horn) | High-salience; most reliably described by current LALMs |

A LALM trained on FreeSound and AudioSet will have strong priors for sound signals and moderate priors for keynote sounds. Soundmarks — culturally-specific, geographically-anchored, institutionally-singular sounds — are structurally absent from web-scraped training corpora. This is the mechanism behind RQ5's domain-shift hypothesis.

**Digital archives use case.** DARIAH-EU's Strategic Plan (2023) `[DARIAH 2023; L1; HIGH/HIGH]` identifies automated captioning of audio-visual cultural heritage as a priority capability. The British Library Sound Archive (>6.5M recordings) and BBC Sound Effects Archive (>33,000 CC-licensed clips) have no systematic free-text caption layer — a structural accessibility failure for blind and low-vision users and for semantic search.

#### § 1 Evidence Trail

| # | Source | Level | Year | Conf | Applic | Status |
|:-:|:-------|:------|:----:|:----:|:------:|:------:|
| 1 | Drossos et al. — Clotho (ICASSP 2020) | L2 | 2020 | HIGH | HIGH | ACCEPTED |
| 2 | Gemmeke et al. — AudioSet (ICASSP 2017) | L2 | 2017 | HIGH | HIGH | ACCEPTED |
| 3 | Heffernan — Museum of Words (1993) | L2 | 1993 | HIGH | HIGH | STALE-VALID |
| 4 | Schafer — Tuning of the World (1977) | L2 | 1977 | HIGH | HIGH | STALE-VALID |
| 5 | DARIAH-EU Strategic Plan (2023) | L1 | 2023 | HIGH | HIGH | ACCEPTED |

---

## § 2. Evaluation Datasets: Hierarchy and Misuse Risks

A systematic error in the AAC literature is treating all audio-caption datasets as interchangeable. They are not.

### 2.1 Tier 1 — Primary Evaluation (Clotho v2.1)

Clotho v2.1 `[Drossos 2020; L2; HIGH/HIGH]` is the canonical evaluation benchmark. Three design decisions make it superior to alternatives:

1. **Five captions per clip**: five independent human annotations enable consensus-based metric computation. With one reference, metric variance is dominated by annotator idiosyncrasy `[Zhou 2022; L2; HIGH/HIGH]`.
2. **15–30 second duration**: longer than AudioCaps (10s), providing richer temporal structure and polyphony opportunities.
3. **Acoustic focus annotation protocol**: annotators instructed to describe *what they hear*, eliminating visual inference bias.

> [!WARNING]
> **Critical versioning error.** Clotho v2.1 is at Zenodo record **4783391**. Record **3490684** is v1 with different splits. Any SPIDEr-FL number computed on v1 is not comparable to DCASE 2024's 29.6% floor `[Labbeti 2024; L1; HIGH/HIGH]`.

| Split | Clips | Purpose |
|:------|:-----:|:--------|
| Development | 3,839 | Pre-processing sanity checks |
| Validation | 1,045 | Development-time model selection |
| **Evaluation ⭐** | **1,045** | **Final metric reporting — RQ1, RQ2, RQ3** |
| Test | 1,045 | Withheld; not used in this project |

### 2.2 Tier 2 — Auxiliary Experiment (AudioCaps)

AudioCaps `[Kim 2019; L2; HIGH/HIGH]` provides ~46,000 YouTube-derived clips with one caption each. **Not** used for primary metric reporting (single reference makes metrics unreliable). Its role:

- **RQ3 (hallucination)**: AudioSet metadata provides ground-truth tags per clip, enabling the CHAIR-audio protocol. Single-event clips (AudioSet tag count = 1) are the stimulus set.
- AudioSet's 632-class ontology `[Gemmeke 2017; L2; HIGH/HIGH]` is the vocabulary for cross-referencing extracted nouns against ground truth.

### 2.3 Tier 3 — Pre-training Corpora (NEVER Evaluation)

> [!CAUTION]
> These datasets are cited for contamination audit (RQ0) and context only. They must never be used as evaluation sets.

| Dataset | Size | Source | Role in This Project |
|:--------|:----:|:-------|:---------------------|
| WavCaps `[Mei 2023; L3; HIGH/HIGH]` | ~400k | FreeSound + YouTube + BBC | RQ0: contamination audit manifest |
| AudioSetCaps | ~6.1M | YouTube / AudioSet | RQ0: contamination audit manifest |
| Clotho-AQA `[Lipping 2022; L2; HIGH/HIGH]` | ~7k | Clotho | RQ0: highest-risk contamination source |

**The contamination risk is structural, not hypothetical.** AudioSetCaps and WavCaps both derive from the same upstream repositories (FreeSound, AudioSet) as Clotho v2.1. AF3's training data card `[Ghosh 2025b; L3; HIGH/HIGH]` must be cross-referenced before RQ1 results can be characterised as "zero-shot."

#### § 2 Evidence Trail

| # | Source | Level | Year | Conf | Applic | Status |
|:-:|:-------|:------|:----:|:----:|:------:|:------:|
| 1 | Drossos et al. — Clotho v2.1, Zenodo 4783391 | L1 | 2021 | HIGH | HIGH | FLOOR DATASET |
| 2 | Kim et al. — AudioCaps (NAACL 2019) | L2 | 2019 | HIGH | HIGH | AUX (RQ3 only) |
| 3 | Gemmeke et al. — AudioSet (ICASSP 2017) | L2 | 2017 | HIGH | HIGH | ONTOLOGY |
| 4 | Labbeti 2024 — DCASE baseline | L1 | 2024 | HIGH | HIGH | FLOOR |

---

## § 3. Traditional AAC: The Pre-LALM Paradigm

### 3.1 Canonical Architecture

Mei, Liu, Plumbley, and Wang (2022) `[Mei 2022; L2; HIGH/HIGH]` survey 50+ papers and identify convergence on a single architectural template by 2021:

```
log-mel spectrogram
      ↓
[ CNN Audio Encoder ]   ← CNN14/PANNs [Kong 2020; L2; HIGH/HIGH]
      ↓                    ResNet, VGGNet, PaSST, AST
[ Temporal Pooling ]
      ↓
[ Sequence Decoder ]    ← BART, GPT-2, Transformer LM
      ↓
[ Caption ]
```

### 3.2 The Comparison Floor: DCASE 2024 CNext-trans

The DCASE 2024 Task 6 baseline `[Labbeti 2024; L1; HIGH/HIGH]`:

- **Encoder**: ConvNeXt pretrained for audio classification
- **Decoder**: Transformer seq2seq with cross-attention
- **Training**: Fully supervised on Clotho; no LLM, no foundation model
- **Result**: **29.6% SPIDEr-FL on Clotho-eval**

This is the supervised baseline that a zero-shot LALM must exceed to justify the thesis claim.

**Hypothesised root cause of the ceiling.** The encoder-decoder model has no dedicated mechanism for polyphonic event segregation. If two events co-occur at frame *t*, their mel-spectrogram representations superimpose. The single encoder embedding plausibly contains entangled information from both events; the decoder generates text for the dominant event; the secondary event is suppressed. Mei (2022) names polyphony as the dominant *open* problem, not as proven architecturally impossible — single-stream encoding without an explicit separation head **is hypothesised to be unable** to represent concurrent events independently at the adapter layer `[Mei 2022; L2; HIGH/HIGH — open-problem framing]`. This project's RQ2 tests whether the same hypothesised limitation persists in AF3's unified-encoder design.

#### § 3 Evidence Trail

| # | Source | Level | Year | Conf | Applic | Status |
|:-:|:-------|:------|:----:|:----:|:------:|:------:|
| 1 | Mei et al. — AAC Survey (EURASIP 2022) | L2 | 2022 | HIGH | HIGH | ACCEPTED |
| 2 | Labbeti — DCASE 2024 T6 Baseline | L1 | 2024 | HIGH | HIGH | **FLOOR** |
| 3 | Kong et al. — PANNs (IEEE TASLP 2020) | L2 | 2020 | HIGH | HIGH | ACCEPTED |

---

## § 4. The LALM Revolution: Architecture, Scale, and Zero-Shot AAC

### 4.1 The Architectural Shift

All LALMs share one blueprint:

```
Waveform → [ Audio Encoder ] → [ Adapter / Q-Former ] → [ LLM Decoder ] → Caption/Answer
               (pretrained,         (lightweight,            (frozen or
                frozen)              bridge module)            LoRA-tuned)
```

Neither the audio encoder nor the LLM was trained for captioning. The adapter bridges representation spaces, enabling emergent zero-shot captioning.

### 4.2 SALMONN — Founding LALM (ICLR 2024)

Tang et al. (2023) `[Tang 2023; L2; HIGH/HIGH]` introduced SALMONN with a **dual audio encoder**:

```
Waveform ──→ [ Whisper-Large-v2 ] ─────┐
             (680k hrs speech)          ├──→ [ Q-Former ] ──→ [ Vicuna-13B ]
Waveform ──→ [ BEATs ]           ─────┘
             (AudioSet events)
```

**Rationale for dual encoding:** Whisper is biased toward speech phonetics; BEATs captures environmental events. The dual design hedges against the domain incompleteness of either encoder.

**Why this matters for RQ2:** SALMONN's dual encoder was designed to separate speech from events — but RQ2 tests *within-domain concurrent events* (two environmental sounds co-occurring). If dual encoding fails here, it means the polyphony problem cannot be solved by encoder specialisation along the speech/environment axis.

**Parameters:** 13B total; ~24GB bf16 / ~14GB int4 `[Tang 2023; L2; HIGH/HIGH]`.

### 4.3 Audio Flamingo 3 — Current SOTA (July 2025)

Goel, Ghosh et al. (2025) `[Goel 2025 / "Ghosh 2025b" project key; L3; HIGH/MED]` present AF3, superseding all prior open and closed LALMs:

| Benchmark | AF3 | Qwen2.5-Omni | GPT-4o-audio |
|:----------|:----|:-------------|:-------------|
| MMAU `[Sakshi 2024; L2; HIGH/HIGH]` | **72.42** †‡ | ~70 | ~70 |
| ClothoAQA | **91.1%** † | — | — |
| CMM-Hallucination | **86.7%** † | — | — |
| Clotho-Entailment | **92.9%** † | — | — |

† Author-reported on the AF3 arXiv preprint (2507.08128, July 2025); not independently replicated as of April 2026.
‡ Earlier internal project drafts cited 72.28 — the verified value is **72.42** (from the AF3 paper body / results tables; the abstract does not state a specific MMAU number; per Phase 1 web-fetch verification, April 2026). Use 72.42 in all new prose.

**Citation note (co-first authors).** The project key `Ghosh 2025b` is retained for backward compatibility with `paper_summaries.md` cards and existing references. The co-first authors are **Arushi Goel★** and **Sreyan Ghosh★** (NVIDIA; ★ = equal contribution, alphabetical order per NVIDIA project page). The wiki source card `wiki/08_sources/goel-2025-af3.md` is authoritative on attribution.

**Confidence/applicability adjusted to HIGH/MED** (was HIGH/HIGH) because: (1) the data card is not yet confirmed to enumerate all training corpora (Q1 in `research_notes.md` remains OPEN); (2) "zero-shot" applicability to Clotho-eval is a claim RQ0 tests, not a premise. Confidence remains HIGH because the institution is NVIDIA, benchmark code is public, and no conflicting independent replication exists as of April 2026.

**Architectural key difference:** AF3 replaces the dual-encoder design with a **unified AF-Whisper encoder** (successor to AF-CLAP from AF2) — a single model trained contrastively on a massive mixed corpus. The dual-encoder hedge is abandoned in favour of *scale and data diversity*. This is the central architectural argument: AF3's success demonstrates that a sufficiently large single encoder trained on sufficiently diverse data renders architectural specialisation unnecessary.

**Parameters:** 8B; ~20GB VRAM bf16 / ~10GB int4 `[Ghosh 2025b; L3; HIGH/HIGH]`.

### 4.4 Qwen2.5-Omni — End-to-End Multimodal (March 2025)

Qwen Team (2025) `[Qwen 2025; L3; HIGH/HIGH]` present an end-to-end model integrating text, audio, image, and video. Serves as optional third data point (Cut 1 in the project scope). **Licence:** Apache-2.0 — lowest legal risk.

#### § 4 Evidence Trail

| # | Source | Level | Year | Conf | Applic | Status |
|:-:|:-------|:------|:----:|:----:|:------:|:------:|
| 1 | Tang et al. — SALMONN (ICLR 2024) | L2 | 2023 | HIGH | MED | BASELINE |
| 2 | Radford et al. — Whisper (ICML 2023) | L2 | 2023 | HIGH | HIGH | ACCEPTED |
| 3 | Chen et al. — BEATs (ICML 2023) | L2 | 2023 | HIGH | HIGH | ACCEPTED |
| 4 | Ghosh et al. — AF2 (arxiv 2503.03983) | L3 | 2025 | HIGH | HIGH | ACCEPTED |
| 5 | **Ghosh et al. — AF3 (arxiv 2507.08128)** | L3 | 2025 | HIGH | HIGH | **PRIMARY SOTA** |
| 6 | Qwen Team — Qwen2.5-Omni (arxiv 2503.20215) | L3 | 2025 | HIGH | HIGH | ACCEPTED |
| 7 | Sakshi et al. — MMAU (arxiv 2410.19168) | L2 | 2024 | HIGH | HIGH | BENCHMARK REF |

**Conflict:** SALMONN is L2; AF3 is L3. Resolution: recency rule — AF3 demonstrably supersedes SALMONN on all benchmarks. Decision disclosed.

---

## § 5. Root Cause Analysis of Three Failure Modes

The three failure modes are not independent bugs. They share a root cause.

### 5.1 Failure Mode 1: Polyphony Under-Description

**Observation:** AAC models systematically omit secondary concurrent acoustic events `[Mei 2022; L2; HIGH/HIGH]`.

**RCA:**
```
Input:    [bark @ 0–3s] + [traffic @ 1–5s]          ← Two concurrent sources
Encoder:  One embedding per frame; frame at t=1.5s encodes bark+traffic entangled
Q-Former: Compresses encoder output to N query tokens; entangled representation persists
LLM:      Text prior favours mentioning louder source
Output:   "A dog barks in the distance."             ← Traffic silently dropped
```

The hypothesised bottleneck is at the **Q-Former**: it compresses multiple entangled concurrent-event embeddings into fixed query tokens, so information about the quieter event is plausibly lost — and no LLM capacity can recover information never transmitted through the adapter `[Ghosh 2025b; L3; HIGH/MED — author-acknowledged open challenge, not author-proven impossibility]`.

> **Independent 2026 corroboration (Phase 1 finding, April 2026).** PolyBench (Mar 2026, arXiv 2603.05128; submitted to INTERSPEECH 2026) introduces a five-subset polyphonic-audio benchmark (counting, classification, detection, concurrency, duration estimation) and reports that state-of-the-art LALMs exhibit "consistent performance degradation in polyphonic audio, indicating a fundamental bottleneck" (abstract). Whether AF3 is among the evaluated models and whether the bottleneck is specifically at the encoder-to-LLM interface requires verification from the full paper body (deferred to Phase 1 ingest of PDF). PolyBench is L3 (preprint) and post-dates AF3, so it cannot replace RQ2 — but it independently reproduces the polyphonic-degradation pattern outside this project's evaluation, strengthening the *motivation* for RQ2 even before any in-project measurement is run. The dedicated wiki source card is `wiki/08_sources/polybench-2026.md`.

### 5.2 Failure Mode 2: Entity Hallucination

**Observation:** LALMs mention sound entities not present in the audio `[Kuan 2024; L2; HIGH/HIGH]`.

**RCA:** The LLM decoder's text prior fills generation gaps when the audio encoder provides ambiguous or low-signal embeddings. Certain concepts co-occur with high frequency in training text (*park → dog → children → birds → traffic*); under an under-constrained audio representation, the LLM completes with its most probable continuation.

**Link to Failure Mode 1:** The information bottleneck *causes* hallucination. When the adapter fails to transmit full acoustic information, the LLM compensates with its text prior. Kuan et al. (2024) `[L2; HIGH/HIGH]` confirm: hallucination rate increases for sounds with high text-prior co-occurrence and is lowest for unexpected sounds.

**Quantified baseline:** AF3 reports 86.7% accuracy on CMM-Hallucination `[Ghosh 2025b; L3; HIGH/HIGH]`, meaning 13.3% hallucinated on a controlled benchmark. On uncontrolled Clotho clips, this is expected to be higher.

### 5.3 Failure Mode 3: Temporal Grounding Loss

**Observation:** LALMs describe events in canonical text-prior order rather than actual onset order `[Kumar 2026; L3; HIGH/HIGH]`.

**RCA:** Autoregressive LLM decoding generates tokens left-to-right with strong ordering priors from training text. When actual onset order deviates from canonical order, the text prior overrides audio evidence.

TAC (Kumar et al., 2026) `[L3; HIGH/HIGH]` demonstrate this with synthetic A-then-B mixtures: event A starts before B but B is louder → LALMs describe B before A. TAC's fix — a **separate temporal grounding head** — bypasses autoregressive ordering bias entirely.

### The Unified Root Cause

> *Information compression in the adapter (Q-Former) destroys concurrent-event separation → LLM operates under-constrained → text prior fills the gap → wrong entities mentioned (hallucination) → wrong events omitted (polyphony) → wrong temporal order (grounding loss). All three are symptoms of one architectural failure: the information bottleneck between encoder and decoder, with no mechanism for concurrent-event segregation at the adapter layer.*

This unified root cause is the central claim of the Discussion chapter.

#### § 5 Evidence Trail

| # | Source | Level | Year | Conf | Applic | Status |
|:-:|:-------|:------|:----:|:----:|:------:|:------:|
| 1 | Mei et al. — AAC Survey (EURASIP 2022) | L2 | 2022 | HIGH | HIGH | ACCEPTED |
| 2 | Kuan et al. — LALM Limits (Interspeech 2024) | L2 | 2024 | HIGH | HIGH | ACCEPTED |
| 3 | Ghosh et al. — AF3 (arxiv 2507.08128) | L3 | 2025 | HIGH | HIGH | ACCEPTED |
| 4 | Kumar et al. — TAC (arxiv 2602.15766) | L3 | 2026 | HIGH | HIGH | ACCEPTED |
| 5 | Rohrbach et al. — CHAIR (EMNLP 2018) | L2 | 2018 | HIGH | MED | ACCEPTED |

**Applicability note on Rohrbach 2018 (MED):** CHAIR was designed for image captioning. Audio adaptation requires replacing image object lists with AudioSet tags and adding the CLAPScore dual criterion. Adaptation disclosed in methodology.

---

## § 6. Evaluation Metrics: Protocol and Validity Claims

### 6.1 N-gram Metrics: Historical Context Only

BLEU `[Papineni 2002; L2; HIGH/HIGH — STALE-VALID]`, METEOR `[Banerjee 2005; L2; HIGH/HIGH — STALE-VALID]`, ROUGE-L `[Lin 2004; L2; HIGH/HIGH — STALE-VALID]` are reported for comparison with prior literature only. Zhou et al. (2022) `[Zhou 2022; L2; HIGH/HIGH]` demonstrate these metrics show significantly lower human-correlation for audio captions than FENSE.

### 6.2 CIDEr and SPICE: Stronger but Domain-Borrowed

CIDEr `[Vedantam 2015; L2; HIGH/HIGH — STALE-VALID: 11yr]` and SPICE `[Anderson 2016; L2; HIGH/HIGH — STALE-VALID: 10yr]` were designed for image captioning and transferred to audio without domain validation.

> **STALE-VALID justification:** Retained only as components of SPIDEr-FL, the official DCASE 2024 scoring function `[Labbeti 2024; L1; HIGH/HIGH]`. No newer domain-validated replacement has been published; any move away from CIDEr/SPICE would break comparability with every SPIDEr-FL number in the prior literature.

### 6.3 SPIDEr-FL: The Official Standard

`SPIDEr = (SPICE + CIDEr) / 2` · `SPIDEr-FL = SPIDEr × Fluency_Error_Penalty` `[Labbeti 2024; L1; HIGH/HIGH]`

The Fluency penalty penalises degenerate LLM outputs (repetition loops, truncated sentences). Implementation: `aac-metrics` `[Labbeti 2024; L1; HIGH/HIGH]` — the only valid implementation for DCASE-comparable numbers. Requires Java 11+. DCASE 2024 baseline: **29.6%**.

### 6.4 FENSE: Highest Human-Correlation Metric

Zhou et al. (2022) `[Zhou 2022; L2; HIGH/HIGH]` combine SentenceBERT similarity with a fluency error penalty. FENSE achieved the highest human-correlation coefficient among all tested metrics. The `aac-metrics` maintainer recommends SPIDEr + FENSE as the **primary metric pair**.

**Limitation:** FENSE requires human references. For RQ5 (Bamberg bells / BBC archive), no references exist — FENSE is undefined there.

### 6.5 CLAPScore: The Only Reference-Free Option

Wu et al. (2023) `[Wu 2023; L2; HIGH/HIGH]` present LAION-CLAP. `CLAPScore(caption, audio) = cosine_similarity(CLAP_audio(audio), CLAP_text(caption))` — no human references required.

**Non-negotiable for RQ5:** The Bamberg bells and BBC clips have zero human captions. SPIDEr-FL, FENSE, and BERTScore are literally undefined. CLAPScore is the only metric that can produce a number.

**Known limitation:** LAION-CLAP may not represent archival Germanic soundscape audio in its embedding space. Disclosed in methodology; motivation for RQ5's qualitative component.

### 6.6 CHAIR-Audio: Hallucination Measurement

Rohrbach et al. (2018) `[Rohrbach 2018; L2; HIGH/MED]` defined CHAIR for image captioning. This project adapts it with a **dual criterion**:

```
entity is "hallucinated" iff
  (a) entity ∉ ground-truth AudioSet tag set   [label-based]
  AND
  (b) CLAPScore(entity, audio) < 0.25          [audio-grounded]
```

The dual criterion prevents false-positive hallucination counts for audible events that AudioSet annotators missed (AudioSet tagging is known to be incomplete).

#### § 6 Evidence Trail

| # | Source | Level | Year | Conf | Applic | Status |
|:-:|:-------|:------|:----:|:----:|:------:|:------:|
| 1 | Labbeti — DCASE 2024 + aac-metrics | L1 | 2024 | HIGH | HIGH | TOOL + FLOOR |
| 2 | Zhou et al. — FENSE (ICASSP 2022) | L2 | 2022 | HIGH | HIGH | PRIMARY METRIC |
| 3 | Wu et al. — LAION-CLAP (ICASSP 2023) | L2 | 2023 | HIGH | HIGH | RQ5 MANDATORY |
| 4 | Rohrbach et al. — CHAIR (EMNLP 2018) | L2 | 2018 | HIGH | MED | ADAPTED |
| 5 | Papineni et al. — BLEU (ACL 2002) | L2 | 2002 | HIGH | HIGH | STALE-VALID |
| 6 | Vedantam et al. — CIDEr (CVPR 2015) | L2 | 2015 | HIGH | MED | STALE-VALID |
| 7 | Anderson et al. — SPICE (ECCV 2016) | L2 | 2016 | HIGH | MED | STALE-VALID |

**Metric reporting minimum:** `SPIDEr-FL · CIDEr · SPICE · FENSE · CLAPScore · CHAIR-audio`

---

## § 7. Research Gap Matrix — Proving Originality

Every RQ maps to a cell in the published literature that is **empty**.

| Measurement | AF3 paper | SALMONN paper | DCASE 2024 | Kuan 2024 | TAC 2026 | **This project** |
|:------------|:---------:|:-------------:|:----------:|:---------:|:--------:|:----------------:|
| SPIDEr-FL, AF3 zero-shot vs DCASE supervised, Clotho-eval | ❌ | ❌ | ❌ | ❌ | ❌ | **✅ RQ1** |
| Contamination audit AF3 + SALMONN vs Clotho-eval | ❌ | ❌ | ❌ | ❌ | ❌ | **✅ RQ0** |
| Polyphony-specific Δ(LALM − baseline) SPIDEr-FL, Clotho | ❌ | ❌ | ❌ | ❌ | ❌ | **✅ RQ2** |
| CHAIR-audio hallucination rate, AF3 vs SALMONN, AudioCaps | ❌ | ❌ | ❌ | partial | ❌ | **✅ RQ3** |
| Temporal A-then-B ordering rate, AF3 vs SALMONN | ❌ | ❌ | ❌ | ❌ | ✅ (TAC only) | **✅ RQ4** |
| CLAPScore-only eval, LALM on cultural-heritage audio, Schafer framing | ❌ | ❌ | ❌ | ❌ | ❌ | **✅ RQ5** |

> [!IMPORTANT]
> "RQ3 partial" for Kuan 2024 means they measured hallucination qualitatively on a different stimulus set without the CHAIR-audio dual CLAPScore criterion. The quantitative CHAIR-audio measurement on AF3 specifically is still an empty cell.

**Originality claim is falsifiable:** if any cell turns out to be pre-occupied by a paper missed at review time, that RQ must be repositioned.

#### § 7 Evidence Trail

| # | Source | Level | Year | Conf | Applic | Status |
|:-:|:-------|:------|:----:|:----:|:------:|:------:|
| 1 | Mei et al. — AAC Survey (2022) | L2 | 2022 | HIGH | HIGH | ACCEPTED |
| 2 | Ghosh et al. — AF3 (2025) | L3 | 2025 | HIGH | HIGH | ACCEPTED |
| 3 | Kumar et al. — TAC (2026) | L3 | 2026 | HIGH | HIGH | ACCEPTED |
| 4 | Kuan et al. — LALM Limits (2024) | L2 | 2024 | HIGH | HIGH | ACCEPTED |

---

## § 8. Intellectual Lineage Diagram

```
1977  Schafer — Soundscape theory (keynote/soundmark/signal)
                        │ humanities framing for RQ5
2017  AudioSet — 632-class ontology → hallucination vocabulary for RQ3
2019  AudioCaps — scale dataset → RQ3 stimulus set
2020  Clotho v2.1 — 5-caption benchmark → primary evaluation for RQ1/RQ2
2020  PANNs/CNN14 — audio classification encoder (encoder-decoder era)
      │
2022  Mei et al. survey — encoder-decoder paradigm documented; polyphony named
2022  FENSE — AAC-specific learned metric; correlates with human judgement
2022  SPIDEr-FL — DCASE 2024 standard metric
      │
2023  SALMONN — first generic LALM; dual encoder; zero-shot captioning
2023  LAION-CLAP — contrastive audio-language; enables CLAPScore (RQ5)
      │
2024  DCASE CNext-trans — 29.6% SPIDEr-FL; supervised floor (RQ1)
2024  Kuan et al. — hallucination in LALMs; text-prior mechanism
2024  MMAU — LALM benchmark standard
      │
2025  AF2 — AF-CLAP unified encoder introduced
2025  AF3 ⭐ — AF-Whisper (successor to AF-CLAP); SOTA; unified scale beats dual-encoder; RQ1/RQ2/RQ3 primary
2025  Qwen2.5-Omni — end-to-end; optional ablation
      │
2026  TAC — temporal grounding head; architectural argument against LLM decoder
      │
HERE  RQ0–RQ5: six empty cells filled
```

Every dated node is cited in §§ 1–7; this diagram is a narrative index.

---

## § 9. Threats to Validity (Wohlin 2012 Four-Axis Taxonomy)

Each threat is named, operationalised, and mitigated in advance `[Wohlin 2012; L2; HIGH/HIGH]`.

### 9.1 Construct Validity

| ID | Threat | Mitigation |
|:--|:-------|:-----------|
| C1 | SPIDEr-FL is a proxy for caption quality, not quality itself | Report FENSE + CLAPScore alongside; triangulate `[Zhou 2022; L2; HIGH/HIGH]` |
| C2 | Polyphony operationalised via annotator tag count may not reflect perceptual polyphony | Cross-validate with CLAP-embedding similarity `[Wu 2023; L2; HIGH/HIGH]` |
| C3 | CHAIR-audio 0.25 CLAPScore threshold is a free parameter | Pre-register 0.25; sensitivity analysis at 0.20 and 0.30 `[Rohrbach 2018; L2; HIGH/MED]` |
| C4 | "Zero-shot" rests on RQ0 contamination audit, not a verifiable property | If RQ0 returns non-zero overlap, demote all "zero-shot" claims |

### 9.2 Internal Validity

| ID | Threat | Mitigation |
|:--|:-------|:-----------|
| I1 | Default decoding temperature differs across models → confounds comparison | Fix `temperature=0.0` (greedy) across all models |
| I2 | Non-deterministic GPU ops → non-replayable bootstrap CIs | `PYTHONHASHSEED=42`, `CUBLAS_WORKSPACE_CONFIG=:4096:8`, `torch.use_deterministic_algorithms(True)` |
| I3 | bf16 silent fp32 fallback on sub-Ampere GPUs | SM ≥ 8.0 hard gate in `setup_check.py` |
| I4 | Prompt engineering drift across experiments | Single canonical prompt template per notebook, pinned in `prompts/` |

### 9.3 External Validity

| ID | Threat | Mitigation |
|:--|:-------|:-----------|
| E1 | Clotho-eval is a FreeSound convenience sample; generalisation to cultural heritage unestablished | RQ5 tests exactly this; framed as OOD probe, not mean-performance estimate |
| E2 | Results specific to `transformers 4.44.*` + AF3 checkpoint at pull time | Pin checkpoint SHA in `environment.yml`; archive model card |
| E3 | n ≤ 20 for RQ5 → no external-validity claim possible | RQ5 pre-registered as `[DESCRIPTIVE_ONLY]` |

### 9.4 Conclusion Validity

| ID | Threat | Mitigation |
|:--|:-------|:-----------|
| V1 | Five simultaneous hypotheses at α=0.05 inflates FWER to ≈0.23 | Holm-Bonferroni correction `[Holm 1979; L2; HIGH/HIGH]` |
| V2 | Percentile bootstrap under-covers on skewed AAC-score distributions | BCa bootstrap, n=1000, seed=42 `[Efron & Tibshirani 1993; L2; HIGH/HIGH]` |
| V3 | Low power at small RQ4/RQ5 sample sizes → false negatives as null | Pre-declared MDE per RQ; non-significant results reported as "underpowered", not "null" |

#### § 9 Evidence Trail

| # | Source | Level | Year | Conf | Applic | Status |
|:-:|:-------|:------|:----:|:----:|:------:|:------:|
| 1 | Wohlin et al. — *Experimentation in SE* ch. 8 | L2 | 2012 | HIGH | HIGH | ACCEPTED |
| 2 | Holm — *Scand. J. Stat.* 6(2) | L2 | 1979 | HIGH | HIGH | ACCEPTED |
| 3 | Efron & Tibshirani — *Bootstrap* ch. 14 | L2 | 1993 | HIGH | HIGH | STALE-VALID |
| 4 | Zhou et al. — FENSE (2022) | L2 | 2022 | HIGH | HIGH | ACCEPTED |

---

## § 10. Statistical Power, MDE & Variance Envelope

### 10.1 Metric Variance

Martin-Morato et al. (2024) `[Martin-Morato 2024; L2; HIGH/MED]` characterise variance of AAC metrics on Clotho-eval-like data:

| Metric | σ (across seeds/splits) | Source |
|:-------|:------------------------|:-------|
| SPIDEr-FL | ~12 pp | Martin-Morato 2024 `[L2; HIGH/MED]` |
| FENSE | ~4 pp | Martin-Morato 2024 `[L2; HIGH/MED]` |
| CLAPScore | ~0.03 | Wu 2023 §5 `[L2; HIGH/HIGH]` |
| CIDEr | ~8 pp | Martin-Morato 2024 `[L2; HIGH/MED]` |
| BLEU-4 | ~3 pp | Martin-Morato 2024 `[L2; HIGH/MED]` |

Applicability is MED because Martin-Morato's variance is measured across seeds of supervised models; LALMs at greedy decoding have zero seed-variance but non-zero split-variance. Used as conservative upper bound.

### 10.2 Minimum Detectable Effect per RQ

SE = σ / √n. Two-sided α=0.05, power 0.80 → MDE ≈ 2.8 × SE `[Cohen 1988; L2; HIGH/HIGH — STALE-VALID]`.

| RQ | n | σ used | SE | MDE | Status |
|:--|:-:|:-------|:--:|:---:|:-------|
| RQ1 SPIDEr-FL | 1,045 | 12 pp | 0.37 pp | **~1.04 pp** | Sufficient for Δ ≈ 5 pp |
| RQ2 polyphony-Δ | ~500 | 12 pp | 0.54 pp | **~1.50 pp** | Sufficient for expected Δ ≥ 3 pp |
| RQ3 CHAIR-audio | 500 | σ=0.10 | 0.45 pp | **~1.25 pp** | Sufficient |
| RQ4 temporal | ~50 | 12 pp | 1.70 pp | **~4.76 pp** | Underpowered for <5 pp effects |
| RQ5 CLAPScore | ≤ 20 | 0.03 | 0.0067 | **~0.019** | `[DESCRIPTIVE_ONLY]` |

### 10.3 Confidence Interval Construction

All CIs use **BCa bootstrap** `[Efron & Tibshirani 1993; L2; HIGH/HIGH]` with n=1,000 resamples and seed=42. Implementation: `scipy.stats.bootstrap(..., method='BCa')`.

#### § 10 Evidence Trail

| # | Source | Level | Year | Conf | Applic | Status |
|:-:|:-------|:------|:----:|:----:|:------:|:------:|
| 1 | Martin-Morato et al. | L2 | 2024 | HIGH | MED | ACCEPTED |
| 2 | Efron & Tibshirani ch. 14 | L2 | 1993 | HIGH | HIGH | STALE-VALID |
| 3 | Cohen — *Statistical Power Analysis* | L2 | 1988 | HIGH | HIGH | STALE-VALID |
| 4 | Wu et al. — LAION-CLAP | L2 | 2023 | HIGH | HIGH | ACCEPTED |

---

## § 11. Evidence Hierarchy

This section classifies all project evidence by maturity and reliability.

### Foundational (field-defining, universally accepted)
- Clotho v2.1 `[Drossos 2020; L2]` — canonical evaluation benchmark
- AudioSet `[Gemmeke 2017; L2]` — ontology standard
- SPIDEr / SPIDEr-FL `[DCASE 2020/2024; L1]` — official metric
- BCa bootstrap `[Efron & Tibshirani 1993; L2]` — statistical inference standard
- Holm-Bonferroni `[Holm 1979; L2]` — FWER correction standard
- Soundscape studies `[Schafer 1977; L2]` — humanities conceptual vocabulary

### Current (peer-reviewed, active use, directly applicable)
- SALMONN `[Tang 2023; L2]` — founding LALM, architectural baseline
- FENSE `[Zhou 2022; L2]` — highest human-correlation metric
- LAION-CLAP `[Wu 2023; L2]` — reference-free metric, RQ5 mandatory
- CHAIR `[Rohrbach 2018; L2]` — hallucination measurement (adapted for audio)
- Kuan et al. `[2024; L2]` — hallucination mechanism in LALMs
- MMAU `[Sakshi 2024; L2]` — LALM benchmark
- Wohlin `[2012; L2]` — threat-to-validity framework
- Martin-Morato `[2024; L2]` — metric variance characterisation

### Emerging (preprints, high institutional credibility, no contradicting evidence)
- **AF3** `[Ghosh 2025b; L3]` — primary model; NVIDIA, public code
- **Qwen2.5-Omni** `[Qwen 2025; L3]` — optional ablation; Apache-2.0
- **TAC** `[Kumar 2026; L3]` — temporal grounding architecture; Adobe/Northwestern
- Audio Flamingo Next `[arxiv 2604.10905; L3]` — bleeding-edge; cite with caution

### Unresolved
- Martin-Morato variance applicability to greedy-decoding LALMs (see `research_notes.md` Q7)
- CLAPScore validity on archival Germanic audio (empirical check during RQ5)
- CHAIR-audio 0.25 threshold (sensitivity analysis planned)

---

## § 12. Pre-Registered Falsification & Family-Wise Correction

### 12.1 Why Pre-Registration

Kerr (1998) `[Kerr 1998; L2; HIGH/HIGH]` documents HARKing — hypothesising after results are known. Pre-registration in `hypotheses_preregistered.yml` makes any deviation epistemically visible.

### 12.2 Per-RQ Null Hypotheses and Kill-Criteria

| RQ | H₀ | Kill-criterion |
|:--|:---|:---------------|
| RQ0 | Zero clip-id overlap with AF3/SALMONN training manifests | Any non-zero overlap demotes "zero-shot" claims |
| RQ1 | `SPIDEr-FL(AF3) ≤ 29.6%` | CI lower bound ≤ 29.6% + 1.04 pp MDE → thesis claim falsified |
| RQ2 | `Δ(poly) = Δ(mono)` | Δ within MDE → polyphony not a differential weakness |
| RQ3 | `CHAIR-audio(AF3) = CHAIR-audio(SALMONN)` | CIs overlap → scale/unified-encoder hypothesis weakened |
| RQ4 | Ordering rate = 50% (chance) | Rate ≥ 80% → autoregressive-text-prior mechanism weakened |
| RQ5 | `[DESCRIPTIVE_ONLY]` | Qualitative: panel finds CLAPScore > 0.3 captions miss soundmark features |
| H_NEG | Hallucination rate on silence ≥ 80% | Rate < 50% → text-prior confabulation mechanism weakened |

### 12.3 Holm-Bonferroni Families

Two disjoint families in `hypotheses_preregistered.yml` `[Holm 1979; L2; HIGH/HIGH]`:

- **Family-1** (SPIDEr-FL): {H1 = RQ1, H2 = RQ2, H3 = RQ3-SPIDEr} — k=3, strictest α' = 0.05/3 ≈ 0.0167
- **Family-2** (CHAIR-audio): {H4 = RQ3-CHAIR} — k=1, α' = 0.05

H5 (RQ5) and H6_RQ5 excluded — `[DESCRIPTIVE_ONLY]`.

### 12.4 Cross-Reference

Authoritative machine-readable spec: `hypotheses_preregistered.yml` inside `implementation_plan.md` Phase 0. If this review and the YAML diverge, **the YAML is canonical**.

#### § 12 Evidence Trail

| # | Source | Level | Year | Conf | Applic | Status |
|:-:|:-------|:------|:----:|:----:|:------:|:------:|
| 1 | Holm — *Scand. J. Stat.* 6(2) | L2 | 1979 | HIGH | HIGH | STALE-VALID |
| 2 | Kerr — HARKing (*PSPR* 2(3)) | L2 | 1998 | HIGH | HIGH | ACCEPTED |
| 3 | Rohrbach et al. — CHAIR | L2 | 2018 | HIGH | MED | ACCEPTED |
| 4 | Labbeti — DCASE baseline 29.6% | L1 | 2024 | HIGH | HIGH | ACCEPTED |

---

## § 13. Competing Explanations Pre-Mortem

For each failure mode, the RCA claim (adapter bottleneck) is the *preferred* explanation, not the only one.

### 13.1 Polyphony Under-Description (§ 5.1)

| Competing explanation | Predicts | Discriminator |
|:----------------------|:---------|:--------------|
| Adapter bottleneck (**preferred**) | Drops second event regardless of type | RQ2 on diverse polyphonic clips |
| Dataset-label noise: secondary events missing from references → model learns to drop them | Omission even when events are labelled | Annotator-augmented 100-clip subset |
| Decoding temperature too low → mode-collapse on dominant event | Temperature sensitivity in ablation | Set temperature=0.3 on 50-clip subset |
| Encoder-frozen vs LoRA: frozen AF-Whisper lacks separation | Failure restored by LoRA-tuning | Out of scope; flagged as follow-up |

### 13.2 Entity Hallucination (§ 5.2)

| Competing explanation | Predicts | Discriminator |
|:----------------------|:---------|:--------------|
| Text-prior confabulation (**preferred**) | Rate correlates with text-prior co-occurrence | Kuan 2024 shows pattern; RQ3 confirms on AF3 |
| AudioSet tag incompleteness → false-positive CHAIR count | Inflated rate on sparse-tag clips | Dual criterion neutralises this |
| Training-set memorisation surfaces verbatim | Hallucinated phrases match WavCaps/Clotho-AQA captions | RQ0 contamination audit checks this |

### 13.3 Temporal Grounding Loss (§ 5.3)

| Competing explanation | Predicts | Discriminator |
|:----------------------|:---------|:--------------|
| Autoregressive text prior (**preferred**) | Salient-first, not onset-first | RQ4 synthetic-mixture protocol |
| Non-causal encoder → no onset info at output | Architectural, not decoder-side | TAC ablation: temporal head on same encoder recovers ordering |
| Annotator convention: humans describe salient-first | LALMs match human order → "correct" | Compare LALM order to *acoustic* order, not *annotator* order |

**Decision:** Each failure mode has ≥ 2 falsifiable alternatives with pre-declared discriminators.

#### § 13 Evidence Trail

| # | Source | Level | Year | Conf | Applic | Status |
|:-:|:-------|:------|:----:|:----:|:------:|:------:|
| 1 | Kuan et al. | L2 | 2024 | HIGH | HIGH | ACCEPTED |
| 2 | Kumar et al. — TAC | L3 | 2026 | HIGH | HIGH | ACCEPTED |
| 3 | Ghosh et al. — AF3 | L3 | 2025 | HIGH | HIGH | ACCEPTED |
| 4 | Mei et al. — Survey | L2 | 2022 | HIGH | HIGH | ACCEPTED |

---

## § 14. Broadened Humanities Lineage

§ 1.2 anchored the framing in Schafer 1977 and Heffernan 1993. This section widens the lineage for a Computational Humanities examiner.

### 14.1 Truax — *Acoustic Communication* (1984)

Truax `[Truax 1984; L2; HIGH/HIGH — STALE-VALID: 42yr, field-defining]` distinguishes *listening-in-search*, *listening-in-readiness*, and *background listening*. An AAC system's output implicitly assumes one mode, typically *listening-in-search*. RQ5 implication: archival bell captions encoding *listening-in-search* miss the *background listening* role of bells in civic acoustic identity.

### 14.2 Augoyard & Torgue — *Sonic Experience* (2006)

Augoyard & Torgue `[Augoyard 2006; L2; HIGH/HIGH]` catalogue 82 *sonic effects* (drone, masking, reverberation, ubiquity). AAC outputs favour sound *sources* over sound *effects*: "bell rings" rather than "bell resonates in reverberant square." RQ5 qualitative audit should score caption coverage against this taxonomy.

### 14.3 Sterne (ed.) — *The Sound Studies Reader* (2012)

Sterne `[Sterne 2012; L2; HIGH/HIGH]` reframes sound studies as a post-humanities interdisciplinary field. This legitimises the project's move: an engineering artefact (LALM) interrogated by humanities-grade critique belongs to sound studies.

### 14.4 Born (ed.) — *Music, Sound and Space* (2013)

Born `[Born 2013; L2; HIGH/HIGH]` develops the spatialisation axis: sounds are place-constituting phenomena. Bamberg bells *are* Bamberg — they index civic space, confessional history, institutional continuity. A LALM trained on decontextualised FreeSound clips cannot represent place-indexical meaning.

### 14.5 Sister-Arts Tradition (brief)

The ekphrasis frame has a parallel in the *sister-arts* tradition — Lessing's *Laokoon* (1766) and Mitchell (1986) `[Mitchell 1986; L2; HIGH/MED — STALE-VALID]` argue that cross-modal translation is always lossy, and that the loss is theoretically interesting. AAC inherits this. Flagged as Discussion chapter horizon.

#### § 14 Evidence Trail

| # | Source | Level | Year | Conf | Applic | Status |
|:-:|:-------|:------|:----:|:----:|:------:|:------:|
| 1 | Truax — *Acoustic Communication* | L2 | 1984 | HIGH | HIGH | STALE-VALID |
| 2 | Augoyard & Torgue — *Sonic Experience* | L2 | 2006 | HIGH | HIGH | ACCEPTED |
| 3 | Sterne (ed.) — *Sound Studies Reader* | L2 | 2012 | HIGH | HIGH | ACCEPTED |
| 4 | Born (ed.) — *Music, Sound and Space* | L2 | 2013 | HIGH | HIGH | ACCEPTED |
| 5 | Mitchell — *Iconology* | L2 | 1986 | HIGH | MED | STALE-VALID |

**Decision:** Humanities lineage extended from 2 to 7 sources. Each tied to a specific RQ or framing choice.

> **`[TODO-ingest; humanities boundary]`** — Two source classes are explicitly *deferred* from this lineage and flagged for a later humanities-ingest session: (1) **WCAG 2.1 AA** as a primary normative source for the accessibility claim in `PROJECT_GUIDE.md` §Why This Matters / Accessibility, and (2) **DARIAH-EU strategic plan** plus institutional documentation for the British Library Sound Archive, BBC Sound Effects Archive, and Europeana as primary sources for the cultural-archive claim. They are currently asserted via secondary references; do **not** fabricate primary citations until the ingest session has retrieved the actual normative documents. The wiki pages `wiki/07_humanities/accessibility.md` and `wiki/07_humanities/digital-archives.md` already self-flag this gap.

---

## § 15. Integrity Gate (Final Checklist)

Before any Evaluation or Discussion chapter is written, these must all be green:

- [ ] Clotho-eval Zenodo record = **4783391** (not 3490684)
- [ ] DCASE 2024 baseline reproduced at **29.6% ± 1% SPIDEr-FL**
- [ ] RQ0 contamination audit completed; "zero-shot" claims conditional
- [ ] Holm-Bonferroni applied to Family-1; Family-2 separate
- [ ] BCa bootstrap (n=1000, seed=42) for every CI
- [ ] Negative controls run; hallucination rate disclosed
- [ ] `setup_check.py` passes SM ≥ 8.0 gate
- [ ] Determinism pins asserted (`PYTHONHASHSEED=42`, `CUBLAS_WORKSPACE_CONFIG=:4096:8`)
- [ ] Every §9 threat has a traceable mitigation
- [ ] Every §13 competing explanation has a pre-declared discriminator

Any unchecked box at submission time must be disclosed.
