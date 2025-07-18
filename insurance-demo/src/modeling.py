import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
import joblib
from data_utils import get_clean_data, get_feature_pipeline

def run_modeling():
    # Pull cleaned data straight from SQL
    df = get_clean_data()  

    # Feature engineering & split
    X, y = get_feature_pipeline(df)  
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    # Grid search
    param_grid = {'n_estimators':[100,200], 'max_depth':[None,5,10]}
    gs = GridSearchCV(RandomForestClassifier(random_state=42), param_grid,
                      cv=5, scoring="roc_auc", n_jobs=-1)
    gs.fit(X_train, y_train)

    print("Best params:", gs.best_params_)
    model = gs.best_estimator_

    # Evaluate
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:,1]
    print(classification_report(y_test, y_pred))
    print("ROC AUC:", roc_auc_score(y_test, y_proba))

    # Save model
    joblib.dump(model, "../src/insurance_cost_model.pkl")

if __name__ == "__main__":
    run_modeling()
