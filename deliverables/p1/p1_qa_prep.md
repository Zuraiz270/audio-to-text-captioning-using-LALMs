# P1 — Q&A Preparation

*18 anticipated questions  ·  5 themes  ·  each answer ≤ 30 seconds*
*Author: Zuraiz · 2026-05-04*

---

## Universal fallback (use when stuck)

> "That is a very good question. I have not fully measured this yet — that's exactly what P2 / the pipeline phase is for. The current pointer in the literature is **[Author Year]**, and my plan is to verify it on Clotho v2.1. I would be happy to share the result with you in P2."

Keep this in your back pocket. Use it once, max twice — it sounds honest. Saying "I don't know" is also fine.

---

## Theme A — Scope & Choice of Models  (5 Qs)

### Q1.  Why is **Falcon3-Audio** your primary model?

**Short answer:** Three reasons. First, it is fully open — *all* its training data is **public**, so I can audit it for Clotho contamination. Second, it uses **single-stage** training, not a complex multi-stage curriculum, so the results are interpretable. Third, it matches the bigger Qwen2-Audio with **only thirty thousand hours** of training audio, while Qwen used over five hundred thousand hours of private data. So Falcon3 is a *clean, honest, audit-friendly baseline*.

**Supporting fact:** Falcon3-Audio paper, IEEE ASRU 2025, document 11434596. It uses Whisper-large-v3 as encoder, a linear projector, and a Falcon3 LLM (1B / 3B / 7B variants).

**Fallback if pushed:** "If you'd prefer I add another single-stage public-data baseline, I can include SLAM-LLM, but my current decision is one primary plus two reference LALMs to keep the comparison clean."

---

### Q2.  Why include **SALMONN** if it is from 2024 — and **Qwen2.5-Omni** if it is so new?

**Short answer:** They are not redundant — they cover different *positions* in the design space.
**SALMONN** is the **survey-standard** model. Almost every recent LALM paper benchmarks against it, so excluding it would make my numbers hard to compare with prior work.
**Qwen2.5-Omni** is the **scale ceiling** — it represents what happens when you throw more data and modalities at the problem. If polyphony failure is a *data-scale* issue, Qwen will solve it. If polyphony failure is a *structural* issue, it will not. That distinction is exactly the point of my study.

**Fallback:** "These two cost me nothing extra to evaluate — pre-trained weights are public, inference only."

---

### Q3.  Why is **Audio Flamingo** *not* a primary target?

**Short answer:** Two reasons. First, an updated version — Audio Flamingo Next — appeared just weeks ago, so the family is *mid-flux* and the canonical "primary" version is unstable. Second, the Falcon3 paper directly compared single-stage public-data training against the Audio-Flamingo cross-attention design and found the simpler approach competitive — so Falcon3 is the *better-defended* primary baseline. Audio Flamingo stays in my literature corpus as **historical architectural context**.

---

### Q4.  Why **three** traditional baselines instead of one?

**Short answer:** They each fix a different confound.
- **CNN14** is the official DCASE 2024 baseline — without it, my paper has no leaderboard reference.
- **AST** is pure transformer — controls for whether *attention* alone explains gains.
- **EnCLAP** is contrastive without an LLM — controls for whether the *language model decoder* is what helps.

Together, they let me say "the LALM gain (or loss) is *not* explained by encoder choice, by attention, or by contrastive learning alone."

---

### Q5.  Are these LALMs **comparable in size**?

**Short answer:** Roughly, but not exactly. *Falcon3-Audio* runs at 1B, 3B, and 7B parameters — I will report the 3B for parity. *SALMONN* is around 13B. *Qwen2.5-Omni* is about 11B. So size differs by **3-4×**, which is a confound I have to discuss honestly. I will mitigate this by also reporting the **per-parameter** caption quality, not only absolute SPIDEr-FL.

**Fallback:** "I am not claiming Falcon3 is *better* than Qwen — I am asking whether they fail polyphony the *same* way or *differently*."

---

## Theme B — Dataset  (4 Qs)

### Q6.  Why **Clotho v2.1** and not **AudioCaps**?

