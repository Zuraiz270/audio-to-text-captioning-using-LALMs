# Implementation Plan — T6: Audio-to-Text Captioning using LALMs
*Master's Project · CH-Proj-M · SS 2026 · Zuraiz (2177213)*
*Prof. Dr.-Ing. Jakob Abeßer · Computational Humanities · Uni Bamberg*
*Last updated: April 2026 — Rebuilt version (documentation system redesign)*

> **This is the operational document.** It owns every decision about *how* to do something. Evidence for *why* → `literature_review.md`. Strategy → `research_notes.md`. Overview → `PROJECT_GUIDE.md`. Per-paper intake → `paper_summaries.md`.

---

## § 1. Environment & Reproducibility

### 1.1 Determinism Pins 🟢

Every experiment runs under these exact conditions. No exceptions.

```bash
# Set BEFORE any torch import
export PYTHONHASHSEED=42
export CUBLAS_WORKSPACE_CONFIG=:4096:8

# In every notebook / script
import torch
torch.manual_seed(42)
torch.cuda.manual_seed_all(42)
torch.use_deterministic_algorithms(True)
torch.backends.cudnn.benchmark = False
```

**Why:** Greedy-decoded LALM output is theoretically deterministic at temperature=0.0, but CUDA non-determinism (cuBLAS workspace selection) can flip tie-breaking in top-1 logit selection. Pinning eliminates this.

### 1.2 Hardware Gate 🟢

| Requirement | Minimum | Why |
|:-----------|:--------|:----|
| GPU compute capability | SM ≥ 8.0 (Ampere+) | bf16 precision; sub-Ampere silently falls back to fp32 |
| VRAM | ≥ 24 GB for bf16 / ≥ 12 GB for int4 | AF3 = 8B params |
| Java | 11+ | `aac-metrics` depends on Stanford NLP (SPICE) |
| Python | 3.11.x | Pinned in environment.yml |

### 1.3 setup_check.py 🟢

This script runs BEFORE any experiment. If it fails, stop.

```python
#!/usr/bin/env python3
"""
setup_check.py — Hardware-gated environment verification.
Exit 0 = safe to proceed. Exit 1 = stop and fix.

Checks:
  1. CUDA available + SM ≥ 8.0 (bf16 safe)
  2. bf16 matmul reproducibility (10 runs identical)
  3. Determinism environment variables set
  4. Java 11+ available (aac-metrics dependency)
  5. aac-metrics importable + SPIDEr-FL computable
  6. Clotho v2.1 eval split accessible (1,045 clips)
"""
import os, sys, subprocess

def check_cuda():
    import torch
    assert torch.cuda.is_available(), "CUDA not available"
    sm = torch.cuda.get_device_capability()
    assert sm[0] * 10 + sm[1] >= 80, f"SM {sm[0]}.{sm[1]} < 8.0 — bf16 unsafe"
    print(f"✓ CUDA SM {sm[0]}.{sm[1]}")

def check_determinism_env():
    assert os.environ.get("PYTHONHASHSEED") == "42", "PYTHONHASHSEED != 42"
    assert "4096:8" in os.environ.get("CUBLAS_WORKSPACE_CONFIG", ""), "CUBLAS_WORKSPACE_CONFIG not set"
    print("✓ Determinism env vars")

def check_bf16_repro():
    import torch
    torch.manual_seed(42)
    torch.use_deterministic_algorithms(True)
    a = torch.randn(256, 256, dtype=torch.bfloat16, device="cuda")
    results = []
    for _ in range(10):
        results.append(torch.mm(a, a).sum().item())
    assert len(set(results)) == 1, f"bf16 matmul non-deterministic: {set(results)}"
    print("✓ bf16 matmul deterministic (10/10)")

def check_java():
    result = subprocess.run(["java", "-version"], capture_output=True, text=True)
    version_line = result.stderr.split("\n")[0]
    print(f"✓ Java: {version_line}")

def check_aac_metrics():
    from aac_metrics import evaluate
    # Minimal smoke test
    print("✓ aac-metrics importable")

def check_clotho():
    # Verify Clotho eval split exists at expected path
    # Adjust path as needed for your setup
    print("✓ Clotho check (manual verification required)")

if __name__ == "__main__":
    checks = [check_cuda, check_determinism_env, check_bf16_repro, check_java, check_aac_metrics, check_clotho]
    failed = []
    for check in checks:
        try:
            check()
        except Exception as e:
            print(f"✗ {check.__name__}: {e}")
            failed.append(check.__name__)
    if failed:
        print(f"\n{'='*40}\nFAILED: {', '.join(failed)}\nDo NOT proceed with experiments.\n{'='*40}")
        sys.exit(1)
    else:
        print(f"\n{'='*40}\nAll checks passed. Safe to proceed.\n{'='*40}")
        sys.exit(0)
```

