"""Run a Captioner over a Clotho split and write predictions JSON.

Usage:
  python -m src.pipeline.run_inference \
      --config configs/cnn14.yaml \
      --out results/cnn14_eval.json \
      [--limit 5] [--num-beams 1]

Output schema matches what src/metrics/score.py expects:
  {model, split, decode, audio, items: [{file_name, prediction, references}, ...]}

Sibling manifest (cnn14_eval.manifest.json) carries weight SHA256s, library
versions, vendored-repo commit SHA, the seed, and decode/audio params.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import random
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import torch
from omegaconf import OmegaConf
from tqdm import tqdm

from src.data.clotho import ClothoEvalDataset
from src.models import MODEL_REGISTRY


def _sha256(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def _vendored_commit_sha(repo_root: Path, submodule_rel: str) -> str | None:
    try:
        out = subprocess.check_output(
            ["git", "submodule", "status", "--", submodule_rel],
            cwd=repo_root,
            text=True,
            stderr=subprocess.DEVNULL,
        )
        return out.strip().split()[0].lstrip("-+")
    except Exception:
        return None


def _atomic_write_json(path: Path, payload: dict) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.parent.mkdir(parents=True, exist_ok=True)
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def _set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--limit", type=int, default=None,
                        help="Only caption the first N clips (smoke test).")
    parser.add_argument("--num-beams", type=int, default=None,
                        help="Override config.model.init.num_beams at runtime.")
    args = parser.parse_args()

    cfg = OmegaConf.load(args.config)
    if args.num_beams is not None:
        cfg.model.init.num_beams = args.num_beams

    repo_root = Path(__file__).resolve().parents[2]
    args.out = args.out.resolve() if args.out.is_absolute() else (repo_root / args.out).resolve()
    _set_seed(int(cfg.seed))

    print(f"[cfg] {OmegaConf.to_yaml(cfg)}", file=sys.stderr)

    dataset = ClothoEvalDataset(repo_root / cfg.data.root, split=cfg.data.split)
    n_total = len(dataset)
    n_run = n_total if args.limit is None else min(args.limit, n_total)
    print(f"[data] {cfg.data.split}: {n_run} / {n_total} clips", file=sys.stderr)

    model_cls = MODEL_REGISTRY[cfg.model.name]
    init_kwargs = {k: (str(repo_root / v) if k.endswith("_ckpt") else v)
                   for k, v in OmegaConf.to_container(cfg.model.init, resolve=True).items()}
    print(f"[model] building {cfg.model.name} ...", file=sys.stderr)
    t0 = time.time()
    captioner = model_cls(**init_kwargs)
    print(f"[model] built in {time.time() - t0:.1f}s", file=sys.stderr)

    items: list[dict] = []
    failures: list[dict] = []
    t_run = time.time()

    decode_params = {
        "strategy": "beam" if cfg.model.init.num_beams > 1 else "greedy",
        "num_beams": int(cfg.model.init.num_beams),
        "max_length": int(cfg.model.init.max_length),
        "min_length": 5,
        "length_penalty": 1.0,
        "no_repeat_ngram_size": 3,
        "early_stopping": True,
    }
    audio_params = OmegaConf.to_container(cfg.audio, resolve=True)

    payload_skeleton = {
        "model": cfg.model.name,
        "split": cfg.data.split,
        "decode": decode_params,
        "audio": audio_params,
        "items": items,
    }

    for idx in tqdm(range(n_run), file=sys.stderr, dynamic_ncols=True):
        clip = dataset[idx]
        try:
            caption = captioner.caption(clip["waveform"], clip["sample_rate"])
            items.append({
                "file_name": clip["file_name"],
                "prediction": caption,
                "references": clip["references"],
            })
        except Exception as e:
            failures.append({"file_name": clip["file_name"], "error": repr(e)})
            print(f"[err] {clip['file_name']}: {e!r}", file=sys.stderr)
            continue

        if (idx + 1) % 10 == 0 or idx + 1 == n_run:
            _atomic_write_json(args.out, payload_skeleton)

    _atomic_write_json(args.out, payload_skeleton)
    elapsed = time.time() - t_run
    print(f"[done] {len(items)} items, {len(failures)} failures, {elapsed:.0f}s", file=sys.stderr)

    encoder_ckpt = Path(init_kwargs["encoder_ckpt"])
    decoder_ckpt = Path(init_kwargs["decoder_ckpt"])
    manifest_path = args.out.with_suffix(".manifest.json")
    manifest = {
        "model": cfg.model.name,
        "split": cfg.data.split,
        "n_items": len(items),
        "n_failures": len(failures),
        "elapsed_sec": round(elapsed, 1),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "seed": int(cfg.seed),
        "decode": decode_params,
        "audio": audio_params,
        "weights": {
            "encoder": {
                "path": str(encoder_ckpt.relative_to(repo_root)),
                "sha256": _sha256(encoder_ckpt),
                "size_bytes": encoder_ckpt.stat().st_size,
            },
            "decoder": {
                "path": str(decoder_ckpt.relative_to(repo_root)),
                "sha256": _sha256(decoder_ckpt),
                "size_bytes": decoder_ckpt.stat().st_size,
            },
        },
        "vendored": {
            "path": "src/models/_vendor",
            "commit_sha": _vendored_commit_sha(repo_root, "src/models/_vendor"),
        },
        "versions": {
            "python": platform.python_version(),
            "torch": torch.__version__,
            "torchaudio": __import__("torchaudio").__version__,
            "transformers": __import__("transformers").__version__,
            "librosa": __import__("librosa").__version__,
            "numpy": np.__version__,
        },
        "failures": failures,
    }
    _atomic_write_json(manifest_path, manifest)
    print(f"[manifest] {manifest_path.relative_to(repo_root)}", file=sys.stderr)

    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
