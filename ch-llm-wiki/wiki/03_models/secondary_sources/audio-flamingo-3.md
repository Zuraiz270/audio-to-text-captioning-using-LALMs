# Audio Flamingo 3

## Extracted Abstract & Intro

Audio Flamingo 3: Advancing Audio Intelligence
with Fully Open Large Audio Language Models
Arushi Goel★1, Sreyan Ghosh★12, Jaehyeon Kim1, Sonal Kumar2, Zhifeng Kong1, Sang-gil Lee1,
Chao-Han Huck Yang1,Ramani Duraiswami2,Dinesh Manocha2,Rafael Valle1,Bryan Catanzaro1
NVIDIA, USA1, University of Maryland, College Park, USA2
★Equal contribution. Alphabetically ordered.
Correspondence: arushig@nvidia.com, sreyang@umd.edu
Project: https://research.nvidia.com/labs/adlr/AF3/
Abstract
We present Audio Flamingo 3 (AF3), a fully open state-of-the-art (SOTA) large
audio-language model that advances reasoning and understanding across speech,
sound, and music. AF3 introduces: (i) AF-Whisper, a unified audio encoder trained
using a novel strategy for joint representation learning across all 3 modalities of
speech, sound, and music; (ii) flexible, on-demand thinking, allowing the model
to do chain-of-thought-type reasoning before answering; (iii) multi-turn, multi-
audio chat; (iv) long audio understanding and reasoning (including speech) up
to 10 minutes; and (v) voice-to-voice interaction. To enable these capabilities,
we propose several large-scale training datasets curated using novel strategies,
including AudioSkills-XL, LongAudio-XL, AF-Think, and AF-Chat, and train
AF3 with a novel five-stage curriculum-based training strategy. Trained on only
open-source audio data, AF3 achieves new SOTA results on over 20+ (long) audio
understanding and reasoning benchmarks, surpassing both open-weight and closed-
source models trained on much larger datasets.
1 Introduction
MMAU
(avg.)MMSU
(avg.)NSynth Inst.
CMM
ClothoAQA
(unan.)
Libri
(Clean)
SPGI
OpenAudioBench
(alpaca)LongAudioBench70% 80% 90% 100%Audio Flamingo 3
Previous SOTA (Open Source)
Previous SOTA (Closed Source)
Figure 1: AF3 vs. prior SOTA LALMs (values
normalized and WER=100-WER). AF3 outper-
forms most open-source/weights (e.g., Qwen2.5-
Omni) and closed (e.g., Gemini 2.5 Pro) LALMs
while being fully open.Audio—including speech, sounds, and music—is cen-
tral to human perception and interaction. It enables
us to understand our surroundings, engage in conver-
sations, express emotions, interpret videos, and enjoy
music. For AI systems to approach artificial general
intelligence (AGI) [ 88], they must similarly develop the
ability to comprehend and reason over diverse audio sig-
nals. While Large Language Models (LLMs) excel at
language-based reasoning, their audio comprehension
remains limited — both in accessibility and capabil-
ity [54,106]. Extending LLMs to process and reason
over audio is essential for building truly context-aware,
intelligent agents.
Audio-Language Models (ALMs) extend the capabil-
ities of LMs to the auditory domain. Early works such
as CLAP [ 33] align audio and text in a shared embed-
ding space, enabling them with tasks like retrieval [ 89].
Preprint. Under review.arXiv:2507.08128v2  [cs.SD]  28 Jul 2025
Models Audio Understanding Voice Multi-turn Chat Long Audio ( >30 secs) O