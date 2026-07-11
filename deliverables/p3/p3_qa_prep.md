# P3 Q&A Preparation — 5 minutes of questions (13 July 2026)

Ranked by likelihood. Answers are written to be SPOKEN: 2 to 4 sentences,
lead with the direct answer, then one piece of evidence. Numbers you must not
fumble are in the cheat card.

---

## A. The two hardest questions (rehearse these out loud)

**Q1. AF3 and SALMONN had Clotho in their training data. How is that
"zero-shot", and doesn't it explain AF3's win?**
Zero-shot describes my protocol: no fine-tuning by me and no in-context
examples, which is the standard usage in LALM benchmarking. It does not mean
Clotho-free training, and the paper discloses exactly that: AF3 lists the
19,195 Clotho development pairs in its own appendix, SALMONN trains on Clotho
in both stages. Two mitigations: the evaluation split is held out for every
system, and the exposure is the same development data the trained baselines
were fitted on, so at the data level the comparison is symmetric. What differs
is the objective, dedicated captioner versus general model, and that is
exactly the thing I measure. It may well contribute to AF3's Clotho-style
register; that is why the paper adds CHAIR and MACE, which do not reward
register mimicry.

**Q2. Your EnCLAP row is 1.1 points under its published score. Maybe your
harness under-scores it and AF3's win over EnCLAP is an artefact?**
I report that gap openly in the paper instead of tuning it away. Three
answers. The harness itself is validated by CNN14, which reproduces its
official score within 0.002 on the same scorer and clips. The shortfall is
plausibly on the checkpoint and decoding side, not the scorer, since EnCLAP++
shows the released checkpoint can reach 0.294 with the same toolkit. And the
conclusion survives either way: AF3's 0.297 exceeds EnCLAP's published
SPIDEr-FL of 0.291, not just my row, and H1 is anchored on CNN14.

## B. Method and fairness

**Q3. Trained baselines vs zero-shot LALMs, is that a fair comparison?**
The dataset split, references, and metric are identical, so the measurement is
fair. The training regime differs on purpose; that is the research question,
not a confound. And the asymmetry is documented, not hidden.

**Q4. LALMs on a cluster, baselines on a laptop. Comparable?**
Yes. Only the compute location moves. Same contract, same inference loop, same
predictions format, same WSL scorer, same 1,045 clips and seed. The A100 is
just a bigger place to run one caption call.

**Q5. SALMONN used beam search, Qwen and AF3 greedy. Inconsistent?**
Each LALM runs at its authors' recommended decoding, because the question is
each model at its best. The trained baselines use beam search too. Every
decode setting is recorded in the run manifest.

**Q6. AF3 in fp32 but Qwen in bf16, why?**
AF3's released weights are natively float32; loading in bf16 produced a real
dtype mismatch in its audio encoder. fp32 is the correct way to run it, it is
higher precision, and it still fits one A100.

**Q7. How do I know your reproduction is right at all?**
CNN14 end to end gives 0.259 versus the published 0.261, with every submetric
within about 0.005. A wrong sample rate, vocabulary, or weight load would blow
that up immediately.

## C. Results interpretation

**Q8. Why does AST score so low? Is it broken?**
No, the low score is the point. AST is a tagger; it lists events but cannot
form a description, and caption metrics punish that. It is the floor that
shows how much captioning adds, and its CHAIR of 0.956 doubles as a validity
check of the hallucination metric.

**Q9. Qwen understands audio but loses badly. Why?**
Its fluency error rate is the lowest in the table, so it is not disfluency.
Its captions are report-style and enumerate events, which mismatches the
Clotho register that overlap metrics reward. On the audio-grounded MACE it
draws level with SALMONN, so reference overlap and grounding genuinely rank
models differently.

