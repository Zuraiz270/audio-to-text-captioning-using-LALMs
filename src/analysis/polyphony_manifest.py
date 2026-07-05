"""Poly/mono split from the SED framewise summary (RQ2, cheap + re-runnable).

Applies the P2 operational definition — a clip is polyphonic iff two AudioSet
classes are simultaneously active for >= 1 s at confidence >= tau — to the
summary produced by sed_summary.py, and writes:
  - data/polyphony_manifest.csv   (file_name,is_polyphonic + diagnostics;
                                   the format src/data/clotho.py:filter_polyphony expects)
  - subsets/poly.txt, subsets/mono.txt  (one file_name per line, for score.py --subset)

Anti-HARKing note: tau=0.50 is the pre-registered primary (public P2 definition).
The fallback rule was committed BEFORE any Delta results were seen: if either
bucket has < 150 clips at 0.50, use the largest stored tau giving both >= 300.

Usage (in .venv):
  python -m src.analysis.polyphony_manifest [--tau 0.5] [--min-overlap-s 1.0]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

FALLBACK_MIN, FALLBACK_TARGET = 150, 300


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", type=Path, default=Path("results/sed_framewise_summary.json"))
    parser.add_argument("--tau", type=float, default=0.50)
    parser.add_argument("--min-overlap-s", type=float, default=1.0)
    parser.add_argument("--manifest", type=Path, default=Path("data/polyphony_manifest.csv"))
    parser.add_argument("--subset-dir", type=Path, default=Path("subsets"))
    args = parser.parse_args()

    repo = Path(__file__).resolve().parents[2]
    summary = json.loads((repo / args.summary).read_text(encoding="utf-8"))
    tau_grid = sorted(summary["tau_grid"], reverse=True)  # e.g. [0.5, 0.3, 0.25, 0.2]

    def split_at(tau: float) -> pd.DataFrame:
        key = f"{tau:.2f}"
        rows = []
        for clip in summary["clips"]:
            t = clip["per_tau"][key]
            rows.append({
                "file_name": clip["file_name"],
                "is_polyphonic": t["max_pairwise_overlap_s"] >= args.min_overlap_s,
                "tau": tau,
                "max_pairwise_overlap_s": t["max_pairwise_overlap_s"],
                "n_active_classes": t["n_active_classes"],
                "best_pair": " | ".join(t["best_pair"]) if t["best_pair"] else "",
            })
        return pd.DataFrame(rows)

    # Report the split at every stored tau (transparency), pick per the rule.
    print("tau   poly  mono  zero-active", file=sys.stderr)
    counts = {}
    for tau in tau_grid:
        df_t = split_at(tau)
        n_poly = int(df_t["is_polyphonic"].sum())
        n_zero = int((df_t["n_active_classes"] == 0).sum())
        counts[tau] = (n_poly, len(df_t) - n_poly)
        print(f"{tau:.2f}  {n_poly:5d} {len(df_t)-n_poly:5d}  {n_zero:5d}", file=sys.stderr)

    chosen = args.tau
    n_poly, n_mono = counts[chosen]
    if min(n_poly, n_mono) < FALLBACK_MIN:
        for tau in tau_grid:  # largest tau first
            if min(counts[tau]) >= FALLBACK_TARGET:
                chosen = tau
                break
        else:
            chosen = min(counts, key=lambda t: -min(counts[t]))  # best available
        print(f"[fallback] tau={args.tau:.2f} degenerate "
              f"(poly={n_poly}, mono={n_mono}); using tau={chosen:.2f} "
              f"per pre-committed rule", file=sys.stderr)

    df = split_at(chosen)
    manifest_path = repo / args.manifest
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(manifest_path, index=False)

    subset_dir = repo / args.subset_dir
    subset_dir.mkdir(parents=True, exist_ok=True)
    poly = df.loc[df["is_polyphonic"], "file_name"]
    mono = df.loc[~df["is_polyphonic"], "file_name"]
    (subset_dir / "poly.txt").write_text("\n".join(poly) + "\n", encoding="utf-8")
    (subset_dir / "mono.txt").write_text("\n".join(mono) + "\n", encoding="utf-8")

    print(f"[done] tau={chosen:.2f}: {len(poly)} poly / {len(mono)} mono "
          f"-> {manifest_path}, {subset_dir}/poly.txt, {subset_dir}/mono.txt", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
