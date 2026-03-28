import tkinter as tk
from tkinter import messagebox
import joblib
import pandas as pd
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Model Load ---
model = joblib.load("plant_rf_model.pkl")
is_auto_on = False

# --- Data storage ---
moisture_points = []
temp_points = []
humidity_points = []
light_points = []
ph_points = []
air_points = []
nutrient_points = []

# --- Logic ---
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

        # Prediction
        df = pd.DataFrame([list(v.values())],
        columns=['moisture','temperature','humidity','light','ph','air_quality','nutrient'])

        prediction = model.predict(df)[0]

        # UI update
        status_label.config(text=f"STATUS: {prediction.upper()}")
        status_label.config(fg="#27ae60" if "healthy" in prediction.lower() else "#e74c3c")

        # --- Append data ---
        moisture_points.append(v['moisture'])
        temp_points.append(v['temperature'])
        humidity_points.append(v['humidity'])
        light_points.append(v['light'])
        ph_points.append(v['ph'])
        air_points.append(v['air_quality'])
        nutrient_points.append(v['nutrient'])

        # keep last 20 points
        if len(moisture_points) > 20:
            moisture_points.pop(0)
            temp_points.pop(0)
            humidity_points.pop(0)
            light_points.pop(0)
            ph_points.pop(0)
            air_points.pop(0)
            nutrient_points.pop(0)

        # --- Graph update ---
        ax.clear()
        ax.plot(moisture_points, label="Moisture")
        ax.plot(temp_points, label="Temp")
        ax.plot(humidity_points, label="Humidity")
        ax.plot(light_points, label="Light")
        ax.plot(ph_points, label="pH")
        ax.plot(air_points, label="Air")
        ax.plot(nutrient_points, label="Nutrient")

        ax.set_title("Live Sensor Trends")
        ax.set_ylim(0,100)
        ax.legend(loc="upper left", fontsize=7)

        canvas.draw()

        root.after(2000, run_simulation)


def toggle():
    global is_auto_on
    is_auto_on = not is_auto_on
    btn.config(text="STOP" if is_auto_on else "START",
               bg="#c0392b" if is_auto_on else "#27ae60")
    if is_auto_on:
        run_simulation()


# --- UI ---
root = tk.Tk()
root.title("AI Plant Dashboard 🌱")
root.geometry("650x720")
root.configure(bg="#1a1a2e")

tk.Label(root, text="🌿 LIVE 7 SENSOR GRAPH",
font=("Arial", 20, "bold"),
bg="#1a1a2e", fg="white").pack(pady=10)

# --- Graph ---
fig, ax = plt.subplots(figsize=(6,4), dpi=100)
fig.patch.set_facecolor('#1a1a2e')
ax.set_facecolor('#16213e')

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=10)

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

btn.pack(pady=10)

root.mainloop()