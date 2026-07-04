#!/bin/bash -l
# 5-clip smoke test for SALMONN-13B on TinyGPU. Submit with:
#   sbatch.tinygpu jobs/salmonn_smoke.sbatch
#SBATCH --job-name=salmonn-smoke
#SBATCH --partition=a100
#SBATCH --gres=gpu:a100:1
#SBATCH --time=01:00:00
#SBATCH --output=salmonn_smoke.%j.out

cd "$WORK/audio-to-text-captioning-using-LALMs"
module load python/3.12-conda cuda/11.8.0
eval "$(conda shell.bash hook)"
conda activate "$WORK/envs/salmonn"

# Weights are local dirs (paths resolve from $WORK in the config); force offline so
# transformers never reaches out from the internet-less compute node.
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1

nvidia-smi
python -m src.pipeline.run_inference \
    --config configs/salmonn.yaml \
    --out results/salmonn_smoke.json \
    --limit 5
