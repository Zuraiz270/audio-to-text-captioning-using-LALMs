# P3 Masterclass: understand the whole project from zero

Read this top to bottom once, then use the self-test in section 15. After
that, you can explain every number, decision, and term in the paper without
notes. Simple words everywhere; precision is not sacrificed.

---

## 1. The project in three sentences

We asked whether the new generation of "large audio-language models" (LALMs),
which are chatbots that can also hear, describe an audio recording as well as
older systems that were trained specifically for that one task. We measured
this fairly by running six systems through one identical pipeline on the same
1,045 audio clips and scoring them with the same official metrics. Answer:
it depends on the model; the newest audio specialist (Audio Flamingo 3) beats
the trained systems, the other two LALMs do not, and nobody wins on every
axis, because the best scorer is not the most grounded one.

## 2. The task, and why it is hard

**Automated audio captioning (AAC)**: input is a sound recording (no speech
transcription, no music tagging), output is one English sentence describing
what is heard. Example: "Rain falls while a car passes by."

Why it is hard:
- Real recordings contain several overlapping sound sources (this overlap is
  called **polyphony**). The model must untangle engines from voices from rain.
- There are thousands of possible sound types (open vocabulary).
- Even judging a caption is hard: "waves crash on a beach" and "the ocean roars
  against the shore" describe the same audio with almost no shared words. This
  is why metrics matter so much in this project.

## 3. The dataset: Clotho v2.1

- The standard academic benchmark for audio captioning. Sounds come from the
  FreeSound website; every clip is 15 to 30 seconds, sampled at 44.1 kHz.
- Each clip has **five captions written by five different humans**. Five,
  because there are many valid ways to describe one sound; metrics compare a
  model's sentence against all five.
- It has a development split (used to TRAIN captioners; 3,839 clips) and an
  **evaluation split (1,045 clips)** used only for testing. We evaluate on the
  full evaluation split, every system, always.
- Decision to remember: we keep audio at its **native 44.1 kHz** and never
  globally resample, because the baseline's published weights were trained at
  native rate. Resampling would shift every spectrogram frame and break the
  reproduction. Proof it was right: our reproduction matched the published
  score.

## 4. The six systems

Think of them as two teams of three.

### Team Traditional

**AST, the tagging floor.** The Audio Spectrogram Transformer is a classifier,
not a captioner: it outputs probabilities for 527 fixed sound classes from the
AudioSet ontology (dog, engine, rain, ...). We take its top five classes and
paste them into a template: "a sound of X, Y, Z...". It only hears the first
10.24 seconds (its fixed input window). Purpose: a floor. It shows what score
you get from naming events without forming a sentence: 0.068 SPIDEr-FL. If a
"real" captioner scored near this, captioning would add nothing.

**CNN14+BART, the official baseline.** The DCASE 2023 challenge baseline.
CNN14 is a 14-layer convolutional network from the PANNs family that turns a
mel spectrogram into audio features; BART is a language model that decodes
those features into a sentence. It was trained end-to-end on Clotho's
development split. Published score 0.261; our reproduction 0.259. That 0.002
agreement is the proof our whole measuring machine works.

