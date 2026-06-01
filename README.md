# CNN14 Baseline Pipeline (DCASE 2023 Task 6A)

Reproduces the **CNN14 + BART** audio-captioning baseline on Clotho v2.1 — the
first traditional-baseline row of the LALM comparison table for CH-Proj-M.

**Verified result:** SPIDEr-FL **0.2592** on full Clotho-eval (1045 clips) vs
published **0.261** — every sub-metric within ~0.005 (CIDEr-D 0.416, SPICE
0.118, METEOR 0.176). CPU, beam=4, seed 42.

> **Two machines by design.** Inference runs on **Windows** (native Python, where
> the audio + model live). Scoring runs in **WSL Ubuntu**, because `aac-metrics`
> needs Java 8–13 for SPICE and this host has Java 23. The predictions JSON is the
> handoff between them.

---

## Prerequisites

- Windows + Python 3.11, ~1.5 GB free disk (weights + HF cache)
- WSL2 Ubuntu (for scoring only)
- `git` with submodule support

## Setup (once)

### Windows side

```powershell
py -3.11 -m venv .venv
.venv\Scripts\activate
git submodule update --init            # pulls src/models/_vendor @ 4f89d0b
pip install -r requirements.txt
python scripts/download_weights.py      # ~1 GB: CNN14 encoder + BART decoder (Zenodo)
python scripts/cache_hf_assets.py       # caches facebook/bart-base tokenizer + config
```

### WSL side

```bash
# inside WSL Ubuntu, at the project root on /mnt/...
bash scripts/setup_wsl_metrics.sh       # apt: openjdk-11; venv .venv-wsl; aac-metrics + jars
```

## Run

### 1. Inference (Windows, ~33 min on CPU)

```powershell
.venv\Scripts\activate
python -m src.pipeline.run_inference --config configs/cnn14.yaml --out results/cnn14_eval.json
```

Smoke test first (5 clips, ~15 s):

```powershell
python -m src.pipeline.run_inference --config configs/cnn14.yaml --out results/smoke.json --limit 5
```

### 2. Score (WSL)

```bash
source .venv-wsl/bin/activate
python -m src.metrics.score --predictions results/cnn14_eval.json --out results/cnn14_eval_scores.json
```

## Outputs (`results/`, git-ignored)

| File | Contents |
|:--|:--|
| `cnn14_eval.json` | 1045 × `{file_name, prediction, references}` |
| `cnn14_eval.manifest.json` | weight SHA256s, vendored commit, lib versions, decode/audio params, seed — the reproducibility receipt |
| `cnn14_eval_scores.json` | SPIDEr-FL, CIDEr-D, SPICE, METEOR, fluency-error rate |

## How it fits together

```
Clotho-eval WAV → [src/data/clotho.py] 44.1 kHz mono
  → [src/models/cnn14_dcase.py] log-mel → CNN14 → BART decoder → caption
  → [src/pipeline/run_inference.py] predictions JSON
  → [src/metrics/score.py, WSL] SPIDEr-FL + friends
```

- `src/models/base.py` defines the `Captioner` ABC — the `.caption(waveform, sr)`
  contract every future model row (AST, EnCLAP, Falcon3-Audio, …) implements.
- `src/models/_vendor` is `felixgontier/dcase-2023-baseline` pinned by commit;
  the CNN14/BARTAAC classes are upstream's, untouched.
- Config lives only in `configs/cnn14.yaml` (no magic numbers in code).

Full design + rationale: `docs/superpowers/plans/` (the approved implementation plan).

## Reproducibility notes

- Native **44.1 kHz** (not 32 kHz): the upstream baseline trains at Clotho's native
  rate (`librosa.load(sr=None)`); the mel params match its call site exactly.
- Deterministic: greedy/beam decoding, fixed seed 42; the manifest pins all versions.
- Scoring metric preset defaults to `dcase2023` (matches the installed `aac-metrics` 0.5.x).
