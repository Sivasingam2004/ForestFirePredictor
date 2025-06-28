# 🔥 generate_map.py
import pandas as pd
import folium

def create_map():
    try:
        df = pd.read_csv("fire_logs.csv")

        if df.empty:
            return  # No data to plot

        # Get the latest row
        latest = df.iloc[-1]

        # Simulated GPS coordinates (you can replace with real GPS values)
        lat = 11.0168  # Example: Coimbatore
        lon = 76.9558

        fire_map = folium.Map(location=[lat, lon], zoom_start=10)

        # Decide marker color
        color = 'red' if latest['Prediction'] == 'HIGH' else 'green'

        # Create a marker
        folium.Marker(
            location=[lat, lon],
            popup=f"🔥 Fire Risk: {latest['Prediction']}<br>🌡 Temp: {latest['Temperature']} °C<br>💧 Humidity: {latest['Humidity']}%",
            icon=folium.Icon(color=color)
        ).add_to(fire_map)

        # Save the map as HTML
        fire_map.save("templates/fire_map.html")

    except Exception as e:
        print("🌍 Error generating map:", e)
