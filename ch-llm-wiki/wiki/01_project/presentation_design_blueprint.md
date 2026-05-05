---
title: Presentation Design Blueprint (P1)
type: design-spec
status: active
created: 2026-05-04
tags: [presentation, design, blueprint, aesthetics]
---

# 🎨 P1 Presentation Design Blueprint
**Target Audience**: Academic Professors (Prof. Abeßer)
**Vibe**: "Premium Acoustic Cybernetic." Deep, authoritative, highly technical, yet visually breathtaking. It must look like a keynote from a top-tier AI lab (e.g., DeepMind or OpenAI).

*(Feed this document directly into Claude/Codex with the `p1_presentation_script.md` to generate the presentation code in Marp, Reveal.js, or HTML/CSS).*

---

## 1. Global Design System (The "Acoustic Dark Mode")

### 🎨 Color Palette
- **Background**: Deep Midnight (`#0A0E17`) - Gives a premium, OLED-like infinite depth.
- **Surface/Cards**: Glassmorphism dark slate (`#151A28` with 40% opacity, 10px backdrop blur, subtle 1px white/10% border).
- **Primary Accent (Audio)**: Neon Cyan (`#00F0FF`) - Represents clean, traditional acoustic signals.
- **Secondary Accent (LLMs)**: Electric Magenta (`#FF007A`) - Represents the neural network/language generation.
- **Text (Primary)**: Off-White (`#F0F4F8`)
- **Text (Muted)**: Steel Gray (`#8A9BB3`)

### 🔤 Typography
- **Headings**: `Space Grotesk` (Weight: 700) - Gives a sharp, futuristic, computational feel.
- **Body Text**: `Inter` (Weight: 400/500) - Maximum readability for dense academic text.
- **Code/Metrics**: `JetBrains Mono` - For citing metric names (e.g., `SPIDEr-FL`, `MACE`).

### 🎇 Global Elements
- **Micro-animations**: Slide transitions should be smooth "Fade and Scale" (105% to 100%).
- **Corner branding**: A subtle glowing audio waveform in the bottom left corner of every slide, pulsing gently.

---

## 2. Slide-by-Slide Visual Layouts

### 🟢 Slide 1: Topic Intro, Applications & Challenges
- **Layout Split**: 40% Left (Text) / 60% Right (Visual).
- **Background**: A very faint, slow-moving abstract data particle background.
- **Text Area**: Title in bold `Space Grotesk`. "Automated Audio Captioning" in white, with the word "Captioning" highlighted in **Neon Cyan**.
- **Hero Visual (Right)**: A high-fidelity, jaw-dropping graphic showing a raw, jagged audio waveform (Cyan) feeding into a glowing neural network node, outputting a glowing text string (Magenta): *"A dog barks in the distance..."*
- **Challenge Callout**: A glassmorphic card overlapping the bottom right that says "CORE CHALLENGE: POLYPHONY" with a warning glow (Amber/Orange `#FFAB00`).

### 🟢 Slide 2: Literature Search Methodology
- **Layout**: Center-aligned hero diagram.
- **Hero Visual**: A glowing, horizontal funnel diagram.
  - **Stage 1 (Left)**: 4 Floating glass logos (IEEE, ACM, arXiv, Scholar) feeding into a wide funnel mouth.
  - **Stage 2 (Middle)**: A glowing filter ring labeled with floating keywords in `JetBrains Mono`: `"Large Audio-Language Models" AND "Polyphony"`.
  - **Stage 3 (Right)**: The funnel narrows into a brilliant glowing orb labeled **"49 High-Impact Papers (2024-2026)"**.
- **Typography**: Keep text minimal. The funnel graphic must dominate the slide and communicate the strict filtering process instantly.

### 🟢 Slide 3: Main Stream 1 - Traditional Baselines
- **Layout**: 3-Column Grid.
- **Visuals**: Three vertical glassmorphic cards hovering over the dark background.
  - **Card 1**: `CNN14` (DCASE Gold Standard). Subtle blue glow.
  - **Card 2**: `AST` (Audio Spectrogram Transformer). Subtle cyan glow.
  - **Card 3**: `EnCLAP` (Contrastive Audio-Text). Subtle teal glow.
- **Details**: Inside each card, use a minimalist iconography (e.g., a grid for CNN, a spectrogram wave for AST) and exactly 2 bullet points of text. 

### 🟢 Slide 4: Main Stream 2 - The LALM Era
- **Layout**: "Evolutionary Tech Tree" or "VS" Layout.
- **Visuals**: A horizontal timeline or connected node graph showing the leap from traditional to LALMs.
- **Nodes**: 
  - Central, largest node: **Falcon3-Audio** (Glowing Magenta, signifying it as the primary target).
  - Branching nodes: **SALMONN** and **Qwen2.5-Omni** (Muted purple glows, secondary targets).
- **Aesthetic touch**: Connect the nodes with animated, flowing energy lines (like synapses firing) to represent the massive parameter scale of these models.

### 🟢 Slide 5: Main Stream 3 - Data Strategy & Metrics
- **Layout**: 50/50 Split (Datasets vs. Metrics).
- **Left Side (Dataset)**: A sleek graphic of the **Clotho v2.1** logo or a stylized audio folder. Below it, a progress bar or density chart visually comparing `1 Caption (AudioCaps)` vs `5 Captions (Clotho)` to instantly justify the choice.
- **Right Side (Metrics)**: A striking visual equation. 
  - `SPIDEr-FL` = Fluency (White text)
  - `MACE` = Entity Hallucination (Highlighted in deep red/magenta to show it catches failures).
- **Vibe**: Highly analytical. Use a radar-chart silhouette in the background to imply rigorous multi-dimensional evaluation.

### 🟢 Slide 6: IEEE References (The "Academic Drop")
- **Layout**: Masonry or dense 2-column grid.
- **Vibe**: Extremely clean and authoritative. No distracting graphics here.
- **Typography**: 
  - Title: "Top-10 Reference Shortlist" in glowing Cyan.
  - Body: Small, highly legible `Inter` font. 
  - Author names in white, Paper titles in muted steel gray, Venues (IEEE, ICASSP) highlighted in Cyan.
- **Effect**: It should look like a meticulously curated wall of academic proof that you can confidently leave on the screen during the 5-minute Q&A. 

---

## 3. Instructions for the AI Generator (Claude/Codex)
*Copy/paste this exact prompt to your AI generator alongside this blueprint:*

> "I need you to generate a presentation using [Marp Markdown / HTML & CSS / Reveal.js]. Read the `p1_presentation_script.md` for the text content, and strictly follow the design system and layouts specified in this `presentation_design_blueprint.md`. Use exactly the colors, fonts (Space Grotesk/Inter), and glassmorphism CSS effects requested. Do not hallucinate extra text. Ensure the slide transitions and UI elements look incredibly premium, dark-mode, and academic."
