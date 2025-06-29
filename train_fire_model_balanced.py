import rasterio
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.utils import resample
import joblib
import os

# 📦 Load stacked raster
stacked_path = "ForestFirePredictor/data/stacked_data.tif"
with rasterio.open(stacked_path) as src:
    stacked_array = src.read()  # (bands, rows, cols)
    profile = src.profile

# 🧹 Reshape for training
n_bands, height, width = stacked_array.shape
X = stacked_array.reshape(n_bands, -1).T

# 🏷️ Labels: assuming fire_binary_simlipal_2021.tif is band 4
y = stacked_array[3].flatten()

# 🧼 Remove nodata (label 255)
valid_mask = y != 255
X_valid = X[valid_mask]
y_valid = y[valid_mask]

# 🧪 Split original
X_train, X_test, y_train, y_test = train_test_split(X_valid, y_valid, test_size=0.2, random_state=42)

# ⚖️ BALANCE classes
X_fire = X_train[y_train == 1]
y_fire = y_train[y_train == 1]

X_nonfire = X_train[y_train == 0]
y_nonfire = y_train[y_train == 0]

X_fire_upsampled, y_fire_upsampled = resample(X_fire, y_fire,
                                              replace=True,
                                              n_samples=len(y_nonfire),
                                              random_state=42)

X_balanced = np.vstack((X_nonfire, X_fire_upsampled))
y_balanced = np.concatenate((y_nonfire, y_fire_upsampled))

# 🌳 Train new classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_balanced, y_balanced)

# 📊 Evaluate
y_pred = clf.predict(X_test)
print("\n📊 Classification Report (Balanced):")
print(classification_report(y_test, y_pred))

# 💾 Save model
os.makedirs("model", exist_ok=True)
joblib.dump(clf, "model/fire_rf_model_balanced.pkl")
print("\n✅ Balanced model saved as: model/fire_rf_model_balanced.pkl")
