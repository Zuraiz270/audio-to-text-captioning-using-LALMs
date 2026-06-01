"""CNN14 + BART captioner — wraps felixgontier/dcase-2023-baseline.

The upstream repo is flat scripts (not a package), so its internal
`from audio_encoders import CNN14Encoder` style only resolves when its
directory is on sys.path. We do that lazily inside `_import_bartaac`.

We cannot `import` the upstream `audio_logmel` module because it reads
data/audio_info.pkl at module load time. The mel-spec function it defines
is short and stable; we inline it here.
"""
from __future__ import annotations

import sys
from pathlib import Path

import librosa
import numpy as np
import torch

from src.models.base import Captioner

_VENDOR_DIR = Path(__file__).resolve().parent / "_vendor"


def _import_bartaac():
    if str(_VENDOR_DIR) not in sys.path:
        sys.path.insert(0, str(_VENDOR_DIR))
    from models import BARTAAC  # vendored at src/models/_vendor/models.py
    return BARTAAC


def _log_mel_spectrogram(
    y: np.ndarray,
    sample_rate: int,
    window_length_secs: float = 0.040,
    hop_length_secs: float = 0.020,
    num_mels: int = 64,
) -> np.ndarray:
    """Mirror of `_vendor/audio_logmel.log_mel_spectrogram`. Output shape: (n_mels, T)."""
    window_length = int(round(sample_rate * window_length_secs))
    hop_length = int(round(sample_rate * hop_length_secs))
    fft_length = 2 ** int(np.ceil(np.log(window_length) / np.log(2.0)))
    mel = librosa.feature.melspectrogram(
        y=y,
        sr=sample_rate,
        n_fft=fft_length,
        hop_length=hop_length,
        win_length=window_length,
        n_mels=num_mels,
    )
    return np.log(mel + np.spacing(1))


def _inference_settings(audio_enc_path: Path, num_beams: int, max_length: int) -> dict:
    """Mock the Hydra-shaped settings dict BARTAAC.__init__ reads.

    Mirrors src/models/_vendor/exp_settings/dcb.yaml — only the keys BARTAAC
    actually touches are populated.
    """
    return {
        "lm": {
            "audio_enc_path": str(audio_enc_path),
            "freeze_audio_enc": True,
            "pretrained": None,
            "config": {
                "vocab_size": 50265,
                "encoder_layers": 0,
                "encoder_ffn_dim": 3072,
                "encoder_attention_heads": 12,
                "decoder_layers": 6,
                "decoder_ffn_dim": 3072,
                "decoder_attention_heads": 12,
                "activation_function": "gelu",
                "d_model": 768,
                "dropout": 0.1,
                "attention_dropout": 0.1,
                "activation_dropout": 0.1,
                "classifier_dropout": 0.0,
            },
            "generation": {
                "max_length": max_length,
                "min_length": 5,
                "early_stopping": True,
                "num_beams": num_beams,
                "length_penalty": 1.0,
                "no_repeat_ngram_size": 3,
            },
            "freeze": dict.fromkeys(
                ("all", "dec", "enc", "attn", "mlp",
                 "dec_attn", "dec_mlp", "dec_self_attn", "enc_mlp", "enc_attn"),
                False,
            ),
        },
        "adapt": {
            "audio_emb_size": 2048,
            "nb_layers": 1,
        },
    }


class CNN14DCASECaptioner(Captioner):
    def __init__(
        self,
        encoder_ckpt: Path | str,
        decoder_ckpt: Path | str,
        device: str = "cpu",
        num_beams: int = 4,
        max_length: int = 100,
        tokenizer_id: str = "facebook/bart-base",
    ) -> None:
        from transformers import AutoTokenizer

        BARTAAC = _import_bartaac()
        self.device = torch.device(device)
        settings = _inference_settings(Path(encoder_ckpt), num_beams, max_length)

        self.model = BARTAAC(settings, self.device)

        ckpt = torch.load(str(decoder_ckpt), map_location=self.device)
        self.model.load_state_dict(ckpt, strict=True)

        # `pretrained: null` means BARTAAC built BART from a bare BartConfig
        # without forced_bos_token_id. The trained checkpoint expects <s> (id 0)
        # forced as the first generated token after </s> (decoder_start, id 2).
        self.model.bart_lm.config.forced_bos_token_id = 0
        self.model.to(self.device).eval()

        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_id, use_fast=True)

    @torch.inference_mode()
    def caption(self, waveform: torch.Tensor, sample_rate: int = 44_100) -> str:
        y = waveform.squeeze(0).cpu().numpy().astype(np.float32, copy=False)
        log_mel = _log_mel_spectrogram(y, sample_rate=sample_rate)
        mel_tensor = torch.from_numpy(log_mel.T).unsqueeze(0).to(self.device).float()
        output_ids = self.model.generate_beam(audio_features=mel_tensor)
        return self.tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()
