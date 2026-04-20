---
type: abstract-snapshot
source: arXiv 1910.09387
retrieved: 2026-04-20
status: abstract-only
---

# Clotho v1 — Abstract Snapshot

**Title:** Clotho: An Audio Captioning Dataset
**Authors:** Konstantinos Drossos, Samuel Lipping, Tuomas Virtanen
**Affiliation:** Tampere University
**arXiv ID:** 1910.09387 (Oct 2019); ICASSP 2020
**Venue:** ICASSP 2020
**Source URL:** https://arxiv.org/abs/1910.09387

## Abstract (verbatim, condensed)

Audio captioning is the novel task of general audio content description using free text. It is an intermodal translation task (not speech-to-text), where a system accepts as an input an audio signal and outputs the textual description (i.e. the caption) of that signal. In this paper we present Clotho, a dataset for audio captioning consisting of 4981 audio samples of 15 to 30 seconds duration and 24 905 captions of eight to 20 words length. There is a balance of gender of annotators, no speech in the audio samples, and a balance of frequencies of words in captions. We employ a three-step framework for crafting the dataset, focusing on diversity, content, and accuracy of the captions. We also present the results of a baseline method that has been employed for benchmarking the dataset.

## Key facts

- 4,981 audio samples, 15–30 s
- 24,905 captions (5 per clip), 8–20 words
- No speech in audio
- Three-step caption-crafting framework
- Annotation gender-balanced
- Source audio: Freesound

## Versions

- v1 (this paper): ICASSP 2020
- v2 / v2.1 (project-relevant): DCASE-2020/2021 expansion
- v2.1 Zenodo DOI: **4783391** (NOT 3490684 — earlier draft error)

## Project notes

- Eval split is the canonical DCASE 2024 Task 6 baseline target (29.6% SPIDEr-FL).
- RQ0 contamination check: AF3 training manifest × Clotho v2.1 eval IDs.
- Referenced across RQ1, RQ2, RQ4.
