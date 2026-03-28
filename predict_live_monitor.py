import tkinter as tk
from tkinter import messagebox
import pandas as pd
import joblib
import random
import csv
from datetime import datetime

# load model
model = joblib.load("plant_rf_model.pkl")

# CSV file name
csv_file = "plant_monitoring_data.csv"

# create CSV header once
with open(csv_file, mode="a", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["time","moisture","temperature","humidity","light","ph","air_quality","nutrient","prediction"])


def predict_and_save():
    moisture = random.randint(20, 80)
    temperature = random.randint(18, 35)
    humidity = random.randint(30, 90)
    light = random.randint(200, 800)
    ph = round(random.uniform(5.5, 7.5), 1)
    air = random.randint(40, 100)
    nutrient = random.randint(20, 90)

    data = pd.DataFrame([[moisture, temperature, humidity, light, ph, air, nutrient]],
                        columns=['moisture','temperature','humidity','light','ph','air_quality','nutrient'])

    prediction = model.predict(data)[0]

    # update GUI
    if prediction == "water_needed":
        result_label.config(text="💧 Help! I need water", fg="blue")
    elif prediction == "stress":
        result_label.config(text="😟 I am stressed", fg="orange")
    else:
        result_label.config(text="🌱 Your plant is happy", fg="green")

    # save to CSV
    with open(csv_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now(),
            moisture,
            temperature,
            humidity,
            light,
            ph,
            air,
            nutrient,
            prediction
        ])

    # run again after 5 sec
    root.after(5000, predict_and_save)


# GUI
root = tk.Tk()
root.title("Live Plant Monitor 🌱")
root.geometry("400x300")

title = tk.Label(root, text="🌱 Live Monitoring Running", font=("Arial",16,"bold"))
title.pack(pady=20)

result_label = tk.Label(root, text="", font=("Arial",14))
result_label.pack(pady=20)

start_btn = tk.Button(root, text="Start Monitoring 📡", command=predict_and_save)
start_btn.pack(pady=10)

root.mainloop()