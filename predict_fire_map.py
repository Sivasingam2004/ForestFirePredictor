import rasterio
import numpy as np
import joblib
import os

# Paths
stacked_path = "ForestFirePredictor/data/stacked_data.tif"
model_path = "model/fire_rf_model.pkl"
output_path = "ForestFirePredictor/data/predicted_fire_map.tif"

# Load stacked raster (only first 8 bands)
with rasterio.open(stacked_path) as src:
    data = src.read()[:8]  # ✅ Only use 8 bands
    profile = src.profile
    height, width = src.height, src.width

# Reshape to 2D: (num_pixels, num_bands)
n_bands, n_rows, n_cols = data.shape
reshaped_data = data.reshape(n_bands, -1).T

# Handle invalid values (like NaNs)
valid_mask = ~np.any(np.isnan(reshaped_data), axis=1)
valid_data = reshaped_data[valid_mask]

# Load model
model = joblib.load(model_path)

# Predict only on valid data
predictions = model.predict(valid_data)

# Create output array and place predictions in valid positions
pred_map = np.full(reshaped_data.shape[0], -1, dtype=np.int8)
pred_map[valid_mask] = predictions
pred_map = pred_map.reshape((n_rows, n_cols))

# Save prediction map
profile.update(dtype=rasterio.int8, count=1)
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with rasterio.open(output_path, 'w', **profile) as dst:
    dst.write(pred_map, 1)

print(f"✅ Fire prediction map saved to: {output_path}")