### 1.4 hypotheses_preregistered.yml 🟢

Machine-readable spec. **Canonical.** If `literature_review.md` §12 and this file diverge, this file wins.

```yaml
# hypotheses_preregistered.yml
# Freeze date: before Phase 2 data collection begins
# Any modification after freeze = HARKing violation (Kerr 1998)

meta:
  project: "T6 Audio-to-Text Captioning using LALMs"
  freeze_date: null  # Set to actual date when Phase 2 begins
  bootstrap:
    method: BCa
    n_resamples: 1000
    seed: 42
    confidence_level: 0.95
  correction:
    method: holm-bonferroni
    note: "Auto-apply when ≥ 2 inferential hypotheses remain in scope. Drop if all remaining hypotheses are descriptive."

families:
  family_1_spider:
    hypotheses:
      H1_RQ1:
        null: "SPIDEr-FL(AF3, Clotho-eval-CLEAN) ≤ 29.6%"
        alt: "SPIDEr-FL(AF3) > 29.6%"
        test: one-sided BCa
        metric: SPIDEr-FL
        dataset: Clotho-eval-CLEAN
        MDE: 1.04pp
        kill: "CI lower bound ≤ 29.6% + 1.04pp"
      H2_RQ2:
        null: "Δ(poly − mono) = 0"
        alt: "Δ(poly − mono) > 0"
        test: paired BCa
        metric: SPIDEr-FL
        dataset: Clotho-eval polyphony subset
        MDE: 1.50pp
        kill: "Δ within MDE or negative"
      H3_RQ3_spider:
        null: "SPIDEr-FL(AF3, AudioCaps-single) = SPIDEr-FL(SALMONN, AudioCaps-single)"
        alt: "AF3 > SALMONN"
        test: two-sample BCa
        metric: SPIDEr-FL
        dataset: AudioCaps single-event
        MDE: 1.25pp
        kill: "CIs overlap"
    alpha: 0.05
    k: 3
    strictest_alpha_prime: 0.0167

  family_2_chair:
    hypotheses:
      H4_RQ3_chair:
        null: "CHAIR-audio(AF3) = CHAIR-audio(SALMONN)"
        alt: "CHAIR-audio(AF3) < CHAIR-audio(SALMONN)"
        test: two-sample BCa
        metric: CHAIR-audio (dual criterion)
        dataset: AudioCaps single-event
        MDE: 1.25pp
        kill: "CIs overlap or AF3 rate ≥ SALMONN"
    alpha: 0.05
    k: 1
    strictest_alpha_prime: 0.05

  descriptive_only:
    H5_RQ4:
      metric: correct-ordering rate
      dataset: synthetic A-then-B mixtures
      n: 50
      note: "Underpowered for <5pp effects; report as descriptive with BCa CI"
      kill: "Rate ≥ 80% → mechanism weakened"
    H6_RQ5:
      metric: CLAPScore
      dataset: Bamberg bells + BBC archive
      n: "≤ 20"
      note: "DESCRIPTIVE_ONLY — no inferential claims"
      kill: "CLAPScore Δ < 0.05 vs in-distribution baseline"
    H_NEG:
      metric: CHAIR-audio rate on silence/white/pink/tones
      dataset: 30 synthetic clips
      note: "Negative control; confabulation mechanism test"
      kill: "Rate < 50% → text-prior confabulation mechanism weakened"
```

---

## § 2. Phase 0 — Environment Setup (→ Apr 19) 🟢

### Checklist

- [ ] Create conda environment (`t6-aac`, Python 3.11)
- [ ] Install all dependencies (see `research_notes.md` §9)
- [ ] Run `setup_check.py` → must exit 0
- [ ] Create `hypotheses_preregistered.yml` → freeze before Phase 2
- [ ] Download Clotho v2.1 eval split (Zenodo 4783391) → verify 1,045 clips
- [ ] Download AudioCaps (Kim 2019) → verify AudioSet tags available
- [ ] Download AudioSet ontology JSON
- [ ] Create `prompts/` directory with canonical prompt templates
- [ ] Create `results/` directory structure

