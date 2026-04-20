# Manual Literature Rebuild Guide — CH-Proj-M

**Project:** Audio-to-Text Captioning using Large Audio-Language Models (LALMs)
**Use case:** manual paper search, source reacquisition, and literature-review rebuilding
**Goal:** rebuild the literature base in a way that is academically defensible, easy to follow, and aligned with Prof. Abeßer’s literature-research method

---

## 1. Non-negotiable rules

### 1.1 Citation priority

Use this priority order when deciding what to keep and what to cite:

1. **Peer-reviewed journal articles** (e.g., TISMIR, IEEE TASLP)
2. **Peer-reviewed conference papers** (e.g., ISMIR, DAFx, ICMC, IEEE ICASSP, WASPAA). *Check the impact factor (h5-index/h5-median) of unfamiliar conferences.*
3. **Official benchmark / dataset / model documentation**
4. **Survey / review / tutorial papers from reputable venues**
5. **arXiv preprints only as fallback** when no proper published version exists

### 1.2 arXiv rule

arXiv is **not** equal in credibility to peer-reviewed work.

Use arXiv for:

- discovery
- very recent frontier work
- temporary fallback when no published version exists yet

Do **not** prefer arXiv if a proper conference or journal version exists.

### 1.3 Search rule

Every major source search should follow this order:

1. Google Scholar
2. IEEE Xplore
3. reverse citation search
4. survey/review paper search
5. only then controlled arXiv fallback

### 1.4 Review-writing rule

The literature review must not become a pile of isolated paper summaries.

It must:

- define the topic and scope clearly
- group literature by themes / methods / gaps / disagreements
- discuss strengths and limitations (and identify areas for further research)
- relate prior work directly to the project’s research questions (how did they influence, support, or motivate this research?)
- synthesize trends instead of listing papers one by one
- **Where applicable, use tables, figures, or flowcharts to summarize and compare key information.**

---

## 2. What I am rebuilding

This literature rebuild has two parallel tracks:

### Track A — Reacquire the sources already used

Before searching for new papers, I will manually recollect the sources already used in the current project ecosystem.

### Track B — Search for missed but important papers

After the current evidence base is reacquired, I will search for:

- missing peer-reviewed versions
- stronger review/survey papers
- adjacent-field papers earlier AI searches may have missed
- better benchmark / metric / failure-mode literature

---

## 3. Current evidence base — what to reacquire first

These are the highest-priority currently used sources that should be recollected first.

### 3.1 Primary project pillars

These are load-bearing for the project and must be reacquired first.

1. **AF3 / Audio Flamingo 3**Alias in current docs: `Goel 2025`, `Ghosh 2025b`Why: primary model for RQ0–RQ4Status: major pillar, but still a preprint in current system
2. **SALMONN**Why: main comparison LALM
3. **Qwen2.5-Omni**Why: optional comparison / ablation model
4. **Clotho**Why: canonical AAC benchmark and main evaluation dataset
5. **AudioCaps**Why: main hallucination stimulus set / auxiliary dataset
6. **DCASE 2024 Task 6 baseline / Labbeti 2024**Why: supervised comparison floor (29.6% SPIDEr-FL)
7. **FENSE**Why: metric justification
8. **LAION-CLAP / CLAPScore source**Why: RQ5 and reference-free evaluation logic
9. **Kuan 2024 hallucination paper**Why: hallucination framing backbone
10. **TAC / Kumar 2026**
    Why: temporal grounding / RQ4 protocol

### 3.2 Core methodological sources

1. **Mei 2022 AAC survey**
2. **Gemmeke 2017 AudioSet**
3. **Rohrbach 2018 CHAIR**
4. **Holm 1979**
5. **Efron & Tibshirani 1993**
6. **Wohlin 2012**
7. **Kerr 1998**

### 3.3 Humanities and CH framing

1. **Schafer 1977**
2. **Heffernan 1993**
3. **Truax 1984**
4. **Augoyard & Torgue 2006**
5. **Sterne 2012**
6. **Born 2013**
7. **Mitchell 1986**

### 3.4 RQ5 / accessibility / archive support still weak

