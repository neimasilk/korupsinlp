# KorpusKorupsi v1.0 — Corpus Statistics

## Overview

| Metric | Value |
|--------|-------|
| Total records | 557 |
| With case metadata | 488 (87.6%) |
| With valid sentence (vonis > 0) | 327 (58.7%) |
| Acquittals (vonis = 0) | 17 (3.1%) |
| Empty scrapes (no data) | 69 (12.4%) |
| Temporal range | 2011-2026 |
| Court regions | 74 unique |

## Sentencing Distribution (n=327)

| Statistic | Value |
|-----------|-------|
| Mean | 4.63 years |
| Median | 4.0 years |
| Std deviation | 3.28 years |
| Minimum | 3 months |
| Maximum | 18 years |
| IQR | 2.0 - 6.0 years |
| Skew | Right-skewed (log-normal shape) |

## Prosecution Demand (n=320)

| Statistic | Value |
|-----------|-------|
| Mean | 6.42 years |
| Median | 5.5 years |
| Mean discount (vonis/tuntutan) | 84.1% |
| Median discount | 70.0% |

## State Financial Loss (n=273, after excluding 3 artifacts)

| Statistic | Value |
|-----------|-------|
| Median | Rp 1.30 billion |
| Minimum | Rp 15 million |
| Maximum | Rp 300 trillion (PT Timah) |
| Distribution | Log-normal, heavy right tail |

### Kerugian Brackets

| Bracket | n | Mean Vonis | Median Vonis |
|---------|---|------------|--------------|
| < Rp100M | 21 | 2.8 yr | 2.0 yr |
| Rp100M - 1B | 92 | 3.5 yr | 3.0 yr |
| Rp1B - 10B | 76 | 4.6 yr | 5.0 yr |
| Rp10B - 100B | 46 | 6.9 yr | 7.0 yr |
| > Rp100B | 19 | 10.4 yr | 10.0 yr |

## Appeal Filer (Pemohon Kasasi)

| Pemohon | n | % |
|---------|---|---|
| JPU (prosecutor) | 195 | 60.6% |
| Terdakwa (defendant) | 127 | 39.4% |
| Unknown/missing | 235 | — |

**Key finding**: No significant difference in sentencing outcomes between groups (p=0.95).

## Geographic Distribution (Top 10)

| Region | n |
|--------|---|
| Jakarta Pusat | 53 |
| Surabaya | 34 |
| Bandung | 27 |
| Makassar | 23 |
| Medan | 21 |
| Kupang | 16 |
| Banda Aceh | 14 |
| Padang | 13 |
| Samarinda | 13 |
| Semarang | 13 |

Jakarta Pusat has higher mean sentences (7.07yr) due to concentration of mega-corruption cases, not jurisdictional harshness.

## Year Distribution

| Year | n |
|------|---|
| 2011-2018 | 35 |
| 2019 | 46 |
| 2020 | 49 |
| 2021 | 75 |
| 2022 | 37 |
| 2023 | 2 |
| 2024 | 55 |
| 2025 | 142 |
| 2026 | 13 |

**Note**: Year distribution reflects MA publication patterns and scraping recency, NOT actual corruption case volume. 2025 is overrepresented (42% of sentenced cases).

## Key Regression Findings

| Model | R² | n | Finding |
|-------|-----|---|---------|
| vonis ~ tuntutan (linear) | 0.600 | 302 | Strongest predictor |
| vonis ~ log(kerugian) | 0.347 | 251 | Second strongest |
| vonis ~ tuntutan + kerugian | 0.615 | 236 | Best combined model |
| discount ratio ~ all vars | 0.013 | 236 | Unpredictable |

## Data Quality

- Golden set validation: 100% vonis accuracy (20/20 diverse cases)
- Missing data is NOT random (MCAR rejected, p=0.002)
- 3 suspected kerugian artifacts excluded (< Rp1M)
- 69 empty scrapes from server errors
