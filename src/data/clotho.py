"""Clotho v2.1 evaluation-split loader.

Yields mono 44.1 kHz float32 waveforms (Clotho native rate, matching the
felixgontier/dcase-2023-baseline training preprocessing — librosa.load(sr=None))
paired with their five ground-truth captions. The polyphony-subset filter is
a stub until the SED pipeline lands; see filter_polyphony() below.
"""
from __future__ import annotations

from pathlib import Path
from typing import TypedDict

import pandas as pd
import soundfile as sf
import torch
import torchaudio.functional as F
from torch.utils.data import Dataset, Subset

TARGET_SAMPLE_RATE = 44_100  # Clotho v2.1 native; what the baseline was trained on


class ClothoItem(TypedDict):
    file_name: str
    waveform: torch.Tensor  # shape (1, T), float32, mono, 44.1 kHz
    sample_rate: int
    references: list[str]


class ClothoEvalDataset(Dataset):
    """Read-only loader over a Clotho v2.1 split.

    Args:
        root: data/clotho_v2.1/  (must contain clotho_captions_<split>.csv
              and clotho_audio_<split>/<split>/*.wav).
        split: "evaluation" | "development" | "validation".
    """

    def __init__(self, root: Path | str, split: str = "evaluation") -> None:
        self.root = Path(root)
        self.split = split

        captions_csv = self.root / f"clotho_captions_{split}.csv"
        audio_dir = self.root / f"clotho_audio_{split}" / split

        if not captions_csv.is_file():
            raise FileNotFoundError(f"Captions CSV not found: {captions_csv}")
        if not audio_dir.is_dir():
            raise FileNotFoundError(f"Audio dir not found: {audio_dir}")

        self.audio_dir = audio_dir
        self.df = pd.read_csv(captions_csv)

        expected = {"file_name", *(f"caption_{i}" for i in range(1, 6))}
        missing = expected - set(self.df.columns)
        if missing:
            raise ValueError(f"Captions CSV missing columns: {sorted(missing)}")

    def __len__(self) -> int:
        return len(self.df)

    def __getitem__(self, idx: int) -> ClothoItem:
        row = self.df.iloc[idx]
        file_name = str(row["file_name"])
        path = self.audio_dir / file_name

        waveform_np, sample_rate = sf.read(str(path), dtype="float32", always_2d=True)
        waveform = torch.from_numpy(waveform_np.T).contiguous()  # (channels, frames)

        if waveform.shape[0] > 1:
            waveform = waveform.mean(dim=0, keepdim=True)

        if sample_rate != TARGET_SAMPLE_RATE:
            waveform = F.resample(waveform, orig_freq=sample_rate, new_freq=TARGET_SAMPLE_RATE)

        return {
            "file_name": file_name,
            "waveform": waveform,
            "sample_rate": TARGET_SAMPLE_RATE,
            "references": [str(row[f"caption_{i}"]) for i in range(1, 6)],
        }


def filter_polyphony(dataset: ClothoEvalDataset, manifest_csv: Path | None = None) -> Dataset:
    """Restrict a Clotho dataset to polyphonic clips.

    Stub: returns the input dataset unchanged when manifest_csv is None.
    When the SED pipeline produces a `file_name,is_polyphonic` CSV, this will
    build a Subset of just the rows where is_polyphonic is True.
    """
    if manifest_csv is None:
        return dataset

    manifest = pd.read_csv(manifest_csv)
    poly_files = set(manifest.loc[manifest["is_polyphonic"], "file_name"])
    indices = [i for i, fn in enumerate(dataset.df["file_name"]) if fn in poly_files]
    return Subset(dataset, indices)
