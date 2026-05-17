# P2 Slide Deck — Claude Design brief

**How to use this file**: paste it (in full) into Claude Design at claude.ai. Then upload the PNGs from `deliverables/p2/figures/` when Claude Design asks for image assets. The brief is structured slide-by-slide; each slide block lists its **text**, its **visuals**, and its **design intent** so Claude Design has everything it needs in one pass.

---

## Deck-level brief

- **Title**: P2 — Data Acquisition Strategy
- **Audience**: Prof. Dr.-Ing. Jakob Abeßer + the CH-Proj-M cohort, Uni Bamberg
- **Author**: Zuraiz · Mat. 2177213
- **Date**: 2026-05-18
- **Talk length**: 5 min talk + 5 min Q&A
- **Slide count**: 5 content slides + 1 references slide = 6 total. Plus 2 **Q&A-only appendix slides** at the end (only shown if the prof asks "what do those rejected datasets look like?"). The main deck stays inside the 5-slide cap.
- **Slide ratio**: 16:9 widescreen
- **Visual language**: match the P1 deck — clean academic, generous whitespace, navy `#1f2a44` and accent blue `#3a5fcd`, warning red `#c25a4f`, single sans-serif (Inter or similar). No stock photos. No clip-art. No emojis. Plot images on a white background.
- **Footer**: every slide bottom-left in 8pt grey: `Zuraiz · P2 · 2026-05-18`. Bottom-right: `slide N / 6`.
- **Header**: top-right corner shows the same three-line mark used on P1 (subtle, low-emphasis).
- **Tone**: factual, no marketing language. The deck is *evidence about a dataset*, not a pitch.

---

## SLIDE 1 — Clotho v2.1 · what & why

### Headline (top-left, ~30pt bold navy)
**Clotho v2.1 — and why it is the right test corpus**

### Subhead (~14pt, light italic, grey)
Zero-shot evaluation ⇒ no recording. The question is *which test corpus*.

### Body (left column, three short bullets, ~14pt navy)
- **DCASE Task 6** official benchmark — leaderboard parity
- **5 captions per clip** — dense annotation enables under-description detection
- **FreeSound-sourced**, *not* AudioSet — lower contamination risk than AudioCaps

### Rejection band (right column, four short bullets, ~12pt grey, prefixed with a small red ×)
Datasets considered and rejected:

- × **AudioCaps** — derived from AudioSet (LALM training overlap)
- × **AudioSetCaps** — same AudioSet family
- × **WavCaps** — web-scraped, overlap risk with Clotho/AudioCaps
- × **Cacophony** — contrastive training corpus, not eval benchmark

### Bottom band (full width, dark navy fill, white text, 12pt)
The ALM Datasets Survey 2025 calls the unverified-pretrain-overlap problem the **"zero-shot illusion"**. This deck makes our test-corpus choice defensible against that illusion.

### Visuals on this slide
- **Bottom-left**: clip-duration histogram → `figures/clip_duration_hist.png`
- **Bottom-right**: caption-length histogram → `figures/caption_length_hist.png`
- **Top-right small badges**: Zenodo DOI badge + "CC-BY 4.0" + "FAIR" pill labels

---

## SLIDE 2 — Acquisition · which mics?

### Headline
**Acquisition — community-curated, heterogeneous devices**

### Subhead
The honest answer to "which mics?" is *all of them*. Device mismatch (Lecture 04) is built in.

### Body — three-paragraph flow (narrative-style, not bullets)
Clotho was *curated*, not *recorded*. Drossos, Lipping, Virtanen at Tampere University assembled the corpus from **FreeSound** uploads. The dataset team's contribution is the captions, not the audio — every clip carries the original uploader's recording device.

This means the corpus inherits **device mismatch** as a built-in property. Studio condenser mics, field recorders, mobile phones with MEMS microphones — Clotho is a sample of *all of them*. Lecture 04 flags this as a generalisation hazard; we treat it as a realistic property of deployment audio rather than a flaw.

For visual contrast, the strip below shows the **same nominal sound (rain)** rendered from three corpora — Clotho, AudioCaps, WavCaps. Length, signal-to-noise ratio, and recording quality differ visibly.

