# P1 Speaker Script  —  read aloud from this page, slide by slide

**Total time target: 4 minutes 40 seconds**  ·  Speak slow. Smile. Breathe.
**Pace:** about 130 words per minute. Roughly 2 short sentences per breath.

---

## How this script works (read this once, then forget it)

- The lines in **`>`** boxes are the **exact words you say**.
- Lines in *italic with [brackets]* are **stage directions — DO NOT say them**.
- **CAPS = say slowly and clearly** (these are tricky words).
- **(pause)** = stop for one full second.
- **(breathe)** = take a small breath.
- At the end of every slide there is a **safety line** — if you forget what to say next, just read the safety line aloud and click to the next slide.

---

# SLIDE 1 — Title slide

**You are at:** 00:00.   **Click to leave at:** 00:35.

*[Walk to the front. Click to slide 1. Wait two seconds. Look at the audience. Smile.]*

> Good morning, everyone.

**(pause — count "one")**

> My project is called **Audio-to-Text Captioning** *(say it as: AW-dee-oh to TEKST CAP-shun-ing)* using **Large Audio-Language Models**.

**(breathe)**

> The course code is **T6**.

> The simple idea is this: the model listens to a sound clip. Then it writes a sentence about that sound.

**(pause)**

> The big question of my project is here on the slide:

> Can these large models describe sounds that **OVERLAP**? When more than one sound happens at the same time, we call this **POLYPHONY**. *(say it as: po-LIH-fo-nee)*

**(pause — look up at the audience)**

> In the next five minutes, I will show you four things. The task. The papers I read. The models I will compare. And the plan for the next months.

*[Click to Slide 2.]*

**Safety line if you freeze:** *"My project is Audio-to-Text Captioning using Large Audio-Language Models. The big question is — can these models describe overlapping sounds?"*

---

# SLIDE 2 — The task & why it matters

**You are at:** 00:35.   **Click to leave at:** 01:50.

*[Move to the side of the screen — do not block the slide. Use your hand to point.]*

> The task is called **Automated Audio Captioning**, or **A-A-C**. *(spell it out: A, A, C)*

**(point at the LEFT side of the slide)**

> The OLD way was tagging. The model gives you words like *"dog, traffic, wind, leaves"*. It is useful, but it is flat.

**(point at the LEFT side again, lower)**

> The NEW way is captioning. The model gives you a real sentence. Like this — and here I will read the sentence on the slide:

*[Read the italic sentence on the slide slowly.]*

> *"A dog barks in the distance, as cars pass on a wet road, while wind rustles nearby leaves."*

**(pause — let it sink in)**

**(point at the RIGHT side of the slide)**

> Why do we care? I want to give three real examples.

> **One — accessibility.** Captions help people who are deaf or hard of hearing.

> **Two — searchable archives.** Imagine fifty years of radio recordings. Captions help us search by what is happening in the sound.

> **Three — smart spaces.** A camera in a hospital, or a city, can react to what it hears.

**(pause)**

**(point at the dark navy strip at the bottom)**

> But here is the **HARD** part. When many sounds happen at the same time — polyphony — today's models drop the small ones. They only describe the loudest one. That is the gap I want to study.

*[Click to Slide 3.]*

**Safety line if you freeze:** *"Captioning matters for accessibility, archives, and smart spaces. The hard part is polyphony — when sounds overlap, the model drops the secondary ones."*

---

# SLIDE 3 — The literature funnel

**You are at:** 01:50.   **Click to leave at:** 03:15.

*[Step closer to the screen. Use your finger to point at each card.]*

**(point at the title)**

> In two weeks, I read **38 papers** from the project corpus of **49**. From those 38, I selected **10 papers** to cite today.

**(breathe)**

**(point at the small italic line under the title)**

> The filter was simple. Only IEEE or ACM peer-reviewed papers, less than three years old, and directly tied to my models, my dataset, my metrics, or my failure modes.

**(pause)**

> The 38 papers fall into **6 streams**. I will name them quickly.

*[Point at each card on the grid as you say its name. Keep it fast — about 5 seconds per card.]*

> **Stream one — datasets, encoders, and tagging baselines.** Eight papers. Examples: *WavCaps, AudioSetCaps, OpenBEATs, CNN14*.

> **Stream two — LALM architectures and engines.** Seven papers. Examples: *Falcon3-Audio, SLAM-LLM, EnCLAP, DeSTA 2.5*.

