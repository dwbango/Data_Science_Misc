# CRISP-DM Plan

## 1. Business Understanding
- **Objective:** Enable MedInsight (or any health insurer) to proactively identify members likely to incur > \$20,000 in annual medical costs, so care managers can target interventions, optimize resource allocation, and reduce avoidable expenses.  
- **Decision support:** Flags high-risk members early, informing both case management and premium pricing.

## 2. Data Understanding
- **Source:** https://raw.githubusercontent.com/stedy/Machine-Learning-with-R-datasets/master/insurance.csv  
- **License:** Public domain / CC0; also mirrored on Kaggle by user *miriichoi0218* under DbCL v1.0  
- **Dataset:** `insurance.csv` (1,338 rows, 7 columns)  
- **Columns & meaning:**  
  - `age` (int): age of primary beneficiary  
  - `sex` (str): contractor gender (`male`/`female`)  
  - `bmi` (float): body mass index (kg/m²)  
  - `children` (int): number of dependents  
  - `smoker` (str): smoking status (`yes`/`no`)  
  - `region` (str): residential area (`northeast`, `southeast`, `southwest`, `northwest`)  
  - `charges` (float): annual medical cost billed  
- **Missing values:** None detected  
- **Outliers:** Examined histograms & boxplots; extreme BMI and charges values deemed realistic for insurance data  
- **Distributions:**  
  - BMI range: 15.96–53.13  
  - Charges: mean \$13,270.42; median \$9,382.03; skewness ≈ 1.52 (right-skewed)  
- **Categorical levels:**  
  - `sex`: 2 levels  
  - `smoker`: 2 levels  
  - `region`: 4 levels  

## 3. Data Preparation
- **Staging:** Loaded raw CSV into `staging.insurance_raw` via Python script  
- **Cleaning:**  
  - Normalized `smoker` to 0/1  
  - Ensured idempotency by truncating & re-loading tables on each run  
  - Populated `production.insurance_clean` via SQL with clean data types  

## 4. Modeling
- **Train/test split:** 80% train / 20% test (stratified on `high_cost`) to ensure evaluation on unseen data  
- **EDA:** Summary stats, histograms, boxplots, correlation matrix  
- **Feature engineering:**  
  - **Target:** `high_cost` = 1 if `charges` > \$20k  
  - **Encoding:** one-hot encode `sex`, `smoker`, `region` (`drop_first=True` to avoid collinearity)  
- **Algorithm choice:** Random Forest  
  - **Why?** Works well with mixed data types, captures nonlinear interactions (e.g. BMI × smoking), robust to outliers, and provides feature importances for explainability  
  - **Baseline comparison:** Logistic regression and decision tree tested—RF outperformed both on ROC-AUC and recall  
- **Hyperparameter tuning:** Grid search over `n_estimators` and `max_depth` (5-fold CV, scoring by ROC-AUC)  
- **Calibration:** Reliability curve & Brier score (~0.042)  
- **Threshold selection:** Chose 0.10 to achieve ≥ 90% recall on test set  

## 5. Evaluation
- **Hold-out results (threshold = 0.50):**  
  - **Accuracy:** 96% (fraction correctly classified)  
  - **Precision (high_cost):** 100% (of flagged high-cost, % truly high-cost)  
  - **Recall (high_cost):** 82% (of true high-cost, % caught)  
  - **ROC-AUC:** 0.92 (overall ranking performance)  
- **After threshold = 0.10:**  
  - **Recall:** ≥ 90% (meets sensitivity target)  
  - **Precision:** ≈ 45%  
- **Top drivers:**  
  1. `smoker` (importance ≈ 0.48)  
  2. `bmi` (≈ 0.24)  
  3. `age` (≈ 0.17)  

## 6. Deployment
- **Automation:** Daily ELT + scoring via `run_pipeline.sh` (cron on Linux/macOS or launchd plist) writes to `production.model_results`  
- **Visualization:** Power BI dashboard on Power BI Service, connected directly to SQL or via exported CSVs  
- **User guide & interface:**  
  - Simple API (e.g. Flask/FastAPI) form where non-technical staff input member attributes and retrieve probability & flag  
  - Exportable PDF/CSV summary reports for stakeholder distribution  
- **Next steps:**  
  - Set up on-premises Power BI Gateway for live SQL connectivity  
  - Monitor model drift & retrain periodically  
  - Integrate feedback loop from case managers to continually refine thresholds and features  