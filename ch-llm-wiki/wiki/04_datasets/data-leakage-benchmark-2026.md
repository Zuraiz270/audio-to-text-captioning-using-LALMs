---
title: "Benchmarking Data Leakage and Generalization in Audio Classification: An Empirical Analysis"
type: source-note
status: active
created: 2026-04-21
updated: 2026-04-22
source_ids: [IEEE-11450559]
source_files: [raw/01_primary_sources/Benchmarking_Data_Leakage_and_Generalization_in_Audio_Classification_An_Empirical_Analysis.pdf]
source_tier: tier-b
canonical_url: https://ieeexplore.ieee.org/document/11450559/
tags: [source-note, matrix-section-1, data-leakage, augmentation, generalization, rq0]
---

# Benchmarking Data Leakage and Generalization in Audio Classification: An Empirical Analysis

| Field | Value |
|:---|:---|
| **Year** | 2025 (published 2026) |
| **Venue** | IEEE ICIIS |
| **Source ID** | IEEE-11450559 |
| **URL** | https://ieeexplore.ieee.org/document/11450559/ |
| **Matrix Section** | 1 — Surveys & Benchmarks |
| **Downloaded via** | Universität Bamberg institutional access |

## Abstract Summary

Empirical study highlighting a critical methodological flaw in audio machine learning: **feature-level data leakage via improper augmentation**. Shows that applying data augmentation *before* splitting the dataset leads to "augmented twins" appearing in both training and test sets, artificially inflating accuracy by up to 25% on datasets like UrbanSound8K.

(Source: Full PDF, IEEE-11450559)

## Key Findings

- **Augmented Twins:** If a sound clip is augmented (e.g., pitch shifted, noise added) and *then* the dataset is split, variants of the same original acoustic event end up in both the training memory and the test evaluation.
- **Accuracy Inflation:** This leakage causes models to overfit to specific source acoustics rather than generalizing. Accuracy metrics can be artificially inflated by up to 25%.
- **Source-Aware Splitting:** Rigorous pipelines MUST split by source/instance *before* any augmentation is applied to the training split.

## Relevance to RQs

- **RQ0 (Contamination):** ★★★ This paper establishes the mechanism of "feature-level data leakage". It proves that even if raw datasets are separated, processing pipelines can create overlap. When evaluating AF3 against Clotho, we must investigate if AF3's training data (if any was augmented or derived from similar sources) constitutes feature-level leakage.
- **Evaluation Validity:** A core theme of this project is ensuring metrics (like CLAPScore vs SPIDEr) actually measure generalization, not memorization. This paper provides empirical backing for strict data hygiene.

## Links

- [RQ0: Contamination](../02_research_questions/rq0-contamination.md)
- [ALM Datasets Survey](alm-datasets-survey-2025.md)
