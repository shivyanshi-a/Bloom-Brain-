from flask import Flask, render_template, request
import joblib
import pandas as pd
import random

app = Flask(__name__)

model = joblib.load("plant_rf_model.pkl")

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    values = {}

    if request.method == "POST":

        # AUTO SENSOR
        if "auto" in request.form:
            values = {
                "moisture": random.randint(20,80),
                "temperature": random.randint(18,35),
                "humidity": random.randint(30,90),
                "light": random.randint(200,800),
                "ph": round(random.uniform(5.5,7.5),1),
                "air": random.randint(40,100),
                "nutrient": random.randint(20,90)
            }

        # MANUAL INPUT
        else:
            values = {
                "moisture": float(request.form["moisture"]),
                "temperature": float(request.form["temperature"]),
                "humidity": float(request.form["humidity"]),
                "light": float(request.form["light"]),
                "ph": float(request.form["ph"]),
                "air": float(request.form["air"]),
                "nutrient": float(request.form["nutrient"])
            }

        data = pd.DataFrame([[
            values["moisture"],
            values["temperature"],
            values["humidity"],
            values["light"],
            values["ph"],
            values["air"],
            values["nutrient"]
        ]],
        columns=['moisture','temperature','humidity','light','ph','air_quality','nutrient'])

        prediction = model.predict(data)[0]

    return render_template("index.html", prediction=prediction, values=values)


if __name__ == "__main__":
    app.run(debug=True)