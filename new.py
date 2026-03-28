import tkinter as tk
import joblib
import pandas as pd
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
from datetime import datetime

# Model load
model = joblib.load("plant_rf_model.pkl")
is_auto_on = False

# CSV file
csv_file = "plant_live_data.csv"

# create header once
with open(csv_file, mode="a", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([
        "time","moisture","temperature","humidity",
        "light","ph","air_quality","nutrient","prediction"
    ])

# data lists
moisture, temp = [], []
humidity, light = [], []
ph, air, nutrient = [], [], []

def run_simulation():
    if is_auto_on:
        v = {
            'moisture': random.randint(10, 95),
            'temperature': random.randint(15, 45),
            'humidity': random.randint(20, 85),
            'light': random.randint(100, 900),
            'ph': round(random.uniform(5.5, 7.5),1),
            'air_quality': random.randint(30, 90),
            'nutrient': random.randint(20, 80)
        }

        df = pd.DataFrame([list(v.values())],
        columns=['moisture','temperature','humidity','light','ph','air_quality','nutrient'])

        prediction = model.predict(df)[0]

        status_label.config(
            text=f"STATUS: {prediction.upper()}",
            fg="#27ae60" if "healthy" in prediction.lower() else "#e74c3c"
        )

        # append
        moisture.append(v['moisture'])
        temp.append(v['temperature'])
        humidity.append(v['humidity'])
        light.append(v['light'])
        ph.append(v['ph'])
        air.append(v['air_quality'])
        nutrient.append(v['nutrient'])

        # keep last 20
        for lst in [moisture,temp,humidity,light,ph,air,nutrient]:
            if len(lst) > 20:
                lst.pop(0)

        # GRAPH 1
        ax1.clear()
        ax1.plot(moisture, label="Moisture")
        ax1.plot(temp, label="Temp")
        ax1.set_title("Moisture & Temperature")
        ax1.legend()

        # GRAPH 2
        ax2.clear()
        ax2.plot(humidity, label="Humidity")
        ax2.plot(light, label="Light")
        ax2.set_title("Humidity & Light")
        ax2.legend()

        # GRAPH 3
        ax3.clear()
        ax3.plot(ph, label="pH")
        ax3.plot(air, label="Air")
        ax3.plot(nutrient, label="Nutrient")
        ax3.set_title("Soil Health")
        ax3.legend()

        canvas.draw()

        # SAVE CSV
        with open(csv_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                datetime.now(),
                v['moisture'],
                v['temperature'],
                v['humidity'],
                v['light'],
                v['ph'],
                v['air_quality'],
                v['nutrient'],
                prediction
            ])

        root.after(2000, run_simulation)


def toggle():
    global is_auto_on
    is_auto_on = not is_auto_on
    btn.config(
        text="STOP" if is_auto_on else "START",
        bg="#c0392b" if is_auto_on else "#27ae60"
    )
    if is_auto_on:
        run_simulation()


# UI
root = tk.Tk()
root.title("Smart Plant AI Dashboard 🌱")
root.geometry("800x750")
root.configure(bg="#1a1a2e")

tk.Label(root,
text="🌿 SMART PLANT DASHBOARD",
font=("Arial",18,"bold"),
bg="#1a1a2e",
fg="white").pack(pady=10)

fig = plt.figure(figsize=(7,6))
fig.patch.set_facecolor('#1a1a2e')

ax1 = fig.add_subplot(311)
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

status_label = tk.Label(root,
text="SYSTEM READY",
font=("Arial",16,"bold"),
bg="#1a1a2e",
fg="gray")
status_label.pack(pady=10)

btn = tk.Button(root,
text="START MONITORING",
font=("Arial",12,"bold"),
bg="#27ae60",
fg="white",
command=toggle,
padx=30,
pady=10)
btn.pack()

root.mainloop()