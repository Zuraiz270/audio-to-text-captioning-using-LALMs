---
title: AF-CLAP / AF-Whisper — Audio-Flamingo unified encoder
type: concept
tags: [encoder, audio-flamingo, clap, primary-architecture]
status: stub
last_reviewed: 2026-04-20
sources: [../08_sources/goel-2025-af3.md, ../08_sources/paper-summaries-legacy.md]
---

## AF-CLAP / AF-Whisper

The audio encoder used by Audio Flamingo 3. Project drafts use both names because the lineage shifted between AF2 and AF3:

- **AF2 era:** "AF-CLAP" — a CLAP-style contrastive audio encoder.
- **AF3 era (per Goel 2025 abstract):** "AF-Whisper" — a *unified* encoder trained jointly across speech, sound, and music using a novel joint-representation strategy. Per the AF3 abstract, AF-Whisper is the encoder; "AF-CLAP" appears in earlier project notes as a carry-forward label.

This page exists because earlier wiki pages and root docs referenced "AF-CLAP" without a dedicated card. Treat the term as a **historical pointer**: "AF-CLAP / AF-Whisper unified encoder" is the precise object across project documents.

### What it is

- Single audio encoder for AF3, replacing the dual-encoder design of SALMONN (Whisper + BEATs).
- Trained for joint representation across all 3 audio modalities (speech, sound, music).
- Feeds the Q-Former-style adapter into the LLM decoder.

### Why it matters here

- **RQ2 polyphony:** the unified-encoder + Q-Former pipeline is the candidate adapter-layer bottleneck for concurrent-event under-description.
- **Naming hygiene:** any wiki page or root doc using "AF-CLAP" should now cross-link here, so the AF2 → AF3 encoder transition is explicit rather than silent.

### Open questions

- Exact AF-Whisper training-data enumeration is contingent on the AF3 HuggingFace data card (Q1 in [`research_notes.md`](../../../research_notes.md) — WAITING-ON-REFETCH).
- Whether AF-Whisper representations explicitly encode concurrency (separable channels per source) or a mixed embedding is not stated in the abstract; this is the mechanism RQ2 indirectly probes.

### Sources

- [goel-2025-af3](../08_sources/goel-2025-af3.md) — primary card for the AF3 paper, in which AF-Whisper is named.
- [paper-summaries-legacy](../08_sources/paper-summaries-legacy.md) — Papers 7 (AF2) and 8 (AF3) for the AF-CLAP → AF-Whisper lineage.

### Cross-links

- [audio-flamingo-3.md](audio-flamingo-3.md)
- [polyphony-under-description.md](../06_failure_modes/polyphony-under-description.md)
