# P2 Speaker Cheat-Sheet — pointers, not prose

**Total: 4 min 40 s** · 9 slides · plain English, confident delivery, no jargon parade.

> The old "read this paragraph word-for-word" script is gone. This file gives you **3 things per slide**: anchor bullets to free-style around · 2–3 "★ say-exact" phrases that must land verbatim · key numbers in **bold** that must be precise. Speak around the bullets in your own words — that's how you avoid sounding like you're reading.

---

## How to use this file (15-minute prep flow)

1. **Read the whole file once** (5 min). Get the shape of the talk.
2. **Drill the ★ say-exact lines** (5 min). Cover the bullets and recite only the starred phrases. There are ~12 of them total — they're your safety net.
3. **One full out-loud run with stopwatch** (5 min). Don't aim for perfect words; aim for the right beats. If you blank, glance down, find a bullet, keep moving.
4. On the day: open this file on phone, glance once between slides if needed.

**Confidence rule**: pros explain hard things simply. If a sentence sounds technical, *replace it with the everyday version below*. The prof respects clarity, not jargon.

---

## Plain-English translation guide (read once)

| If you see / think | Say it like this instead |
|:---|:---|
| Δ MACE | "the gap between polyphonic and monophonic accuracy" |
| `card(E_model) < card(E_ref ∩ E_audio)` | "the model misses sounds that both the captions and the audio say are there" |
| Chromaprint fingerprint | "audio fingerprinting" |
| MEMS microphone | "the cheap microphone in a phone" |
| Mechanical Turk crowdworkers | "online paid annotators" |
| SED (Sound Event Detection) | "an automatic sound-tagger" |
| FreeSound | "an open-source sound library" |
| Zero-shot evaluation | "we use the models out-of-the-box, no extra training" |
| AudioSet | "Google's giant sound-tag dataset that most LALMs train on" |
| `librosa.stft` | "the standard Python library for audio spectrograms" |

---

## Confidence pivots (use when stuck on a Q&A)

Memorize these 5. Each one buys you 5–10 seconds and looks expert:

1. **"That's a great question — let me frame it through the contamination lens."** → then talk contamination.
2. **"The honest answer is that we'll know after the audit."** → applies to anything about LALM performance.
3. **"That's covered in P3 / the term paper — out of scope for this milestone."** → applies to fine-tuning, multilingual, music, etc.
4. **"There's a fallback in my plan for exactly that case."** → audit fails, manifest closed, etc.
5. **"Per Lecture 4, the standard answer here is…"** → for any data-strategy concept (FAIR, GSP, weak/strong labels).

---

# THE TALK — slide by slide

## 🟦 TITLE SLIDE · 00:00 → 00:15

**Stage**: walk to front · click to title · 2 seconds silence · eye contact with prof.

★ **"Good morning. My project is Audio-to-Text Captioning with Large Audio-Language Models — milestone two of five."**

★ **"Last time, I named contamination as my Risk to Watch. Today closes that loop."**

*Click straight to Slide 1.*

**If you freeze**: "Today is P2 — my data acquisition strategy."

---

## 🟦 SLIDE 1 · TEST CORPUS · 00:15 → 00:55 *(40 s)*

★ **"My choice is Clotho v2.1."**

**Anchors — free-style around these (pick 3 in your own words)**:
- Official DCASE Task 6 benchmark → direct leaderboard comparison
- **5 captions per clip** — dense annotation, lets us detect missed sounds
- FreeSound-sourced, *not* AudioSet → much lower contamination risk
- On Zenodo with a DOI, **CC-BY 4.0**, fully **FAIR**

**Numbers that must be precise**: **5 captions per clip** (vs. 1 in AudioCaps) · **Zenodo record 4783391**

**Why-not-the-others (one-liners, point at the rejection column)**:
- AudioCaps → built from AudioSet → most LALMs trained on it
- AudioSetCaps → same family, same problem
- WavCaps → web-scraped, overlap risk
- Cacophony → that's training data, not an evaluation benchmark

★ **"The ALM Datasets Survey 2025 calls this the zero-shot illusion. This deck makes our choice defensible against that illusion."**

**Transition**: "Now — how was Clotho actually collected?" → click to Slide 2.

**If you freeze**: "Clotho is the DCASE benchmark, FreeSound-sourced, five captions per clip. Everything else has contamination."

---

## 🟦 SLIDE 2 · ACQUISITION (mics?) · 00:55 → 02:00 *(65 s)*

