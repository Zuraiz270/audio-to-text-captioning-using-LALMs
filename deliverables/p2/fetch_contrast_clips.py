"""Stream a handful of AudioCaps + WavCaps clips from HuggingFace for the
slide-2 cross-corpus contrast strip.

We do NOT clone the full datasets — only ~3 clips per corpus matching a
configurable caption keyword. Saved as 16-bit mono WAV at 22050 Hz so the
file sizes stay tiny (~1 MB each).

Usage:
    python deliverables/p2/fetch_contrast_clips.py --keyword rain
    python deliverables/p2/fetch_contrast_clips.py --keyword dog --n 2

Notes on HuggingFace access:
    Most public mirrors work without login. If any subset asks for auth, run
        huggingface-cli login
    once and provide your HF token. WavCaps subsets occasionally require
    accepting terms on the dataset's HF page first.
"""

from __future__ import annotations

import argparse
import io
from pathlib import Path

import numpy as np
import soundfile as sf

try:
    from datasets import load_dataset
except ImportError as e:  # pragma: no cover
    raise SystemExit(
        "`datasets` not installed. Run:\n"
        "    pip install -r deliverables/p2/requirements.txt"
    ) from e

PROJECT_ROOT = Path(__file__).resolve().parents[2]
AUDIOCAPS_DIR = PROJECT_ROOT / "data" / "audiocaps"
WAVCAPS_DIR = PROJECT_ROOT / "data" / "wavcaps"
AUDIOCAPS_DIR.mkdir(parents=True, exist_ok=True)
WAVCAPS_DIR.mkdir(parents=True, exist_ok=True)

TARGET_SR = 22050  # tiny files; we only need them for visual rendering


# Candidate HF dataset IDs (tried in order — first one that works wins).
AUDIOCAPS_CANDIDATES = [
    ("confit/audiocaps", "test", None),
    ("d0rj/audiocaps", "test", None),
    ("OpenSound/audiocaps-eval", "test", None),
]
WAVCAPS_CANDIDATES = [
    # cvssp/WavCaps has 4 subsets; FreeSound is the most diverse for sound events
    ("cvssp/WavCaps", "train", "FreeSound"),
    ("cvssp/WavCaps", "train", "BBC_Sound_Effects"),
    ("cvssp/WavCaps", "train", "SoundBible"),
]


def _to_wav_bytes(audio_array: np.ndarray, sr: int) -> bytes:
    """Resample/convert audio array → WAV bytes at TARGET_SR mono 16-bit."""
    if audio_array.ndim == 2:
        audio_array = audio_array.mean(axis=1)
    if sr != TARGET_SR:
        # avoid librosa dep for resample — simple linear interpolation
        old_n = len(audio_array)
        new_n = int(round(old_n * TARGET_SR / sr))
        audio_array = np.interp(
            np.linspace(0, old_n, new_n, endpoint=False),
            np.arange(old_n),
            audio_array,
        )
    audio_array = np.clip(audio_array, -1.0, 1.0)
    buf = io.BytesIO()
    sf.write(buf, audio_array, TARGET_SR, format="WAV", subtype="PCM_16")
    return buf.getvalue()


def _try_stream(ds_id: str, split: str, subset: str | None):
    print(f"  trying {ds_id} (split={split}, subset={subset})...")
    kwargs = {"streaming": True}
    if subset:
        kwargs["name"] = subset
    try:
        return load_dataset(ds_id, split=split, **kwargs)
    except Exception as e:  # broad on purpose; mirrors fail in many ways
        print(f"    failed: {type(e).__name__}: {str(e)[:120]}")
        return None


def _caption_of(row: dict) -> str:
    """Extract the most likely caption field across HF dataset schemas."""
    for k in ("caption", "captions", "text", "title", "description", "label"):
        if k in row and row[k]:
            v = row[k]
            return v[0] if isinstance(v, list) else str(v)
    return ""


def fetch(corpus: str, candidates: list, keyword: str, n: int,
          out_dir: Path) -> int:
    print(f"\n[{corpus}] looking for {n} clips matching keyword '{keyword}'")
    saved = 0
    for ds_id, split, subset in candidates:
        if saved >= n:
            break
        ds = _try_stream(ds_id, split, subset)
        if ds is None:
            continue
        print(f"  scanning stream for '{keyword}'...")
        scanned = 0
        for row in ds:
            scanned += 1
            if scanned % 200 == 0:
                print(f"    {scanned} rows scanned, {saved}/{n} saved")
            caption = _caption_of(row).lower()
            if keyword.lower() not in caption:
                continue
            # find the audio field
            audio_field = None
            for k in ("audio", "wav", "mp3"):
                if k in row and row[k]:
                    audio_field = row[k]
                    break
            if audio_field is None:
                continue
            try:
                arr = np.asarray(audio_field["array"], dtype=np.float32)
                sr = int(audio_field["sampling_rate"])
            except (KeyError, TypeError):
                continue
            tag = (corpus[:3] + "_" + keyword + "_" + str(saved + 1)).lower()
            out_wav = out_dir / f"{tag}.wav"
            out_wav.write_bytes(_to_wav_bytes(arr, sr))
            cap_path = out_dir / f"{tag}.caption.txt"
            cap_path.write_text(caption.strip(), encoding="utf-8")
            print(f"    saved {out_wav.name} ({len(arr) / sr:.1f}s) — “{caption[:80]}”")
            saved += 1
            if saved >= n:
                break
            if scanned > 5000:
                print(f"    scanned 5000 rows, only {saved} matched — moving on")
                break
        if saved >= n:
            break
    print(f"[{corpus}] done: {saved}/{n} clips saved to {out_dir.relative_to(PROJECT_ROOT)}")
    return saved


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--keyword", default="rain",
                        help="Caption keyword to filter by (default: rain)")
    parser.add_argument("--n", type=int, default=1,
                        help="How many clips per corpus (default: 1)")
    args = parser.parse_args()

    print(f"Hugging Face streaming fetch — keyword='{args.keyword}', n={args.n}")
    print("AudioCaps and WavCaps subsets will be tried in order until one works.")

    ac = fetch("AudioCaps", AUDIOCAPS_CANDIDATES, args.keyword, args.n,
               AUDIOCAPS_DIR)
    wc = fetch("WavCaps", WAVCAPS_CANDIDATES, args.keyword, args.n,
               WAVCAPS_DIR)

    print("\nsummary:")
    print(f"  AudioCaps: {ac} clip(s) at data/audiocaps/")
    print(f"  WavCaps:   {wc} clip(s) at data/wavcaps/")
    if ac == 0 or wc == 0:
        print(
            "\nIf any corpus returned 0 clips:\n"
            "  - try a more common keyword: dog, water, music, voice\n"
            "  - try `huggingface-cli login` first (some subsets are gated)\n"
            "  - or visit the HF dataset page in a browser and accept terms"
        )


if __name__ == "__main__":
    main()
