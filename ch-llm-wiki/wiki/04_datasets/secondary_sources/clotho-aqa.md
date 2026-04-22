# Clotho-AQA

## Extracted Abstract & Intro

Clotho-AQA: A Crowdsourced Dataset for Audio
Question Answering
Samuel Lipping, Parthasaarathy Sudarsanam, Konstantinos Drossos, Tuomas Virtanen
Audio Research Group, Tampere University, Tampere, Finland
fsamuel.lipping, parthasaarathy.ariyakulamsudarsanam, konstantinos.drossos, tuomas.virtanen g@tuni.ﬁ
Abstract —Audio question answering (AQA) is a multimodal
translation task where a system analyzes an audio signal and
a natural language question, to generate a desirable natural
language answer. In this paper, we introduce Clotho-AQA, a
dataset for Audio question answering consisting of 1991 audio
ﬁles each between 15 to 30 seconds duration selected from the
Clotho dataset. For each audio ﬁle, we collect six different
questions and corresponding answers by crowdsourcing using
Amazon Mechanical Turk. The questions and answers are pro-
duced by different annotators. Out of the six questions for each
audio, two questions each are designed to have ‘yes’ and ‘no’ as
answers, while the remaining two questions have other single-
word answers. For each question, we collect answers from three
different annotators. We also present two baseline experiments
to describe the usage of our dataset for the AQA task —
a Long short-term memory (LSTM) based multimodal binary
classiﬁer for ‘yes’ or ‘no’ type answers and an LSTM based
multimodal multi-class classiﬁer for 828 single-word answers.
The binary classiﬁer achieved an accuracy of 62.7% and the
multi-class classiﬁer achieved a top-1 accuracy of 54.2% and a
top-5 accuracy of 93.7%. Clotho-AQA dataset is freely available
online at https://zenodo.org/record/6473207.
Index Terms —audio question answering, Clotho-AQA, dataset
I. I NTRODUCTION
Question answering (QA) refers to task of providing natural
language answers to questions posed in natural language.
When a natural signal such as image or audio is used as
an auxiliary input, a question can also be targeted to the
their contents, leading to visual question answering or audio
question answering. The use of natural language enables
representing complex high-level information about the inputs
such as structure, repetitions and order of events in the
case of audio signals. Creating such a multimodal system to
answer the question requires inferring information about the
contents of the signal that are relevant to the question. Recent
advancements in deep learning has made it a suitable choice
to tackle these problems.
Question answering has been largely populated with datasets
outside audio with visual question answering [1–5], video
question answering [6–9], and textual question answering [10,
11]. Since most of these datasets contain real-world data (i.e.
not automatically generated), they have been annotated by
human annotators. Crowdsourcing is a convenient way to do
this and has been employed sucessfully in various question
answering datasets in modalities outside audio [3, 6, 10] as
well as other multimodal audio-to-text tasks [12, 13].To the authors knowle