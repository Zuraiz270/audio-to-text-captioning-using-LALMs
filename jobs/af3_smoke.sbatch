#!/bin/bash -l
# 5-clip smoke test for Audio Flamingo 3 on TinyGPU. Submit with:
#   sbatch.tinygpu jobs/af3_smoke.sbatch
#SBATCH --job-name=af3-smoke
#SBATCH --partition=a100
#SBATCH --gres=gpu:a100:1
#SBATCH --time=01:00:00
#SBATCH --output=af3_smoke.%j.out

cd "$WORK/audio-to-text-captioning-using-LALMs"
module load python/pytorch2.6py3.12
# AF3 is transformers-native; it reuses the Qwen row's transformers 5.x env.
source "$WORK/envs/qwen/bin/activate"

export HF_HOME="$WORK/hf_cache"
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1

nvidia-smi
python -m src.pipeline.run_inference \
    --config configs/af3.yaml \
    --out results/af3_smoke.json \
    --limit 5