**EnCLAP-base, the stronger trained captioner.** Feeds BART two views of the
audio at once: EnCodec (a neural audio codec that compresses audio into
discrete tokens, like words for sound) and CLAP (a model that embeds audio and
text into one shared vector space, so "similar meaning" means "nearby
vectors"). Trained on AudioCaps, then fine-tuned on Clotho. Our row scores
0.280; published is 0.295 SPIDEr / 0.291 SPIDEr-FL. Our row runs about 1.1
points low; we disclose this openly (see section 12).

### Team LALM (all zero-shot: we never trained or fine-tuned anything)

**Qwen2.5-Omni-7B, the generalist.** Alibaba's everything-model: text, images,
audio, and speech in one network. We use it audio-in, text-out, and call
`disable_talker()` to switch off its speech-generation head (saves GPU
memory). 7B means seven billion parameters. It is the weakest LALM here
(0.188) because it writes report-style prose, not Clotho-style captions.

**SALMONN-13B, the older audio specialist.** A pipeline of parts: Whisper (a
speech encoder) plus BEATs (a general audio encoder) hear the clip; a
**Q-Former** (a small translator network with learned "query" tokens) squeezes
their outputs into a handful of vectors; those go into Vicuna-13B (a LLaMA
chat model) adapted with LoRA (small low-rank add-on weights). Scores 0.225,
between Qwen and the trained captioners.

**Audio Flamingo 3, the current specialist and the headline.** NVIDIA's
audio-language model: a Whisper-style encoder (128 mel bands) feeding a
Qwen2-7B language model. Ships natively in the transformers library. Scores
**0.297**, beating both trained captioners on every metric. Its captions read
exactly like Clotho references, short and factual.

### Settings you must be able to recite

- **Decoding**: how the language model picks words. *Greedy* = always the most
  likely next word (Qwen, AF3). *Beam search* = keeps the 4 best partial
  sentences and picks the best complete one (SALMONN, and both trained
  captioners). Rule we followed: every model runs at its authors' recommended
  setting, and every setting is recorded in the run manifest.
- **Precision**: how numbers are stored on the GPU. bf16 and fp16 are
  half-size (faster, less memory), fp32 is full-size. Qwen ran bf16, SALMONN
  fp16, AF3 **fp32** because its released weights are natively fp32 and
  loading it in bf16 caused a genuine type-mismatch crash in its encoder.
  fp32 is more precise, so this is the model at its best, not a handicap.
- **Prompt**: each LALM got one fixed instruction like "Describe the audio in
  one short, factual sentence." Recorded per run. Qwen's version adds "no
  questions, no commentary" because it liked appending "What do you think?"
  (we also strip trailing questions in a post-filter; verified zero `?` in the
  final run).
- **Seed 42**: the random-number starting point, fixed everywhere, so runs are
  repeatable.
- max_new_tokens 64 for LALMs; 1,045/1,045 clips completed for every system.

## 5. The metrics, built up from zero

### Step 1: n-grams
An n-gram is a run of n consecutive words. "waves crash loudly" has bigrams
"waves crash" and "crash loudly". Overlap metrics count shared n-grams between
the model caption and the five references.

### Step 2: CIDEr (and CIDEr-D)
Counts shared n-grams (n = 1 to 4) but weights each by **TF-IDF**: words that
appear in every caption everywhere ("a", "sound") count little; rare,
informative words ("ratchet") count a lot. So CIDEr rewards saying the
specific words the human references used. The -D variant adds small penalties
against gaming. Range roughly 0 to 1+ here; AF3 gets 0.460.

### Step 3: SPICE
Ignores exact wording. It parses captions into little graphs of
(object, attribute, relation), like (rain, falls) and (car, passes), and
scores the overlap of those graphs. So SPICE rewards describing the right
THINGS, CIDEr rewards using the right WORDS. AF3: 0.137.

### Step 4: SPIDEr
Just the average of CIDEr and SPICE: content words and content structure,
one number. The DCASE community's main metric family.

### Step 5: FER and SPIDEr-FL (our headline metric)
Problem: n-gram metrics can reward broken half-sentences. Fix: a trained
detector (from the FENSE metric family) checks each caption for fluency
errors (incomplete sentence, repeated words, missing verb...). **FER** =
fraction of a model's captions flagged. **SPIDEr-FL** = SPIDEr where a flagged
caption loses 90 percent of its score. All our LALMs have tiny FER (0.005 to
0.017), so their scores are earned by content, not lost to gibberish. This
matters for defense: Qwen's low score is NOT because its output is malformed;
its FER is the lowest in the table.

### METEOR
Older word-matching metric with synonym support. Reported for completeness.

### CHAIR-audio (our hallucination metric, RQ3)
Borrowed from image captioning (CHAIR, EMNLP 2018) where it counts caption
objects that are not in the image. Our audio port: take the 527 AudioSet class
names, split them into 604 matchable surface forms ("domestic animals, pets"
becomes two forms), and scan each model caption for them with deterministic
word matching (plurals and -ing forms included, no learned components, fully
reproducible). A mentioned entity is **hallucinated** if it appears in NEITHER
(a) the union of the five human references NOR (b) the sounds actually
detected in the audio by our sound-event detector. Requiring both (a) and (b)
to miss is the **dual criterion**; it is deliberately conservative.
- **CHAIR-s** = fraction of captions containing at least one hallucinated
  entity (per-caption rate). This is what H4 was tested on.
- **CHAIR-i** = fraction of all entity mentions that are hallucinated
  (per-claim rate).
- **coverage** = fraction of captions where the matcher found any entity at
  all (about 0.75 to 0.91 per model). The closed vocabulary misses synonyms;
  that bias hits all models equally and mostly cancels in the paired H4
  comparison.

### MACE (secondary, audio-grounded)
Scores a caption using CLAP embeddings of the actual audio (plus the reference
texts) instead of word overlap, with the same fluency-penalty idea. Its value:
it does not care whether you used the references' words, only whether the
caption matches the sound. Caveats we disclose: its backend listens to a
random 7-second crop per call (run-to-run noise about 0.002), and we clamp
captions to 30 words for its text encoder (affects 3 of 3,135 captions). We
therefore use it as a cross-check, never as the headline.

## 6. RQ1 and why "it depends on the model" is the RIGHT conclusion

The full ordering (SPIDEr-FL): AST 0.068 << Qwen 0.188 < SALMONN 0.225 <
CNN14 0.259 < EnCLAP 0.280 < **AF3 0.297**.

- Claim "zero-shot LALMs beat trained captioners": FALSE, two counterexamples
  (Qwen, SALMONN both lose to both trained systems).
- Claim "zero-shot LALMs lose to trained captioners": FALSE, one
  counterexample (AF3 beats both, on every single metric).
- The only statement the table supports: **whether** a zero-shot LALM beats
  trained captioners **depends on which LALM**. And the pattern is
  informative, not random: the current, large-scale, audio-specialized model
  wins; the general omni-model and the older specialist do not.

If asked "isn't that a non-answer?": a conditional answer with the condition
identified is MORE information than yes or no. We also confirmed it
statistically: H1 (AF3 above the published 0.261 baseline) is significant with
the confidence interval's lower bound at 0.283, and H3 (AF3 above SALMONN,
paired on the same clips) at +0.072. Both p about 0.001.

