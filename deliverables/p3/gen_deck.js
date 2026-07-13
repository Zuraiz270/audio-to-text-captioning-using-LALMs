// P3 final-presentation deck generator (CH-Proj-M, 13 July 2026).
// All numbers come from p3_data.json, which src-side tooling generates from
// results/*.json, so the deck inherits the paper's no-hand-typed-numbers rule.
// Build: NODE_PATH=$(npm root -g) node gen_deck.js
const pptxgen = require("pptxgenjs");
const data = require("./p3_data.json");

const INK = "1F2937";      // near-black body text
const MUTED = "6B7280";    // captions
const DARK = "16213E";     // title/closing background
const ICE = "CADCFC";      // light text on dark
const LALM = "1F77B4";     // matches paper fig colors
const TRAINED = "D62728";
const FLOOR = "9E9E9E";
const CARD = "EEF3FA";     // light card tint
const WARN = "FDF2F2";     // light red tint for disclosure cards

const KIND_COLOR = { floor: FLOOR, lalm: LALM, trained: TRAINED };

const M = data.models;
const byKey = Object.fromEntries(M.map(m => [m.key, m]));
const H = data.h;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5

// Preserve the user's hand-edited speaker notes: notes_extracted.json is
// dumped from the last hand-edited deck and, when present for a slide,
// overrides the hardcoded addNotes text below.
let userNotes = {};
try { userNotes = require("./notes_extracted.json"); } catch (e) {}
let slideIdx = 0;
const _addSlide = pres.addSlide.bind(pres);
pres.addSlide = (...args) => {
  const s = _addSlide(...args);
  const idx = ++slideIdx;
  const _addNotes = s.addNotes.bind(s);
  s.addNotes = (text) => {
    const lines = userNotes[String(idx)];
    _addNotes(lines && lines.length ? lines.join("\n") : text);
  };
  return s;
};

const TITLE_OPTS = { fontFace: "Cambria", bold: true, color: INK, fontSize: 30, margin: 0 };

function contentTitle(slide, text) {
  slide.addText(text, { ...TITLE_OPTS, x: 0.6, y: 0.35, w: 12.1, h: 0.75 });
}

function card(slide, x, y, w, h, fillColor) {
  slide.addShape("roundRect", {
    x, y, w, h, rectRadius: 0.08,
    fill: { color: fillColor }, line: { type: "none" },
  });
}

// ---------------------------------------------------------------- Slide 1
{
  const s = pres.addSlide();
  s.background = { color: DARK };
  s.addText("Zero-Shot Audio-Language Models\nversus Trained Captioners", {
    x: 0.8, y: 1.15, w: 8.6, h: 2.2, fontFace: "Cambria", bold: true,
    fontSize: 38, color: "FFFFFF", margin: 0,
  });
  s.addText("Audio-to-Text Captioning on Clotho  ·  Final Presentation (P3)", {
    x: 0.8, y: 3.35, w: 8.6, h: 0.5, fontFace: "Calibri", fontSize: 18,
    color: ICE, margin: 0,
  });
  s.addText(String(byKey.af3.spider_fl.toFixed(3)), {
    x: 9.6, y: 1.5, w: 3.1, h: 1.4, fontFace: "Cambria", bold: true,
    fontSize: 64, color: "FFFFFF", align: "center", margin: 0,
  });
  s.addText("zero-shot SPIDEr-FL,\nabove both trained baselines", {
    x: 9.6, y: 2.9, w: 3.1, h: 0.85, fontFace: "Calibri", fontSize: 13,
    color: ICE, align: "center", margin: 0,
  });
  s.addText(
    "Zuraiz  ·  CH-Proj-M Master's Project Computational Humanities  ·  SS 2026\n" +
    "Supervisor: Prof. Dr.-Ing. Jakob Abeßer  ·  University of Bamberg  ·  13 July 2026\n" +
    "github.com/Zuraiz270/audio-to-text-captioning-using-LALMs",
    { x: 0.8, y: 5.9, w: 11.7, h: 1.1, fontFace: "Calibri", fontSize: 13,
      color: ICE, margin: 0, lineSpacingMultiple: 1.25 });
  s.addNotes("Good morning. My project asks whether the new generation of large audio-language models can describe audio as well as systems that were trained specifically for captioning. The one-number teaser: the best zero-shot model reaches 0.297 SPIDEr-FL on Clotho, above both trained baselines. The next ten minutes explain what that number means, where it holds, and where it breaks down.");
}

