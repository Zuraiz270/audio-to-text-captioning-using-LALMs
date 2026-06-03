"""Download the EnCLAP checkpoint from Google Drive via gdown.

The CLAP checkpoint (630k-audioset-fusion-best.pt) is handled by
download_weights.py; this script only fetches the EnCLAP model checkpoint
(config.json + pytorch_model.bin), which lives on Google Drive.

The published Drive layout is {audiocaps,clotho,clotho_finetune,both}/{base,large};
we want clotho_finetune/base. The repo README only links the top-level folder,
so pass the clotho_finetune/base *subfolder* link with --url to fetch ~1 GB
instead of the whole ~8 GB tree. With no --url, it downloads the whole tree.

    python scripts/download_weights_enclap.py \
        --url "https://drive.google.com/drive/folders/<clotho_finetune-base-id>" \
        --out weights/enclap_base_clotho_finetune
"""
from __future__ import annotations

import argparse
from pathlib import Path

import gdown

REPO_ROOT = Path(__file__).resolve().parent.parent
WEIGHTS_DIR = REPO_ROOT / "weights"

# Top-level pretrained-checkpoints folder (all datasets x base/large, ~8 GB).
FULL_FOLDER_URL = "https://drive.google.com/drive/folders/1JOcKyNOlKud0PY93ETGDlUJnWhmSC35m"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url", default=FULL_FOLDER_URL,
        help="Drive folder URL. Pass the clotho_finetune/base subfolder to "
             "avoid downloading the whole tree.",
    )
    parser.add_argument(
        "--out", type=Path, default=WEIGHTS_DIR / "enclap_base_clotho_finetune",
        help="Local output directory for the checkpoint.",
    )
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    print(f"[gdown] {args.url}\n        -> {args.out}")
    gdown.download_folder(
        url=args.url,
        output=str(args.out),
        quiet=False,
        use_cookies=False,
    )

    bins = list(args.out.rglob("pytorch_model.bin"))
    cfgs = list(args.out.rglob("config.json"))
    print(f"[done] found {len(bins)} pytorch_model.bin, {len(cfgs)} config.json under {args.out}")
    if not bins or not cfgs:
        print("[warn] expected config.json + pytorch_model.bin — point the wrapper "
              "at the directory that contains BOTH.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
