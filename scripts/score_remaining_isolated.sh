#!/bin/bash
# Runs from Git Bash on Windows. One wsl.exe invocation per scoring run, so a
# WSL crash costs one run, not the batch. Skips outputs that already exist.
set -u
REPO_WIN='E:\ISSS\Summer 2026\CH-Proj-M Master'\''s project Computational Humanities'
cd "$(dirname "$0")/.."

run_score() {  # args: model subset("full"|poly|mono)
  local m="$1" s="$2" args out peritem
  if [ "$s" = "full" ]; then
    out="results/${m}_eval_scores_check.json"
    peritem="results/${m}_eval_peritem_full.json"
    args=""
  else
    out="results/${m}_eval_scores_${s}.json"
    peritem="results/${m}_eval_peritem_${s}.json"
    args="--subset subsets/${s}.txt"
  fi
  if [ -f "$peritem" ]; then echo "[skip] $m/$s exists"; return 0; fi
  echo "=== $m / $s ==="
  wsl.exe --cd "$REPO_WIN" -- bash -c ".venv-wsl/bin/python -m src.metrics.score --predictions results/${m}_eval.json --out ${out} --per-item ${peritem} ${args} 2>&1 | tail -2" </dev/null
  local rc=$?
  if [ $rc -ne 0 ]; then
    echo "[FAIL rc=$rc] $m/$s — restarting WSL and retrying once"
    wsl.exe --shutdown </dev/null; sleep 10
    wsl.exe --cd "$REPO_WIN" -- bash -c ".venv-wsl/bin/python -m src.metrics.score --predictions results/${m}_eval.json --out ${out} --per-item ${peritem} ${args} 2>&1 | tail -2" </dev/null \
      || echo "[FAIL-2] $m/$s gave up"
  fi
}

for m in qwen_omni enclap cnn14 ast; do run_score "$m" full; done
for m in af3 salmonn qwen_omni enclap cnn14 ast; do
  for s in poly mono; do run_score "$m" "$s"; done
done
echo ALL_ISOLATED_RUNS_DONE
