"""Framewise SED summary over Clotho-eval (RQ2 polyphony pipeline, expensive step).

Runs PANNs Cnn14_DecisionLevelMax (framewise sound-event detection, 32 kHz,
~100 fps interpolated output, verified empirically) over every eval clip and
stores, per clip and per threshold tau, which AudioSet classes are active and
for how long two classes are *simultaneously* active. The cheap, re-runnable
poly/mono split lives in polyphony_manifest.py and reads this file.

Raw framewise probabilities are NOT stored (1045 clips x ~2900 frames x 527
classes would be multi-GB); only the per-tau activation summary is kept.

Usage (in .venv):
  python -m src.analysis.sed_summary \
      --out results/sed_framewise_summary.json [--limit 5]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from itertools import combinations
from pathlib import Path

import librosa
import numpy as np
import pandas as pd

TAU_GRID = (0.20, 0.25, 0.30, 0.50)
SED_SR = 32_000  # Cnn14_DecisionLevelMax operates at 32 kHz


def _longest_run(mask: np.ndarray) -> int:
    """Length (frames) of the longest consecutive True run."""
    if not mask.any():
        return 0
    padded = np.concatenate(([False], mask, [False]))
    edges = np.flatnonzero(padded[1:] != padded[:-1])
    return int((edges[1::2] - edges[0::2]).max())


def _atomic_write_json(path: Path, payload: dict) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.parent.mkdir(parents=True, exist_ok=True)
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)
    os.replace(tmp, path)


def summarize_clip(probs: np.ndarray, fps: float, labels: list[str]) -> dict:
    """Per-tau activation summary for one clip's framewise probs (T, 527)."""
    per_tau: dict[str, dict] = {}
    for tau in TAU_GRID:
        active = probs >= tau  # (T, C)
        cols = np.flatnonzero(active.any(axis=0))
        active_labels = [
            {
                "label": labels[c],
                "max_prob": round(float(probs[:, c].max()), 4),
                "longest_run_s": round(_longest_run(active[:, c]) / fps, 3),
            }
            for c in cols
        ]
        # Longest run where the SAME two classes are co-active — the faithful
        # reading of "≥2 simultaneous classes active ≥1 s". A per-frame count
        # would let the class identity churn mid-window.
        best_overlap, best_pair = 0.0, None
        for c1, c2 in combinations(cols, 2):
            run_s = _longest_run(active[:, c1] & active[:, c2]) / fps
            if run_s > best_overlap:
                best_overlap, best_pair = run_s, (labels[c1], labels[c2])
        per_tau[f"{tau:.2f}"] = {
            "n_active_classes": len(cols),
            "active_labels": active_labels,
            "max_pairwise_overlap_s": round(best_overlap, 3),
            "best_pair": list(best_pair) if best_pair else None,
        }
    return per_tau


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("results/sed_framewise_summary.json"))
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    from panns_inference import SoundEventDetection, labels

    repo = Path(__file__).resolve().parents[2]
    csv = repo / "data/clotho_v2.1/clotho_captions_evaluation.csv"
    audio_dir = repo / "data/clotho_v2.1/clotho_audio_evaluation/evaluation"
    file_names = pd.read_csv(csv)["file_name"].tolist()
    if args.limit:
        file_names = file_names[: args.limit]
    out_path = args.out if args.out.is_absolute() else repo / args.out

    sed = SoundEventDetection(checkpoint_path=None, device="cpu")

    clips: list[dict] = []
    payload = {
        "checkpoint": "Cnn14_DecisionLevelMax_mAP=0.385 (zenodo 3987831)",
        "sample_rate": SED_SR,
        "tau_grid": list(TAU_GRID),
        "clips": clips,
    }
    t0 = time.time()
    for i, fn in enumerate(file_names):
        audio, _ = librosa.load(audio_dir / fn, sr=SED_SR, mono=True)
        duration = len(audio) / SED_SR
        probs = np.asarray(sed.inference(audio[None, :]))[0]  # (T, 527)
        fps = probs.shape[0] / duration
        clips.append({
            "file_name": fn,
            "duration_s": round(duration, 3),
            "n_frames": int(probs.shape[0]),
            "fps": round(fps, 2),
            "per_tau": summarize_clip(probs, fps, labels),
        })
        if (i + 1) % 25 == 0 or i + 1 == len(file_names):
            _atomic_write_json(out_path, payload)
            rate = (i + 1) / (time.time() - t0)
            print(f"[{i+1}/{len(file_names)}] {rate:.2f} clips/s", file=sys.stderr)

    _atomic_write_json(out_path, payload)
    print(f"[done] {len(clips)} clips -> {out_path} ({time.time()-t0:.0f}s)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
