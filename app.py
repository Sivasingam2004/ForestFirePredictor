from flask import Flask, render_template
import pandas as pd
import generate_graphs

app = Flask(__name__)

@app.route("/")
def index():
    try:
        generate_graphs.main()  # Regenerate graphs
        df = pd.read_csv("fire_logs.csv")
        latest = df.iloc[-1] if not df.empty else None
        return render_template("dashboard.html", latest=latest)
    except Exception as e:
        return f"<h1>Error loading dashboard: {e}</h1>"

@app.route("/map")
def map_view():
    return render_template("map.html")  # Show map view

if __name__ == "__main__":
    app.run(debug=True)