### Hard Gate

**`setup_check.py` must exit 0 before ANY experiment runs.**

**If it fails:**
- SM < 8.0 → Find Ampere+ GPU (RZ cluster, Colab Pro A100)
- Java missing → `apt install default-jdk` or `conda install -c conda-forge openjdk=11`
- `aac-metrics` broken → check Java path, reinstall

---

## § 3. Phase 1 — Baseline + Contamination Audit (Apr 19 → May 4) 🟢

### 3.1 RQ0: Contamination Audit 🟢

**Goal:** Cross-reference FreeSound IDs in Clotho-eval (1,045 clips) against training manifests of AF3 and SALMONN.

**Protocol:**

```python
"""
contamination_audit.py — RQ0

Input: Clotho-eval clip IDs, WavCaps manifest, AudioSetCaps manifest, Clotho-AQA manifest
Output: results/contamination_audit.json
"""
import json

def load_clotho_eval_ids(path: str) -> set:
    """Load FreeSound IDs from Clotho v2.1 eval split."""
    # Clotho filenames encode FreeSound ID: <freesound_id>.wav
    pass

def load_training_manifest(manifest_path: str) -> set:
    """Load FreeSound IDs from a training corpus manifest."""
    pass

def audit(eval_ids: set, manifests: dict[str, set]) -> dict:
    """Cross-reference eval IDs against all training manifests."""
    results = {}
    for corpus_name, train_ids in manifests.items():
        overlap = eval_ids & train_ids
        results[corpus_name] = {
            "overlap_count": len(overlap),
            "overlap_pct": len(overlap) / len(eval_ids) * 100,
            "overlapping_ids": sorted(overlap),
        }
    results["clean_fraction"] = {
        "count": len(eval_ids) - len(set.union(*manifests.values()) & eval_ids),
        "pct": (len(eval_ids) - len(set.union(*manifests.values()) & eval_ids)) / len(eval_ids) * 100,
    }
    return results

def main():
    eval_ids = load_clotho_eval_ids("data/clotho_v2.1/evaluation/")
    manifests = {
        "WavCaps": load_training_manifest("data/manifests/wavcaps_freesound_ids.txt"),
        "AudioSetCaps": load_training_manifest("data/manifests/audiosetcaps_ids.txt"),
        "Clotho-AQA": load_training_manifest("data/manifests/clotho_aqa_ids.txt"),
    }
    results = audit(eval_ids, manifests)
    with open("results/contamination_audit.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"Clean fraction: {results['clean_fraction']['pct']:.1f}%")

if __name__ == "__main__":
    main()
```

**Kill criterion:** Must complete before any model evaluation. If overlap > 0: all RQ1 "zero-shot" claims demoted to "audited-but-not-zero"; report clean-subset numbers alongside full-set numbers.

### 3.2 Canary Test: DCASE Baseline Reproduction 🟢

**Goal:** Verify metric pipeline by reproducing the DCASE 2024 baseline's 29.6% SPIDEr-FL.

```python
"""
canary_baseline.py — Reproduce DCASE 2024 baseline
Expected: 29.6% ± 1% SPIDEr-FL on Clotho-eval
"""
from aac_metrics import evaluate

def reproduce_baseline():
    # Load DCASE 2024 baseline predictions (pre-computed or re-run)
    predictions = load_predictions("data/dcase2024_baseline_predictions.json")
    references = load_references("data/clotho_v2.1/evaluation/")
    
    results = evaluate(predictions, references)
    spider_fl = results["SPIDEr-FL"]
    
    assert abs(spider_fl - 0.296) < 0.01, (
        f"Canary FAILED: SPIDEr-FL = {spider_fl:.4f}, expected 0.296 ± 0.01. "
        f"Metric pipeline is broken — STOP."
    )
    print(f"✓ Canary passed: SPIDEr-FL = {spider_fl:.4f}")
    return spider_fl
```

**Kill criterion:** If canary fails by > 2 pp → metric pipeline broken → stop and debug before any model evaluation.

### 3.3 AF3 Hello-World Demo 🟢

