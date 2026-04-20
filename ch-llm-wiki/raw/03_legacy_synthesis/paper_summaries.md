# Paper Summaries — T6: Audio-to-Text Captioning
*Master's Project · CH-Proj-M · SS 2026 · Zuraiz (2177213)*
*Prof. Dr.-Ing. Jakob Abeßer · Computational Humanities · Uni Bamberg*
*Last updated: April 2026 — Rebuilt version (standardised card format)*

> **How to use.** Each card follows a fixed format. Fill in `[YOUR NOTES]` after reading. The pre-filled sections are verified against primary sources. "What it means for us" is limited to ≤ 2 sentences + RQ tags — extended interpretation belongs in `literature_review.md`.

> **Tier convention:**
> - **T1** — read before Phase 1 (May 4): Drossos, Mei, Labbeti, AF3, Kuan, Schafer
> - **T2** — read before Phase 2 (May 18): SALMONN, FENSE, CLAP, CHAIR, TAC
> - **T3** — reference / supplementary

---

## Paper 1 — Drossos 2020 — Clotho: An Audio Captioning Dataset

- **Venue / Level:** ICASSP 2020 · **L2** · **Year:** 2020 · **Link:** arXiv 1910.09387 · Zenodo **4783391**
- **Confidence / Applicability:** HIGH / HIGH

**Claim:** The first purpose-built AAC benchmark with 5 human captions per clip and acoustic-focus annotation protocol.
**Method:** 6,974 FreeSound clips (CC-licensed, 15–30s), five independent AMT crowdsourcers per clip.
**Key numbers:** 6,974 clips × 5 captions; eval split = 1,045 clips; DCASE 2024 Task 6 official eval set.
**Threat to validity:** "Acoustic focus" instruction cannot be empirically verified — some captions contain inferred visual content.
**Feeds:** RQ0, RQ1, RQ2, RQ3 — primary evaluation set. Lit-review §1, §2.
**One-sentence reservation:** Do not cite for annotation *accuracy* — inter-annotator agreement on event identification was never measured.

**[YOUR NOTES]:**

---

## Paper 2 — Gemmeke 2017 — AudioSet: Ontology and Human-Labeled Dataset

- **Venue / Level:** ICASSP 2017 · **L2** · **Year:** 2017 · **Link:** DOI 10.1109/ICASSP.2017.7952261
- **Confidence / Applicability:** HIGH / HIGH

**Claim:** A 632-class hierarchical ontology of everyday sounds plus 2.1M weakly-labelled YouTube clips.
**Method:** Expert-curated 7-category hierarchy, clip-level (weak) labels, 2.084M labelled clips.
**Key numbers:** 632 classes — the hallucination vocabulary for CHAIR-audio (RQ3).
**Threat to validity:** Rater agreement moderate (κ ≈ 0.5 on some subsets); audible events systematically un-tagged. Motivates CLAPScore dual criterion.
**Feeds:** RQ3 — ontology for hallucination measurement. Lit-review §2, §6.6.
**One-sentence reservation:** Do not cite AudioSet labels as complete ground truth — use as lower bound; cross-check with CLAPScore.

**[YOUR NOTES]:**

---

## Paper 3 — Kim 2019 — AudioCaps: Generating Captions for Audios in the Wild

- **Venue / Level:** NAACL 2019 · **L2** · **Year:** 2019 · **Link:** audiocaps.github.io
- **Confidence / Applicability:** HIGH / HIGH for RQ3 stimulus; HIGH / LOW for primary metric

**Claim:** First large-scale (46k) audio captioning dataset from AudioSet with human captions.
**Method:** ~46k AudioSet YouTube clips (10s) × 1 crowdsourced caption.
**Key numbers:** ~46,000 clips × 1 caption; AudioSet tags available per clip.
**Threat to validity:** Single-caption metrics are annotator-dominated; not comparable to Clotho multi-reference scores.
**Feeds:** RQ3 only — stimulus set for hallucination experiment (single-event clips). Lit-review §2.2.
**One-sentence reservation:** Do not report SPIDEr-FL on AudioCaps as the headline — single reference violates the metric's assumed condition.

**[YOUR NOTES]:**