## 7. RQ2: the polyphony analysis, machinery and meaning

**Goal**: compare captioning on clips with overlapping sound events versus
single-source clips. Problem: Clotho has no labels saying which clips are
polyphonic. Solution: create pseudo-labels with **sound event detection
(SED)**.

- Tool: PANNs `Cnn14_DecisionLevelMax`, a CNN that outputs, 100 times per
  second, probabilities for the 527 AudioSet classes (framewise output; this
  is why the announced PaSST was swapped out: PaSST only gives one label set
  per clip, no timeline; disclosed as a deviation).
- Rule: a clip is **polyphonic** if two different classes are simultaneously
  active for at least 1 continuous second at confidence at least tau.
- The preregistered tau = 0.50 turned out degenerate: only 106 polyphonic
  clips and 609 clips with no detected activity at all. The **pre-committed
  fallback rule** (written down BEFORE seeing any results: require at least
  300 clips per bucket, else take the largest stored tau that satisfies it)
  selected tau = 0.25, giving **336 polyphonic / 709 monophonic**.
- Sanity check without SED: the references of "polyphonic" clips mention more
  distinct sound entities than monophonic ones (4.5 vs 3.8 on average; at
  least two entities in 97 percent vs 87 percent). So the split points the
  right way, independent of the detector.

**Result**: every system, all six, scores HIGHER on the polyphonic subset
(deltas +0.019 to +0.094). H2 is formally supported for all three LALMs, but
because the baselines shift equally, the correct reading is: polyphonic clips
are EASIER for caption metrics (more events = more matchable content), and the
monophonic bucket collects quiet, ambiguous clips (219 of them have zero SED
activation). It is a property of the data, not of LALMs.

**Connection to Prof. Abeßer's own work** (Harish and Abeßer, DCASE 2025):
they evaluated LALMs on a synthetic dataset (USM) across three levels: tagging
(low), counting and loudness ranking (mid), captioning (high). Their
event-level tasks degrade as polyphony grows; their caption-level metric
stays roughly flat. Ours shows the same at caption level on REAL recordings.
So: counting and naming every event gets harder with polyphony; producing one
good reference-like description does not. The findings complement each other.
MACE (audio-grounded) shows the same positive direction (+0.021 to +0.032),
so this is not an artifact of reference wording.

## 8. RQ3: hallucination, and the insight behind the null

CHAIR-s at tau 0.25: SALMONN 0.332 < AF3 0.347 ~ CNN14 0.350 ~ EnCLAP 0.351
<< Qwen 0.550 << AST 0.956.

