# src/app.py

import os
import streamlit as st
import pandas as pd
import joblib

# ─── Configuration ─────────────────────────────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), "insurance_cost_model.pkl")
THRESHOLD  = 0.10

# Load the trained model
model = joblib.load(MODEL_PATH)

st.title("🏥 Insurance High-Cost Risk Calculator")

# ─── User Inputs ───────────────────────────────────────────────────────────────
age      = st.number_input("Age",      min_value=0,   max_value=120, value=40)
sex      = st.selectbox("Sex",        ["female", "male"])
bmi      = st.number_input("BMI",      min_value=10.0, max_value=60.0, value=30.0)
children = st.number_input("Children", min_value=0,   max_value=10,   value=0)
smoker   = st.selectbox("Smoker",     ["no", "yes"])
region   = st.selectbox("Region",     ["northeast", "southeast", "southwest", "northwest"])

# ─── Prediction ────────────────────────────────────────────────────────────────
if st.button("Predict"):
    # 1) Build raw DataFrame; note smoker is boolean so dummy will be `smoker_True`
    df = pd.DataFrame([{
        "age": age,
        "sex": sex,
        "bmi": bmi,
        "children": children,
        "smoker": (smoker == "yes"),
        "region": region
    }])

    # 2) One-hot encode sex, smoker, region (drop_first=True to match training)
    X = pd.get_dummies(df, columns=["sex", "smoker", "region"], drop_first=True)

    # 3) Ensure all model features exist, in correct order
    expected = [
        "age", "bmi", "children",
        "sex_male",     # from sex dummy
        "smoker_True",  # from boolean smoker
        "region_northwest", "region_southeast", "region_southwest"
    ]
    for col in expected:
        if col not in X.columns:
            X[col] = 0
    X = X[expected]

    # 4) Predict
    proba = float(model.predict_proba(X)[:,1][0])
    flag  = proba >= THRESHOLD

    # 5) Display (now with two decimal places)
    st.markdown(f"**💰 Probability of high cost:** {proba:.2%}")
    st.markdown(f"**🚩 High-cost flag:** {'Yes' if flag else 'No'}")