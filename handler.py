from flask import Flask, request
import pandas as pd
import pickle
import os
from fraud_detection.dataPrep import FraudDetection

model = pickle.load(open("model/fraud_detection.pkl", "rb"))

app = Flask(__name__)


@app.route("/predict", methods=['POST'])
def predict():
    test_json = request.get_json()

    if test_json:
        if isinstance(test_json, dict):
            df_raw = pd.DataFrame(test_json, index=[0])
        else:
            df_raw = pd.DataFrame(test_json, columns=test_json[0].keys())

    pipeline = FraudDetection()

    df = pipeline.data_preparation(df_raw)

    pred = model.predict(df)

    df['prediction'] = pred

    return df.to_json(orient='records')


if __name__ == "__main__":
    port = os.environ.get("PORT", 5000)
    app.run(host="0.0.0.0", port= port)
