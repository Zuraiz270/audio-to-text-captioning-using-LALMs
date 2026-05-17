"""Render the waveform + log-mel spectrogram panels for the P2 deck.

Uses `librosa.stft` exactly as Prof. Abeßer's Lecture 04 slide 17 names.
Outputs are written to deliverables/p2/figures/. Run from the project root:

    python deliverables/p2/spectrogram_demo.py

Requires Clotho v2.1 audio at data/clotho_v2.1/development/Development/*.wav
(and optionally AudioCaps + WavCaps samples for the slide-2 contrast strip).

Panels produced (slide -> filename):
  slide 2 -> contrast_<dataset>_rain.png   waveform + spectrogram for
                                           the same nominal class across
                                           Clotho / AudioCaps / WavCaps
  slide 3 -> canonical_clotho.png          one canonical clip — waveform +
                                           spectrogram + caption
  slide 4 -> gallery_<i>_<class>.png       4-6 representative class panels
  slide 4 -> mono_example.png              mono panel: caption + waveform +
                                           spectrogram
  slide 4 -> poly_example.png              poly panel: caption + waveform +
                                           spectrogram

Also copies the two example .wav files into deliverables/p2/audio_samples/
so PowerPoint can embed playback links.


===========================================================================
BACKGROUND: WHAT THIS SCRIPT DOES AT A HIGH LEVEL
===========================================================================
Sound is a pressure wave sampled into numbers (e.g., 44,100 numbers per
second).  A *waveform* plot shows amplitude vs time — useful, but it hides
WHICH frequencies are present.

A *spectrogram* reveals frequency content over time by:
  1. Cutting the audio into short overlapping windows  (STFT)
  2. Computing the frequency spectrum of each window   (DFT per frame)
  3. Stacking those spectra side-by-side               (time on x, freq on y)
  4. Warping the frequency axis to match human hearing  (mel scale)
  5. Converting power to decibels                       (log scale)

This script loads .wav files, runs that pipeline via librosa, and saves
the resulting waveform + spectrogram figures as PNGs for a presentation.
===========================================================================
"""

from __future__ import annotations

import shutil
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------------------------------
# IMPORT LIBROSA — the core audio-analysis library
# ---------------------------------------------------------------------------
# librosa provides:
#   - librosa.load()       → read a WAV/MP3 into a numpy array
#   - librosa.stft()       → Short-Time Fourier Transform
#   - librosa.feature.melspectrogram() → apply mel filter bank
#   - librosa.power_to_db() → convert power values to decibels
#   - librosa.display.specshow() → render a spectrogram as an image
# ---------------------------------------------------------------------------
try:
    import librosa
    import librosa.display
except ImportError as e:  # pragma: no cover
    raise SystemExit(
        "librosa is required. Install via:\n"
        "    pip install -r deliverables/p2/requirements.txt"
    ) from e

# ---------------------------------------------------------------------------
# PATH CONFIGURATION
# ---------------------------------------------------------------------------
# Path(__file__) = this script's location on disk.
# .resolve()     = make it an absolute path (no ".." or symlinks).
# .parents[2]    = go up 2 directories:
#     this file:  <root>/deliverables/p2/spectrogram_demo.py
#     parents[0]: <root>/deliverables/p2/
#     parents[1]: <root>/deliverables/
#     parents[2]: <root>/                 ← PROJECT_ROOT
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CLOTHO_AUDIO_DIR = PROJECT_ROOT / "data" / "clotho_v2.1" / "clotho_audio_development" / "development"
AUDIOCAPS_DIR = PROJECT_ROOT / "data" / "audiocaps"
WAVCAPS_DIR = PROJECT_ROOT / "data" / "wavcaps"

FIG_DIR = Path(__file__).resolve().parent / "figures"
SAMPLES_DIR = Path(__file__).resolve().parent / "audio_samples"
FIG_DIR.mkdir(parents=True, exist_ok=True)       # create figures/ if missing
SAMPLES_DIR.mkdir(parents=True, exist_ok=True)    # create audio_samples/ if missing

