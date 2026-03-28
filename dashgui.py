import tkinter as tk
from tkinter import messagebox
import pandas as pd
import joblib
import random

# model load
model = joblib.load("plant_rf_model.pkl")

# prediction function
def predict():
    try:
        moisture = float(entry_moisture.get())
        temperature = float(entry_temp.get())
        humidity = float(entry_humidity.get())
        light = float(entry_light.get())
        ph = float(entry_ph.get())
        air = float(entry_air.get())
        nutrient = float(entry_nutrient.get())

        data = pd.DataFrame([[moisture, temperature, humidity, light, ph, air, nutrient]],
                            columns=['moisture','temperature','humidity','light','ph','air_quality','nutrient'])

        prediction = model.predict(data)[0]

        if prediction == "water_needed":
            result_label.config(text="💧 Help! I need water", fg="blue")
            messagebox.showwarning("Plant Alert", "💧 Help! I need water")

        elif prediction == "stress":
            result_label.config(text="😟 I am stressed", fg="orange")
            messagebox.showwarning("Plant Alert", "😟 Plant is stressed")

        else:
            result_label.config(text="🌱 Your plant is happy", fg="green")
            messagebox.showinfo("Plant Status", "🌱 Your plant is happy")

    except:
        messagebox.showerror("Error", "Please enter valid values")


# auto sensor function
def auto_fill():
    entry_moisture.delete(0, tk.END)
    entry_moisture.insert(0, random.randint(20, 80))

    entry_temp.delete(0, tk.END)
    entry_temp.insert(0, random.randint(18, 35))

    entry_humidity.delete(0, tk.END)
    entry_humidity.insert(0, random.randint(30, 90))

    entry_light.delete(0, tk.END)
    entry_light.insert(0, random.randint(200, 800))

    entry_ph.delete(0, tk.END)
    entry_ph.insert(0, round(random.uniform(5.5, 7.5), 1))

    entry_air.delete(0, tk.END)
    entry_air.insert(0, random.randint(40, 100))

    entry_nutrient.delete(0, tk.END)
    entry_nutrient.insert(0, random.randint(20, 90))


# GUI
root = tk.Tk()
root.title("Smart Plant AI 🌱")
root.geometry("420x560")
root.configure(bg="#f0fff0")

title = tk.Label(root, text="🌱 Smart Plant Monitor", font=("Arial",16,"bold"), bg="#f0fff0")
title.pack(pady=10)

tk.Label(root, text="Moisture", bg="#f0fff0").pack()
entry_moisture = tk.Entry(root)
entry_moisture.pack()

tk.Label(root, text="Temperature", bg="#f0fff0").pack()
entry_temp = tk.Entry(root)
entry_temp.pack()

tk.Label(root, text="Humidity", bg="#f0fff0").pack()
entry_humidity = tk.Entry(root)
entry_humidity.pack()

tk.Label(root, text="Light", bg="#f0fff0").pack()
entry_light = tk.Entry(root)
entry_light.pack()

tk.Label(root, text="pH", bg="#f0fff0").pack()
entry_ph = tk.Entry(root)
entry_ph.pack()

tk.Label(root, text="Air Quality", bg="#f0fff0").pack()
entry_air = tk.Entry(root)
entry_air.pack()

tk.Label(root, text="Nutrient", bg="#f0fff0").pack()
entry_nutrient = tk.Entry(root)
entry_nutrient.pack()

tk.Button(root, text="Auto Sensor 📡", command=auto_fill, bg="orange").pack(pady=5)

tk.Button(root, text="Check Plant 🌿", command=predict, bg="green", fg="white").pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 14, "bold"), bg="#f0fff0")
result_label.pack(pady=20)

root.mainloop()