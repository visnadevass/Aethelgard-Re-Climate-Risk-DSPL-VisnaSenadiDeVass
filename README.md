# Aethelgard Re Climate Risk Analysis using Ridge Regression

## Overview

This project was completed as part of the **5DATA004C – Data Science Project Lifecycle** module at the **University of Westminster**.

The objective is to investigate the relationship between greenhouse gas contributions and global temperature anomalies using historical climate data. A predictive machine learning model was developed to forecast future temperature anomalies and provide business recommendations for the fictitious global reinsurance company **Aethelgard Re**.

---

## Project Objectives

- Integrate multiple historical climate datasets.
- Perform data cleaning and preprocessing.
- Conduct Exploratory Data Analysis (EDA).
- Analyse correlations between greenhouse gas variables and global temperature anomalies.
- Detect and address multicollinearity using Variance Inflation Factor (VIF).
- Develop a Ridge Regression model.
- Evaluate model performance using MAE, RMSE and R².
- Forecast global temperature anomalies for the period 2022–2031.
- Provide actuarial recommendations to support insurance premium pricing and climate risk management.

---

## Dataset

The analysis uses six historical climate datasets:

- contribution-temp-rise-degrees.csv
- contribution-to-temp-rise-by-gas.csv
- ghg-emissions-by-world-region.xlsx
- global-warming-fossil.xlsx
- global-warming-land.xlsx
- temperature-anomaly.csv

These datasets were merged using the **Year** variable to create a single analytical dataset covering **1851–2021**.

---

## Methodology

The project followed the standard Data Science Project Lifecycle:

1. Data Collection
2. Data Cleaning and Preprocessing
3. Exploratory Data Analysis (EDA)
4. Correlation Analysis
5. Multicollinearity Analysis (VIF)
6. Feature Scaling
7. Ridge Regression Model Development
8. Model Evaluation
9. Ten-Year Forecasting
10. Business Recommendations

---

## Technologies Used

- Python
- Jupyter Notebook
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Statsmodels

---

## Model Performance

| Metric | Result |
|---------|---------|
| MAE | 0.0829°C |
| RMSE | 0.0960°C |
| R² Score | 0.7977 |

The Ridge Regression model explained approximately **79.8%** of the variation in global temperature anomalies.

---

## Key Findings

- Greenhouse gas variables show very strong positive correlations with global temperature anomaly.
- Severe multicollinearity was identified among predictor variables.
- Ridge Regression successfully handled multicollinearity while maintaining good predictive performance.
- The model forecasts a continued increase in global temperature anomalies between **2022 and 2031**.
- The findings support the use of dynamic climate-based underwriting models for future insurance risk assessment.

---

## Repository Contents

```
.
├── Climate_Risk_Analysis.ipynb
├── Cleaned_Dataset.csv
├── requirements.txt
├── README.md
├── LICENSE
```

---

## Running the Project

Open the Jupyter Notebook and run all cells sequentially.

The notebook includes:

- Data preprocessing
- Exploratory Data Analysis
- Correlation analysis
- VIF analysis
- Ridge Regression model
- Model evaluation
- Forecasting
- Visualisations

---

## References

- Intergovernmental Panel on Climate Change (IPCC)
- NASA Climate Change
- United Nations Climate Change
- Our World in Data

---

## Author

**Visna Senadi De Vass**

University of Westminster

Module: **5DATA004C – Data Science Project Lifecycle**

Academic Year: **2025/26**

---

## License

This project is licensed under the **MIT License**.
## Author

KJP Visna Senadi De Vass