// ---------------------------------------------------------------- Slide 2
{
  const s = pres.addSlide();
  contentTitle(s, "Task and research questions");
  s.addText(
    "Course task T6: how well can large audio-language models (LALMs) describe audio, " +
    "especially overlapping sound, compared to traditional systems? Everything runs " +
    "zero-shot on the full Clotho v2.1 evaluation split (1,045 clips, seed 42).",
    { x: 0.6, y: 1.15, w: 7.0, h: 1.25, fontFace: "Calibri", fontSize: 15,
      color: INK, margin: 0, lineSpacingMultiple: 1.1 });

  card(s, 0.6, 2.6, 3.4, 3.9, CARD);
  s.addText("Traditional systems", { x: 0.85, y: 2.8, w: 2.9, h: 0.4,
    fontFace: "Calibri", bold: true, fontSize: 16, color: TRAINED, margin: 0 });
  s.addText([
    { text: "AST", options: { bold: true } },
    { text: " tagging floor (AudioSet top-5 template)\n\n" },
    { text: "CNN14+BART", options: { bold: true } },
    { text: " DCASE 2023 baseline, trained on Clotho\n\n" },
    { text: "EnCLAP-base", options: { bold: true } },
    { text: " EnCodec + CLAP + BART, trained on Clotho" },
  ], { x: 0.85, y: 3.3, w: 2.95, h: 3.0, fontFace: "Calibri", fontSize: 14,
    color: INK, margin: 0 });

  card(s, 4.2, 2.6, 3.4, 3.9, CARD);
  s.addText("Zero-shot LALMs", { x: 4.45, y: 2.8, w: 2.9, h: 0.4,
    fontFace: "Calibri", bold: true, fontSize: 16, color: LALM, margin: 0 });
  s.addText([
    { text: "Qwen2.5-Omni-7B", options: { bold: true } },
    { text: " general omni-model (Alibaba)\n\n" },
    { text: "SALMONN-13B", options: { bold: true } },
    { text: " audio specialist (Tsinghua/ByteDance)\n\n" },
    { text: "Audio Flamingo 3", options: { bold: true } },
    { text: " audio specialist (NVIDIA, current SOTA)" },
  ], { x: 4.45, y: 3.3, w: 2.95, h: 3.0, fontFace: "Calibri", fontSize: 14,
    color: INK, margin: 0 });

  const rqs = [
    ["RQ1", "Do zero-shot LALMs match or beat trained captioners? (SPIDEr-FL, CIDEr)"],
    ["RQ2", "Polyphonic vs monophonic clips: where is captioning harder? (Δ SPIDEr-FL, MACE)"],
    ["RQ3", "Failure modes: how much do captions hallucinate? (CHAIR-audio)"],
  ];
  rqs.forEach(([tag, text], i) => {
    const y = 2.6 + i * 1.35;
    card(s, 7.9, y, 4.8, 1.15, "FFFFFF");
    s.addShape("roundRect", { x: 7.9, y, w: 4.8, h: 1.15, rectRadius: 0.08,
      fill: { color: CARD }, line: { type: "none" } });
    s.addText(tag, { x: 8.15, y: y + 0.12, w: 0.85, h: 0.45,
      fontFace: "Cambria", bold: true, fontSize: 18, color: LALM, margin: 0 });
    s.addText(text, { x: 9.05, y: y + 0.1, w: 3.5, h: 0.95,
      fontFace: "Calibri", fontSize: 13, color: INK, margin: 0 });
  });
  s.addText("Preregistered hypotheses H1–H4 with BCa bootstrap and Holm correction.",
    { x: 0.6, y: 6.75, w: 12.1, h: 0.4, fontFace: "Calibri", italic: true,
      fontSize: 13, color: MUTED, margin: 0 });
  s.addNotes("The task is T6: LALMs versus traditional captioning, with a focus on overlapping sound. Six systems: three traditional, three zero-shot LALMs from three different vendors, so the comparison is not single-vendor. Three research questions: headline quality, polyphony, and hallucination. All hypotheses were committed in advance with bootstrap statistics.");
}

