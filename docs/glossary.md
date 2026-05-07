<!--
AttriSense — docs/glossary.md
Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
Version: 1.0.0
Date   : 2026-05-07
License: MIT — see LICENSE in repo root.
Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
-->

# Glossary

> Definitions of every term that shows up in the docs and dashboard.

## A

**AUC (Area Under the Curve)** — a single-number summary of a binary classifier's ranking quality. Ranges 0.5 (random) to 1.0 (perfect). AttriSense reports test AUC ~0.85.

## B

**Brier score** — mean squared error between predicted probabilities and binary outcomes. Lower is better; 0 is perfect. Used to measure calibration.

## C

**Calibration** — the property that predicted probabilities match observed frequencies. A 70% prediction should be wrong 30% of the time.

**Causal uplift** — the difference in expected outcome under treatment vs. control for a single individual. Distinct from average treatment effect (which averages over the population).

**Cox proportional hazards** — a survival-analysis model. Outputs a curve of "P(still here at month X)". Used in AttriSense's `survival_curves` table.

**csh / tcsh** — C-shell and TENEX C-shell. Older Unix shells with different quoting / redirection semantics from bash. AttriSense's dev machine uses csh — see [troubleshooting](troubleshooting.md#csh-quirks).

## D

**Disparate impact (DI) ratio** — selection rate of the disadvantaged group divided by selection rate of the advantaged group. Fails the EEOC four-fifths rule below 0.80.

## E

**EconML** — Microsoft Research library for treatment-effect estimation. Used for the Causal Uplift tab.

**EEOC four-fifths rule** — a US employment law guideline that flags disparate impact when one group's selection rate is < 80% of another's. From the 1978 Uniform Guidelines on Employee Selection Procedures.

**Embeddings** — fixed-length numeric vectors that represent text. Similar text → similar vectors. AttriSense uses OpenAI's `text-embedding-3-small` (1536-dim) when available, hashing trigrams (256-dim) when not.

## F

**FAISS (Facebook AI Similarity Search)** — Meta's library for efficient vector similarity search. Used for the multilingual RAG index.

**Fairness audit** — a check that the model behaves similarly across protected groups. AttriSense runs the EEOC four-fifths rule by default.

## G

**Gold question** — a hand-validated NL→SQL pair used for evaluating the AI Assistant. There are 50 in `gold_questions.py`.

## H

**Hashing embeddings** — a fallback embedding method that uses character trigram hashes. Deterministic, dependency-free, much worse than a real model — but works offline.

**HRIS** — Human Resources Information System. The system of record for employee data (e.g., Workday, SAP SuccessFactors).

## I

**Imbalanced dataset** — a classification problem where one class is much rarer than the other. Voluntary turnover is the rare class in AttriSense (~12% positive). Handled with SMOTE.

## L

**LangChain** — Python framework for composing LLM calls into chains and agents. Used for the NL→SQL chain.

**LL144 (NYC Local Law 144)** — a 2023 NYC law requiring annual independent bias audits for automated employment decision tools used in covered hiring/promotion uses.

## M

**Model card** — a structured disclosure document for an ML model. Pattern from Mitchell et al. 2019. AttriSense's lives at [ethics/model-card.md](ethics/model-card.md).

## N

**NL→SQL** — Natural Language to SQL. The AI Assistant feature: type a question in English, get SQL + a result table.

## P

**Plotly** — interactive charting library. Used everywhere AttriSense renders a non-SHAP chart.

**Probe (reachability)** — a small request to a remote API used to test if it's reachable before committing to it. AttriSense's multilingual RAG probes OpenAI with a 5-second `embed_query("ping")`.

**Propensity score matching** — a causal-inference technique that pairs treated and untreated units with similar covariates. The right approach for real causal estimates, not used in AttriSense's demoware uplift.

## R

**Random Forest** — an ensemble of decision trees trained on bootstrap samples. AttriSense's primary classifier.

**RAG (Retrieval-Augmented Generation)** — a pattern where an LLM is given retrieved documents as context. AttriSense uses RAG over synthetic exit-interview text.

**Risk band** — categorical bucket of the continuous risk score. Low / Medium / High based on `RISK_THRESHOLDS = {"high": 0.75, "medium": 0.40}`.

## S

**SHAP (SHapley Additive exPlanations)** — a method for decomposing a model's prediction into per-feature contributions. AttriSense uses TreeExplainer (exact for tree models).

**SHAP_Explained** — a binary flag in `workforce_predictions` indicating whether per-feature SHAP values are stored for an employee. True for all high-risk + a sample of others.

**SMOTE (Synthetic Minority Over-sampling Technique)** — a method for synthesising minority-class samples to balance imbalanced datasets. Applied to the training fold only.

**SQLite** — embedded SQL database. AttriSense's data store. Single file, no server.

**Streamlit** — Python framework for data apps. AttriSense's UI layer.

**Survival analysis** — modelling time-to-event data. AttriSense uses Cox PH for time-to-attrition curves.

## T

**T-learner** — a meta-learner pattern in causal inference: train one outcome model per treatment arm, then estimate uplift as the difference. AttriSense's Causal Uplift tab uses this.

**TF-IDF (Term Frequency–Inverse Document Frequency)** — a classical text-representation method. AttriSense uses TF-IDF + cosine similarity for the NL→SQL fallback ranker.

**TreeExplainer** — SHAP's exact attribution method for tree ensembles. Faster and more accurate than KernelExplainer.

## U

**Uplift** — see "Causal uplift".

## V

**Voluntary turnover** — an employee leaving on their own initiative (resignation, retirement). The label AttriSense's model predicts.
