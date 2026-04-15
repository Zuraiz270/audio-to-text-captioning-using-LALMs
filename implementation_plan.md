# Implementation Plan (Definitive Merged) — T6: Audio-to-Text Captioning using LALMs
*Master's Project · CH-Proj-M · SS 2026 · Zuraiz (2177213)*
*Prof. Dr.-Ing. Jakob Abeßer · Computational Humanities · Uni Bamberg*
*Merges: Antigravity v5 (execution base) + Claude Code v6 (hardening / reviewability)*

---

## Central Thesis

> Current-generation LALMs — **Audio Flamingo 3** (NVIDIA, Jul 2025), **Qwen2.5-Omni** (Alibaba, Mar 2025) — *zero-shot*, **conditional on a passed training-set contamination audit (RQ0)**, match or exceed the supervised DCASE 2024 baseline (CNext-trans, 29.6% SPIDEr-FL) on Clotho v2.1, yet exhibit three structurally-related failure modes: (a) polyphonic under-description, (b) entity hallucination, (c) loss of temporal ordering. Characterising the magnitude and structure of these failure modes — with pre-registered hypotheses, bootstrap 95% CIs, Cohen's κ-gated annotation, and CLAPScore for out-of-distribution cultural audio where no references exist — is the academic contribution.

---

## § 0.5 — Decision Provenance (CLAUDE.md §3 Evidence Trail)

Every architectural decision in this plan is defensible against reviewer challenge.

| # | Decision | Source | Level | Year | Conf | Applic | Status |
|:-:|:---------|:-------|:------|:----:|:----:|:------:|:------:|
| D1 | **AF3 as primary model** (vs. SALMONN, Qwen2.5-Omni) | Ghosh et al. — AF3 (arxiv 2507.08128) | L3 | 2025 | HIGH | HIGH | ACCEPTED |
| D2 | **transformers pin = `4.44.*`** with `trust_remote_code=True` | AF3 HuggingFace model card | L1 | 2025 | HIGH | HIGH | ACCEPTED |
| D3 | **bf16 precision** for primary runs | PyTorch bf16 docs + NVIDIA Ampere compute-capability (SM ≥ 8.0) | L1 | 2024 | HIGH | HIGH | ACCEPTED |
| D4 | **Metric stack = SPIDEr-FL · CIDEr · SPICE · FENSE · CLAPScore · CHAIR-audio** | DCASE 2024 T6 baseline `[Labbeti 2024; L1]` + Zhou 2022 FENSE `[L2]` + Wu 2023 LAION-CLAP `[L2]` + Rohrbach 2018 CHAIR `[L2]` | L1/L2 | 2018-24 | HIGH | HIGH | ACCEPTED |
| D5 | **BCa bootstrap** (bias-corrected accelerated) instead of plain percentile | Efron & Tibshirani 1993 ch. 14 | L2 | 1993 | HIGH | HIGH | ACCEPTED |

---

## Pre-flight Blockers — Resolve Before May 4

> [!IMPORTANT]
> All four must be green before Phase 1 yields a live demo.

### 1. Compute ✅ RESOLVED
No local NVIDIA GPU detected.
| Option | VRAM | Cost | Use |
|:-------|:-----|:-----|:----|
| **Uni Bamberg RZ (A100/H100)** | 40–80GB | Free (apply Apr 15) | Primary for final bf16 runs |
| **Google Colab Pro (A100 40GB)** | 40GB | ~€10/mo | Fallback — AF3-8B bf16 fits |

### 2. Java Runtime for SPICE
`aac-metrics` requires JRE 11+. On Colab: `!apt-get install -y default-jre`.

### 3. HuggingFace Licences
- `nvidia/audio-flamingo-3` — NVIDIA Open Model License.
- `tsinghua-ee/SALMONN` — research-only; mirror weights.
- Qwen2.5-Omni — Apache-2.0 (lowest risk).

### 4. Contamination Audit Data Access (WavCaps ID fix)
> [!WARNING]
> WavCaps does **NOT** provide MD5 hashes in its manifest. The AF3 implementation must cross-reference Clotho's FreeSound IDs against the WavCaps FreeSound-ID list.

