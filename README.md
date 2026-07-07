# Audio-to-Text Captioning using LALMs (CH-Proj-M, SS 2026)

Master's project, Computational Humanities, University of Bamberg
(supervisor: Prof. Dr.-Ing. Jakob Abeßer). The project compares three
zero-shot large audio-language models against three traditional systems on the
full Clotho v2.1 evaluation split (1045 clips, seed 42), with a polyphony
analysis (RQ2) and a hallucination analysis (RQ3) on top.

Key documents:

- **Term paper**: `deliverables/paper/` (PDF, LaTeX sources, generated tables
  and figures).
- **`PROJECT_LOGBOOK.md`**: the complete engineering and decision record,
  including the defense Q&A kit. Read this to understand every number.
- **`hypotheses_preregistered.yml`**: the declared analysis plan (H1 to H4,
  thresholds, fallback rules). All deviations are disclosed in the paper.
- **`results/`**: predictions, run manifests, corpus and per-item scores,
  hypothesis tests, CHAIR-audio, MACE, and the SED summary. Every number in
  the paper traces back to a file here.

## Final results (SPIDEr-FL, full Clotho-eval, identical harness)

| System | Type | SPIDEr-FL | Published anchor |
|:--|:--|:--|:--|
| AST (top-5 tag template) | tagging floor | 0.068 | n/a (not a captioner) |
| Qwen2.5-Omni-7B | zero-shot LALM | 0.188 | n/a (zero-shot) |
| SALMONN-13B | zero-shot LALM | 0.225 | n/a (zero-shot) |
| CNN14+BART (DCASE 2023) | trained | 0.259 | 0.261 (official) |
| EnCLAP-base | trained | 0.280 | 0.291 SPIDEr-FL / 0.295 SPIDEr |
| **Audio Flamingo 3** | zero-shot LALM | **0.297** | n/a (zero-shot) |

CNN14 reproduces its official score within 0.002 and validates the harness.
The EnCLAP row runs about 1.1 pp below its published anchor (EnCLAP++ measures
0.291 SPIDEr-FL for the released checkpoint with the same toolkit); this
shortfall is disclosed in the paper rather than tuned away. Hypotheses: H1,
H2, H3 supported; H4 null retained. Details, subsets, CHAIR and MACE numbers:
see the paper and the logbook.

Note: the third LALM was originally planned to be Falcon3-Audio; its weights
were never publicly released (verified against the paper and the authors'
Hugging Face page), so it was replaced by Audio Flamingo 3. The logbook
records this decision.

## How the pipeline works

Every system implements one contract, `Captioner.caption(waveform, sr) -> str`
(`src/models/base.py`), behind a registry, so one inference loop
(`src/pipeline/run_inference.py`) and one scorer (`src/metrics/score.py`)
serve all six rows. Each run writes a predictions JSON plus a manifest with
checkpoint SHA-256s, library versions, decode parameters, and the seed.

```
Clotho-eval WAV -> src/data/clotho.py (44.1 kHz mono)
  -> src/models/<row>.py (features -> caption)
  -> src/pipeline/run_inference.py (predictions JSON + manifest)
  -> src/metrics/score.py (WSL: SPIDEr-FL, CIDEr-D, SPICE, METEOR, FER)
  -> src/analysis/* (subsets, CHAIR-audio, MACE, hypothesis tests, figures)
```

Compute layout:

- **Baselines (CPU, this machine)**: CNN14 in `.venv` (transformers 4.41),
  EnCLAP in `.venv-enclap` (transformers 4.29, incompatible by upstream
  design), AST in `.venv` (no extra weights).
- **Scoring (WSL Ubuntu, `.venv-wsl`)**: `aac-metrics` 0.5.5 needs Java 8 to
  13 for SPICE; the host has Java 23, so scoring lives in WSL with OpenJDK 11.
  The predictions JSON is the only handoff.
- **LALMs (NHR@FAU TinyGPU, one A100-40GB per run)**: Qwen2.5-Omni and AF3 in
  a transformers 5.x env, SALMONN in its own conda py3.10 env (torch 2.0.1).
  Compute nodes are offline; models are pre-cached and runs are submitted via
  the sbatch files in `jobs/`. Configs in `configs/<row>.yaml` are the single
  source of truth per row.
- **MACE (`.venv-mace`)**: reference implementation, MS-CLAP backend,
  torch/torchaudio pinned to 2.4.1.

## Reproducing

Baseline setup (row by row):

```powershell
# CNN14 (.venv)
py -3.11 -m venv .venv; .venv\Scripts\activate
git submodule update --init src/models/_vendor
pip install -r requirements.txt
python scripts/download_weights.py
python scripts/cache_hf_assets.py

# EnCLAP (.venv-enclap)
py -3.11 -m venv .venv-enclap; .venv-enclap\Scripts\activate
git submodule update --init src/models/_vendor_enclap
pip install -r requirements-enclap.txt
python scripts/download_weights_enclap.py --out weights/enclap_pretrained
```

Inference and scoring (swap the row name and the matching venv):

```powershell
python -m src.pipeline.run_inference --config configs/cnn14.yaml --out results/cnn14_eval.json
```

```bash
# WSL
bash scripts/setup_wsl_metrics.sh   # once
source .venv-wsl/bin/activate
python -m src.metrics.score --predictions results/cnn14_eval.json --out results/cnn14_eval_scores.json
# --subset subsets/poly.txt|mono.txt for the RQ2 subsets, --per-item for the bootstrap inputs
```

Analysis (in `.venv`, except MACE in `.venv-mace`):

```powershell
python -m src.analysis.sed_summary            # PANNs framewise SED over all clips
python -m src.analysis.polyphony_manifest     # tau rule -> subsets/poly.txt, mono.txt
python -m src.analysis.chair_audio            # closed-vocabulary hallucination rates
python -m src.analysis.mace_scores            # MACE poly/mono (in .venv-mace)
python -m src.analysis.hypothesis_tests       # BCa bootstrap + Holm, H1 to H4
python -m src.analysis.make_figures           # all paper tables and figures
```

## Reproducibility notes

- Native 44.1 kHz end to end; the loader never resamples globally (models
  resample internally where their upstream expects it).
- Vendored upstream code is pinned by submodule commit
  (`felixgontier/dcase-2023-baseline` @ 4f89d0b, `jaeyeonkim99/EnCLAP` @
  e4976a4); model classes are untouched.
- Deterministic: seed 42 everywhere, decode settings recorded per row in the
  manifest, scoring preset `dcase2023`.
- Paper tables and figures are generated by `src/analysis/make_figures.py`
  from `results/*.json`; no number in the paper is hand-typed.