---

## Paper 4 — Mei 2022 — Automated Audio Captioning: An Overview

- **Venue / Level:** EURASIP JASMP 2022 · **L2** · **Year:** 2022 · **Link:** arXiv 2205.05949
- **Confidence / Applicability:** HIGH / MED — authoritative for pre-LALM era; survey scope excludes LALMs

**Claim:** Comprehensive survey of 50+ AAC papers (2017–2022), documenting convergence on encoder-decoder architecture and naming polyphony as dominant open challenge.
**Method:** Taxonomy: encoder × decoder × training regime; systematic metric comparison.
**Key numbers:** 50+ papers; convergence on CNN14/PANNs + Transformer decoder by 2021; polyphony explicitly named un-solved.
**Threat to validity:** Bounded at 2022 — any post-2022 shift (LALMs) not covered.
**Feeds:** RQ1 (historical context), RQ2 (polyphony problem statement). Lit-review §3, §5.1.
**One-sentence reservation:** Do not cite for current-practice claims about LALMs — the paper predates them.

**[YOUR NOTES]:**

---

## Paper 5 — Labbeti 2024 — DCASE 2024 Task 6 Baseline

- **Venue / Level:** DCASE 2024 technical report · **L1** · **Year:** 2024 · **Link:** github.com/Labbeti/dcase2024-task6-baseline
- **Confidence / Applicability:** HIGH / HIGH

**Claim:** Publicly reproducible supervised AAC baseline achieving **29.6% SPIDEr-FL** on Clotho-eval.
**Method:** ConvNeXt encoder + Transformer decoder; supervised on Clotho; `aac-metrics` for scoring.
**Key numbers:** **29.6% SPIDEr-FL** — the comparison floor for RQ1.
**Threat to validity:** Single training run; seed variance not reported. Canary reproduction tests this.
**Feeds:** RQ1 — comparison floor; Phase 2 canary test. Lit-review §3.2.
**One-sentence reservation:** Do not cite 29.6% as an upper bound on supervised AAC — DCASE challenge winners score higher; this is the reproducible single-run floor.

**[YOUR NOTES]:**

---

## Paper 6 — Tang 2023 — SALMONN: Generic Hearing Abilities for LLMs

- **Venue / Level:** ICLR 2024 · **L2** · **Year:** 2023 · **Link:** arXiv 2310.13289
- **Confidence / Applicability:** HIGH / MED — peer-reviewed but architecture superseded by AF3

**Claim:** First LALM with generic hearing — speech, music, and environmental audio — via dual audio encoder.
**Method:** Whisper-L-v2 (speech) + BEATs (events) → Q-Former → Vicuna-13B.
**Key numbers:** 13B parameters; first published LALM with zero-shot Clotho-style captioning.
**Threat to validity:** "Generic hearing abilities" evaluated on curated benchmarks not including Clotho-eval SPIDEr-FL.
**Feeds:** RQ1 (historical LALM baseline), RQ2 (dual encoder test). Lit-review §4.2.
**One-sentence reservation:** Do not cite as current SOTA LALM — AF3 supersedes it on all major benchmarks.

**[YOUR NOTES]:**

---

## Paper 7 — Ghosh 2025a — Audio Flamingo 2 (AF2)

- **Venue / Level:** NVIDIA preprint · **L3** · **Year:** 2025 · **Link:** arXiv 2503.03983
- **Confidence / Applicability:** HIGH / HIGH despite L3 — public code, no contradicting evidence

**Claim:** Introduces the AF-CLAP unified encoder and long-audio capability via sparse attention.
**Method:** Custom contrastive pretraining on mixed corpus; sparse attention for long-context; 3B and 7B variants.
**Key numbers:** AF-CLAP encoder carried forward into AF3 unchanged.
**Threat to validity:** L3 preprint, single-institution, no independent replication.
**Feeds:** Architectural context for AF3; AF-CLAP encoder lineage. Lit-review §4.3.
**One-sentence reservation:** Do not cite as primary model — AF3 supersedes; cite only for architectural lineage.

**[YOUR NOTES]:**

---

## Paper 8 — Ghosh 2025b — Audio Flamingo 3 (AF3) ⭐ PRIMARY MODEL

