# PROJECT LOGBOOK — Engineering Master Document

*CH-Proj-M · Audio-to-Text Captioning with LALMs · Uni Bamberg · Zuraiz (2177213)*
*Prof. Dr.-Ing. Jakob Abeßer · last updated: 2026-06-29*

---

## 0. How to use this document

This is the **single living record** of the engineering work on this project.
Read it top to bottom and you will understand — and be able to defend in the P3
oral — every line of code, every number, and every decision that was made.

- **It is updated at the end of every working session.** Each session adds a dated
  entry to §4, ticks/extends the checklist in §8, and records any new component
  (§3), decision (§6), or defense answer (§7).
- **Every number here is backed by a file in `results/`; every claim by a commit.**
  Nothing is asserted that the repository cannot prove.
- Sections 6 and 7 are your **defense kit** — the calls an examiner will probe and
  the short answers to give.

Scope: this logbook covers the **engineering work** (the traditional-baseline
pipeline). The literature review (P1, 4 May) and data-acquisition strategy (P2,
18 May) are background — see `PROJECT_GUIDE.md` and `deliverables/p1`, `p2`.

---

## 1. Project context (1 minute)

The course task **T6** asks: *how well can Large Audio-Language Models (LALMs)
describe audio — especially overlapping/polyphonic sound — compared to traditional
systems?* We answer it with three research questions:

| RQ | Question | Primary metric |
|:--|:--|:--|
| **RQ1** | Do LALMs match/beat traditional captioning baselines? | SPIDEr-FL, CIDEr |
| **RQ2** *(core)* | Do LALMs describe overlapping events as well as tagging? | Δ MACE (poly − mono) |
| **RQ3** | What are the failure modes (hallucination, temporal loss)? | CHAIR-audio |

Everything is **zero-shot** (no training) to fit a one-semester budget. The plan
is a comparison table: a few **traditional baselines** (CNN14, EnCLAP, AST) as the
floor, then the **LALMs** (Falcon3-Audio primary, SALMONN, Qwen2.5-Omni). This
logbook is about building and verifying that floor. Source-of-truth spec:
`PROJECT_GUIDE.md`.

---

## 2. The system at a glance

Every model implements **one contract** — `Captioner.caption(waveform, sr) -> str`
(`src/models/base.py`). A registry (`src/models/__init__.py`,
`MODEL_REGISTRY`) maps a config name (`cnn14`, `enclap`, `ast`) to a class, so the
same inference loop and scorer serve every row. Adding a model = write one wrapper +
one registry line + one config.

**Five-stage data flow:**

```
[1] Clotho-eval WAV + 5 human captions     src/data/clotho.py   (44.1 kHz mono)
        │
[2] audio features (mel / EnCodec+CLAP)     src/models/<row>.py
        │
[3] decoder → caption string                src/models/<row>.py  (BART, beam=4)
        │
[4] predictions JSON                        src/pipeline/run_inference.py
        │   ── handoff: Windows → WSL ──
[5] SPIDEr-FL / CIDEr / SPICE / …           src/metrics/score.py (WSL)
```

**Two deliberate splits** (both are defensible engineering, see §6):

1. **Two machines.** Inference runs on **Windows** (native Python, where audio +
   models live). Scoring runs in **WSL Ubuntu**, because the `aac-metrics` SPICE
   metric needs Java 8–13 and this host has Java 23. The predictions JSON is the
   handoff. WSL env: `.venv-wsl`, OpenJDK 11, `aac-metrics` 0.5.5.
2. **Two Windows environments.** CNN14 needs `transformers==4.41` (`.venv`);
   EnCLAP's vendored model only runs on `transformers==4.29` (`.venv-enclap`).
   They are mutually incompatible, so each row has its own venv + requirements file.

---

## 3. How each piece works (component deep-dive)