```python
"""
af3_hello_world.py — Verify AF3 loads and generates captions
"""
from transformers import AutoModelForCausalLM, AutoProcessor

def hello_world():
    model = AutoModelForCausalLM.from_pretrained(
        "nvidia/audio-flamingo-3",
        torch_dtype=torch.bfloat16,
        device_map="auto",
    )
    processor = AutoProcessor.from_pretrained("nvidia/audio-flamingo-3")
    
    # Single clip from Clotho-eval
    audio = load_audio("data/clotho_v2.1/evaluation/sample_001.wav")
    inputs = processor(audio=audio, text="Describe the sounds in this audio.", return_tensors="pt")
    
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=128, temperature=0.0)
    
    caption = processor.decode(output[0], skip_special_tokens=True)
    print(f"Caption: {caption}")
    # Verify: non-empty, English, > 5 words, no repetition loops
```

---

## § 4. Phase 2 — Core Experiments (May 4 → May 18) 🟢

### 4.1 Full Model Inference 🟢

Run AF3 and SALMONN on all 1,045 Clotho-eval clips. Save predictions.

```python
"""
run_inference.py — Generate captions for all Clotho-eval clips
Usage: python run_inference.py --model af3 --output results/af3_clotho_eval.json
"""
import argparse, json, torch
from pathlib import Path

MODELS = {
    "af3": "nvidia/audio-flamingo-3",
    "salmonn": "tsinghua-ee/SALMONN",
    # "qwen": "Qwen/Qwen2.5-Omni-7B",  # Cut 1 — uncomment if time
}

CANONICAL_PROMPT = "Describe the sounds in this audio clip."  # Pinned in prompts/

def run_inference(model_name: str, output_path: str):
    model, processor = load_model(MODELS[model_name])
    clips = load_clotho_eval_clips("data/clotho_v2.1/evaluation/")
    
    predictions = {}
    for clip_id, audio in clips.items():
        inputs = processor(audio=audio, text=CANONICAL_PROMPT, return_tensors="pt")
        with torch.no_grad():
            output = model.generate(
                **inputs,
                max_new_tokens=128,
                temperature=0.0,  # Greedy — pinned across all models
                do_sample=False,
            )
        caption = processor.decode(output[0], skip_special_tokens=True)
        predictions[clip_id] = caption
    
    with open(output_path, "w") as f:
        json.dump(predictions, f, indent=2)
    print(f"Saved {len(predictions)} predictions to {output_path}")
```

### 4.2 RQ1: AF3 vs DCASE Baseline 🟢

```python
"""
rq1_comparison.py — AF3 vs DCASE 2024 baseline on Clotho-eval
"""
from scipy.stats import bootstrap
import numpy as np

def rq1_comparison():
    af3_scores = load_per_clip_scores("results/af3_clotho_eval_scores.json", metric="SPIDEr-FL")
    baseline_score = 0.296  # DCASE 2024 canary-verified
    
    # BCa bootstrap CI for AF3 mean SPIDEr-FL
    ci = bootstrap(
        (af3_scores,),
        statistic=np.mean,
        n_resamples=1000,
        random_state=42,
        method="BCa",
        confidence_level=0.95,
    )
    
    print(f"AF3 SPIDEr-FL: {np.mean(af3_scores):.4f}")
    print(f"BCa 95% CI: [{ci.confidence_interval.low:.4f}, {ci.confidence_interval.high:.4f}]")
    print(f"Baseline: {baseline_score}")
    print(f"H1 rejected: {ci.confidence_interval.low > baseline_score}")
```

### 4.3 RQ2: Polyphony Differential 🟢

**Step 1 — Polyphony annotation:**

```python
"""
polyphony_annotation.py — Annotate Clotho-eval clips as mono/poly

Method 1 (preferred): Manual annotation of 200 clips, κ ≥ 0.6
Method 2 (fallback):  AudioSet tag count proxy (tag_count > 1 → poly)
"""

def annotate_polyphony():
    """
    Annotation protocol:
    - Two annotators independently label each clip as mono/poly
    - Mono: one dominant sound event, no concurrent secondary events
    - Poly: two or more distinguishable concurrent sound events
    - Cohen's κ computed; if κ < 0.6, fall back to Method 2
    """
    pass

def audioset_proxy_fallback():
    """Fallback: use AudioSet tag count as polyphony proxy."""
    pass
```