# ---------------------------------------------------------------------------
# STFT / MEL PARAMETERS — these control the spectrogram resolution
# ---------------------------------------------------------------------------
#
# SR (Sample Rate) = 44,100 Hz
#   → We capture 44,100 amplitude measurements per second.
#   → A 5-second clip = 5 × 44,100 = 220,500 float values in a 1-D array.
#   → The highest frequency we can represent = SR/2 = 22,050 Hz (Nyquist).
#
# N_FFT = 1024 (the "window size" for the STFT)
#   → Each STFT frame analyzes a chunk of 1024 consecutive samples.
#   → Duration of one window = 1024 / 44100 ≈ 23.2 milliseconds.
#   → Number of unique frequency bins = N_FFT // 2 + 1 = 513 bins.
#   → Frequency resolution = SR / N_FFT = 44100 / 1024 ≈ 43.1 Hz per bin.
#     (bin 0 = 0 Hz, bin 1 = 43 Hz, bin 2 = 86 Hz, ..., bin 512 = 22050 Hz)
#
# HOP = 512 (how far the window slides between frames)
#   → Each frame overlaps the previous one by N_FFT - HOP = 512 samples (50%).
#   → Time between consecutive frames = 512 / 44100 ≈ 11.6 ms.
#   → For a 2-second clip (88,200 samples):
#       num_frames ≈ 1 + (88200 - 1024) / 512 ≈ 171 frames.
#
# N_MELS = 64
#   → Collapse 513 linear frequency bins into 64 mel-spaced bands.
#   → The mel scale is ~linear below 700 Hz, ~logarithmic above.
#   → This matches how humans perceive pitch: 100→200 Hz feels the same
#     "distance" as 1000→2000 Hz.
#
# TRADEOFF (very important to understand):
#   Larger N_FFT → better frequency detail, but worse time precision
#   Smaller N_FFT → better time detail, but worse frequency precision
#   This is a fundamental physics limit (uncertainty principle analogy).
# ---------------------------------------------------------------------------
SR = 44100
N_FFT = 1024
HOP = 512
N_MELS = 64

# ---------------------------------------------------------------------------
# VISUAL STYLING — color palette for the plots
# ---------------------------------------------------------------------------
PALETTE = {
    "navy": "#1f2a44",     # dark blue for titles / text
    "accent": "#3a5fcd",   # medium blue for the waveform line
    "warn": "#c25a4f",     # muted red for annotation text
}

# Set matplotlib defaults so every plot has consistent fonts and resolution
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.titlesize": 12,
    "axes.labelsize": 10,
    "axes.titleweight": "bold",
    "figure.dpi": 160,       # high-res output for the slide deck
})


