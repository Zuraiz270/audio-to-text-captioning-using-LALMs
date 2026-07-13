# P3 Speaker Script — 10 minutes, spoken version (13 July 2026)

How to use this:
- Times are cumulative targets at the END of each slide.
- Say scores as "point two five nine", not "zero point...". Say SPIDEr-FL as
  "SPIDER F-L". Say Clotho as "KLOH-tho". Say Qwen as "chwen" (or just "the
  Qwen model"). Say Abeßer as "AH-bess-er".
- [square brackets] are actions, not words. Don't read them.
- Running late at the end of slide 6? On slide 8, say only the first two
  points. Never cut slide 9.
- Short sentences are on purpose. Breathe at every period.

---

## Slide 1 — Title (0:40)

Good morning everyone.

My project asks one simple question. Today's big AI models can hear. But can
they describe what they hear, as well as systems that were trained just for
that one job?

[point at the number]

This number is the short answer. Point two nine seven. That's the best
zero-shot model, and it's above both trained baselines I reproduced.

The next ten minutes: what this number means, where it holds, and where it
breaks down.

## Slide 2 — Task and research questions (1:50)

So, the task. Audio captioning means: audio goes in, one English sentence
comes out. Like: "Rain falls while a car passes by."

I compare six systems. Two teams.

[left side]

The traditional team. AST, which only lists sound tags. That's my floor. And
two real captioners, trained on Clotho: the official CNN14 baseline, and
EnCLAP.

[right side]

The LALM team, all zero-shot. I never trained anything. Qwen, a general
do-everything model. SALMONN, an older audio specialist. And Audio Flamingo 3
from NVIDIA, the current state of the art. Three models, three different
companies. So this is not a one-vendor story.

Three questions. One: do they match the trained systems? Two: what happens on
clips with overlapping sounds? Three: how much do they hallucinate?

And important: all hypotheses were written down before the runs.

## Slide 3 — Method (3:00)

How do I make this comparison fair? One harness. Let me walk the flow, left
to right.

[trace the boxes with your hand]

It starts with the data. The Clotho evaluation set. One thousand forty-five
clips, untouched, native sample rate.

Box two: every system implements the same tiny interface. Audio in, caption
out. A small CPU model and a thirteen-billion-parameter model on an A100 look
exactly the same to my pipeline.

Box three: each run writes its predictions, plus a receipt. Checkpoint hashes,
library versions, decode settings, the seed. Every number in my paper traces
back to a file.

Box four: one scorer for everyone. Same clips, same five references, same
metric.

And box five: all the analysis, the subsets, CHAIR, MACE, the statistics,
reads only from those files.

Three reasons to trust this machine.

First: it reproduces the official baseline. Point two five nine against point
two six one published. The ruler works.

Second: the big models ran on the cluster, offline, from pre-cached
checkpoints, with a fixed one-line prompt.

Third: all six systems finished every clip. Zero failures.

## Slide 4 — RQ1 (4:30)

Okay, the headline.

[point at chart, bottom to top]

The answer to question one is not yes or no. It depends on the model.

Look at the order. Every LALM beats the tag floor by three to four times. So
they all really describe, they don't just list.

But. Qwen and SALMONN both stay below both trained captioners. So the claim
"LALMs beat trained systems"? False in general.

And then Audio Flamingo 3. It beats both trained captioners. On every single
metric. Zero-shot. And its point two nine seven is even above EnCLAP's
published score of point two nine one.

The statistics hold. Hypothesis one: even the careful lower bound is point two
eight three, clearly over the bar. Hypothesis three: paired on the same clips,
AF3 is plus point zero seven two over SALMONN. Both very significant.

One honest note, bottom right. My EnCLAP row runs about one point below its
published number. That's disclosed in the paper. And my main hypothesis is
anchored on CNN14, which reproduces almost exactly. So nothing depends on it.

## Slide 5 — Captions (5:30)

Now forget numbers for a moment. This is what the systems actually say. Same
clip, real outputs.

The human wrote: people walking, voices, soft music.

AST gives a tag list. Not a sentence.

Qwen says "the audio contains..." — like a report. No human reference ever
sounds like that. And it lists many events.

SALMONN and EnCLAP: short, natural sentences.

And Audio Flamingo 3 sounds exactly like a Clotho reference. That's exactly
what the metrics reward.

But look at the red word. A zipper. Fluent, specific... and not supported by
the references or by the audio. Keep that zipper in mind. It comes back.

## Slide 6 — RQ2 (7:00)

Question two: overlapping sound. Polyphony.

Clotho has no polyphony labels, so I built them. A sound event detector marks
which sounds are active at every moment. If two sounds overlap for at least
one second, the clip counts as polyphonic. The first threshold from the plan
turned out degenerate, so a fallback rule, written down before any results,
picked the final one. Three hundred thirty-six polyphonic clips, seven hundred
nine monophonic.

And here's the surprise.

[point at chart]

Every bar is positive. Every system scores higher on the polyphonic clips.
Even the trained ones. Even the tag floor.

So yes, hypothesis two formally passes for all three LALMs. But the baselines
shift the same way. Which means: this is a property of the data, not of the
models. Clips with more events give a caption more to match. The quiet,
ambiguous clips are the hard ones.

The MACE metric, which listens to the audio itself, agrees. So it's not a
wording artifact.

And this connects to your own work, Professor. Your DCASE paper with Harish
showed: tagging and counting get worse with polyphony. I show: describing does
not. Event level suffers, caption level doesn't. The two findings complement
each other.

But notice the tension in that. The models describe scenes they cannot fully
count. So what is the description really capturing? Hold that thought. It
comes back on my last slide.

## Slide 7 — RQ3 (8:30)

Question three: hallucination.

I ported the CHAIR metric from image captioning to audio. A mentioned sound
counts as hallucinated only if it's missing from the five human references AND
missing from the detected audio events. Double check, so it's conservative.

[point at chart]

The four serious captioners cluster around point three three to point three
five. Qwen is the outlier at point five five. And AST at point nine six is
actually good news — a blind tag list SHOULD fail this metric. That validates
it.

Hypothesis four is my null result. Audio Flamingo does NOT hallucinate less
than SALMONN. The best captioner is not the most grounded one. And I report
that as a finding.

But here's the interesting part. Per single claim, AF3 is the MOST grounded
model in the whole table. Lowest rate per mention. It just makes more claims
per caption. One point five four entities versus one point three eight. More
claims, more chances to be wrong.

That's the zipper, in numbers.

And one bonus failure: greedy decoding once drove Qwen into a five-hundred-
fifteen-word loop. "Tapped, tapped, tapped..." We caught it because every
single output is kept.

## Slide 8 — Limitations (9:30)

Every project has weak points. These are mine, openly.

The scoreboard: three hypotheses supported, one null, reported as a result.

The preregistration was drafted before the runs, but never formally frozen. So
I claim a declared plan, not confirmatory research, and I list all seven
deviations.

"Zero-shot" means my protocol: no fine-tuning, no examples. It does not mean
the models never saw Clotho. Both audio specialists had Clotho training pairs
in their corpora. Their own papers say so. That's the same data my baselines
trained on, so it stays symmetric. And it's disclosed.

The EnCLAP gap is reported, not tuned away. And everything, code, results,
logbook, preregistration, is public.

All of this is in the paper, and I'm glad to discuss any of it.

## Slide 9 — Takeaways (10:00)

Three things to remember.

One. Whether a zero-shot model beats trained captioners depends on the model.
The current audio specialist really does.

Two. Polyphonic clips score higher for everyone. That's the dataset, not the
models. And it complements the event-level picture from your own work.

Three. Caption quality and audio grounding are different axes. Measure both.

And one question this project leaves open. I would genuinely like your view on
it. If describing a scene stays easy while counting its events gets harder,
what do caption metrics actually measure: scene understanding, or scene
summarization? I think a joint protocol, events and captions on the same real
clips, could answer that.

Everything is reproducible from the repository.

Thank you.