- AST at 0.956 is the **validity check**: an indiscriminate top-5 tag list
  should fail a hallucination metric, and it does.
- Qwen is the outlier: it enumerates several events per caption (2.08 entities
  on average), so it makes many unsupported claims.
- **H4 asked**: does AF3 hallucinate LESS than SALMONN? Answer: no. Null
  retained (difference -0.015, p = 0.82, same verdict at all three thresholds).
  We report this as a finding, not a failure.
- **The decomposition that explains it** (know this cold): per individual
  mention, AF3 is the MOST grounded system in the table (CHAIR-i 0.299,
  lowest). But it mentions more entities per caption than SALMONN (1.54 vs
  1.38), and every extra claim is another chance to be unsupported. Richness
  buys score and buys risk at the same time. The concrete example is AF3's
  "zipper" caption on creaky.wav: fluent, specific, unsupported.
- Extra failure mode: greedy decoding drove Qwen into a 515-word
  "tapped, tapped, ..." repetition loop on one clip (opening attic.wav). We
  caught it because per-clip outputs are kept, and the fluency metric flags it.

Big picture sentence: overlap quality and audio grounding are different axes;
the model that wins one does not automatically win the other; evaluations
should report both.

## 9. The statistics in plain words

- **Hypothesis test**: we state a "null" (boring) claim, like "AF3 is not
  better than 0.261", then check how incompatible the data is with it.
- **p-value**: the probability of seeing our result (or better) if the boring
  claim were true. p = 0.001 means: practically never by luck.
- **Bootstrap**: instead of assuming a formula for uncertainty, we resample
  our 1,045 per-clip scores with replacement 1,000 times, recompute the mean
  each time, and read the spread. **BCa** is a refined version that corrects
  for bias and skew. Works because corpus SPIDEr-FL is exactly the mean of
  per-clip scores (we verified this equality).
- **95 percent CI lower bound**: the pessimistic edge of the estimate. For H1
  it is 0.2828, still above the bar of 0.2714 (= 0.261 + the preregistered
  minimum detectable effect of 1.04 points). That is why H1 stands.
- **One-sided**: we only asked "is it bigger", as preregistered.
- **Holm correction**: when testing several hypotheses, luck gets more
  chances, so the significance bar is tightened for each additional test. Our
  smallest p had to beat 0.0167 (three tests in the family) and did.
- **Paired vs two-sample**: H3 compares two models on the SAME clips
  (difference per clip = paired = more sensitive). H2 compares two DIFFERENT
  clip sets (poly vs mono), so pairing is undefined and a two-sample bootstrap
  is used; disclosed as deviation 6.
- **Preregistration**: writing hypotheses, thresholds, and decision rules down
  BEFORE seeing results, so you cannot bend the analysis to the data
  afterwards (the sin called HARKing). Ours was drafted before the LALM runs
  but the freeze field was never filled, so we honestly claim a "declared
  analysis plan", not certified confirmatory research, and list all seven
  deviations in the paper.

## 10. The engineering (why an examiner should trust the numbers)

- **One contract**: every system implements `caption(waveform, sample_rate) ->
  string`. A registry maps config names to classes. Therefore ONE inference
  loop and ONE scorer serve all six systems; nothing is measured differently
  per model.
- **Manifests**: every run records checkpoint SHA-256 hashes, library
  versions, decode parameters, prompt, and seed. Any number in the paper can
  be traced to one JSON file and one commit.
- **Robustness**: predictions are flushed to disk every 10 clips (a crash
  loses at most 9), and a single broken file cannot kill a run.
- **Two machines, by design**: inference on Windows, scoring in WSL Ubuntu
  because the SPICE metric needs Java 8 to 13 and the host has Java 23. The
  predictions JSON is the only handoff.
