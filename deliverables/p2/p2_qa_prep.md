# P2 — Q&A Preparation

*18 anticipated questions · 5 themes · each answer ≤ 30 seconds*
*Author: Zuraiz · 2026-05-18*

---

## Universal fallback (use when stuck)

> "That is a good question. The empirical answer comes from the audit and the polyphony split, both of which I run in the next 8 weeks. The current literature pointer is **[Author, Year]**, and I will report the result in P3."

Keep this in your back pocket. Use it once, max twice.

---

## Theme A — Dataset choice (4 Qs)

### Q1.  Why **Clotho v2.1** over AudioCaps?

**Short answer:** Three reasons.

- **DCASE Task 6 official benchmark** — leaderboard parity (DCASE 2024 baseline SPIDEr-FL ≈ 29.6 %).
- **5 captions per clip** — dense annotation lets me distinguish *under-description* from single-annotator variance. AudioCaps has 1 caption per training clip.
- **FreeSound-sourced, not AudioSet-derived** — almost every LALM trains on AudioSet, so a zero-shot claim against AudioCaps is not really zero-shot.

**Empirical wedge:** FD-DeCap (IEEE TASLP 2025, doc 11333308) reports SPIDEr **0.282 on Clotho** vs. **0.429 on AudioCaps** — even after causal-inference debiasing, the contaminated corpus scores ~50 % higher. The gap is the wedge.

---

### Q2.  Why not WavCaps? It is much larger.

**Short answer:** WavCaps is **400 K** web-scraped clips with **LLM-generated** captions. Two reasons to reject for evaluation:

- Captions are not human-verified — they inherit the biases of the generating LLM.
- WavCaps's largest sub-source is FreeSound, which is **the same source as Clotho** — direct contamination risk for any LALM trained on either.

Useful for *training* in a different study; not useful for *evaluating* zero-shot LALMs.

---

### Q3.  Why not AudioSetCaps or Cacophony?

**AudioSetCaps**: AudioSet-derived with synthetic captions — same family rejection as AudioCaps, plus the captions are themselves LALM-generated. **Cacophony** is a 13 K-hour **contrastive training corpus**, not an evaluation benchmark. Both considered, both rejected.

---

### Q4.  Could you also report AudioCaps numbers as a robustness check?

Yes — as an *addition*, not a replacement. I'd disclose the FD-DeCap gap and treat AudioCaps numbers as upper bounds while Clotho gives the honest figure. This appears in the term paper, not P2.

---

## Theme B — Acquisition, mics, and annotation (4 Qs)

### Q5.  Which microphones were used?

**Honest answer:** all of them. Clotho is curated from **FreeSound** community uploads — studio mics, field recorders, mobile phones with MEMS microphones. The dataset team's contribution is the captions, not the audio. **Device mismatch** (per Lecture 04, slides 6–7) is a built-in property of the corpus.

This is a realistic property of deployment audio. We acknowledge it; we do not pretend otherwise.

---

### Q6.  Why is there no original recording in this project?

**Zero-shot evaluation protocol.** T6 targets pretrained LALMs. Recording our own data would not change what we test — the models still saw their training data, not our recordings. (And per Lecture 04 slide 12, recording original audio would activate Privacy-Enhancing Technology requirements which are out of scope.)

---

### Q7.  Weak vs. strong labels — how do you handle it?

Clotho is **weak**: clip-level captions, no time-stamps. For the polyphony split (RQ2) I derive **pseudo-strong** labels by running **PaSST / PANNs CNN14** SED over the development split — sets of detected events with start/end times. The Δ MACE metric uses both: weak labels as `E_ref` (the 5-caption union vocabulary), pseudo-strong labels as `E_audio`.

---

### Q8.  Are 5 reference captions enough to detect under-description?

**Floor, not ceiling.**
- 5 captions give the **union vocabulary** `E_ref` — if the model mentions fewer entities than the union, that is a clear under-description signal.
- True polyphony can exceed what any single caption captures, so I also use the SED set `E_audio` as a second ground truth.
- I report both grounds — the gap between them tells you the human-labelling ceiling. (Carried from P1 Q9.)

---

## Theme C — Polyphony split (3 Qs)

### Q9.  Where does the **polyphony threshold** come from?

Operational definition: a clip is **polyphonic** if **≥ 2 simultaneous AudioSet classes** are active for **≥ 1 s** at confidence ≥ 0.5 (PaSST).

Threshold defence:
- **Any-overlap** (≥ 1 frame) is too lax — inflates the polyphonic bucket with brief co-occurrences.
- **≥ 3 classes / ≥ 1 s** is too strict — depopulates the bucket and weakens statistical power.

The ≥ 2 / ≥ 1 s rule sits in the middle and is defensible; I will report sensitivity by ablating it (term paper).

---

### Q10.  What is the **formal under-description test**?

A clip is under-described iff
&nbsp;&nbsp;&nbsp;&nbsp;**card(E_model) &lt; card(E_ref ∩ E_audio)**
where
- `E_audio` = SED-detected events on the clip,
- `E_ref` = union over the 5 reference captions,
- `E_model` = entities in the model's output.

