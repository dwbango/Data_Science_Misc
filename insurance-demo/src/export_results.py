# src/export_results.py

import pandas as pd
from sqlalchemy import create_engine
import os

# ─── Configuration ──────────────────────────────────────────
DB_CONN      = "mssql+pymssql://sa:MyStrongPass123@localhost:1433/InsurancePrediction"
OUTPUT_PATH  = os.path.join(os.path.dirname(__file__), '..', 'data', 'model_results.csv')

# ─── Export routine ──────────────────────────────────────────
def export_model_results():
    engine = create_engine(DB_CONN)
    df = pd.read_sql("SELECT * FROM production.model_results", engine)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Exported {len(df)} rows to {OUTPUT_PATH}")

if __name__ == "__main__":
    export_model_results()