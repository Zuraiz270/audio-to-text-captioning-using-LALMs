"""Pull a small representative sample (~6 clips) from AudioCaps and WavCaps.

These clips back the slide-2 dataset-rejection narrative: "this is what each
corpus actually looks like, and here is why we did not pick it".

AudioCaps clips are pulled via yt-dlp from YouTube using audiocap-id metadata
(streamed from d0rj/audiocaps on HuggingFace). WavCaps clips are pulled from
the SoundBible subset (smallest WavCaps source) using its direct download
URLs in the cached cvssp/WavCaps JSON.

Run from project root:
    python deliverables/p2/fetch_dataset_samples.py

Total disk: ~10-20 MB. Writes into data/audiocaps/ and data/wavcaps/ with a
sidecar .caption.txt next to each .wav.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import urllib.request
from pathlib import Path

try:
    from datasets import load_dataset
    from huggingface_hub import hf_hub_download
except ImportError as e:  # pragma: no cover
    raise SystemExit(
        "Install dependencies first:\n"
        "    pip install -r deliverables/p2/requirements.txt"
    ) from e

PROJECT_ROOT = Path(__file__).resolve().parents[2]
AUDIOCAPS_DIR = PROJECT_ROOT / "data" / "audiocaps"
WAVCAPS_DIR = PROJECT_ROOT / "data" / "wavcaps"
AUDIOCAPS_DIR.mkdir(parents=True, exist_ok=True)
WAVCAPS_DIR.mkdir(parents=True, exist_ok=True)

# Each bucket = one representative clip from each corpus, spanning categories
# Bucket name -> set of keywords (any match in the caption qualifies)
BUCKETS = {
    "rain":    {"rain"},
    "dog":     {"dog", "dogs"},
    "music":   {"music", "musical", "song"},
    "vehicle": {"car", "engine", "motor", "truck", "vehicle"},
    "voice":   {"speaking", "talking", "voice", "voices", "speaks"},
    "water":   {"water", "stream", "river", "wave", "waves"},
}


def _slug(s: str) -> str:
    return "".join(c if c.isalnum() else "_" for c in s).strip("_").lower()


# ---------------------------------------------------------------------------
# AudioCaps  --  via yt-dlp + ffmpeg, segment cut to start_time .. start_time+10
# ---------------------------------------------------------------------------

def _audiocaps_pick_one_per_bucket() -> dict[str, dict]:
    """Stream metadata until we have one clip per bucket."""
    print("scanning d0rj/audiocaps for one clip per bucket ...")
    ds = load_dataset("d0rj/audiocaps", split="test", streaming=True)
    picks: dict[str, dict] = {}
    for row in ds:
        cap = row["caption"].lower()
        cap_words = set(cap.split())
        for bucket, keywords in BUCKETS.items():
            if bucket in picks:
                continue
            if cap_words & keywords:
                picks[bucket] = row
                print(f"  {bucket:8s} -> yt={row['youtube_id']} t={row['start_time']} "
                      f"\"{row['caption']}\"")
                break
        if len(picks) == len(BUCKETS):
            break
    missing = set(BUCKETS) - set(picks)
    if missing:
        print(f"  (no AudioCaps match for: {sorted(missing)})")
    return picks


def _ytdlp_one(youtube_id: str, start: int, out_wav: Path) -> bool:
    """Use yt-dlp to grab a 10-second clip via download-sections."""
    url = f"https://www.youtube.com/watch?v={youtube_id}"
    end = start + 10
    out_template = str(out_wav.with_suffix(".%(ext)s"))
    cmd = [
        "yt-dlp", "-x", "--audio-format", "wav",
        "--download-sections", f"*{start}-{end}",
        url, "-o", out_template,
        "--no-warnings", "--quiet",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        print(f"    timeout: {youtube_id}")
        return False
    if result.returncode != 0:
        msg = (result.stderr or result.stdout or "").strip().splitlines()[-1:]
        print(f"    failed: {youtube_id} :: {msg[0] if msg else 'unknown'}")
        return False
    return out_wav.exists()


def fetch_audiocaps_samples() -> int:
    picks = _audiocaps_pick_one_per_bucket()
    saved = 0
    for bucket, row in picks.items():
        out = AUDIOCAPS_DIR / f"audiocaps_{bucket}_1.wav"
        if out.exists():
            print(f"  {bucket}: already have {out.name}, skipping")
            saved += 1
            continue
        print(f"  fetching AudioCaps `{bucket}` (yt={row['youtube_id']})...")
        if _ytdlp_one(row["youtube_id"], int(row["start_time"]), out):
            cap = AUDIOCAPS_DIR / f"audiocaps_{bucket}_1.caption.txt"
            cap.write_text(row["caption"].strip(), encoding="utf-8")
            print(f"    wrote {out.name}")
            saved += 1
    return saved


# ---------------------------------------------------------------------------
# WavCaps SoundBible  --  via direct download_link in cached HF JSON
# ---------------------------------------------------------------------------

def fetch_wavcaps_samples() -> int:
    json_fp = hf_hub_download(
        "cvssp/WavCaps",
        "json_files/SoundBible/sb_final.json",
        repo_type="dataset",
    )
    with open(json_fp, encoding="utf-8") as f:
        data = json.load(f)["data"]
    print(f"WavCaps/SoundBible: {len(data)} clips in JSON, picking one per bucket ...")
    picks: dict[str, dict] = {}
    for entry in data:
        cap_words = set(entry["caption"].lower().split())
        for bucket, keywords in BUCKETS.items():
            if bucket in picks:
                continue
            # require duration between 5 and 25 seconds for tight files
            if not 5 <= entry["duration"] <= 25:
                continue
            if cap_words & keywords:
                picks[bucket] = entry
                print(f"  {bucket:8s} -> id={entry['id']} dur={entry['duration']:.1f}s "
                      f"\"{entry['caption']}\"")
                break
        if len(picks) == len(BUCKETS):
            break
    missing = set(BUCKETS) - set(picks)
    if missing:
        # relax duration constraint for misses
        for entry in data:
            if not missing:
                break
            cap_words = set(entry["caption"].lower().split())
            for bucket in list(missing):
                keywords = BUCKETS[bucket]
                if cap_words & keywords:
                    picks[bucket] = entry
                    missing.remove(bucket)
                    print(f"  {bucket:8s} -> id={entry['id']} dur={entry['duration']:.1f}s "
                          f"(relaxed)  \"{entry['caption']}\"")
                    break

    saved = 0
    for bucket, entry in picks.items():
        out = WAVCAPS_DIR / f"wavcaps_{bucket}_1.wav"
        if out.exists():
            print(f"  {bucket}: already have {out.name}, skipping")
            saved += 1
            continue
        print(f"  fetching WavCaps `{bucket}` (id={entry['id']})...")
        req = urllib.request.Request(
            entry["download_link"],
            headers={"User-Agent": "Mozilla/5.0"},
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                payload = r.read()
        except Exception as e:
            print(f"    failed: {type(e).__name__}: {e}")
            continue
        out.write_bytes(payload)
        cap_path = WAVCAPS_DIR / f"wavcaps_{bucket}_1.caption.txt"
        cap_path.write_text(entry["caption"], encoding="utf-8")
        print(f"    wrote {out.name} ({out.stat().st_size / 1024:.1f} KB)")
        saved += 1
    return saved


def main() -> None:
    n_ac = fetch_audiocaps_samples()
    n_wc = fetch_wavcaps_samples()
    print(f"\nsummary: {n_ac} AudioCaps clip(s), {n_wc} WavCaps clip(s)")
    print(f"  -> data/audiocaps/")
    print(f"  -> data/wavcaps/")


if __name__ == "__main__":
    main()
