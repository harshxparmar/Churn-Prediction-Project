from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load model files
model = pickle.load(open("model/model.pkl", "rb"))
scaler = pickle.load(open("model/scaler.pkl", "rb"))
features = pickle.load(open("model/features.pkl", "rb"))
threshold = pickle.load(open("model/threshold.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():

    input_data = request.form.to_dict()
    input_df = pd.DataFrame([input_data])

    # Convert numeric fields
    for col in input_df.columns:
        try:
            input_df[col] = pd.to_numeric(input_df[col])
        except:
            pass

    # One-hot encoding
    input_df = pd.get_dummies(input_df)

    # Add missing columns
    for col in features:
        if col not in input_df.columns:
            input_df[col] = 0

    input_df = input_df[features]

    # Scale
    input_scaled = scaler.transform(input_df)

    # Predict probability
    probability = model.predict_proba(input_scaled)[0][1]

    # Apply optimized threshold
    prediction = 1 if probability >= threshold else 0

    # Risk level
    if probability < 0.30:
        risk = "Low Risk"
    elif probability < 0.60:
        risk = "Medium Risk"
    else:
        risk = "High Risk"

    # Business suggestion
    if prediction == 1:
        result = "Customer is likely to CHURN"
        suggestion = "Offer retention discounts, loyalty benefits, or personalized offers."
    else:
        result = "Customer is likely to STAY"
        suggestion = "Maintain engagement through premium services and satisfaction monitoring."

    return render_template(
        "result.html",
        prediction=result,
        probability=round(probability * 100, 2),
        risk=risk,
        suggestion=suggestion
    )

@app.route("/predict_json", methods=["POST"])
def predict_json():
    input_data = request.form.to_dict()
    input_df = pd.DataFrame([input_data])

    # Convert numeric fields
    for col in input_df.columns:
        try:
            input_df[col] = pd.to_numeric(input_df[col])
        except:
            pass

    # One-hot encoding
    input_df = pd.get_dummies(input_df)

    # Add missing columns
    for col in features:
        if col not in input_df.columns:
            input_df[col] = 0

    input_df = input_df[features]

    # Scale
    input_scaled = scaler.transform(input_df)

    # Predict probability
    probability = model.predict_proba(input_scaled)[0][1]

    # Apply optimized threshold
    prediction = 1 if probability >= threshold else 0

    # Risk level
    if probability < 0.30:
        risk = "Low Risk"
    elif probability < 0.60:
        risk = "Medium Risk"
    else:
        risk = "High Risk"

    # Business suggestion
    if prediction == 1:
        result = "Customer is likely to CHURN"
        suggestion = "Offer retention discounts, loyalty benefits, or personalized offers."
    else:
        result = "Customer is likely to STAY"
        suggestion = "Maintain engagement through premium services and satisfaction monitoring."

    return jsonify({
        'prediction': result,
        'probability': round(probability * 100, 2),
        'risk': risk,
        'suggestion': suggestion
    })

if __name__ == "__main__":
    app.run(debug=True)