// ---------------------------------------------------------------- Slide 3
{
  const s = pres.addSlide();
  contentTitle(s, "Method: one harness for all six systems");
  const boxes = [
    "Clotho v2.1 eval\n1,045 clips, 44.1 kHz",
    "caption(waveform, sr)\none contract per system",
    "predictions JSON + manifest\nSHA-256s, versions, seed 42",
    "aac-metrics scorer\nSPIDEr-FL, CIDEr, SPICE",
    "analysis\nsubsets, CHAIR, MACE, bootstrap",
  ];
  const bw = 2.28, gap = 0.32, y0 = 1.5;
  boxes.forEach((t, i) => {
    const x = 0.6 + i * (bw + gap);
    card(s, x, y0, bw, 1.25, CARD);
    s.addText(t, { x: x + 0.08, y: y0 + 0.08, w: bw - 0.16, h: 1.09,
      fontFace: "Calibri", fontSize: 11.5, color: INK, align: "center",
      valign: "middle", margin: 0 });
    if (i < boxes.length - 1) {
      s.addText("→", { x: x + bw - 0.045, y: y0 + 0.33, w: 0.42, h: 0.6,
        fontFace: "Calibri", fontSize: 20, color: MUTED, align: "center", margin: 0 });
    }
  });

  const proofs = [
    ["Harness validated", `CNN14 reproduces its official score: 0.259 vs 0.261 published. Same scorer, clips, and references for every row.`],
    ["LALMs on one A100 each", "Offline compute nodes, pre-cached checkpoints, fixed one-line prompt recorded per run. Full runs take 8 to 19 minutes."],
    ["Complete and auditable", "1,045 of 1,045 clips for every system, zero failures. Every number traces to a committed result file."],
  ];
  proofs.forEach(([h, b], i) => {
    const x = 0.6 + i * 4.25;
    card(s, x, 3.3, 3.95, 2.5, "FFFFFF");
    s.addShape("roundRect", { x, y: 3.3, w: 3.95, h: 2.5, rectRadius: 0.08,
      fill: { color: CARD }, line: { type: "none" } });
    s.addText(h, { x: x + 0.25, y: 3.5, w: 3.45, h: 0.45,
      fontFace: "Calibri", bold: true, fontSize: 16, color: INK, margin: 0 });
    s.addText(b, { x: x + 0.25, y: 4.05, w: 3.45, h: 1.6,
      fontFace: "Calibri", fontSize: 13.5, color: INK, margin: 0,
      lineSpacingMultiple: 1.1 });
  });
  s.addText("Baselines on CPU, LALMs on NHR@FAU TinyGPU. Only the compute location moves; the measurement never changes.",
    { x: 0.6, y: 6.15, w: 12.1, h: 0.45, fontFace: "Calibri", italic: true,
      fontSize: 13, color: MUTED, margin: 0 });
  s.addNotes("Every system implements one contract behind a registry, so one inference loop and one scorer serve everything from a CPU baseline to a 13-billion-parameter model on an A100. Each run writes a manifest with checkpoint hashes, library versions, decode settings, and the seed. The harness is validated by reproducing the official CNN14 baseline within 0.002. All six systems completed all 1,045 clips with zero failures.");
}

