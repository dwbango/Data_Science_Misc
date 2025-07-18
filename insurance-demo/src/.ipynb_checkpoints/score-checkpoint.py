import joblib
import pandas as pd
from sqlalchemy import create_engine

# Configuration
DB_CONN    = "mssql+pymssql://sa:MyStrongPass123@localhost:1433/InsurancePrediction"
MODEL_PATH = "insurance_cost_model.pkl"
THRESHOLD  = 0.10

def main():
    # 1) Load model
    model = joblib.load(MODEL_PATH)

    # 2) Load clean data
    engine = create_engine(DB_CONN)
    df = pd.read_sql("SELECT * FROM production.insurance_clean", engine)

    # 3) Preprocess exactly as in notebook
    X = df.drop(columns=['charges'], errors='ignore')
    X = pd.get_dummies(
        X,
        columns=['sex','smoker','region'],
        drop_first=True
    )

    # Ensure all training columns are present
    expected = ['age','bmi','children',
                'sex_male','smoker_True',
                'region_northwest','region_southeast','region_southwest']
    for col in expected:
        if col not in X.columns:
            X[col] = 0

    # And order them
    X = X[expected]

    # 4) Score
    proba = model.predict_proba(X)[:,1]
    preds = (proba >= THRESHOLD).astype(int)

    # 5) Build and write results
    results = df.copy()
    results['prob_high_cost'] = proba
    results['high_cost_pred'] = preds

    results.to_sql(
        "model_results",
        schema="production",
        con=engine,
        if_exists="replace",
        index=False
    )
    print(f"Scored {len(results)} rows at threshold={THRESHOLD}")

if __name__ == "__main__":
    main()