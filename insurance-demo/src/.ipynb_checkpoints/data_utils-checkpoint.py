# src/data_utils.py

import os
import pandas as pd
from pandas import DataFrame, Series
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from typing import Tuple

def get_engine() -> Engine:
    """
    Return a SQLAlchemy engine connected to the InsurancePrediction database.
    """
    conn_str = "mssql+pymssql://sa:MyStrongPass123@localhost:1433/InsurancePrediction"
    return create_engine(conn_str)

def load_data(path: str | None = None) -> DataFrame:
    """
    Load the raw insurance CSV into a pandas DataFrame.

    Parameters
    ----------
    path : str, optional
        Filesystem path to `insurance.csv`. If None, will load
        '../data/insurance.csv' relative to this script.

    Returns
    -------
    DataFrame
        Loaded insurance data.
    """
    if path is None:
        base_dir = os.path.dirname(__file__)
        path = os.path.join(base_dir, "..", "data", "insurance.csv")
    return pd.read_csv(path)

def get_clean_data() -> DataFrame:
    """
    Read the cleaned insurance table from production schema in SQL Server.

    Returns
    -------
    DataFrame
        All rows from `production.insurance_clean`.
    """
    engine = get_engine()
    return pd.read_sql("SELECT * FROM production.insurance_clean", engine)

def get_feature_pipeline(df: DataFrame) -> Tuple[DataFrame, Series]:
    """
    Build model-ready features and target from raw DataFrame.

    Steps:
      1. Create binary target `high_cost` (1 if charges > 20,000).
      2. Drop the original `charges` and `high_cost` columns from X.
      3. One-hot encode categorical cols: sex, smoker, region.

    Parameters
    ----------
    df : DataFrame
        Raw DataFrame including `charges`.

    Returns
    -------
    X : DataFrame
        Feature matrix for modeling.
    y : Series
        Binary target vector.
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