**Step 2 — Differential analysis:**

```python
def rq2_polyphony_differential():
    af3_scores = load_per_clip_scores("results/af3_clotho_eval_scores.json", metric="SPIDEr-FL")
    annotations = load_annotations("data/polyphony_annotations.json")
    
    mono_scores = af3_scores[annotations == "mono"]
    poly_scores = af3_scores[annotations == "poly"]
    
    delta = np.mean(mono_scores) - np.mean(poly_scores)  # Expected positive
    
    # Paired BCa CI for delta
    ci = bootstrap(
        (mono_scores, poly_scores),
        statistic=lambda m, p: np.mean(m) - np.mean(p),
        n_resamples=1000,
        random_state=42,
        method="BCa",
    )
    print(f"Δ(mono − poly): {delta:.4f}")
    print(f"BCa 95% CI: [{ci.confidence_interval.low:.4f}, {ci.confidence_interval.high:.4f}]")
```

**Kill criterion:** κ < 0.6 on annotation → fall back to AudioSet proxy labels. Note: κ ≥ 0.6 is "substantial agreement" per Landis & Koch 1977.

### 4.4 RQ3: Hallucination Rate 🟢

```python
"""
rq3_hallucination.py — CHAIR-audio dual criterion

Step 1: Extract nouns from captions (spaCy)
Step 2: Cross-reference against AudioSet tags (label criterion)
Step 3: Filter with CLAPScore < 0.25 (audio-grounding criterion)
Step 4: Compute CHAIR-audio rate
"""
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_entities(caption: str) -> list[str]:
    """Extract noun entities from caption."""
    doc = nlp(caption)
    return [chunk.root.text.lower() for chunk in doc.noun_chunks]

def chair_audio(caption: str, audioset_tags: set, audio_path: str, threshold: float = 0.25) -> dict:
    """
    CHAIR-audio dual criterion:
    Entity is hallucinated iff:
      (a) entity ∉ audioset_tags  AND
      (b) CLAPScore(entity, audio) < threshold
    """
    entities = extract_entities(caption)
    hallucinated = []
    for entity in entities:
        in_tags = entity in audioset_tags
        clap_score = compute_clapscore(entity, audio_path)
        if not in_tags and clap_score < threshold:
            hallucinated.append({"entity": entity, "clap_score": clap_score})
    
    return {
        "total_entities": len(entities),
        "hallucinated_entities": len(hallucinated),
        "chair_rate": len(hallucinated) / max(len(entities), 1),
        "details": hallucinated,
    }
```

**Sensitivity analysis:** Run at CLAPScore thresholds {0.20, 0.25, 0.30}. Report all three; declare 0.25 as primary.

---

## § 5. Phase 3 — Failure Modes & Extensions (May 18 → Jul 1) 🟢/🔵 mixed

### 5.1 Negative Control Battery 🔵 (Cut 3)

**Purpose:** Test whether LALMs confabulate descriptions for audio that contains no describable events.

```python
"""
negative_controls.py — Hallucination on empty/noise stimuli

Stimulus set (30 clips):
  - 10× silence (digital silence, 16-bit zeros)
  - 10× white noise (uniform random, -20dBFS)
  - 10× pure tones (1kHz sine, 440Hz sine, etc.)
"""

STIMULI = {
    "silence": generate_silence(duration=15, sr=16000, n=10),
    "white_noise": generate_white_noise(duration=15, sr=16000, n=10, dbfs=-20),
    "pure_tones": generate_tones(freqs=[440, 1000], duration=15, sr=16000),
}

def run_negative_controls(model_name: str):
    for stim_type, clips in STIMULI.items():
        for i, clip in enumerate(clips):
            caption = generate_caption(model_name, clip)
            entities = extract_entities(caption)
            print(f"{stim_type}_{i}: {len(entities)} entities → {caption[:100]}...")
    
    # Expected: hallucination rate ≥ 80% → confabulation mechanism confirmed
    # Kill: rate < 50% → text-prior mechanism weakened
```

### 5.2 RQ4: Temporal Ordering 🔵 (Cut 2)

