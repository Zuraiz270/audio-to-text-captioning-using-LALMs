"""AST tagging baseline — the pure-audio *tagging* floor for RQ1.

`MIT/ast-finetuned-audioset-10-10-0.4593` (Gong et al., 2021) is an Audio
Spectrogram Transformer that classifies audio into the 527 AudioSet labels — it
is NOT a captioner. To place it in the captioning table we take its top-k tags
and wrap them in a minimal template sentence, then score that with the same
metrics. The expected result is a LOW SPIDEr, *below* the real captioners
(CNN14, EnCLAP): that gap is the finding ("naming events ≠ describing scenes").

AST ships inside `transformers`, so this runs in the CNN14 `.venv` — no vendored
repo, no separate env, no downloaded weights (just the HF model cache).

Limitations (defensible, documented):
- AST truncates to ~10.24 s, so it only "hears" the first ~10 s of each clip.
- AudioSet is multi-label, so we rank by sigmoid probability and take top-k.
"""
from __future__ import annotations

import re

import torch
import torchaudio.functional as AF
from transformers import ASTFeatureExtractor, ASTForAudioClassification

from src.models.base import Captioner

_AST_SR = 16_000  # AST's required input sample rate


def _clean(label: str) -> str:
    """AudioSet label -> caption word: drop parentheticals, lowercase.

    e.g. "Wind noise (microphone)" -> "wind noise"; "Speech" -> "speech".
    """
    return re.sub(r"\s*\([^)]*\)", "", label).strip().lower()


class ASTTaggingCaptioner(Captioner):
    def __init__(
        self,
        model_id: str = "MIT/ast-finetuned-audioset-10-10-0.4593",
        device: str = "cpu",
        top_k: int = 5,
        revision: str | None = None,
    ) -> None:
        self.device = torch.device(device)
        self.top_k = top_k
        self.feature_extractor = ASTFeatureExtractor.from_pretrained(model_id, revision=revision)
        self.model = (
            ASTForAudioClassification.from_pretrained(model_id, revision=revision)
            .to(self.device)
            .eval()
        )
        self.id2label = self.model.config.id2label

    @torch.inference_mode()
    def caption(self, waveform: torch.Tensor, sample_rate: int = 44_100) -> str:
        audio = waveform.squeeze(0).to(torch.float32)
        if sample_rate != _AST_SR:
            audio = AF.resample(audio, sample_rate, _AST_SR)

        inputs = self.feature_extractor(
            audio.numpy(), sampling_rate=_AST_SR, return_tensors="pt"
        )
        logits = self.model(inputs.input_values.to(self.device)).logits[0]
        # AudioSet is multi-label -> sigmoid + top-k, not argmax.
        probs = torch.sigmoid(logits)
        top_idx = torch.topk(probs, self.top_k).indices.tolist()

        tags: list[str] = []
        seen: set[str] = set()
        for i in top_idx:
            tag = _clean(self.id2label[i])
            if tag and tag not in seen:
                seen.add(tag)
                tags.append(tag)

        if not tags:
            return "a sound"
        if len(tags) == 1:
            return f"a sound of {tags[0]}"
        return f"a sound of {', '.join(tags[:-1])} and {tags[-1]}"