- **Venue / Level:** NVIDIA preprint · **L3** · **Year:** 2025 · **Link:** arXiv 2507.08128 · HF: nvidia/audio-flamingo-3
- **Confidence / Applicability:** HIGH / HIGH

**Claim:** SOTA open-source LALM surpassing all prior models on all major audio understanding benchmarks.
**Method:** Unified AF-CLAP encoder → Adapter → 8B LLM. Read the data card for RQ0.
**Key numbers:** MMAU 72.28, ClothoAQA 91.1%, CMM-Hallucination 86.7%, Clotho-Entailment 92.9%.
**Threat to validity:** Training corpus includes AudioSetCaps and WavCaps (same upstream as Clotho). "Zero-shot" is a claim RQ0 tests, not a premise.
**Feeds:** RQ0, RQ1, RQ2, RQ3, RQ4 — primary model. Lit-review §4.3.
**One-sentence reservation:** Do not cite benchmark numbers as zero-shot capability without qualifying by RQ0 audit result.

> [!IMPORTANT]
> When reading: note every training dataset in §3 and the HuggingFace data card. This is the RQ0 input.

**[YOUR NOTES — CRITICAL: list all training datasets]:**

---

## Paper 9 — Qwen Team 2025 — Qwen2.5-Omni

- **Venue / Level:** Alibaba preprint · **L3** · **Year:** 2025 · **Link:** arXiv 2503.20215
- **Confidence / Applicability:** HIGH / HIGH — Apache-2.0 = lowest legal risk

**Claim:** End-to-end multimodal model (text + audio + image + video) with streaming output.
**Method:** Different architectural bet from AF3's audio-language specialisation.
**Key numbers:** Apache-2.0 licence; competitive with AF3 on several audio benchmarks.
**Threat to validity:** Multimodal benchmarks reduce to text-heavy reasoning; audio grounding undermeasured.
**Feeds:** Optional ablation (Cut 1). Lit-review §4.4.
**One-sentence reservation:** Do not cite overall multimodal scores as evidence of audio capability specifically.

**[YOUR NOTES]:**

---

## Paper 10 — Kuan 2024 — Understanding Sounds, Missing the Questions

- **Venue / Level:** Interspeech 2024 · **L2** · **Year:** 2024 · **Link:** isca-archive.org/interspeech_2024/kuan24_interspeech.pdf
- **Confidence / Applicability:** HIGH / HIGH

**Claim:** LALM hallucination is a language-prior failure: models confabulate sounds that co-occur frequently in text even when absent from audio.
**Method:** Controlled stimuli: high text-prior risk vs. low text-prior / high perception demand. Measured false-positive hallucination rate across LALMs.
**Key numbers:** First systematic hallucination measurement; mechanism confirmed: text prior > audio evidence.
**Threat to validity:** Small curated stimulus set; generalisation to natural Clotho clips is a conjecture.
**Feeds:** RQ3 (foundational motivation). Lit-review §5.2.
**One-sentence reservation:** Do not cite hallucination rates as AF3 numbers — the study predates AF3 and measured different LALMs.

**[YOUR NOTES]:**

---

## Paper 11 — Kumar 2026 — TAC: Timestamped Audio Captioning

- **Venue / Level:** Adobe Research / Northwestern preprint · **L3** · **Year:** 2026 · **Link:** arXiv 2602.15766
- **Confidence / Applicability:** HIGH / HIGH

**Claim:** LALMs describe events in canonical text-prior order rather than onset order; TAC resolves this via temporal grounding head + synthetic-mixture training.
**Method:** Synthetic A-then-B pipeline; separate temporal grounding head predicting onset/offset timestamps.
**Key numbers:** TAC correct-ordering rate significantly above LALMs; measurably lower hallucination on overlapping events.
**Threat to validity:** Synthetic mixtures have sharper onsets than natural polyphony; advantage may not transfer.
**Feeds:** RQ4 (replication protocol + oracle). Lit-review §5.3.
**One-sentence reservation:** Do not cite as evidence of natural-polyphony superiority — results are on synthetic data.

**[YOUR NOTES]:**

---

