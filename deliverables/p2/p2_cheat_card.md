# P2 Cheat Card — print, fold, keep in pocket

## The dataset choice in one sentence

**Clotho v2.1 — DCASE Task 6 official, 5 captions per clip, FreeSound-sourced (not AudioSet) — lower contamination risk than every alternative.**

## Five facts to remember

1. **Clotho v2.1** — 44.1 kHz mono WAV, 15–30 s clips, 5 captions of 8–20 words each, CC-BY 4.0 on Zenodo (record 4783391).
2. **Weak labels** — clip-level captions, no time-stamps. Strong (segment-level) labels are *derived* via PaSST/PANNs SED.
3. **Under-description test** — clip is under-described iff `card(E_model) < card(E_ref ∩ E_audio)`.
4. **Polyphony bucket** — ≥ 2 simultaneous AudioSet classes for ≥ 1 s, conf ≥ 0.5.
5. **DCASE 2024 baseline** — SPIDEr-FL ≈ 29.6 %. Our reference.

## Five things to repeat out loud

- "**Clotho v2.1, FreeSound-sourced, CC-BY 4.0, fully FAIR.**"
- "**Five captions per clip, 8 to 20 words each.**"
- "**Weak annotation — pseudo-strong labels derived via PaSST.**"
- "**Three-layer audit, per LALM, not aggregated.**"
- "**Falcon3-Audio's manifest is public — its key sell.**"

## Three rejections — in one breath each

- **AudioCaps**: AudioSet-derived → contamination. *FD-DeCap reports 0.282 SPIDEr on Clotho vs. 0.429 on AudioCaps — even after debiasing the contaminated corpus scores 50 % higher.*
- **WavCaps**: 400 K web-scraped clips with LLM-generated captions, and its FreeSound sub-source overlaps Clotho directly.
- **Cacophony**: contrastive *training* corpus (13 K hours), not an evaluation benchmark.

## The two P1 commitments I close on slide 5

- **Risk to Watch** (contamination) → closed via the three-layer audit.
- **Open Question** (do the 3 LALMs fail polyphony the same way?) → drives **per-model** audit reporting, not aggregated.

## Nine short Q&A reflexes

1. *Why Clotho not AudioCaps?* → DCASE official · 5 captions · less contaminated. **0.282 vs 0.429 SPIDEr gap.**
2. *Which mics?* → All of them. FreeSound contributors. Device mismatch is built-in.
3. *Why no recording?* → Zero-shot protocol. Pretrained weights only.
4. *Weak or strong labels?* → Weak. Pseudo-strong derived via PaSST.
5. *Polyphony threshold?* → ≥ 2 classes, ≥ 1 s, conf ≥ 0.5.
6. *If Falcon3 manifest closed?* → It is not. Public manifest is its key sell.
7. *If SALMONN / Qwen manifests closed?* → Fall back to audio fingerprinting + text overlap.
8. *"All team members shall present"?* → Solo project, Mat. 2177213.
9. *Synonym variance ("rain" vs "water drops")?* → SPIDEr metric handles semantics; PaSST tagger maps to a fixed taxonomy.

## If you freeze

> "Clotho v2.1 is FreeSound-sourced, has five captions per clip, and avoids the AudioSet contamination that breaks the zero-shot claim on AudioCaps. The next eight weeks: audit, polyphony split, inference, metrics."

## Last 10 seconds

> "Thank you. I am happy to take your questions."
