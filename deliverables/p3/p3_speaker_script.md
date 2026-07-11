# P3 Speaker Script — 10 minutes (13 July 2026)

Target pace: ~135 words/minute. Times are cumulative targets at the END of each
slide. If running over at slide 6, compress slide 8 to its first and second
cards only; never cut slide 9.

---

## Slide 1 — Title (0:40)

Good morning. My project asks a simple question: can the new generation of
large audio-language models describe audio as well as systems that were
trained specifically for audio captioning? The short answer is on the right of
the slide. The best zero-shot model reaches 0.297 SPIDEr-FL on Clotho, which
is above both trained baselines I reproduced. The next ten minutes explain
what that number means, where it holds, and where it breaks down.

## Slide 2 — Task and research questions (1:50)

The course task is T6: audio-to-text captioning with LALMs, with a focus on
overlapping, polyphonic sound. I compare six systems under one harness. On the
traditional side: AST as a pure tagging floor, and two trained captioners,
the DCASE 2023 CNN14 baseline and EnCLAP-base, both trained on Clotho. On the
LALM side: Qwen2.5-Omni as a general omni-model, SALMONN-13B as an earlier
audio specialist, and NVIDIA's Audio Flamingo 3 as the current state of the
art. Three vendors, so it is not a single-vendor story. Three research
questions: do zero-shot LALMs match trained captioners; what happens on
polyphonic versus monophonic clips; and how much do the captions hallucinate.
All four hypotheses were committed in advance, with bootstrap statistics and
Holm correction.

## Slide 3 — Method (3:00)

Every system implements one contract: caption in, waveform and sample rate,
caption out. One inference loop and one scorer serve everything from a CPU
baseline to a 13-billion-parameter model on an A100. Each run writes a
manifest with checkpoint hashes, library versions, decode settings, and the
seed, so every number traces to a file. Three facts give the harness
credibility. First, it reproduces the official CNN14 baseline at 0.259 against
0.261 published, within 0.002. Second, the LALMs ran on offline cluster nodes
from pre-cached checkpoints with a fixed one-line prompt, recorded per run.
Third, all six systems completed all 1,045 evaluation clips with zero
failures. Baselines ran on my laptop, LALMs on the TinyGPU cluster; only the
compute location moves, the measurement never changes.

## Slide 4 — RQ1 (4:30)

Here is the headline. The answer to RQ1 is not yes or no; it depends on the
model. Every LALM clears the tagging floor by a factor of three to four, so
they all genuinely describe rather than list. But Qwen and SALMONN stay below
both trained captioners, so the claim that zero-shot LALMs beat trained
systems is false in general. Audio Flamingo 3 is the exception: it beats both
trained captioners on every metric, and its 0.297 is also above EnCLAP's
published SPIDEr-FL of 0.291. Hypothesis one is significant: the confidence
interval's lower bound is 0.283, clearly above the 0.261 anchor. Hypothesis
three as well: paired per clip, AF3 is 0.072 above SALMONN. One disclosure,
bottom right: my EnCLAP reproduction runs about one point below its published
anchor. That is in the paper, openly, and H1 is anchored on CNN14, which
reproduces almost exactly.

## Slide 5 — Captions (5:30)

Numbers aside, this is what the systems actually say, verbatim, for one clip.
The human reference describes people walking, voices, soft music. AST gives a
tag list, not a sentence. Qwen wraps everything in report language, "the audio
contains", which no Clotho reference ever uses, and it enumerates several
events. SALMONN and the trained models produce short declaratives. Audio
Flamingo 3 reads closest to the Clotho register, and that is exactly what
overlap metrics reward. But look at the red word: a zipper. Fluent, specific,
and supported by neither the references nor the audio tags. Keep that zipper
in mind; it is the bridge to the hallucination question.

## Slide 6 — RQ2 (7:00)

For polyphony I split the 1,045 clips with sound event detection: a clip is
polyphonic if two AudioSet classes are simultaneously active for at least one
second. The preregistered threshold of 0.5 turned out degenerate, so the
pre-committed fallback rule selected 0.25, giving 336 polyphonic and 709
monophonic clips. The result surprised me: every system scores higher on the
polyphonic subset. Hypothesis two is formally supported for all three LALMs,
but the baselines shift by the same amount, so this is a property of the data,
not of the LALMs. Event-rich clips give captions more content to match, while
the monophonic bucket collects quiet, ambiguous recordings. The audio-grounded
MACE metric shows the same direction, so it is not an artefact of reference
overlap. And this connects directly to Professor Abeßer's and Harish's DCASE
paper: at the event level, tagging and counting degrade with polyphony. At the
caption level, description does not. The two findings complement each other
across levels.

## Slide 7 — RQ3 (8:30)

Hallucination, measured with CHAIR adapted to audio: an entity counts as
hallucinated if neither the five references nor the audio tags support it.
The four serious captioners cluster between 0.33 and 0.35. Qwen is the
outlier at 0.55, and AST at 0.96 is the validity check, as an indiscriminate
tag list should fail this metric. Hypothesis four is the null result:
Audio Flamingo 3 does not hallucinate less than SALMONN, and I report that as
a finding. The decomposition explains it. Per individual mention, AF3 is
actually the most grounded system in the whole table, with the lowest
CHAIR-i. It simply makes more claims per caption, 1.54 entities versus 1.38,
and every extra claim is another chance to be wrong. That is the zipper,
quantified. One more failure mode: greedy decoding drove Qwen into a 515-word
"tapped, tapped" loop on one clip. We caught it because per-clip outputs are
retained.

## Slide 8 — Honesty (9:30)

Everything on this slide is already written in the paper, so nothing should
have to come out in questions. The scoreboard: three hypotheses supported, one
null retained and reported. Four disclosures. The preregistration was drafted
before the LALM runs but never formally frozen, so I claim a declared analysis
plan, not confirmatory status, and list all seven deviations. Zero-shot means
my protocol, no fine-tuning and no examples; it does not mean the models never
saw Clotho, and both audio specialists list Clotho development pairs in their
training corpora. That is symmetric with what the baselines trained on, and it
is disclosed. The EnCLAP anchor gap is reported, not tuned away. And the whole
project, code, manifests, results, logbook, preregistration, is public.

## Slide 9 — Takeaways (10:00)

Three things to remember. Whether a zero-shot LALM beats trained captioners
depends on the model, and the current audio specialist genuinely does.
Polyphonic clips score higher for every system, a dataset effect that
complements the event-level degradation in Professor Abeßer's own work. And
caption quality and audio grounding are different axes; evaluations should
report both. Thank you.