## Paper S1 — Zhou 2022 — FENSE

- **Venue / Level:** ICASSP 2022 · **L2** · **Year:** 2022 · **Link:** arXiv 2110.04684
- **Confidence / Applicability:** HIGH / HIGH

**Claim:** Image-caption metrics transfer poorly to audio. FENSE achieves highest human-correlation.
**Method:** SentenceBERT similarity × Fluency Error Penalty.
**Key numbers:** Highest human-correlation; BLEU/ROUGE/METEOR weakest.
**Threat to validity:** Human judgement pool small, English-only, demographics unreported.
**Feeds:** Primary metric pair (with SPIDEr-FL). Lit-review §6.4.
**One-sentence reservation:** FENSE is NOT reference-free — it requires human references and is undefined on RQ5 archival audio.

**[YOUR NOTES]:**

---

## Paper S2 — Wu 2023 — LAION-CLAP

- **Venue / Level:** ICASSP 2023 · **L2** · **Year:** 2023 · **Link:** github.com/LAION-AI/CLAP
- **Confidence / Applicability:** HIGH / HIGH for RQ5; HIGH / MED on archival audio

**Claim:** Open-source contrastive audio-language model enabling CLAPScore — the only reference-free quality metric.
**Method:** Large-scale contrastive pretraining on mixed audio corpus.
**Key numbers:** CLAPScore = cosine_similarity(CLAP_audio, CLAP_text); no references required.
**Threat to validity:** Training corpus web-scraped; likely under-represents archival Germanic audio.
**Feeds:** RQ5 (non-negotiable). Lit-review §6.5.
**One-sentence reservation:** Do not report CLAPScore on archival Germanic audio without disclosing training-domain mismatch.

**[YOUR NOTES]:**

---

## Paper S3 — Rohrbach 2018 — CHAIR

- **Venue / Level:** EMNLP 2018 · **L2** · **Year:** 2018 · **Link:** ACL Anthology D18-1437
- **Confidence / Applicability:** HIGH / MED — canonical but audio adaptation is non-trivial

**Claim:** Image captioning models hallucinate objects at 5–20%; CHAIR measures this systematically.
**Method:** CHAIR_i = |hallucinated objects| / |all mentioned objects|; uses segmentation-mask ground truth.
**Key numbers:** 5–20% hallucination rate in modern image captioners.
**Threat to validity:** CHAIR uses pixel-accurate segmentation; audio substitutes AudioSet tags (weaker). Motivates dual criterion.
**Feeds:** RQ3 (adapted CHAIR-audio protocol). Lit-review §6.6.
**One-sentence reservation:** Do not report naive CHAIR-audio (tag-only) — AudioSet incompleteness biases upward; always use dual criterion.

**[YOUR NOTES]:**

---

## Paper S4 — Schafer 1977 — *The Tuning of the World*

- **Venue / Level:** Knopf 1977 · **L2 — STALE-VALID: 49yr** · **Year:** 1977
- **Confidence / Applicability:** HIGH / HIGH — no conceptual successor exists

**Claim:** Sound is a cultural object; keynote sounds, soundmarks, and sound signals position acoustic events within social meaning-systems.
**Method:** Qualitative classification of soundscape elements based on ecological listening.
**Key numbers:** Three acoustic categories (keynote / soundmark / signal) with distinct salience profiles.
**Threat to validity:** Taxonomy developed in 1970s Canadian/European context; generalisation debated.
**Feeds:** RQ5 (humanities framing, soundmark = primary target). Lit-review §1.2, §14.
**One-sentence reservation:** Do not cite for empirical claims about modern soundscapes — pair with Augoyard 2006 and Born 2013.

**[YOUR NOTES — read Chapters 1 and 9]:**

---

## Paper S5 — Holm 1979 — Sequential Rejective Multiple Test Procedure

- **Venue / Level:** Scand. J. Stat. · **L2 — STALE-VALID** · **Year:** 1979
- **Confidence / Applicability:** HIGH / HIGH

