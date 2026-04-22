# SALMONN

## Extracted Abstract & Intro

Published as a conference paper at ICLR 2024
SALMONN: T OWARDS GENERIC HEARING ABILI-
TIES FOR LARGE LANGUAGE MODELS
Changli Tang1∗, Wenyi Yu1∗, Guangzhi Sun1, Xianzhao Chen2, Tian Tan2
Wei Li2,Lu Lu2,Zejun Ma2,Chao Zhang1†
Department of Electronic Engineering, Tsinghua University1
ByteDance2
{tcl20,ywy22 }@mails.tsinghua.edu.cn, cz277@tsinghua.edu.cn
ABSTRACT
Hearing is arguably an essential ability of artificial intelligence (AI) agents in the
physical world, which refers to the perception and understanding of general audi-
tory information consisting of at least three types of sounds: speech, audio events,
and music. In this paper, we propose SALMONN, a speech audio language music
open neural network, built by integrating a pre-trained text-based large language
model (LLM) with speech and audio encoders into a single multimodal model.
SALMONN enables the LLM to directly process and understand general audio in-
puts and achieve competitive performances on a number of speech and audio tasks
used in training, such as automatic speech recognition and translation, auditory-
information-based question answering, emotion recognition, speaker verification,
and music and audio captioning etc.SALMONN also has a diverse set of emer-
gent abilities unseen in the training, which includes but is not limited to speech
translation to untrained languages, speech-based slot filling, spoken-query-based
question answering, audio-based storytelling, and speech audio co-reasoning etc.
The presence of cross-modal emergent abilities is studied, and a novel few-shot ac-
tivation tuning approach is proposed to activate such abilities. To our knowledge,
SALMONN is the first model of its type and can be regarded as a step towards AI
with generic hearing abilities. The source code, model checkpoints and data are
available at https://github.com/bytedance/SALMONN .
1 I NTRODUCTION
Text-based large language models (LLMs) (Brown et al., 2020; Touvron et al., 2023; Chiang et al.,
2023; Anil et al., 2023; Du et al., 2022) have demonstrated remarkable and even human-level perfor-
mance in many natural language processing (NLP) tasks (OpenAI, 2023). Meanwhile, instruction
tuning (Wei et al., 2022a; Chung et al., 2022; Ouyang et al., 2022; Peng et al., 2023), where data is
organised as pairs of user instruction (or prompt) and reference response, has emerged as an LLM
training paradigm that allows LLMs to follow open-ended user instructions. There is a burgeoning
research interest in empowering LLMs with multimodal perception abilities. Recent studies focus
on connecting LLMs with either the encoder of one additional type of input, such as image (Li et al.,
2023a; Alayrac et al., 2022; Dai et al., 2023), silent video (Maaz et al., 2023; Chen et al., 2023b;
Zhao et al., 2022), audio events (Gong et al., 2023b; Lyu et al., 2023) or speech (Chen et al., 2023a),
or the encoders of multiple input types together (Su et al., 2023; Zhang et al., 2023b). A connection
module and LLM adaptor