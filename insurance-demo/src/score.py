# src/score.py

import os
import joblib
import pandas as pd
from sqlalchemy import create_engine

# ─── Configuration ─────────────────────────────────────────────────────────────

# SQL Server connection string
DB_CONN = "mssql+pymssql://sa:MyStrongPass123@localhost:1433/InsurancePrediction"

# Path to the trained model (sis in the same folder as this script)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "insurance_cost_model.pkl")

# Classification threshold for “high_cost”
THRESHOLD = 0.10


# ─── Helper functions ─────────────────────────────────────────────────────────

def load_clean_data():
    """Fetch cleaned claims from SQL Server into a DataFrame."""
    engine = create_engine(DB_CONN)
    df = pd.read_sql("SELECT * FROM production.insurance_clean", engine)
    return df, engine


def preprocess_for_scoring(df: pd.DataFrame) -> pd.DataFrame:
    """
    Mirror the feature engineering used in training:
      - Drop raw 'charges'
      - One-hot encode sex, smoker, region (drop_first=True)
      - Ensure all expected columns are present & in the right order
    """
    X = df.drop(columns=["charges"], errors="ignore")
    X = pd.get_dummies(X, columns=["sex", "smoker", "region"], drop_first=True)

    expected_cols = [
        "age", "bmi", "children",
        "sex_male", "smoker_True",
        "region_northwest", "region_southeast", "region_southwest"
    ]
    for col in expected_cols:
        X.setdefault(col, 0)  # add missing cols with zeros

    return X[expected_cols]


# ─── Main scoring routine ─────────────────────────────────────────────────────

def main():
    # 1) Load model
    model = joblib.load(MODEL_PATH)

    # 2) Read clean data
    df, engine = load_clean_data()

    # 3) Prepare features
    X = preprocess_for_scoring(df)

    # 4) Score
    proba = model.predict_proba(X)[:, 1]
    preds = (proba >= THRESHOLD).astype(int)

    # 5) Write back results
    results = df.copy()
    results["prob_high_cost"] = proba
    results["high_cost_pred"] = preds

    results.to_sql(
        name="model_results",
        schema="production",
        con=engine,
        if_exists="replace",
        index=False
    )

    print(f"Scored {len(results)} rows at threshold={THRESHOLD}")


if __name__ == "__main__":
    main()