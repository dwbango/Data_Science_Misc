# src/modeling.py

import os
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
import joblib

from data_utils import get_clean_data, get_feature_pipeline

def run_modeling(
    test_size: float = 0.2,
    random_state: int = 42,
    n_jobs: int = -1,
    model_path: str = None
) -> None:
    """
    Train, evaluate, and persist a RandomForest model for high-cost prediction.

    Steps:
    1) Load cleaned data from SQL Server.
    2) Build features X and target y.
    3) Split into train/test sets.
    4) Perform GridSearchCV over RF hyperparameters.
    5) Print classification report & ROC AUC.
    6) Save the best model to disk (inside src/).
    """
    # 1) Load & preprocess
    df = get_clean_data()
    X, y = get_feature_pipeline(df)

    # 2) Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        stratify=y,
        random_state=random_state,
    )

    # 3) Hyperparameter grid search
    param_grid = {
        "n_estimators": [100, 200, 300],
        "max_depth":    [None, 5, 10],
    }
    gs = GridSearchCV(
        RandomForestClassifier(random_state=random_state),
        param_grid,
        cv=5,
        scoring="roc_auc",
        n_jobs=n_jobs,
    )
    gs.fit(X_train, y_train)

    # 4) Evaluation
    best = gs.best_estimator_
    print(f"Best parameters: {gs.best_params_}")

    y_pred  = best.predict(X_test)
    y_proba = best.predict_proba(X_test)[:, 1]

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    auc = roc_auc_score(y_test, y_proba)
    print(f"ROC AUC: {auc:.3f}")

    # 5) Persist model into the same folder as this script
    script_dir = os.path.dirname(__file__)
    dest = model_path or os.path.join(script_dir, "insurance_cost_model.pkl")
    joblib.dump(best, dest)
    print(f"Saved trained model to: {dest}")


if __name__ == "__main__":
    run_modeling()