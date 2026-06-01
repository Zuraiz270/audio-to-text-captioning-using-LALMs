"""Download CNN14 + DCASE-2023 BART captioning weights from Zenodo.

Two records, both required:
  - 10.5281/zenodo.7752975 -> audio_encoder.pth  (~321 MB)  -> weights/cnn14_audio_encoder.pth
  - 10.5281/zenodo.7688773 -> dcase_baseline_pre_trained.bin (~715 MB, MD5 8a083c24...)

Idempotent: skips download if the target exists and (when a hash is known) matches.
Stdlib-only so it can run before requirements.txt is installed.
"""
from __future__ import annotations

import hashlib
import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WEIGHTS_DIR = REPO_ROOT / "weights"


@dataclass(frozen=True)
class WeightAsset:
    url: str
    dest: Path
    md5: str | None  # None when upstream Zenodo record does not publish a hash for this file


ASSETS: tuple[WeightAsset, ...] = (
    WeightAsset(
        url="https://zenodo.org/record/7752975/files/audio_encoder.pth?download=1",
        dest=WEIGHTS_DIR / "cnn14_audio_encoder.pth",
        md5=None,
    ),
    WeightAsset(
        url="https://zenodo.org/record/7688773/files/dcase_baseline_pre_trained.bin?download=1",
        dest=WEIGHTS_DIR / "dcase_baseline_pre_trained.bin",
        md5="8a083c24dbe9dd16a6a13faf3514f5ed",
    ),
)


def md5_of(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def download(asset: WeightAsset) -> None:
    asset.dest.parent.mkdir(parents=True, exist_ok=True)

    if asset.dest.exists():
        if asset.md5 is None:
            print(f"[skip] {asset.dest.name} exists (no published MD5 to verify)")
            return
        actual = md5_of(asset.dest)
        if actual == asset.md5:
            print(f"[skip] {asset.dest.name} exists, MD5 ok")
            return
        print(f"[redo] {asset.dest.name} MD5 mismatch (got {actual}, want {asset.md5}); redownloading")
        asset.dest.unlink()

    print(f"[get ] {asset.url}")
    tmp = asset.dest.with_suffix(asset.dest.suffix + ".part")

    req = urllib.request.Request(asset.url, headers={"User-Agent": "chprojm-cnn14-baseline/1.0"})
    with urllib.request.urlopen(req) as resp, tmp.open("wb") as out:
        total = int(resp.headers.get("Content-Length") or 0)
        read = 0
        chunk = 1 << 20
        while True:
            buf = resp.read(chunk)
            if not buf:
                break
            out.write(buf)
            read += len(buf)
            if total:
                pct = 100.0 * read / total
                sys.stdout.write(f"\r       {read / 1e6:8.1f} MB / {total / 1e6:.1f} MB  ({pct:5.1f}%)")
            else:
                sys.stdout.write(f"\r       {read / 1e6:8.1f} MB")
            sys.stdout.flush()
    sys.stdout.write("\n")

    if asset.md5 is not None:
        actual = md5_of(tmp)
        if actual != asset.md5:
            tmp.unlink()
            raise SystemExit(f"MD5 mismatch for {asset.dest.name}: got {actual}, want {asset.md5}")
        print(f"       MD5 ok ({actual})")
    tmp.replace(asset.dest)
    print(f"[done] {asset.dest.relative_to(REPO_ROOT)}  ({asset.dest.stat().st_size / 1e6:.1f} MB)")


def main() -> int:
    for asset in ASSETS:
        download(asset)
    print("\nAll weights present in", WEIGHTS_DIR)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