**Claim:** Holm-Bonferroni controls FWER exactly like Bonferroni but is uniformly more powerful for k > 1.
**Method:** Rank p-values ascending; compare *i*-th to α/(k − i + 1).
**Key numbers:** For k=3, strictest α' = 0.05/3 ≈ 0.0167.
**Threat to validity:** For small families, power advantage is modest.
**Feeds:** §12 pre-registered falsification; `hypotheses_preregistered.yml`. Lit-review §12.3.
**One-sentence reservation:** Do not cite as much stronger than Bonferroni for small families — the key is that it never inflates false-positive rate.

---

## Paper S6 — Efron & Tibshirani 1993 — *An Introduction to the Bootstrap*

- **Venue / Level:** Chapman & Hall · **L2 — STALE-VALID** · **Year:** 1993
- **Confidence / Applicability:** HIGH / HIGH

**Claim:** BCa bootstrap is accurate to second order and preferred for skewed/small-sample statistics.
**Method:** Non-parametric resampling with bias-correction and acceleration.
**Key numbers:** n=1,000 resamples standard; BCa preferred for n < 300.
**Threat to validity:** Small-sample unreliability explicitly warned; MDE analysis is the applicability check.
**Feeds:** All RQs — CI construction method. Lit-review §10.
**One-sentence reservation:** Do not cite as justifying bootstrap on any sample size — the book warns about small samples.

---

## Paper S7 — Heffernan 1993 — *Museum of Words*

- **Venue / Level:** U. Chicago Press · **L2 — STALE-VALID** · **Year:** 1993
- **Confidence / Applicability:** HIGH / MED

**Claim:** Ekphrasis is inter-modal translation from non-verbal to verbal representation — a continuous lineage from Homer through Romanticism.
**Method:** Literary-critical analysis of ekphrastic tradition.
**Key numbers:** n/a (humanities)
**Threat to validity:** Applicability to audio (not visual) ekphrasis requires one analogical move, disclosed.
**Feeds:** Humanities anchor for framing AAC as machine ekphrasis. Lit-review §1.2, §14.
**One-sentence reservation:** Do not collapse ekphrasis onto "description in general" — it is specifically about inter-semiotic translation with gain and loss.

---

## Paper S8 — Truax 1984 — *Acoustic Communication*

- **Venue / Level:** Ablex Publishing · **L2 — STALE-VALID: 42yr** · **Year:** 1984
- **Confidence / Applicability:** HIGH / MED

**Claim:** Three listening modes (listening-in-search, listening-in-readiness, background listening) as foundation of soundscape-as-communication.
**Method:** Theoretical extension of Schafer 1977 from catalogue to process.
**Key numbers:** n/a (theoretical framework)
**Threat to validity:** Mapping human listening modes onto machine output is the research question's central move.
**Feeds:** RQ5 (listening-modes audit lens). Lit-review §14.1.
**One-sentence reservation:** Truax's framework is descriptive, not predictive — use to audit captions, not judge them.

---

## Paper S9 — Augoyard & Torgue 2006 — *Sonic Experience*

- **Venue / Level:** McGill-Queen's UP · **L2** · **Year:** 2006
- **Confidence / Applicability:** HIGH / HIGH

**Claim:** Catalogues ~80 sonic effects (anamnesis, drone, masking, reverberation) — perceptual-semantic primitives for sound experience.
**Method:** Empirical catalogue from francophone urban soundscape research.
**Key numbers:** ~80 sonic effects
**Threat to validity:** Partially culturally-bound (francophone origins).
**Feeds:** RQ5 (sonic-effects taxonomy for qualitative audit). Lit-review §14.2.
**One-sentence reservation:** Do not treat as universal ontology — catalogue has francophone urban origins.

---

## Paper S10 — Sterne 2012 (ed.) — *The Sound Studies Reader*

- **Venue / Level:** Routledge · **L2** · **Year:** 2012
- **Confidence / Applicability:** HIGH / MED

**Claim:** Sound studies is a post-humanities discipline distinct from musicology, acoustics, and engineering.
**Method:** Edited anthology consolidating the field.
**Key numbers:** n/a (disciplinary framing)
**Threat to validity:** Applicability to an ML thesis is indirect but legitimising.
**Feeds:** Disciplinary identification for the thesis. Lit-review §14.3.
**One-sentence reservation:** Sound studies is pluralistic — cite for disciplinary identification, not methodological commitment.