# ===========================================================================
# CORE DSP FUNCTION: _log_mel()
# ===========================================================================
#
# DRY RUN with a 2-second mono clip at 44,100 Hz:
#   y.shape = (88200,)   ← 88,200 float samples
#
# STEP 1 — librosa.stft(y, n_fft=1024, hop_length=512)
#   What happens internally:
#     a) librosa pads y slightly so the last frame fits.
#     b) A Hann window of length 1024 is created:
#          w[n] = 0.5 × (1 − cos(2π·n / 1023)),  n = 0..1023
#        This window tapers smoothly to zero at both edges, reducing
#        spectral leakage (artifacts from cutting the signal abruptly).
#     c) For each frame t (t = 0, 1, 2, ...):
#          - Extract chunk: y[t*512 : t*512 + 1024]  (1024 samples)
#          - Multiply element-wise by the Hann window
#          - Compute the DFT of the 1024 windowed samples
#          - Keep only the first 513 complex values (the rest are mirrors)
#     d) Stack all frames side by side → complex matrix (513, ~171)
#
#   Output: complex128 array, shape (513, 171)
#   Each value is a complex number:  a + bj
#     |a + bj| = magnitude = "how loud this frequency is in this frame"
#     angle(a + bj) = phase = "where in the cycle" (we discard this)
#
# STEP 2 — np.abs(...) ** 2  →  Power Spectrogram
#   np.abs(complex) computes sqrt(a² + b²) for each element → magnitudes
#   ** 2 squares those magnitudes → power values
#   Output: float64 array, shape (513, 171), all values ≥ 0
#
# STEP 3 — librosa.feature.melspectrogram(S=spec, sr=44100, n_mels=64)
#   Builds a (64, 513) mel filter bank matrix, then multiplies:
#     mel = filterbank @ spec   →  (64, 513) @ (513, 171) = (64, 171)
#   Each of the 64 triangular filters sums energy from a range of the 513
#   frequency bins.  Low-frequency filters are narrow (high precision where
#   humans are sensitive); high-frequency filters are wide (we can't
#   distinguish fine differences up there).
#   Output: float64 array, shape (64, 171)
#
# STEP 4 — librosa.power_to_db(mel, ref=np.max)
#   Converts power to decibels:  dB = 10 × log10(mel / ref)
#   ref=np.max → the loudest cell becomes 0 dB, everything else is negative.
#   Typical range: 0 dB (loudest) to about −80 dB (near silence).
#   Output: float64 array, shape (64, 171), values in [−80, 0]
#
# ===========================================================================
def _log_mel(y: np.ndarray, sr: int) -> np.ndarray:
    """Compute the log-mel-spectrogram via the librosa.stft pipeline.

    Full pipeline:  raw audio → STFT → |magnitude|² → mel filterbank → dB

    Args:
        y:  1-D numpy array of audio samples, shape (num_samples,).
        sr: Sample rate in Hz (e.g. 44100).

    Returns:
        2-D numpy array of shape (N_MELS, num_frames) with values in dB.
    """
    # --- STFT then power spectrogram ---
    # librosa.stft returns complex values; np.abs gets magnitudes; **2 = power
    # Result shape: (N_FFT//2 + 1, num_frames) = (513, ~171) for 2s audio
    spec = np.abs(librosa.stft(y, n_fft=N_FFT, hop_length=HOP)) ** 2

    # --- Mel filter bank ---
    # S=spec tells librosa "I already computed the power spectrogram; just
    # apply the mel filters".  If we passed y= instead, it would redo the STFT.
    # Result shape: (N_MELS, num_frames) = (64, ~171)
    mel = librosa.feature.melspectrogram(S=spec, sr=sr, n_mels=N_MELS)

    # --- Convert to decibels ---
    # Human loudness perception is logarithmic: a 10× power increase sounds
    # like "twice as loud".  dB scale captures this.
    # ref=np.max normalizes so the peak = 0 dB.
    return librosa.power_to_db(mel, ref=np.max)


