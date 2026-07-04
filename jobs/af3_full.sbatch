#!/bin/bash -l
# Full 1045-clip Audio Flamingo 3 run on TinyGPU. Submit with:
#   sbatch.tinygpu jobs/af3_full.sbatch
#SBATCH --job-name=af3-full
#SBATCH --partition=a100
#SBATCH --gres=gpu:a100:1
#SBATCH --time=06:00:00
#SBATCH --output=af3_full.%j.out

cd "$WORK/audio-to-text-captioning-using-LALMs"
module load python/pytorch2.6py3.12
source "$WORK/envs/qwen/bin/activate"

export HF_HOME="$WORK/hf_cache"
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1

nvidia-smi
python -m src.pipeline.run_inference \
    --config configs/af3.yaml \
    --out results/af3_eval.json