★ **"The honest answer to 'which mics?' is all of them."**

**Anchors**:
- Clotho was **curated, not recorded** — Tampere team assembled it from FreeSound uploads
- Every clip carries the original uploader's recording device
- Studio condensers, field recorders, phones with cheap built-in mics — *all of them*
- Lecture 4 calls this **device mismatch** — for us it's a built-in property, not a flaw
- Real deployment audio is also mixed devices → Clotho is more realistic, not less

**Point at the contrast strip (bottom of slide)**:

★ **"Same nominal sound — rain — three corpora. The difference is visible."**

- Clotho → clean, 15–30 s, mono WAV
- AudioCaps → 10 s YouTube clips, encoding artifacts
- WavCaps → web-scraped, length and quality vary wildly

**Transition**: "OK — but what does Clotho actually look like as a dataset?" → Slide 3.

**If you freeze**: "Clotho is community-curated from FreeSound. Mixed mics is honest, not a bug. The strip shows three corpora side by side."

---

## 🟦 SLIDE 3 · PROPERTIES + ANNOTATION · 02:00 → 02:55 *(55 s)*

★ **"Five captions per clip. Annotation is weak — clip-level, no time-stamps."**

**Numbers from the properties card** (read straight off the slide, don't memorize):
- **44.1 kHz**, mono, 16-bit WAV
- **15 to 30 seconds** per clip
- **~6,974 clips** across dev/val/eval splits
- **5 captions per clip**, **8–20 words** each
- Open vocabulary, no fixed taxonomy

★ **"Weak labels means clip-level only — no start-and-end times. Strong labels exist in DCASE Task 4. We'll derive them ourselves later, with a sound-tagger."**

**Point at the canonical Clotho panel** (waveform + spectrogram):

★ **"This is the spectrogram, made with librosa.stft — the standard Python library."**

(Pronunciation: **li-BRO-sa dot S-T-F-T**.)

**Transition**: "How will I detect when the model misses sounds?" → Slide 4.

**If you freeze**: "44 kHz, mono, 15-to-30 seconds. Five captions per clip. Weak labels. Spectrograms via librosa."

---

## 🟦 SLIDE 4 · CLASSES + THE POLYPHONY TEST · 02:55 → 04:00 *(65 s)*

★ **"Clotho has no fixed taxonomy. I derive the classes from the captions."**

**Top-20 bar chart (point at it)**:
- Music, water, traffic dominate. Long tail beyond that.
- Eventually I replace this with an automatic sound-tagger (PaSST or PANNs) for the polyphony split.

**Mono / Poly panels (point at the two side-by-side)**:

★ **"Monophonic — one source. Polyphonic — two or more overlapping sources."**

*(Click the audio icon on the mono panel if the room is quiet enough — let it play 2 seconds, then talk over it briefly.)*

**Bottom band — the formula** (point but don't read it letter-by-letter):

★ **"A clip is under-described when the model lists fewer sounds than the audio actually contains. That's the definition of failure I'm measuring."**

★ **"Delta MACE — the gap between polyphonic and monophonic accuracy — is my answer to research question two."**

**Transition**: "What's the biggest risk to all of this?" → Slide 5.

**If you freeze**: "Polyphony bucket vs. mono bucket. Delta MACE is the difference. The formula at the bottom defines under-description."

---

## 🟦 SLIDE 5 · RISKS + PATH TO EVALUATION · 04:00 → 04:40 *(40 s — the climax)*

**Slow down. This is what the prof is waiting for.**

★ **"P1 closed with contamination as my Risk to Watch. Here is how I close that loop."**

**Audit anchors (point at the bullets, pick 2)**:
- Audit covers **only the 3 LALMs** — Falcon3, SALMONN, Qwen2.5-Omni. Baselines are fine, their training data is small and known.
- **Per-model, not aggregated** — otherwise we hide the differences between models.
- **Falcon3's training manifest is public** — that's its key selling point. File-by-file audit is possible.
- SALMONN and Qwen → fall back to **audio fingerprinting + caption overlap**.

**Empirical wedge — point at the big numbers**:

★ **"FD-DeCap reports SPIDEr of 0.282 on Clotho versus 0.429 on AudioCaps — even after debiasing. The contaminated corpus scores 50 percent higher. That's the evidence for choosing Clotho."**

**Numbers that must be precise**: **0.282** · **0.429** · ~**50%** gap · DCASE baseline **29.6%**

**Closing line** *(after pausing 1 second)*:

★ **"Thank you. I am happy to take your questions."**

*Stay near the screen. Don't move until the first question.*

**If you freeze**: "Three-layer audit, per model. Falcon3's manifest is public. FD-DeCap shows a fifty-percent gap. Thank you."

---

# Q&A — pre-loaded answers

> **Format per question**: trigger line · 1-sentence answer (the one you'd say) · evidence to back it · pivot if pushed.

## The 6 questions you're most likely to get

### "Why Clotho over AudioCaps?"
- **Answer**: "Three reasons: it's the official DCASE benchmark, it has 5 captions per clip versus 1, and it's not built on AudioSet — which most LALMs train on."
- **Evidence**: FD-DeCap's 0.282 vs 0.429 SPIDEr gap.
- **If pushed**: "Even with debiasing, AudioCaps scored 50% higher — that's empirical proof of the contamination effect."

### "Which microphones?"
- **Answer**: "All of them — Clotho is FreeSound-sourced, so it's a mixture of studio mics, field recorders, and phones."
- **Evidence**: Lecture 4 calls this device mismatch.
- **If pushed**: "That's honest. Real deployment audio is also mixed. We can't control mics without recording our own data — which is out of scope for zero-shot evaluation."

### "Why no own recordings?"
- **Answer**: "The project is zero-shot evaluation of pre-trained LALMs. Recording our own data would be a different research question."
- **Pivot**: If pushed, fall back to "That's what P3 or the term paper could explore."

### "Weak vs. strong labels?"
- **Answer**: "Clotho is weak — clip-level captions, no time-stamps. We derive strong-label-like information later, with an automatic sound-tagger."
- **Evidence**: Lecture 4 slide 10 introduces this distinction directly.

### "How will you measure polyphony?"
- **Answer**: "Two or more overlapping sound classes for at least one second. We bucket each clip as mono or poly, then compute Delta MACE — the accuracy gap between buckets."
- **Evidence**: P1 Q&A item 14 defined this formally.

### "Is 5 captions per clip enough?"
- **Answer**: "It's a floor, not a ceiling. We combine the 5 captions with automatic sound-tagging to triangulate which sounds were actually in the clip."

### "Why zero-shot? Is that from the literature?" *(likely follow-up — be ready)*
- **Answer (one sentence)**: "Zero-shot is a deliberate scope decision, not a literature mandate. Three reasons: I'm characterising how these models actually behave when deployed; fine-tuning would confound the model-vs-model comparison; and zero-shot results are reproducible — anyone with the public weights can re-run them."
- **Evidence**: PROJECT_GUIDE.md explicitly lists *"training new models or fine-tuning LALMs"* as out of scope. The Falcon3-Audio, SALMONN, and Qwen2.5-Omni papers all report Clotho/AudioCaps SPIDEr as the pretrained model's out-of-the-box behaviour — that's the field convention for cross-corpus AAC reporting.
- **If pushed on "but the CNN14 baseline is fine-tuned on Clotho"**: "Yes — I acknowledge the asymmetry. The CNN14 number is a leaderboard reference, not an apples-to-apples competitor. What I'm really measuring is: do the three LALMs, used as the world deploys them, match or beat a fine-tuned tagger? If they do, it's a strong claim. If they don't, that's also informative."
- **If pushed on "the zero-shot illusion"**: "That's exactly the threat the ALM Datasets Survey 2025 raises — and it's precisely why my P2 includes the contamination audit on slide 5. The audit is what makes the zero-shot claim defensible, not just assumed."

## Other questions to be ready for (skim, don't memorize)

| Trigger | 1-line answer |
|:---|:---|
| "What if a manifest is closed?" | "We skip layer 1 for that model — Chromaprint and n-gram overlap still work." |
| "Aggregated vs per-model contamination?" | "Per-model — P1's open question was whether the three LALMs fail polyphony the same way. Aggregation hides the answer." |
| "Spectrogram parameters?" | "n_fft 1024, hop 512, 64 mel bins, in decibels — librosa.stft as the lecture specifies." |
| "Privacy / PETs?" | "Clotho has no speech retained — privacy isn't a concern. It would be if we recorded our own data." |
| "What about music?" | "Out of scope — harmonic polyphony is harder. Environmental sounds only." |
| "What if contamination is heavy?" | "We report on the clean subset and discuss contamination separately. The study isn't invalidated." |
| "What if the hypothesis is wrong?" | "A negative result is publishable too — either way we answer the research question." |
| "Where will inference run?" | "Falcon3 on a single 24 GB GPU. Qwen2.5-Omni on the cluster or a rented A100. Inference only." |
| "Hallucination vs creative-but-correct?" | "Hallucinated means it fails BOTH the audio-grounded check and the caption check. MACE handles this." |
| "English-only captions?" | "Yes — Clotho is English. Multilingual extension is out of scope here." |
| "All team members shall present?" | "I'm solo, registered as Mat. 2177213. So presenter equals author." |

## Two appendix triggers (you control which slide you flip to)

### "What does AudioCaps actually look like?"
*[Navigate forward to Appendix A.]*
- **Say**: "Five representative AudioCaps clips. Each one is 10 seconds of YouTube taken from AudioSet. Notice the YouTube encoding artifacts in the spectrograms — and the captions are single-annotator. That's the third reason Clotho is preferred."
- *[Click back to Slide 5 to close.]*

### "And WavCaps?"
*[Navigate forward to Appendix B.]*
- **Say**: "SoundBible — the most curated of WavCaps's four sub-sources. Captions are LLM-generated from web metadata, not human-verified. And the FreeSound sub-source of WavCaps overlaps the exact platform Clotho is sourced from — direct contamination risk."
- *[Click back to Slide 5.]*

---

# Emergency cuts (if you're past 03:00 at end of Slide 3)

| Slide | What to cut | Time saved |
|:---|:---|:---:|
| 4 | Don't click the audio sample, just point at it | 10 s |
| 4 | Skip reading the formula — just say the "under-described" line | 15 s |
| 5 | Drop the FD-DeCap empirical wedge → go straight to "thank you" | 15 s |
| 2 | Cut the WavCaps third panel, compare Clotho and AudioCaps only | 10 s |

**Total possible save: ~50 s.**

**Never cut**: *Clotho v2.1, contamination, Falcon3-Audio's public manifest, Delta MACE, FD-DeCap 0.282 vs 0.429, and "Thank you — I am happy to take your questions."*

---

# Pronunciation cheat-box

| Word on slide | Say it like this |
|:---|:---|
| Clotho | **KLOTH**-oh |
| FreeSound | FREE-sound |
| Chromaprint | **KROW**-ma-print |
| Falcon3-Audio | **FAL**-kon-three AW-dee-oh |
| SALMONN | **SAL**-monn (rhymes with "salmon") |
| Qwen2.5-Omni | **KWEN** two-point-five **OM**-nee |
| Polyphony | po-**LIH**-fo-nee |
| Δ MACE | **DEL**-ta **MAYS** |
| SPIDEr-FL | **SPI**-der F-L |
| `librosa.stft` | li-**BRO**-sa dot S-T-F-T |
| Drossos | **DROSS**-os |
| Tampere | **TAM**-per-eh (Finnish city) |
| FAIR | F-A-I-R (spelled out, four letters) |

---

# Dry-run timing log

| Slide | Target end | Run 1 | Run 2 | Notes |
|:---|:---:|:---:|:---:|:---|
| Title | 00:15 | __ : __ | __ : __ | Two beats silence at the start. |
| 1 | 00:55 | __ : __ | __ : __ | Open with "my choice is Clotho v2.1". |
| 2 | 02:00 | __ : __ | __ : __ | Point at the contrast strip — don't read it. |
| 3 | 02:55 | __ : __ | __ : __ | Don't list every number — read off slide. |
| 4 | 04:00 | __ : __ | __ : __ | The formula explanation is the climax of this slide. |
| 5 | 04:40 | __ : __ | __ : __ | "Thank you" — then stop and stay. |
| **TOTAL** | **04:40** | __ : __ | __ : __ | Target window 4:30 – 4:50. Hard ceiling 5:00. |

---

# What the prof is grading (per Lecture 04 brief)

| Required item | Where it lives in your deck |
|:---|:---|
| Metadata, acquisition strategy, mics | Slide 1 + Slide 2 |
| Classes, #examples per class | Slide 4 (top-20 bar chart) |
| Sample rate, format, file duration | Slide 3 (properties card) |
| Annotation type (weak / strong) | Slide 3 (right column) |
| Audio examples + spectrogram (`librosa.stft`) | Slide 3 canonical + Slide 4 mono/poly panels |
| All team members shall present | Solo project (Mat. 2177213) — presenter = author |

**All six required items are visibly on the deck — you have nothing to hide and nothing to invent. Just point and talk.**
