import tkinter as tk
from tkinter import messagebox
import joblib
import pandas as pd
import random
import csv
from datetime import datetime
import os

# --- 1. Model Load ---
model = joblib.load("plant_rf_model.pkl")
is_auto_on = False

# --- 2. Data Logging Function ---
def log_to_csv(data_dict, prediction):
    file_name = "plant_monitoring_history.csv"
    file_exists = os.path.isfile(file_name)
    
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Agar nayi file hai toh header likho
        if not file_exists:
            writer.writerow(['Timestamp', 'Moisture', 'Temp', 'Humidity', 'Light', 'pH', 'Air_Quality', 'Nutrient', 'Prediction'])
        
        # Current time aur data row
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = [timestamp] + list(data_dict.values()) + [prediction]
        writer.writerow(row)

# --- 3. Main Logic ---
def run_simulation():
    if is_auto_on:
        # Sensor Simulation
        v = {
            'moisture': random.randint(10, 95),
            'temperature': random.randint(15, 45),
            'humidity': random.randint(20, 85),
            'light': random.randint(100, 900),
            'ph': round(random.uniform(5.0, 8.5), 1),
            'air_quality': random.randint(10, 100),
            'nutrient': random.randint(10, 100)
        }
        
        # Model Prediction
        df = pd.DataFrame([list(v.values())], columns=list(v.keys()))
        prediction = model.predict(df)[0]

        # UI Update
        card_m.config(text=f"💧 Moisture\n{v['moisture']}%")
        card_t.config(text=f"🌡️ Temp\n{v['temperature']}°C")
        card_h.config(text=f"☁️ Humidity\n{v['humidity']}%")
        card_l.config(text=f"☀️ Light\n{v['light']}")
        
        status_label.config(text=f"STATUS: {prediction.upper()}")
        
        # --- ALERT LOGIC ---
        if "WATER" in prediction.upper() or "UNHEALTHY" in prediction.upper():
            status_label.config(fg="#e74c3c")
            # Sirf pehli baar ya critical condition par alert (taki bar-bar popup na aaye)
            # messagebox.showwarning("⚠️ EMERGENCY", f"Action Required: {prediction}")
        else:
            status_label.config(fg="#27ae60")

        # --- LOGGING CALL ---
        log_to_csv(v, prediction)
        
        root.after(3000, run_simulation)

def toggle():
    global is_auto_on
    is_auto_on = not is_auto_on
    btn.config(text="STOP SYSTEM" if is_auto_on else "START SYSTEM", 
               bg="#c0392b" if is_auto_on else "#27ae60")
    if is_auto_on: run_simulation()

# --- 4. UI Layout ---
root = tk.Tk()
root.title("AI Plant Monitoring Pro")
root.geometry("500x600")
root.configure(bg="#1a1a2e")

tk.Label(root, text="🌿 SMART MONITOR PRO", font=("Arial", 20, "bold"), bg="#1a1a2e", fg="white").pack(pady=20)

frame = tk.Frame(root, bg="#1a1a2e")
frame.pack(pady=10)

def make_card(parent, txt, r, c):
    l = tk.Label(parent, text=txt, font=("Arial", 11, "bold"), bg="#16213e", fg="#48dbfb", width=16, height=4)
    l.grid(row=r, column=c, padx=10, pady=10)
    return l

card_m = make_card(frame, "💧 Moisture\n--", 0, 0)
card_t = make_card(frame, "🌡️ Temp\n--", 0, 1)
card_h = make_card(frame, "☁️ Humidity\n--", 1, 0)
card_l = make_card(frame, "☀️ Light\n--", 1, 1)

status_label = tk.Label(root, text="SYSTEM IDLE", font=("Arial", 16, "bold"), bg="#1a1a2e", fg="gray")
status_label.pack(pady=20)

btn = tk.Button(root, text="START SYSTEM", font=("Arial", 12, "bold"), bg="#27ae60", fg="white", 
                command=toggle, padx=25, pady=12, bd=0)
btn.pack(pady=10)

tk.Label(root, text="*Data is being logged to plant_monitoring_history.csv", 
         font=("Arial", 8), bg="#1a1a2e", fg="#576574").pack(side="bottom", pady=10)

root.mainloop()