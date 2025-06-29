# app.py
from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/prediction')
def prediction():
    pred_map_path = os.path.join('static', 'maps', 'predicted_fire_map.png')
    return render_template('prediction.html', image_path=pred_map_path)

@app.route('/spread')
def spread():
    time_steps = ['2hr', '4hr', '6hr', '12hr', '24hr']
    images = []
    for t in time_steps:
        path = os.path.join('static', 'maps', f'fire_spread_{t}.png')
        images.append({'label': f'Fire Spread after {t}', 'path': path})
    return render_template('spread.html', images=images)

if __name__ == '__main__':
    app.run(debug=True)