# ===========================================================================
# RENDERING: _render_panel()
# ===========================================================================
#
# This function takes ONE audio file and produces ONE figure with two panels:
#   Top:    waveform   (amplitude vs time — the raw "shape" of the sound)
#   Bottom: log-mel spectrogram (frequency content vs time — color = loudness)
#
# DRY RUN — _render_panel("rain.wav", "Rain falling...", "Rain", out.png):
#
#   1. librosa.load("rain.wav", sr=44100, mono=True)
#      → reads the WAV, resamples to 44100 Hz, mixes stereo→mono
#      → y.shape = (88200,)  (2 seconds of audio)
#      → sr = 44100
#
#   2. _log_mel(y, sr) → log_mel.shape = (64, 171), values in dB
#
#   3. plt.subplots(2, 1) creates a figure with two vertically stacked axes:
#      ax_wave (top, height ratio 1) and ax_spec (bottom, height ratio 2)
#
#   4. Waveform plot:
#      times = np.linspace(0, 2.0, 88200)  → evenly spaced [0.0, ..., 2.0]
#      ax_wave.plot(times, y)  → plots amplitude vs time as a line
#
#   5. Spectrogram plot:
#      librosa.display.specshow(log_mel, ...)
#      → internally maps the (64, 171) matrix onto a colored image
#      → x_axis='time' converts frame indices to seconds using hop_length
#      → y_axis='mel' labels the y-axis with mel-frequency Hz values
#      → cmap='magma' uses the magma colormap (black → purple → orange → yellow)
#
#   6. Colorbar, caption text, save to PNG, close figure.
#
# ===========================================================================
def _render_panel(
    wav_path: Path,
    caption: str,
    title: str,
    out: Path,
    annotation: str | None = None,
) -> None:
    # --- Load audio ---
    # sr=SR forces resampling to our target rate (44100 Hz)
    # mono=True mixes L+R channels into one channel if the file is stereo
    # Returns: y = 1-D float array, sr = integer sample rate
    y, sr = librosa.load(str(wav_path), sr=SR, mono=True)

    # --- Compute the spectrogram via our pipeline ---
    log_mel = _log_mel(y, sr)

    # --- Create a 2-row, 1-column figure ---
    # height_ratios=[1, 2] means the spectrogram panel is 2× taller than waveform
    # sharex=False because the waveform uses raw sample times while specshow
    # manages its own x-axis ticks internally
    fig, (ax_wave, ax_spec) = plt.subplots(
        2, 1, figsize=(6.5, 4.2), sharex=False,
        gridspec_kw={"height_ratios": [1, 2]},
    )

    # --- Top panel: waveform ---
    # np.linspace(0, duration, num_samples) gives each sample its time in sec
    # e.g., for 88200 samples at 44100 Hz: times = [0.0, 0.0000227, ..., 2.0]
    times = np.linspace(0, len(y) / sr, len(y))
    ax_wave.plot(times, y, color=PALETTE["accent"], linewidth=0.6)
    ax_wave.set_xlim(0, len(y) / sr)     # x-axis spans [0, duration_seconds]
    ax_wave.set_ylabel("Amplitude")       # y-axis = signal amplitude [-1, 1]
    ax_wave.set_title(title, loc="left", color=PALETTE["navy"])
    ax_wave.set_xticks([])                # hide x ticks (spectrogram below has them)
    # Remove top, right, bottom borders for a clean look
    for spine in ("top", "right", "bottom"):
        ax_wave.spines[spine].set_visible(False)

    # --- Bottom panel: log-mel spectrogram ---
    # specshow() renders the 2-D dB array as a heatmap image
    # x_axis='time': converts frame index → seconds (using hop_length & sr)
    # y_axis='mel':  labels frequency axis in mel-scaled Hz
    # cmap='magma':  perceptually uniform dark-to-bright colormap
    img = librosa.display.specshow(
        log_mel, sr=sr, hop_length=HOP, x_axis="time", y_axis="mel",
        ax=ax_spec, cmap="magma",
    )
    ax_spec.set_ylabel("Mel frequency")
    ax_spec.set_xlabel("Time (s)")

    # Add a colorbar showing the dB scale alongside the spectrogram
    # format="%+2.0f dB" prints values like "+0 dB", "-40 dB"
    fig.colorbar(img, ax=ax_spec, format="%+2.0f dB",
                 fraction=0.035, pad=0.02)

    # --- Caption text below the spectrogram ---
    # transform=ax_spec.transAxes → coordinates are in axis-fraction space
    # (0.0, -0.25) means "left edge, 25% below the bottom of the axis"
    caption_y = -0.25
    ax_spec.text(0.0, caption_y, f"caption: \u201c{caption}\u201d",
                 transform=ax_spec.transAxes, fontsize=9.5,
                 color=PALETTE["navy"], wrap=True, style="italic")

    # Optional annotation line (e.g., "source: clotho") below the caption
    if annotation:
        ax_spec.text(0.0, caption_y - 0.10, annotation,
                     transform=ax_spec.transAxes, fontsize=8,
                     color=PALETTE["warn"])

    # --- Save and close ---
    # tight_layout minimizes whitespace; rect=(0, 0.02, 1, 1) leaves 2% at bottom
    # for the caption text that extends below the axes
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    plt.close(fig)    # free memory (important when rendering many panels)
    print(f"wrote {out.relative_to(PROJECT_ROOT)}")


# ---------------------------------------------------------------------------
# CLIP SELECTION — Edit these tuples to choose which audio clips to render.
# Each tuple: (wav_filename, caption_text, plot_title)
# ---------------------------------------------------------------------------

# Slide 3 — one canonical clip (a "typical" Clotho sample)
CANONICAL_CLOTHO: tuple[str, str, str] | None = (
    "20091225.rain.wav",
    "Rain falling down onto a house or building.",
    "Canonical Clotho v2.1 sample — rain",
)

