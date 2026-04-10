# Paper 2 Outline — FINAL (Scopus Version)

## Title
**"Charge Type, Judicial Opacity, and the Limits of Prediction: A Computational Analysis of Indonesian Corruption Sentences"**

## Target
Crime, Law and Social Change (Springer, Q1 Law / Q2 Sociology, IF ~2.3)

## Status
Draft complete (207 lines, ~3300 words). Analysis script verified.
All key statistics stable across seeds, bootstrap CIs exclude zero.

## Key Numbers (from scripts/11_paper2_analysis.py)
- Pasal 2 OLS: b=+0.724yr, 95% CI [0.255, 1.203], p=0.002
- Cohen's d (controlled): 0.50, CI [0.22, 0.79]
- Discount R2: -0.10 (unpredictable)
- TF-IDF: delta=-0.158 (significantly worse)
- Keywords: 10/10 positive, 4/10 significant (marginal)
- Geographic: composition effect (controlled p=0.16)
- Judge ANOVA: F=1.94, p=0.020, range ~3yr
