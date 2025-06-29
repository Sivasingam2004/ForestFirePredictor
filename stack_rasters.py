import os
import rasterio
import numpy as np

# Input aligned directory
aligned_dir = "ForestFirePredictor/data/aligned"

# Output stacked file
output_file = "ForestFirePredictor/data/stacked_data.tif"

# List all .tif files in the aligned directory
tif_files = [os.path.join(aligned_dir, f) for f in os.listdir(aligned_dir) if f.endswith(".tif")]
tif_files.sort()  # optional: keeps band order consistent

# Read metadata from the first file
with rasterio.open(tif_files[0]) as src0:
    meta = src0.meta
    width = src0.width
    height = src0.height
    crs = src0.crs
    transform = src0.transform

# Update metadata for stacked bands
meta.update(count=len(tif_files))

# Create the stacked GeoTIFF
with rasterio.open(output_file, 'w', **meta) as dst:
    for idx, file in enumerate(tif_files, start=1):
        with rasterio.open(file) as src:
            band = src.read(1)
            dst.write(band, idx)
            print(f"✅ Added {os.path.basename(file)} as Band {idx}")

print(f"\n🎉 Stacked raster saved to: {output_file}")