---

## Paper S11 — Born 2013 (ed.) — *Music, Sound and Space*

- **Venue / Level:** Cambridge UP · **L2** · **Year:** 2013
- **Confidence / Applicability:** HIGH / MED

**Claim:** Sound-spatialisation is constitutive, not decorative — space is heard, not merely a container.
**Method:** Edited volume on spatial audio as humanities object.
**Key numbers:** n/a (theoretical)
**Threat to validity:** Arguments about human spatial perception; mapping onto LALM gaps requires analogical move.
**Feeds:** RQ5 (place-indexicality of soundmarks). Lit-review §14.4.
**One-sentence reservation:** Born's arguments are about human perception; mapping onto what LALMs miss requires explicit disclosure.

---

## Paper S12 — Mitchell 1986 — *Iconology*

- **Venue / Level:** U. Chicago Press · **L2 — STALE-VALID: 40yr** · **Year:** 1986
- **Confidence / Applicability:** HIGH / MED

**Claim:** The sister-arts tradition is a structural claim about inter-semiotic translation, not a rhetorical flourish.
**Method:** Critical iconology tracing text/image division.
**Key numbers:** n/a (theory)
**Threat to validity:** Mitchell is partly *critical* of sister-arts claims — cite as source of tradition *and* its self-critique.
**Feeds:** Discussion chapter horizon (extending image→text to audio→text). Lit-review §14.5.
**One-sentence reservation:** Cite as source of the tradition and its self-critique, not as endorsement.

---

## Paper S13 — Wohlin et al. 2012 — *Experimentation in Software Engineering*

- **Venue / Level:** Springer · **L2** · **Year:** 2012
- **Confidence / Applicability:** HIGH / HIGH

**Claim:** Empirical studies must be planned against four-axis threat framework: Construct, Internal, External, Conclusion validity.
**Method:** Textbook methodology for SE experimentation.
**Key numbers:** 14 threats across 4 axes in this project's application.
**Threat to validity:** Framework is discipline-agnostic within SE; does not anticipate LLM-specific issues (e.g., contamination), which are annotated as adapted threats.
**Feeds:** Lit-review §9 (all threat tables). Implementation_plan verification gates.
**One-sentence reservation:** Wohlin does not cover LLM-specific threats — contamination threats are adapted additions.

---

## Paper S14 — Kerr 1998 — HARKing

- **Venue / Level:** Personality and Social Psychology Review · **L2** · **Year:** 1998
- **Confidence / Applicability:** HIGH / HIGH

**Claim:** HARKing (hypothesising after results are known) inflates Type-I error and corrupts replication. Pre-registration is the structural fix.
**Method:** Meta-analysis of publication bias and post-hoc hypothesis construction.
**Key numbers:** n/a (methodological argument)
**Threat to validity:** None — argument is domain-agnostic.
**Feeds:** Lit-review §12 (pre-registration rationale). Implementation_plan `hypotheses_preregistered.yml`.
**One-sentence reservation:** Kerr does not claim HARKing is always malicious — honest exploration is legitimate if labelled as such.

---

## Paper S15 — Lipping et al. 2022 — Clotho-AQA

- **Venue / Level:** EUSIPCO 2022 · **L2** · **Year:** 2022
- **Confidence / Applicability:** HIGH / HIGH

**Claim:** Extends Clotho with ~7k crowdsourced QA pairs for instruction-following evaluation.
**Method:** Question-answer annotation over 4,500 Clotho audio clips.
**Key numbers:** ~7k QA pairs; highest-risk contamination source for 2024-era LALMs.
**Threat to validity:** QA is not captioning — overlap risk is about shared audio IDs, not task-format leakage.
**Feeds:** RQ0 (contamination audit — highest-risk manifest). Lit-review §2.3.
**One-sentence reservation:** Clotho-AQA overlap with Clotho-eval is about *audio IDs*, not *task format*.

---

## Reading Progress Tracker

| # | Paper | Tier | Summary Read | Critical Appraisal | [YOUR NOTES] Done | Date |
|:-:|:------|:----:|:------------:|:------------------:|:-----------------:|:----:|
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
