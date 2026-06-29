"""Pre-cache the `.venv` Hugging Face assets (CNN14 + AST rows) into the HF cache.

After this runs once with internet, set TRANSFORMERS_OFFLINE=1 to forbid network
calls during inference.
- CNN14: the captioning checkpoint stores BART decoder weights but not the BPE
  vocab or model config; both come from `facebook/bart-base` on the Hub.
- AST: the whole `MIT/ast-finetuned-audioset-10-10-0.4593` model + feature
  extractor come from the Hub (~350 MB).
(EnCLAP's assets live in `.venv-enclap`; cache those from that env separately.)
"""
from __future__ import annotations

import os

# HF defaults to a 10s read timeout, which is too tight for the ~558 MB
# model.safetensors served through the Xet bridge. Bump before importing.
os.environ.setdefault("HF_HUB_DOWNLOAD_TIMEOUT", "120")
os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")

from transformers import (  # noqa: E402
    ASTFeatureExtractor,
    ASTForAudioClassification,
    BartForConditionalGeneration,
    BartTokenizer,
)

BART_ID = "facebook/bart-base"
AST_ID = "MIT/ast-finetuned-audioset-10-10-0.4593"


def main() -> int:
    print(f"Caching tokenizer for {BART_ID} ...")
    BartTokenizer.from_pretrained(BART_ID)
    print(f"Caching model weights + config for {BART_ID} ...")
    BartForConditionalGeneration.from_pretrained(BART_ID)
    print(f"Caching feature extractor + model for {AST_ID} ...")
    ASTFeatureExtractor.from_pretrained(AST_ID)
    ASTForAudioClassification.from_pretrained(AST_ID)
    print("Done. Set TRANSFORMERS_OFFLINE=1 for subsequent runs to enforce offline use.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
