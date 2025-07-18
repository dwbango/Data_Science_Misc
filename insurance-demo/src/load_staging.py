# load_staging.py

import os
import pandas as pd
from sqlalchemy import create_engine

# Database connection string
SERVER   = "localhost"
PORT     = "1433"
DATABASE = "InsurancePrediction"
USER     = "sa"
PASSWORD = "MyStrongPass123"
CONN_STR = (
    f"mssql+pymssql://{USER}:{PASSWORD}@{SERVER}:{PORT}/{DATABASE}"
)

def main():
    # Locate the CSV in ../data
    csv_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../data/insurance.csv")
    )

    # Read and load
    df = pd.read_csv(csv_path)
    engine = create_engine(CONN_STR)
    df.to_sql(
        "insurance_raw",
        schema="staging",
        con=engine,
        if_exists="replace",  # replace to keep it idempotent
        index=False
    )
    print(f"Loaded {len(df)} rows into staging.insurance_raw")

if __name__ == "__main__":
    main()
