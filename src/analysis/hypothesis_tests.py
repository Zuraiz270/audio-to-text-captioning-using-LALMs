"""Preregistered hypothesis tests (BCa bootstrap, Holm-Bonferroni).

Implements hypotheses_preregistered.yml exactly where possible and documents
every deviation (the prereg was drafted but never frozen; all deviations are
listed in the term paper):
  H1  SPIDEr-FL(AF3) > 0.261 on full Clotho-eval (one-sided; CLEAN subset was
      never defined -> full set, same clip set as the 26.1% baseline anchor).
  H2  Delta SPIDEr-FL (poly - mono) > 0 per LALM. Poly/mono are DISJOINT clip
      sets, so the prereg's "paired" wording is undefined as written ->
      two-sample bootstrap (disclosed). AF3 = prereg primary.
  H3  AF3 > SALMONN, SPIDEr-FL, PAIRED per-clip on full Clotho-eval
      (prereg said AudioCaps-single two-sample; dataset never acquired ->
      Clotho paired replacement, statistically stronger, disclosed).
  H4  CHAIR-s(AF3) < CHAIR-s(SALMONN), paired indicator differences, at
      tau 0.25 primary with [0.20, 0.30] sensitivity per the prereg
      reporting rule (INDETERMINATE if threshold-sensitive).

Bootstrap: BCa, n_resamples=1000, rng=default_rng(42) per test (prereg).
One-sided 95% lower bound == lower endpoint of the two-sided 90% BCa CI.
Bootstrap p-values: (1 + #{resamples <= null}) / (B + 1); resolution 1/1001.
Holm-Bonferroni within family_1 {H1, H2-AF3, H3}; family_2 {H4} alone.

Usage (in .venv):  python -m src.analysis.hypothesis_tests
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.stats import bootstrap

B = 1000
SEED = 42
H1_THRESHOLD = 0.261
H1_MDE = 0.0104
H2_MDE = 0.0150
REPO = Path(__file__).resolve().parents[2]


def _peritem(path: str, metric: str = "spider_fl") -> dict[str, float]:
    d = json.loads((REPO / path).read_text(encoding="utf-8"))
    return {it["file_name"]: it["scores"][metric] for it in d["items"]}


def _boot_one_sample(x: np.ndarray, null: float) -> dict:
    """Mean, one-sided 95% lower bound (BCa), bootstrap p for alt mean > null."""
    rng = np.random.default_rng(SEED)
    res = bootstrap((x,), np.mean, n_resamples=B, method="BCa",
                    confidence_level=0.90, rng=rng)
    dist = res.bootstrap_distribution
    p = (1 + int((dist <= null).sum())) / (B + 1)
    return {
        "mean": float(x.mean()), "n": int(x.size),
        "ci95_lower_one_sided": float(res.confidence_interval.low),
        "p_boot_one_sided": p,
    }


def _boot_two_sample(a: np.ndarray, b: np.ndarray) -> dict:
    """mean(a) - mean(b), BCa CI + one-sided bootstrap p for alt diff > 0."""
    rng = np.random.default_rng(SEED)

    def stat(x, y, axis):
        return x.mean(axis=axis) - y.mean(axis=axis)

    res = bootstrap((a, b), stat, n_resamples=B, method="BCa",
                    confidence_level=0.90, rng=rng)
    dist = res.bootstrap_distribution
    p = (1 + int((dist <= 0.0).sum())) / (B + 1)
    return {
        "diff": float(a.mean() - b.mean()), "n_a": int(a.size), "n_b": int(b.size),
        "ci95_lower_one_sided": float(res.confidence_interval.low),
        "p_boot_one_sided": p,
    }


def _paired_diffs(a: dict[str, float], b: dict[str, float]) -> np.ndarray:
    keys = sorted(set(a) & set(b))
    if len(keys) < min(len(a), len(b)):
        print(f"[warn] paired keys {len(keys)} < inputs {len(a)}/{len(b)}", file=sys.stderr)
    return np.array([a[k] - b[k] for k in keys])


def _holm(pvals: dict[str, float], alpha: float = 0.05) -> dict[str, dict]:
    """Holm-Bonferroni step-down; returns per-test corrected alpha + verdict."""
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    k = len(items)
    out, rejected = {}, True
    for rank, (name, p) in enumerate(items):
        alpha_prime = alpha / (k - rank)
        rejected = rejected and (p <= alpha_prime)  # step-down stops at first failure
        out[name] = {"p": p, "alpha_prime": round(alpha_prime, 5), "reject_null": bool(rejected)}
    return out


def main() -> int:
    results: dict = {"config": {"method": "BCa", "n_resamples": B, "seed": SEED,
                                "p_resolution": round(1 / (B + 1), 5)}}

    # ---- H1 ----------------------------------------------------------------
    af3_full = _peritem("results/af3_eval_peritem_full.json")
    h1 = _boot_one_sample(np.array(list(af3_full.values())), H1_THRESHOLD)
    h1["null"] = f"mean SPIDEr-FL(AF3) <= {H1_THRESHOLD}"
    h1["kill_flag"] = h1["ci95_lower_one_sided"] <= H1_THRESHOLD + H1_MDE
    h1["deviation"] = "evaluated on full Clotho-eval; CLEAN subset was never defined"
    results["H1_RQ1"] = h1

    # ---- H2 (per LALM; AF3 primary) ----------------------------------------
    results["H2_RQ2"] = {}
    for model in ("af3", "qwen_omni", "salmonn"):
        try:
            poly = _peritem(f"results/{model}_eval_peritem_poly.json")
            mono = _peritem(f"results/{model}_eval_peritem_mono.json")
        except FileNotFoundError as e:
            results["H2_RQ2"][model] = {"skipped": f"missing input: {e.filename}"}
            continue
        h2 = _boot_two_sample(np.array(list(poly.values())), np.array(list(mono.values())))
        h2["null"] = "mean(poly) - mean(mono) = 0 (alt: > 0)"
        h2["kill_flag"] = h2["diff"] < H2_MDE
        h2["deviation"] = ("two-sample bootstrap: poly/mono are disjoint clip sets, "
                           "the prereg's 'paired' wording is undefined as written")
        results["H2_RQ2"][model] = h2

    # ---- H3 (paired AF3 vs SALMONN, full set) ------------------------------
    salmonn_full = _peritem("results/salmonn_eval_peritem_full.json")
    d = _paired_diffs(af3_full, salmonn_full)
    h3 = _boot_one_sample(d, 0.0)
    h3["null"] = "mean per-clip [AF3 - SALMONN] SPIDEr-FL = 0 (alt: > 0)"
    h3["deviation"] = "Clotho-eval paired replacement for unacquired AudioCaps-single"
    results["H3_RQ3_spider"] = h3

    # ---- H4 (paired CHAIR-s indicators, tau sensitivity) --------------------
    chair_path = REPO / "results/chair_audio.json"
    if chair_path.exists():
        chair = json.loads(chair_path.read_text(encoding="utf-8"))
        ind = chair["h4_indicators"]
        h4_by_tau = {}
        for tau in ("0.25", "0.20", "0.30"):
            a = {k: float(v) for k, v in ind["salmonn"][tau].items()}
            b = {k: float(v) for k, v in ind["af3"][tau].items()}
            d4 = _paired_diffs(a, b)  # >0 means SALMONN hallucinates more
            t = _boot_one_sample(d4, 0.0)
            t["null"] = "CHAIR-s(SALMONN) - CHAIR-s(AF3) = 0 (alt: > 0)"
            h4_by_tau[tau] = t
        rejects = {tau: h4_by_tau[tau]["p_boot_one_sided"] <= 0.05 for tau in h4_by_tau}
        h4_by_tau["threshold_sensitive"] = len(set(rejects.values())) > 1
        h4_by_tau["verdict"] = ("INDETERMINATE (threshold-sensitive)"
                                if h4_by_tau["threshold_sensitive"]
                                else ("reject_null" if rejects["0.25"] else "retain_null"))
        h4_by_tau["deviation"] = "Clotho-eval paired replacement; dual-criterion CHAIR"
        results["H4_RQ3_chair"] = h4_by_tau
    else:
        results["H4_RQ3_chair"] = {"skipped": "results/chair_audio.json not found"}

    # ---- Holm-Bonferroni ----------------------------------------------------
    fam1 = {"H1": results["H1_RQ1"]["p_boot_one_sided"],
            "H3": results["H3_RQ3_spider"]["p_boot_one_sided"]}
    if isinstance(results["H2_RQ2"].get("af3"), dict) and "p_boot_one_sided" in results["H2_RQ2"]["af3"]:
        fam1["H2_af3"] = results["H2_RQ2"]["af3"]["p_boot_one_sided"]
    results["holm_family_1"] = _holm(fam1)
    if "p_boot_one_sided" in results.get("H4_RQ3_chair", {}).get("0.25", {}):
        results["holm_family_2"] = _holm({"H4": results["H4_RQ3_chair"]["0.25"]["p_boot_one_sided"]})

    out = REPO / "results/hypothesis_tests.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(results, indent=1)[:2000], file=sys.stderr)
    print(f"[done] -> {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
