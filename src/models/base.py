"""Abstract Captioner contract.

Every model row in the comparison table (CNN14, AST, EnCLAP, SALMONN,
Falcon3-Audio, Qwen2.5-Omni, ...) implements .caption(waveform, sample_rate)
and returns a single natural-language string. The predictions JSON schema
downstream assumes exactly that shape.
"""
from __future__ import annotations

import abc

import torch


class Captioner(abc.ABC):
    @abc.abstractmethod
    def caption(self, waveform: torch.Tensor, sample_rate: int) -> str:
        """Return a single caption for the given mono waveform.

        Args:
            waveform: shape (1, T), float32, mono.
            sample_rate: integer sample rate of the waveform in Hz.
        """
        raise NotImplementedError