Sources for RQ0:
- Clotho-AQA manifest: `https://zenodo.org/records/6473207`
- WavCaps manifest: `https://huggingface.co/datasets/cvssp/WavCaps`
- AudioSetCaps YouTube-ID list
- AF3 training data card

---

## Phase 0 — Environment & Reproducibility (→ Apr 19)

### `environment.yml` (pinned + determinism constraints)

```yaml
name: t6-aac
channels: [conda-forge, pytorch, nvidia]
dependencies:
  - python=3.11
  - pytorch=2.4.*
  - torchaudio=2.4.*
  - pytorch-cuda=12.1
  - openjdk=11
  - pip
  - pip:
    - transformers==4.44.*
    - accelerate
    - bitsandbytes
    - librosa==0.10.*
    - soundfile
    - resampy
    - aac-datasets
    - aac-metrics
    - fense
    - bert-score
    - pycocoevalcap
    - laion-clap
    - spacy
    - imagehash
    - jupyter
    - pandas
    - matplotlib
    - seaborn
    - pyyaml
variables:
  CLOTHO_ZENODO_RECORD: "4783391"   # v2.1
  BOOTSTRAP_SEED: "42"              
  PYTHONHASHSEED: "42"
  CUBLAS_WORKSPACE_CONFIG: ":4096:8"
  TOKENIZERS_PARALLELISM: "false"  
```

### `setup_check.py` — Hardware-Gated & Deterministic

```python
"""
Pre-flight: fail loudly if environment cannot produce comparable numbers.
Includes Ampere SM >= 8.0 gate for proper bf16, and deterministic cublas logic.
"""
import os, subprocess, sys
import torch, transformers
from aac_metrics import evaluate

ZENODO_EXPECTED = "4783391"  
TRANSFORMERS_MIN = "4.44.0"

assert os.environ.get("CLOTHO_ZENODO_RECORD") == ZENODO_EXPECTED
assert os.environ.get("BOOTSTRAP_SEED")
assert os.environ.get("PYTHONHASHSEED") == "42"
assert os.environ.get("CUBLAS_WORKSPACE_CONFIG") == ":4096:8"
torch.use_deterministic_algorithms(True, warn_only=False)

if torch.cuda.is_available():
    p = torch.cuda.get_device_properties(0)
    cc = torch.cuda.get_device_capability(0)  
    print(f"GPU: {p.name} | VRAM: {p.total_memory/1e9:.1f} GB | SM: {cc[0]}.{cc[1]}")
    if cc[0] < 8:
        sys.exit(
            f"FATAL: SM {cc[0]}.{cc[1]} detected. "
            "bf16 silently falls back to fp32 → invalidates timing/memory limit."
        )
    if p.total_memory / 1e9 < 14:
        print("WARNING: < 14 GB VRAM; AF3 int4 may fail. Use Colab Pro.")
else:
    print("WARNING: no CUDA; CPU-only runs are out-of-scope for Phase 2/3.")

assert transformers.__version__ >= TRANSFORMERS_MIN

subprocess.run(["java", "-version"], check=True, capture_output=True)
_ = evaluate([["a dog barks"]], [[["a dog barks loudly"]]])
print("setup_check OK")
```

### `hypotheses_preregistered.yml` (with Holm-Bonferroni & BCa)

