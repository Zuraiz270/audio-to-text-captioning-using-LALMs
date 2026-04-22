# AudioCaps

## Extracted Abstract & Intro

Proceedings of NAACL-HLT 2019 , pages 119–132
Minneapolis, Minnesota, June 2 - June 7, 2019. c2019 Association for Computational Linguistics119AudioCaps : Generating Captions for Audios in The Wild
Chris Dongjoo Kim Byeongchang Kim Hyunmin Lee Gunhee Kim
Department of Computer Science and Engineering & Center for Superintelligence
Seoul National University, Seoul, Korea
fcdjkim,byeongchang.kim g@vision.snu.ac.kr flhm1442,gunhee g@snu.ac.kr
Abstract
We explore the problem of audio caption-
ing1: generating natural language description
for any kind of audio in the wild, which has
been surprisingly unexplored in previous re-
search. We contribute a large-scale dataset of
46K audio clips with human-written text pairs
collected via crowdsourcing on the AudioSet
dataset (Gemmeke et al., 2017). Our thorough
empirical studies not only show that our col-
lected captions are indeed loyal to the audio
inputs but also discover what forms of audio
representation and captioning models are ef-
fective for audio captioning. From extensive
experiments, we also propose two novel com-
ponents that are integrable with any attention-
based captioning model to help improve audio
captioning performance: the top-down multi-
scale encoder and aligned semantic attention.
1 Introduction
Captioning , the task of translating a multimedia
input source into natural language, has been sub-
stantially studied over the past few years. The vast
majority of the journey has been through the vi-
sual senses ranging from static images to videos.
Yet, the exploration into the auditory sense has
been circumscribed to human speech transcrip-
tion (Panayotov et al., 2015; Nagrani et al., 2017),
leaving the basic natural form of sound in an un-
charted territory of the captioning research.
Recently, sound event detection has gained
much attention such as DCASE challenges
(Mesaros et al., 2017) along with the release of
a large scale AudioSet dataset (Gemmeke et al.,
2017). However, sound classiﬁcation ( e.g. pre-
dicting multiple labels for a given sound) and
event detection ( e.g. localizing the sound of in-
terest in a clip) may not be sufﬁcient for a full un-
derstanding of the sound. Instead, a natural sen-
1For a live demo and details, https://audiocaps.github.io
[Audio Classification]rumble | vehicle | speech | car | outside[Video Captioning]A bus passing by with some people walking by in the afternoon.[Audio Captioning]A muffled rumble with man and woman talking in the background while a siren blares in the distance.
Figure 1: Comparison of audio captioning with audio
classiﬁcation and video captioning tasks.
tence offers a greater freedom to express a sound,
because it allows to characterize objects along
with their states, properties, actions and interac-
tions. For example, suppose that suddenly sirens
are ringing in the downtown area. As a natural re-
action, people may notice the presence of an emer-
gency vehicle, even though they are unable to see
any ﬂashing lights nor feel