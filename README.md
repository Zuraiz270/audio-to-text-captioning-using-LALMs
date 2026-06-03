# Traditional Baselines Pipeline (Clotho v2.1)

Reproduces the **traditional audio-captioning baselines** for CH-Proj-M — the
rows the LALMs (Falcon3-Audio, SALMONN, Qwen2.5-Omni) are benchmarked against.
Every model implements one `Captioner.caption(waveform, sr) -> str` contract, so
they share the same inference loop, predictions-JSON schema, and scorer.

**Verified results** — full Clotho-eval (1045 clips), CPU, beam=4, seed 42:

| Row | Model | SPIDEr-FL | SPIDEr | CIDEr-D | SPICE | Published (SPIDEr) |
|:--|:--|:--|:--|:--|:--|:--|
| 1 | CNN14 + BART (DCASE 2023 Task 6A) | 0.2592 | 0.2671 | 0.4162 | 0.1181 | ~0.261 ✓ |
| 2 | EnCLAP-base (EnCodec+CLAP+BART, ICASSP 2024) | **0.2801** | **0.2826** | **0.4425** | **0.1226** | ~0.283 ✓ |

EnCLAP > CNN14 on every metric — the expected 2024 > 2023 ordering.

> **Two machines by design.** Inference runs on **Windows** (native Python, where
> the audio + models live). Scoring runs in **WSL Ubuntu**, because `aac-metrics`
> needs Java 8–13 for SPICE and this host has Java 23. The predictions JSON is the
> handoff between them.
>
> **Two Windows envs by necessity.** CNN14 uses `transformers==4.41` (`.venv`);
> EnCLAP's vendored `EnClapBart` only works on `transformers==4.29` (`.venv-enclap`).
> They are mutually incompatible, so each row gets its own venv + requirements file.

---

## Prerequisites

- Windows + Python 3.11; ~12 GB free disk (EnCLAP weights are ~9 GB, CNN14 ~1 GB)
- WSL2 Ubuntu (for scoring only)
- `git` with submodule support

## Setup (once)

### Shared: WSL scorer

```bash
# inside WSL Ubuntu, at the project root on /mnt/...
bash scripts/setup_wsl_metrics.sh       # apt: openjdk-11; venv .venv-wsl; aac-metrics + jars
```

### Row 1 — CNN14 (`.venv`)

```powershell
py -3.11 -m venv .venv
.venv\Scripts\activate
git submodule update --init src/models/_vendor    # felixgontier/dcase-2023-baseline @ 4f89d0b
pip install -r requirements.txt
python scripts/download_weights.py                # CNN14 encoder + BART decoder + CLAP (shared w/ EnCLAP)
python scripts/cache_hf_assets.py                 # facebook/bart-base tokenizer + config
```

### Row 2 — EnCLAP (`.venv-enclap`)

```powershell
py -3.11 -m venv .venv-enclap
.venv-enclap\Scripts\activate
git submodule update --init src/models/_vendor_enclap   # jaeyeonkim99/EnCLAP
pip install -r requirements-enclap.txt
# weights: CLAP fusion ckpt (via download_weights.py above) + the EnCLAP checkpoint:
python scripts/download_weights_enclap.py --out weights/enclap_pretrained   # gdown Drive folder (~9 GB)
# bart-large tokenizer + EnCodec 24 kHz auto-download on first run (cached)
```

## Run

Inference on Windows, scoring on WSL. Swap `cnn14` ⇄ `enclap` and the matching venv.

```powershell
# CNN14 (~33 min CPU) — .venv
python -m src.pipeline.run_inference --config configs/cnn14.yaml  --out results/cnn14_eval.json
# EnCLAP (~90 min CPU) — .venv-enclap
python -m src.pipeline.run_inference --config configs/enclap.yaml --out results/enclap_eval.json
```

Smoke-test either with `--limit 5` first.

```bash
# WSL — scores whichever predictions file you point at
source .venv-wsl/bin/activate
python -m src.metrics.score --predictions results/enclap_eval.json --out results/enclap_eval_scores.json
# --subset <file_of_file_names>  restricts to a fixed clip set (same-clip-set comparisons)
```

## Outputs (`results/`, git-ignored)

Per model `<m>`: `<m>_eval.json` (1045 predictions + refs), `<m>_eval.manifest.json`
(weight SHA256s, vendored commit, lib versions, decode/audio params, seed — the
reproducibility receipt), `<m>_eval_scores.json` (SPIDEr-FL, CIDEr-D, SPICE,
METEOR, fluency-error rate).

## How it fits together

```
Clotho-eval WAV → [src/data/clotho.py] 44.1 kHz mono
  → [src/models/<row>.py] features → decoder → caption
  → [src/pipeline/run_inference.py] predictions JSON   (model-agnostic)
  → [src/metrics/score.py, WSL] SPIDEr-FL + friends
```

- `src/models/base.py` — the `Captioner` ABC every row implements.
- `src/models/__init__.py` — `MODEL_REGISTRY` maps `--config`'s `model.name` to a class.
- `src/models/cnn14_dcase.py` wraps `_vendor` (felixgontier/dcase-2023-baseline);
  `src/models/enclap.py` wraps `_vendor_enclap` (jaeyeonkim99/EnCLAP). Both pinned
  by submodule commit; upstream classes are untouched.
- Config lives only in `configs/<row>.yaml` (no magic numbers in code).

## Reproducibility notes

- Native **44.1 kHz** end-to-end: CNN14's upstream trains at Clotho's native rate;
  EnCLAP resamples internally (24 kHz EnCodec / 48 kHz CLAP). The loader never
  resamples to 32 kHz (a generic-PANNs assumption that would misalign features).
- **EnCLAP env is isolated** at `transformers==4.29` / `tokenizers==0.13.3` +
  `torchvision` (laion-clap needs it); CLAP must be the **fusion + HTSAT-tiny**
  checkpoint (`630k-audioset-fusion-best.pt`).
- Deterministic: beam search, fixed seed 42; manifests pin all library versions.
- Scoring preset defaults to `dcase2023` (matches the installed `aac-metrics` 0.5.x).