# Slide 4 — mono + poly example pair
# "Monophonic" = single sound source (just a cat meowing)
# "Polyphonic" = multiple overlapping sources (coffee machine + people talking)
MONO_EXAMPLE: tuple[str, str, str] | None = (
    "miau.wav",
    "A cat is meowing and crying at a steady pace, without letup.",
    "Monophonic — single sound source",
)
POLY_EXAMPLE: tuple[str, str, str] | None = (
    "Busy Coffee Shop.wav",
    "A coffee machine operates as people converse in the background.",
    "Polyphonic — multiple overlapping events",
)

# Slide 4 — class gallery (4-6 clips spanning the dataset's variety)
GALLERY: list[tuple[str, str, str]] = [
    ("TwoToneDoorbell.wav",
     "A doorbell is rung as it resounds continuously.",
     "Mechanical \u00b7 doorbell"),
    ("police_car_siren-esp.wav",
     "A siren with a high pitch was blared multiple times.",
     "Urban \u00b7 siren"),
    ("Summer Ambiance .wav",
     "A few birds chirping during an ominous breezing wind.",
     "Nature \u00b7 birds + wind"),
    ("Creaking and squeaking of old headsets.wav",
     "A person performing a delicate engineering task.",
     "Indoor \u00b7 mechanical detail"),
]

# Slide 2 — 3-dataset contrast strip (same nominal class across corpora)
# This compares how different datasets capture the same concept ("rain")
CONTRAST_STRIP: dict[str, tuple[Path, str, str] | None] = {
    "clotho": (
        CLOTHO_AUDIO_DIR / "Rain_inside_of_a_Car.wav",
        "It is raining and hailing on the roof top.",
        "Clotho — rain",
    ),
    "audiocaps": (
        PROJECT_ROOT / "data" / "audiocaps" / "audiocaps_rain_1.wav",
        "Rain is falling continuously.",
        "AudioCaps — rain",
    ),
    "wavcaps": (
        PROJECT_ROOT / "data" / "wavcaps" / "wavcaps_rain_1.wav",
        "Light rain and crickets at sunset.",
        "WavCaps — rain",
    ),
}

# Slide 2 — "what each dataset looks like" galleries
# These are the bucketed samples fetched by fetch_dataset_samples.py.
# Each panel: corpus-tagged caption + waveform + log-mel spectrogram.
DATASET_GALLERY_BUCKETS = ["rain", "dog", "music", "vehicle", "water", "voice"]


# ===========================================================================
# RENDER FUNCTIONS — each one renders a specific slide's figures
# ===========================================================================

def render_canonical() -> None:
    """Slide 3: Render one canonical Clotho sample (waveform + spectrogram)."""
    if CANONICAL_CLOTHO is None or not CLOTHO_AUDIO_DIR.exists():
        print("CANONICAL_CLOTHO not set or audio dir missing; skipping")
        return
    fname, caption, title = CANONICAL_CLOTHO   # unpack the 3-tuple
    _render_panel(
        CLOTHO_AUDIO_DIR / fname, caption, title,
        FIG_DIR / "canonical_clotho.png",
    )


def render_mono_poly() -> None:
    """Slide 4: Render mono vs poly examples + copy WAVs for PowerPoint embed.

    DRY RUN:
      Loop iteration 1: example=MONO_EXAMPLE, slot="mono"
        fname = "miau.wav"
        → renders figures/mono_example.png
        → copies miau.wav to audio_samples/mono_example.wav

      Loop iteration 2: example=POLY_EXAMPLE, slot="poly"
        fname = "Busy Coffee Shop.wav"
        → renders figures/poly_example.png
        → copies file to audio_samples/poly_example.wav
    """
    if MONO_EXAMPLE is None or POLY_EXAMPLE is None:
        print("MONO_EXAMPLE / POLY_EXAMPLE not set; skipping")
        return
    for example, slot in ((MONO_EXAMPLE, "mono"), (POLY_EXAMPLE, "poly")):
        fname, caption, title = example
        src = CLOTHO_AUDIO_DIR / fname
        _render_panel(src, caption, title, FIG_DIR / f"{slot}_example.png")
        # Also copy the WAV so PowerPoint can link to it for playback
        shutil.copy(src, SAMPLES_DIR / f"{slot}_example.wav")
        print(f"copied {fname} -> audio_samples/{slot}_example.wav")


