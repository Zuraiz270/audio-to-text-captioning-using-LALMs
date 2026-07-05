#!/bin/bash
# Re-score all six rows on the full set, emitting per-item sentence scores
# (bootstrap input). Sequential on purpose: SPICE's JVM is memory-hungry.
set -uo pipefail
cd "$(dirname "$0")/.."
for m in af3 salmonn qwen_omni enclap cnn14 ast; do
  echo "=== $m ==="
  .venv-wsl/bin/python -m src.metrics.score \
    --predictions "results/${m}_eval.json" \
    --out "results/${m}_eval_scores_check.json" \
    --per-item "results/${m}_eval_peritem_full.json" 2>&1 | tail -3
done
echo ALL_PERITEM_FULL_DONE