**Q10. Everyone scores HIGHER on polyphonic clips. Isn't that backwards?**
It surprised me too, which is why the baselines matter: they shift by the same
amount, so it is subset difficulty, not an LALM property. Event-rich clips
give captions more matchable content; the monophonic bucket concentrates
quiet, ambiguous clips, including 219 with no SED activation at all. The
reference-entity audit supports the split: polyphonic clips' references name
4.5 distinct entities versus 3.8.

**Q11. So do you contradict our DCASE paper?**
No, we complement it. You showed event-level tasks, tagging and counting,
degrade with polyphony. I show caption-level description does not, on real
recordings. Counting everything gets harder; producing a reference-like
description does not. Same hierarchy, different levels.

**Q12. H4 failed. Is CHAIR just too crude to see the difference?**
The null is not threshold-sensitive, it holds at all three taus, and the
decomposition makes it interpretable: AF3 has the lowest per-mention rate in
the table but mentions more entities per caption, 1.54 versus 1.38. So the
per-caption null is a real trade-off between richness and risk, not metric
noise.

## D. Analysis choices

**Q13. PANNs SED as ground truth for polyphony, isn't that circular or biased?**
They are pseudo-labels and I say so. Biases exist, ontology parents can
co-fire. Two defenses: the reference-entity audit confirms the split's
direction independently, and the pre-committed fallback rule chose the
threshold before any subset results were seen. PaSST was dropped because the
definition needs frame-level output; disclosed as a deviation.

**Q14. Your CHAIR vocabulary misses synonyms, coverage is only 0.8.**
True, and it is a closed-vocabulary metric by design, deterministic and
reproducible with no learned components. The miss bias applies uniformly to
all models and largely cancels in the paired H4 comparison.

**Q15. Why is MACE only a secondary metric?**
Its backend randomly crops a 7-second window per call, giving about 0.002
run-to-run noise, and it needed two implementation workarounds. It is
excellent as an audio-grounded cross-check, which is how I use it; it agrees
with AF3 over SALMONN and with the poly-mono direction.

**Q16. The preregistration was never frozen. Is this HARKing?**
The freeze field is literally null in the committed file, so I do not claim
confirmatory status; the paper calls it a declared analysis plan and lists all
seven deviations. The one re-anchoring, 29.6 to 26.1, fixed a factual error
before any LALM result existed.

**Q17. The prereg lists H5, H6, and a negative control I never saw in the paper.**
Those were explicitly descriptive-only probes: temporal ordering,
out-of-distribution clips, a silence control. They were cut for semester scope
before being run, deviation seven in the paper. No inferential hypothesis
depends on them.

**Q18. Why EnCLAP-base and not large?**
Base establishes the trained-captioner floor at a third of the compute; the
published gain of large is small, 0.299 versus 0.295 in the finetune setting.
The pipeline swaps to large by changing one config path.

## E. Meta

**Q19. How much of this did the AI do?**
The AI transparency statement in the paper documents it: Claude was used
throughout for pipeline code, analysis scripts, literature triage, and LaTeX,
under my direction and review, with a session-dated logbook in the repository.
Every number is produced by committed scripts on raw model outputs, and I can
walk through any decision in the logbook, from the sample-rate choice to the
threshold fallback rule.

**Q20. Your paper has 19 references; the guideline said 8 to 10.**
Every one of the 19 is cited in the text and verified against the primary
source. I read 8 to 10 as a floor for a six-page paper, and I preferred citing
the actual sources for every claim over trimming to a count.

**Q21. What would you do next?**
Three things: temporally strong labels on real data so event ordering can be
scored next to captions; joint event-and-caption protocols on the same clips,
extending the three-level idea beyond synthetic mixtures; and grounded metrics
reported alongside overlap scores by default.

**Q22. The paper was 3.5 hours late.**
Falcon3-Audio's weights turned out never to have been publicly released, so
the third LALM was replaced with AF3 late in the project; the reruns and queue
waits on TinyGPU pushed the write-up past the deadline. The replacement
produced the strongest result in the table.
