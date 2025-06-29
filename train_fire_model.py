import rasterio
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Path to stacked raster
raster_path = "ForestFirePredictor/data/stacked_data.tif"

# Load stacked data
with rasterio.open(raster_path) as src:
    data = src.read()  # shape: (bands, rows, cols)
    profile = src.profile

# Reshape for ML: (bands, rows*cols) → (rows*cols, bands)
bands, rows, cols = data.shape
X = data.reshape((bands, -1)).T  # shape: (n_samples, n_features)

# Remove pixels with any NaNs
mask = ~np.any(np.isnan(X), axis=1)
X_clean = X[mask]

# Label: Band 4 is fire_binary (index 3)
y = X_clean[:, 3].astype(int)  # Assuming 1 = fire, 0 = no fire

# Remove label from features
X_features = np.delete(X_clean, 3, axis=1)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X_features, y, test_size=0.2, random_state=42)

# Train model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print("\n📊 Classification Report:\n", classification_report(y_test, y_pred))

# Save model
joblib.dump(clf, "model/fire_rf_model.pkl")

print("✅ Model saved at model/fire_rf_model.pkl")
