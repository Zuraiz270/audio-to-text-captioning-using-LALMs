# Colab — LALM runs

The LALMs need a GPU, so they run on Google Colab (not the local Windows/WSL setup).
Each notebook produces the **same predictions-JSON schema** the local pipeline uses,
so the output drops straight into `src/metrics/score.py` for an apples-to-apples
comparison with the CNN14 / EnCLAP / AST baselines.

## `qwen2_5_omni_smoke.ipynb` — first de-risk run

A self-contained 5-clip smoke test for **Qwen2.5-Omni**. It:
- detects the Colab GPU and **auto-picks 3B vs 7B** by VRAM (7B needs ≥ ~38 GB;
  otherwise 3B), bf16, talker disabled (text-only);
- captions 5 Clotho-eval clips with a fixed prompt ("Describe the audio in one
  sentence."), greedy decode;
- writes `qwen_smoke.json` to Drive in the project schema.

**One-time setup:** upload the Clotho eval audio folder +
`clotho_captions_evaluation.csv` (~2 GB) to your Drive, then set `DRIVE_CLOTHO`
in the notebook's *Paths* cell.

**Run:** open in Colab (Runtime = GPU), run top to bottom, and **restart the
runtime once after the install cell** (Colab pins an old transformers).

**Report back:** the printed GPU/VRAM line + the 5 captions. That tells us which
model size fits and whether the captions look right — then we wire the full
1045-clip run + scoring (either in Colab or by pulling the JSON back to WSL).

## VRAM cheat-sheet (bf16, audio-only, inference)

| Model | ~VRAM (30 s clip) | Fits free T4 (16 GB)? |
|:--|:--|:--|
| Qwen2.5-Omni-3B | ~18–22 GB | no (needs L4/A100 ~24 GB) |
| Qwen2.5-Omni-7B | ~31 GB+ | no (needs A100) |

If even 3B over-runs the GPU, the fallback is 4-bit (`bitsandbytes`) — but note
that as a comparability caveat in the term paper (quantized ≠ full precision).
