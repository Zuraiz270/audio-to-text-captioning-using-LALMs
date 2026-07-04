"""SALMONN-13B captioner — wraps bytedance/SALMONN (salmonn branch, pinned a58bba7).

SALMONN (Tang et al., ICLR 2024) fuses a Whisper-large-v2 speech encoder and a
BEATs audio encoder through a window-level Q-Former into Vicuna-13B, with a LoRA
adaptor. Audio captioning (AAC) is one of its documented tasks; we use it
audio-only. It slots into the same Captioner contract as every other row.

The upstream repo is flat modules (config.py, utils.py, models/…), not a package,
so we inject its root on sys.path lazily — the same tactic as the CNN14 wrapper. It
pins transformers==4.28.0 / torch==2.0.1, so it runs in its own cluster conda env
(see requirements-salmonn.txt). All heavy imports are lazy, so importing the model
registry stays cheap in the CPU/other environments that lack those versions.
"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

import soundfile as sf
import torch

from src.models.base import Captioner

_VENDOR_DIR = Path(__file__).resolve().parent / "_vendor_salmonn"
_SALMONN_SR = 16_000  # both the Whisper encoder and BEATs operate at 16 kHz


def _lazy_imports():
    if str(_VENDOR_DIR) not in sys.path:
        sys.path.insert(0, str(_VENDOR_DIR))
    from models.salmonn import SALMONN
    from utils import prepare_one_sample
    from transformers import WhisperFeatureExtractor
    from omegaconf import OmegaConf
    return SALMONN, prepare_one_sample, WhisperFeatureExtractor, OmegaConf


class SalmonnCaptioner(Captioner):
    def __init__(
        self,
        salmonn_ckpt: str,
        whisper_path: str,
        beats_path: str,
        vicuna_path: str,
        device: str = "cuda:0",
        num_beams: int = 4,
        max_new_tokens: int = 64,
        prompt_template: str = "USER: {}\nASSISTANT:",
        caption_prompt: str = "Please describe the audio in one short, factual sentence.",
    ) -> None:
        SALMONN, prepare_one_sample, WhisperFeatureExtractor, OmegaConf = _lazy_imports()
        self._prepare_one_sample = prepare_one_sample
        self.device = torch.device(device)
        self.prompt_template = prompt_template
        self.caption_prompt = caption_prompt

        # Mirror configs/decode_config.yaml's `model:` block. from_config loads the
        # trained Q-Former + LoRA + projection from `ckpt` (salmonn_v1.pth) with
        # strict=False; Whisper/BEATs/Vicuna load from their own paths. low_resource
        # stays False so Vicuna loads in fp16 (no 8-bit quantisation).
        model_cfg = OmegaConf.create({
            "llama_path": vicuna_path,
            "whisper_path": whisper_path,
            "beats_path": beats_path,
            "ckpt": salmonn_ckpt,
            "lora": True,
            "lora_rank": 8,
            "lora_alpha": 32,
            "lora_dropout": 0.1,
            "use_speech_Qformer": True,
            "num_speech_query_token": 1,
            "freeze_speech_QFormer": False,
            "window_level_Qformer": True,
            "second_per_window": 0.333333,
            "second_stride": 0.333333,
            "speech_llama_proj_model": "",
            "freeze_speech_llama_proj": False,
            "low_resource": False,
            "multi_prompt": True,
            "prompt_template": prompt_template,
        })
        self.model = SALMONN.from_config(model_cfg)
        self.model.to(self.device).eval()
        self.wav_processor = WhisperFeatureExtractor.from_pretrained(whisper_path)

        self.generate_cfg = OmegaConf.create({
            "max_new_tokens": max_new_tokens,
            "num_beams": num_beams,
            "do_sample": False,
            "min_length": 1,
            "temperature": 1.0,
            "top_p": 0.9,
            "repetition_penalty": 1.0,
            "length_penalty": 1.0,
        })

    @torch.no_grad()
    def caption(self, waveform: torch.Tensor, sample_rate: int = 44_100) -> str:
        import torchaudio.functional as AF

        audio = waveform.squeeze(0).to(torch.float32)
        if sample_rate != _SALMONN_SR:
            # prepare_one_sample reads the file at its native rate and feeds that to
            # the 16 kHz Whisper extractor + BEATs, so we resample before writing.
            audio = AF.resample(audio, sample_rate, _SALMONN_SR)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf:
            tmp = tf.name
        try:
            sf.write(tmp, audio.cpu().numpy(), _SALMONN_SR)
            samples = self._prepare_one_sample(tmp, self.wav_processor)
            prompt = [self.prompt_template.format(
                "<Speech><SpeechHere></Speech> " + self.caption_prompt.strip()
            )]
            with torch.cuda.amp.autocast(dtype=torch.float16):
                text = self.model.generate(samples, self.generate_cfg, prompts=prompt)[0]
            return text.strip()
        finally:
            os.unlink(tmp)
