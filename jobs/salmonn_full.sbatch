#!/bin/bash -l
# Full 1045-clip SALMONN-13B run on TinyGPU. Submit with:
#   sbatch.tinygpu jobs/salmonn_full.sbatch
#SBATCH --job-name=salmonn-full
#SBATCH --partition=a100
#SBATCH --gres=gpu:a100:1
#SBATCH --time=12:00:00
#SBATCH --output=salmonn_full.%j.out

cd "$WORK/audio-to-text-captioning-using-LALMs"
module load python/3.12-conda cuda/11.8.0
eval "$(conda shell.bash hook)"
conda activate "$WORK/envs/salmonn"

# SALMONN's Q-Former reads bert-base-uncased's config from the HF cache; point
# HF_HOME at the pre-populated cache on $WORK (bert staged on the frontend).
export HF_HOME="$WORK/hf_cache"
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1

nvidia-smi
python -m src.pipeline.run_inference \
    --config configs/salmonn.yaml \
    --out results/salmonn_eval.json