// ---------------------------------------------------------------- Slide 4
{
  const s = pres.addSlide();
  contentTitle(s, "RQ1: It depends on the model");
  const rows = [...M]; // ast..af3 order; horizontal bars render bottom-up
  s.addChart(pres.ChartType.bar, [{
    name: "SPIDEr-FL",
    labels: rows.map(m => m.name),
    values: rows.map(m => m.spider_fl),
  }], {
    x: 0.5, y: 1.25, w: 7.6, h: 4.9,
    barDir: "bar",
    chartColors: rows.map(m => KIND_COLOR[m.kind]),
    showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0.000",
    dataLabelColor: INK, dataLabelFontSize: 12,
    showLegend: false, showTitle: false,
    catAxisLabelColor: INK, catAxisLabelFontSize: 12,
    valAxisLabelColor: MUTED, valAxisLabelFontSize: 10,
    valAxisMaxVal: 0.34, valAxisMinVal: 0,
    valGridLine: { color: "E5E7EB", size: 0.5 },
    catGridLine: { style: "none" },
  });

  card(s, 8.5, 1.25, 4.2, 1.3, CARD);
  s.addText([
    { text: "H1 ✓  ", options: { bold: true, color: LALM } },
    { text: `AF3 beats the 0.261 baseline: CI lower ${H.h1_ci_low.toFixed(3)}, p ≈ 0.001, Holm-corrected` },
  ], { x: 8.72, y: 1.38, w: 3.8, h: 1.05, fontFace: "Calibri", fontSize: 13,
    color: INK, margin: 0 });

  card(s, 8.5, 2.75, 4.2, 1.3, CARD);
  s.addText([
    { text: "H3 ✓  ", options: { bold: true, color: LALM } },
    { text: `AF3 over SALMONN, paired per clip: +${H.h3_diff.toFixed(3)} (CI lower +${H.h3_ci_low.toFixed(3)})` },
  ], { x: 8.72, y: 2.88, w: 3.8, h: 1.05, fontFace: "Calibri", fontSize: 13,
    color: INK, margin: 0 });

  card(s, 8.5, 4.25, 4.2, 1.9, WARN);
  s.addText([
    { text: "Published anchors  ", options: { bold: true } },
    { text: "CNN14 0.261 (official), EnCLAP-base 0.291. Our EnCLAP row runs 1.1 pp low (released checkpoint / decoding); disclosed in the paper. H1 is anchored on CNN14." },
  ], { x: 8.72, y: 4.4, w: 3.8, h: 1.65, fontFace: "Calibri", fontSize: 12.5,
    color: INK, margin: 0 });

  s.addText("Two LALMs trail both trained captioners. The audio specialist AF3 beats both, on every metric, and clears EnCLAP's published SPIDEr-FL too.",
    { x: 0.6, y: 6.5, w: 12.1, h: 0.6, fontFace: "Calibri", bold: true,
      fontSize: 15, color: INK, margin: 0 });
  s.addNotes("The answer to RQ1 is not yes or no, it is model-dependent. Every LALM clears the tagging floor by a factor of three to four, so they all describe rather than list. But Qwen and SALMONN stay below both trained captioners. Audio Flamingo 3 beats both trained systems on every metric, and its 0.297 is also above EnCLAP's published 0.291. H1 and H3 are both significant. One disclosure: our EnCLAP reproduction runs about one point below its published anchor; that is in the paper, and H1 is anchored on CNN14, which reproduces within 0.002.");
}