```yaml
bootstrap_n_resamples: 1000
bootstrap_seed: 42                       
bootstrap_method: BCa                    
significance_alpha: 0.05
multiple_comparison: holm_bonferroni     

# Inferential families: each inner list is Holm-Bonferroni-corrected together.
# Descriptive hypotheses are reported with BCa CIs but NOT subject to family-wise
# error correction (per literature_review.md §11 pre-registration).
hypothesis_families_inferential: [[H1, H2, H3], [H4]]
hypothesis_descriptive:          [H5, H6_RQ5, H_NEGATIVE_CONTROL]

# Backward compat (do not remove — downstream scripts may key on these):
hypothesis_family_H1_H3: [H1, H2, H3]    
hypothesis_family_H4:    [H4]            

# Convention: pre_registered_effect = expected effect size to detect (pp for SPIDEr-FL / CHAIR-audio).
# MDE floors (statistical detection limit given σ and n) are separate — see literature_review.md §10.2.

H1:
  claim: "AF3 zero-shot SPIDEr-FL BCa-95%-CI lower bound > 29.6% on RQ0-cleaned Clotho-eval"
  metric: SPIDEr-FL
  test: one-sided BCa bootstrap CI
  pre_registered_effect: 2.0  
H2:
  claim: "AF3 > SALMONN on SPIDEr-FL, non-overlapping 95% CIs"
  metric: SPIDEr-FL
  test: two-sample BCa bootstrap
  pre_registered_effect: 3.0
H3:
  claim: "Δ(AF3 − baseline) SPIDEr-FL larger on polyphonic than monophonic clips"
  metric: SPIDEr-FL
  test: paired BCa bootstrap
  pre_registered_effect: 3.5
H4:
  claim: "AF3 hallucination rate < SALMONN by ≥ 5 pp, non-overlapping 95% CIs"
  metric: CHAIR-audio entity rate
  test: two-sample BCa bootstrap
  pre_registered_effect: 5.0
H5:
  claim: "Correct temporal-ordering rate ≤ 60% for both AF3 and SALMONN"
  metric: correct_ordering_rate
  flag: [DESCRIPTIVE_ONLY]   
H6_RQ5:
  claim: "LALM CLAPScore on cultural audio < in-distribution baseline by ≥ 0.05"
  metric: CLAPScore
  flag: [DESCRIPTIVE_ONLY]   
H_NEGATIVE_CONTROL:
  claim: "On silent / white-noise clips, entity hallucination rate ≥ 80%"
  metric: CHAIR-audio entity rate
  falsifier: "rate < 50% → text-prior confabulation mechanism weakened (literature_review.md §5.2)"
```

### `Makefile`

```makefile
.PHONY: all audit eval figures paper clean check-figures

all: audit eval figures paper

audit:
	jupyter nbconvert --to notebook --execute notebooks/00_contamination_audit.ipynb

eval:
	python -m scripts.run_full_eval    

figures:
	python figures/make_all.py         

paper:
	cd term_paper && latexmk -pdf main.tex

# CI reproducibility: pixel diff, not byte identity (LaTeX timestamps prevent byte-identity)
check-figures:
	python figures/pixel_diff_check.py --tolerance 1e-3

clean:
	rm -rf results/*.csv figures/*.pdf term_paper/main.pdf
```

---

## Phase 1 — Literature Review, Contamination Audit, Baseline Demo (Apr 19 → May 4) 🎯

### `notebooks/00_contamination_audit.ipynb` — RQ0, the gating check

> [!IMPORTANT]
> This runs **before** any model inference. If AF3 trained on Clotho-eval audio, its "zero-shot" score is leaked-supervised. RQ1 must then report on the clean subset only. Implementation utilizes FreeSound IDs properly.

```python
import hashlib, json, pandas as pd, librosa, imagehash
from PIL import Image
from aac_datasets import Clotho

ds = Clotho(root="./data", subset="eval", download=True)

def freesound_id_from_fname(fname: str) -> str:
    return fname.split("-")[0]

eval_clips = [{"fname": c["fname"], "freesound_id": freesound_id_from_fname(c["fname"])} for c in ds]

wavcaps_fs_ids  = set(pd.read_csv("manifests/wavcaps_freesound.csv")["freesound_id"].astype(str))
clotho_aqa_ids  = set(pd.read_csv("manifests/clotho_aqa.csv")["freesound_id"].astype(str))

overlap = {
    "wavcaps": [c["fname"] for c in eval_clips if c["freesound_id"] in wavcaps_fs_ids],
    "clotho_aqa": [c["fname"] for c in eval_clips if c["freesound_id"] in clotho_aqa_ids],
}
clean_fnames = [c["fname"] for c in eval_clips
                if c["freesound_id"] not in wavcaps_fs_ids
                and c["freesound_id"] not in clotho_aqa_ids]

# ... standard output to results/contamination_audit.json and clotho_eval_clean.csv ...
```

### `notebooks/01_data_explore.ipynb`
Duration histogram · caption-length histogram · vocabulary Zipf plot · 20 hand-tagged poly/mono pilot clips for RQ2 sanity check.

### `notebooks/02_af3_hello_world.ipynb` — May 4 live demo.

---

## Phase 1.5 — Exclusion-Flow Diagram (CONSORT-style)

