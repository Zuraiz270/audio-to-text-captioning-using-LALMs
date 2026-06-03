"""EnCLAP captioner — wraps jaeyeonkim99/EnCLAP (ICASSP 2024).

EnCodec (24 kHz discrete codes) + LAION-CLAP (audio embedding) -> BART decoder.
The upstream repo is flat scripts; its inference.py defines a clean `EnClap`
class with `infer_from_audio(audio_1d, sample_rate) -> [caption]`, so we add its
directory to sys.path and wrap that class behind the Captioner contract.

Two weight files are required:
  - enclap_ckpt: a directory (config.json + pytorch_model.bin) — here the
    EnCLAP-base `clotho_finetune` checkpoint (AudioCaps-pretrained, Clotho-tuned).
  - clap_ckpt: a LAION-CLAP checkpoint. It MUST be the fusion + HTSAT-tiny
    variant (630k-audioset-fusion-best.pt) to match EnClap's hardcoded
    enable_fusion=True, amodel="HTSAT-tiny".

EnCLAP resamples internally — 24 kHz for EnCodec, 48 kHz for CLAP — so we feed
it Clotho's native 44.1 kHz float32 mono waveform unchanged.
"""
from __future__ import annotations

import sys
from pathlib import Path

import torch

from src.models.base import Captioner

_VENDOR_DIR = Path(__file__).resolve().parent / "_vendor_enclap"


def _import_enclap():
    # Upstream is flat scripts: inference.py does `from modeling.enclap_bart ...`,
    # which only resolves when its own directory is on sys.path.
    if str(_VENDOR_DIR) not in sys.path:
        sys.path.insert(0, str(_VENDOR_DIR))
    from inference import EnClap  # vendored at src/models/_vendor_enclap/inference.py
    return EnClap


class EnCLAPCaptioner(Captioner):
    def __init__(
        self,
        enclap_ckpt: Path | str,
        clap_ckpt: Path | str,
        device: str = "cpu",
        num_beams: int = 4,
        max_length: int = 50,
        clap_audio_model: str = "HTSAT-tiny",
        clap_enable_fusion: bool = True,
    ) -> None:
        EnClap = _import_enclap()
        self.device = torch.device(device)
        self.enclap = EnClap(
            ckpt_path=str(enclap_ckpt),
            clap_audio_model=clap_audio_model,
            clap_enable_fusion=clap_enable_fusion,
            clap_ckpt_path=str(clap_ckpt),
            device=self.device,
        )
        # Mirror upstream's generation_config, minus `_from_model_config`: that
        # stray key is accepted by transformers 4.29 but rejected as an unknown
        # generate() kwarg by 4.30+.
        self.generation_config = {
            "bos_token_id": 0,
            "decoder_start_token_id": 2,
            "eos_token_id": 2,
            "forced_bos_token_id": 0,
            "forced_eos_token_id": 2,
            "pad_token_id": 1,
            "no_repeat_ngram_size": 3,
            "early_stopping": True,
            "num_beams": num_beams,
            "max_length": max_length,
        }

    @torch.inference_mode()
    def caption(self, waveform: torch.Tensor, sample_rate: int = 44_100) -> str:
        audio_1d = waveform.squeeze(0).to(torch.float32)
        captions = self.enclap.infer_from_audio(audio_1d, sample_rate, self.generation_config)
        return captions[0].strip()
