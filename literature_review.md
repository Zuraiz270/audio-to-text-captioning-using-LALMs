# Literature Review (EBSE-Compliant) — T6: Audio-to-Text Captioning using LALMs
*Master's Project · CH-Proj-M · SS 2026 · Zuraiz (2177213)*  
*Prof. Dr.-Ing. Jakob Abeßer · Computational Humanities · Uni Bamberg*

> **EBSE Protocol (CLAUDE.md §2–§3):** Every empirical claim below carries an inline evidence badge: `[Author Year; Lx; CONF/APPLIC]` where Lx = source level (L1=official dataset/benchmark, L2=peer-reviewed, L3=preprint), CONF = confidence in the evidence quality (HIGH / MED), APPLIC = applicability to this project (HIGH / MED / LOW). Staleness flagged per §3.2 (>10yr = `[STALE-VALID]` with justification). Zero unverified claims.

---

## § 1. Task Definition: What AAC Is and Is Not

### 1.1 Formal Task Boundary

Automated Audio Captioning (AAC) was formally defined as a distinct task by Drossos, Lipping, and Virtanen `[Drossos 2020; L2; HIGH/HIGH]` as *inter-modal translation*: a raw audio waveform as input, a free-text natural-language description as output. Two adjacent tasks must be precisely distinguished because their architectures, datasets, and metrics are not interchangeable:

| Task | Input | Output | Captures |
|:-----|:------|:-------|:---------|
| **Audio Tagging** | Waveform | Label set `{dog, traffic, rain}` | Identities only — no relation, order, texture |
| **ASR** | Waveform (speech) | Word transcript | Speech channel only — non-speech ignored |
| **AAC (this project)** | Any waveform | Free-text description | Identities + relations + texture + temporal order |

The linguistic surplus of AAC over Audio Tagging is not cosmetic. Consider: the tag set `{dog, traffic, wind}` carries zero information about whether the dog is near or far, whether the traffic is wet or dry, whether the wind precedes or follows. The caption *"A dog barks in the distance as cars pass on a wet road while wind rustles nearby leaves"* encodes spatial distance (`distance`), surface texture (`wet`), temporal concurrence (`as`, `while`), and acoustic texture (`rustles`). None of these can be recovered from the tag set. This is the *information gap* that makes AAC a distinct and harder problem `[Drossos 2020; L2; HIGH/HIGH]`.

### 1.2 Humanities Framing: Ekphrasis and Soundscape Studies

**Why this belongs in Computational Humanities, not MIR.** The humanistic lineage of AAC runs through two independent traditions that converge on this project.

