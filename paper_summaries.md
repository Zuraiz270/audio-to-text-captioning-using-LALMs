# Paper Summaries (Definitive Merged) — T6: Audio-to-Text Captioning
*Master's Project · CH-Proj-M · SS 2026 · Zuraiz (2177213)*
*Merges: Antigravity v5 (reading template) + Claude Code v6 (critical appraisal layer)*

> **How to use.** For each paper: fill in `[YOUR NOTES]` after reading. The pre-filled sections are verified against primary sources. The critical appraisal section (Threat / Conf-Applic / Reservation) trains you to cite each paper *as a reviewer*, not a fan.

> **Tier convention.**
> - **TIER 1** — read before Phase 1 (May 4): Drossos 2020, Mei 2022, Labbeti 2024, AF3, Kuan 2024, Schafer 1977
> - **TIER 2** — read before Phase 2 (May 18): SALMONN, FENSE, CLAP, CHAIR, TAC
> - **TIER 3** — reference / supplementary: Gemmeke 2017, AudioCaps, AF2, Qwen, Holm, Efron

---

## Paper 1 — Drossos 2020 — Clotho: An Audio Captioning Dataset

- **Venue / Level**: ICASSP 2020 · **L2**
- **Links**: arXiv 1910.09387 · Zenodo **4783391** (v2.1 — use this one, NOT 3490684)
- **Tier**: 1 · ~45 min

**What it claims:**
> The first purpose-built AAC benchmark with 5 human-written captions per clip and an annotation protocol that focuses strictly on *what is heard*, eliminating visual-inference bias.

**How it works (method):**
- 6,974 FreeSound clips (CC-licensed, 15–30s)
- Five independent AMT crowdsourcers per clip with bespoke instructions: *"describe what you hear, not what you imagine"*
- Dev / Val / Eval / Test splits designed to prevent category leakage

**Key numbers:**
- 6,974 clips × 5 captions = 34,870 annotations
- Evaluation split: **1,045 clips** — the exclusive benchmark for RQ1/RQ2/RQ3
- DCASE 2024 Task 6 uses this as the official evaluation set

**What it means for us:**
- RQ1/RQ2/RQ3: primary evaluation. Every SPIDEr-FL number refers to Clotho-eval.
- RQ0: clip filenames encode FreeSound IDs → fingerprint for contamination audit
- Five-caption design: CHAIR-audio noun absent from all 5 references AND CLAPScore < 0.25 → hallucinated

**Threat to validity (dominant: Construct):**  
"Acoustic focus" instruction cannot be empirically verified — some captions contain inferred content ("people in a restaurant") beyond pure acoustic description. Affects metric validity against references.

**Confidence / Applicability:** HIGH / HIGH — canonical source, same domain.

**One-sentence reservation:**  
Do not cite Drossos 2020 for annotation *accuracy* — inter-annotator agreement on event *identification* was never measured.

**One quote:**
> *"Audio captioning is the novel task of general audio content description using free text. It is an intermodal translation task."*

**[YOUR NOTES — fill in after reading]:**

---

## Paper 2 — Gemmeke 2017 — AudioSet: An Ontology and Human-Labeled Dataset

- **Venue / Level**: ICASSP 2017 · **L2**
- **Link**: DOI 10.1109/ICASSP.2017.7952261
- **Tier**: 3 · ~30 min

**What it claims:**
> A hierarchical ontology of 632 everyday sound classes plus 2.1M weakly-labelled YouTube clips — the universal vocabulary for audio event understanding.

**How it works (method):**
- Expert-curated 7-category hierarchy (Human, Animal, Music, Natural, Vehicle, …) → 632 leaf classes
- Clip-level (weak) labels, not frame-level — annotators confirm "this class is present somewhere in the 10s clip"
- 2.084M labelled clips

**Key numbers:**
- 632 classes — the hallucination vocabulary for CHAIR-audio (RQ3)
- Clip-level labels: weaker ground truth than frame-level (relevant for C1 threat)

**What it means for us:**
- RQ3: 632-class ontology = vocabulary for extracting nouns and checking hallucination
- RQ0: AudioSetCaps is derived from AudioSet → contamination manifest

**Threat to validity (dominant: Internal):**  
Rater agreement is moderate (κ ≈ 0.5 on some subsets per Google follow-up); audible events are systematically un-tagged. Inflates false-positive hallucination counts → motivates the CLAPScore dual criterion.

**Confidence / Applicability:** HIGH / HIGH — canonical ontology, no replacement.

**One-sentence reservation:**  
Do not cite AudioSet labels as complete ground truth — use as lower bound; cross-check with CLAPScore (dual-criterion hallucination).

**[YOUR NOTES — fill in after reading]:**

---

## Paper 3 — Kim 2019 — AudioCaps: Generating Captions for Audios in the Wild

- **Venue / Level**: NAACL 2019 · **L2**
- **Link**: audiocaps.github.io
- **Tier**: 3 · ~30 min

**What it claims:**
> The first large-scale (46k clip) audio captioning dataset derived from AudioSet with human-written captions, enabling scale-up research.

