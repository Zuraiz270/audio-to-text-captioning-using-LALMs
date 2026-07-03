"""Qwen2.5-Omni captioner (Alibaba) — GPU-cluster LALM row.

Qwen2.5-Omni is a multimodal (text / vision / audio / speech) model. We use it
audio-only with text-only output (the speech "talker" is disabled to save VRAM).
It slots into the same Captioner contract as every other row.

Needs a recent transformers (>=4.52) plus `qwen-omni-utils`, so it runs in its own
environment on the cluster (see requirements-qwen.txt). All heavy imports are lazy
so importing the model registry stays cheap in the CPU/other envs.
"""
from __future__ import annotations

import os
import tempfile

import soundfile as sf
import torch

from src.models.base import Captioner

_SYSTEM = (
    "You are Qwen, a virtual human developed by the Qwen Team, Alibaba Group, "
    "capable of perceiving auditory and visual inputs, as well as generating text "
    "and speech."
)


def _lazy_imports():
    from transformers import Qwen2_5OmniForConditionalGeneration, Qwen2_5OmniProcessor
    from qwen_omni_utils import process_mm_info
    return Qwen2_5OmniForConditionalGeneration, Qwen2_5OmniProcessor, process_mm_info


class QwenOmniCaptioner(Captioner):
    def __init__(
        self,
        model_id: str = "Qwen/Qwen2.5-Omni-7B",
        device: str = "cuda",
        num_beams: int = 1,
        max_new_tokens: int = 64,
        caption_prompt: str = "Describe the audio in one sentence.",
    ) -> None:
        Model, Processor, process_mm_info = _lazy_imports()
        self._process_mm_info = process_mm_info
        self.num_beams = num_beams
        self.max_new_tokens = max_new_tokens
        self.caption_prompt = caption_prompt

        self.model = Model.from_pretrained(
            model_id, torch_dtype=torch.bfloat16, device_map="auto"
        )
        if hasattr(self.model, "disable_talker"):
            self.model.disable_talker()  # text-only output, frees VRAM
        self.processor = Processor.from_pretrained(model_id)

    @torch.inference_mode()
    def caption(self, waveform: torch.Tensor, sample_rate: int = 44_100) -> str:
        audio = waveform.squeeze(0).to(torch.float32).cpu().numpy()
        # qwen_omni_utils loads audio from a path; write a short-lived temp WAV.
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf:
            tmp = tf.name
        try:
            sf.write(tmp, audio, sample_rate)
            conversation = [
                {"role": "system", "content": [{"type": "text", "text": _SYSTEM}]},
                {"role": "user", "content": [
                    {"type": "audio", "audio": tmp},
                    {"type": "text", "text": self.caption_prompt},
                ]},
            ]
            text = self.processor.apply_chat_template(
                conversation, add_generation_prompt=True, tokenize=False
            )
            audios, images, videos = self._process_mm_info(
                conversation, use_audio_in_video=False
            )
            inputs = self.processor(
                text=text, audio=audios, images=images, videos=videos,
                return_tensors="pt", padding=True,
            ).to(self.model.device)
            out = self.model.generate(
                **inputs, return_audio=False, do_sample=False,
                num_beams=self.num_beams, max_new_tokens=self.max_new_tokens,
            )
            gen = out[:, inputs["input_ids"].shape[1]:]
            txt = self.processor.batch_decode(
                gen, skip_special_tokens=True, clean_up_tokenization_spaces=False
            )[0]
            return txt.strip()
        finally:
            os.unlink(tmp)