### Data — `src/data/clotho.py`
`ClothoEvalDataset` reads `clotho_captions_evaluation.csv` (columns
`file_name, caption_1…caption_5`) and the WAVs under
`clotho_audio_evaluation/evaluation/`. Each item returns
`{file_name, waveform (1×T float32 mono), sample_rate, references}`.
- **WHY 44.1 kHz (not 32 kHz):** it keeps Clotho's native rate. The generic
  "CNN14 wants 32 kHz" assumption is wrong for *these* weights — the upstream
  baseline trains at native rate. Resampling to 32 kHz would misalign every mel
  frame. (Proof: the reproduction matched the paper.)
- `filter_polyphony()` is a **stub** today (returns all clips); its signature is
  already shaped for the future SED-based polyphony subset (RQ2).

### Models
- **`base.py`** — the `Captioner` ABC. One abstract method, `caption(...)`. This
  is the contract that makes the pipeline model-agnostic.
- **`cnn14_dcase.py`** — wraps the vendored DCASE-2023 baseline. CNN14 encoder +
  HuggingFace BART decoder. Gotchas (all commented in code): it injects the vendor
  dir on `sys.path` (upstream is flat scripts); it inlines the log-mel function
  (the upstream module crashes on import because it reads a pickle at load time);
  it sets `forced_bos_token_id=0` (the checkpoint needs `<s>` forced first, else
  output is empty). The CNN14 encoder weights and the BART decoder weights live in
  **two separate Zenodo records** and must *both* load, or the audio tower stays
  random.
- **`enclap.py`** — wraps the vendored EnCLAP. Pipeline: **EnCodec** (24 kHz
  discrete audio codes) + **LAION-CLAP** (one audio embedding) → **BART** decoder.
  The vendored `EnClap` class already exposes `infer_from_audio(audio, sr)`, so the
  wrapper is thin. It strips the upstream `_from_model_config` generation key
  (rejected by transformers ≥4.30). EnCLAP resamples internally, so we hand it the
  same native 44.1 kHz.
- **`ast_tagging.py`** — wraps **AST** (`MIT/ast-finetuned-audioset-10-10-0.4593`)
  from `transformers` (no vendored repo, runs in `.venv`). AST is a 527-class
  AudioSet **tagger**, not a captioner: the wrapper resamples to 16 kHz, runs the
  classifier, takes the **top-5** labels (sigmoid, multi-label), cleans them, and
  wraps them in a template — "a sound of A, B, C, D and E". The *tagging floor*, not
  a real captioner. Limitation: AST truncates to ~10.24 s, so it only hears the
  first ~10 s of each clip.
- **`__init__.py`** — `MODEL_REGISTRY = {"cnn14": …, "enclap": …, "ast": …}`.
- **`_vendor/`** — `felixgontier/dcase-2023-baseline` pinned at commit `4f89d0b`
  (git submodule). **`_vendor_enclap/`** — `jaeyeonkim99/EnCLAP` pinned at
  `e4976a4`. We *vendor, never reimplement*: the model classes are upstream's,
  untouched, so we inherit the exact architecture.

### Pipeline — `src/pipeline/run_inference.py`
Loads a `configs/<row>.yaml`, seeds RNGs (42), resolves the model from the
registry, loops over the 1045 clips, and writes the predictions JSON. Robustness:
**atomic incremental flush** every 10 clips (crash at clip 800 keeps 1–799);
**per-clip try/except** (one bad file is skipped, not fatal); and a **manifest**
(`<row>_eval.manifest.json`) recording weight SHA256s, vendored commit, library
versions, decode/audio params, and seed — the reproducibility receipt. The
manifest hashes *any* init kwarg ending in `_ckpt`, so it is model-agnostic
(commit `da90315`).

### Metrics — `src/metrics/score.py` (runs in WSL)
Reads the predictions JSON, builds aligned candidate + reference lists, and calls
`aac_metrics.functional.evaluate`. Default preset `dcase2023` (the installed
aac-metrics 0.5.x has no `dcase2024`). `--subset <file>` restricts scoring to a
fixed list of `file_name`s — used to compare rows on the *same clip set*
(commit `979cea5`).