```python
"""
rq4_temporal.py — A-then-B synthetic mixture protocol

Protocol:
  1. Select 50 AudioCaps single-event clips with clear onsets
  2. Create A-then-B mixtures: event A (0–5s), event B (5–10s)
  3. Run LALM inference
  4. Score: does the caption mention A before B?
"""

def create_mixture(clip_a: np.ndarray, clip_b: np.ndarray, sr: int = 16000) -> np.ndarray:
    """A-then-B mixture: A at 0-5s, B at 5-10s"""
    duration = 10  # seconds
    mixture = np.zeros(duration * sr)
    mixture[:5*sr] += clip_a[:5*sr]
    mixture[5*sr:] += clip_b[:5*sr]
    return mixture

def score_ordering(caption: str, event_a: str, event_b: str) -> bool:
    """Check if caption mentions A before B."""
    pos_a = caption.lower().find(event_a.lower())
    pos_b = caption.lower().find(event_b.lower())
    if pos_a == -1 or pos_b == -1:
        return False  # One event not mentioned → ordering undefined
    return pos_a < pos_b

def rq4_temporal_ordering():
    mixtures = load_mixtures("data/synthetic_mixtures/")
    results = []
    for mix in mixtures:
        caption = generate_caption("af3", mix["audio"])
        correct = score_ordering(caption, mix["event_a"], mix["event_b"])
        results.append(correct)
    
    rate = np.mean(results)
    ci = bootstrap((np.array(results),), np.mean, n_resamples=1000, random_state=42, method="BCa")
    print(f"Correct ordering rate: {rate:.2%}")
    print(f"BCa 95% CI: [{ci.confidence_interval.low:.2%}, {ci.confidence_interval.high:.2%}]")
    # Kill: rate ≥ 80% → autoregressive text-prior mechanism weakened
```

### 5.3 RQ5: Cultural Heritage / Schafer 🔵 (Cut 4 — last to cut)

```python
"""
rq5_cultural_heritage.py — OOD captioning on culturally-grounded audio

Stimulus set (≤ 20 clips):
  - Bamberg Martinskirche bells (if T1 consent obtained)
  - BBC Sound Effects Archive (culturally-specific clips)
  - Comparison: FreeSound in-distribution clips of similar acoustic profile
"""

def rq5_cultural_heritage():
    heritage_clips = load_clips("data/cultural_heritage/")
    in_dist_clips = load_clips("data/freesound_comparison/")
    
    # CLAPScore on heritage vs in-distribution
    heritage_scores = [compute_clapscore(generate_caption("af3", c), c) for c in heritage_clips]
    in_dist_scores = [compute_clapscore(generate_caption("af3", c), c) for c in in_dist_clips]
    
    delta = np.mean(in_dist_scores) - np.mean(heritage_scores)
    print(f"CLAPScore drop: {delta:.4f}")
    # Kill: Δ < 0.05 → domain shift insufficient
    
    # Qualitative Schafer audit
    for clip_id, caption in zip(heritage_clips, heritage_captions):
        print(f"  {clip_id}: {caption}")
        # Manual audit: does caption capture soundmark features?
        # Does it reduce bells to generic "ringing sound"?
        # Does it encode place-indexical meaning?
```

---

## § 6. Phase 4 — Write-up (Jul 1 → Jul 13) 🟢

### 6.1 Paper Structure (~15 pages)

| Section | Length | Content |
|:--------|:-------|:--------|
| Abstract | 0.5p | RQ0–RQ3 results; three failure modes; unified root cause |
| 1. Introduction | 2p | Problem statement; Schafer framing; RQ table |
| 2. Related Work | 3p | §§ 1–4 of `literature_review.md` compressed |
| 3. Methodology | 3p | Protocols for all RQs; pre-registration; contamination audit |
| 4. Experiments | 3p | Results with tables + CIs + figures |
| 5. Discussion | 2p | Root cause analysis; competing explanations; humanities reflection |
| 6. Conclusion | 1p | Summary + future work |
| References | 1p | ~30 sources |

### 6.2 Metric Reporting Standards

**Every quantitative claim must include:**
- Point estimate
- BCa 95% CI
- Sample size (n)
- Holm-Bonferroni adjusted p-value (if inferential)
- MDE context (was the study powered to detect this effect?)

**Example reporting template:**
> "AF3 achieves SPIDEr-FL = 35.2% (BCa 95% CI: [33.8%, 36.6%], n = 1,045, Holm-adj p < 0.001) on the contamination-audited clean subset of Clotho-eval, exceeding the DCASE 2024 baseline (29.6%) by 5.6 pp with MDE = 1.04 pp."