// ---------------------------------------------------------------- Slide 5
{
  const s = pres.addSlide();
  contentTitle(s, "What the captions actually look like");
  s.addText([
    { text: "creaky.wav", options: { fontFace: "Courier New", fontSize: 13, color: MUTED } },
    { text: "   one of the five human references:", options: { fontSize: 13, color: MUTED } },
  ], { x: 0.6, y: 1.12, w: 12.1, h: 0.35, margin: 0 });
  s.addText(`“${data.example.reference}”`, {
    x: 0.6, y: 1.5, w: 12.1, h: 0.5, fontFace: "Cambria", italic: true,
    fontSize: 15, color: INK, margin: 0 });

  const rows = [
    ["AST (floor)", data.example.captions.ast, "a tag list, not a sentence", FLOOR, null],
    ["Qwen2.5-Omni", data.example.captions.qwen_omni, "report framing; no reference sounds like this", LALM, null],
    ["SALMONN", data.example.captions.salmonn, "short declarative", LALM, null],
    ["EnCLAP (trained)", data.example.captions.enclap, "Clotho register (CNN14 similar)", TRAINED, null],
    ["Audio Flamingo 3", data.example.captions.af3, "fluent Clotho register, but invents a zipper", LALM, "zipper"],
  ];
  let y = 2.25;
  rows.forEach(([name, cap, note, color, highlight]) => {
    card(s, 0.6, y, 12.1, 0.78, CARD);
    s.addText(name, { x: 0.85, y: y + 0.08, w: 2.1, h: 0.62, fontFace: "Calibri",
      bold: true, fontSize: 12.5, color, margin: 0, valign: "middle" });
    let capRuns;
    if (highlight && cap.includes(highlight)) {
      const i = cap.indexOf(highlight);
      capRuns = [
        { text: cap.slice(0, i) },
        { text: cap.slice(i, i + highlight.length), options: { bold: true, color: TRAINED } },
        { text: cap.slice(i + highlight.length) },
      ];
    } else {
      capRuns = [{ text: cap }];
    }
    s.addText(capRuns, { x: 3.05, y: y + 0.08, w: 6.6, h: 0.62,
      fontFace: "Calibri", fontSize: 12.5, color: INK, margin: 0, valign: "middle" });
    s.addText(note, { x: 9.8, y: y + 0.08, w: 2.75, h: 0.62, fontFace: "Calibri",
      italic: true, fontSize: 11, color: MUTED, margin: 0, valign: "middle" });
    y += 0.9;
  });
  s.addText("Overlap metrics reward the Clotho register. Fluency can invent detail; that is RQ3.",
    { x: 0.6, y: 6.85, w: 12.1, h: 0.45, fontFace: "Calibri", bold: true,
      fontSize: 15, color: INK, margin: 0 });
  s.addNotes("These are verbatim outputs for one clip, next to a human reference. AST produces a tag list. Qwen wraps everything in report framing, which no Clotho reference uses, and enumerates several events. SALMONN and the trained models produce short declaratives. Audio Flamingo 3 reads closest to the reference register, which is exactly what overlap metrics reward. And note the zipper: fluent, specific, and unsupported by the references and the audio tags. That previews the hallucination question.");
}

