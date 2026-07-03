#!/bin/bash -l
# 5-clip smoke test for Qwen2.5-Omni on TinyGPU. Submit with:
#   sbatch.tinygpu jobs/qwen_smoke.sbatch
#SBATCH --job-name=qwen-smoke
#SBATCH --partition=a100
#SBATCH --gres=gpu:a100:1
#SBATCH --time=01:00:00
#SBATCH --output=qwen_smoke.%j.out

cd "$WORK/audio-to-text-captioning-using-LALMs"
module load python/pytorch2.6py3.12
source "$WORK/envs/qwen/bin/activate"

# Keep the HF model cache on $WORK (not the small $HOME quota) and run offline
# from the model pre-downloaded on the frontend (compute nodes have no internet).
export HF_HOME="$WORK/hf_cache"
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1

nvidia-smi
python -m src.pipeline.run_inference \
    --config configs/qwen_omni.yaml \
    --out results/qwen_smoke.json \
    --limit 5