### Scripts & configs
- `scripts/download_weights.py` — CNN14 encoder + BART decoder (Zenodo, MD5-checked)
  and the LAION-CLAP checkpoint; idempotent, resumes by skip.
- `scripts/download_weights_enclap.py` — `gdown` the EnCLAP checkpoint from Drive.
- `scripts/cache_hf_assets.py` — pre-caches the BART tokenizer.
- `scripts/setup_wsl_metrics.sh` — apt OpenJDK 11 + `.venv-wsl` + aac-metrics jars.
- `configs/cnn14.yaml`, `configs/enclap.yaml` — single source of truth per row
  (weight paths, device, beams, seed). No magic numbers in code.

---

## 4. Chronological work log

### 2026-06-01 — CNN14 baseline built, corrected, documented
- **`c7c4ebf` feat(baseline)** — Built the whole pipeline (loader, `Captioner`
  ABC, CNN14 wrapper around vendored `felixgontier/dcase-2023-baseline`, inference
  loop + manifest, WSL scorer). **Result: SPIDEr-FL 0.2592** on 1045 clips vs
  published 0.261 — faithful reproduction.
- **Key correction discovered:** the spec called this the "DCASE **2024** CNN14
  baseline (29.6 %)". That was wrong on two counts — the 2024 baseline is
  **ConvNeXt** (not CNN14), and the real CNN14 is the **2023** baseline at
  **26.1 %**. Pivoted to the correct repo before writing any code.
- **`c89e53a` docs** — propagated 29.6 % → 26.1 % across `PROJECT_GUIDE.md`,
  `hypotheses_preregistered.yml` (H1 threshold), and the wiki.
- **`ac9e291` docs** — first README.
- **`979cea5` feat(metrics)** — `--subset` flag for same-clip-set comparisons.
- **`1c7ab7c`** — added the lecture-05 "Project Pipeline" PDF.

### 2026-06-03 — EnCLAP baseline + generalisation
- **`da90315` refactor** — made the run-manifest model-agnostic (hash any
  `*_ckpt`), so EnCLAP reuses the pipeline unchanged.
- **`18c00d2` feat(enclap)** — EnCLAP-base row: wrapper around vendored
  `jaeyeonkim99/EnCLAP`, isolated `.venv-enclap` (transformers 4.29), weights
  (CLAP fusion ckpt + Drive checkpoint). **Result: SPIDEr 0.2826** vs published
  ~0.283 — faithful; **beats CNN14 on every metric**.
- **`57b888c` docs** — README now covers both rows + the two-env rationale.

### 2026-06-29 — AST tagging baseline (the RQ1 floor)
- **feat(ast)** — AST AudioSet tagger as row 3, via `transformers` in `.venv` (no
  vendored repo, no weights download). Top-5 tags → "a sound of …" template. Also
  made `run_inference`'s decode-provenance model-agnostic (it no longer assumes
  beam-search keys, which a tagger lacks). **Result: SPIDEr-FL 0.0684** — ~4× below
  CNN14/EnCLAP, the expected tagging-floor ordering (AST ≪ CNN14 < EnCLAP). No
  published number to match (AST is not a captioner); success = behaviour + ordering.

---

## 5. Verified results

Full Clotho-eval (1045 clips), CPU, seed 42. Sources: `results/<row>_eval_scores.json`.