**Short answer:** Three reasons.
- **Clotho** is the **DCASE 2024 Task 6 official benchmark** — required for leaderboard comparability.
- **Clotho** has **five human captions per clip**, AudioCaps has only one. Five captions let me distinguish *under-description* from *single-annotator variance*.
- **AudioCaps** is built from AudioSet, which is part of the training data of several LALMs. **Clotho** is from FreeSound and is *less likely* to be contaminated.

**Fallback:** "I will probably also report AudioCaps numbers as a robustness check in the term paper — that's an addition, not a replacement."

---

### Q7.  How big is the **polyphony subset** of Clotho?

**Short answer:** Honest answer — **I haven't formally measured it yet**. Defining and quantifying the polyphony subset is the *first task* of P2. My plan is to use a sound-event-detection model — like the one in the recent SED Review 2025 — to count concurrent events per clip, then split Clotho into mono- and poly- buckets. I expect 30 to 50 % of clips to qualify as polyphonic.

**Fallback:** "If you have a published threshold you trust, I would love to use it as my anchor."

---

### Q8.  How will you check for **training-data contamination**?

**Short answer:** Falcon3-Audio publishes its full training manifest — that's its main selling point. I will hash all Clotho v2.1 audio fingerprints and grep them against the Falcon3 manifest. For SALMONN and Qwen, the manifests are not fully public, so I will use **acoustic fingerprinting** — a 2026 paper, *Data Leakage Benchmark*, IEEE ASRU 2025, document 11450559 — to flag near-duplicates probabilistically. I will report contamination rates per model so my SPIDEr-FL numbers are interpretable.

---

### Q9.  Five reference captions per clip — is that **enough** to measure under-description?

**Short answer:** It is enough as a *floor*, not a *ceiling*.
- The five captions give me a **union vocabulary** of mentioned events per clip. If the model output mentions *fewer* unique events than the union, that's a clear under-description signal.
- But the *true* polyphony of a clip can exceed what any single human caption captures, so I will also use a **sound-event-detector** as a second ground truth.
- Both grounds will be reported — the gap between them tells you the human-labelling ceiling.

---

## Theme C — Metrics  (4 Qs)

### Q10.  What is the difference between **SPIDEr-FL** and **CIDEr**?

**Short answer:**
- **CIDEr** is **TF-IDF-weighted n-gram overlap** with reference captions.
- **SPICE** is **scene-graph overlap** — it parses a caption into an object/relation graph.
- **SPIDEr** is the average of CIDEr and SPICE.
- **SPIDEr-FL** adds a **fluency penalty** — it punishes incomplete or ungrammatical outputs.
The fluency penalty matters specifically because LLMs occasionally produce "blank" or repeated output.

**Supporting fact:** SPIDEr-FL is the official DCASE 2024 Task 6 metric. The DCASE 2024 baseline scores 29.6 % SPIDEr-FL.

---

### Q11.  What does **MACE** measure that SPIDEr-FL **cannot**?

**Short answer:** MACE looks at the **audio signal itself**, not just the reference text. It has three parts. One — cosine similarity between **CLAP embeddings of audio and caption**. Two — the same between **caption and reference**. Three — a **fluency penalty**. The first part is the new idea — every prior metric just compared text-to-text. So if a model hallucinates "birds" because the reference mentions "park", SPIDEr might still reward it, but MACE will catch the audio-text mismatch.

**Supporting fact:** Dixit et al., MACE, IEEE ICASSP-W 2025, document 11011270. MACE outperforms FENSE by +3.28 % on AudioCaps and +4.36 % on Clotho when predicting human judgments.

---

### Q12.  CHAIR was made for **image** captioning — does it transfer to **audio**?

**Short answer:** Not directly — that is exactly why I called it "**CHAIR-audio**" in my slides.
The original CHAIR counts visual objects in a caption that are not in the image. To adapt it to audio, I will replace the COCO object list with the **AudioSet ontology** — about 632 sound classes — and use a sound-event detector to verify presence. So it is an *adaptation*, not a direct transfer, and I will validate it with manual checks on a 100-clip sample.

---

### Q13.  Will you also do a **human evaluation**?

**Short answer:** A small one, yes. I do not have the budget for a full crowdsourced study, but I plan a **30-clip listening test** with five raters — myself plus four classmates if they agree. Raters will mark each generated caption as *complete*, *under-described*, or *hallucinated*. This 30-clip sample will be my correlation anchor between MACE and human judgment. The results go in the term paper, not P2.

