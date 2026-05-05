---
title: P1 Presentation Script
type: presentation
status: active
created: 2026-05-04
tags: [presentation, p1, script]
---

# P1 Presentation Script (May 4th)

**Time Limit**: 5 Minutes
**Slide Limit**: 5 Content Slides + 1 Reference Slide

## Slide 1: Topic Intro, Applications & Challenges
**Title**: Audio-to-Text Captioning: Tasks and Challenges
**Visuals**: A high-level diagram of AAC alongside bullet points for applications (Accessibility, Media Retrieval) and the core challenge of **polyphony**.
**Script (1 min)**:
- "Hello everyone. My project focuses on Automated Audio Captioning (AAC)."
- "Unlike simple audio tagging, captioning generates grammatical, natural-language sentences that capture temporal relations and spatial cues."
- "The applications are huge, like advanced audio search and accessibility for the deaf."
- "However, the primary challenge—and the core of my research—is **polyphony**. When multiple sound events overlap, current SOTA models tend to under-describe the scene or hallucinate entities that aren't there."

## Slide 2: Literature Search Methodology
**Title**: Literature Search & Selection Strategy
**Visuals**: A funnel diagram showing "Databases -> Keywords -> Shortlisting (49 Papers) -> 3 Main Streams".
**Script (1 min)**:
- "Before diving into the findings, I want to briefly explain how I built my 49-paper evidence base."
- "I searched IEEE Xplore, ACM, and arXiv using keyword combinations like 'Automated Audio Captioning' AND 'Large Audio-Language Models', alongside terms like 'Polyphony' and 'Hallucination'."
- "I shortlisted these 49 papers by strictly including research on multimodal architectures and evaluation metrics from 2024-2026, while explicitly excluding unrelated fields like speech recognition."
- "This rigorous process naturally categorized the literature into three main streams, which I'll cover next."

## Slide 3: Main Stream 1 - Traditional Baselines
**Title**: Literature: Traditional AAC Paradigms
**Visuals**: Logos or simple architecture blocks for CNN14, AST, EnCLAP.
**Script (1 min)**:
- "In reviewing the literature, the first main stream of research involves traditional baseline architectures."
- "These include the DCASE CNN14, which is the official gold standard for tagging, and Audio Spectrogram Transformers (AST)."
- "I'm also looking at bleeding-edge non-LLM models like EnCLAP, which uses contrastive audio-text learning without the heavy footprint of an LLM decoder."

## Slide 4: Main Stream 2 - The LALM Era
**Title**: Literature: State-of-the-Art LALMs
**Visuals**: Logos for Falcon3-Audio, SALMONN, Qwen2.5-Omni.
**Script (1 min)**:
- "The second, and current, stream of research is Large Audio-Language Models."
- "These models use an audio encoder fused directly with an LLM."
- "My primary evaluation targets here are Falcon3-Audio, which is heavily peer-reviewed, alongside models like SALMONN and Qwen2.5-Omni to see if their massive parameter counts actually solve the polyphony problem or just hide it behind fluent text."

## Slide 5: Main Stream 3 - Data Strategy & Metrics
**Title**: Literature: Evaluation, Datasets, and Metrics
**Visuals**: Logos/Equations for Clotho v2.1, SPIDEr-FL, and MACE.
**Script (1 min)**:
- "Finally, the literature on datasets and evaluation metrics is crucial."
- "I am explicitly utilizing the **Clotho v2.1** dataset rather than AudioCaps. This avoids the severe data leakage risks associated with AudioSet, and Clotho's 5 human-written captions per clip give us the necessary density to evaluate polyphony."
- "For metrics, I'll use the standard SPIDEr-FL, but my focus is on MACE (Metric for evaluating Audio Captioning Entities) to specifically quantify entity hallucination."
- "This will definitively measure if LALMs are hallucinating more than traditional systems when faced with overlapping sounds."

---

## Slide 6 (Additional): References
*(Leave this on screen during the 5-minute Q&A)*