**How it works (method):**
- ~46k AudioSet YouTube clips (10s each) × 1 crowdsourced caption
- AMT task: *describe events* (different from Clotho's *describe what you hear*)
- Single caption per clip — a cost-scale trade-off

**Key numbers:**
- ~46,000 clips × 1 caption
- AudioSet tags available per clip → ground truth for CHAIR-audio

**What it means for us:**
- RQ3 only: stimulus set for hallucination experiment (single-event clips via AudioSet tag count = 1)
- NOT used for primary metric reporting (single caption → metric variance annotator-dominated)

**Threat to validity (dominant: Construct):**  
Single-caption SPIDEr-FL on AudioCaps is annotator-dominated; results are not comparable to Clotho-eval multi-reference SPIDEr-FL.

**Confidence / Applicability:** HIGH / HIGH for RQ3 stimulus; HIGH / LOW for primary metric.

**One-sentence reservation:**  
Do not report SPIDEr-FL on AudioCaps as the headline — single reference violates the metric's assumed condition.

**[YOUR NOTES — fill in after reading]:**

---

## Paper 4 — Mei 2022 — Automated Audio Captioning: An Overview

- **Venue / Level**: EURASIP JASMP 2022 · **L2**
- **Link**: arXiv 2205.05949
- **Tier**: 1 · ~1.5 hrs

**What it claims:**
> A comprehensive survey of 50+ AAC papers (2017–2022) documenting the convergence on encoder-decoder architecture and naming polyphony as the dominant open challenge.

**How it works (method):**
- Taxonomy: encoder (CNN/Transformer) × decoder (RNN/Transformer) × training regime
- Systematic metric comparison
- Forward-looking open-challenges section

**Key numbers:**
- 50+ papers surveyed
- Field converged by 2021 on CNN14/PANNs encoder + Transformer decoder
- Polyphony explicitly named as un-solved

**What it means for us:**
- RQ1: provides historical baseline context — where the field was before LALMs
- RQ2: explicitly names the polyphony problem we study

**Threat to validity (dominant: External):**  
Survey is bounded at 2022; any post-2022 architectural shift (LALMs) is not covered. Cite for the pre-LALM era only.

**Confidence / Applicability:** HIGH / MED — authoritative for its era; survey scope excludes LALMs.

**One-sentence reservation:**  
Do not cite Mei 2022 for current-practice claims about LALMs — the paper predates them.

**One quote:**
> *"The inability to handle polyphonic audio scenes — clips containing multiple simultaneous sound events — remains one of the key open challenges in automated audio captioning."*

**[YOUR NOTES — fill in after reading]:**

---

## Paper 5 — Labbeti 2024 — DCASE 2024 Task 6 Baseline

- **Venue / Level**: DCASE 2024 technical report (official baseline) · **L1**
- **Links**: github.com/Labbeti/dcase2024-task6-baseline · dcase.community
- **Tier**: 1 · ~30 min + time to run it

**What it claims:**
> A publicly reproducible supervised AAC baseline achieving **29.6% SPIDEr-FL** on Clotho-eval — the comparison floor for all experiments.

**How it works (method):**
- **Encoder**: ConvNeXt pretrained for audio classification → frame-level log-mel embeddings
- **Decoder**: Transformer seq2seq with cross-attention
- **Training**: Supervised on Clotho; no LLM, no foundation model
- **Evaluation**: `aac-metrics` (the only valid implementation for DCASE-comparable numbers)

**Key numbers:**
- **29.6% SPIDEr-FL on Clotho-eval** ← The single most important number in the whole project
- This is the floor AF3 must exceed for RQ1 H1 to stand

**What it means for us:**
- RQ1: the comparison floor. Phase 2.0.0 canary: reproduce 29.6% ±1% before any LALM evaluation. If canary fails → metric pipeline is broken → nothing else is valid.

**Threat to validity (dominant: Conclusion):**  
Single training run; seed variance not reported. The canary reproduction implicitly tests whether seed variance dominates the quoted number.

**Confidence / Applicability:** HIGH / HIGH — L1 official baseline with public code.

**One-sentence reservation:**  
Do not cite 29.6% as an upper bound on supervised AAC — DCASE challenge winners (ensemble systems) score higher; 29.6% is the reproducible single-run floor.

**[YOUR NOTES — fill in after reading]:**

---

## Paper 6 — Tang 2023 — SALMONN: Generic Hearing Abilities for LLMs

- **Venue / Level**: ICLR 2024 · **L2**
- **Links**: arXiv 2310.13289 · github.com/bytedance/SALMONN
- **Tier**: 2 · ~1 hr

**What it claims:**
> The first LALM with generic hearing ability — simultaneously competent on speech, music, and environmental audio — via a dual audio encoder bridging to a 13B LLM.

**How it works (method):**
```
Waveform → [Whisper-Large-v2 (680k hrs speech)] ─┐
                                                   ├→ [Window-level Q-Former] → [Vicuna-13B]
Waveform → [BEATs (AudioSet events)]            ─┘
```
Whisper captures phonemic/prosodic structure; BEATs captures environmental events. Q-Former bridges both to the LLM token space.

**Key numbers:**
- 13B parameters; ~24GB bf16 / ~14GB int4
- First published LALM with zero-shot Clotho-style captioning

**What it means for us:**
- RQ1: historical LALM baseline
- RQ2: dual encoder was *designed* to separate speech from events — our test of whether this handles *within-domain concurrent events* (two environmental sounds co-occurring)

**Threat to validity (dominant: Construct):**  
"Generic hearing abilities" evaluated on curated benchmarks not including Clotho-eval SPIDEr-FL. The claim is partially constructed by benchmark selection. RQ1 supplies independent evaluation.

**Confidence / Applicability:** HIGH / MED — peer-reviewed ICLR, but architecture superseded by AF3.

**One-sentence reservation:**  
Do not cite SALMONN as current SOTA LALM — Ghosh 2025b explicitly supersedes it on all major benchmarks.

**[YOUR NOTES — fill in after reading]:**

---

## Paper 7 — Ghosh 2025a — Audio Flamingo 2 (AF2)

- **Venue / Level**: NVIDIA preprint · **L3**
- **Link**: arXiv 2503.03983
- **Tier**: 3 · ~45 min

**What it claims:**
> Introduces the AF-CLAP unified audio encoder (replacing dual-encoder designs) and long-audio capability (multi-minute clips) via sparse attention.

**How it works (method):**
- AF-CLAP: custom contrastive pretraining on speech + events + music mixed corpus simultaneously
- Sparse attention for long-context processing
- 3B and 7B LLM variants

**Key numbers:**
- AF-CLAP encoder carried forward into AF3 unchanged
- Long-audio benchmarks (MusicQA-long, ClothoAQA-long)

**What it means for us:**
- Architectural context for AF3; cite when introducing the AF-CLAP encoder in methodology
- The abandonment of dual-encoder is the architectural argument: scale + unified > specialised + combined

**Threat to validity (dominant: External):**  
L3 preprint, single-institution (NVIDIA), no independent replication as of April 2026.

**Confidence / Applicability:** HIGH / HIGH despite L3 — public code, no contradicting evidence.

**One-sentence reservation:**  
Do not cite AF2 as the primary model — AF3 supersedes it; AF2 is cited only for architectural lineage.

**[YOUR NOTES — fill in after reading]:**

---

## Paper 8 — Ghosh 2025b — Audio Flamingo 3 (AF3) ⭐ PRIMARY MODEL

- **Venue / Level**: NVIDIA preprint · **L3**
- **Links**: arXiv 2507.08128 · huggingface.co/nvidia/audio-flamingo-3
- **Tier**: 1 · ~1.5 hrs (read every section; pay special attention to training data for RQ0)

**What it claims:**
> SOTA open-source LALM surpassing all prior open and closed models (GPT-4o-audio, Gemini Pro v2.5) on all major audio understanding benchmarks, while being fully open-source.

**How it works (method):**
```
Audio → [AF-CLAP unified encoder] → [Adapter] → [8B LLM] → Caption/Answer
```
Trained on a mixed corpus — **read the data card on HuggingFace for RQ0 contamination audit**.

**Key numbers:**

| Benchmark | AF3 Score |
|:----------|:---------:|
| MMAU | 72.28 |
| ClothoAQA | 91.1% |
| CMM-Hallucination | **86.7%** ← means 13.3% still hallucinated |
| Clotho-Entailment | 92.9% |

**What it means for us:**
- RQ0, RQ1, RQ2, RQ3, RQ4: primary model under study
- 86.7% CMM-Hallucination accuracy means 13.3% failure rate on a *controlled* benchmark → expect higher on uncontrolled Clotho clips

**Threat to validity (dominant: Internal — DATA CONTAMINATION):**  
Training corpus includes AudioSetCaps and WavCaps, both derived from the same FreeSound/AudioSet upstream as Clotho-eval. The "zero-shot" framing is a claim RQ0 tests — not a premise to accept.

**Confidence / Applicability:** HIGH / HIGH — institutionally backed, code public, direct subject of this project.

**One-sentence reservation:**  
Do not cite AF3's benchmark numbers as zero-shot capability without qualifying by the RQ0 audit result.

> [!IMPORTANT]
> When you read this paper: note every training dataset mentioned in §3 (Training Data) and the HuggingFace data card. Write the list in [YOUR NOTES]. This is the RQ0 input.

**[YOUR NOTES — fill in after reading; CRITICAL: list all training datasets]:**

---

## Paper 9 — Qwen Team 2025 — Qwen2.5-Omni

- **Venue / Level**: Alibaba preprint · **L3**
- **Link**: arXiv 2503.20215 · github.com/QwenLM/Qwen2.5-Omni
- **Tier**: 3 · ~45 min

**What it claims:**
> End-to-end multimodal model (text + audio + image + video) with streaming output — a different architectural bet from AF3's audio-language specialisation.

**Key numbers:**
- Apache-2.0 licence = lowest legal risk of all models in this project
- Competitive with AF3 on several audio benchmarks

**What it means for us:**
- RQ4 optional ablation: if AF3 and Qwen2.5-Omni show the same failure pattern → finding is LALM-general, not AF3-specific

**Threat to validity (dominant: Construct):**  
Multimodal benchmarks often reduce to text-heavy reasoning; genuine audio-specific grounding is undermeasured.

**Confidence / Applicability:** HIGH / HIGH — Apache-2.0 is the lowest legal risk.

**One-sentence reservation:**  
Do not cite Qwen2.5-Omni's overall multimodal scores as evidence of audio capability specifically.

**[YOUR NOTES — fill in after reading]:**

---

## Paper 10 — Kuan 2024 — Understanding Sounds, Missing the Questions

- **Venue / Level**: Interspeech 2024 · **L2**
- **Links**: isca-archive.org/interspeech_2024/kuan24_interspeech.pdf · github.com/kuan2jiu99/audio-hallucination
- **Tier**: 1 · ~45 min

**What it claims:**
> LALM hallucination is a *language-prior failure*, not an audio-perception failure: models confabulate sounds that co-occur frequently in natural language even when those sounds are absent from the audio.

**How it works (method):**
- Controlled stimuli: audio with expected co-occurring sounds (high text-prior confabulation risk) vs. unexpected sounds (low text-prior, high perception demand)
- Compares false-positive hallucination rate across SALMONN and contemporaries
- Finding: hallucination rate correlates with text-prior co-occurrence frequency, not acoustic presence

**Key numbers:**
- First systematic measurement of hallucination in LALMs
- Mechanism confirmed: text prior > audio evidence in LLM generation

**What it means for us:**
- RQ3: foundational motivation; mechanism is why we expect CHAIR-audio to find non-zero rate even on AF3
- Framing: hallucination = *computational anamnesis* (Augoyard 2006 term)

**Threat to validity (dominant: External):**  
Stimuli set is small and curated; generalisation to natural uncurated Clotho clips is a conjecture. RQ3 is exactly that replication at scale.

**Confidence / Applicability:** HIGH / HIGH — peer-reviewed Interspeech, direct relevance.

**One-sentence reservation:**  
Do not cite Kuan 2024's hallucination rates as AF3 numbers — the study predates AF3 and measured different LALMs.

**One quote:**
> *"LALMs generate descriptions that include sounds not present in the input audio, driven by the LLM's language prior rather than acoustic evidence."*

**[YOUR NOTES — fill in after reading]:**

---

## Paper 11 — Kumar 2026 — TAC: Timestamped Audio Captioning

- **Venue / Level**: Adobe Research / Northwestern preprint · **L3**
- **Links**: arXiv 2602.15766 · sonalkum.github.io/tacmodel
- **Tier**: 2 · ~1 hr

**What it claims:**
> LALMs describe events in canonical text-prior order rather than actual acoustic onset order, and hallucinate frequently on overlapping events. TAC resolves this via an explicit temporal grounding head and synthetic-mixture training.

**How it works (method):**
- **Synthetic-mixture pipeline**: clean single-event clips mixed at known onset/offset times → polyphonic training data with ground-truth temporal labels
- **Temporal grounding head**: predicts onset/offset timestamps *separately* from the caption generator; bypasses autoregressive ordering bias
- Output format: *"At 2.1s, a dog begins to bark. At 5.4s, a car horn overlaps."*

**What it means for us:**
- RQ4: TAC is the method we replicate for the synthetic-mixture experiments; cite as oracle
- The architectural argument: LLM autoregressive decoder is fundamentally mismatched for temporal structure → separate grounding head is the fix → this is the Discussion chapter's claim

**Threat to validity (dominant: External):**  
Synthetic mixtures have acoustically sharper onsets than natural polyphony; TAC's advantage may not transfer. RQ4 mitigates by cross-testing on natural polyphonic Clotho clips.

**Confidence / Applicability:** HIGH / HIGH — recent, directly relevant, well-designed.

**One-sentence reservation:**  
Do not cite TAC as evidence of natural-polyphony superiority — results are on synthetic data; natural-clip generalisation is an open question RQ4 addresses.

**One quote:**
> *"Large Audio Language Models struggle to disentangle overlapping events in complex acoustic scenes, yielding temporally inconsistent captions and frequent hallucinations."*

**[YOUR NOTES — fill in after reading]:**

---

## Paper S1 — Zhou 2022 — FENSE

- **Venue / Level**: ICASSP 2022 · **L2**
- **Link**: arXiv 2110.04684
- **Tier**: 2 · ~30 min

**What it claims:**
> Image-caption metrics transfer poorly to audio captioning. FENSE (SentenceBERT similarity × Fluency Error Penalty) achieves the highest correlation with human quality judgement among all tested metrics.

**Key numbers:**
- FENSE highest human-correlation; BLEU/ROUGE/METEOR weakest
- `pip install fense`; requires reference captions (undefined for RQ5 archival audio)

**Threat to validity (dominant: Construct):**  
"Human judgement" pool is small, English-only, demographics unreported. High correlation ≠ domain validity across cultures.

**Confidence / Applicability:** HIGH / HIGH — peer-reviewed, direct relevance.

**One-sentence reservation:**  
Do not cite FENSE as reference-free — it requires human references and is undefined on RQ5 archival audio.

**[YOUR NOTES — fill in after reading]:**

---

## Paper S2 — Wu 2023 — LAION-CLAP

- **Venue / Level**: ICASSP 2023 · **L2**
- **Link**: github.com/LAION-AI/CLAP
- **Tier**: 2 · ~30 min

**What it claims:**
> An open-source contrastive audio-language model trained at CLIP-equivalent scale, enabling CLAPScore — the only reference-free quality metric for audio captioning.

**Key numbers:**
- CLAPScore = cosine_similarity(CLAP_audio(audio), CLAP_text(caption))
- No human references required → non-negotiable for RQ5

**Threat to validity (dominant: External):**  
Training corpus is web-scraped; likely under-represents archival Germanic audio (Bamberg bells). RQ5 CLAPScore must be triangulated with qualitative Schafer-taxonomy analysis.

**Confidence / Applicability:** HIGH / HIGH for RQ5; HIGH / MED specifically on archival audio.

**One-sentence reservation:**  
Do not report CLAPScore on archival Germanic audio without explicitly disclosing the training-domain mismatch.

**[YOUR NOTES — fill in after reading]:**

---

## Paper S3 — Rohrbach 2018 — CHAIR

- **Venue / Level**: EMNLP 2018 · **L2**
- **Link**: ACL Anthology D18-1437
- **Tier**: 2 · ~30 min

**What it claims:**
> Image captioning models hallucinate objects at 5–20%; CHAIR (Caption Hallucination Assessment with Image Relevance) measures this systematically using segmentation-mask ground truth.

**Key numbers:**
- CHAIR_i = |hallucinated objects| / |all mentioned objects|
- Modern image captioners: 5–20% hallucination rate

**Adaptation for audio (CHAIR-audio, this project):**
```
hallucinated iff: (a) entity ∉ AudioSet tags  AND  (b) CLAPScore < 0.25
```

**Threat to validity (dominant: Construct):**  
CHAIR uses pixel-accurate segmentation masks; audio substitutes AudioSet tags (weaker, incomplete). This is the §9.1 C1 threat; the dual criterion mitigates it.

**Confidence / Applicability:** HIGH / MED — canonical metric but audio adaptation is non-trivial.

**One-sentence reservation:**  
Do not report naive CHAIR-audio (tag-only criterion) — AudioSet incompleteness biases it upward; always use the dual criterion.

**[YOUR NOTES — fill in after reading]:**

---

## Paper S4 — Schafer 1977 — *The Tuning of the World*

- **Venue / Level**: Knopf 1977 (re-issued as *The Soundscape* 1994) · **L2 — STALE-VALID: 49yr**
- **Read**: Ch. 1 (Ear Cleaning), Ch. 9 (Soundscape Design), Glossary: keynote / soundmark / sound signal
- **Tier**: 1 · ~2 hrs selective

**What it claims:**
> Sound is a cultural object; the vocabulary of keynote sounds, soundmarks, and sound signals positions acoustic events within social and geographical meaning-systems.

**Key concepts:**

| Category | Definition | RQ5 Relevance |
|:---------|:-----------|:-------------|
| Keynote sound | Background tone defining an environment | Must describe even at low salience |
| **Soundmark** | Community-specific culturally-anchored sound | Primary RQ5 target — structurally OOD |
| Sound signal | Foreground sound demanding attention | High salience — reliably described |

**What it means for us:**
- RQ5 framing: the Bamberg bells are *soundmarks* — culturally-specific, geographically-anchored. The claim is that LALMs trained on FreeSound lack the prior to describe them correctly.

**Threat to validity (dominant: External):**  
Taxonomy developed in 1970s Canadian/European listening context; generalisation to non-Western soundscapes is debated (Sterne 2012).

**Confidence / Applicability:** HIGH / HIGH — no conceptual successor exists; still cited in contemporary sound studies.

**One-sentence reservation:**  
Do not cite Schafer 1977 for empirical claims about modern soundscapes — the listening walks are 1970s data; pair with Augoyard 2006 and Born 2013 for contemporary validity.

**One quote:**
> *"The soundscape of the world is changing. Modern man is beginning to inhabit a world with an acoustic environment radically different from any he has hitherto known."*

**[YOUR NOTES — fill in after reading Chapters 1 and 9]:**

---

## Paper S5 — Holm 1979 — Sequential Rejective Multiple Test Procedure

- **Venue / Level**: Scandinavian Journal of Statistics · **L2 — STALE-VALID: foundational statistics**
- **Tier**: 3 · ~15 min (read only the method; the math is simple)

**What it claims:**
> Holm-Bonferroni controls family-wise error rate exactly like Bonferroni but is uniformly more powerful for k > 1 hypotheses.

**Method:** Rank p-values ascending; compare *i*-th to α/(k − i + 1). Stop when comparison fails.

**What it means for us:**
- §9.4/§11: applied to the {RQ1, RQ2, RQ3, RQ4, RQ5} family to correct α=0.05 for 5 simultaneous hypotheses (otherwise 22.6% false-positive probability).

**Confidence / Applicability:** HIGH / HIGH — field standard.

**One-sentence reservation:**  
Do not cite Holm as much stronger than Bonferroni — for small families (k=5) the power advantage is modest; the key is that it never inflates false-positive rate.

---

## Paper S6 — Efron & Tibshirani 1993 — *An Introduction to the Bootstrap*

- **Venue / Level**: Chapman & Hall · **L2 — STALE-VALID: foundational statistics**
- **Tier**: 3 · ~20 min (read §12 on BCa; §1–2 for context)

**What it claims:**
> Non-parametric bootstrap CIs are asymptotically valid; BCa (bias-corrected accelerated) is accurate to second order and preferred for skewed/small-sample statistics.

**What it means for us:**
- All RQs: source of the `n_resamples=10,000` standard and the BCa choice for n < 300 (polyphony subset ≈ 150 clips).

**Confidence / Applicability:** HIGH / HIGH — canonical source, universally applicable.

**One-sentence reservation:**  
Do not cite Efron 1993 as justifying bootstrap on any sample size — the book explicitly warns about small-sample unreliability; §10 MDE analysis is the applicability check.

---

## Paper S7 — Heffernan 1993 — *Museum of Words: The Poetics of Ekphrasis from Homer to Ashbery*

- **Venue / Level**: University of Chicago Press · **L2 — STALE-VALID: foundational humanities**
- **Tier**: 2 · ~60 min (read Intro + ch. 1 on Homeric ekphrasis)
- **Status**: Reading pending — structural placeholder for cross-ref integrity with `literature_review.md` §1.2 + §13.

**What it claims (per lit-review §13):**
> Ekphrasis is the verbal representation of visual (and, by extension, non-verbal) representation — a rhetorical operation that turns perception into narrative description. Heffernan reframes the tradition from Homer's Shield of Achilles (Iliad 18) through Romanticism to late-modern poetry as a continuous lineage of *inter-modal translation*.

**What it means for us:**
- §1.2 + §13: Supplies the canonical humanities precedent for framing AAC as *machine ekphrasis* — a descriptive, not classificatory, task. The thesis' humanities contribution rests on this lineage.

**Confidence / Applicability:** HIGH / MED — the source is authoritative for the ekphrasis tradition; applicability to audio (not visual) ekphrasis requires one analogical move, which is disclosed.

**One-sentence reservation:**  
Do not collapse ekphrasis onto "description in general" — Heffernan's thesis is specifically about inter-semiotic translation with attendant gain and loss.

---

## Paper S8 — Truax 1984 — *Acoustic Communication*

- **Venue / Level**: Ablex Publishing · **L2 — STALE-VALID: foundational sound studies**
- **Tier**: 3 · ~45 min (ch. 2 "Listening" + ch. 5 "Soundscape" are load-bearing)
- **Status**: Reading pending — structural placeholder for cross-ref integrity with `literature_review.md` §13.

**What it claims (per lit-review §13):**
> Introduces the three-level *listening modes* taxonomy — listening-in-search, listening-in-readiness, background listening — as the foundation of soundscape-as-communication. Extends Schafer 1977 from catalogue to process.

**What it means for us:**
- RQ5 (humanities case study): the listening-modes grid is the audit lens applied to LALM-generated captions on cultural audio. Cross-ref to `literature_review.md` §13.

**Confidence / Applicability:** HIGH / MED — canonical in sound studies; applicability requires mapping human listening modes onto machine output, which is the research question's central move.

**One-sentence reservation:**  
Truax's framework is descriptive, not predictive — use it to audit captions, not to judge them.

---

## Paper S9 — Augoyard & Torgue 2006 — *Sonic Experience: A Guide to Everyday Sounds*

- **Venue / Level**: McGill-Queen's University Press · **L2 — sound-effects taxonomy**
- **Tier**: 3 · ~40 min (read Intro + 3-4 representative effects)
- **Status**: Reading pending — structural placeholder for cross-ref integrity with `literature_review.md` §13.

**What it claims (per lit-review §13):**
> Catalogues ~80 "sonic effects" (anamnesis, drone, masking, reverberation, cocktail-party, …) — a lexicon of perceptual-semantic phenomena that structure the experience of sound.

**What it means for us:**
- §13: the sonic-effects catalogue is the taxonomy the RQ5 humanities case study uses to audit what AAC systems can and cannot articulate. Particularly relevant for polyphony (masking/cocktail-party) and spatial cues (reverberation).

**Confidence / Applicability:** HIGH / HIGH — the taxonomy is precisely the vocabulary absent from DCASE metrics.

**One-sentence reservation:**  
The catalogue is descriptive and partially culturally-bound (francophone urban soundscape origins) — do not treat it as a universal ontology.

---

## Paper S10 — Sterne 2012 (ed.) — *The Sound Studies Reader*

- **Venue / Level**: Routledge (edited volume) · **L2 — disciplinary framing**
- **Tier**: 3 · ~30 min (Introduction only; anthology otherwise)
- **Status**: Reading pending — structural placeholder for cross-ref integrity with `literature_review.md` §13.

**What it claims (per lit-review §13):**
> Consolidates sound studies as a post-humanities discipline distinct from musicology, acoustics, and audio engineering — foregrounding cultural, political, and infrastructural dimensions of sound.

**What it means for us:**
- §13: positions the thesis within a recognisable disciplinary home (sound studies) rather than presenting humanities framing as ad-hoc decoration.

**Confidence / Applicability:** HIGH / MED — authoritative for disciplinary framing; applicability to an ML engineering thesis is indirect but legitimising.

**One-sentence reservation:**  
Sound studies is pluralistic — cite Sterne for disciplinary identification, not for any particular methodological commitment.

---

## Paper S11 — Born 2013 (ed.) — *Music, Sound and Space: Transformations of Public and Private Experience*

- **Venue / Level**: Cambridge University Press · **L2 — spatial-audio humanities**
- **Tier**: 3 · ~30 min (Introduction only)
- **Status**: Reading pending — structural placeholder for cross-ref integrity with `literature_review.md` §13.

**What it claims (per lit-review §13):**
> Develops the thesis that sound-spatialisation is a constitutive (not decorative) feature of auditory experience — space is heard, not merely a container for sound.

**What it means for us:**
- §13: supplies theoretical grounding for the observation that LALMs systematically elide spatial cues (distance, reverb, proximity) from captions — a humanities-motivated critique not visible through SPIDEr-FL alone.

**Confidence / Applicability:** HIGH / MED — authoritative on spatial audio as humanities object.

**One-sentence reservation:**  
Born's arguments are about human spatial perception; mapping onto what LALMs miss requires the explicit analogical move disclosed in §13.

---

## Paper S12 — Mitchell 1986 — *Iconology: Image, Text, Ideology*

- **Venue / Level**: University of Chicago Press · **L2 — STALE-VALID: sister-arts theory**
- **Tier**: 3 · ~40 min (Introduction + ch. on text/image division)
- **Status**: Reading pending — structural placeholder for cross-ref integrity with `literature_review.md` §13.

**What it claims (per lit-review §13):**
> The *ut pictura poesis* ("as is painting, so is poetry") tradition is not a rhetorical flourish but a structural claim about inter-semiotic translation between image and text — a "sister-arts" gesture that Mitchell both traces and problematises.

**What it means for us:**
- §13: extending Mitchell's sister-arts logic to audio↔text (rather than image↔text) is the theoretical gesture that positions AAC inside a 2000-year humanities conversation, not as a novel engineering task.

**Confidence / Applicability:** HIGH / MED — canonical iconology; applicability requires one analogical move (image→audio) which is disclosed.

**One-sentence reservation:**  
Mitchell's project is partly *critical* of sister-arts claims — cite him as source of the tradition *and* its self-critique, not as endorsement.

---

## Paper S13 — Wohlin et al. 2012 — *Experimentation in Software Engineering*

- **Venue / Level**: Springer · **L2 — field-standard methodology textbook**
- **Tier**: 2 · ~60 min (ch. 8 Threats to Validity is mandatory; §6 for experiment design)
- **Status**: Reading pending — foundational for `literature_review.md` §9 threats-to-validity framework.

**What it claims:**
> Empirical software-engineering studies must be planned and reported against a four-axis threat framework: Construct validity (C1–C4), Internal validity (I1–I4), External validity (E1–E3), Conclusion validity (V1–V3). Each identified threat must be matched to an explicit mitigation.

**What it means for us:**
- §9: every threat-to-validity table in the lit-review (14 threats across 4 axes) is structured on Wohlin's framework. This is the methodological backbone of the EBSE hardening layer.

**Confidence / Applicability:** HIGH / HIGH — field standard; directly applicable to an empirical LALM evaluation study.

**One-sentence reservation:**  
Wohlin's framework is discipline-agnostic within SE; its threats inventory does not anticipate LLM-specific issues (e.g., training-data contamination), which are annotated as *adapted* threats in §9.

---

## Paper S14 — Kerr 1998 — *HARKing: Hypothesizing After the Results are Known*

- **Venue / Level**: Personality and Social Psychology Review · **L2 — STALE-VALID: foundational methodology**
- **Tier**: 3 · ~15 min (short paper, ~20 pages)
- **Status**: Reading pending — structural placeholder; core rationale is already summarised in `literature_review.md` §9 + §11.

**What it claims:**
> Presenting a post-hoc hypothesis as if it had been a-priori ("HARKing") inflates Type-I error, corrupts replication, and is a form of scientific misconduct even when unintentional. Pre-registration is the structural fix.

**What it means for us:**
- §9 + §11: motivates the full pre-registration apparatus (`hypotheses_preregistered.yml` + per-RQ H₀ falsifiers) *before* any data is touched. Without Kerr's argument there is no reason for the pre-registration gate.

**Confidence / Applicability:** HIGH / HIGH — field-standard justification for pre-registration, domain-agnostic.

**One-sentence reservation:**  
Kerr does not claim HARKing is always malicious — honest exploration is legitimate *if transparently labelled as such*; the thesis adopts this distinction in §11.

---

## Paper S15 — Lipping et al. 2022 — Clotho-AQA: A Crowdsourced Dataset for Audio Question Answering

- **Venue / Level**: EUSIPCO 2022 · **L2 — peer-reviewed dataset paper**
- **Tier**: 2 · ~30 min (read full paper)
- **Status**: Reading pending — structural placeholder. Previously mis-attributed to *Labbeti 2022* in earlier draft; corrected in lit-review E1 (this entry supersedes the incorrect author).

**What it claims:**
> Extends the Clotho audio-caption dataset with ~7k crowd-sourced question–answer pairs over the same 4,500 audio clips, enabling instruction-following evaluation for audio-language models.

**What it means for us:**
- RQ0 (contamination audit): Clotho-AQA is **the highest-risk contamination source** for the 2024-era LALM generation because AF3 / SALMONN training corpora plausibly ingested it. The RQ0 FreeSound-ID cross-ref specifically targets Clotho-AQA overlap.
- `literature_review.md` §2.3: attribution must cite Lipping 2022 (L2), **not** Labbeti 2022 (which does not exist for this dataset — the dataset paper is Lipping).

**Confidence / Applicability:** HIGH / HIGH — primary source for the dataset, directly relevant.

**One-sentence reservation:**  
Clotho-AQA is QA, not captioning — overlap risk is about shared audio IDs (and therefore shared captions via Clotho), not about task-format leakage.

---

## Reading Progress Tracker

| # | Paper | Tier | v5 Summary Read | Critical Appraisal Read | [YOUR NOTES] Done | Date |
|:-:|:------|:----:|:---------------:|:----------------------:|:-----------------:|:----:|
| 1 | Drossos 2020 — Clotho | T1 | ⬜ | ⬜ | ⬜ | |
| 2 | Gemmeke 2017 — AudioSet | T3 | ⬜ | ⬜ | ⬜ | |
| 3 | Kim 2019 — AudioCaps | T3 | ⬜ | ⬜ | ⬜ | |
| 4 | Mei 2022 — AAC Survey | T1 | ⬜ | ⬜ | ⬜ | |
| 5 | Labbeti 2024 — DCASE baseline | T1 | ⬜ | ⬜ | ⬜ | |
| 6 | Tang 2023 — SALMONN | T2 | ⬜ | ⬜ | ⬜ | |
| 7 | Ghosh 2025a — AF2 | T3 | ⬜ | ⬜ | ⬜ | |
| 8 | **Ghosh 2025b — AF3 ⭐** | **T1** | ⬜ | ⬜ | ⬜ | |
| 9 | Qwen Team 2025 | T3 | ⬜ | ⬜ | ⬜ | |
| 10 | Kuan 2024 — Hallucination | T1 | ⬜ | ⬜ | ⬜ | |
| 11 | Kumar 2026 — TAC | T2 | ⬜ | ⬜ | ⬜ | |
| S1 | Zhou 2022 — FENSE | T2 | ⬜ | ⬜ | ⬜ | |
| S2 | Wu 2023 — LAION-CLAP | T2 | ⬜ | ⬜ | ⬜ | |
| S3 | Rohrbach 2018 — CHAIR | T2 | ⬜ | ⬜ | ⬜ | |
| S4 | **Schafer 1977 ⭐** | **T1** | ⬜ | ⬜ | ⬜ | |
| S5 | Holm 1979 | T3 | ⬜ | ⬜ | ⬜ | |
| S6 | Efron & Tibshirani 1993 | T3 | ⬜ | ⬜ | ⬜ | |
| S7 | Heffernan 1993 — Museum of Words | T2 | ⬜ | ⬜ | ⬜ | |
| S8 | Truax 1984 — Acoustic Communication | T3 | ⬜ | ⬜ | ⬜ | |
| S9 | Augoyard & Torgue 2006 — Sonic Experience | T3 | ⬜ | ⬜ | ⬜ | |
| S10 | Sterne 2012 (ed.) — Sound Studies Reader | T3 | ⬜ | ⬜ | ⬜ | |
| S11 | Born 2013 (ed.) — Music, Sound and Space | T3 | ⬜ | ⬜ | ⬜ | |
| S12 | Mitchell 1986 — Iconology | T3 | ⬜ | ⬜ | ⬜ | |
| S13 | **Wohlin 2012 — Experimentation in SE** | **T2** | ⬜ | ⬜ | ⬜ | |
| S14 | Kerr 1998 — HARKing | T3 | ⬜ | ⬜ | ⬜ | |
| S15 | Lipping 2022 — Clotho-AQA | T2 | ⬜ | ⬜ | ⬜ | |
