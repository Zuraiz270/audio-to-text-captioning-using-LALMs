# Description and Discussion on DCASE 2026

## Extracted Abstract & Intro

DESCRIPTION AND DISCUSSION ON DCASE 2026 CHALLENGE TASK 4:
SPATIAL SEMANTIC SEGMENTATION OF SOUND SCENES
Masahiro Yasuda∗1, Binh Thien Nguyen∗1, Noboru Harada1, Romain Serizel2, Mayank Mishra2
Marc Delcroix1, Carlos Hernandez-Olivan1, Shoko Araki1
Daiki Takeuchi1, Tomohiro Nakatani1, Nobutaka Ono3
1NTT, Inc., Japan, masahiro.yasuda@ntt.com
2University de Lorraine, CNRS, Inria, Loria, France
3Tokyo Metropolitan University, Japan
ABSTRACT
This paper presents an overview of the Detection and Classifica-
tion of Acoustic Scenes and Events (DCASE) 2026 Challenge Task
4, Spatial Semantic Segmentation of Sound Scenes (S5). The S5
task focuses on the joint detection and separation of sound events
in complex spatial audio mixtures, contributing to the foundation
of immersive communication. First introduced in DCASE 2025,
the S5 task continues in DCASE 2026 Task 4 with key changes to
better reflect real-world conditions, including allowing mixtures to
contain multiple sources of the same class and to contain no tar-
get sources. In this paper, we describe task setting, along with the
corresponding updates to the evaluation metrics and dataset. The
experimental results of the submitted systems are also reported and
analyzed. The official access point for data and code ishttps://
github.com/nttcslab/dcase2026_task4_baseline.
Index Terms—Sound event detection and separation, Seman-
tic segmentation of sound scenes, Spatial signal, First-order am-
bisonics
1. INTRODUCTION
Spatial semantic segmentation of sound scenes (S5) refers to
the task of identifying and separating individual sound events from
complex spatial audio signals. It takes a multi-channel mixture as
input and produces a set of estimated single-channel source signals,
each associated with its corresponding sound event class label. S5
supports the development of technologies across a wide range of
applications, including immersive communication, extended reality
(XR) systems, and acoustic scene monitoring in smart and assisted
living environments.
Detection and Classification of Acoustic Scenes and Events
2025 Challenge Task 4 (DCASE25T4) marks the first challenge
to feature the S5 task, specifically focusing on indoor sound event
environments recorded using first-order Ambisonics microphone
arrays. Its baseline systems utilize a two-step strategy: first, an
audio tagging (AT) model identifies the source classes present in
the mixture; then, a label-queried source separation (LQSS) model
separates the corresponding audio signals. The dataset included a
This work was partially supported by JST Strategic International
Collaborative Research Program (SICORP), Grant Number JPMJSC2306,
Japan. This work was partially supported by the Agence Nationale de la
Recherche (Project Confluence, grant number ANR-23-EDIA-0003).
* These authors contributed equally to this work.
Input
Multi -channel spatial signal
S5
System
Speech
AlarmClockSpeechOutput
Separated signal and its class
(b) Overview of  S5 with same -