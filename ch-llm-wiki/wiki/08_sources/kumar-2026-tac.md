---
type: source-card
status: draft
last_reviewed: 2026-04-20
---

# Kumar et al. 2026 — TAC (Timestamped Audio Captioning)

**Raw file:** [kumar-2026-tac-abstract.md](../../raw/01_primary_sources/kumar-2026-tac-abstract.md)
**External:** arXiv 2602.15766 (https://arxiv.org/abs/2602.15766)
**Venue / Level:** Preprint (Feb 2026) — L3
**License:** CC BY 4.0
**Confidence / Applicability:** MED / HIGH — confirmed real preprint as of 2026-04-20; numerical claims pending PDF re-fetch

## Claim

Large audio-language models exhibit substantial gaps in *temporal grounding* — locating sound events in time — versus dedicated audio-event-detection systems. Timestamped Audio Captioning (TAC) is a benchmark and protocol for measuring this gap using synthetic A-then-B mixtures with ground-truth onset labels.

## Method

- Synthetic A-then-B mixtures (Clotho/AudioSet sources)
- Ground-truth temporal onset labels
- Evaluation on contemporary LALMs vs. dedicated event-detection models

## Key numbers

- Specific quantitative gap **not transcribed** pending PDF re-fetch (avoiding fabrication).
- Project does not depend on a specific number — RQ4 measures the gap independently.

## Threat to validity

- Preprint, single team.
- Synthetic-mixture protocol may not generalise to natural temporally-complex scenes.

## Feeds

- RQ4 (temporal-grounding probe is project's H5 hypothesis)
- implementation_plan.md §6 (RQ4 protocol)
- literature_review.md §6

## One-sentence reservation

RQ4 is designed around the *protocol* (synthetic A-then-B with ground-truth onsets), not the specific paper — RQ4 stands even if TAC is later retracted.

## Cross-links

- [temporal-grounding-loss.md](../06_failure_modes/temporal-grounding-loss.md)
- [paper-summaries-legacy.md](paper-summaries-legacy.md) — earlier bridge, now superseded