### Visuals on this slide
- **Top-right inset (small)**: studio-mic vs. MEMS-mic image strip — *re-use the images from Lecture 04 slides 6–7 with explicit credit "B2, B3 © RØDE / eetasia.com via Lecture 04"*
- **Bottom row (3 panels, side by side)**: contrast strip — each panel = waveform + log-mel spectrogram + 1-line caption + "Clotho / AudioCaps / WavCaps" header
  - `figures/contrast_clotho_rain.png`
  - `figures/contrast_audiocaps_rain.png`
  - `figures/contrast_wavcaps_rain.png`

---

## SLIDE 3 — Audio properties + annotation

### Headline
**Audio properties + annotation**

### Subhead
Weak-label benchmark, 5 captions per clip, `librosa.stft` for spectrograms.

### Left column — properties card (use the rendered infographic, no retyping)
Replace the column with the `figures/audio_properties_card.png` image directly. The card lists: sample rate (44.1 kHz), channels (mono), bit depth (16-bit), format (WAV PCM), duration (15–30 s), captions per clip (5), caption length (8–20 words), vocabulary (open), licence (CC-BY 4.0), distribution (Zenodo record 4783391 — FAIR).

### Right column — annotation block
**Annotation type: weak** (clip-level, no time-stamps).

Five human-written captions per clip, 8–20 words each, crowdsourced via Amazon Mechanical Turk from English-speaking annotators. Post-processed to remove unique words, named entities, and speech transcription — Clotho is **not** a speech corpus.

Strong (segment-level) labels are derived later via PaSST/PANNs SED.

### Visuals on this slide
- **Left column (full-height)**: `figures/audio_properties_card.png`
- **Right column, lower half**: a small inset of the **weak-vs-strong-label diagram** — re-use Lecture 04's slide-10 SED-vs-AT image (B6, B7) with credit "© DCASE 2018/2020 via Lecture 04"
- **Right column, top**: one canonical Clotho clip panel — waveform + log-mel spectrogram + caption → `figures/canonical_clotho.png`

---

## SLIDE 4 — Classes + examples + the polyphony test

### Headline
**Sound classes, examples — and how I will detect under-description**

### Top band — top-20 AudioSet classes
Left side: `figures/top20_class_bar.png` (bar chart). Right side, two short lines:

- Open-vocabulary captions → no fixed taxonomy. Pseudo-classes derived by **PaSST / PANNs CNN14** tagging on the dev split.
- Long-tail distribution dominated by *music*, *water*, *traffic*.

### Middle band — mono vs. poly contrast
Two side-by-side example panels. Each panel: caption text · waveform · log-mel spectrogram (via `librosa.stft`, n_fft=1024, hop=512, 64 mel bins, dB).

- Left: `figures/mono_example.png` labelled **Monophonic**
- Right: `figures/poly_example.png` labelled **Polyphonic**

### Bottom band — the formal test (rendered as a centered LaTeX-style formula on dark navy fill, white text)

**Under-description test for RQ2 (Δ MACE):**

A clip is under-described iff
&nbsp;&nbsp;&nbsp;&nbsp;**card(E_model) &lt; card(E_ref ∩ E_audio)**
where E_audio = SED-detected event set, E_ref = union over the 5 reference captions, E_model = the model's output entities.

(Two-line caption under the formula: "From P1 Q&A Q14. Δ MACE = fraction of under-described clips in the polyphony bucket − the same fraction in the mono bucket.")

### Visuals on this slide
- `figures/top20_class_bar.png` (top-left)
- `figures/mono_example.png` (middle-left)
- `figures/poly_example.png` (middle-right)
- Optional: 2–4 class gallery panels along the bottom if space permits → `figures/gallery_*.png` thumbnails

---

## SLIDE 5 — Risks + path to evaluation

### Headline
**Risks I am closing on this slide**

### Top band — explicit P1 callback (italic, 14pt)
> P1 closed with **Contamination** as my Risk to Watch and an **Open Question**: do the three LALMs fail polyphony the same way, or differently? Both shape this slide.

### Left half — three-layer audit diagram
Use the rendered `figures/audit_diagram.png` directly. To its right, a tight bullet block:

- **Audit scope**: the 3 LALMs only (Falcon3-Audio · SALMONN · Qwen2.5-Omni). The 3 traditional baselines (CNN14 / AST / EnCLAP) use small, fully-known training corpora — no contamination concern.
- **Per-model, not aggregated**. Aggregation hides differential failure modes.
- **Falcon3-Audio's manifest is public** — its key sell. File-ID layer is fully usable there. For SALMONN / Qwen2.5-Omni, Chromaprint fingerprinting + caption n-gram cover the gap.

### Right half — empirical wedge (small callout box, light grey fill, dark text)
**FD-DeCap (IEEE TASLP 2025, doc 11333308)** reports SPIDEr after causal-inference debiasing:

- **Clotho: 0.282**
- **AudioCaps: 0.429**

The contaminated corpus scores ~50% higher — the direct empirical wedge for the Clotho choice.

### Bottom band — 8-week Gantt
Use the rendered `figures/gantt_8week.png` directly. One-line caption below:
*DCASE 2024 baseline SPIDEr-FL ≈ 29.6% — our reference value at first evaluation.*

### Footer line (small italic, right-aligned)
Out of scope: original recording (zero-shot protocol).

### Visuals on this slide
- `figures/audit_diagram.png` (left half)
- `figures/gantt_8week.png` (bottom band)

---

## SLIDE 6 — References (IEEE format)

A single column, two rows of references. Each in IEEE format, monospace numerical labels `[1]–[8]`.

[1] Drossos, K., Lipping, S., Virtanen, T. "Clotho: An Audio Captioning Dataset." *IEEE ICASSP*, 2020. Zenodo record 4783391 (v2.1).

[2] Falconi et al. "Competitive Audio-Language Models with Data-Efficient Single-Stage Training on Public Data (Falcon3-Audio)." *IEEE ASRU*, 2025. doi:10.1109/ASRU.2025.11434596.

[3] Dixit et al. "MACE: Leveraging Audio for Evaluating Audio Captioning Systems." *IEEE ICASSP-W*, 2025. doi:10.1109/ICASSPW.2025.11011270.

[4] IEEE ASRU 2025. "Data Leakage Benchmark." doi:10.1109/ASRU.2025.11450559.

[5] Mei et al. "Beyond the Status Quo: Critical Reflection on Audio Captioning Metrics." *IEEE/ACM TASLP*, 2023. doi:10.1109/TASLP.2023.3321968.

[6] Dixit / Khare et al. "FD-DeCap: A Front-Door Causal Inference-Based Framework for Debiasing Audio Captioning." *IEEE/ACM TASLP*, 2025. doi:10.1109/TASLP.2025.11333308.

[7] Kong et al. "PANNs: Large-Scale Pretrained Audio Neural Networks for Audio Pattern Recognition (CNN14)." *IEEE/ACM TASLP*, vol. 28, pp. 2880–2894, 2020. doi:10.1109/TASLP.2020.3030497.

[8] Prof. J. Abeßer. *CH-Proj-M Lecture 04 — Data in Machine Listening*, Uni Bamberg, SS 2026 (course material).

### Footer note (small italic, centred)
Shortlist of 8 data-strategy references from the project's 49-paper corpus. Full corpus + 38 read papers indexed in the project wiki.

---

---

## APPENDIX A (Q&A only) — What AudioCaps looks like

### Headline
**AudioCaps — five representative clips**

### Subhead (small italic)
*Not in the main deck. Shown only if Prof. Abeßer asks "and what does AudioCaps actually look like?"*

### Body — short intro line
AudioCaps is derived from 10-second YouTube segments of **AudioSet**. Captions are single-annotator. Below are five clips spanning common categories — note the strong YouTube-encoding artifacts and uneven SNR.

### Visuals — 5-panel grid (2 + 3 layout, each panel = waveform + log-mel spectrogram + caption)
- `figures/audiocaps_gallery_rain.png` — *"Rain is falling continuously."*
- `figures/audiocaps_gallery_dog.png` — *"A man speaks as birds chirp and dogs bark."*
- `figures/audiocaps_gallery_water.png` — *"A man talking as a stream of water trickles in the background."*
- `figures/audiocaps_gallery_vehicle.png` — *"A rocket flies by followed by a loud explosion and fire crackling as a truck engine runs idle."*
- `figures/audiocaps_gallery_music.png` — *"Music and a man speaking followed by bleeps and someone singing."*