> **Stream three — alignment, prompting, and fine-tuning.** Thirteen papers. The biggest stream. Examples: *Audio Chain-of-Thought, Omni-R1, Acoustic Prompt Tuning*.

> **Stream four — evaluation metrics and bias.** Five papers. Examples: *MACE* and *CLAIRA*. These are new audio-aware metrics.

> **Stream five — domain extensions.** Four papers. Soundscape captioning, audio-visual.

> **Stream six — datasets governance and licensing.** One paper.

**(pause — look at the audience)**

**(point at the bottom callout)**

> My focus is on streams **two and four**. How LALMs fail on polyphony, and how we measure that failure honestly.

*[Click to Slide 4.]*

**Safety line if you freeze:** *"38 papers in six streams. I shortlisted 10 for today. My focus is streams two and four — how LALMs fail on polyphony."*

---

# SLIDE 4 — The models and the questions

**You are at:** 03:15.   **Click to leave at:** 04:15.

*[Move to the side. Point at the LEFT column.]*

> On the LEFT, three **traditional baselines**. They use tagging, no language model.

> *CNN14*, the official DCASE baseline. *AST*, a pure transformer. *EnCLAP*, a contrastive model.

*[Point at the RIGHT column, then at the gold star next to Falcon3-Audio.]*

> On the RIGHT, three **state-of-the-art LALMs**. They use an audio encoder plus a large language model.

> *Falcon3-Audio* is my **PRIMARY** model — see the **STAR** next to it. It uses only public training data, so I can audit it.

> *SALMONN* is the survey-standard. *Qwen2.5-Omni* is the bleeding-edge one. I want to test if **size alone** can solve polyphony.

**(pause)**

**(point at the dark navy band at the bottom)**

> Now, the questions. There are three.

**(point at RQ1)**

> **RQ1.** Do LALMs match or beat traditional tagging on standard metrics? I will measure this with **SPIDEr-FL** *(say: SPI-der-F-L)* and **CIDEr** *(say: SY-der), which are caption quality metrices. they evaluate how similar the geneated sentence is to the human witten copus*.

**(point at the starred RQ2)**

> **RQ2** is the **CORE question**. How accurately do LALMs describe overlapping sound events compared to tagging? I will measure this with **Delta MACE** (a polyphony-awarre metric)— the difference of peforrmance between the polyphonic and the monophonic subsets.

**(point at RQ3)**

> **RQ3.** What is the entity-hallucination rate of LALMs on polyphonic audio? Hallucination means the model writes a sound that is not really there. I will measure this with **CHAIR-audio** *(a hallucination metic which detect false sound desciption)*.

*[Click to Slide 5.]*

**Safety line if you freeze:** *"Three baselines. Three LALMs. Falcon3-Audio is the primary. Three research questions: parity, polyphony, hallucination."*

---

# SLIDE 5 — The roadmap

**You are at:** 04:15.   **Click to leave at:** 04:40.

*[Stand in the middle. This is the closing — slow down.]*

*[Point at the timeline circles in order.]*

> Today is step **ONE** of four. P1 — the literature review.

> Step **TWO** is the data strategy, on May 18.

> Step **THREE** is the pipeline and the code, in June.

> Step **FOUR** is the term paper and the final defence, in July.

**(pause — look at the audience)**

*[Point at the left box — RISK TO WATCH.]*

> The risk I am watching is **training-data contamination** of Clotho *(say: KLOTH-oh)*. I will audit the Falcon3-Audio data manifest in P2.

*[Point at the right box — OPEN QUESTION.]*

> The open question I am most curious about — do all three LALMs fail polyphony in the same way, or does each one fail differently?

**(short pause — smile — look at Prof. Abeßer)**

> Thank you. I am happy to take your questions.

*[STOP. Stay near the screen. Do NOT walk back to your seat. Wait for questions.]*

**Safety line if you freeze:** *"Today is step one of four. The risk is contamination. The open question is whether the three LALMs fail polyphony in the same way. Thank you."*

---

# SLIDE 6 — References (only show if asked)

**You only show this if a professor asks for sources during Q&A.**

> These are the 10 papers I cite in this talk. I shortlisted them from the 38 papers I read in this phase. The full 49-paper corpus is in my project wiki.

*[Click back to Slide 5 after the question is answered.]*

---

# 🟡 If you are running too long — emergency cuts

If you reach **Slide 3 already past 02:30**, here is what to skip:

| Slide | What to cut                                                                                            | Time saved |
| :---- | :----------------------------------------------------------------------------------------------------- | :--------: |
| 3     | Drop streams 5 and 6 — say*"plus two smaller streams: domain extensions and dataset governance."*   |   20 sec   |
| 4     | Drop SALMONN's one-line description and the metric explanations under each RQ. Just say the RQ titles. |   25 sec   |
| 5     | Drop the open-question line. Keep risk + thank-you.                                                    |   10 sec   |

**Total possible save: about 55 seconds.**

**NEVER cut these things:**

- The three research questions on Slide 4 (just shorten them).
- The words *Clotho*, *Falcon3-Audio*, *MACE*.
- The closing **"Thank you. I am happy to take your questions."**

---

# 🔴 Pronunciation cheat box

Stick this in your pocket. If you forget how to say a word, look here.

| Word on slide        | Say it like this                                        |
| :------------------- | :------------------------------------------------------ |
| polyphony            | po-**LIH**-fo-nee                                 |
| Falcon3-Audio        | **FAL**-kon-three-**AW**-dee-oh             |
| SALMONN              | **SAL**-monn (one word)                           |
| Qwen2.5-Omni         | **KWEN**-two-point-five-**OM**-nee          |
| Clotho               | **KLOTH**-oh                                      |
| SPIDEr-FL            | **SPI**-der-F-L (spell out F-L)                   |
| CIDEr                | **SY**-der                                        |
| MACE                 | **MAYS**                                          |
| CHAIR-audio          | **CHAIR** (like furniture) — **AW**-dee-oh |
| Δ MACE (delta MACE) | **DEL**-ta MAYS                                   |
| Falcon3              | FAL-kon-three                                           |
| ekphrasis            | **EK**-fra-sis (only if a professor asks)         |

---

# 🟢 Body language — keep this in your head

1. **Smile** before slide 1. Smile after slide 5.
2. **Stand to the SIDE of the screen** — never block the slides.
3. **Look at three faces** — front-left, centre, front-right. Rotate every 10 seconds.
4. **Pause for 2 seconds** before you click. Silence reads as confidence.
5. **Keep hands at waist level**, palms a little visible. NO pockets. NO crossed arms.
6. Do NOT read the slide word-for-word. Use your own slightly different words.
7. After the closing — **STAY** near the screen for Q&A. Do not return to your seat.

---

# 🟣 The first 30 seconds, in your sleep

Before you walk to the front, say this whole opener once silently in your head:

> *"Good morning, everyone. My project is called Audio-to-Text Captioning using Large Audio-Language Models. The course code is T6. The simple idea — the model listens to a sound clip and writes a sentence about it. The big question is — can these models describe sounds that overlap? In the next five minutes, I will show you four things: the task, the papers I read, the models I compare, and the plan."*

That is roughly 70 words. About 35 seconds. If you remember this opener, the rest will follow.

---

# 🔵 Dry-run timing log (write down your two practice runs)

| Slide           |   Target end   |         Run 1         |         Run 2         | Note                                  |
| :-------------- | :-------------: | :-------------------: | :-------------------: | :------------------------------------ |
| 1               |      00:35      |      **:**      |      **:**      | Smile. Mention T6 to anchor.          |
| 2               |      01:50      |      **:**      |      **:**      | Don't read the italic sentence twice. |
| 3               |      03:15      |      **:**      |      **:**      | The big content slide — slow down.   |
| 4               |      04:15      |      **:**      |      **:**      | Three RQs. RQ2 is the star.           |
| 5               |      04:40      |      **:**      |      **:**      | Eye contact at "Thank you."           |
| **TOTAL** | **04:40** | ****:**** | ****:**** | Aim 4:30–4:45. Never go past 5:00.   |

---

# 🩵 If a question makes you panic — say one of these

1. **"Could you say the question again, please?"** *(buys 3 seconds)*
2. **"That is a good question. Let me think for a moment."** *(buys 5 seconds)*
3. **"I have not measured this yet. My current plan is to handle it in P2."** *(safe fallback)*
4. **"I am not sure of the exact number, but the related paper is [Author, Year]. I can email you the link."** *(shows you know the literature)*

**Last rule:** when in doubt, **smile, breathe, speak slowly**. Confidence is 70 % delivery and 30 % content.

---

**Good luck. You have done the work. Now just deliver it.**