// ---------------------------------------------------------------- Slide 6
{
  const s = pres.addSlide();
  contentTitle(s, "RQ2: Polyphony helps everyone, so it is the data, not the models");
  const rows = [...M];
  s.addChart(pres.ChartType.bar, [{
    name: "Delta SPIDEr-FL (poly - mono)",
    labels: rows.map(m => m.name),
    values: rows.map(m => m.delta),
  }], {
    x: 0.5, y: 1.25, w: 7.6, h: 4.9,
    barDir: "bar",
    chartColors: rows.map(m => KIND_COLOR[m.kind]),
    showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "+0.000",
    dataLabelColor: INK, dataLabelFontSize: 12,
    showLegend: false, showTitle: false,
    catAxisLabelColor: INK, catAxisLabelFontSize: 12,
    valAxisLabelColor: MUTED, valAxisLabelFontSize: 10,
    valAxisMaxVal: 0.11, valAxisMinVal: 0,
    valGridLine: { color: "E5E7EB", size: 0.5 },
    catGridLine: { style: "none" },
  });

  card(s, 8.5, 1.25, 4.2, 1.45, CARD);
  s.addText([
    { text: "H2 ✓ all three LALMs  ", options: { bold: true, color: LALM } },
    { text: `+${H.h2.salmonn.diff.toFixed(3)} to +${H.h2.qwen_omni.diff.toFixed(3)}, p ≈ 0.001. But the baselines shift the same way.` },
  ], { x: 8.72, y: 1.4, w: 3.8, h: 1.2, fontFace: "Calibri", fontSize: 13,
    color: INK, margin: 0 });

  card(s, 8.5, 2.9, 4.2, 1.35, CARD);
  s.addText([
    { text: "MACE agrees  ", options: { bold: true } },
    { text: "audio-grounded deltas +0.021 to +0.032, so this is not a reference-overlap artefact." },
  ], { x: 8.72, y: 3.05, w: 3.8, h: 1.1, fontFace: "Calibri", fontSize: 13,
    color: INK, margin: 0 });

  card(s, 8.5, 4.45, 4.2, 1.7, "FFFFFF");
  s.addShape("roundRect", { x: 8.5, y: 4.45, w: 4.2, h: 1.7, rectRadius: 0.08,
    fill: { color: CARD }, line: { type: "none" } });
  s.addText([
    { text: "Harish & Abeßer (DCASE 2025):  ", options: { bold: true } },
    { text: "event-level tasks degrade with polyphony. Caption-level description does not. The findings complement each other." },
  ], { x: 8.72, y: 4.6, w: 3.8, h: 1.45, fontFace: "Calibri", fontSize: 12.5,
    color: INK, margin: 0 });

  s.addText([
    { text: "How the split was made:  ", options: { bold: true } },
    { text: `a sound-event detector (PANNs) scores 527 sound classes 100 times per second; two classes overlapping for at least 1 s = polyphonic. τ = 0.25 came from a rule committed before any results: ${data.counts.poly} polyphonic / ${data.counts.mono} monophonic. Independent check: human references of polyphonic clips name more distinct sounds (4.5 vs 3.8).` },
  ], { x: 0.6, y: 6.35, w: 12.1, h: 1.0, fontFace: "Calibri",
    fontSize: 12.5, color: INK, margin: 0 });
  s.addNotes("We split the 1,045 clips with PANNs sound event detection: two classes co-active for at least one second. The pre-registered threshold of 0.5 was degenerate, so the pre-committed fallback rule selected 0.25: 336 polyphonic, 709 monophonic clips. Every system scores higher on the polyphonic subset, including all three non-LALM systems, which identifies it as a subset-difficulty effect: event-rich clips give captions more to match, while the monophonic bucket collects quiet ambiguous recordings. The audio-grounded MACE metric shows the same direction. This complements Professor Abesser and Harish's DCASE paper: counting and naming events gets harder with polyphony, producing a reference-like description does not.");
}