**Title**: Top-10 Reference Shortlist
**Content**:
> [1] C. S. J. et al., "Beyond the Status Quo: A Survey on Audio Captioning," *IEEE/ACM Trans. Audio, Speech, Lang. Process.*, 2023.
> [2] Falcon3 Team, "Falcon3-Audio: An Open-Source Audio-Language Model," *ICASSP*, 2026.
> [3] EnCLAP Authors, "EnCLAP: Contrastive Learning for Audio-Text," 2024.
> [4] SLAM-LLM Authors, "SLAM-LLM: Speech and Audio LLM Framework," 2025.
> [5] K. Drossos et al., "Clotho: An Audio Captioning Dataset," *ICASSP*, 2020.
> [6] MACE Authors, "MACE: Metric for Evaluating Audio Captioning Entities," 2025.
> [7] Leakage Benchmark Authors, "Data Leakage in Audio-Language Models," 2026.
> [8] Hallucination Authors, "Reducing Entity Hallucination in Audio Captioning," 2026.
> [9] Audio-CoT Authors, "Audio-CoT: Chain-of-Thought Reasoning for Audio," 2026.
> [10] SED Authors, "A Review of Sound Event Detection," 2025.

---

## Anticipated Q&A (5 Minutes)
*Professor Abeßer expects you to defend your literature choices and methodology. Pre-plan your answers to these likely questions:*

**Q1: Why are you evaluating LALMs against traditional tagging models? How is that a fair comparison?**
> **A:** "It's a baseline parity check. Traditional models like CNN14 are the DCASE gold standard for detecting entities. If a massive, billion-parameter LALM cannot even detect the same overlapping acoustic entities as a lightweight CNN, its fluent text generation is just an illusion of understanding. We map the traditional tags to entities to make it comparable."

**Q2: You mentioned Clotho v2.1. Why not use AudioCaps since it has 46,000 clips?**
> **A:** "Two main reasons: Data Leakage and Caption Density. AudioCaps is built on AudioSet, which almost all LALMs have been pre-trained on, meaning 'zero-shot' tests would be contaminated. Clotho provides a safer out-of-domain test. Also, Clotho has 5 human captions per clip, which gives us the dense ground-truth needed to accurately measure polyphony and hallucination."

**Q3: How exactly do you define and separate 'Entity Hallucination' from 'Polyphony Under-description'?**
> **A:** "Polyphony under-description is an *omission* error—the model misses a background bird because a dog is barking loudly. Entity hallucination is an *insertion* error—the model claims there is a siren when there is only wind, often due to language-prior biases where it associates certain words together regardless of the audio."

**Q4: You have 49 papers but only listed 10 references. Why these 10?**
> **A:** "The 49 papers cover the broad context, but these 10 form the functional core of my methodology. They represent the exact dataset I'm using (Clotho), the specific metrics (MACE), the baseline paradigms (CNN14/EnCLAP), and the specific failure modes (hallucination) I'm testing."

**Q5: Why did you choose Falcon3-Audio as your primary evaluation target?**
> **A:** "Falcon3-Audio is an open-source, peer-reviewed model trained on clean, documented public data, making it an ideal primary target for an academic audit. Models like Qwen2.5-Omni or SALMONN are included to see if massive parameter scaling alone can brute-force a solution to polyphony."

**Q6: Could you just fine-tune an LALM on polyphonic audio instead of testing it zero-shot?**
> **A:** "Fine-tuning is a valid next step, but it's out of scope for this initial phase. My goal is to evaluate the *inherent* zero-shot capabilities and biases of these massive models. If we fine-tune them first, we risk masking their foundational flaws rather than understanding why they happen."

**Q7: What if we used proprietary API models like GPT-4o instead of open-source LALMs like Falcon3?**
> **A:** "Proprietary models are 'black boxes' which makes rigorous academic auditing impossible. Because their training data is hidden, we cannot perform a contamination audit to verify if they are truly acting zero-shot. Open-source LALMs guarantee reproducible, transparent results."

**Q8: Can you clarify the difference between SPIDEr-FL and MACE, and why SPIDEr-FL isn't enough?**
> **A:** "SPIDEr-FL measures overall n-gram overlap and fluency. It's great for sentence quality but poor at penalizing specific factual errors. MACE specifically isolates and counts *entities* (nouns/events). A caption might be highly fluent (high SPIDEr) but confidently hallucinate a dog (low MACE). We need MACE to specifically audit hallucination."