| Metric | AST (tag floor) | CNN14 (2023) | EnCLAP-base (2024) | What it measures |
|:--|:--|:--|:--|:--|
| **SPIDEr-FL** | 0.0684 | 0.2592 | **0.2801** | headline: CIDEr+SPICE blend, fluency-penalised |
| SPIDEr | 0.0831 | 0.2671 | 0.2826 | CIDEr+SPICE average |
| CIDEr-D | 0.1102 | 0.4162 | 0.4425 | n-gram overlap, TF-IDF weighted |
| SPICE | 0.0560 | 0.1181 | 0.1226 | scene-graph (objects/relations) match |
| METEOR | 0.0948 | 0.1756 | 0.1795 | unigram match with synonyms |
| Fluency-error (↓) | 0.1799 | 0.0287 | 0.0134 | how often the caption is disfluent |
| **vs published** | n/a (tagger) | ~0.261 ✓ | ~0.283 ✓ | captioners reproduce their papers |

**Reading it:** the ordering is **AST ≪ CNN14 < EnCLAP**. AST (pure tagging) scores
~4× lower than the real captioners — that gap is the RQ1 finding: naming events ≠
describing scenes. CNN14 and EnCLAP each land within ~0.005 of their published
numbers, which makes the harness *trustworthy* for the LALM rows to come. AST has
no paper number because it is a classifier, not a captioner — its high
fluency-error (0.18) reflects the disfluent tag-template.

---

## 6. Key decisions & corrections (your defensible calls)

| Decision | Why | Evidence |
|:--|:--|:--|
| **CNN14 = DCASE 2023, not 2024** | The 2024 baseline is ConvNeXt; the real CNN14 captioner is the 2023 Task-6A baseline. | Verified the two repos + Zenodo; reproduced 0.259 ≈ published 0.261. |
| **Baseline number 26.1 %, not 29.6 %** | 29.6 % is the 2024 ConvNeXt; quoting it for "CNN14" conflated two models. | Corrected in guide + hypotheses + wiki (`c89e53a`). |
| **Native 44.1 kHz, not 32 kHz** | The upstream weights are trained at native rate (`librosa.load(sr=None)`). | The reproduction matched — a wrong rate would have wrecked it. |
| **Vendor upstream, don't reimplement** | Inherit the exact architecture; zero transcription risk. | `strict=True` checkpoint load succeeded for both rows. |
| **Score in WSL** | `aac-metrics` SPICE needs Java 8–13; the host has Java 23. | SPIDEr computed cleanly under WSL OpenJDK 11. |
| **Isolated EnCLAP env** | Its `EnClapBart` only runs on transformers 4.29, incompatible with CNN14's 4.41. | Default install pulled transformers 5.9 → import failed; pinning 4.29 fixed it. |
| **H1 re-anchored pre-freeze** | The preregistration was never frozen (`freeze_date: null`), so fixing a factual error is **not HARKing**. | `hypotheses_preregistered.yml` + dated wiki `log.md` entry. |

---

## 7. Examiner Q&A (defense prep)

**Q: Your CNN14 baseline is fine-tuned on Clotho, but the LALMs are zero-shot.
Is that a fair comparison?**
A: The *dataset split* and *metric* are identical (Clotho-eval, SPIDEr-FL), so the
measurement is fair. The training regime differs on purpose — that is the thing we
study, not a hidden flaw. If a zero-shot LALM matches a fine-tuned tagger, that is
a *stronger* result, not a weaker one. We document this asymmetry openly.

**Q: How do you know your reproduction is correct?**
A: We re-ran the official baseline end to end and got SPIDEr-FL 0.259 vs the
published 0.261 — and every sub-metric within ~0.005. A wrong sample rate, vocab,
or weight load would have produced a much larger gap.

**Q: Why EnCLAP-*base* and not large?**
A: Base is the lighter model and still reproduces its paper number (0.283). Large
(~0.295) costs ~3× the compute for a small gain; base is enough to establish the
baseline floor. The pipeline can swap to large by changing one config path.

**Q: Why two Python environments?**
A: EnCLAP's released code is written for transformers 4.29; CNN14's wrapper uses
4.41. These versions are incompatible. Rather than fight it, each baseline runs in
its own isolated environment with pinned requirements — fully reproducible.