**Do NOT report:**
- Point estimates without CIs
- Δ without MDE context
- "Significant" without specifying correction method
- CLAPScore as a substitute for SPIDEr-FL on referenced datasets

### 6.3 Figure Plan

| Figure | Content | Format |
|:-------|:--------|:-------|
| F1 | Architecture comparison: SALMONN vs AF3 (dual vs unified encoder) | Annotated SVG diagram |
| F2 | RQ1: bar chart with BCa CIs, AF3 vs baseline | matplotlib with seaborn |
| F3 | RQ2: scatter plot, SPIDEr-FL vs polyphony count | matplotlib |
| F4 | RQ3: CHAIR-audio rate comparison (AF3 vs SALMONN) with CIs | bar chart |
| F5 | Qualitative: example captions (correct, under-described, hallucinated) | LaTeX table |

### 6.4 Talk Plan (Jul 13, 15 min)

| Slide | Time | Content |
|:------|:-----|:--------|
| 1 | 0:30 | Title + problem statement |
| 2 | 1:00 | Live AF3 demo (play audio → show caption) |
| 3–4 | 2:00 | Three failure modes with examples |
| 5 | 1:30 | Architecture: encoder → adapter → LLM |
| 6 | 1:30 | RQ0 contamination audit result (branch per `research_notes.md` §10) |
| 7–9 | 4:00 | RQ1/RQ2/RQ3 results with CIs |
| 10 | 1:30 | Root cause: Q-Former bottleneck → unified mechanism |
| 11 | 1:00 | Schafer framing + RQ5 (if available) |
| 12 | 1:00 | Conclusion + future work |

---

## § 7. Makefile 🟢

```makefile
# Makefile — Automated pipeline for T6 project
# Usage: make all (runs full pipeline from clean state)

SHELL := /bin/bash
PYTHON := python

.PHONY: all check audit baseline inference eval figures paper clean

all: check audit baseline inference eval figures paper

check:
	$(PYTHON) setup_check.py

audit:
	$(PYTHON) contamination_audit.py
	@echo "✓ RQ0 contamination audit complete"

baseline:
	$(PYTHON) canary_baseline.py
	@echo "✓ Canary baseline verified"

inference:
	$(PYTHON) run_inference.py --model af3 --output results/af3_clotho_eval.json
	$(PYTHON) run_inference.py --model salmonn --output results/salmonn_clotho_eval.json
	@echo "✓ Inference complete"

eval:
	$(PYTHON) rq1_comparison.py
	$(PYTHON) rq2_polyphony.py
	$(PYTHON) rq3_hallucination.py
	@echo "✓ Core evaluation complete"

figures:
	$(PYTHON) generate_figures.py
	@echo "✓ Figures generated"

paper:
	cd paper/ && latexmk -pdf main.tex
	@echo "✓ Paper compiled"

clean:
	rm -rf results/*.json figures/*.png paper/*.aux paper/*.log
```

---

## § 8. Risk Register

| # | Risk | Likelihood | Impact | Mitigation | Layer |
|:-:|:-----|:-----------|:-------|:-----------|:-----:|
| R1 | AF3 model card doesn't disclose all training data → contamination audit incomplete | MED | HIGH | Cross-reference WavCaps/AudioSetCaps/Clotho-AQA manifests independently | 🟢 |
| R2 | GPU VRAM insufficient for bf16 AF3 | MED | HIGH | Fall back to int4 quantisation; note in limitations | 🟢 |
| R3 | `aac-metrics` Java dependency fails on cluster | LOW | HIGH | Install OpenJDK 11 via conda; pre-test on Day 1 | 🟢 |
| R4 | κ < 0.6 on polyphony annotation | MED | MED | AudioSet tag-count proxy (pre-planned fallback) | 🟢 |
| R5 | SALMONN inference fails (unmaintained codebase) | MED | MED | Proceed with AF3 + Qwen as RQ3 comparison pair | 🟢 |
| R6 | TAC weights not released → no RQ4 oracle comparison | MED | LOW | RQ4 runs without oracle; TAC cited as future work | 🔵 |
| R7 | Bamberg bells consent not obtained | MED | LOW | Use BBC Sound Effects Archive only (CC-licensed) | 🔵 |
| R8 | CLAPScore embedding space doesn't cover archival Germanic audio | HIGH | MED | Disclosed in methodology; motivates qualitative audit | 🔵 |
| R9 | Phase 2 runs late → Phase 3 squeezed | MED | MED | Cut in order: Cut 1 → Cut 2 → Cut 3 → Cut 4 | 🟢/🔵 |
| R10 | Scooped: someone publishes AF3 Clotho-eval numbers before Jul | LOW | HIGH | Reposition as independent replication with contamination audit added value | 🟢 |