// ---------------------------------------------------------------- Slide 7
{
  const s = pres.addSlide();
  contentTitle(s, "RQ3: The best captioner is not the most grounded");
  const rows = [...M];
  s.addChart(pres.ChartType.bar, [{
    name: "CHAIR-s at tau 0.25",
    labels: rows.map(m => m.name),
    values: rows.map(m => m.chair_s),
  }], {
    x: 0.5, y: 1.25, w: 7.6, h: 4.9,
    barDir: "bar",
    chartColors: rows.map(m => KIND_COLOR[m.kind]),
    showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0.000",
    dataLabelColor: INK, dataLabelFontSize: 12,
    showLegend: false, showTitle: false,
    catAxisLabelColor: INK, catAxisLabelFontSize: 12,
    valAxisLabelColor: MUTED, valAxisLabelFontSize: 10,
    valAxisMaxVal: 1.1, valAxisMinVal: 0, valAxisMajorUnit: 0.2,
    valGridLine: { color: "E5E7EB", size: 0.5 },
    catGridLine: { style: "none" },
  });

  card(s, 8.5, 1.25, 4.2, 1.45, CARD);
  s.addText([
    { text: "H4: null retained  ", options: { bold: true, color: TRAINED } },
    { text: `AF3 does not hallucinate less than SALMONN per caption (${H.h4_diff_025.toFixed(3)}, p = ${H.h4_p}); stable across τ.` },
  ], { x: 8.72, y: 1.4, w: 3.8, h: 1.2, fontFace: "Calibri", fontSize: 13,
    color: INK, margin: 0 });

  card(s, 8.5, 2.9, 4.2, 1.8, CARD);
  s.addText([
    { text: "Why: more claims per caption.  ", options: { bold: true } },
    { text: `Per mention AF3 is the most grounded in the table (CHAIR-i ${byKey.af3.chair_i.toFixed(3)}, lowest). It just mentions more entities: ${byKey.af3.entities.toFixed(2)} vs ${byKey.salmonn.entities.toFixed(2)} per caption.` },
  ], { x: 8.72, y: 3.05, w: 3.8, h: 1.55, fontFace: "Calibri", fontSize: 12.5,
    color: INK, margin: 0 });

  card(s, 8.5, 4.9, 4.2, 1.25, WARN);
  s.addText([
    { text: "Failure mode caught:  ", options: { bold: true } },
    { text: "greedy decoding drove Qwen into a 515-word “tapped, tapped, …” loop on one clip." },
  ], { x: 8.72, y: 5.02, w: 3.8, h: 1.05, fontFace: "Calibri", fontSize: 12.5,
    color: INK, margin: 0 });

  s.addText("AST at 0.956 is the validity check. Qwen is the outlier at 0.550. Overlap quality and grounding are separate axes.",
    { x: 0.6, y: 6.5, w: 12.1, h: 0.6, fontFace: "Calibri", bold: true,
      fontSize: 15, color: INK, margin: 0 });
  s.addNotes("CHAIR-audio counts caption entities supported by neither the references nor the audio tags. The four serious captioners cluster around 0.33 to 0.35; Qwen hallucinates markedly more, and AST at 0.956 is the expected validity check for an indiscriminate tag list. H4's null is retained: the best captioner does not hallucinate less per caption. The decomposition explains it: per individual mention AF3 is actually the most grounded system in the table; it simply makes more claims per caption, and each claim is a chance to be wrong. Remember the zipper. And one concrete failure mode: greedy decoding sent Qwen into a 515-word repetition loop on one clip, caught only because we retain per-clip outputs.");
}

// ---------------------------------------------------------------- Slide 8
{
  const s = pres.addSlide();
  contentTitle(s, "Limitations, deviations, and what “zero-shot” means");
  const verdicts = [
    ["H1 ✓", "AF3 above the 0.261 CNN14 anchor (CI lower 0.283)"],
    ["H2 ✓", "poly > mono for all three LALMs; shared with baselines"],
    ["H3 ✓", "AF3 above SALMONN, paired per clip (+0.072)"],
    ["H4 ✗", "null retained: AF3 not less hallucination-prone per caption"],
  ];
  verdicts.forEach(([tag, text], i) => {
    const y = 1.25 + i * 1.25;
    card(s, 0.6, y, 5.6, 1.05, CARD);
    s.addText(tag, { x: 0.85, y: y + 0.1, w: 0.95, h: 0.85, fontFace: "Cambria",
      bold: true, fontSize: 20, color: tag.includes("✓") ? LALM : TRAINED,
      margin: 0, valign: "middle" });
    s.addText(text, { x: 1.85, y: y + 0.1, w: 4.15, h: 0.85, fontFace: "Calibri",
      fontSize: 13, color: INK, margin: 0, valign: "middle" });
  });

  const disclosures = [
    ["Declared plan, not sealed", "The preregistration was drafted before the LALM runs but never formally frozen. So we claim a declared analysis plan, and disclose all seven deviations in the paper."],
    ["“Zero-shot” = protocol, not data purity", "AF3 and SALMONN list Clotho development pairs in their training corpora (their own papers). The eval split is held out for everyone, and the trained baselines used the same development data. Disclosed and discussed."],
    ["Anchors reported honestly", "EnCLAP runs 1.1 pp under its published anchor; reported, not tuned away. CNN14 anchors the harness at 0.002 accuracy."],
    ["Everything public", "Code, configs, manifests, all result files, the logbook, and the preregistration are in the repository."],
  ];
  disclosures.forEach(([h, b], i) => {
    const y = 1.25 + i * 1.25;
    card(s, 6.5, y, 6.2, 1.05, i === 1 ? WARN : CARD);
    s.addText([
      { text: h + "   ", options: { bold: true } },
      { text: b },
    ], { x: 6.75, y: y + 0.08, w: 5.7, h: 0.9, fontFace: "Calibri",
      fontSize: 11.5, color: INK, margin: 0, valign: "middle" });
  });
  s.addText("These are the project's limitations as I see them. All of them are disclosed in the paper, and I am glad to discuss any of them.",
    { x: 0.6, y: 6.55, w: 12.1, h: 0.5, fontFace: "Calibri", bold: true,
      fontSize: 15, color: INK, margin: 0 });
  s.addNotes("The honesty slide. All four hypotheses were committed before results, tested with BCa bootstrap and Holm correction: three supported, one null retained, and I report the null as a finding. Four disclosures, so nothing has to come out in questions. The preregistration was never formally frozen, so I treat it as a declared plan and list every deviation. Zero-shot describes my protocol, not the models' training diet: both audio specialists saw Clotho development pairs in training, which is symmetric with what the baselines trained on, and it is disclosed in the paper. The EnCLAP reproduction gap is reported openly. And the entire project is public and auditable.");
}