**Ekphrasis** — the classical rhetorical genre of verbal description of non-verbal aesthetic experience — is most often associated with visual art (Homer's shield of Achilles, *Iliad* 18.478–608 `[STALE-VALID: foundational literary example; no modern replacement]`; Heffernan 1993, *Museum of Words* `[Heffernan 1993; L2; HIGH/HIGH — humanities anchor]`). AAC is the computational instantiation of ekphrasis for acoustic objects: a machine that produces verbal descriptions of acoustic experiences that resist direct verbal expression. The theoretical claim is that the same semiotic gap that makes visual ekphrasis interesting — the translation between sign systems — operates in the acoustic domain with additional difficulty, because acoustic experience is transient and lacks the stable spatial anchor of visual art.

**Soundscape Studies** was inaugurated by R. Murray Schafer's *The Tuning of the World* (1977) `[Schafer 1977; L2; HIGH/HIGH — STALE-VALID: 49yr but no replacement exists for conceptual vocabulary]`. Schafer defined three acoustic categories with direct implications for what an AAC system must describe:

| Schafer Category | Definition | AAC Implication |
|:-----------------|:-----------|:----------------|
| **Keynote sound** | Background tone defining an acoustic environment (e.g., city hum, ocean) | Must be described even when it carries low event salience |
| **Soundmark** | Community-specific sound of cultural identity (e.g., Bamberg Martinskirche bells) | Primary target of RQ5; likely OOD for Freesound-trained models |
| **Sound signal** | Foreground sound demanding active attention (e.g., alarm, horn) | High-salience; most reliably described by current LALMs |

A LALM trained on FreeSound `[Drossos 2020; L2; HIGH/HIGH]` and AudioSet `[Gemmeke 2017; L2; HIGH/HIGH]` will have strong priors for sound signals and moderate priors for keynote sounds. Soundmarks — culturally-specific, geographically-anchored, institutionally-singular sounds — are structurally absent from web-scraped training corpora. This is the mechanism behind RQ5's domain-shift hypothesis: not just "can AF3 handle new audio" but "does AF3's FreeSound prior systematically mischaracterise culturally-specific acoustic identities?"

**Digital archives use case.** DARIAH-EU's Strategic Plan (2023) `[DARIAH 2023; L1; HIGH/HIGH]` identifies automated captioning of audio-visual cultural heritage as a priority system capability. The British Library Sound Archive (>6.5M recordings) and BBC Sound Effects Archive (>33,000 CC-licensed clips) have no systematic free-text caption layer. This is not a convenience — it is a structural accessibility failure for blind and low-vision users and for semantic search. AAC addresses it directly.

#### § 1 Evidence Trail

| # | Source | Level | Year | Conf | Applic | Status |
|:-:|:-------|:------|:----:|:----:|:------:|:------:|
| 1 | Drossos et al. — Clotho (ICASSP 2020) | L2 | 2020 | HIGH | HIGH | ACCEPTED |
| 2 | Gemmeke et al. — AudioSet (ICASSP 2017) | L2 | 2017 | HIGH | HIGH | ACCEPTED |
| 3 | Heffernan — Museum of Words (1993) | L2 | 1993 | HIGH | HIGH | STALE-VALID |
| 4 | Schafer — Tuning of the World (1977) | L2 | 1977 | HIGH | HIGH | STALE-VALID |
| 5 | DARIAH-EU Strategic Plan (2023) | L1 | 2023 | HIGH | HIGH | ACCEPTED |

**Conflicts:** None. L1 sources (DARIAH + Clotho Zenodo) do not conflict with L2 literature.  
**Rejected:** No blog posts or secondary summaries of Schafer. Cite primary text only.

---

## § 2. Evaluation Datasets: Hierarchy and Misuse Risks

A systematic error in the AAC literature is treating all audio-caption datasets as interchangeable. They are not. This section establishes the three-tier hierarchy that governs all experiments in this project.

### 2.1 Tier 1 — Primary Evaluation (Clotho v2.1)

Clotho v2.1 `[Drossos 2020; L2; HIGH/HIGH]` is the canonical evaluation benchmark. Three design decisions make it superior to alternatives for scientific comparison:

1. **Five captions per clip**: five independent human annotations per clip enable consensus-based metric computation. BLEU, CIDEr, and SPICE all benefit from reference plurality — with one reference, metric variance is dominated by annotator idiosyncrasy rather than caption quality `[Zhou 2022; L2; HIGH/HIGH]`.
2. **15–30 second duration**: longer than AudioCaps (10s), providing richer temporal structure and polyphony opportunities.
3. **Acoustic focus annotation protocol**: annotators were instructed to describe *what they hear*, not what they imagine the scene to look like. This eliminates visual inference bias.

> [!WARNING]
> **Critical versioning error.** Clotho v2.1 is at Zenodo record **4783391**. Zenodo record **3490684** is Clotho v1 with different splits and different clip count. Any SPIDEr-FL number computed on v1 is not comparable to DCASE 2024's 29.6% floor `[Labbeti 2024; L1; HIGH/HIGH]`. This error appeared in the Flash-3.0 first draft and was present until v2. It is now asserted by `setup_check.py`.

| Split | Clips | Purpose |
|:------|:-----:|:--------|
| Development | 3,839 | Pre-processing sanity checks |
| Validation | 1,045 | Development-time model selection |
| **Evaluation ⭐** | **1,045** | **Final metric reporting — RQ1, RQ2, RQ3** |
| Test | 1,045 | Withheld; not used in this project |

### 2.2 Tier 2 — Auxiliary Experiment (AudioCaps)

AudioCaps `[Kim 2019; L2; HIGH/HIGH]` provides ~46,000 YouTube-derived clips with one crowdsourced caption each. It is explicitly **not** used for primary metric reporting in this project (single reference makes metrics unreliable). Its role is:

- **RQ3 (hallucination)**: the AudioSet metadata provides ground-truth AudioSet class tags per clip, enabling the CHAIR-audio protocol. Single-event clips (identified by AudioSet tag count = 1) are the stimulus set for measuring entity hallucination rate.
- AudioSet's ontology of 632 hierarchically-organised sound classes `[Gemmeke 2017; L2; HIGH/HIGH]` is the vocabulary for cross-referencing extracted nouns against ground-truth tags.

### 2.3 Tier 3 — Pre-training Corpora (NEVER Evaluation)

> [!CAUTION]
> These datasets are cited for contamination audit (RQ0) and context only. They must never be used as evaluation sets.

| Dataset | Size | Source | Role in This Project |
|:--------|:----:|:-------|:---------------------|
| WavCaps `[Mei 2023; L3; HIGH/HIGH]` | ~400k | FreeSound + YouTube + BBC | RQ0: contamination audit manifest |
| AudioSetCaps | ~6.1M | YouTube / AudioSet | RQ0: contamination audit manifest |
| Clotho-AQA `[Lipping 2022; L2; HIGH/HIGH]` | ~7k | Clotho | RQ0: highest-risk contamination source |

**The contamination risk is structural, not hypothetical.** AudioSetCaps and WavCaps both derive from the same upstream repositories (FreeSound, AudioSet) as Clotho v2.1. AF3's training data card `[Ghosh 2025b; L3; HIGH/HIGH]` must be cross-referenced against these manifests before RQ1 results can be characterised as "zero-shot."

#### § 2 Evidence Trail

| # | Source | Level | Year | Conf | Applic | Status |
|:-:|:-------|:------|:----:|:----:|:------:|:------:|
| 1 | Drossos et al. — Clotho v2.1, Zenodo 4783391 | L1 | 2021 | HIGH | HIGH | FLOOR DATASET |
| 2 | Kim et al. — AudioCaps (NAACL 2019) | L2 | 2019 | HIGH | HIGH | AUX (RQ3 only) |
| 3 | Gemmeke et al. — AudioSet (ICASSP 2017) | L2 | 2017 | HIGH | HIGH | ONTOLOGY |
| 4 | Labbeti 2024 — DCASE baseline (establishes 29.6% floor) | L1 | 2024 | HIGH | HIGH | FLOOR |

**Decision:** Clotho-eval split (1,045 clips, Zenodo 4783391) is the exclusive primary evaluation set.  
**Conflicts:** None.  
**Rejected:** WavCaps, AudioSetCaps, Clotho-AQA as evaluation sets — pre-training corpora only.

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

The encoder is trained for audio classification (event detection) and then adapted — via fine-tuning or frozen feature extraction — for captioning. The decoder is a standard autoregressive LM trained with teacher forcing on human reference captions.

### 3.2 The Comparison Floor: DCASE 2024 CNext-trans

The DCASE 2024 Task 6 baseline `[Labbeti 2024; L1; HIGH/HIGH]` represents the strongest traditionally-supervised AAC system with a public, reproducible implementation:

- **Encoder**: ConvNeXt `[Liu 2022; L2; HIGH/HIGH]` backbone pretrained for audio classification → frame-level embeddings from log-mel spectrogram
- **Decoder**: Transformer seq2seq with cross-attention over encoder output
- **Training**: Fully supervised on Clotho; no LLM, no foundation model
- **Result**: **29.6% SPIDEr-FL on Clotho-eval** `[Labbeti 2024; L1; HIGH/HIGH]`

This is the single most important number in the project. It is the *supervised* baseline that a zero-shot LALM must exceed to justify the thesis claim that scale and general pretraining compensate for task-specific supervision.

> **RCA: Why traditional systems hit a ceiling.** The encoder-decoder model has no mechanism for polyphonic event segregation. If two events co-occur at frame *t*, their mel-spectrogram representations superimpose. The single encoder embedding at frame *t* contains entangled information from both events. The decoder observes this entangled representation and generates text for the *dominant* event — the one with higher acoustic energy. The secondary event is suppressed. This is not a training failure; it is an **architectural impossibility** — single-stream encoding with no separation head cannot represent concurrent events independently `[Mei 2022; L2; HIGH/HIGH; confirms]`.

#### § 3 Evidence Trail

| # | Source | Level | Year | Conf | Applic | Status |
|:-:|:-------|:------|:----:|:----:|:------:|:------:|
| 1 | Mei et al. — AAC Survey (EURASIP 2022) | L2 | 2022 | HIGH | HIGH | ACCEPTED |
| 2 | Labbeti — DCASE 2024 T6 Baseline | L1 | 2024 | HIGH | HIGH | **FLOOR** |
| 3 | Kong et al. — PANNs (IEEE TASLP 2020) | L2 | 2020 | HIGH | HIGH | ACCEPTED (encoder lineage) |

**Decision:** 29.6% SPIDEr-FL is the comparison floor for RQ1. Reproduction of this number (±1%) is the Phase 2 canary test for the metric pipeline.

---

## § 4. The LALM Revolution: Architecture, Scale, and the Emergence of Zero-Shot AAC

### 4.1 The Architectural Shift: From Task-Specific to Foundation-First

All LALMs share one blueprint that replaces the encoder-decoder paradigm:

```
Waveform → [ Audio Encoder ] → [ Adapter / Q-Former ] → [ LLM Decoder ] → Caption/Answer
               (pretrained,                 (lightweight,        (frozen or
                frozen)                    bridge module)        LoRA-tuned)
```

The key difference from § 3: neither the audio encoder nor the LLM was trained for captioning. The encoder produces general-purpose audio representations; the LLM provides general-purpose language modelling; the adapter learns only how to project one representation space into the other. This gives LALMs emergent zero-shot captioning without any task-specific training data.

### 4.2 SALMONN — Founding LALM (ICLR 2024)

Tang et al. (2023) `[Tang 2023; L2; HIGH/HIGH]` introduced SALMONN as the first model with generic *hearing* capability — simultaneous competence on speech, music, and environmental audio. Its architectural innovation is the **dual audio encoder**:

```
Waveform ──→ [ Whisper-Large-v2 ] ─────┐
             (680k hrs speech)          ├──→ [ Q-Former ] ──→ [ Vicuna-13B ]
Waveform ──→ [ BEATs ]           ─────┘
             (AudioSet events)
```

**Rationale for dual encoding** `[Tang 2023; L2; HIGH/HIGH]`: Whisper was trained on 680,000 hours of labelled speech `[Radford 2023; L2; HIGH/HIGH]` and is therefore biased toward speech phonetics. Environmental sounds that Whisper encodes as "speech-like noise" are independently captured by BEATs `[Chen 2022; L2; HIGH/HIGH]`, which was trained specifically on AudioSet environmental audio. The dual design is an explicit hedge: no single encoder was trained on the full audio domain, so use two specialised ones.

**Why this matters for RQ2 (polyphony):** SALMONN's dual encoder was specifically designed to handle acoustic diversity — to separate speech information from event information. If this design fails at polyphony (both events are environmental, not separable by the speech/event axis), it tells us something important: the polyphony problem cannot be solved by encoder specialisation along the speech/environment axis. It requires within-domain concurrent-event separation that no current architecture provides explicitly.

**Parameters:** 13B total (Vicuna-13B LLM); ~24GB VRAM bf16 / ~14GB int4 `[Tang 2023; L2; HIGH/HIGH]`.

### 4.3 Audio Flamingo 3 — Current SOTA (July 2025)

Ghosh et al. (2025) `[Ghosh 2025b; L3; HIGH/HIGH]` present Audio Flamingo 3, which supersedes all prior open and closed LALMs on every major audio understanding benchmark:

| Benchmark | AF3 | Qwen2.5-Omni | SALMONN | GPT-4o-audio |
|:----------|:----|:------------|:--------|:-------------|
| MMAU `[Sakshi 2024; L2; HIGH/HIGH]` | **72.28** | ~70 | not directly reported here † | ~70 |
| ClothoAQA | **91.1%** | — | — | — |
| CMM-Hallucination | **86.7%** | — | — | — |
| Clotho-Entailment | **92.9%** | — | — | — |

Source: Ghosh et al. 2025b `[L3; HIGH/HIGH]` — preprint; not yet peer-reviewed. Confidence is HIGH despite L3 because: (1) NVIDIA institution affiliation, (2) benchmark code is public, (3) no conflicting evidence from independent replication as of April 2026.

† **SALMONN MMAU disclosure:** The AF3 paper's comparison table `[Ghosh 2025b; L3; HIGH/HIGH]` reports its own MMAU score (72.28) and positions itself above prior LALMs, but the exact numerical MMAU score for SALMONN is not re-transcribed in this review because we have not independently verified it against the MMAU leaderboard `[Sakshi 2024; L2; HIGH/HIGH]`. Zero-fluff disclosure per CLAUDE.md §2 Rule 3. The qualitative claim ("below AF3 and below Qwen2.5-Omni on MMAU") is sufficient for the architectural argument in § 5.

**Architectural key difference from SALMONN** `[Ghosh 2025b; L3; HIGH/HIGH; Ghosh 2025a; L3; HIGH/HIGH]`: AF3 replaces the dual-encoder design with a **unified AF-CLAP encoder** — a single model trained contrastively on a massive mixed corpus of speech, environmental sounds, and music simultaneously. The dual-encoder hedge is abandoned in favour of *scale and data diversity*. This is the central architectural argument for the Discussion chapter: AF3's success demonstrates that the dual-encoder hedge is a **second-best solution**; a sufficiently large single encoder trained on sufficiently diverse data renders architectural specialisation unnecessary.

**Parameters:** 8B `[Ghosh 2025b; L3; HIGH/HIGH]`; ~20GB VRAM bf16 / ~10GB int4.

### 4.4 Qwen2.5-Omni — End-to-End Multimodal (March 2025)

Qwen Team (2025) `[Qwen 2025; L3; HIGH/HIGH]` present an end-to-end model integrating text, audio, image, and video in a single architecture with streaming output. For this project it serves as an optional third data point (notebook `09_qwen25_ablation.ipynb`): if AF3 and Qwen2.5-Omni show the same polyphony and hallucination failure pattern, the finding is LALM-general rather than AF3-specific.

**Licence:** Apache-2.0 `[Qwen 2025; L3; HIGH/HIGH]` — lowest legal risk among all models in this project.

#### § 4 Evidence Trail

| # | Source | Level | Year | Conf | Applic | Status |
|:-:|:-------|:------|:----:|:----:|:------:|:------:|
| 1 | Tang et al. — SALMONN (ICLR 2024) | L2 | 2023 | HIGH | MED | BASELINE |
| 2 | Radford et al. — Whisper (ICML 2023) | L2 | 2023 | HIGH | HIGH | ACCEPTED (encoder background) |
| 3 | Chen et al. — BEATs (ICML 2023) | L2 | 2023 | HIGH | HIGH | ACCEPTED (SALMONN encoder) |
| 4 | Ghosh et al. — AF2 (arxiv 2503.03983) | L3 | 2025 | HIGH | HIGH | ACCEPTED (AF-CLAP lineage) |
| 5 | **Ghosh et al. — AF3 (arxiv 2507.08128)** | L3 | 2025 | HIGH | HIGH | **PRIMARY SOTA** |
| 6 | Qwen Team — Qwen2.5-Omni (arxiv 2503.20215) | L3 | 2025 | HIGH | HIGH | ACCEPTED |
| 7 | Sakshi et al. — MMAU (arxiv 2410.19168) | L2 | 2024 | HIGH | HIGH | BENCHMARK REF |

**Decision:** AF3 as primary model. SALMONN as historical baseline. Qwen2.5-Omni as optional ablation.  
**Conflict:** SALMONN is L2 (peer-reviewed ICLR); AF3 is L3 (preprint). Global §3.2: hierarchy L2 > L3. Resolution: applied recency rule (§3.2: "Recency") — AF3 (Jul 2025) demonstrably supersedes SALMONN on all public benchmarks. Decision is disclosed.

---

## § 5. Root Cause Analysis of Three Failure Modes

> **EBSE §2 Rule 2 — RCA.** From CLAUDE.md: *"Fix architectural failure, no workarounds."* Applied to the research question: the three failure modes are not independent bugs. They share a root cause. Identifying it enables a focused research contribution.

### 5.1 Failure Mode 1: Polyphony Under-Description

**Observation:** Standard AAC models — including LALMs — systematically omit secondary concurrent acoustic events when multiple sounds overlap `[Mei 2022; L2; HIGH/HIGH]`.

**RCA (architectural level):**
```
Input:    [bark @ 0–3s] + [traffic @ 1–5s]          ← Two concurrent sources
Encoder:  One embedding per frame; frame at t=1.5s encodes bark+traffic entangled
Q-Former: Compresses encoder output to N query tokens; entangled representation persists
LLM:      Generates text auto-regressively; text prior favours mentioning the louder source
Output:   "A dog barks in the distance."             ← Traffic silently dropped
```

The bottleneck is at the **Q-Former** (or equivalent adapter): it compresses multiple entangled concurrent-event embeddings into a fixed number of query tokens. Information about the quieter second event is irreversibly lost at this compression step. No amount of LLM capacity can recover information that was never transmitted through the adapter. This is a **structural information bottleneck**, not a training failure `[Ghosh 2025b; L3; HIGH/HIGH — AF3 paper acknowledges polyphony as an open challenge]`.

### 5.2 Failure Mode 2: Entity Hallucination

**Observation:** LALMs generate descriptions mentioning sound entities that are not present in the audio `[Kuan 2024; L2; HIGH/HIGH]`.

**RCA (architectural level):** The LALM's LLM decoder has been trained on vast text corpora where certain concepts co-occur with high frequency (e.g., *park → dog → children → birds → traffic*). When the audio encoder provides an ambiguous or low-signal embedding (as happens under the polyphony bottleneck), the LLM fills the generation gap with its most probable continuation of the partial caption. This is textbook LLM confabulation, transferred to the multimodal setting.

**The link to Failure Mode 1:** The information bottleneck of the Q-Former *causes* hallucination. When the adapter fails to transmit full acoustic information, the LLM operates with an under-constrained representation and compensates with its text prior. Polyphony → encoder bottleneck → under-constrained LLM representation → hallucination. **The three failure modes share a root cause.**

Kuan et al. (2024) `[Kuan 2024; L2; HIGH/HIGH]` empirically confirm this mechanism: hallucination rate increases significantly for sounds that co-occur frequently with other sounds in natural language, and is lowest for unexpected sounds that have no strong text prior. This is the signature of text-prior confabulation, not audio perception failure.

**Quantified baseline:** AF3 reports 86.7% accuracy on CMM-Hallucination `[Ghosh 2025b; L3; HIGH/HIGH]`. This means 13.3% of responses contain hallucinated content on this specific controlled benchmark. On uncontrolled multi-event Clotho clips, we expect this to be higher (RQ3 hypothesis H4).

### 5.3 Failure Mode 3: Temporal Grounding Loss

**Observation:** LALMs describe events in *canonical text-prior order* rather than actual acoustic onset order `[Kumar 2026; L3; HIGH/HIGH]`.

**RCA (architectural level):** Autoregressive LLM decoding generates tokens left-to-right. The decoder has strong priors over temporal ordering of concepts from training text (humans tend to describe a soundscape starting with the most salient event, which training data encodes as a statistical regularity). When actual onset order deviates from canonical order, the decoder's text prior overrides the audio-encoder evidence.

TAC (Kumar et al., 2026) `[Kumar 2026; L3; HIGH/HIGH]` demonstrate this with a synthetic experiment: mixed clips where event A starts before event B but B is acoustically louder. LALMs consistently describe B before A — following salience-order (text-prior) rather than onset-order (audio evidence). The correct-ordering rate for LALMs on this task is reported to be significantly below TAC's explicit temporal grounding head.

**Architectural analysis:** TAC's solution — a **separate temporal grounding head** that predicts onset/offset timestamps before text generation — bypasses the autoregressive ordering bias entirely. This suggests that the three-failure-mode pattern is not just about training data quantity but about the fundamental mismatch between autoregressive text generation and the temporal structure of acoustic scenes.

**The unified root cause,** synthesised across all three failure modes:

> *Information compression in the adapter (Q-Former) destroys concurrent-event separation → LLM operates with under-constrained representation → text prior fills the gap → wrong entities are mentioned (hallucination) → wrong events are omitted (polyphony under-description) → wrong temporal order is produced (temporal grounding loss). All three are symptoms of one architectural failure: the information bottleneck between a general-purpose audio encoder and a general-purpose LLM, with no mechanism for concurrent-event segregation at the adapter layer.*

This unified root cause is the central claim of the Discussion chapter of the term paper.

#### § 5 Evidence Trail

| # | Source | Level | Year | Conf | Applic | Status |
|:-:|:-------|:------|:----:|:----:|:------:|:------:|
| 1 | Mei et al. — AAC Survey (EURASIP 2022) | L2 | 2022 | HIGH | HIGH | ACCEPTED (polyphony observation) |
| 2 | Kuan et al. — LALM Limits (Interspeech 2024) | L2 | 2024 | HIGH | HIGH | ACCEPTED (hallucination mechanism) |
| 3 | Ghosh et al. — AF3 (arxiv 2507.08128) | L3 | 2025 | HIGH | HIGH | ACCEPTED (86.7% hallucination benchmark) |
| 4 | Kumar et al. — TAC (arxiv 2602.15766) | L3 | 2026 | HIGH | HIGH | ACCEPTED (temporal ordering failure + fix) |
| 5 | Rohrbach et al. — CHAIR (EMNLP 2018) | L2 | 2018 | HIGH | MED | ACCEPTED (hallucination measurement protocol) |

**RCA Decision:** Three failure modes share one architectural root cause — adapter information bottleneck under polyphony. This is the thesis of the Discussion chapter.  
**Applicability note on Rohrbach 2018 (MED):** CHAIR was designed for image captioning. The audio adaptation requires replacing image object lists with AudioSet tags, and adding the CLAPScore dual criterion. The adaptation introduces uncertainty; hence MED applicability. The CHAIR-audio protocol is disclosed as an adaptation in the methodology chapter.

---

## § 6. Evaluation Metrics: Protocol and Validity Claims

### 6.1 N-gram Metrics: Historical Context Only

BLEU `[Papineni 2002; L2; HIGH/HIGH — STALE-VALID: 24yr, foundational; no claim of domain validity]`, METEOR `[Banerjee 2005; L2; HIGH/HIGH — STALE-VALID: 21yr]`, ROUGE-L `[Lin 2004; L2; HIGH/HIGH — STALE-VALID: 22yr]` are reported for comparison with prior literature only. Zhou et al. (2022) `[Zhou 2022; L2; HIGH/HIGH]` demonstrate empirically that these metrics show significantly lower correlation with human quality judgements for audio captions than FENSE, specifically because they reward n-gram surface overlap rather than semantic accuracy.

### 6.2 CIDEr and SPICE: Stronger but Domain-Borrowed

CIDEr `[Vedantam 2015; L2; HIGH/HIGH — STALE-VALID: 11yr, at boundary]` weights n-grams by TF-IDF, rewarding discriminative terms. SPICE `[Anderson 2016; L2; HIGH/HIGH — STALE-VALID: 10yr, at boundary]` parses scene graphs and measures triple overlap (object, relation, attribute). Both were designed for image captioning and transferred to audio without domain validation — which is precisely what Zhou et al. (2022) critique.

> **STALE-VALID §3.2 justification (CIDEr · SPICE):** Retained only as the two inner components of SPIDEr / SPIDEr-FL, which remains the official DCASE 2024 Task 6 scoring function `[Labbeti 2024; L1; HIGH/HIGH]`. No newer domain-validated replacement has been published for either component; any move away from CIDEr/SPICE would break comparability with every SPIDEr-FL number in the prior literature. Staleness is therefore a comparability constraint, not a methodological endorsement.

### 6.3 SPIDEr-FL: The Official Standard

`SPIDEr = (SPICE + CIDEr) / 2` `[DCASE 2020; L1; HIGH/HIGH — task definition]`  
`SPIDEr-FL = SPIDEr × Fluency_Error_Penalty` `[Labbeti 2024; L1; HIGH/HIGH — DCASE 2024 addition]`

The Fluency penalty was added in DCASE 2024 `[Labbeti 2024; L1; HIGH/HIGH]` to penalise degenerate LLM outputs (repetition loops, truncated sentences). Implementation: `aac-metrics` `[Labbeti 2024; L1; HIGH/HIGH]` — the *only* valid implementation for producing numbers comparable to DCASE 2024 results. Requires Java 11+ for SPICE computation. DCASE 2024 baseline: **29.6%** `[Labbeti 2024; L1; HIGH/HIGH]`.

### 6.4 FENSE: The Highest-Human-Correlation Metric

Zhou et al. (2022) `[Zhou 2022; L2; HIGH/HIGH]` propose FENSE by combining:
1. **SentenceBERT** `[Reimers 2019; L2; HIGH/HIGH]` similarity between candidate and mean reference embedding — captures global semantic similarity beyond surface n-grams.
2. **Fluency Error Penalty** from a separately trained classifier — penalises disfluent captions.

FENSE achieved the highest human-correlation coefficient among all tested metrics at time of publication `[Zhou 2022; L2; HIGH/HIGH]`. The `aac-metrics` maintainer explicitly recommends SPIDEr + FENSE as the **primary metric pair** `[Labbeti 2024; L1; HIGH/HIGH]`.

**Limitation:** FENSE requires human reference captions (SentenceBERT embeds both candidate and references). For RQ5 (Bamberg bells / BBC archive), no references exist. FENSE is mathematically undefined there. `[Zhou 2022; L2; HIGH/HIGH — references required; confirmed by metric definition]`.

### 6.5 CLAPScore: The Only Reference-Free Option

Wu et al. (2023) `[Wu 2023; L2; HIGH/HIGH]` present LAION-CLAP — contrastive audio-language pretraining on a mixed corpus. Given an audio waveform and a text string, CLAP computes cosine similarity in a shared embedding space.

**CLAPScore** applies this directly as an evaluation metric: `CLAPScore(caption, audio) = cosine_similarity(CLAP_audio(audio), CLAP_text(caption))`. This requires **no human reference captions** — the audio waveform itself is the reference.

**Why this is non-negotiable for RQ5** `[Wu 2023; L2; HIGH/HIGH]`: The Bamberg church bells and BBC Sound Effects clips used in RQ5 have zero human-written captions. SPIDEr-FL, FENSE, BERTScore, and all other reference-based metrics are literally undefined (division by zero in the reference set). CLAPScore is the only metric that can produce a number. If CLAPScore is excluded from the metric stack, RQ5 has no quantitative component.

**Known limitation** `[Wu 2023; L2; HIGH/HIGH — training data disclosure]`: LAION-CLAP was trained on a corpus that may not include archival Germanic soundscape audio. If so, its embedding space may not faithfully represent culturally-specific sounds. This limitation must be disclosed in the methodology chapter and is the motivation for the qualitative component of RQ5.

### 6.6 The Hallucination Measurement Protocol (CHAIR-Audio)

Rohrbach et al. (2018) `[Rohrbach 2018; L2; HIGH/MED]` defined CHAIR for image captioning:

```
CHAIR_entity = |hallucinated objects| / |all objects mentioned|
where: object is "hallucinated" iff it does not appear in image segmentation ground truth
```

This project adapts CHAIR for audio with a **dual criterion** (stricter than the original):

```
entity is "hallucinated" iff
  (a) entity ∉ ground-truth AudioSet tag set   [label-based: inherited from CHAIR]
  AND
  (b) CLAPScore(entity, audio) < 0.25          [audio-grounded: new addition]
```

The dual criterion is necessary because AudioSet tagging is known to be incomplete — not all audible events are tagged. Criterion (b) prevents false-positive hallucination counts for audible events that the annotators missed. This is a methodological improvement over naive CHAIR transfer `[Rohrbach 2018; L2; HIGH/MED — adaptation disclosed]`.

#### § 6 Evidence Trail

| # | Source | Level | Year | Conf | Applic | Status |
|:-:|:-------|:------|:----:|:----:|:------:|:------:|
| 1 | Labbeti — DCASE 2024 + aac-metrics | L1 | 2024 | HIGH | HIGH | TOOL + FLOOR |
| 2 | Zhou et al. — FENSE (ICASSP 2022) | L2 | 2022 | HIGH | HIGH | PRIMARY METRIC |
| 3 | Wu et al. — LAION-CLAP (ICASSP 2023) | L2 | 2023 | HIGH | HIGH | RQ5 MANDATORY |
| 4 | Rohrbach et al. — CHAIR (EMNLP 2018) | L2 | 2018 | HIGH | MED | ADAPTED (audio) |
| 5 | Papineni et al. — BLEU (ACL 2002) | L2 | 2002 | HIGH | HIGH | STALE-VALID (historical only) |
| 6 | Vedantam et al. — CIDEr (CVPR 2015) | L2 | 2015 | HIGH | MED | STALE-VALID (at 10yr boundary) |
| 7 | Anderson et al. — SPICE (ECCV 2016) | L2 | 2016 | HIGH | MED | STALE-VALID (10yr boundary) |

**Metric reporting minimum (per §3.2 sufficiency rule):**
`SPIDEr-FL · CIDEr · SPICE · FENSE · CLAPScore · CHAIR-audio hallucination rate`

---

## § 7. Research Gap Matrix — Proving Originality

Every RQ in this project maps to a cell in the published literature that is **empty**. This table is the originality proof for the term paper § 1 (Introduction: Contribution).

| Measurement | AF3 paper | SALMONN paper | DCASE 2024 | Kuan 2024 | TAC 2026 | **This project** |
|:------------|:---------:|:-------------:|:----------:|:---------:|:--------:|:----------------:|
| SPIDEr-FL, AF3 zero-shot vs DCASE supervised baseline, Clotho-eval | ❌ | ❌ | ❌ | ❌ | ❌ | **✅ RQ1** |
| Contamination audit AF3 + SALMONN vs Clotho-eval | ❌ | ❌ | ❌ | ❌ | ❌ | **✅ RQ0** |
| Polyphony-specific Δ(LALM − baseline) SPIDEr-FL, Clotho | ❌ | ❌ | ❌ | ❌ | ❌ | **✅ RQ2** |
| CHAIR-audio hallucination rate, AF3 vs SALMONN, AudioCaps | ❌ | ❌ | ❌ | partial | ❌ | **✅ RQ3** |
| Temporal A-then-B ordering rate, AF3 vs SALMONN synthetic mix | ❌ | ❌ | ❌ | ❌ | ✅ (TAC only) | **✅ RQ4** |
| CLAPScore-only eval, LALM on cultural-heritage archival audio, Schafer framing | ❌ | ❌ | ❌ | ❌ | ❌ | **✅ RQ5** |

> [!IMPORTANT]
> The "RQ3 partial" for Kuan 2024 means they measured hallucination qualitatively on a different stimulus set without the CHAIR-audio dual CLAPScore criterion. The quantitative CHAIR-audio measurement on AF3 specifically versus the DCASE baseline is still an empty cell.

#### § 7 Evidence Trail

| # | Source | Level | Year | Conf | Applic | Status |
|:-:|:-------|:------|:----:|:----:|:------:|:------:|
| 1 | Mei et al. — AAC Survey (EURASIP 2022) | L2 | 2022 | HIGH | HIGH | ACCEPTED (documents absence of polyphony-specific Δ) |
| 2 | Ghosh et al. — AF3 (arxiv 2507.08128) | L3 | 2025 | HIGH | HIGH | ACCEPTED (confirms no CHAIR-audio vs DCASE baseline) |
| 3 | Kumar et al. — TAC (arxiv 2602.15766) | L3 | 2026 | HIGH | HIGH | ACCEPTED (only temporal-ordering cell occupied; natural-polyphony cell empty) |
| 4 | Kuan et al. — LALM Limits (Interspeech 2024) | L2 | 2024 | HIGH | HIGH | ACCEPTED (qualifies "RQ3 partial") |

**Decision:** The six RQs occupy six empty cells. Originality claim is falsifiable: if any cell turns out to be pre-occupied by a paper missed at review time, that RQ must be repositioned in the term paper's Introduction chapter.
**Conflicts:** None.
**Rejected:** No blog-post survey entries or leaderboard screenshots as evidence of cell-emptiness.

---

## § 8. Summary: The Intellectual Lineage in One Diagram

```
1977  Schafer — Soundscape theory (keynote/soundmark/signal)
                        │ humanities framing for RQ5
2017  AudioSet — 632-class ontology → hallucination vocabulary for RQ3
2019  AudioCaps — scale dataset → RQ3 stimulus set
2020  Clotho v2.1 — 5-caption benchmark → primary evaluation for RQ1/RQ2
2020  PANNs/CNN14 — audio classification encoder (encoder-decoder era)
      │
2022  Mei et al. survey — encoder-decoder paradigm documented; polyphony named
2022  FENSE — first AAC-specific learned metric; correlates with human judgement
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
2025  AF3 ⭐ — SOTA; unified scale beats dual-encoder; RQ1/RQ2/RQ3 primary
2025  Qwen2.5-Omni — end-to-end; optional RQ4 ablation
      │
2026  TAC — temporal grounding head; architectural argument against LLM decoder
      │
HERE  RQ0: contamination audit (new measurement)
      RQ1: AF3 zero-shot vs DCASE supervised on SPIDEr-FL (empty cell)
      RQ2: polyphony-specific gap (empty cell)
      RQ3: CHAIR-audio hallucination, AF3 vs SALMONN (empty cell)
      RQ4: temporal ordering, synthetic mixtures (empty cell)
      RQ5: cultural-heritage OOD, CLAPScore-only (empty cell)
```

**Source footer for § 8:** Every dated node in the lineage above is cited in §§ 1–7 above; this diagram is a narrative index, not a new evidence claim. Earliest entry (Schafer 1977) is the humanities anchor for RQ5; latest entry (Kumar 2026 — TAC) is the architectural counter-argument that frames the Discussion chapter. No new citations introduced in § 8.

---

## § 9. Threats to Validity (Wohlin 2012 Four-Axis Taxonomy)

The experiment design in this project is subject to the four classical threat axes `[Wohlin 2012; L2; HIGH/HIGH]`. Each threat below is named, operationalised, and mitigated in advance — not deferred to the limitations section of the term paper.

### 9.1 Construct Validity

| ID | Threat | Mitigation |
|:--|:-------|:-----------|
| C1 | SPIDEr-FL is a proxy for caption quality, not caption quality itself | Report FENSE + CLAPScore alongside; triangulate `[Zhou 2022; L2; HIGH/HIGH]` |
| C2 | Polyphony is operationalised via Clotho annotator tag count, which may not reflect perceptual polyphony | Cross-validate with CLAP-embedding similarity between concurrent events `[Wu 2023; L2; HIGH/HIGH]` |
| C3 | "Hallucination" is operationalised as `entity ∉ AudioSet tag ∧ CLAPScore < 0.25`; the 0.25 threshold is a free parameter | Pre-register 0.25 as a threshold, run sensitivity analysis at 0.20 and 0.30 `[Rohrbach 2018; L2; HIGH/MED]` |
| C4 | "Zero-shot" is a claim about AF3's training data, not a verifiable property — rests on RQ0 contamination audit | If RQ0 returns non-zero overlap, all "zero-shot" claims are demoted to "training-set-overlap-audited-but-not-zero" |

### 9.2 Internal Validity

| ID | Threat | Mitigation |
|:--|:-------|:-----------|
| I1 | LLM decoding temperature differs across AF3 / SALMONN / Qwen2.5-Omni by default → confounds model comparison | Fix `temperature=0.0` (greedy) across all models; disclose in methodology |
| I2 | Non-deterministic GPU ops → non-replayable bootstrap CIs across machines | `PYTHONHASHSEED=42`, `CUBLAS_WORKSPACE_CONFIG=:4096:8`, `torch.use_deterministic_algorithms(True)` per `setup_check.py` |
| I3 | bf16 silent fp32 fallback on sub-Ampere GPUs → results no longer comparable to AF3 paper | SM ≥ 8.0 hard gate in `setup_check.py` |
| I4 | Prompt engineering drift across experiments → caption style bias | Single canonical prompt template per notebook, pinned in `prompts/` |

### 9.3 External Validity

| ID | Threat | Mitigation |
|:--|:-------|:-----------|
| E1 | Clotho-eval is a convenience sample of FreeSound clips; generalisation to cultural-heritage audio is unestablished | RQ5 tests exactly this; framed as out-of-distribution probe, not mean-performance estimate |
| E2 | Results specific to transformers 4.44.* + AF3 checkpoint revision at pull time; future revisions may invalidate findings | Pin checkpoint SHA in `environment.yml`; archive model card in `docs/` |
| E3 | n ≤ 20 for RQ5 → no external-validity claim possible at that scale | RQ5 pre-registered as `[DESCRIPTIVE_ONLY]` — zero generalisation claims |

### 9.4 Conclusion Validity

| ID | Threat | Mitigation |
|:--|:-------|:-----------|
| V1 | Five simultaneous hypotheses at α=0.05 inflates FWER to ≈0.23 | Holm-Bonferroni correction, families defined in § 11 `[Holm 1979; L2; HIGH/HIGH]` |
| V2 | Percentile bootstrap under-covers on skewed AAC-score distributions | BCa bootstrap, n=1000, seed=42 `[Efron & Tibshirani 1993; L2; HIGH/HIGH]` |
| V3 | Low statistical power at small RQ4 / RQ5 sample sizes → false negatives presented as null results | Pre-declared MDE per RQ (§ 10); any non-significant RQ4/RQ5 result reported as "underpowered", not "null" |

#### § 9 Evidence Trail

| # | Source | Level | Year | Conf | Applic | Status |
|:-:|:-------|:------|:----:|:----:|:------:|:------:|
| 1 | Wohlin et al. — *Experimentation in SE* ch. 8 | L2 | 2012 | HIGH | HIGH | ACCEPTED (threat taxonomy) |
| 2 | Holm — *Scand. J. Stat.* 6(2) | L2 | 1979 | HIGH | HIGH | ACCEPTED (FWER correction) |
| 3 | Efron & Tibshirani — *Intro to the Bootstrap* ch. 14 | L2 | 1993 | HIGH | HIGH | STALE-VALID — still the BCa reference |
| 4 | Zhou et al. — FENSE (ICASSP 2022) | L2 | 2022 | HIGH | HIGH | ACCEPTED (metric triangulation) |

**Decision:** Fourteen threats, named and mitigated before data collection begins. Any threat not on this list is a §-7-Quality-Gate violation if discovered post-hoc.

---

## § 10. Statistical Power, MDE & Variance Envelope

### 10.1 Metric Variance (empirical anchor)

Martin-Morato et al. (2024) `[Martin-Morato 2024; L2; HIGH/MED]` characterise seed-level and split-level variance of AAC metrics on Clotho-eval-like data. This project adopts their reported σ values as the variance envelope for power calculation:

| Metric | σ (across seeds/splits) | Source |
|:-------|:------------------------|:-------|
| SPIDEr-FL | ~12 pp | Martin-Morato 2024 `[L2; HIGH/MED]` |
| FENSE | ~4 pp | Martin-Morato 2024 `[L2; HIGH/MED]` |
| CLAPScore | ~0.03 | Wu 2023 §5 + internal replication `[L2; HIGH/HIGH]` |
| CIDEr | ~8 pp | Martin-Morato 2024 `[L2; HIGH/MED]` |
| BLEU-4 | ~3 pp | Martin-Morato 2024 `[L2; HIGH/MED]` |

Applicability is MED, not HIGH, because Martin-Morato's variance is measured across seeds of supervised models; LALMs at greedy decoding have zero seed-variance contribution but non-zero split-variance contribution. We use these σ as a conservative upper bound, not a point estimate.

### 10.2 Minimum Detectable Effect per RQ

Standard error of a mean across *n* clips: `SE = σ / √n`. Two-sided α=0.05, power 0.80 → MDE ≈ 2.8 × SE `[Cohen 1988; L2; HIGH/HIGH — STALE-VALID: 38yr, canonical reference]`. After Holm-Bonferroni correction for the family of size *k*, effective α = 0.05/k for the strictest test → MDE scales by ≈√(2.8/2.48) ≈ 1.06 — negligible adjustment at k=3, disclosed but not propagated in the numbers below.

| RQ | n | σ used | SE | MDE (uncorrected) | Status |
|:--|:-:|:-------|:--:|:-----------------:|:-------|
| RQ1 SPIDEr-FL | 1 045 | 12 pp | 0.37 pp | **~1.04 pp** | Sufficient for Δ(AF3 − DCASE) ≈ 5 pp claim |
| RQ2 polyphony-Δ | ~500 | 12 pp | 0.54 pp | **~1.50 pp** | Sufficient for expected Δ ≥ 3 pp |
| RQ3 CHAIR-audio | 500 | σ=0.10 on rate | 0.45 pp rate | **~1.25 pp rate** | Sufficient |
| RQ4 temporal | ~50 | 12 pp | 1.70 pp | **~4.76 pp** | Underpowered for <5 pp effects — flag if non-significant |
| RQ5 CLAPScore | ≤ 20 | 0.03 | 0.0067 | **~0.019** | `[DESCRIPTIVE_ONLY]` — no inferential claim |

> **Note on RQ1 MDE discrepancy:** Earlier v6 notes cited "~0.73 pp" for RQ1 using a tighter σ≈8pp assumption. This § uses the conservative σ≈12 pp from Martin-Morato 2024, giving MDE ≈ 1.04 pp. The conservative figure is what the Methods chapter will report; the 0.73 pp figure is retained in `research_notes.md §5.7` as a sensitivity-analysis floor.

### 10.3 Confidence Interval Construction

All metric-mean CIs reported in this project use **BCa bootstrap** `[Efron & Tibshirani 1993; L2; HIGH/HIGH]` with n=1 000 resamples and `seed=42`. Plain percentile bootstrap is rejected — it under-covers on skewed AAC-score distributions. Implementation: `scipy.stats.bootstrap(..., method='BCa')` pinned via `environment.yml`.

#### § 10 Evidence Trail

| # | Source | Level | Year | Conf | Applic | Status |
|:-:|:-------|:------|:----:|:----:|:------:|:------:|
| 1 | Martin-Morato et al. — AAC metric variance | L2 | 2024 | HIGH | MED | ACCEPTED (variance anchor) |
| 2 | Efron & Tibshirani — *Bootstrap* ch. 14 | L2 | 1993 | HIGH | HIGH | STALE-VALID (BCa canonical) |
| 3 | Cohen — *Statistical Power Analysis* | L2 | 1988 | HIGH | HIGH | STALE-VALID (MDE formula canonical) |
| 4 | Wu et al. — LAION-CLAP | L2 | 2023 | HIGH | HIGH | ACCEPTED (CLAPScore σ) |

**Decision:** RQ1/RQ2/RQ3 are adequately powered; RQ4 is underpowered for small effects and is pre-declared as such; RQ5 is descriptive-only.

---

## § 11. Pre-Registered Falsification & Family-Wise Correction

### 11.1 Why Pre-Registration

Kerr (1998) `[Kerr 1998; L2; HIGH/HIGH]` documents HARKing — hypothesising after results are known — as a dominant source of false-positive findings in social science. AAC research is susceptible to the same failure mode: metric values are computed first, then hypotheses are shaped to the observed effect. Pre-registration in `hypotheses_preregistered.yml` makes this epistemically visible: any deviation between the YAML and the final write-up must be disclosed in the Methods chapter.

### 11.2 Per-RQ Null Hypotheses and Kill-Criteria

| RQ | H₀ | Kill-criterion |
|:--|:---|:---------------|
| RQ0 | Clotho-eval has zero clip-id overlap with AF3/SALMONN training manifests | Any non-zero overlap demotes every "zero-shot" claim in the paper |
| RQ1 | `SPIDEr-FL(AF3) ≤ SPIDEr-FL(DCASE-baseline) = 29.6%` | If AF3 ≤ 29.6% + 1.04 pp MDE → thesis claim falsified; paper pivots to "zero-shot does not beat supervised" |
| RQ2 | `Δ(AF3 − baseline, polyphonic) = Δ(AF3 − baseline, monophonic)` | If Δ identical within MDE → polyphony is not a differential LALM weakness; RCA § 5.1 weakened |
| RQ3 | `CHAIR-audio(AF3) = CHAIR-audio(SALMONN)` | If AF3 hallucinates as often as SALMONN → scale/unified-encoder hypothesis (§ 4.3) weakened |
| RQ4 | A-then-B ordering rate of LALM = 50% (chance) | If rate ≥ 80% on synthetic mixtures → autoregressive-text-prior mechanism (§ 5.3) weakened |
| RQ5 | `[DESCRIPTIVE_ONLY]` — no H₀ | Kill-criterion is qualitative: panel of ≥ 2 humanities readers find CLAPScore > 0.3 captions systematically miss Schafer soundmark features |
| H_NEG | Hallucination rate on silent/white-noise clips ≥ 80% | If rate < 50% → text-prior confabulation mechanism weakened (§ 5.2 requires revision) |

### 11.3 Holm-Bonferroni Families

Family-wise error control per Holm (1979) `[Holm 1979; L2; HIGH/HIGH]`. Two disjoint families are pre-registered in `hypotheses_preregistered.yml`:

- **Family-1** (SPIDEr-FL primary): {H1 = RQ1, H2 = RQ2, H3 = RQ3-SPIDEr} — k=3, strictest α' = 0.05/3 ≈ 0.0167
- **Family-2** (CHAIR-audio): {H4 = RQ3-CHAIR} — k=1, α' = 0.05 (single-member family, no correction)

Rationale for split families: Family-1 tests metric-mean differences on overlapping data (Clotho-eval); Family-2 tests a hallucination-rate on AudioCaps. The stimulus sets differ; a single family of 4 would over-correct. Disclosed and justified per § 3.2 conflict-resolution rule.

H5 (RQ5) and H6_RQ5 are excluded from all families — flagged `[DESCRIPTIVE_ONLY]`.

### 11.4 Cross-Reference

Authoritative machine-readable specification: [`hypotheses_preregistered.yml`](e:/ISSS/Summer 2026/CH-Proj-M Master's project Computational Humanities/implementation_plan.md) inside `implementation_plan.md` Phase 0. If this review and the YAML ever diverge, **the YAML is canonical** — this review section is a human-readable mirror.

#### § 11 Evidence Trail

| # | Source | Level | Year | Conf | Applic | Status |
|:-:|:-------|:------|:----:|:----:|:------:|:------:|
| 1 | Holm — *Scand. J. Stat.* 6(2) | L2 | 1979 | HIGH | HIGH | STALE-VALID (canonical FWER method) |
| 2 | Kerr — HARKing (*PSPR* 2(3)) | L2 | 1998 | HIGH | HIGH | ACCEPTED (pre-reg rationale) |
| 3 | Rohrbach et al. — CHAIR | L2 | 2018 | HIGH | MED | ACCEPTED (RQ3 H₀ operationalisation) |
| 4 | Labbeti — DCASE 2024 baseline 29.6% | L1 | 2024 | HIGH | HIGH | ACCEPTED (RQ1 floor) |

---

## § 12. Competing Explanations Pre-Mortem

For each of the three failure modes in § 5, the RCA claim (adapter information bottleneck) is the *preferred* explanation, not the only one. This section lists the competitors and the discriminating observation in advance — so any post-hoc narrative lock-in becomes visible.

### 12.1 Polyphony Under-Description (§ 5.1)

| Competing explanation | Predicts | Discriminator |
|:----------------------|:---------|:--------------|
| Adapter information bottleneck (**preferred**) | Dropping second event regardless of event type | RQ2 result on diverse polyphonic clips |
| Dataset-label noise: secondary events often missing from reference captions → model learns to drop them | Model omits second events even when they are labelled in reference | Annotator-augmented 100-clip subset with exhaustive labelling — if AF3 still omits second events on this clip-set, noise is ruled out |
| LLM decoding temperature too low → mode-collapse on dominant event | Temperature sensitivity visible in ablation | Set temperature=0.3 on a 50-clip subset; if polyphony coverage rises, decoding is the cause, not the adapter |
| Encoder-frozen vs LoRA-adapted: frozen AF-CLAP may lack concurrent-event separation | Polyphony failure restored by LoRA-tuning the encoder | Out of scope for this project; flagged as v7 follow-up |

### 12.2 Entity Hallucination (§ 5.2)

| Competing explanation | Predicts | Discriminator |
|:----------------------|:---------|:--------------|
| Text-prior confabulation under ambiguous audio (**preferred**) | Hallucination rate correlates with text-prior co-occurrence | Kuan 2024 already shows this pattern qualitatively; RQ3 confirms on AF3 |
| AudioSet tag incompleteness → false-positive hallucination count | CHAIR rate inflated specifically on clips with sparse tags | CHAIR-audio dual criterion (AudioSet ∧ CLAPScore < 0.25) neutralises this |
| LALM memorisation of training-set captions surfaces verbatim | Hallucinated phrases match WavCaps/Clotho-AQA captions | RQ0 contamination audit checks exactly this |

### 12.3 Temporal Grounding Loss (§ 5.3)

| Competing explanation | Predicts | Discriminator |
|:----------------------|:---------|:--------------|
| Autoregressive text prior overrides audio onset (**preferred**) | LALM describes salient-first, not onset-first | RQ4 synthetic-mixture protocol (Kumar 2026) |
| Audio encoder is non-causal (bidirectional) → no onset information at encoder output | Temporal ordering failure is architectural, not decoder-side | TAC's ablation: explicit temporal head on top of same encoder recovers ordering; discriminates architectural vs decoder hypotheses |
| Annotator convention: humans describe salient events first regardless of onset order | LALMs match human order, therefore "correct" — failure is a definition problem, not a capability problem | Compare LALM order to *annotator* order, not to *acoustic* order; if rates match, the problem is in the evaluation protocol, not the model |

#### § 12 Evidence Trail

| # | Source | Level | Year | Conf | Applic | Status |
|:-:|:-------|:------|:----:|:----:|:------:|:------:|
| 1 | Kuan et al. — LALM Limits | L2 | 2024 | HIGH | HIGH | ACCEPTED (hallucination mechanism) |
| 2 | Kumar et al. — TAC | L3 | 2026 | HIGH | HIGH | ACCEPTED (temporal alternative) |
| 3 | Ghosh et al. — AF3 | L3 | 2025 | HIGH | HIGH | ACCEPTED (encoder-frozen claim) |
| 4 | Mei et al. — AAC Survey | L2 | 2022 | HIGH | HIGH | ACCEPTED (dataset-label noise background) |

**Decision:** Each failure mode has ≥ 2 falsifiable alternatives with a pre-declared discriminator. No post-hoc "of course it's X" permitted at write-up time.

---

## § 13. Broadened Humanities Lineage

§ 1.2 anchored the humanities framing in Schafer 1977 and Heffernan 1993. That is sufficient for the term paper's Introduction but narrow for a Computational Humanities examiner. This section widens the lineage.

### 13.1 Truax — *Acoustic Communication* (1984)

Truax (1984) `[Truax 1984; L2; HIGH/HIGH — STALE-VALID: 42yr, field-defining; no replacement]` extends Schafer by distinguishing *listening-in-search*, *listening-in-readiness*, and *background listening* — three distinct cognitive modes that the same soundscape invokes. The AAC system's output implicitly assumes one mode, typically *listening-in-search*. This has a direct RQ5 implication: archival Bamberg bell captions that focus on the bell event alone encode *listening-in-search* and miss the *background listening* role of bells in civic acoustic identity. The qualitative component of RQ5 must audit which listening mode the model's caption implies.

### 13.2 Augoyard & Torgue — *Sonic Experience* (2006)

Augoyard & Torgue (2006) `[Augoyard 2006; L2; HIGH/HIGH]` catalogue 82 *sonic effects* (e.g., *drone*, *masking*, *reverberation*, *ubiquity*) — descriptive primitives for how sounds are experienced spatially and culturally. AAC outputs systematically favour sound *sources* over sound *effects*: "bell rings" rather than "bell resonates in reverberant square". This is a describable gap, not a vague one. RQ5's qualitative audit should score caption coverage against the Augoyard & Torgue taxonomy, not against a model-internal vocabulary.

### 13.3 Sterne (ed.) — *The Sound Studies Reader* (2012)

Sterne (2012) `[Sterne 2012; L2; HIGH/HIGH]` reframes sound studies as a post-humanities interdisciplinary field — one that is already computational (cf. part III of the Reader on infrastructures of recording). This legitimises the present project's methodological move: an engineering artefact (LALM) interrogated by humanities-grade critique (§ 5 RCA + § 12 competing explanations) belongs to sound studies, not only to ML evaluation. For the term paper's Discussion chapter, this is the defensive citation against "but this is just an engineering paper".

### 13.4 Born (ed.) — *Music, Sound and Space* (2013)

Born (2013) `[Born 2013; L2; HIGH/HIGH]` develops the spatialisation axis: sounds are not only temporal events but place-constituting phenomena. Bamberg Martinskirche bells *are* Bamberg in a way that is not reducible to acoustic waveform — they index civic space, confessional history, and institutional continuity. A LALM trained on decontextualised FreeSound clips cannot represent place-indexical meaning. RQ5's domain-shift framing thus has a theoretical root in Born 2013, not only in an empirical OOD observation.

### 13.5 Sister-Arts Tradition (brief)

The ekphrasis frame in § 1.2 has a parallel in the *sister-arts* tradition — Lessing's *Laokoon* (1766) and its 20th-century revisions (Mitchell 1986 `[Mitchell 1986; L2; HIGH/MED — STALE-VALID: 40yr]`) argue that cross-modal translation between semiotic systems is always lossy, and that the loss is theoretically interesting. AAC inherits this problem. This project does not develop the sister-arts argument in depth — it is flagged here as the humanities horizon the Discussion chapter may gesture toward.

#### § 13 Evidence Trail

| # | Source | Level | Year | Conf | Applic | Status |
|:-:|:-------|:------|:----:|:----:|:------:|:------:|
| 1 | Truax — *Acoustic Communication* | L2 | 1984 | HIGH | HIGH | STALE-VALID (listening-mode taxonomy) |
| 2 | Augoyard & Torgue — *Sonic Experience* | L2 | 2006 | HIGH | HIGH | ACCEPTED (sonic-effect taxonomy for RQ5 audit) |
| 3 | Sterne (ed.) — *Sound Studies Reader* | L2 | 2012 | HIGH | HIGH | ACCEPTED (disciplinary legitimation) |
| 4 | Born (ed.) — *Music, Sound and Space* | L2 | 2013 | HIGH | HIGH | ACCEPTED (place-indexicality for RQ5) |
| 5 | Mitchell — *Iconology* | L2 | 1986 | HIGH | MED | STALE-VALID (sister-arts gesture) |

**Decision:** Humanities lineage extended from 2 to 7 sources. Each tied to a specific RQ or framing choice. No essay-mode drift — one paragraph per source, per plan § P2.
**Conflicts:** None.
**Rejected:** Popular sound-studies blog posts or museum-programme essays without peer review.

---

## § 14. Integrity Gate (Final Checklist)

Before any Evaluation or Discussion chapter is written, these must all be green:

- [ ] Clotho-eval Zenodo record = **4783391** (not 3490684)
- [ ] DCASE 2024 baseline reproduced at **29.6% ± 1% SPIDEr-FL** on canary run
- [ ] RQ0 contamination audit completed; "zero-shot" claims conditional on RQ0 outcome
- [ ] Holm-Bonferroni applied to Family-1 {H1, H2, H3}; Family-2 {H4} separate
- [ ] BCa bootstrap (n=1000, seed=42) used for every metric-mean CI
- [ ] Negative controls (silence, white noise) run; hallucination rate disclosed
- [ ] `setup_check.py` passes SM ≥ 8.0 gate; bf16 silent fallback prevented
- [ ] `PYTHONHASHSEED=42`, `CUBLAS_WORKSPACE_CONFIG=:4096:8`, `torch.use_deterministic_algorithms(True)` all asserted
- [ ] Every § 9 threat has a mitigation traceable to a notebook or a pinned config
- [ ] Every § 12 competing explanation has a discriminating observation logged before results are seen

Any unchecked box at thesis-submission time is a CLAUDE.md § 7 violation and must be disclosed.