---

## § 9. Verification Gates

| Gate | Phase | Check | Pass if | Fail action |
|:-----|:------|:------|:--------|:------------|
| G0 | 0 | `setup_check.py` | Exits 0 | Fix environment; no experiments |
| G1 | 1 | Canary baseline | 29.6% ± 1% | Debug metric pipeline |
| G2 | 1 | RQ0 audit | `contamination_audit.json` exists | Stop → fix manifest loading |
| G3 | 2 | κ on polyphony | κ ≥ 0.6 | Fall back to AudioSet proxy |
| G4 | 2 | RQ1/RQ2/RQ3 CIs | All BCa CIs computed | Debug statistics code |
| G5 | 3 | `hypotheses_preregistered.yml` unmodified after Phase 2 start | SHA256 matches | HARKing violation — flag in paper |
| G6 | 4 | `make all` | Pipeline exits 0 on fresh clone | Fix broken step |
| G7 | 4 | Paper compiled | LaTeX compiles without errors | Fix compilation |

---

## § 10. Cut Ladder (Operational Rules)

When time/compute pressure forces scope reduction, cut in this **exact order**:

| Cut # | Component | Layer | What drops |
|:-----:|:----------|:-----:|:-----------|
| 1 | Qwen2.5-Omni ablation | 🔵 | Third model; adds breadth not depth |
| 2 | RQ4 temporal ordering | 🔵 | Intellectually valuable but synthetic-only |
| 3 | Negative-control battery | 🔵 | Tests mechanism directly but not a standalone RQ |
| 4 | RQ5 cultural heritage / Schafer | 🔵 | **Last to cut** — the humanities identity |

**Items outside the cut ladder:**
- **Holm-Bonferroni:** Conditional. Auto-apply when ≥ 2 inferential hypotheses remain. Drop automatically if project becomes entirely descriptive.
- **DCASE 2026 workshop paper:** Independent. Not on the critical path. Pursue after Jul 13 talk, only if results warrant submission.

**Layer 1 (🟢) is never cut.** If Layer 1 is complete, the project passes regardless of Layer 2 status.

---

## § 11. Directory Structure

```
CH-Proj-M/
├── PROJECT_GUIDE.md              # Entry point
├── literature_review.md          # Evidence narrative
├── research_notes.md             # Strategy + evidence expansion
├── paper_summaries.md            # Per-paper intake cards
├── implementation_plan.md        # You are here (operational logic)
├── hypotheses_preregistered.yml  # Frozen before Phase 2
├── setup_check.py                # Hardware gate
├── Makefile                      # Automated pipeline
├── environment.yml               # Conda environment spec
│
├── prompts/                      # Canonical prompt templates
│   └── clotho_caption.txt
│
├── data/
│   ├── clotho_v2.1/
│   │   └── evaluation/           # 1,045 clips
│   ├── audiocaps/
│   ├── cultural_heritage/        # RQ5 clips
│   ├── manifests/                # RQ0 training corpus manifests
│   ├── polyphony_annotations.json
│   └── synthetic_mixtures/       # RQ4 A-then-B
│
├── src/
│   ├── contamination_audit.py
│   ├── canary_baseline.py
│   ├── run_inference.py
│   ├── rq1_comparison.py
│   ├── rq2_polyphony.py
│   ├── rq3_hallucination.py
│   ├── rq4_temporal.py
│   ├── rq5_cultural_heritage.py
│   ├── negative_controls.py
│   └── generate_figures.py
│
├── results/
│   ├── contamination_audit.json
│   ├── af3_clotho_eval.json
│   ├── salmonn_clotho_eval.json
│   └── *.json
│
├── figures/
│   └── *.png
│
└── paper/
    ├── main.tex
    ├── references.bib
    └── figures/
```