### Bottom footnote (small grey italic)
Captions in this corpus are **single-annotator**, which is one of the three reasons Clotho (5 captions per clip) is preferred.

---

## APPENDIX B (Q&A only) — What WavCaps / SoundBible looks like

### Headline
**WavCaps (SoundBible subset) — six representative clips**

### Subhead (small italic)
*Q&A-only. Shown if asked "and WavCaps?"*

### Body — short intro line
WavCaps is a 400K-clip web-scraped corpus combining four sub-sources (AudioSet_SL, BBC Sound Effects, FreeSound, **SoundBible**). The SoundBible subset shown here is the most curated; the FreeSound subset overlaps directly with Clotho's source platform — a contamination risk.

### Visuals — 6-panel grid (2 × 3)
- `figures/wavcaps_gallery_rain.png` — *"Light rain and crickets at sunset."*
- `figures/wavcaps_gallery_dog.png` — *"A dog is barking."*
- `figures/wavcaps_gallery_music.png` — *"A music box is playing."*
- `figures/wavcaps_gallery_water.png` — *"Water is being poured into a glass."*
- `figures/wavcaps_gallery_vehicle.png` — *"An old car's engine is starting and running."*
- `figures/wavcaps_gallery_voice.png` — *"Someone is talking about their child pretending to be a superhero."*

### Bottom footnote (small grey italic)
WavCaps captions are **LLM-generated from web metadata** — they inherit any biases of the generating LLM, and the FreeSound subset overlaps Clotho's source. Both are reasons Clotho is preferred for a clean zero-shot benchmark.

---

## Asset upload manifest

When Claude Design asks for image assets, upload in this order from `deliverables/p2/figures/`:

**Main deck (slides 1–5):**

1. `clip_duration_hist.png` — slide 1
2. `caption_length_hist.png` — slide 1
3. `contrast_clotho_rain.png` — slide 2
4. `contrast_audiocaps_rain.png` — slide 2
5. `contrast_wavcaps_rain.png` — slide 2
6. `audio_properties_card.png` — slide 3
7. `canonical_clotho.png` — slide 3
8. `top20_class_bar.png` — slide 4
9. `mono_example.png` — slide 4
10. `poly_example.png` — slide 4
11. `gallery_1_mechanical_doorbell.png` — slide 4
12. `gallery_2_urban_siren.png` — slide 4
13. `gallery_3_nature_birds_+_wind.png` — slide 4
14. `gallery_4_indoor_mechanical_detail.png` — slide 4
15. `audit_diagram.png` — slide 5
16. `gantt_8week.png` — slide 5

**Q&A appendix slides:**

17. `audiocaps_gallery_rain.png` — appendix A
18. `audiocaps_gallery_dog.png` — appendix A
19. `audiocaps_gallery_water.png` — appendix A
20. `audiocaps_gallery_vehicle.png` — appendix A
21. `audiocaps_gallery_music.png` — appendix A
22. `wavcaps_gallery_rain.png` — appendix B
23. `wavcaps_gallery_dog.png` — appendix B
24. `wavcaps_gallery_music.png` — appendix B
25. `wavcaps_gallery_water.png` — appendix B
26. `wavcaps_gallery_vehicle.png` — appendix B
27. `wavcaps_gallery_voice.png` — appendix B

The two lecture re-use images (slide 2 mic comparison, slide 3 weak-vs-strong) can be screenshotted from `raw/00_course/CH-Proj-M-04-Audio_Datasets_Editing_Annotation.pdf` slides 6, 7, 10 — credit them on-slide as noted above.

---

## After Claude Design produces the deck

1. Export the result as a `.pptx` into `deliverables/p2/Zuraiz_P2_Data_Strategy.pptx`.
2. Open in PowerPoint locally and rehearse against [`p2_speaker_script.md`](p2_speaker_script.md) — confirm dry-run timing ≤ 5 min 15 s.
3. Embed the two audio samples (`audio_samples/mono_example.wav`, `audio_samples/poly_example.wav`) on slide 4 so playback is possible if Prof. Abeßer asks.
4. Final visual QA: every slide rendered, no overflow, footer correct, references slide all 8 entries present.