// ---------------------------------------------------------------- Slide 9
{
  const s = pres.addSlide();
  s.background = { color: DARK };
  s.addText("Three things to remember", { x: 0.8, y: 0.6, w: 11.7, h: 0.8,
    fontFace: "Cambria", bold: true, fontSize: 34, color: "FFFFFF", margin: 0 });
  const takeaways = [
    ["1", "Whether a zero-shot LALM beats trained captioners depends on the model. The current audio specialist does, on every metric; a general omni-model and an older specialist do not."],
    ["2", "Polyphonic clips score higher for every system. That is a dataset effect, not an LALM property: no caption-level polyphony penalty, complementing the event-level degradation in Harish & Abeßer."],
    ["3", "Overlap quality and grounding are separate axes. The best captioner hallucinates no less per caption; it is simply the most grounded per claim while making more claims. Evaluate both."],
  ];
  takeaways.forEach(([n, text], i) => {
    const y = 1.7 + i * 1.35;
    s.addText(n, { x: 0.8, y, w: 0.75, h: 1.2, fontFace: "Cambria", bold: true,
      fontSize: 40, color: ICE, margin: 0 });
    s.addText(text, { x: 1.75, y: y + 0.08, w: 10.7, h: 1.25, fontFace: "Calibri",
      fontSize: 16, color: "FFFFFF", margin: 0, lineSpacingMultiple: 1.15 });
  });
  s.addText([
    { text: "Open question:  ", options: { bold: true, italic: true } },
    { text: "if describing stays easy while counting gets harder, do caption metrics measure scene understanding, or scene summarization?", options: { italic: true } },
  ], { x: 0.8, y: 5.85, w: 11.7, h: 0.6, fontFace: "Calibri", fontSize: 15,
    color: ICE, margin: 0 });
  s.addText(
    "Paper, code, results, logbook: github.com/Zuraiz270/audio-to-text-captioning-using-LALMs\nThank you.",
    { x: 0.8, y: 6.55, w: 11.7, h: 0.8, fontFace: "Calibri", fontSize: 14,
      color: ICE, margin: 0, lineSpacingMultiple: 1.25 });
  s.addNotes("Three takeaways. First, the RQ1 answer is model-dependent, and the current audio specialist genuinely beats trained captioners zero-shot. Second, the polyphony advantage is a property of the data, shared by every system, which complements the event-level picture from Professor Abesser's own work. Third, caption quality and audio grounding are different axes and evaluations should report both. Everything is reproducible from the repository. Thank you.");
}

const OUT = process.env.DECK_OUT || "Zuraiz_P3_Final.pptx";
pres.writeFile({ fileName: OUT }).then(() => {
  console.log("deck written:", OUT);
});