The fraction of clips where this holds, split by polyphony bucket, gives **Δ MACE = (poly fraction) − (mono fraction)** — the headline RQ2 metric. (P1 Q&A Q14.)

---

### Q11.  Which SED tool — PaSST or CNN14?

**PaSST primary, CNN14 as sanity check.** PaSST is SOTA; CNN14 is the DCASE 2024 baseline. If their splits disagree on a clip, I keep the conservative bucket (mono if either says mono) and flag the disagreement in the term paper. I also plan a 100-clip manual audit to verify.

---

## Theme D — Contamination audit (4 Qs)

### Q12.  How will you check **training-data contamination**?

**Three-layer audit, per LALM, not aggregated:**

1. **File-ID match** — direct lookup of Clotho clip IDs against each LALM's training manifest.
2. **Chromaprint audio fingerprint** — fallback for near-duplicates / re-encoded clips.
3. **Caption n-gram overlap** — flag clips whose captions appear verbatim in any training set's text.

I will report contamination rate **per model** — that is the only way to answer P1's Open Question ("do the three LALMs fail polyphony the same way?"). Aggregation would hide differential failure modes.

---

### Q13.  What if a LALM's manifest is **closed**?

**Falcon3-Audio's manifest is public** — its key selling point (P1 Q1). Layers 1, 2, and 3 are all usable.

**SALMONN and Qwen2.5-Omni** publish only partial manifests. For them, Layer 1 is skipped — only fingerprinting and caption overlap apply. This is disclosed as a limitation in the contamination table.

---

### Q14.  What if contamination turns out to be **heavy**?

**Still informative.** Three options:
- Report polyphony failure on the **clean subset** (clips that pass all three audit layers) and discuss the contaminated subset separately.
- Compute a contamination-discounted Δ MACE: weight each clip by its contamination probability.
- In the worst case, the study still answers "**how much** of LALM performance is contamination?" — a publishable result in itself.

The study is not invalidated by contamination — only by ignoring it.

---

### Q15.  Why audit **all three** LALMs, not just Falcon3?

P1's Open Question: "do all three LALMs fail polyphony the same way, or differently?" An aggregate audit would average over model-specific failures and tell us nothing. The audit *must* be per-model. (This is also why I argued for per-parameter metric reporting in P1 — same logic.)

---

## Theme E — Methodology / housekeeping (3 Qs)

### Q16.  What are the **headline metrics**?

Carried unchanged from P1:

- **RQ1**: SPIDEr-FL · CIDEr
- **RQ2 (core)**: Δ MACE = (poly under-description fraction) − (mono under-description fraction)
- **RQ3**: CHAIR-audio · MACE Precision

CLAPScore and CLAIRA are alternative metrics I keep on the radar; not in the primary set.

---

### Q17.  Spectrogram parameters?

`librosa.stft` with `n_fft = 1024`, `hop_length = 512`. Then `librosa.feature.melspectrogram` with 64 mel bins, then `librosa.power_to_db`. Exactly the tool the prof's brief names.

---

### Q18.  "All team members shall present" — where is your team?

This is a **solo project** per my registration (Matrikel 2177213). Presenter = author.

---

## Wildcard reserve answers (if a question goes outside the 18 above)

- **"Is this task also relevant for music?"** → Out of scope. Harmonic polyphony is harder; environmental sound is hard enough.
- **"Why English captions?"** → Clotho is English, LALM decoders are English. Audiopedia (2025) covers multilingual audio QA but is not in scope here.
- **"What if your hypothesis is wrong?"** → A negative result (LALMs match tagging on polyphony) is also a publishable finding. Either way, the study is informative.
- **"What about real-time / streaming?"** → Out of scope. All evaluation is offline on 15–30 s clips.
- **"Where will inference run?"** → Falcon3-3B on a single 24 GB GPU; Qwen2.5-Omni on the university cluster or a rented A100. Inference only, no training.
- **"Privacy / PETs?"** → Not a concern for Clotho — captions were post-processed to remove speech transcription per Drossos+ 2020. Would matter only if we recorded our own data.
- **"FAIR / licence?"** → Clotho is CC-BY 4.0 on Zenodo (record 4783391) — fully FAIR-compliant per Lecture 04.
- **"What does AudioCaps actually look like?"** → Show Appendix A in the deck.
- **"What does WavCaps actually look like?"** → Show Appendix B in the deck.

---

## Final mental rules for Q&A

1. **Restate the question in one short line first.** Buys 3 seconds, confirms you heard it correctly.
2. **Conclusion first, then reasons.**
3. **If you don't know — say so honestly**, then point to the literature you'd consult.
4. **Per-model, not aggregated.** That phrase resolves at least three plausible follow-up questions.
5. **The contamination audit comes *before* the polyphony evaluation.** This ordering is the spine of the project — every methodological question collapses to it.
