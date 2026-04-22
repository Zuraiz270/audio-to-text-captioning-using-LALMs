# Audio Flamingo Next

## Extracted Abstract & Intro

2026-4-14
Audio Flamingo Next: Next-Generation
Open Audio-Language Models for Speech,
Sound, and Music
Sreyan Ghosh1,2,∗Arushi Goel1,∗Kaousheik Jayakumar2Lasha Koroshinadze2
Nishit Anand2Zhifeng Kong1Siddharth Gururani1Sang-gil Lee1Jaehyeon Kim1
Aya Aljafari1Chao-Han Huck Yang1Sungwon Kim1Ramani Duraiswami2
Dinesh Manocha2Mohammad Shoeybi1Bryan Catanzaro1Ming-Yu Liu1Wei Ping1
1NVIDIA, USA2University of Maryland, USA
∗Project-Leads. Ordering was decided with a coin toss.
Code Model Project Page
Abstract.We present Audio Flamingo Next (AF-Next), the next-generation and most capable large audio-
language model in the Audio Flamingo series, designed to advance understanding and reasoning over speech,
environmental sounds, and music. Compared to Audio Flamingo 3, AF-Next introduces: (i) a stronger
foundational audio–language model that significantly improves accuracy across diverse audio understanding
tasks; (ii) scalable strategies for constructing large-scale audio understanding and reasoning data beyond
existing academic benchmarks; (iii) support for long and complex audio inputs up to 30 minutes; and (iv)
Temporal Audio Chain-of-Thought, a new reasoning paradigm that explicitly grounds intermediate reasoning
steps to timestamps in long audio, enabling fine-grained temporal alignment and improved interpretability.
To enable these capabilities, we first conduct a systematic analysis of Audio Flamingo 3 to identify key gaps in
audio understanding and reasoning. We then curate and scale new large-scale datasets totaling over 1 million
hours to address these limitations and expand the existing AudioSkills-XL, LongAudio-XL, AF-Think, and
AF-Chat datasets. AF-Next is trained using a curriculum-based strategy spanning pre-training, mid-training,
and post-training stages. Extensive experiments across 20 audio understanding and reasoning benchmarks,
including challenging long-audio tasks, show that AF-Next outperforms similarly sized open models by large
margins and remains highly competitive with, and sometimes surpasses, much larger open-weight and closed
models. Beyond benchmark performance, AF-Next exhibits strong real-world utility and transfers well to
unseen tasks, highlighting its robustness and generalization ability. In addition to all data, code, and methods,
we open-source 3 variants of AF-Next, including AF-Next-Instruct, AF-Next-Think, and AF-Next-Captioner,
meant for QA, advanced reasoning, and detailed captioning, respectively.
1. Introduction
Audio, spanning speech, environmental sounds, and music, is central to how humans perceive and in-
teract with the world. Robust audio understanding enables core capabilities such as conversation, sit-
uational awareness, and music listening, and underpins applications including automatic speech recog-
nition (ASR), audio captioning, and music information retrieval (MIR). Historically, these problems
were studied in isolation using small, task-specific models (Peng et al., 2026; Heydari and Duan, 2021)