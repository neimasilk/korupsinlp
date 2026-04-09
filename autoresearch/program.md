# Autoresearch Program — KorupsiNLP Text Feature Experiments

## Goal

Find text features from judicial reasoning (pertimbangan hakim) that improve
sentence prediction beyond the tuntutan-only baseline (R²=0.600).

The research question: **Can the language judges use to justify their decisions
predict sentencing severity beyond what prosecution demand already explains?**

## Setup

1. Read this file (`program.md`) and `prepare.py` to understand the rules
2. Read `train.py` to understand the current state
3. Run the baseline: `python -m autoresearch.train`
4. Record the result in `results.tsv`

## Rules

### What you CAN do
- Modify `autoresearch/train.py` — preprocessing, features, model, hyperparams
- Try different TF-IDF configurations (max_features, ngram_range, min_df, max_df, sublinear_tf)
- Try different text preprocessing (stopwords, stemming, lowercasing, regex cleaning)
- Try different models: Ridge, Lasso, ElasticNet, SVR, RandomForest, GradientBoosting
- Try dimensionality reduction (TruncatedSVD on TF-IDF)
- Try custom features: text length, sentence count, keyword counts
- Combine text features with structured features in different ways
- Try feature selection methods

### What you CANNOT do
- Modify `prepare.py` (read-only — data loading, splits, evaluation)
- Change the train/val/test split or random seed
- Install new packages (use what's in pyproject.toml)
- Access the test set during experiments (test set is for final Paper 2 evaluation only)
- Modify any files outside `autoresearch/`

## The Metric

**Primary: `val_r2`** — R² on the validation set. Higher is better.
- Baseline to beat: **0.600** (M9 tuntutan-only linear model)
- An experiment is KEPT if `val_r2 > current_best_val_r2`
- An experiment is DISCARDED if `val_r2 <= current_best_val_r2`

**Secondary** (reported but not used for keep/discard):
- `val_mae` — Mean Absolute Error in years (lower is better)
- `val_rmse` — Root Mean Squared Error (lower is better)
- `val_spearman` — Spearman rank correlation (higher is better)

## Time Budget

60 seconds per experiment. Most sklearn experiments finish in 1-5 seconds.
If an experiment exceeds 60s, it should be simplified.

## The Experiment Loop

1. Look at the current `train.py` and `results.tsv`
2. Think of a modification that might improve `val_r2`
3. Modify `train.py` with one clear change
4. Commit: `git commit -am "autoresearch: <description>"`
5. Run: `python -m autoresearch.train > autoresearch/run.log 2>&1`
6. Parse `val_r2` from run.log
7. If crashed → diagnose, fix, try again
8. Record in `results.tsv`: commit_hash, val_r2, status, description
9. If `val_r2 > current_best` → KEEP (advance branch)
10. If `val_r2 <= current_best` → DISCARD (`git reset --hard HEAD~1`)
11. **REPEAT** — never stop until manually interrupted

## Results Format

`results.tsv` columns (tab-separated):
```
commit	val_r2	val_mae	status	description
abc1234	0.612	1.85	keep	tfidf ngram=(1,3) max_features=10000
def5678	0.598	1.92	discard	remove tuntutan, text-only
```

## Domain Context

The pertimbangan hakim (judicial reasoning) is written in formal Indonesian legal
language. Key characteristics:
- Formal register, very different from conversational Indonesian
- Contains references to pasal (articles), dakwaan (charges), tuntutan (prosecution demand)
- Aggravating factors: "memberatkan" — corruption scale, position abuse, no remorse
- Mitigating factors: "meringankan" — cooperation, first offense, family breadwinner
- The word "menyesal" (regretful), "kooperatif" (cooperative), "tulang punggung keluarga"
  (family breadwinner) may correlate with lighter sentences
- Legal terms: "menyalahgunakan wewenang", "memperkaya diri sendiri", "merugikan keuangan negara"

## Simplicity Criterion

All else equal, simpler is better:
- A 0.001 R² gain from adding 50 lines of code → questionable
- A 0.001 R² gain from removing code → definitely keep
- If val_r2 is the same but code is much cleaner → keep the cleaner version

## Experiment Ideas (suggestions, not requirements)

1. Increase max_features to 10000 or 20000
2. Try trigrams: ngram_range=(1,3)
3. Add keyword count features: count of "menyesal", "kooperatif", "jabatan" etc.
4. Try Lasso for automatic feature selection
5. Try GradientBoosting (may capture nonlinear text-sentence relationships)
6. Try TruncatedSVD to reduce TF-IDF dimensions to 100-200
7. Try text_only mode (remove tuntutan) to measure pure text predictive power
8. Try using only the last 2000 chars of pertimbangan (closest to verdict)
9. Indonesian stopword removal (common words: yang, dan, di, dari, untuk, ...)
10. If stuck for 10 experiments, try a radically different approach
