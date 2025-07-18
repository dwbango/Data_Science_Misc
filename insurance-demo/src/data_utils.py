# src/data_utils.py

import pandas as pd
from sqlalchemy import create_engine

def get_engine():
    """
    Return a SQLAlchemy engine connected to InsurancePrediction.
    """
    conn = "mssql+pymssql://sa:MyStrongPass123@localhost:1433/InsurancePrediction"
    return create_engine(conn)

def load_data(path: str = "../data/insurance.csv") -> pd.DataFrame:
    """
    Load raw insurance CSV into a DataFrame.
    """
    return pd.read_csv(path)

def get_clean_data() -> pd.DataFrame:
    """
    Read production.insurance_clean from SQL Server.
    """
    engine = get_engine()
    return pd.read_sql("SELECT * FROM production.insurance_clean", engine)

def get_feature_pipeline(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """
    Build X, y for modeling:
      - high_cost = 1 if charges > 20k
      - drop raw charges
      - one-hot encode sex, smoker, region
    """
    df = df.copy()
    df["high_cost"] = (df["charges"] > 20_000).astype(int)
    X = df.drop(["charges", "high_cost"], axis=1)
    X = pd.get_dummies(
        X,
        columns=["sex", "smoker", "region"],
        drop_first=True
    )
    y = df["high_cost"]
    return X, y