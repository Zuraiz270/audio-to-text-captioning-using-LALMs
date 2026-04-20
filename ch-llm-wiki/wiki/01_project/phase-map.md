---
title: Phase Map — Phase 0 → Phase 4
type: concept
tags: [phases, timeline, deadlines, gates]
status: stable
last_reviewed: 2026-04-20
sources: [../08_sources/ch-proj-m-00-topics.md, ../08_sources/ch-proj-m-00-intro.md, ../08_sources/project-guide-legacy.md]
---

## Origin

The phase map operationalizes Topic T6 from the course-issued catalog ([`ch-proj-m-00-topics`](../08_sources/ch-proj-m-00-topics.md)) under the timeline and deliverable structure of the CH-Proj-M course intro deck ([`ch-proj-m-00-intro`](../08_sources/ch-proj-m-00-intro.md)).

> *Canonical phase map and red lines:* [`PROJECT_GUIDE.md` §Phase Map](../../../PROJECT_GUIDE.md) and [`implementation_plan.md`](../../../implementation_plan.md) (legacy synthesis context).

## Phases

| Phase | Dates | Key activities | Hard gate |
|:------|:------|:---------------|:----------|
| **Phase 0** — Environment | → Apr 19 | Conda env, determinism pins, `setup_check.py`, `hypotheses_preregistered.yml` | `setup_check.py` exits 0 |
| **Phase 1** — Baseline + Audit | Apr 19 → May 4 | RQ0 contamination audit, data exploration, AF3 hello-world demo | Canary: DCASE baseline reproduces 29.6% ± 1% |
| **Phase 2** — Core Experiments | May 4 → May 18 | AF3 + SALMONN full eval; polyphony subset annotation; RQ1, RQ2, RQ3 | κ ≥ 0.6 on annotation; all BCa CIs computed |
| **Phase 3** — Failure Modes | May 18 → Jul 1 | RQ3 hallucination, RQ4 temporal, RQ5 humanities, negative controls | Layer-tagged; mixed L1/L2 |
| **Phase 4** — Write-up | Jul 1 → Jul 13 | `make all` pipeline, paper draft, talk preparation | Paper submitted Jul 6; talk delivered Jul 13 |

## Hard deliverable deadlines

| Deliverable | Date | Format |
|:------------|:-----|:-------|
| Term paper | **Jul 6** | ~15 pages, LaTeX |
| Talk | **Jul 13** | 15 min + Q&A |
| Repository | **Jul 13** | Git repo with `Makefile`, notebooks, `environment.yml`, `hypotheses_preregistered.yml` |

Deadline source: [`ch-proj-m-00-intro`](../08_sources/ch-proj-m-00-intro.md).

## Red lines (stop-and-fix)

- **DCASE canary fails by > 2 pp** → metric pipeline is broken. Stop and debug.
- **`setup_check.py` fails SM ≥ 8.0 gate** → bf16 results invalid. Switch hardware.
- **`hypotheses_preregistered.yml` modified after Phase 2 data collection begins** → HARKing violation.

## Sources

- [`ch-proj-m-00-topics`](../08_sources/ch-proj-m-00-topics.md) — origin of the topic and its dataset / RQ framing.
- [`ch-proj-m-00-intro`](../08_sources/ch-proj-m-00-intro.md) — deliverables, deadlines, course logistics.
- [project-guide-legacy](../08_sources/project-guide-legacy.md) — canonical phase structure (Phase 0–4), hard-gate definitions, and red-line stop conditions as project-internal synthesis.