- **Separate Python environments** because upstream code pins incompatible
  library versions: `.venv` (CNN14, AST), `.venv-enclap` (transformers 4.29),
  `.venv-wsl` (scoring), `.venv-mace` (MACE), plus two cluster environments
  (a transformers 5.x env shared by Qwen and AF3, and a Python 3.10 conda env
  for SALMONN's old torch 2.0.1 stack).
- **The cluster**: NHR@FAU TinyGPU, one A100 40 GB per run, submitted via
  Slurm. Compute nodes have NO internet, so models were pre-downloaded and
  runs are offline and repeatable by construction. Full 1,045-clip runs:
  Qwen 8.3 min, SALMONN about 19, AF3 about 17.5.
- **Vendor, never reimplement**: baseline model code is pulled in as pinned
  git submodules and left untouched, so we inherit the exact published
  architecture instead of introducing transcription bugs.

## 11. Every major decision, one line of defense each

| Decision | Defense |
|:--|:--|
| CNN14 = DCASE 2023 baseline, not 2024 | 2024's baseline is a different net (ConvNeXt); the real CNN14 captioner is 2023 at 0.261. Corrected before freezing anything. |
| Native 44.1 kHz | Upstream trains at native rate; reproduction succeeding proves it. |
| Vendored submodules | Exact published architecture, zero transcription risk. |
| Scoring in WSL | SPICE needs Java 8-13; host has Java 23. |
| Separate venvs | Upstream pins are mutually incompatible; isolation beats fighting. |
| Falcon3-Audio dropped | Its weights were never publicly released (checked paper, author page, model hub). Replaced by AF3. |
| AF3 in fp32 | Its native precision; bf16 crashes its encoder; fp32 is higher precision anyway. |
| Authors' own decode per LALM | "Each model at its best"; all recorded in manifests. |
| tau 0.50 -> 0.25 | Pre-committed fallback rule, written before results existed. |
| PaSST -> PANNs SED | Definition needs frame-level output; PaSST is clip-level. Disclosed. |
| EnCLAP anchor corrected to 0.291/0.295 | The 0.283 "published" figure was wrong; honesty beats a flattering fake anchor; AF3 clears the true anchor anyway. |
| Zero-shot disclosure | AF3 and SALMONN saw Clotho dev pairs in training (their own papers say so); symmetric with baselines; disclosed in abstract and discussion. |
| H4 null reported as-is | A preregistered null is a result; the CHAIR-i decomposition makes it interpretable. |

## 12. The uncomfortable topics, handled

**"Your EnCLAP is 1.1 points low."** Yes, and the paper says so in four
places. Harness validity rests on CNN14 (within 0.002). The follow-up paper
EnCLAP++ shows the released checkpoint can reach 0.294 with the same scoring
toolkit, so the gap is likely checkpoint or decoding side. AF3 beats EnCLAP's
PUBLISHED 0.291 anyway, so no conclusion depends on our low row.

**"Zero-shot but trained on Clotho?"** Zero-shot describes OUR protocol (no
fine-tuning, no examples). AF3's own appendix lists 19,195 Clotho development
pairs in its training mix; SALMONN trains on Clotho in both stages. The
evaluation split is held out for everyone, and the exposure is the same
development data the baselines trained on, so the comparison stays symmetric.
Disclosed in the abstract and discussed; it is also exactly why we added the
audio-grounded metrics (CHAIR, MACE) that do not reward reference-style
mimicry.

**"Prereg never frozen."** Correct, the freeze field is null in the committed
file. Therefore we claim only a declared analysis plan and disclose every
deviation, including the three descriptive probes (temporal ordering,
out-of-distribution clips, silence negative control) that were cut for scope
and never run.

**"How much did the AI do?"** The paper's AI Transparency Statement answers
this per course requirements: Claude was used throughout, for pipeline code,
analysis, literature triage, and LaTeX, under my direction and review, with a
session-dated logbook in the public repository. Every number comes from
committed scripts running on raw model outputs. The defense of this is
understanding, which is what this document gives you: be able to explain any
decision in section 11 and any number in the cheat card, and the question
answers itself.

## 13. Timeline (what happened when)

- **01.06** CNN14 baseline built and reproduced (0.259 vs 0.261); the
  2023-vs-2024 labeling error found and fixed everywhere.
- **03.06** EnCLAP row added by reusing the same pipeline (0.280).
- **29.06** AST tagging floor added (0.068).
- **04.07** Cluster onboarding. Falcon3-Audio found to have no public weights,
  replaced by AF3. Qwen2.5-Omni full run and scoring (0.188).
- **04.07** SALMONN: four checkpoints, own conda env, BEATs checkpoint rescued
  from a dead link via a verified mirror; full run (0.225).
- **05.07** AF3: one dtype bug (fixed by fp32), full run, headline result
  (0.297).
- **05-06.07** SED split, CHAIR-audio, MACE, per-item scores, bootstrap tests
  (H1-H4), all figures and tables generated from result files; 6-page paper
  written and submitted.
- **07.07** Full audit: EnCLAP anchor corrected, zero-shot disclosure added,
  README rewritten, results committed to the public repo.
- **11.07** This P3 package.

## 14. Glossary (one line each)

- **LALM**: a language model with an audio encoder bolted on, so it can hear.
- **Zero-shot**: using a model on a task without training it for that task.
- **Encoder / decoder**: the part that turns input into vectors / the part
  that turns vectors into output words.
- **Mel spectrogram**: a picture of sound; time on x, pitch bands on y,
  loudness as intensity; scaled to human hearing.
- **Token**: a word piece a language model reads and writes.
- **Beam search / greedy**: keep n best sentence candidates / always take the
  single most likely next word.
- **bf16 / fp16 / fp32**: number formats on the GPU; 16-bit is smaller and
  faster, 32-bit is more precise.
- **Checkpoint**: a saved file of model weights.
- **SED**: sound event detection; which sound classes are active when.
- **PANNs / CNN14**: a family of pretrained audio CNNs / its 14-layer member.
- **AudioSet**: Google's ontology of 527 sound classes.
- **Whisper**: OpenAI's speech encoder, reused as an audio feature extractor.
- **BEATs**: a self-supervised general audio encoder (used inside SALMONN).
- **Q-Former**: a small translator network that compresses encoder output into
  a few tokens an LLM can read.
- **LoRA**: cheap fine-tuning via small add-on matrices.
- **EnCodec**: a neural audio codec; audio becomes discrete tokens.
- **CLAP**: contrastive audio-text embedding; same space for sounds and words.
- **CIDEr / SPICE / SPIDEr**: right words / right things / their average.
- **FER / SPIDEr-FL**: share of disfluent captions / SPIDEr with a 90 percent
  penalty on flagged captions.
- **CHAIR-s / CHAIR-i**: captions with at least one unsupported entity /
  unsupported share of all entity mentions.
- **MACE**: caption scored against the audio itself via CLAP embeddings.
- **BCa bootstrap / Holm / MDE**: resampling-based uncertainty / multiple-test
  correction / smallest effect we declared worth detecting.
- **Preregistration / HARKing**: committing the analysis before results / the
  sin of hypothesizing after results are known.
- **Manifest**: the per-run receipt (hashes, versions, settings, seed).
- **Slurm / sbatch**: the cluster's job scheduler / the command to submit.

## 15. Self-test (cover the answers, say them out loud)

1. Why 44.1 kHz? (native training rate of the baseline; reproduction proves it)
2. Why is AST included if it scores 0.068? (tagging floor + CHAIR validity check)
3. What exactly does 0.259 vs 0.261 buy you? (harness validity for every row)
4. Why is SPIDEr-FL the headline and not CIDEr? (DCASE standard; adds fluency
   penalty so broken sentences cannot score)
5. Qwen scored lowest. Is it bad at hearing? (no; lowest FER, competitive
   MACE; it phrases in report style that overlap metrics punish)
6. Why did every system improve on polyphonic clips? (more events = more
   matchable content; baselines shift equally, so data property)
7. How was the polyphony threshold chosen? (prereg 0.50 degenerate;
   pre-committed fallback rule selected 0.25; 336/709)
8. What makes an entity "hallucinated"? (in neither the 5 references nor the
   SED tags: dual criterion)
9. Why did H4 fail and why is that interesting? (AF3 makes more claims per
   caption; per claim it is the MOST grounded: CHAIR-i 0.299)
10. What did Harish and Abeßer show, and what do you add? (event-level tasks
    degrade with polyphony on synthetic USM; caption-level does not, and we
    confirm that on real Clotho recordings)
11. Name the three disclosures on your honesty slide without looking.
    (prereg not frozen; zero-shot vs Clotho training data; EnCLAP anchor gap)
12. What is in a run manifest? (checkpoint hashes, library versions, decode
    params, prompt, seed)
13. Why three different LALM vendors? (so the conclusion is not a
    single-vendor artifact)
14. Why fp32 for AF3 and does it bias anything? (native precision, bf16
    crashes; higher precision, and measurement is unchanged)
15. What would you do next? (strong temporal labels on real data; joint
    event+caption protocols; grounded metrics reported by default)

If you can answer all fifteen without hesitation, you are ready. The numbers
themselves are on the cheat card; drill those separately.