**Q: Why is the baseline the DCASE 2023 system when the slides said 2024?**
A: The 2024 baseline uses a ConvNeXt encoder, not CNN14. The CNN14 + Transformer
captioner is the 2023 Task-6A baseline. We corrected the label and the number
(26.1 %) everywhere, before the preregistration was frozen.

**Q: Why does AST score so low (0.068)? Is it broken?**
A: No — that low score is the point. AST is a *tagger*: it lists sound events
("a sound of dog, bark, animal") but cannot form a real description. Captioning
metrics reward fluent sentences, so a tag-list scores ~4× below the captioners.
AST is the *floor* that shows how much real captioning adds. We also feed it only
the first ~10 s of each clip, because that is AST's fixed input window.

---

## 8. Future checklist

**Done ✓**
- [x] CNN14 baseline — built, reproduced (SPIDEr-FL 0.2592), committed.
- [x] EnCLAP-base baseline — built, reproduced (SPIDEr 0.2826), committed.
- [x] **AST tagging baseline — built (SPIDEr-FL 0.0684, the floor), committed.**
- [x] **All three traditional baselines done** — the RQ1 comparison floor is complete.
- [x] Model-agnostic pipeline (Captioner ABC, registry, generalised manifest + decode).
- [x] `--subset` scoring for same-clip-set comparisons.
- [x] Numbers/labels corrected across guide, hypotheses, wiki.
- [x] README + this logbook.

**LALM rows** (the main project)
- [ ] **Falcon3-Audio** (primary) — needs cluster GPU access (asking Prof.).
- [ ] SALMONN, Qwen2.5-Omni.

**RQ2 / RQ3 track**
- [ ] **Polyphony SED subset** — PaSST/PANNs tagging → poly/mono split; activates
      `filter_polyphony()`.
- [ ] **MACE-F1** — separate metric stack (entity-level), for Δ MACE.
- [ ] **CHAIR-audio** — hallucination metric (RQ3).
- [ ] **RQ1 parity run** — score the baselines on the same CLEAN subset the LALMs use.

**Housekeeping**
- [ ] Merge `feat/cnn14-baseline` → `main`.
- [ ] `git gc` (clear loose-object warnings).
- [ ] Term paper (6 pp, due 6 Jul) · P3 defence (13 Jul).

---

## 9. Glossary & key facts to remember

- **Clotho v2.1** — the evaluation dataset; 1045 eval clips, 5 human captions each,
  15–30 s, native 44.1 kHz, FreeSound-sourced.
- **SPIDEr-FL** — the headline metric: average of CIDEr and SPICE, with a fluency
  penalty. Higher is better. DCASE Task-6 standard.
- **CIDEr / SPICE** — n-gram overlap / scene-graph match (the two halves of SPIDEr).
- **CNN14** — a 14-layer convolutional audio encoder (from PANNs); here paired with
  a BART decoder. The DCASE **2023** Task-6A baseline, **26.1 %** SPIDEr-FL.
- **EnCLAP** — EnCodec + CLAP + BART captioner (ICASSP 2024). Base ≈ **0.283** SPIDEr.
- **AST** — Audio Spectrogram Transformer (Gong 2021); a 527-class AudioSet
  **tagger** (not a captioner), the tagging floor at SPIDEr-FL **0.068**.
- **EnCodec / CLAP / BART** — neural audio codec / audio-text embedding model /
  the language-model decoder.
- **LALM** — Large Audio-Language Model (Falcon3-Audio, SALMONN, Qwen2.5-Omni).
- **The two repos we vendor** — `felixgontier/dcase-2023-baseline` (`_vendor`,
  `4f89d0b`) and `jaeyeonkim99/EnCLAP` (`_vendor_enclap`, `e4976a4`).
- **Magic numbers** — beam=4, seed=42, 1045 eval clips, 44.1 kHz, CNN14 26.1 % /
  EnCLAP 28.3 % published.
