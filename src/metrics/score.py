"""Score caption predictions against references with aac-metrics.

Runs from the WSL .venv-wsl venv (needs OpenJDK 11 for SPICE/METEOR):

    source .venv-wsl/bin/activate
    python -m src.metrics.score \
        --predictions results/cnn14_eval.json \
        --out results/cnn14_eval_scores.json

Reads the predictions JSON written by src/pipeline/run_inference.py, computes
the DCASE-standard metric bundle via `aac_metrics.functional.evaluate`, and
writes a sibling scores JSON. MACE is a separate metric stack and will be
added in a follow-up task.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _as_float(v):
    """aac-metrics returns 0-d torch tensors; unwrap to plain float for JSON."""
    try:
        import torch
        if isinstance(v, torch.Tensor):
            return float(v.detach().cpu().item())
    except ImportError:
        pass
    return float(v)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument(
        "--metrics", default="dcase2023",
        help="aac_metrics preset name. 'dcase2023' is the validated default "
             "(aac-metrics 0.5.x has no 'dcase2024' preset); 'all' / 'default' "
             "also accepted, or a comma-separated list of metric names.",
    )
    args = parser.parse_args()

    with args.predictions.open("r", encoding="utf-8") as f:
        pred = json.load(f)

    items = pred["items"]
    candidates = [it["prediction"] for it in items]
    mult_references = [it["references"] for it in items]
    print(f"[score] {len(items)} items, metric preset: {args.metrics}", file=sys.stderr)

    from aac_metrics.functional.evaluate import evaluate
    corpus_scores, _sent_scores = evaluate(candidates, mult_references, metrics=args.metrics)
    flat = {k: _as_float(v) for k, v in corpus_scores.items()}

    out = {
        "model": pred.get("model"),
        "split": pred.get("split"),
        "decode": pred.get("decode"),
        "audio": pred.get("audio"),
        "n_items": len(items),
        "metric_preset": args.metrics,
        "metrics": flat,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"[done] wrote {args.out}", file=sys.stderr)
    for k in sorted(flat):
        print(f"  {k:24s} {flat[k]:.4f}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
