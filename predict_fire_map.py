import numpy as np
import rasterio
from joblib import load

# Paths
stacked_path = "ForestFirePredictor/data/stacked_data.tif"
model_path = "model/fire_rf_model_balanced.pkl"  # ✅ Load balanced model
output_path = "ForestFirePredictor/data/predicted_fire_map.tif"

# Load stacked data
with rasterio.open(stacked_path) as src:
    stacked_array = src.read()  # shape: (bands, height, width)
    meta = src.meta.copy()

# Prepare data
bands, height, width = stacked_array.shape
flat_pixels = stacked_array.reshape(bands, -1).T  # shape: (num_pixels, num_bands)

# Mask invalid pixels (e.g., nan)
valid_mask = ~np.any(np.isnan(flat_pixels), axis=1)
valid_data = flat_pixels[valid_mask]

# Load model
model = load(model_path)

# Predict
predictions = model.predict(valid_data)

# Reconstruct full prediction map
full_prediction = np.zeros(flat_pixels.shape[0], dtype=np.uint8)
full_prediction[:] = 0  # Default = non-fire
full_prediction[valid_mask] = predictions
predicted_map = full_prediction.reshape(height, width)

# Save output
meta.update(count=1, dtype=rasterio.uint8)
with rasterio.open(output_path, 'w', **meta) as dst:
    dst.write(predicted_map, 1)

print(f"\n✅ Fire prediction map saved to: {output_path}")
