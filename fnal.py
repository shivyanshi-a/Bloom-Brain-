import tkinter as tk
from tkinter import messagebox
import joblib
import pandas as pd
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- 1. Model Load ---
model = joblib.load("plant_rf_model.pkl")
is_auto_on = False
data_points = [] # Graph ke liye values store karega

# --- 2. Logic ---
def run_simulation():
    if is_auto_on:
        v = {
            'moisture': random.randint(10, 95),
            'temperature': random.randint(15, 45),
            'humidity': random.randint(20, 85),
            'light': random.randint(100, 900),
            'ph': 6.5, 'air_quality': 50, 'nutrient': 50
        }
        
        # Prediction
        df = pd.DataFrame([list(v.values())], columns=['moisture', 'temperature', 'humidity', 'light', 'ph', 'air_quality', 'nutrient'])
        prediction = model.predict(df)[0]

        # UI Update
        card_m.config(text=f"💧 Moisture\n{v['moisture']}%")
        card_t.config(text=f"🌡️ Temp\n{v['temperature']}°C")
        status_label.config(text=f"STATUS: {prediction.upper()}")
        status_label.config(fg="#27ae60" if "healthy" in prediction.lower() else "#e74c3c")

        # --- GRAPH UPDATE LOGIC ---
        data_points.append(v['moisture'])
        if len(data_points) > 20: data_points.pop(0) # Sirf last 20 points dikhayenge
        
        ax.clear()
        ax.plot(data_points, marker='o', color='#48dbfb', linewidth=2)
        ax.set_title("Live Moisture Trend", color="white", fontsize=10)
        ax.set_facecolor('#16213e')
        ax.set_ylim(0, 100)
        canvas.draw()
        
        root.after(2000, run_simulation)

def toggle():
    global is_auto_on
    is_auto_on = not is_auto_on
    btn.config(text="STOP" if is_auto_on else "START", bg="#c0392b" if is_auto_on else "#27ae60")
    if is_auto_on: run_simulation()

# --- 3. UI Setup ---
root = tk.Tk()
root.title("AI Dashboard with Live Graph")
root.geometry("600x700")
root.configure(bg="#1a1a2e")

tk.Label(root, text="🌿 LIVE SENSOR GRAPH", font=("Arial", 20, "bold"), bg="#1a1a2e", fg="white").pack(pady=10)

# Cards Frame
frame = tk.Frame(root, bg="#1a1a2e")
frame.pack()

card_m = tk.Label(frame, text="💧 Moisture\n--", font=("Arial", 12, "bold"), bg="#16213e", fg="#48dbfb", width=15, height=4)
card_m.grid(row=0, column=0, padx=10, pady=10)

card_t = tk.Label(frame, text="🌡️ Temp\n--", font=("Arial", 12, "bold"), bg="#16213e", fg="#ff9f43", width=15, height=4)
card_t.grid(row=0, column=1, padx=10, pady=10)

# --- MATPLOTLIB FIGURE ---
fig, ax = plt.subplots(figsize=(5, 3), dpi=100)
fig.patch.set_facecolor('#1a1a2e')
ax.set_facecolor('#16213e')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=10)

status_label = tk.Label(root, text="SYSTEM READY", font=("Arial", 16, "bold"), bg="#1a1a2e", fg="gray")
status_label.pack(pady=10)

btn = tk.Button(root, text="START MONITORING", font=("Arial", 12, "bold"), bg="#27ae60", fg="white", command=toggle, padx=30, pady=10)
btn.pack(pady=10)

root.mainloop()