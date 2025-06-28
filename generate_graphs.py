import pandas as pd
import matplotlib.pyplot as plt
import folium
from datetime import datetime

# Load data
df = pd.read_csv("fire_logs.csv")

# Convert timestamp to datetime
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# 🔥 Assign numeric values to prediction for plotting
df["Prediction_Value"] = df["Prediction"].apply(lambda x: 1 if x == "HIGH" else 0)

# Plot 1: Temperature
plt.figure(figsize=(10, 4))
plt.plot(df["Timestamp"], df["Temperature"], color='red', label='Temperature (°C)')
plt.title("Temperature Over Time")
plt.xlabel("Time")
plt.ylabel("°C")
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(True)
plt.legend()
plt.savefig("static/graph_temperature.png")
plt.close()

# Plot 2: Humidity
plt.figure(figsize=(10, 4))
plt.plot(df["Timestamp"], df["Humidity"], color='blue', label='Humidity (%)')
plt.title("Humidity Over Time")
plt.xlabel("Time")
plt.ylabel("%")
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(True)
plt.legend()
plt.savefig("static/graph_humidity.png")
plt.close()

# Plot 3: Gas Sensor
plt.figure(figsize=(10, 4))
plt.plot(df["Timestamp"], df["Gas"], color='green', label='Gas Value')
plt.title("Gas Sensor Data Over Time")
plt.xlabel("Time")
plt.ylabel("Sensor Reading")
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(True)
plt.legend()
plt.savefig("static/graph_gas.png")
plt.close()

# Plot 4: Fire Risk (HIGH/LOW)
plt.figure(figsize=(10, 4))
plt.plot(df["Timestamp"], df["Prediction_Value"], marker='o', linestyle='--', color='purple', label='Fire Risk (1=HIGH)')
plt.title("Fire Risk Over Time")
plt.xlabel("Time")
plt.ylabel("Risk (0=LOW, 1=HIGH)")
plt.yticks([0, 1])
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(True)
plt.legend()
plt.savefig("static/graph_risk.png")
plt.close()

# 🌍 Generate map

def generate_map():
    # Example static coordinates (replace with live GPS later)
    latitude = 13.0827
    longitude = 80.2707

    m = folium.Map(location=[latitude, longitude], zoom_start=7)
    folium.Marker(
        [latitude, longitude],
        popup="🔥 High Fire Risk Detected!",
        icon=folium.Icon(color="red")
    ).add_to(m)

    m.save("templates/map.html")

def main():
    generate_map()

if __name__ == "__main__":
    main()