def render_gallery() -> None:
    """Slide 4: Render 4-6 gallery panels showing dataset variety.

    DRY RUN with GALLERY = [("TwoToneDoorbell.wav", ..., "Mechanical · doorbell"), ...]:
      i=1: safe = "mechanical_·_doorbell"
           → figures/gallery_1_mechanical_·_doorbell.png
      i=2: → figures/gallery_2_urban_·_siren.png
      i=3: → figures/gallery_3_nature_·_birds_+_wind.png
      i=4: → figures/gallery_4_indoor_·_mechanical_detail.png
    """
    if not GALLERY:
        print("GALLERY empty; skipping")
        return
    for i, (fname, caption, title) in enumerate(GALLERY, 1):
        # Make a filesystem-safe version of the title for the filename
        safe = title.lower().replace(" ", "_").replace("/", "_")
        _render_panel(
            CLOTHO_AUDIO_DIR / fname, caption, title,
            FIG_DIR / f"gallery_{i}_{safe}.png",
        )


def render_contrast_strip() -> None:
    """Slide 2: Render the same audio class from 3 different datasets.

    DRY RUN:
      label="clotho":   → figures/contrast_clotho_rain.png
      label="audiocaps": → figures/contrast_audiocaps_rain.png
      label="wavcaps":   → figures/contrast_wavcaps_rain.png
    """
    for label, spec in CONTRAST_STRIP.items():
        if spec is None:
            print(f"contrast slot `{label}` not set; skipping")
            continue
        wav, caption, title = spec
        _render_panel(
            wav, caption, title,
            FIG_DIR / f"contrast_{label}_rain.png",
            annotation=f"source: {label}",   # red text noting the corpus
        )


def render_dataset_gallery(corpus: str, base_dir: Path) -> None:
    """Render the 'what does this dataset look like' panel for slide 2.

    Picks up the bucket WAVs produced by fetch_dataset_samples.py and renders
    one panel per bucket. Used to back the rejection narrative ("here is what
    AudioCaps / WavCaps actually look like, and why we did not pick them").

    DRY RUN for corpus="audiocaps", base_dir=<root>/data/audiocaps/:
      For each bucket in ["rain", "dog", "music", "vehicle", "water", "voice"]:
        wav = <root>/data/audiocaps/audiocaps_rain_1.wav
        If it exists → render figures/audiocaps_gallery_rain.png
        If not → skip
      Prints "audiocaps gallery: 3 panels rendered" (for however many exist)
    """
    if not base_dir.exists():
        print(f"{corpus} dir missing; skipping dataset gallery")
        return
    rendered = 0
    for bucket in DATASET_GALLERY_BUCKETS:
        wav = base_dir / f"{corpus}_{bucket}_1.wav"
        cap_path = base_dir / f"{corpus}_{bucket}_1.caption.txt"
        if not wav.exists():
            continue
        # Read the caption from a companion .txt file if it exists
        caption = cap_path.read_text(encoding="utf-8").strip() if cap_path.exists() else ""
        _render_panel(
            wav, caption, f"{corpus.capitalize()} — {bucket}",
            FIG_DIR / f"{corpus}_gallery_{bucket}.png",
        )
        rendered += 1
    print(f"{corpus} gallery: {rendered} panels rendered")


# ===========================================================================
# MAIN — orchestrates all rendering
# ===========================================================================
def main() -> None:
    """Entry point: check for audio data, then render all slide figures.

    Execution order:
      1. render_canonical()        → slide 3: one canonical Clotho sample
      2. render_mono_poly()        → slide 4: mono vs poly comparison
      3. render_gallery()          → slide 4: 4 diverse audio class examples
      4. render_contrast_strip()   → slide 2: same class, 3 datasets
      5. render_dataset_gallery()  → slide 2: AudioCaps & WavCaps previews
    """
    if not CLOTHO_AUDIO_DIR.exists():
        print(
            f"Clotho audio not yet at {CLOTHO_AUDIO_DIR}\n"
            "Complete Step 0 download (see plan), then re-run."
        )
        return
    render_canonical()
    render_mono_poly()
    render_gallery()
    render_contrast_strip()
    render_dataset_gallery("audiocaps", PROJECT_ROOT / "data" / "audiocaps")
    render_dataset_gallery("wavcaps", PROJECT_ROOT / "data" / "wavcaps")


if __name__ == "__main__":
    main()
