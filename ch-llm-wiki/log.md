# Wiki Log — CH-Proj-M

*Append-only audit trail. Format: `YYYY-MM-DD HH:MM | <ACTION> | <relative path> | <one-line summary>`*

---

2026-04-20 00:25 | CREATE | CLAUDE.md | Schema established (14 sections: purpose, architecture, folder conventions, page schema, citation rules, cross-link rules, ingest/query/lint workflows, contradiction handling, logging, file boundaries, root-doc relationship, glossary policy §13.1, new-session conventions).
2026-04-20 00:25 | CREATE | index.md | Initial navigable map of all seed pages plus first two source cards.
2026-04-20 00:25 | CREATE | log.md | Audit trail initialized.
2026-04-20 00:25 | CREATE | raw/ | Folder skeleton created (00_course, 01_primary_sources, 02_secondary_sources, 03_legacy_synthesis, 04_experiments, assets) with .gitkeep in empty folders.
2026-04-20 00:25 | CREATE | wiki/ | Folder skeleton created (00_overview through 11_glossary) with .gitkeep in 09_comparisons and 10_outputs.
2026-04-20 00:25 | CREATE | raw/00_course/CH-Proj-M-00-Topics.pdf | Copied from repo root into raw/ as immutable course material (preparation for first ingest).
2026-04-20 00:25 | CREATE | raw/00_course/CH-Proj-M-00-Intro.pdf | Copied from repo root into raw/ as immutable course material (preparation for second ingest).
2026-04-20 00:30 | CREATE | wiki/00_overview/README.md | Wiki orientation page.
2026-04-20 00:30 | CREATE | wiki/01_project/scope.md | L1/L2 scope summary with cross-links to PROJECT_GUIDE.md §Scope.
2026-04-20 00:30 | CREATE | wiki/01_project/phase-map.md | Phase 0–4 timeline with hard gates.
2026-04-20 00:30 | CREATE | wiki/02_research_questions/rq-index.md | RQ0–RQ5 index with primary metric per RQ.
2026-04-20 00:30 | CREATE | wiki/03_models/audio-flamingo-3.md | Primary model card (stub — pending source ingest).
2026-04-20 00:30 | CREATE | wiki/03_models/salmonn.md | Secondary model card (stub — pending source ingest).
2026-04-20 00:30 | CREATE | wiki/03_models/qwen2-5-omni.md | Tertiary model card (stub — pending source ingest).
2026-04-20 00:30 | CREATE | wiki/04_datasets/clotho-v2-1.md | Primary dataset card (stub — pending Drossos 2020 ingest).
2026-04-20 00:30 | CREATE | wiki/04_datasets/audiocaps.md | Hallucination stimulus dataset card (stub — pending Kim 2019 ingest).
2026-04-20 00:30 | CREATE | wiki/05_metrics/fense.md | Metric card (stub — pending Zhou 2022 ingest).
2026-04-20 00:30 | CREATE | wiki/05_metrics/spider-fl.md | DCASE 2024 official metric card (stub — pending Labbeti 2024 ingest).
2026-04-20 00:30 | CREATE | wiki/06_failure_modes/polyphony-under-description.md | Failure mode 1.
2026-04-20 00:30 | CREATE | wiki/06_failure_modes/entity-hallucination.md | Failure mode 2.
2026-04-20 00:30 | CREATE | wiki/06_failure_modes/temporal-grounding-loss.md | Failure mode 3.
2026-04-20 00:30 | CREATE | wiki/07_humanities/ekphrasis.md | Humanities frame 1.
2026-04-20 00:30 | CREATE | wiki/07_humanities/soundscape-schafer.md | Humanities frame 2 (keynote / soundmark / signal).
2026-04-20 00:30 | CREATE | wiki/07_humanities/accessibility.md | Humanities frame 3.
2026-04-20 00:30 | CREATE | wiki/07_humanities/digital-archives.md | Humanities frame 4.
2026-04-20 00:30 | CREATE | wiki/08_sources/INDEX.md | Source-card index initialized.
2026-04-20 00:30 | CREATE | wiki/11_glossary/README.md | Glossary stub linking to PROJECT_GUIDE.md §Glossary; per-term page growth permitted per §13.1.
2026-04-20 00:35 | INGEST | raw/00_course/CH-Proj-M-00-Topics.pdf | First ingest: course topic catalog (T1–T10). T6 is this project's chosen topic. End-to-end demonstration of the §7 ingest workflow.
2026-04-20 00:35 | CREATE | wiki/08_sources/ch-proj-m-00-topics.md | Source card for first-ingest target.
2026-04-20 00:35 | EDIT | wiki/08_sources/INDEX.md | Added row for ch-proj-m-00-topics.
2026-04-20 00:35 | EDIT | wiki/01_project/scope.md | Added citation to ch-proj-m-00-topics for the T6 topic statement; bumped last_reviewed.
2026-04-20 00:35 | EDIT | wiki/01_project/phase-map.md | Added citation to ch-proj-m-00-topics for course-issued topic origin; bumped last_reviewed.
2026-04-20 00:38 | INGEST | raw/00_course/CH-Proj-M-00-Intro.pdf | Second ingest: course intro deck (logistics, deliverables, deadlines). Demonstrates the workflow is repeatable, not one-off.
2026-04-20 00:38 | CREATE | wiki/08_sources/ch-proj-m-00-intro.md | Source card for second-ingest target.
2026-04-20 00:38 | EDIT | wiki/08_sources/INDEX.md | Added row for ch-proj-m-00-intro.
2026-04-20 00:38 | EDIT | wiki/01_project/phase-map.md | Added citation to ch-proj-m-00-intro for paper/talk deadlines; bumped last_reviewed.
2026-04-20 00:50 | INGEST | raw/03_legacy_synthesis/paper_summaries.md | Legacy ingest A1/5: project-internal 26-paper structured catalogue copied as raw legacy synthesis (24 KB).
2026-04-20 00:50 | CREATE | wiki/08_sources/paper-summaries-legacy.md | Source card for paper_summaries.md (L4, status: stable). Acts as bridge citation for 14 stub concept pages until primary papers are ingested.
2026-04-20 00:50 | EDIT | wiki/08_sources/INDEX.md | Added row for paper-summaries-legacy with full Cited-by list (14 concept pages).
2026-04-20 00:50 | EDIT | wiki/03_models/audio-flamingo-3.md | Added paper-summaries-legacy citation; [UNSOURCED-PRIMARY: Ghosh 2025b, Ghosh 2025a] markers retained.
2026-04-20 00:50 | EDIT | wiki/03_models/salmonn.md | Added paper-summaries-legacy citation; [UNSOURCED-PRIMARY: Tang 2023] marker retained.
2026-04-20 00:50 | EDIT | wiki/03_models/qwen2-5-omni.md | Added paper-summaries-legacy citation; [UNSOURCED-PRIMARY: Qwen Team 2025] marker retained.
2026-04-20 00:50 | EDIT | wiki/04_datasets/clotho-v2-1.md | Added paper-summaries-legacy citation; [UNSOURCED-PRIMARY: Drossos 2020] marker retained.
2026-04-20 00:50 | EDIT | wiki/04_datasets/audiocaps.md | Added paper-summaries-legacy citation; [UNSOURCED-PRIMARY: Kim 2019, Gemmeke 2017] markers retained.
2026-04-20 00:50 | EDIT | wiki/05_metrics/fense.md | Added paper-summaries-legacy citation; [UNSOURCED-PRIMARY: Zhou 2022] marker retained.
2026-04-20 00:50 | EDIT | wiki/05_metrics/spider-fl.md | Added paper-summaries-legacy citation; [UNSOURCED-PRIMARY: Labbeti 2024] marker retained.
2026-04-20 00:50 | EDIT | wiki/06_failure_modes/polyphony-under-description.md | Added paper-summaries-legacy citation; [UNSOURCED-PRIMARY: Mei 2022, Drossos 2020] markers retained.
2026-04-20 00:50 | EDIT | wiki/06_failure_modes/entity-hallucination.md | Added paper-summaries-legacy citation; [UNSOURCED-PRIMARY: Rohrbach 2018, Gemmeke 2017, Wu 2023, Kuan 2024] markers retained.
2026-04-20 00:50 | EDIT | wiki/06_failure_modes/temporal-grounding-loss.md | Added paper-summaries-legacy citation; [UNSOURCED-PRIMARY: Kumar 2026] marker retained.
2026-04-20 00:50 | EDIT | wiki/07_humanities/ekphrasis.md | Added paper-summaries-legacy citation; [UNSOURCED-PRIMARY: Heffernan 1993, Mitchell 1986] markers retained.
2026-04-20 00:50 | EDIT | wiki/07_humanities/soundscape-schafer.md | Added paper-summaries-legacy citation; [UNSOURCED-PRIMARY: Schafer 1977 ⭐, Truax 1984, Sterne 2012, Augoyard 2006, Born 2013] markers retained.
2026-04-20 00:50 | EDIT | wiki/07_humanities/accessibility.md | Added paper-summaries-legacy citation but flagged: legacy contains no WCAG/BLV cards; explicit raw-file deposit still needed.
2026-04-20 00:50 | EDIT | wiki/07_humanities/digital-archives.md | Added paper-summaries-legacy citation but flagged: legacy contains no archive-side cards; explicit raw-file deposit still needed.
2026-04-20 01:10 | INGEST | raw/03_legacy_synthesis/PROJECT_GUIDE.md | Legacy ingest A2/5: project entry-point doc (scope, phase map, RQ table, glossary; 269 lines) copied as raw legacy synthesis.
2026-04-20 01:10 | CREATE | wiki/08_sources/project-guide-legacy.md | Source card for PROJECT_GUIDE.md (L4, status: stable). Bridge citation for scope, phase-map, rq-index, 11_glossary/README.
2026-04-20 01:10 | EDIT | wiki/08_sources/INDEX.md | Added row for project-guide-legacy with Cited-by list (4 pages).
2026-04-20 01:10 | EDIT | wiki/01_project/scope.md | Added project-guide-legacy citation (frontmatter + Sources body).
2026-04-20 01:10 | EDIT | wiki/01_project/phase-map.md | Added project-guide-legacy citation (frontmatter + Sources body).
2026-04-20 01:10 | EDIT | wiki/02_research_questions/rq-index.md | Added project-guide-legacy citation (frontmatter + Sources body — combined with research-notes-legacy from Step 5 in single edit pass).
2026-04-20 01:10 | EDIT | wiki/11_glossary/README.md | Added project-guide-legacy citation (frontmatter + new Sources body section).
2026-04-20 01:10 | EDIT | index.md | Added project-guide-legacy entry under §08 Sources.
2026-04-20 01:11 | INGEST | raw/03_legacy_synthesis/literature_review.md | Legacy ingest A3/5: EBSE evidence narrative (15 §§; 661 lines) copied as raw legacy synthesis. §1.2 strengthens digital-archives via DARIAH-EU 2023 + BL + BBC + Europeana.
2026-04-20 01:11 | CREATE | wiki/08_sources/literature-review-legacy.md | Source card for literature_review.md (L4, status: stable). Bridge citation for 7 humanities + failure-mode pages.
2026-04-20 01:11 | EDIT | wiki/08_sources/INDEX.md | Added row for literature-review-legacy with Cited-by list (7 pages).
2026-04-20 01:11 | EDIT | wiki/07_humanities/ekphrasis.md | Added literature-review-legacy citation (§13 unified humanities + §5–§6 RCA frame).
2026-04-20 01:11 | EDIT | wiki/07_humanities/soundscape-schafer.md | Added literature-review-legacy citation (§13 Schafer canonical frame; §1.2 Europeana / DARIAH archives).
2026-04-20 01:11 | EDIT | wiki/07_humanities/accessibility.md | Added literature-review-legacy citation; partial-coverage flag retained — no dedicated WCAG card in legacy.
2026-04-20 01:11 | EDIT | wiki/07_humanities/digital-archives.md | Added literature-review-legacy citation; substantial improvement — §1.2 names DARIAH-EU 2023 + BL + BBC + Europeana as deployment-horizon archives.
2026-04-20 01:11 | EDIT | wiki/06_failure_modes/polyphony-under-description.md | Added literature-review-legacy citation (§5.1, §5.2, §6.4 unified RCA).
2026-04-20 01:11 | EDIT | wiki/06_failure_modes/entity-hallucination.md | Added literature-review-legacy citation (§6.6 CHAIR-audio dual criterion).
2026-04-20 01:11 | EDIT | wiki/06_failure_modes/temporal-grounding-loss.md | Added literature-review-legacy citation (§6 third structural failure; TAC mitigation).
2026-04-20 01:11 | EDIT | index.md | Added literature-review-legacy entry under §08 Sources.
2026-04-20 01:12 | INGEST | raw/03_legacy_synthesis/implementation_plan.md | Legacy ingest A4/5: operational playbook (determinism pins / hardware gate / Makefile / risks R1–R10 / gates G0–G7; 842 lines) copied as raw legacy synthesis.
2026-04-20 01:12 | CREATE | wiki/08_sources/implementation-plan-legacy.md | Source card for implementation_plan.md (L4, status: stable). Bridge citation for fense, spider-fl, audio-flamingo-3, salmonn, qwen2-5-omni.
2026-04-20 01:12 | EDIT | wiki/08_sources/INDEX.md | Added row for implementation-plan-legacy with Cited-by list (5 pages).
2026-04-20 01:12 | EDIT | wiki/05_metrics/fense.md | Added implementation-plan-legacy citation (operational secondary-metric role).
2026-04-20 01:12 | EDIT | wiki/05_metrics/spider-fl.md | Added implementation-plan-legacy citation (DCASE 29.6% canary, BCa CI protocol n=1000 seed=42, σ ≈ 12 pp).
2026-04-20 01:12 | EDIT | wiki/03_models/audio-flamingo-3.md | Added implementation-plan-legacy citation (hardware gate SM ≥ 8.0, determinism pins, 4-cut ladder, MMAU 72.28).
2026-04-20 01:12 | EDIT | wiki/03_models/salmonn.md | Added implementation-plan-legacy citation (RQ3 hallucination comparison protocol; historical LALM baseline).
2026-04-20 01:12 | EDIT | wiki/03_models/qwen2-5-omni.md | Added implementation-plan-legacy citation (L2 ablation slot; first-to-cut order).
2026-04-20 01:12 | EDIT | index.md | Added implementation-plan-legacy entry under §08 Sources.
2026-04-20 01:13 | INGEST | raw/03_legacy_synthesis/research_notes.md | Legacy ingest A5/5: strategy doc (architecture-axis SALMONN→AF3→TAC; 7 open questions; Wohlin §6 RQ design matrix; May-4 talk branching A/B/C; 378 lines) copied as raw legacy synthesis.
2026-04-20 01:13 | CREATE | wiki/08_sources/research-notes-legacy.md | Source card for research_notes.md (L4, status: stable). Bridge citation for rq-index.md.
2026-04-20 01:13 | EDIT | wiki/08_sources/INDEX.md | Added row for research-notes-legacy with Cited-by list (1 page).
2026-04-20 01:13 | EDIT | index.md | Added research-notes-legacy entry under §08 Sources.
2026-04-20 06:25 | LINT | wiki/ | All 8 checks per CLAUDE.md §9 run; report delivered inline in conversation. Summary: PASS frontmatter (25/25 non-INDEX), PASS broken-links, PASS raw-file pointers (7/7), PASS citation-rule (no source card primary basis on root doc), PASS stale (0 days, all today). 1 soft-orphan (00_overview/README.md — orientation page reachable via root index.md only). 1 duplicate slug README.md (intentional folder-orientation convention: 00_overview + 11_glossary). 38 [UNSOURCED] markers across 17 files (intentional bridge markers awaiting primary-paper ingest).
2026-04-20 09:00 | INGEST | raw/01_primary_sources/goel-2025-af3-abstract.md | Phase 1 abstract snapshot: AF3 (arXiv 2507.08128). Lead author = Goel (NOT Ghosh — corrected). MMAU 72.42 (NOT 72.28 — corrected).
2026-04-20 09:00 | INGEST | raw/01_primary_sources/tang-2023-salmonn-abstract.md | Phase 1 abstract snapshot: SALMONN (ICLR 2024 / arXiv 2310.13289).
2026-04-20 09:00 | INGEST | raw/01_primary_sources/qwen-2025-omni-abstract.md | Phase 1 abstract snapshot: Qwen2.5-Omni (arXiv 2503.20215).
2026-04-20 09:00 | INGEST | raw/01_primary_sources/drossos-2020-clotho-abstract.md | Phase 1 abstract snapshot: Clotho v1 (ICASSP 2020 / arXiv 1910.09387). Zenodo DOI 4783391 confirmed for v2.1.
2026-04-20 09:00 | INGEST | raw/01_primary_sources/zhou-2022-fense-abstract.md | Phase 1 abstract snapshot: FENSE (ICASSP 2022 / arXiv 2110.04684).
2026-04-20 09:00 | INGEST | raw/01_primary_sources/kumar-2026-tac-abstract.md | Phase 1 abstract snapshot: TAC (arXiv 2602.15766, Feb 17 2026). Disambiguation RESOLVED: real preprint, not hallucinated.
2026-04-20 09:00 | INGEST | raw/01_primary_sources/polybench-2026-abstract.md | Phase 1 abstract snapshot: PolyBench (arXiv 2603.05128). Independent post-AF3 corroboration of RQ2.
2026-04-20 09:05 | CREATE | wiki/08_sources/goel-2025-af3.md | Source card for AF3, supersedes paper-summaries-legacy as primary basis for AF3 claims.
2026-04-20 09:05 | CREATE | wiki/08_sources/tang-2023-salmonn.md | Source card for SALMONN.
2026-04-20 09:05 | CREATE | wiki/08_sources/qwen-2025-omni.md | Source card for Qwen2.5-Omni.
2026-04-20 09:05 | CREATE | wiki/08_sources/drossos-2020-clotho.md | Source card for Clotho.
2026-04-20 09:05 | CREATE | wiki/08_sources/zhou-2022-fense.md | Source card for FENSE.
2026-04-20 09:05 | CREATE | wiki/08_sources/kumar-2026-tac.md | Source card for TAC, retires the [UNSOURCED-PRIMARY: Kumar 2026] bridge.
2026-04-20 09:05 | CREATE | wiki/08_sources/polybench-2026.md | Source card for PolyBench.
2026-04-20 09:10 | EDIT | wiki/03_models/audio-flamingo-3.md | Status stub→draft. Added goel-2025-af3 primary citation. Replaced [UNSOURCED] table cells with sourced facts. Lead author corrected to Goel. MMAU corrected to 72.42 with † preprint qualifier.
2026-04-20 09:10 | EDIT | wiki/03_models/salmonn.md | Status stub→draft. Added tang-2023-salmonn primary citation. Updated training-data placeholder.
2026-04-20 09:10 | EDIT | wiki/03_models/qwen2-5-omni.md | Status stub→draft. Density 33% → ≥80%. Added qwen-2025-omni citation. TMRoPE + Thinker-Talker + block-wise streaming populated.
2026-04-20 09:10 | EDIT | wiki/04_datasets/clotho-v2-1.md | Status stub→draft. Added drossos-2020-clotho primary citation. Sample rate populated (44.1 kHz per §2.2 of paper, to confirm vs v2.1 release notes).
2026-04-20 09:10 | EDIT | wiki/04_datasets/audiocaps.md | Sample-rate cell rewritten as deferred (Kim 2019 PDF re-fetch pending) — honest [UNSOURCED-PRIMARY] retained.
2026-04-20 09:10 | EDIT | wiki/05_metrics/fense.md | Status stub→draft. Added zhou-2022-fense primary citation. Implementation populated (Sentence-BERT all-mpnet-base-v2).
2026-04-20 09:10 | EDIT | wiki/06_failure_modes/polyphony-under-description.md | Status stub→draft. Added polybench-2026 + drossos-2020-clotho citations. Drossos [UNSOURCED-PRIMARY] retired; Mei 2022 retained pending PDF.
2026-04-20 09:10 | EDIT | wiki/06_failure_modes/temporal-grounding-loss.md | Status stub→draft. Added kumar-2026-tac citation; [UNSOURCED-PRIMARY: Kumar 2026] retired.
2026-04-20 09:15 | CREATE | wiki/03_models/af-clap.md | Concept page for AF-CLAP / AF-Whisper unified encoder — naming-hygiene bridge between AF2 and AF3 lineage; cross-linked from AF3 model card.
2026-04-20 09:15 | CREATE | wiki/02_research_questions/rq0-contamination.md | Dedicated RQ0 page: hypothesis form, method, partial-disclosure fallback, threats-to-validity. Cross-linked from rq-index and audio-flamingo-3.
2026-04-20 09:15 | CREATE | wiki/09_comparisons/af3-zero-shot-claim.md | Comparison: author "zero-shot" claim vs. project's RQ0-tested premise. Resolution: keep both; report A with † qualifier under B's protocol.
2026-04-20 09:15 | CREATE | wiki/09_comparisons/clapscore-threshold-0-25.md | Comparison: 0.25 threshold as free parameter; honest parameterisation via {0.20, 0.25, 0.30} sensitivity sweep with INDETERMINATE rule on disagreement.
2026-04-20 09:15 | EDIT | wiki/02_research_questions/rq-index.md | RQ0 row links to dedicated rq0-contamination page. RQ1 framing softened ("claimed-zero-shot, RQ0-tested"). RQ3 row split into H3 (absolute) + H4 (vs SALMONN) sub-hypotheses. RQ5 row reframed as descriptive primary, CLAPScore secondary [LOW–MED applicability].
2026-04-20 09:18 | EDIT | wiki/08_sources/INDEX.md | Added 7 new rows (goel-2025-af3, tang-2023-salmonn, qwen-2025-omni, drossos-2020-clotho, zhou-2022-fense, kumar-2026-tac, polybench-2026).
2026-04-20 09:18 | EDIT | index.md | Added rq0-contamination (§02), af-clap (§03), 7 new source cards (§08), 2 new comparison pages (§09).
2026-04-20 09:25 | LINT | wiki/ + root docs | Verification pass. UNSOURCED 38→21 (drop of 17 across 6 retired primary bridges). Boundary check PASS (edits scoped to 5 root docs + ch-llm-wiki/, no PDF or non-doc edits). Numerical consistency: MMAU 72.42 propagated correctly; one residual 72.28 in research_notes.md §F (Ghosh 2025b card) corrected. DCASE 29.6 consistent across all live docs. Zenodo 4783391 vs 3490684 disambiguation consistent. Legacy synthesis files (raw/03_legacy_synthesis/) remain immutable — historical 72.28 preserved per §12.
