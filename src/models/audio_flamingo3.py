"""Audio Flamingo 3 captioner (NVIDIA) — third LALM row.

AF3 (`nvidia/audio-flamingo-3-hf`) is transformers-native
(`AudioFlamingo3ForConditionalGeneration`): a Whisper-style audio encoder (128 mel
bins) feeding a Qwen2-7B text decoder through a projector. We use it audio-only for
captioning. It runs in the *same* transformers 5.x environment as the Qwen row (no
separate build), so this is the lightest LALM row to add.

All heavy imports are lazy so importing the model registry stays cheap in the
CPU/other environments that lack transformers 5.x.
"""
from __future__ import annotations

import os
import tempfile

import soundfile as sf
import torch

from src.models.base import Captioner

_AF3_SR = 16_000  # the Whisper-style encoder (128 mel bins) operates at 16 kHz


def _lazy_imports():
    from transformers import AudioFlamingo3ForConditionalGeneration, AutoProcessor
    return AudioFlamingo3ForConditionalGeneration, AutoProcessor


class AudioFlamingo3Captioner(Captioner):
    def __init__(
        self,
        model_id: str = "nvidia/audio-flamingo-3-hf",
        device: str = "cuda",
        num_beams: int = 1,
        max_new_tokens: int = 64,
        caption_prompt: str = "Describe the audio in one short, factual sentence.",
    ) -> None:
        Model, Processor = _lazy_imports()
        self.num_beams = num_beams
        self.max_new_tokens = max_new_tokens
        self.caption_prompt = caption_prompt

        self.model = Model.from_pretrained(
            model_id, torch_dtype=torch.bfloat16, device_map="auto"
        )
        self.model.eval()
        self.processor = Processor.from_pretrained(model_id)

    @torch.inference_mode()
    def caption(self, waveform: torch.Tensor, sample_rate: int = 44_100) -> str:
        import torchaudio.functional as AF

        audio = waveform.squeeze(0).to(torch.float32)
        if sample_rate != _AF3_SR:
            audio = AF.resample(audio, sample_rate, _AF3_SR)
        # The processor loads audio from a path; write a short-lived 16 kHz temp WAV.
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf:
            tmp = tf.name
        try:
            sf.write(tmp, audio.cpu().numpy(), _AF3_SR)
            conversation = [{
                "role": "user",
                "content": [
                    {"type": "text", "text": self.caption_prompt},
                    {"type": "audio", "path": tmp},
                ],
            }]
            inputs = self.processor.apply_chat_template(
                conversation, tokenize=True, add_generation_prompt=True, return_dict=True,
            ).to(self.model.device)
            # The processor emits float32 audio features; the model is bf16. Cast the
            # floating-point tensors to match, leaving integer ids/masks untouched.
            for k, v in list(inputs.items()):
                if torch.is_tensor(v) and torch.is_floating_point(v):
                    inputs[k] = v.to(torch.bfloat16)
            out = self.model.generate(
                **inputs, do_sample=False, num_beams=self.num_beams,
                max_new_tokens=self.max_new_tokens,
            )
            text = self.processor.batch_decode(
                out[:, inputs["input_ids"].shape[1]:], skip_special_tokens=True,
            )[0]
            return text.strip()
        finally:
            os.unlink(tmp)
