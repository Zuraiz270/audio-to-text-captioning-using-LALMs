#!/bin/bash
# Score all six rows on the poly and mono subsets (RQ2), with per-item scores
# for the bootstrap. Sequential: SPICE's JVM is memory-hungry.
set -uo pipefail
cd "$(dirname "$0")/.."
for m in af3 salmonn qwen_omni enclap cnn14 ast; do
  for s in poly mono; do
    echo "=== $m / $s ==="
    .venv-wsl/bin/python -m src.metrics.score \
      --predictions "results/${m}_eval.json" \
      --out "results/${m}_eval_scores_${s}.json" \
      --subset "subsets/${s}.txt" \
      --per-item "results/${m}_eval_peritem_${s}.json" 2>&1 | tail -2
  done
done
echo ALL_SUBSET_RUNS_DONE