```
Clotho-eval split (Drossos 2020; Zenodo 4783391)
        n = 1,045
            │
            ▼
  RQ0 contamination audit (notebooks/00_contamination_audit.ipynb)
            │
            ▼   excluded: n_contaminated
  Clotho-eval CLEAN (n = 1,045 − n_contaminated)
            │
            ├─► RQ1 / RQ2 primary eval (01_af3, 02_salmonn, 03_baseline)
            │
            ▼   excluded: clips missing any of 5 refs (QA pass)
  Polyphony sub-selection (06_polyphony_subset.ipynb)
            │
            ▼
  Annotated subset: 100 candidates → κ ≥ 0.6 gate
            │
            ▼   selected: 50 poly + 50 duration-matched mono
  RQ2 analysis set (n = 100)
            │
  AudioCaps single-event subset (RQ3) (n = 500)
            │
  Synthetic A-then-B mixes (RQ4) (n = 50)
            │
  Humanities case study (RQ5) (n ≤ 20)
            │
  Negative controls (RQ sanity, IP6) (n = 30) (silence, white/pink noise, pure tones)
```

---

## Phase 2 — Core Experiments (May 4 → May 18) 🎯

### `03_dcase_baseline.ipynb`
[CNext-trans baseline](https://github.com/Labbeti/dcase2024-task6-baseline) on Clotho-eval.  
**Must reproduce 29.6% ± 1% SPIDEr-FL.** This is the canary.

### `04_af3_full_eval.ipynb` & `05_salmonn_full_eval.ipynb` 
Models evaluated on **contamination-cleaned** Clotho-eval clips.  
Compute SPIDEr-FL, FENSE, CLAPScore. BCa 95% CIs.  
**Preprocessing**: audio normalization and resampling (16 kHz mono) are handled inline inside `04_af3_full_eval.ipynb` and `05_salmonn_full_eval.ipynb` using `aac_datasets.Clotho` default pipeline — no dedicated preprocessing notebook is required.

### `06_polyphony_subset.ipynb`
Two independent annotators label 100 candidate clips. Gate: **Cohen's κ ≥ 0.6.** 

---

## Phase 3 — Failure-Mode Experiments (May 18 → Jul 1)

### `07_hallucination.ipynb` — RQ3 (Fixed CLAP pipeline)

```python
"""
Dual criterion hallucination. Entity is hallucinated iff:
(a) absent from ground-truth tags AND (b) CLAPScore < 0.25.
Fixes torch-cosine-similarity shape error heavily impacting metric robustness.
"""
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine
# ...
audio_emb = clap.get_audio_embedding_from_filelist([audio_path], use_tensor=False)
text_emb = clap.get_text_embedding([noun], use_tensor=False)
sim = float(sklearn_cosine(audio_emb, text_emb)[0, 0])
# ...
```

### `07b_negative_controls.ipynb` (Falsifiable Sanity Check)
Negative-control battery to test for text-prior confabulation mapping.
```python
# 10 × silence, 10 × white noise, 5 × pink noise, 5 × pure tones
# Expected outcome: entity hallucination rate ≥ 80% (confabulation baseline). 
# Falsifier is < 50%.
```

### `08_temporal_ordering.ipynb` — RQ4 (optional)
Synthesise 50 *A-then-B* mixtures using `librosa` (per Kumar 2026 TAC temporal-grounding protocol, arxiv 2602.15766). Report ordering rate.

### `09_qwen25_ablation.ipynb` & `10_humanities_case_study.ipynb` (RQ5)
Qualitative studies on out-of-distribution (Bamberg cultural bell data + BBC Archive) focusing purely on CLAPScore.

---

## Phase 4 — Paper + Final Talk (Jul 1 → Jul 6 📄 → Jul 13 🎤)

1. `make audit` and `make eval` to run the fully automated pipelines.
2. `make figures` processes all generated CSVs. 
3. Submit `term_paper/main.pdf` by Jul 6 EOD. 

---

## License & Ethics Audit (GDPR strict)

| Asset | License | Academic | GDPR / Ethics note |
|:------|:--------|:--------:|:-------------------|
| Clotho v2.1 | CC-BY 4.0 | ✓ | No PII |
| AudioCaps | YouTube ToS | ✓ | Art. 89(1) research exemption; no redistribution |
| AF3 / SALMONN | Open / Research | ✓ | Mirror weights |
| **Bamberg bell recordings (T1)** | TBD — T1 group | ✓ | **Art. 89(1)** — public space recording involves incidental bystander speech. *Prerequisite:* T1-group written consent AND deletion protocol. Exclude clips where bystander speech is intelligible. |

---

## Data Management Plan (DMP) Skeleton

Points to `docs/DMP.md` (DFG-aligned):
- **§1 Data types, formats:** Clotho/AudioCaps (external), weights (~60GB), Bamberg bells (~300MB), Results (~10MB)
- **§3 Storage & security:** Uni Bamberg GitLab + regional encrypted SSD
- **§4 Legal & ethical:** GDPR Art. 89 clause
- **§5 Retention:** 5yr research retention; raw audio deletion post-thesis

---

## Risk Register (w/ Cook 1991 Calibration)

*Cook Probability Definitions: HIGH (>50%), MED (10-50%), LOW (<10%).*

| # | Risk | P | Impact | Mitigation |
|:-:|:-----|:-:|:------:|:-----------|
| R1 | VRAM insufficient for AF3-8B bf16 | HIGH | Critical | Colab Pro + RZ Day 0; int4 fallback with quality delta documented |
| R2 | Java/SPICE silent failure | MED | High | `setup_check.py` smoke-tests `aac_metrics.evaluate` before any inference |
| R12 | Data contamination voids RQ1 zero-shot claim | MED | Critical | RQ0 gating audit in Phase 1; report clean-subset numbers + disclose |
| R14 | CC v4 WavCaps MD5 KeyError | — | Critical | Fixed by using FreeSound IDs correctly |
| R15 | CC v4 CLAP shape error in hallucination | — | Critical | Fixed by relying on sklearn cosine |
| **R17** | SM < 8.0 hardware degrades bf16 silently | MED | High | `setup_check.py` explicit Ampere+ gate |
| **R18** | `transformers` pin too loose | MED | High | Guard >= 4.44 in `setup_check.py` |
| **R19** | Holm-Bonferroni renders H3 non-significant | MED | Med | Report both uncorrected and Holm-adjusted p-values |
| **R21** | Bystander speech in T1 bells | LOW | Critical | GDPR pseudonymisation bounds; manual QA exclusions |
| **R22** | Neg-control hallucination rate is low | MED | Med | Mechanism weakened; adjust Discussion chapter |

---

## Verification Plan & Integrity Gate (v5 + v6 Combined)

Before Phase 2 begins, all of these MUST be green:
- [ ] `CLOTHO_ZENODO_RECORD=4783391` asserted 
- [ ] DCASE 29.6% canary reproduced ± 1% 
- [ ] RQ0 contamination audit executed; `clean_fraction` reported 
- [ ] Negative-control battery generated; baseline hallucination logged
- [ ] `hypotheses_preregistered.yml` committed with git SHA (w/ Holm-Bonf + BCa flags)
- [ ] `setup_check.py` exits 0 on RZ / Colab Pro (w/ SM≥8.0 gating)
- [ ] κ ≥ 0.6 on polyphony labelling logged 
- [ ] Pixel-diff CI on figures passes 
- [ ] License audit + GDPR Art. 89(1) clause satisfied for T1 Bamberg bell clips

---

## Evidence Provenance (v5 + v6 Trail)

| Source | Level | Year | Conf | Applic | Status |
|:-------|:------|:----:|:----:|:------:|:------:|
| NVIDIA Compute Capability / PyTorch determinism | L1 | 2024 | HIGH | HIGH | ACCEPTED |
| Holm (Scand. J. Stat. 1979) / Efron (1993 bootstrap) | L2 | — | HIGH | HIGH | STALE-VALID |
| Kerr (HARKing fallacy) / Cook (Probability) | L2 | — | HIGH | HIGH | ACCEPTED |
| GDPR Regulation (EU) 2016/679 Art. 89(1) | L3 | 2016 | HIGH | HIGH | STATUTORY |
| DFG Guidelines for Research Data | L3 | 2015 | HIGH | HIGH | ACCEPTED |
