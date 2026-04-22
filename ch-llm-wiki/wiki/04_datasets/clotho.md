# Clotho_an_Audio_Captioning_Dataset

## Extracted Abstract & Intro

CLOTHO: AN AUDIO CAPTIONING DATASET
Konstantinos Drossos, Samuel Lipping, and Tuomas Virtanen
Audio Research Group, Tampere University, Tampere, Finland
fﬁrstname.lastname g@tuni.ﬁ
ABSTRACT
Audio captioning is the novel task of general audio content
description using free text. It is an intermodal translation task
(not speech-to-text), where a system accepts as an input an au-
dio signal and outputs the textual description (i.e. the caption)
of that signal. In this paper we present Clotho, a dataset for
audio captioning consisting of 4981 audio samples of 15 to
30 seconds duration and 24 905 captions of eight to 20 words
length, and a baseline method to provide initial results. Clotho
is built with focus on audio content and caption diversity, and
the splits of the data are not hampering the training or evalua-
tion of methods. All sounds are from the Freesound platform,
and captions are crowdsourced using Amazon Mechanical
Turk and annotators from English speaking countries. Unique
words, named entities, and speech transcription are removed
with post-processing. Clotho is freely available online1.
Index Terms —audio captioning, dataset, Clotho
1. INTRODUCTION
Captioning is the intermodal translation task of describing
the human-perceived information in a medium, e.g. images
(image captioning) or audio (audio captioning), using free
text [ 1,2,3,4]. In particular, audio captioning was ﬁrst intro-
duced in [ 4], it does not involve speech transcription, and is
focusing on identifying the human-perceived information in
an general audio signal and expressing it through text, using
natural language. This information includes identiﬁcation of
sound events, acoustic scenes, spatiotemporal relationships of
sources, foreground versus background discrimination, con-
cepts, and physical properties of objects and environment. For
example, given an audio signal, an audio captioning system
would be able to generate captions like “a door creaks as it
slowly revolves back and forth”2.
The dataset used for training an audio captioning method
deﬁnes to a great extent what the method can learn [ 1,5].
The research leading to these results has received funding from the Eu-
ropean Research Council under the European Unions H2020 Framework
Programme through ERC Grant Agreement 637422 EVERYSOUND. Part of
the computations leading to these results were performed on a TITAN-X GPU
donated by NVIDIA to K. Drossos. The authors also wish to acknowledge
CSC-IT Center for Science, Finland, for computational resources.
1https://zenodo.org/record/3490684
2Actual caption from the training split of Clotho dataset.Diversity in captions allows the method to learn and exploit
the perceptual differences on the content (e.g. a thin plastic
rattling could be perceived as a ﬁre crackling) [ 1]. Also, the
evaluation of the method becomes more objective and general
by having more captions per audio signal [5].
Recently, two different datasets for audio captioning were
presented, Audio Capt