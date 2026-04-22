# Audio Flamingo 2

## Extracted Abstract & Intro

Audio Flamingo 2: An Audio-Language Model with Long-Audio
Understanding and Expert Reasoning Abilities
Sreyan Ghosh* 1 2Zhifeng Kong1Sonal Kumar2S Sakshi2Jaehyeon Kim1Wei Ping1Rafael Valle1
Dinesh Manocha2Bryan Catanzaro1
Abstract
Understanding and reasoning over non-speech
sounds and music are crucial for both humans
and AI agents to interact effectively with their
environments. In this paper, we introduce Audio
Flamingo 2 (AF2), an Audio-Language Model
(ALM) with advanced audio understanding and
reasoning capabilities. AF2 leverages (i) a cus-
tom CLAP model, (ii) synthetic Audio QA data
for fine-grained audio reasoning, and (iii) a multi-
stage curriculum learning strategy. AF2 achieves
state-of-the-art performance with only a 3B pa-
rameter small language model, surpassing large
open-source and proprietary models across over
20 benchmarks. Next, for the first time, we extend
audio understanding to long audio segments (30
secs to 5 mins) and propose LongAudio , a large
and novel dataset for training ALMs on long audio
captioning and question-answering tasks. Fine-
tuning AF2 on LongAudio leads to exceptional
performance on our proposed LongAudioBench ,
an expert annotated benchmark for evaluating
ALMs on long audio understanding capabilities.
We conduct extensive ablation studies to con-
firm the efficacy of our approach. Project Web-
site: https://research.nvidia.com/
labs/adlr/AF2/
1. Introduction
Understanding non-speech sounds, non-verbal speech, and
music (collectively referred to as “audio” in this paper)
is essential for real-world applications such as detecting
anomalies in industrial environments, recognizing emo-
tional cues, and improving assistive technologies for the
impaired. While Large Language Models (LLMs) have
*Work done during an internship at NVIDIA.1NVIDIA, Santa
Clara, CA, USA2University of Maryland, College Park, MD, USA.
Correspondence to: Sreyan Ghosh <sreyang@umd.edu >, Zhifeng
Kong<zkong@nvidia.com >.
Preliminary work. Under review. Copyright 2025 by the author(s).
ClothoAQAAudio Entailment
ClothoAudio Entailment
AudioCaps
Medley-Solos DB
MMAU
Music
MMAU
Sound
MuchoMusic
CompA-R-test
LongAudioBench
(ours)OpenAQACREMA-D20% 40% 60% 80%AudioCapsAudioFlamingo 2
100%
Previous SOTAFigure 1: Audio Flamingo 2 versus previous SOTA ALMs on au-
dio understanding and reasoning benchmarks (values normalized).
AF2 outperforms all baselines and has smaller model footprints.
demonstrated remarkable reasoning capabilities through lan-
guage, extending these systems to comprehend audio is
key to building intelligent systems capable of reasoning
with contextual auditory cues (Kong et al., 2024). Verbal
speech, inherently tied to language, benefits significantly
from (L)LM advancements (Watanabe et al., 2018; Chen
et al., 2024a); however, the potential to enhance perception
and reasoning over non-verbal audio remains largely under-
explored (Ghosh et al., 2024c). Audio-Language Models
(ALMs) extend language models with audio understand