# PROJECT LOGBOOK — Engineering Master Document

*CH-Proj-M · Audio-to-Text Captioning with LALMs · Uni Bamberg · Zuraiz (2177213)*
*Prof. Dr.-Ing. Jakob Abeßer · last updated: 2026-07-06*

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
floor, then the **LALMs** (Qwen2.5-Omni-7B, SALMONN-13B, Audio Flamingo 3). This
logbook covers building the floor **and** running the LALMs on a GPU cluster.
Source-of-truth spec: `PROJECT_GUIDE.md`.

> **LALM lineup — why these three.** Falcon3-Audio was the original primary pick
> but its **weights were never publicly released** (verified against the paper HTML,
> the author's HF page, and an HF model search — only the text-only Falcon3 exists).
> It was replaced by **Audio Flamingo 3** (NVIDIA), which ships natively in
> `transformers` 5.x. Final set: **Qwen2.5-Omni-7B** (done), **SALMONN-13B**,
> **Audio Flamingo 3** — one Alibaba, one Tsinghua/BLSP-family, one NVIDIA, so the
> comparison is not single-vendor.

---

## 2. The system at a glance

Every model implements **one contract** — `Captioner.caption(waveform, sr) -> str`
(`src/models/base.py`). A registry (`src/models/__init__.py`,
`MODEL_REGISTRY`) maps a config name (`cnn14`, `enclap`, `ast`, `qwen_omni`) to a
class, so the same inference loop and scorer serve every row — a laptop CPU
baseline and a 7B LALM on an A100 use the identical loop. Adding a model = write one
wrapper + one registry line + one config.

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
3. **A third machine for the LALMs — a GPU cluster.** The 7B+ LALMs do not fit on
   the laptop, so inference for those rows runs on **NHR@FAU TinyGPU** (A100 40 GB).
   The *same* `run_inference.py` + config + predictions-JSON contract runs there
   unchanged; only the venv and the compute move. Scoring still comes home to WSL.
   The cluster is offline on its compute nodes, so models are pre-cached and the run
   is fully deterministic (seed 42). Details in §3a.

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
- **`qwen_omni.py`** — wraps **Qwen2.5-Omni-7B** (Alibaba), the first LALM row. A
  multimodal (text/vision/audio/speech) model used **audio-only, text-only output**:
  the wrapper calls `disable_talker()` to drop the speech head and free VRAM. All
  transformers-5.x imports are **lazy** so the registry stays importable in the CPU
  envs that lack them. `qwen_omni_utils.process_mm_info` loads audio from a *path*,
  so `caption()` writes a short-lived temp WAV. bf16, greedy decode (`num_beams=1`,
  `max_new_tokens=64`). A `_strip_chat()` post-filter drops any trailing
  interrogative sentence — the model likes to append "What do you think?", which
  Clotho references never do; removing it lifts fluency (FER 0.005, near-zero
  SPIDEr→SPIDEr-FL penalty). Runs in `$WORK/envs/qwen` on the cluster (transformers
  5.13), **not** on the laptop.
- **`salmonn.py`** — wraps **SALMONN-13B** (Tang et al., ICLR 2024), the second LALM
  row, via vendored `bytedance/SALMONN` (`_vendor_salmonn`, `salmonn` branch, pinned
  `a58bba7`). Whisper-large-v2 + BEATs encoders → window-level Q-Former → Vicuna-13B
  + LoRA. Audio-only, fp16, `num_beams=4` (SALMONN's authored decode default). Lazy
  imports (its `transformers==4.28` stack lives only in the cluster conda env). The
  wrapper resamples Clotho's 44.1 kHz → 16 kHz (Whisper+BEATs) and `_clean()`s the
  `<s>/</s>` markers SALMONN's `generate()` returns. `from_config` loads the trained
  `salmonn_v1.pth` (Q-Former+LoRA) over random init; the encoders/LLM load from four
  local checkpoint paths, resolved from `$WORK` via OmegaConf `oc.env`.
- **`audio_flamingo3.py`** — wraps **Audio Flamingo 3** (NVIDIA), the third LALM row.
  Transformers-native `AudioFlamingo3ForConditionalGeneration`: a Whisper-style
  128-mel audio encoder + a Qwen2-7B decoder. Audio-only, greedy, **fp32** (its
  native dtype — bf16 caused an encoder dtype mismatch). Runs in the *same*
  transformers 5.x env as the Qwen row (no vendored repo, no new env). Same
  temp-WAV-path + 16 kHz resample pattern as the other LALMs.
- **`__init__.py`** — `MODEL_REGISTRY = {"cnn14": …, "enclap": …, "ast": …, "qwen_omni": …, "salmonn": …, "af3": …}`.
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
- `configs/cnn14.yaml`, `configs/enclap.yaml`, `configs/qwen_omni.yaml` — single
  source of truth per row (weight paths / model_id, device, beams, prompt, seed).
  No magic numbers in code.
- `jobs/qwen_smoke.sbatch`, `jobs/qwen_full.sbatch` — Slurm submission scripts for
  the cluster (partition `a100`, 1×A100, offline env, `nvidia-smi` receipt).
- `requirements-qwen.txt` — the LALM env (transformers ≥4.52, `qwen-omni-utils`,
  accelerate). Header documents the one cluster quirk: the site pytorch module ships
  **without** torchaudio/torchvision, so both are `pip install --no-deps` from the
  cu126 wheel index to match torch 2.6.0.

### 3a. The GPU cluster (NHR@FAU TinyGPU) — how the LALM rows run

- **Access path:** portal invite → SSH key (up to 2 h to propagate) → jump host
  `csnhr.nhr.fau.de` → frontend `tinyx.nhr.fau.de`. Account `barz144h`, project
  `barz101`. `~/.ssh/config` defines `csnhr` and `tinygpu` (the latter `ProxyJump`s
  through the former), so `ssh tinygpu` is one hop for us.
- **Hardware / scheduler:** `a100` partition = A100 40 GB, 1–4 GPUs/node, 24 h
  walltime, Slurm via `sbatch.tinygpu`. Qwen2.5-Omni-7B uses **~22 GB**, so 1 GPU.
- **The offline constraint (important):** compute nodes have **no internet**. So the
  model is pre-downloaded on the *frontend* into `$WORK/hf_cache` (22.4 GB), and jobs
  export `HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 HF_HOME=$WORK/hf_cache`. `$WORK` =
  `/home/woody/barz/barz144h` (the large quota; `$HOME` is tiny).
- **Data staging:** the 1045 Clotho eval WAVs were pushed with a **resumable
  tar-over-ssh loop** (`scratchpad/upload_clotho.sh`) — it diffs remote vs local
  `ls`, tars only the missing files, and retries on connection drops until
  `ls | wc -l == 1045`. Needed because a naïve upload died at 70/1045 on a reset.
- **Run:** `git clone` the repo (fine-grained GitHub token, Contents-read), build
  `$WORK/envs/qwen`, `sbatch` the smoke (5 clips) then the full job. **The
  predictions JSON + manifest are the only artefacts that come back** — scoring is
  identical to every other row (WSL, dcase2023). This is the whole point of the
  Captioner contract: the cluster is just a bigger `caption()`.

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

### 2026-07-04 — First LALM row: Qwen2.5-Omni-7B on the GPU cluster
- **Dropped Falcon3-Audio, added Audio Flamingo 3.** Falcon3-Audio's weights were
  never publicly released (verified: paper HTML, author HF page, HF model search —
  only the text-only Falcon3 exists). Replaced by NVIDIA **Audio Flamingo 3**, which
  is native in `transformers` 5.x. Final LALM set: Qwen2.5-Omni-7B, SALMONN-13B, AF3.
- **Cluster onboarding (NHR@FAU TinyGPU)** — see §3a: SSH key + jump host + frontend,
  `$WORK/envs/qwen` build, torchaudio/torchvision `--no-deps` fix, resumable upload of
  the 1045 WAVs, model pre-cached (22.4 GB) for offline compute nodes.
- **`qwen_omni` wrapper + config + sbatch** — audio-only, talker disabled, bf16,
  greedy. A `_strip_chat()` post-filter + a firm prompt kill the model's chatty
  trailing questions (verified: **zero** trailing `?` in the full run).
- **Full run** (job `1729803`, 1×A100): **1045/1045 items, 0 failures, 8.3 min**.
  `results/qwen_omni_eval.json` + manifest downloaded home.
- **Scored in WSL** (dcase2023). One fix along the way: SPICE's JVM (`-Xmx8G`) was
  **OOM-killed** on the 16 GB laptop (WSL default 2 GB swap); added a
  `C:\Users\zurai\.wslconfig` with 16 GB swap so the heap spills to disk not dies.
- **Result: SPIDEr-FL 0.1880.** Sits **above the AST tagging floor** (0.068, ~2.7×)
  but **below both trained captioners** (CNN14 0.259, EnCLAP 0.280). This is the RQ1
  headline: a zero-shot LALM does not beat an in-domain-trained captioner on Clotho's
  own overlap metrics. Fluency is near-perfect (FER 0.005), so the gap is genuine
  content/style mismatch, not disfluency.

### 2026-07-04 — Second LALM row: SALMONN-13B on the GPU cluster
- **Verified everything from upstream source before coding** (Falcon3 lesson): the
  four checkpoints, the fp16-no-quant default, and that `from_config` loads the
  trained `salmonn_v1.pth` (Q-Former + LoRA) or the row emits garbage. Wrapper around
  vendored `bytedance/SALMONN` (`salmonn` branch, pinned `a58bba7`): Whisper-large-v2
  + BEATs → window-level Q-Former → Vicuna-13B + LoRA, audio-only, `num_beams=4`.
- **Own isolated env.** SALMONN pins `transformers==4.28.0` / `torch==2.0.1`, needing
  Python ≤3.10 — incompatible with the cluster's 3.12 and the Qwen env. Built a
  conda **Python 3.10** env (`$WORK/envs/salmonn`), torch 2.0.1 cu118. Cleared four
  cluster quirks: conda `defaults`-channel ToS (→ `conda-forge`), read-only pkgs
  cache (→ `CONDA_PKGS_DIRS` on `$WORK`), `pkg_resources` missing (→ `setuptools<81`
  for old accelerate), and offline `bert-base-uncased` (Q-Former reads its config —
  pre-cached it + set `HF_HOME`).
- **BEATs checkpoint rescued.** The authoritative `cpt2` file lives on a **dead
  OneDrive link** (migrated to SharePoint, 403). Found + **structurally verified** an
  exact HF mirror (`WeiChihChen/…cpt2`; correct `cfg`/`model`/`label_dict` keys,
  genuine BEATs weight names).
- **Two fix-retry cycles** (each ~6 min because loading 13 B from disk precedes any
  error): missing `bert-base-uncased`, then `<s>/</s>` markers in `generate()` output
  (added `_clean()`, verified on the smoke captions).
- **Smoke (5 clips)** produced coherent captions ("A bike bell is ringing.") →
  `salmonn_v1.pth` loaded correctly; fits on **one A100-40 GB** (no 2-GPU needed).
- **Full run** (job `1731381`, 1×A100): **1045/1045, 0 failures, ~19 min.**
- **Result: SPIDEr-FL 0.2246** — **beats Qwen (0.188)** and sits between it and CNN14
  (0.259). The audio-specialist 13 B model outperforms the general omni 7 B, as
  expected. SPICE 0.111 is within 0.007 of CNN14 — comprehension near trained level;
  the gap is mostly phrasing (CIDEr).

### 2026-07-05 — Third LALM row: Audio Flamingo 3 (the headline result)
- **The lightest row.** AF3 (`nvidia/audio-flamingo-3-hf`) is **transformers-native**
  (`AudioFlamingo3ForConditionalGeneration`): a Whisper-style 128-mel audio encoder +
  a **Qwen2-7B** text decoder. It imports in the *existing* Qwen env (transformers
  5.13) — **no new environment, no vendored repo**. Wrapper mirrors the Qwen temp-WAV
  pattern; jobs reuse `$WORK/envs/qwen`; model pre-cached (33 GB) to `$WORK/hf_cache`.
- **One real bug, fixed cleanly.** Smoke first failed on every clip with a dtype
  mismatch (`float` audio features vs `bf16` model bias). AF3's *native* dtype is
  float32, so bf16 created mixed-dtype internals; loading in **fp32** (~28 GB, fits
  one A100-40 GB, and fp32 is higher precision than bf16 so no quality trade-off)
  resolved it without any per-tensor casting.
- **Smoke (5 clips)** produced clean, notably Clotho-style captions ("A ratchet is
  being used to wind up a toy.") — closer to the reference register than SALMONN's.
- **Full run** (job `1731417`, 1×A100): **1045/1045, 0 failures, ~17.5 min.**
- **Result: SPIDEr-FL 0.2968 — beats BOTH trained captioners** (CNN14 0.259, EnCLAP
  0.280), on **every** metric (CIDEr 0.460 > 0.443, SPICE 0.137 > 0.123, METEOR
  0.186 > 0.180). The **first model in the table to clear the trained baselines**, and
  it does so zero-shot. This reframes RQ1: *whether* a zero-shot LALM beats trained
  captioners depends on the model — a current SOTA audio-specialist does, a general
  omni and an older audio LALM do not.

### 2026-07-05/06 — RQ2 + RQ3 + statistics + TERM PAPER (submitted)
- **Polyphony split (RQ2).** PANNs `Cnn14_DecisionLevelMax` framewise SED
  (API verified: 100 fps, 527 classes; sanity: pug clip → Dog/Snoring) over all
  1045 clips → `results/sed_framewise_summary.json`. P2 rule ("two classes
  co-active ≥1 s at τ"): τ=0.50 was **degenerate** (106 poly, 609 clips with zero
  activation) — the **pre-committed** fallback rule selected τ=0.25 → **336 poly /
  709 mono** (`subsets/poly.txt`, `mono.txt`). Audit: references of poly clips
  name more distinct entities (4.5 vs 3.8; ≥2 in 97% vs 87%).
- **CHAIR-audio (RQ3).** Closed 527-label AudioSet vocabulary (605 surface forms,
  deterministic matcher, coverage ~0.8), dual criterion (hallucinated iff absent
  from 5-ref union AND SED tags). **CHAIR-s @ τ=0.25: SALMONN 0.332 < AF3 0.347 ≈
  CNN14 0.350 ≈ EnCLAP 0.351 ≪ Qwen 0.550 ≪ AST 0.956** (AST = validity check).
- **Per-item scores + preregistered tests.** `score.py --per-item` (verified:
  mean per-item spider_fl == corpus exactly); BCa bootstrap n=1000 seed 42 +
  Holm. **H1 ✓** AF3 > 0.261 (CI low 0.2828 > 0.2714, p≈.001). **H2 ✓ all three
  LALMs**: Δ(poly−mono) positive (+.059…+.094, p≈.001) — but baselines shift the
  same way (+.060/+.073), so it is a *subset-difficulty* effect, not LALM-specific;
  contrast with Harish & Abeßer's event-level degradation. **H3 ✓** AF3 > SALMONN
  paired (+0.072, p≈.001). **H4 ✗ null retained** (not threshold-sensitive): AF3
  does NOT hallucinate less than SALMONN. All in `results/hypothesis_tests.json`.
- **Infrastructure root cause found.** The repeated WSL freezes were **C: drive
  full** (0 bytes free): the WSL swap.vhdx grew until the disk died. Fix: deleted
  the bloated swap (C: → 13.6 GB free), `.wslconfig` → memory=12GB, swap=8GB
  **moved to E:**. Scoring then completed without incident (18 per-item files).
  Crash-isolated runner: `scripts/score_remaining_isolated.sh` (one WSL invocation
  per run + auto-retry).
- **MACE (secondary)**: reference implementation (msclap backend — NOT laion-clap;
  verified from source) wired in `.venv-mace` + `src/analysis/mace_scores.py`;
  runs on poly/mono for the 3 LALMs.
- **TERM PAPER built and packaged**: 4 pp IEEEtran, all tables/figures generated
  from `results/*.json` (`src/analysis/make_figures.py` — zero hand-typed numbers),
  citations verified against primary sources, AI Transparency Statement + repo URL
  included, all 6 prereg deviations disclosed.
  `deliverables/paper/Zuraiz_LALM_Audio_Captioning_CH_Proj_M_SS_2026.{pdf,zip}`.
- **Housekeeping**: `feat/cnn14-baseline` merged (ff) into **main**, pushed, `git gc`.

---

## 5. Verified results

Full Clotho-eval (1045 clips), seed 42. Baselines on laptop CPU; LALMs on A100.
Sources: `results/<row>_eval_scores.json`. Columns ordered by SPIDEr-FL.

| Metric | AST *(floor)* | Qwen2.5-Omni-7B *(0-shot)* | SALMONN-13B *(0-shot)* | CNN14 *(trained)* | EnCLAP *(trained)* | Audio Flamingo 3 *(0-shot)* | What it measures |
|:--|:--|:--|:--|:--|:--|:--|:--|
| **SPIDEr-FL** | 0.0684 | 0.1880 | 0.2246 | 0.2592 | 0.2801 | **0.2968** | headline: CIDEr+SPICE blend, fluency-penalised |
| SPIDEr | 0.0831 | 0.1883 | 0.2288 | 0.2671 | 0.2826 | **0.2982** | CIDEr+SPICE average |
| CIDEr-D | 0.1102 | 0.2860 | 0.3470 | 0.4162 | 0.4425 | **0.4596** | n-gram overlap, TF-IDF weighted |
| SPICE | 0.0560 | 0.0905 | 0.1105 | 0.1181 | 0.1226 | **0.1368** | scene-graph (objects/relations) match |
| METEOR | 0.0948 | 0.1412 | 0.1516 | 0.1756 | 0.1795 | **0.1861** | unigram match with synonyms |
| Fluency-error (↓) | 0.1799 | **0.0048** | 0.0172 | 0.0287 | 0.0134 | 0.0105 | how often the caption is disfluent (`fer`) |
| **vs published** | n/a (tagger) | n/a (0-shot) | n/a (0-shot) | ~0.261 ✓ | ~0.283 ✓ | n/a (0-shot) | the captioners reproduce their papers |

**Reading it (RQ1) — the headline result:** the ordering is
**AST ≪ Qwen < SALMONN < CNN14 < EnCLAP < AF3**
(0.068 → 0.188 → 0.225 → 0.259 → 0.280 → 0.297). The answer to "do LALMs beat
traditional baselines?" is **not a flat yes/no — it depends on the model**:
- **Two of three LALMs (Qwen, SALMONN) trail both trained captioners.** So it is
  *false* that zero-shot LALMs beat trained systems in general.
- **The SOTA audio-specialist (Audio Flamingo 3) beats both trained captioners
  outright, zero-shot, on every metric** — CIDEr 0.460 > EnCLAP 0.443, SPICE 0.137 >
  0.123, METEOR 0.186 > 0.180. It is the first model in the table to clear the
  trained captioners.

Why AF3 wins where Qwen/SALMONN do not: it is purpose-built and large-scale trained
by NVIDIA for audio understanding incl. captioning, and its outputs are visibly
Clotho-style ("A machine is being operated with a button being pressed repeatedly"),
so they match the overlap metrics that reward reference-like phrasing. The within-set
LALM ordering is also sensible — audio-specialist AF3 > audio-specialist SALMONN >
general-omni Qwen. Trustworthiness: CNN14 and EnCLAP each reproduce their papers
within ~0.005, and every LALM is highly fluent (FER ≤ 0.017, tiny SPIDEr→SPIDEr-FL
penalties), so these are genuine content differences, not scoring artefacts. The
open RQ2/RQ3 question is whether AF3's lead holds on **polyphonic** clips and whether
it hallucinates more than the trained models when it is confidently wrong.

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

**Q: Your zero-shot LALM (Qwen, 0.188) *loses* to the trained baselines. Doesn't
that undermine the whole LALM premise?**
A: No — it answers RQ1 honestly. On Clotho's *own* overlap metrics, a model trained
on Clotho references has a structural advantage: those metrics reward matching the
reference vocabulary and phrasing. Qwen is zero-shot and still nearly triples the
tagging floor, so it clearly understands the audio; it just phrases it differently.
The interesting science is *where* it diverges (RQ2 polyphony, RQ3 hallucination),
which caption-overlap scores alone cannot see. We report the number straight and
let the sub-analyses carry the argument.

**Q: How do you know Qwen's low score isn't just chatty, malformed output?**
A: Because we measured fluency directly: Qwen's fluency-error rate (`fer`) is 0.005,
the **lowest** of all four rows, and its SPIDEr→SPIDEr-FL fluency penalty is only
0.0003. We also post-filter trailing questions (`_strip_chat`) and verified **zero**
`?`-terminated captions in the 1045-clip run. The captions are clean declaratives;
the gap to the trained models is content/style, not disfluency.

**Q: The LALM ran on a cluster, the baselines on your laptop. Is that comparable?**
A: Yes — only the *compute* moved, not the *method*. Every row implements the same
`Captioner.caption()` contract, runs through the same `run_inference.py`, emits the
same predictions-JSON, and is scored by the same WSL `score.py` with the same
dcase2023 preset on the same 1045 Clotho-eval clips, seed 42. The A100 is just a
bigger place to run one `caption()` call; nothing in the measurement changed.

**Q: SALMONN (0.225) beats Qwen (0.188). Why, and does one LALM being better change
the RQ1 answer?**
A: SALMONN is a 13 B audio-specialist with two dedicated audio encoders (Whisper +
BEATs) fused by a Q-Former trained on audio tasks; Qwen2.5-Omni is a 7 B general
model spanning text/vision/audio/speech. The specialist doing better on audio
captioning is the expected ordering and a sanity check that the harness
discriminates. It does **not** change RQ1: *both* zero-shot LALMs still sit below
both in-domain-trained captioners, so the "trained > zero-shot on Clotho overlap
metrics" conclusion holds across two independent architectures, which is stronger
than one model would be.

**Q: SALMONN's decode uses beam search but Qwen used greedy. Isn't that inconsistent?**
A: Each LALM runs at its authors' recommended decoding — SALMONN's config ships
`num_beams=4`, Qwen-Omni is run greedy — because the question is each model at its
best, and both decodes are recorded per-row in the manifest. The trained baselines
also use beam search, so SALMONN's setting is not an outlier. The comparison that
matters (dataset, split, metric, references) is held identical.

**Q: Audio Flamingo 3 beats your trained baselines zero-shot. Is that real, or did
something leak?**
A: Real. Three checks: (1) the *same* harness reproduces CNN14 and EnCLAP within
~0.005 of their published numbers, so it is not inflating scores; (2) AF3 ran fully
offline from a pre-cached checkpoint with no access to Clotho references — the
predictions JSON only ever sees the audio; (3) the result is consistent with AF3
being a current SOTA audio-understanding model (NVIDIA, Qwen2-7B decoder, large-scale
audio-caption training). Its captions are visibly Clotho-style, which is exactly why
it scores well on overlap metrics. The honest framing for RQ1 is that the *best*
audio LALM beats trained captioners while two other LALMs do not — the answer is
model-dependent, not a blanket "LALMs win."

**Q: You ran AF3 in fp32 but Qwen in bf16 — why, and does it bias the comparison?**
A: AF3's released weights are natively float32; loading it in bf16 produced a
genuine dtype mismatch in its audio encoder, so fp32 is the *correct* way to run it
(and it still fits one 40 GB A100). fp32 is higher precision than bf16, so if
anything it is the model at its best — the user's stated requirement. Precision is a
per-model deployment detail recorded in each manifest; it does not touch the
measurement (same clips, metric, references).

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

**LALM rows** (the main project) — **all three done**
- [x] **GPU cluster access** — NHR@FAU TinyGPU (A100 40 GB), env + data + model staged.
- [x] **Qwen2.5-Omni-7B — scored: SPIDEr-FL 0.1880**, committed.
- [x] **SALMONN-13B — scored: SPIDEr-FL 0.2246**, committed.
      (Fits 1×A100-40 GB in fp16; own conda py3.10 env for the torch 2.0.1 stack.)
- [x] **Audio Flamingo 3 — scored: SPIDEr-FL 0.2968 — beats both trained baselines**,
      committed. (Transformers-native, reuses the Qwen env; fp32 on 1×A100-40 GB.)
- [ ] ~~Falcon3-Audio~~ — **dropped**: weights never publicly released (verified).

**RQ2 / RQ3 track — done**
- [x] **Polyphony SED subset** — PANNs framewise SED, τ=0.25 (pre-committed fallback
      from 0.50): 336 poly / 709 mono. (PaSST dropped: clip-level only, disclosed.)
- [x] **CHAIR-audio** — dual-criterion hallucination on all 6 rows (H4: null retained).
- [x] **Hypothesis tests** — BCa + Holm: H1 ✓, H2 ✓ (all LALMs), H3 ✓, H4 ✗.
- [x] **RQ1 parity** — resolved: all rows scored on the identical full 1045-clip set
      (the "CLEAN" subset was never defined; disclosed as deviation).
- [x] **MACE** — secondary metric via reference implementation (poly/mono, 3 LALMs).

**Housekeeping**
- [x] Merged `feat/cnn14-baseline` → `main`, pushed, `git gc`.
- [x] **Term paper submitted artifacts built** (4 pp IEEE, PDF + ZIP, 06.07).
- [ ] P3 defence deck (13 Jul) — `deliverables/p3/`, reuse paper figures.

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
- **LALM** — Large Audio-Language Model. Our set (all done): **Qwen2.5-Omni-7B**
  (Alibaba, SPIDEr-FL 0.188), **SALMONN-13B** (Tsinghua/ByteDance, 0.225), **Audio
  Flamingo 3** (NVIDIA, **0.297 — beats the trained baselines**). Falcon3-Audio was
  dropped — weights never released.
- **Audio Flamingo 3 (AF3)** — NVIDIA audio-language model: Whisper-style 128-mel
  encoder + Qwen2-7B decoder. Transformers-native (`audio-flamingo-3-hf`); runs fp32
  in the same env as Qwen. The top scorer overall.
- **SALMONN** — Whisper-large-v2 + BEATs encoders → window-level Q-Former → Vicuna-13B
  + LoRA (Tang et al., ICLR 2024). 13 B, audio-specialist. Needs four checkpoints and
  the old `transformers 4.28`/`torch 2.0.1` stack (its own conda py3.10 env).
- **NHR@FAU TinyGPU** — the GPU cluster the LALM rows run on. A100 40 GB, Slurm,
  offline compute nodes. Account `barz144h`, project `barz101`, `$WORK` = the big
  quota. Qwen2.5-Omni-7B ≈ 22 GB VRAM, 8.3 min for the full 1045-clip run.
- **The two repos we vendor** — `felixgontier/dcase-2023-baseline` (`_vendor`,
  `4f89d0b`) and `jaeyeonkim99/EnCLAP` (`_vendor_enclap`, `e4976a4`).
- **Magic numbers** — beam=4, seed=42, 1045 eval clips, 44.1 kHz, CNN14 26.1 % /
  EnCLAP 28.3 % published.