---

## Theme D — Methodology & Failure Modes  (3 Qs)

### Q14.  How exactly do you define **"under-description"** of polyphony?

**Short answer:** Operationally, in three steps.
1. Run a sound-event detector on the clip → get a set of events `E_audio`.
2. Take the set of events mentioned across all 5 reference captions → `E_ref`.
3. Take the set of events in the model's output → `E_model`.

A clip is **under-described** if `|E_model| < |E_ref ∩ E_audio|`. The fraction of clips where this happens, by polyphony bucket, is my main RQ2 metric. I will report **Δ MACE** between the polyphonic and monophonic subsets to confirm the trend statistically.

---

### Q15.  How do you tell **hallucination** from a **creative-but-correct** caption?

**Short answer:** This is the central trap of caption evaluation. My approach:
- An entity is **hallucinated** if it fails *both* — the audio-grounded check (CLAP audio-text similarity below a threshold) **and** the reference-grounded check (entity not in any of the 5 reference captions).
- An entity is **creative-but-correct** if it fails the reference check but *passes* the audio check — i.e., the audio actually contains it, but no human caption happened to mention it.
- The MACE audio-text component is precisely the tool for this, which is one reason I picked it.

---

### Q16.  Are you **fine-tuning** any of these models?

**Short answer:** **No.** Everything is **zero-shot**, with **pre-trained weights** only. This is per scope — both because the goal is to characterise *deployed* models and because fine-tuning would confound the comparison. Audio is a high-cost domain and I want my results to be reproducible by anyone who downloads the weights.

---

## Theme E — Significance & Limitations  (2 Qs)

### Q17.  What is the **application impact** if your hypothesis is right?

**Short answer:** If LALMs systematically under-describe polyphonic audio, three application areas need to know.
- **Accessibility** — captions for the deaf will silently drop background events that the user might *care* about (a doorbell, a baby crying behind dialogue).
- **Surveillance and safety** — a "smart hospital" listening for falls might miss a fall happening *behind* speech.
- **Cultural-heritage indexing** — soundscape archives indexed with LALMs would systematically lose their *richness* — exactly the texture the archive was meant to preserve.
So this is not just a benchmark issue — it is a deployment risk.

---

### Q18.  What is the **biggest threat** to the validity of your study?

**Short answer:** The biggest threat is **dataset contamination**. If Clotho clips are present in any LALM's training data, my polyphony numbers will be optimistically biased — the model will look better than it really is. That's why my P2 is *entirely* about the data strategy and contamination audit. The second threat is the size mismatch I mentioned earlier — I will mitigate it with per-parameter reporting.

**Fallback if pushed:** "If contamination turns out to be high, the study still has a result — I can report polyphony failure on the *clean* subset and discuss the contamination separately."

---

## Wildcard reserve answers

If a question hits a topic outside the 18 above:

- **"Is this task also relevant for music?"** → "Music adds harmonic polyphony, which is even harder. My project focuses on environmental sound; music is out of scope but a clear extension."
- **"Why English captions?"** → "Clotho is English, and the LALMs' decoders are English-trained. Multilingual audio captioning is a real open problem — I cite *Audiopedia (2025)* — but it is not my P1 scope."
- **"What if your hypothesis is wrong?"** → "Then I will report a *negative* result — that LALMs match tagging on polyphony — and that is also a publishable finding. Either way, the study is informative."
- **"What about real-time / streaming?"** → "Out of scope. All my evaluation is offline, on 15-30 second clips. Streaming AAC is its own subfield."
- **"Where will you run the experiments?"** → "On Falcon3-3B I can run inference on a single 24 GB GPU. For Qwen2.5-Omni I will use the university cluster or rent an A100 for a day."

---

## Final mental rules for Q&A

1. **Always restate the question in one short line first.** This buys you 3 seconds and confirms you heard it.
2. **Give the conclusion first, then the reasons** — opposite of how I write code.
3. **If you do not know — say so honestly**, then point to the literature you would consult.
4. **Do not over-promise.** If the prof asks "will you do X?" and X is outside scope, say "X is interesting but outside P1 scope. I'd plan it as future work."
5. **Look at the questioner first, then break eye contact and look at the rest of the room while answering.**
