from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load trained model, scaler and encoder
model = joblib.load("model.joblib")
scaler = joblib.load("scaler.joblib")
encoder = joblib.load("encoder.joblib")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get values from the form
        sepal_length = float(request.form["sepal_length"])
        sepal_width = float(request.form["sepal_width"])
        petal_length = float(request.form["petal_length"])
        petal_width = float(request.form["petal_width"])

        # Create input with the SAME column names used during training
        features = pd.DataFrame([{
            "sepal_length": sepal_length,
            "sepal_width": sepal_width,
            "petal_length": petal_length,
            "petal_width": petal_width
        }])

        # Scale the input
        features_scaled = scaler.transform(features)

        # Make prediction
        prediction = int(model.predict(features_scaled)[0])

        # Convert numeric prediction to species name
        species_names = {
            0: "setosa",
            1: "versicolor",
            2: "virginica"
        }

        species = species_names[prediction]

        print("Prediction:", species)

        return render_template(
            "index.html",
            prediction=species
        )

    except Exception as e:
        print("ERROR:", e)

        return render_template(
            "index.html",
            error=str(e)
        )


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)