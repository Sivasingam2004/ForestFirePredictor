import numpy as np
import rasterio
import matplotlib.pyplot as plt
import os

# Load prediction map
input_path = "data/predicted_fire_map.tif"
output_folder = "static/maps"
os.makedirs(output_folder, exist_ok=True)

with rasterio.open(input_path) as src:
    prediction = src.read(1)
    profile = src.profile

# Create a copy for simulation
fire_map = (prediction == 1).astype(np.uint8)

# Define spread function
def spread_fire(fire_map, iterations):
    new_map = fire_map.copy()
    for _ in range(iterations):
        # Check 8 neighbors
        padded = np.pad(new_map, 1)
        neighbors = sum([
            padded[:-2, :-2], padded[:-2, 1:-1], padded[:-2, 2:],
            padded[1:-1, :-2],                  padded[1:-1, 2:],
            padded[2:, :-2],  padded[2:, 1:-1],  padded[2:, 2:]
        ])
        # Spread if at least 1 neighbor is burning
        new_map = np.where((neighbors > 0) & (prediction == 0), 1, new_map)
    return new_map

# Spread durations in "iterations"
spread_durations = {
    "2hr": 1,
    "4hr": 2,
    "6hr": 3,
    "12hr": 5,
    "24hr": 8,
}

# Generate and save simulation images
for label, steps in spread_durations.items():
    spread = spread_fire(fire_map, steps)
    plt.figure(figsize=(6, 6))
    plt.imshow(spread, cmap="Reds")
    plt.title(f"Fire Spread after {label}")
    plt.axis("off")
    out_path = os.path.join(output_folder, f"fire_spread_{label}.png")
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()
    print(f"✅ Saved: {out_path}")
