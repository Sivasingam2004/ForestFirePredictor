import serial
import pandas as pd
import joblib
import csv
from datetime import datetime

# Load trained model
model = joblib.load("fire_risk_model.pkl")

# Connect to ESP32
ser = serial.Serial('COM4', 115200)

# CSV setup
log_filename = 'fire_logs.csv'

# 🔁 Create the CSV file with header if not exists
with open(log_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'Temperature', 'Humidity', 'Gas', 'Prediction'])

# Main loop
while True:
    line = ser.readline().decode().strip()

    # ✅ Skip garbage
    if not line or not all(c in "0123456789.,-" for c in line):
        continue

    try:
        temp, hum, gas = map(float, line.split(','))

        # Prepare input for model
        sensor_df = pd.DataFrame({
            'Temperature': [temp],
            'Humidity': [hum],
            'Gas': [gas]
        })

        # Predict
        pred = model.predict(sensor_df)[0]
        status = "HIGH" if pred == 1 else "LOW"

        # Get timestamp
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Print to terminal
        if pred == 1:
            print(f"🚨 HIGH FIRE RISK! Temp: {temp} Humidity: {hum} Gas: {gas}")
        else:
            print(f"✅ Safe. Temp: {temp} Humidity: {hum} Gas: {gas}")

        # Append to CSV
        with open(log_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([now, temp, hum, gas, status])

    except Exception as e:
        print("⚠️ Error:", e)