These need explicit reacquisition because they were flagged as incomplete or deferred in the current system:

1. **WCAG 2.1 AA**
2. **DARIAH-EU Strategic Plan**
3. **British Library Sound Archive**
4. **BBC Sound Effects Archive**
5. **Europeana Sounds**

---

## 4. Reacquisition workflow for every source

Use this exact process for every important source.

### Step 1 — Find the best version

Search in this order:

1. Google Scholar
2. IEEE Xplore
3. **ISMIR Explorer** (https://ismir-explorer.ai.ovgu.de/app/)
4. official publisher / venue page
5. official dataset / benchmark / model page
6. arXiv only if no proper published version exists

### Step 1.5 — The Two-Pass Reading Protocol

Before committing a paper:
- **Pass 1 (Skim):** Read Introduction, Conclusion, Figures, and Tables.
- **Pass 2 (Detailed - if promising):** Read Methodology and Evaluation & Results.

### Step 2 — Check if a preprint was later published

For every preprint:

- search the exact title in Google Scholar
- check “all versions”
- check venue pages (IEEE, ACL, ISMIR, OpenReview, ISCA, etc.)
- if a published version exists, use that instead

### Step 3 — Save properly

For every accepted source:

- save PDF or official page
- save full citation metadata / BibTeX
- rename consistently (e.g., using the BibTeX key)
- write short bullet-point notes (and mark passages directly in the PDF)
- record what this source supports in the project

### Step 4 — Categorize it

Put every source into one or more buckets:

- task / benchmark
- dataset
- model
- metric
- failure mode
- contamination / reproducibility
- statistics / methods
- humanities framing
- accessibility / archives

### Step 5 — Decide what to do with it

Each source gets one action:

- keep as peer-reviewed
- keep as official benchmark / dataset / model doc
- keep as preprint but mark cautiously
- replace arXiv with venue version
- downgrade / use cautiously
- remove if unsupported

---

## 5. Search themes

Use these themes to structure the search.

| Theme                                | Why it matters                        | What I am trying to find                             | Best first stop |
| ------------------------------------ | ------------------------------------- | ---------------------------------------------------- | --------------- |
| AAC task definition & benchmark      | defines task and canonical evaluation | benchmark papers, DCASE reports, dataset papers      | IEEE Xplore     |
| Traditional AAC                      | historical baseline before LALMs      | encoder-decoder AAC, pre-LLM methods                 | IEEE Xplore     |
| LALM-based AAC                       | current model family under test       | AF3, SALMONN, Qwen-type work                         | Google Scholar  |
| Audio encoders / representations     | architecture claims and lineage       | Whisper, BEATs, CLAP, unified encoders               | IEEE Xplore     |
| Metric validity                      | whether metrics are defensible        | FENSE, SPIDEr-FL, CLAPScore, human-correlation work  | IEEE Xplore     |
| Hallucination / grounding            | RQ3 backbone                          | hallucination, faithfulness, grounding literature    | Google Scholar  |
| Contamination / reproducibility      | RQ0 backbone                          | overlap, leakage, audit, benchmark integrity         | Google Scholar  |
| Temporal grounding / event order     | RQ4 backbone                          | timestamped captioning, temporal reasoning           | IEEE Xplore     |
| Polyphony / overlapping sounds       | RQ2 backbone                          | polyphonic SED, overlapping events                   | IEEE Xplore     |
| Humanities / sound studies           | CH framing                            | ekphrasis, soundscape, sound studies                 | Google Scholar  |
| Accessibility / archive access       | RQ5 justification                     | WCAG, BLV access, sound archives                     | Google Scholar  |
| Cultural heritage / digital archives | RQ5 applied context                   | DARIAH, BL, BBC, Europeana, metadata and findability | Google Scholar  |

---

## 6. High-yield exact search queries

---

### 6.1 AAC task and benchmark

**Google Scholar**

- `"automated audio captioning" survey`
- `"audio captioning" benchmark Clotho`
- `"DCASE" "task 6" audio captioning`
- `"AudioCaps" captioning dataset`
- `"automated audio captioning" review`

**IEEE Xplore**

- `("Document Title":"automated audio captioning")`
- `("Abstract":"audio captioning" AND "Clotho")`
- `("All Metadata":"DCASE" AND "task 6")`

---

### 6.2 Traditional AAC

**Google Scholar**

- `"audio captioning" transformer`
- `"audio captioning" encoder-decoder`
- `"audio captioning" PANN`
- `"audio captioning" HTSAT`
- `"audio captioning" reinforcement learning`

**IEEE Xplore**

- `("Abstract":"audio captioning" AND "transformer")`
- `("Abstract":"audio captioning" AND "encoder-decoder")`
- `("Abstract":"audio captioning" AND ("PANN" OR "HTSAT"))`

---

### 6.3 LALM / audio-language models

**Google Scholar**

- `"large audio-language model" captioning`
- `"audio LLM" captioning`
- `"audio understanding" benchmark LLM`
- `"audio language model" survey`
- `"Audio Flamingo" SALMONN Qwen audio`

**IEEE Xplore**

- `("Document Title":"large audio-language model")`
- `("Abstract":"audio-language model" AND captioning)`
- `("Abstract":"multimodal large language model" AND audio)`

---

### 6.4 Hallucination / grounding

**Google Scholar**

- `"hallucination" "audio language model"`
- `"hallucination" "audio captioning"`
- `"faithfulness" "audio caption"`
- `"grounding" "audio language model"`
- `"sound event hallucination"`

**IEEE Xplore**

- `("Abstract":"hallucination" AND ("audio" OR "audio-language"))`
- `("Abstract":"grounding" AND "audio language model")`
- `("Abstract":"faithfulness" AND audio AND caption)`

---

### 6.5 Contamination / leakage / reproducibility

**Google Scholar**

- `"data contamination" benchmark LLM`
- `"benchmark contamination" audio`
- `"training data overlap" Clotho AudioCaps`
- `"test set leakage" multimodal`
- `"reproducibility" "audio captioning"`

**IEEE Xplore**

- `("Abstract":"reproducibility" AND "audio captioning")`
- `("Abstract":"training data" AND ("AudioSet" OR "Clotho") AND overlap)`
- `("Abstract":"benchmark contamination" AND audio)`

---

### 6.6 Temporal grounding / sequencing

**Google Scholar**

- `"timestamped audio captioning"`
- `"temporal grounding" audio`
- `"event order" audio captioning`
- `"dense audio captioning"`
- `"audio question answering" temporal`

**IEEE Xplore**

- `("Abstract":"timestamp" AND "audio captioning")`
- `("Abstract":"temporal reasoning" AND audio)`
- `("Abstract":"sound event localization" AND captioning)`

---

### 6.7 Polyphony / overlapping sounds

**Google Scholar**

- `"polyphonic sound event detection" survey`
- `"overlapping sound events" audio`
- `"polyphony" "audio captioning"`
- `"sound event detection" review`

**IEEE Xplore**

- `("Document Title":"polyphonic sound event detection")`
- `("Abstract":"overlapping" AND "sound event")`
- `("All Metadata":"DCASE" AND "task 4")`

---

### 6.8 Humanities / sound studies

**Google Scholar**

- `"ekphrasis" sound`
- `"sonic ekphrasis"`
- `"soundscape" Schafer soundmark`
- `"sound studies" handbook`
- `"verbal description" "non-verbal" sound`

**IEEE Xplore**

- low yield — use Scholar first

---

### 6.9 Accessibility / archives / cultural heritage

**Google Scholar**

- `"audio description" blind low vision`
- `"WCAG 2.1" audio`
- `"sound archive" digital humanities`
- `"British Library" sound archive`
- `"Europeana Sounds"`
- `"BBC sound effects archive"`
- `"DARIAH" sound humanities`

**IEEE Xplore**

- `("Abstract":"audio description" AND ("blind" OR "low vision"))`
- `("Abstract":"audio archive" AND metadata)`

---

## 7. Queries most likely to recover papers earlier AI searches missed

### Blind spot A — papers that do not say “audio captioning”

Use:

- `"audio understanding" benchmark LLM`
- `"audio reasoning" benchmark`
- `"multimodal large language model" audio evaluation`

### Blind spot B — papers about evaluation validity, not model design

Use:

- `"audio captioning" "human evaluation"`
- `"reference-free" audio caption evaluation`
- `"caption metric" reliability human judgment`
- `"FENSE" audio captioning`
- `"CLAPScore" audio evaluation`

### Blind spot C — papers from neighboring fields

Use:

- `"polyphonic sound event detection" survey`
- `"overlapping sound events" detection`
- `"audio-visual" temporal grounding`
- `"object hallucination" image captioning CHAIR`
- `"POPE" hallucination benchmark`

### Blind spot D — humanities / archive / accessibility papers hidden from ML-style search

Use:

- `"sound archive" metadata access`
- `"digital humanities" sound archive`
- `"audio description" accessibility standards`
- `"sound studies" handbook`
- `"acoustic ecology" Schafer`

---

## 8. Survey / review / tutorial search block

These are especially important because Prof. Abeßer explicitly recommends survey/review-style sources and reverse literature research. *(Tip: Look for articles around 8-12 pages, as they tend to offer a more comprehensive review).*

### AAC / audio-language / metrics / polyphony

**Google Scholar**

- `"automated audio captioning" survey`
- `"audio captioning" tutorial`
- `"audio language model" survey`
- `"sound event detection" survey`
- `"polyphonic sound event detection" review`
- `"audio captioning evaluation" review`

**IEEE Xplore**

- `("Document Title":"survey" AND "audio captioning")`
- `("Document Title":"review" AND "sound event detection")`
- `("Abstract":"survey" AND "audio language model")`

### Humanities / archive access

**Google Scholar**

- `"sound studies" handbook`
- `"sound studies" companion`
- `"digital humanities" sound survey`
- `"audio description" review accessibility`

---

## 9. Reverse citation chasing seeds

Use these as the starting anchor set.

| Seed                | Why it is useful                     |
| ------------------- | ------------------------------------ |
| Clotho              | core AAC benchmark anchor            |
| AudioCaps           | auxiliary AAC dataset anchor         |
| Mei 2022 AAC survey | historical backbone and citation map |
| DCASE 2024 baseline | canonical benchmark floor            |
| SALMONN             | early LALM architecture anchor       |
| AF3                 | primary model anchor                 |
| FENSE               | metric validity anchor               |
| LAION-CLAP          | CLAPScore / representation anchor    |
| Kuan 2024           | hallucination framing anchor         |
| TAC                 | temporal grounding anchor            |
| Schafer 1977        | humanities framing anchor            |

For each seed:

- search backward: what does it cite?
- search forward: who cites it?
- prioritize 2020–2026 forward citations for technical work
- prioritize foundational backward citations for humanities/theory work

---

## 10. Practical working routine

### Pass 1 — Reacquire current evidence

Start with the currently used sources.
Do not search for novelty first.
Stabilize the evidence base first.

### Pass 2 — Search by theme

Use the search themes and query blocks above.

### Pass 3 — Check preprints properly

For every important preprint:

- search for venue version
- replace arXiv if a proper conference/journal version exists

### Pass 4 — Build structured notes (Matrix Method)

For every source, build structured notes that can cleanly translate into comparison tables.

**Standard criteria:**
- citation
- source type
- what it supports
- theme
- trust level
- whether it replaces a weaker source
- whether it should go into the wiki

**Comparison Matrix items (per Prof. Abeßer's guidance):**
Think of categories to compare different methods which will structure your related work later. E.g., track the `Feature | Dataset | Model` for each paper so they can be dropped straight into a markdown table.

### Pass 5 — Rebuild the related work section

Only after the source set is recollected and cleaned:

- group papers by theme
- synthesize trends
- identify gaps
- connect them to the project RQs

---

## 11. Final principle

This literature rebuild is **not** about collecting as many papers as possible.

It is about collecting:

- the **right** papers
- from the **right** venues
- with the **right** citation priority
- and then rebuilding the literature review in a way that is:
  - peer-reviewed first
  - theme-based
  - method-aware
  - gap-oriented
  - aligned with the actual project
