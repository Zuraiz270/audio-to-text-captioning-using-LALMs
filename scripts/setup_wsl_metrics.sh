#!/usr/bin/env bash
# Set up the WSL-side metrics environment.
#
# Run from inside WSL Ubuntu, project root:
#   cd /mnt/e/ISSS/Summer\ 2026/CH-Proj-M\ Master\'s\ project\ Computational\ Humanities
#   bash scripts/setup_wsl_metrics.sh

set -euo pipefail

echo "=== apt: OpenJDK 11 + Python 3.12 venv (Ubuntu 24.04 default) ==="
sudo apt update
sudo apt install -y openjdk-11-jre-headless python3-venv python3-pip

echo "=== java version (expect 11.x) ==="
java -version

echo "=== creating .venv-wsl ==="
python3 -m venv .venv-wsl
# shellcheck disable=SC1091
source .venv-wsl/bin/activate
pip install --upgrade pip

echo "=== pip install requirements-wsl.txt ==="
pip install -r requirements-wsl.txt

echo "=== aac-metrics-download (METEOR + SPICE jars) ==="
aac-metrics-download

echo
echo "WSL metrics env ready. To score predictions:"
echo "  source .venv-wsl/bin/activate"
echo "  python -m src.metrics.score --predictions results/cnn14_eval.json --out results/cnn14_eval_scores.json"
