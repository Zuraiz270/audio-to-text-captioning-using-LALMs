# P3 Cheat Card — the numbers, one page

## The table (SPIDEr-FL, full Clotho-eval, 1,045 clips, seed 42)

| System | SPIDEr-FL | poly | mono | Δ | CHAIR-s | CHAIR-i | ents/cap |
|:--|:--|:--|:--|:--|:--|:--|:--|
| AST (floor) | 0.068 | 0.081 | 0.062 | +0.019 | 0.956 | 0.602 | 5.49 |
| Qwen2.5-Omni-7B | 0.188 | 0.250 | 0.157 | +0.094 | 0.550 | 0.437 | 2.08 |
| SALMONN-13B | 0.225 | 0.262 | 0.204 | +0.059 | 0.332 | 0.314 | 1.38 |
| CNN14+BART | 0.259 | 0.298 | 0.238 | +0.060 | 0.350 | 0.318 | 1.37 |
| EnCLAP-base | 0.280 | 0.329 | 0.256 | +0.073 | 0.351 | 0.320 | 1.52 |
| **AF3** | **0.297** | 0.356 | 0.268 | +0.088 | 0.347 | **0.299** | 1.54 |

MACE (poly / mono / Δ): AF3 0.620/0.593/+0.028 · SALMONN 0.559/0.538/+0.021 ·
Qwen 0.560/0.528/+0.032.

## Hypotheses

- **H1 ✓** AF3 > 0.261: mean 0.2968, CI lower **0.2828** > 0.2714 (0.261 + MDE
  1.04pp), p ≈ 0.001, Holm α′ = 0.0167.
- **H2 ✓** all three LALMs: Δ +0.059…+0.094, CI lowers +0.032…+0.071,
  p ≈ 0.001. Baselines shift +0.019…+0.073 → subset difficulty.
- **H3 ✓** AF3 − SALMONN paired per clip: **+0.072** (CI lower +0.058).
- **H4 ✗** null retained: SALMONN − AF3 CHAIR-s = **−0.015**, p = 0.82;
  same sign at τ 0.20/0.25/0.30 → not threshold-sensitive.
- Stats: BCa bootstrap, n = 1000, seed 42, Holm-Bonferroni, per-clip
  SPIDEr-FL mean equals corpus score exactly.

## Anchors and reproduction

- CNN14: ours **0.259** vs official **0.261** (DCASE 2023 site) → harness valid.
- EnCLAP-base: ours **0.280** vs published **0.295** SPIDEr (ICASSP Table 2,
  finetune setting) / **0.291** SPIDEr-FL (EnCLAP++, same aac-metrics) →
  −1.1pp, disclosed. AF3 0.297 > 0.291 anyway.
- AF3's own paper: Clotho CIDEr ≈ 0.50; ours 0.460 with one-line prompt.

## Splits, metrics, mechanics

- Polyphony: PANNs `Cnn14_DecisionLevelMax`, 2 classes co-active ≥ 1 s.
  τ = 0.50 degenerate (106 poly, 609 zero-activation) → pre-committed fallback
  τ = 0.25 → **336 poly / 709 mono**. 219 mono clips have zero activation at 0.25.
  Entity audit: poly refs 4.5 vs mono 3.8 entities; ≥2 in 97% vs 87%.
- CHAIR-audio: 527 AudioSet labels → 604 surface forms; hallucinated iff
  absent from 5-ref union AND SED tags (dual criterion). Coverage ≈ 0.75–0.91.
- MACE: reference impl, MS-CLAP backend; 7 s random crop → ±0.002 noise;
  30-word clamp hits 3/3135 captions.
- SPIDEr-FL = (CIDEr + SPICE)/2 with FENSE fluency penalty (same detector
  family as the FENSE metric in Harish & Abeßer).
- Runtimes 1×A100: Qwen 8.3 min (~22 GB bf16), SALMONN ~19 min (fp16, beam 4),
  AF3 ~17.5 min (~28 GB fp32). All rows 1045/1045, zero failures.
- Fun fact: Qwen produced a 515-word "tapped, tapped…" loop on
  `opening attic.wav`; AF3 invented a "zipper" on `creaky.wav`.

## Zero-shot disclosure (say it before he does)

AF3 lists **19,195 Clotho dev pairs** in its training appendix; SALMONN
pre-trains AND instruction-tunes on Clotho; Qwen undisclosed. Eval split held
out for all. Same dev data the baselines trained on → symmetric. Disclosed in
abstract + discussion.

## Three takeaways

1. Zero-shot vs trained is **model-dependent**; the current audio specialist wins.
2. Poly > mono for everyone → **dataset effect**; complements event-level
   degradation in Harish & Abeßer.
3. **Overlap ≠ grounding**: best captioner not less hallucination-prone per
   caption (but most grounded per mention). Report both axes.
