"""Render the supporting charts for the P2 deck.

Outputs all figures into deliverables/p2/figures/. Run from the project root:

    python deliverables/p2/figures.py

Requires the Clotho v2.1 metadata + caption CSVs in data/clotho_v2.1/.

Charts produced (slide -> filename):
  slide 1  -> clip_duration_hist.png       distribution of clip durations
  slide 1  -> caption_length_hist.png      distribution of caption lengths (words)
  slide 3  -> audio_properties_card.png    one-card infographic of audio properties
  slide 4  -> top20_class_bar.png          top-20 AudioSet classes (caption-keyword
                                           proxy until SED chart is produced by
                                           spectrogram_demo.py)
  slide 5  -> audit_diagram.png            three-layer contamination audit diagram
  slide 5  -> gantt_8week.png              8-week path-to-evaluation Gantt
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "clotho_v2.1"
OUT_DIR = Path(__file__).resolve().parent / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

PALETTE = {
    "navy": "#1f2a44",
    "accent": "#3a5fcd",
    "warn": "#c25a4f",
    "good": "#5a8f3d",
    "muted": "#9aa3b2",
}

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "axes.titleweight": "bold",
    "figure.dpi": 160,
})


def _save(fig: plt.Figure, name: str) -> Path:
    out = OUT_DIR / name
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"wrote {out.relative_to(PROJECT_ROOT)}")
    return out


def _load_captions() -> pd.DataFrame:
    """Load the Clotho dev caption CSV. Concatenates dev + val + eval if present."""
    parts = []
    for split in ("development", "validation", "evaluation"):
        path = DATA_DIR / f"clotho_captions_{split}.csv"
        if path.exists():
            df = pd.read_csv(path)
            df["split"] = split
            parts.append(df)
    if not parts:
        raise FileNotFoundError(
            f"No Clotho caption CSVs found under {DATA_DIR}. "
            "Step 0 download not yet complete."
        )
    return pd.concat(parts, ignore_index=True)


def _load_metadata() -> pd.DataFrame:
    parts = []
    for split in ("development", "validation", "evaluation"):
        path = DATA_DIR / f"clotho_metadata_{split}.csv"
        if path.exists():
            df = pd.read_csv(path, encoding="ISO-8859-1")
            df["split"] = split
            parts.append(df)
    if not parts:
        raise FileNotFoundError(
            f"No Clotho metadata CSVs found under {DATA_DIR}. "
            "Step 0 download not yet complete."
        )
    return pd.concat(parts, ignore_index=True)


def clip_duration_hist() -> None:
    """Slide 1 — Clotho clip duration histogram (15-30 s spec; verify empirically).

    Clotho metadata CSV does not include duration. Compute from start_end_samples
    field, assuming 44.1 kHz sample rate (per Drossos+ 2020 spec).
    """
    import ast
    meta = _load_metadata()
    if "start_end_samples" not in meta.columns:
        print("metadata missing start_end_samples; skipping clip_duration_hist")
        return
    SR = 44100
    durations = []
    for s in meta["start_end_samples"].dropna():
        try:
            arr = ast.literal_eval(s)  # "[start, end]"
            durations.append((arr[1] - arr[0]) / SR)
        except (ValueError, SyntaxError, IndexError):
            continue
    durations = pd.Series(durations)
    fig, ax = plt.subplots(figsize=(6, 3.2))
    ax.hist(durations, bins=30, color=PALETTE["accent"], edgecolor="white")
    ax.axvline(durations.mean(), color=PALETTE["warn"], linestyle="--",
               label=f"mean = {durations.mean():.1f} s")
    ax.set_xlabel("Clip duration (s)")
    ax.set_ylabel("Number of clips")
    ax.set_title("Clotho v2.1 — clip duration distribution")
    ax.legend(frameon=False)
    _save(fig, "clip_duration_hist.png")


def caption_length_hist() -> None:
    """Slide 1 / 3 — caption length in words (spec: 8-20)."""
    df = _load_captions()
    caption_cols = [c for c in df.columns if c.lower().startswith("caption")]
    lengths = []
    for col in caption_cols:
        lengths.extend(df[col].dropna().astype(str).str.split().str.len().tolist())
    fig, ax = plt.subplots(figsize=(6, 3.2))
    ax.hist(lengths, bins=range(min(lengths), max(lengths) + 2),
            color=PALETTE["accent"], edgecolor="white")
    ax.set_xlabel("Words per caption")
    ax.set_ylabel("Number of captions")
    ax.set_title(f"Clotho v2.1 — caption length distribution (n={len(lengths)})")
    _save(fig, "caption_length_hist.png")


def audio_properties_card() -> None:
    """Slide 3 — one-card infographic. Hard-coded from Drossos+ 2020 + Zenodo."""
    rows = [
        ("Sample rate", "44.1 kHz"),
        ("Channels", "1 (mono)"),
        ("Bit depth", "16-bit"),
        ("Format", "WAV (PCM)"),
        ("Clip duration", "15 – 30 s"),
        ("Captions per clip", "5"),
        ("Caption length", "8 – 20 words"),
        ("Vocabulary", "open (no fixed taxonomy)"),
        ("Licence", "CC-BY 4.0"),
        ("Distribution", "Zenodo record 4783391 — FAIR"),
    ]
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.axis("off")
    ax.set_title("Clotho v2.1 — audio properties at a glance",
                 loc="left", color=PALETTE["navy"], pad=14)
    for i, (k, v) in enumerate(rows):
        y = 0.92 - i * 0.085
        ax.text(0.03, y, k, fontsize=11, color=PALETTE["muted"],
                transform=ax.transAxes)
        ax.text(0.45, y, v, fontsize=11, color=PALETTE["navy"], weight="bold",
                transform=ax.transAxes)
    _save(fig, "audio_properties_card.png")


def top20_class_bar(use_caption_proxy: bool = True) -> None:
    """Slide 4 — top-20 AudioSet classes bar chart.

    Until spectrogram_demo.py runs PaSST/PANNs SED tagging, this uses a
    caption-keyword frequency proxy. Flagged as a limitation in the slide
    annotation. Replace by reading classes from the SED output CSV.
    """
    if use_caption_proxy:
        df = _load_captions()
        caption_cols = [c for c in df.columns if c.lower().startswith("caption")]
        words = []
        # tight content-word stop list -- enough for a top-20 chart
        stop = {
            "a", "an", "the", "is", "are", "was", "were", "be", "being", "been",
            "and", "or", "but", "as", "if", "of", "on", "in", "at", "to", "for",
            "with", "by", "from", "this", "that", "these", "those", "it", "its",
            "while", "when", "then", "there", "here", "very", "more", "some",
            "all", "no", "not", "one", "two", "three", "you", "he", "she", "they",
            "we", "i", "his", "her", "their", "our", "my", "your", "what", "which",
            "who", "whom", "out", "up", "down", "into", "over", "under", "before",
            "after", "between", "through", "off", "near", "far", "around", "back",
            "front", "side", "top", "bottom", "left", "right",
            "sounds", "sound", "noises", "noise", "noisy", "loud", "loudly",
            "softly", "quiet", "quietly", "distance", "background", "foreground",
            "begins", "begin", "stops", "stop", "continues", "continue", "moves",
            "move", "moving", "going", "going", "comes", "come", "coming", "goes",
            "go", "happens", "happen", "happening", "occurs", "occur", "occurring",
            "person", "people", "someone", "something", "anyone", "anything",
            "thing", "things", "lot", "lots", "many", "few",
        }
        for col in caption_cols:
            for cap in df[col].dropna().astype(str):
                for w in cap.lower().split():
                    w = "".join(ch for ch in w if ch.isalpha())
                    if w and w not in stop and len(w) > 2:
                        words.append(w)
        counts = Counter(words).most_common(20)
        labels = [w for w, _ in counts][::-1]
        values = [c for _, c in counts][::-1]
        annotation = "caption-keyword proxy — SED chart lands in term paper"
    else:
        # placeholder for the SED-derived chart once spectrogram_demo.py runs
        raise NotImplementedError("Wire up SED-output reading after Step 0 audio")

    fig, ax = plt.subplots(figsize=(6.5, 5))
    ax.barh(labels, values, color=PALETTE["accent"])
    ax.set_xlabel("Caption mentions")
    ax.set_title("Top-20 sound-event words in Clotho captions")
    ax.text(1.0, -0.18, annotation, transform=ax.transAxes,
            ha="right", va="top", fontsize=8, style="italic",
            color=PALETTE["muted"])
    _save(fig, "top20_class_bar.png")


def audit_diagram() -> None:
    """Slide 5 — three-layer contamination audit diagram."""
    layers = [
        ("Layer 1 — File-ID match", "Falcon3-Audio:  manifest is public", PALETTE["good"]),
        ("Layer 2 — Audio fingerprint\n(Chromaprint)",
         "SALMONN, Qwen2.5-Omni:  manifests partial", PALETTE["accent"]),
        ("Layer 3 — Caption n-gram overlap",
         "All three LALMs", PALETTE["warn"]),
    ]
    fig, ax = plt.subplots(figsize=(7.5, 4))
    ax.axis("off")
    ax.set_title("Three-layer contamination audit — per-LALM",
                 loc="left", color=PALETTE["navy"], pad=14)
    for i, (title, note, color) in enumerate(layers):
        y = 0.78 - i * 0.28
        box = plt.Rectangle((0.04, y - 0.10), 0.92, 0.20,
                            transform=ax.transAxes,
                            facecolor=color, alpha=0.12, edgecolor=color)
        ax.add_patch(box)
        ax.text(0.07, y + 0.02, title, transform=ax.transAxes,
                fontsize=11, weight="bold", color=color)
        ax.text(0.07, y - 0.06, note, transform=ax.transAxes,
                fontsize=9.5, color=PALETTE["navy"])
    _save(fig, "audit_diagram.png")


def gantt_8week() -> None:
    """Slide 5 — 8-week path to first evaluation."""
    weeks = [
        ("Audit (file-ID + fingerprint + n-gram)", 1, 2, PALETTE["accent"]),
        ("Polyphony split (PaSST + CNN14)", 3, 1, PALETTE["good"]),
        ("Zero-shot inference (3 LALMs + 3 baselines)", 4, 3, PALETTE["navy"]),
        ("SPIDEr-FL · MACE · Δ MACE · CHAIR-audio", 7, 2, PALETTE["warn"]),
    ]
    fig, ax = plt.subplots(figsize=(7.5, 3.3))
    for i, (label, start, length, color) in enumerate(weeks):
        ax.barh(i, length, left=start, color=color, edgecolor="white",
                height=0.55)
        ax.text(start + length / 2, i, label, ha="center", va="center",
                fontsize=9, color="white", weight="bold")
    ax.set_yticks([])
    ax.set_xlabel("Week")
    ax.set_xlim(0.5, 9.5)
    ax.set_xticks(range(1, 9))
    ax.set_title("8-week path to first evaluation (DCASE baseline SPIDEr-FL ≈ 29.6%)")
    for spine in ("left", "top", "right"):
        ax.spines[spine].set_visible(False)
    _save(fig, "gantt_8week.png")


def main() -> None:
    audio_properties_card()  # hard-coded — runs without data
    audit_diagram()          # hard-coded — runs without data
    gantt_8week()            # hard-coded — runs without data

    # require Clotho metadata/captions
    for fn in (clip_duration_hist, caption_length_hist, top20_class_bar):
        try:
            fn()
        except FileNotFoundError as e:
            print(f"skipping {fn.__name__}: {e}")


if __name__ == "__main__":
    main()
