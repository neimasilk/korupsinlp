# Session 11 Analysis Findings (10 April 2026)

## 1. Structured Text Features — Three-Phase Experiment

### Phase 1: TF-IDF (Sessions 10-11, 30 experiments)
- All bag-of-words approaches significantly HURT in cross-validation
- Best: 100 TF-IDF unigrams + tuntutan + kerugian, Ridge α=0.05
- 5×10 CV: R²=0.460, vs baseline -0.072 (p<0.0001)

### Phase 2: Domain-Specific Keyword Features
16 binary/count features from pertimbangan text:
- pasal_2, pasal_3, pasal_12, miliar, mengembalikan, jabatan, etc.
- Alpha sweep: optimal α=50
- 5×10 CV: R²=0.498, vs baseline +0.007 (p=0.69) — neutral

### Phase 3: Exhaustive Feature Selection
- Tested all C(11,k) subsets for k=1..4 with 3×10 CV
- **Best: tuntutan + pasal_2 + gratifikasi (3 features)**
- Forward selection confirms: NO additional feature helps
- **5×10 CV: R²=0.521, vs baseline +0.030 (p=0.055)**

### Key Insight: Text-Derived vs Structured Metadata
- Text-derived pasal_2 (from pertimbangan): +0.030, p=0.055
- Structured pasal_2 (from metadata column): -0.003, p=0.81
- **Why**: text captures the *operative* charge; metadata lists *all* charges

## 2. Outlier Analysis

### Vonis > Tuntutan Cases (n=40, 13.9%)
- Judge gives MORE than prosecution asked
- Mean vonis: 5.3yr vs mean tuntutan: 2.9yr
- Mean kerugian: 118 billion IDR (very large cases)
- Concentrated in Jakarta Pusat (18%)

### Predicting Vonis > Tuntutan
- Logistic regression AUC = 0.784 (5×5 stratified CV)
- Key predictors: low tuntutan, pasal_2, absence of meringankan
- Heavy cases rarely mention memberatkan/meringankan (7.1% vs 22.8%)

### Extreme Cases
- Bandung: 0.2yr tuntutan → 5yr vonis (2000% "discount")
- Jakarta Pusat: 2yr → 8yr (400%)
- Tanjungkarang: 7.5yr → 0.25yr (3% discount — extreme lenience)

### Outlier Court Concentration
| Court | Outlier Rate |
|-------|-------------|
| Tanjungkarang | 40% |
| Semarang | 30% |
| Palembang | 25% |
| Bandung | 14% |

## 3. PN Data Investigation

### Discovery
- PN court slugs verified working on MA directory
- pn-surabaya: 344+ verdicts for 2024 alone
- Parser fixed for PN merged text (selama8 → selama 8)

### Critical Limitation
- PN HTML detail pages only publish MENGADILI section
- NO tuntutan, NO kerugian, NO pertimbangan text
- NO PDF downloads available
- **PN verdicts cannot be used for regression analysis**

## 4. Corpus Scaling Strategy Update
- MA year-filtered scraping is the path forward
- Global korupsi directory has 499 pages (~40K verdicts)
- Current coverage sparse for 2013-2023
- MA site unreliable today — retry needed
