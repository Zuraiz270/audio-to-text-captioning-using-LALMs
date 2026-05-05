---
title: Literature Search Strategy
type: methodology
status: active
created: 2026-05-04
tags: [literature, methodology, keywords, search]
---

# Literature Search Strategy

## Purpose
To document the systematic literature review process used to arrive at the 49-paper evidence matrix for this project.

## 1. Search Strategy & Keywords

The literature search was conducted across primary academic databases including **IEEE Xplore**, **ACM Digital Library**, **Google Scholar**, and **arXiv** (for bleeding-edge preprints in the fast-moving LALM space).

### Primary Keyword Combinations
The search utilized boolean combinations of the following core concepts:
- **Task Definition**: `"Automated Audio Captioning"` OR `"Audio Captioning"` OR `"AAC"`
- **Architecture**: `"Large Audio-Language Models"` OR `"LALM"` OR `"Audio-LLM"` OR `"Audio Encoder-LLM"`
- **Failure Modes**: `"Polyphony"` OR `"Sound Event Overlap"` OR `"Audio Hallucination"` OR `"Entity Hallucination"`
- **Benchmarks**: `"DCASE Task 6"` OR `"Clotho"` OR `"AudioCaps"`

*Example Query*: `("Automated Audio Captioning" OR "AAC") AND ("Large Audio-Language Models" OR "Hallucination")`

## 2. Shortlisting Criteria (How 49 Papers Were Selected)

An initial sweep yielded hundreds of papers. The 49-paper evidence base was distilled using the following inclusion/exclusion criteria:

### Inclusion Criteria
1. **Direct Relevance**: Must specifically address audio captioning, evaluation metrics (like MACE/SPIDEr), or multimodal audio-text architectures.
2. **Temporal Relevance**: High priority given to papers published between 2024–2026 to capture the current state-of-the-art LALM explosion. Foundational baselines (like Clotho/CNN14) from 2020–2023 were retained for historical context.
3. **Task Parity**: Papers evaluating overlapping sound events (polyphony) and zero-shot reasoning.

### Exclusion Criteria
1. **Out of Scope Tasks**: Papers purely focused on Automatic Speech Recognition (ASR), Music Generation, or Text-to-Speech (TTS) were excluded.
2. **Redundancy**: Minor incremental papers that did not shift the architectural paradigm or propose a new evaluation metric were filtered out.

## 3. Categorization into Streams
The final 49 papers were then tagged and categorized into three main streams for analysis:
1. Traditional AAC Baselines
2. State-of-the-Art LALMs
3. Evaluation Metrics & Failure Modes (Hallucination/Polyphony)
