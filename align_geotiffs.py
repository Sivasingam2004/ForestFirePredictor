import os
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

# 📌 Reference file for alignment
ref_file = "ForestFirePredictor/data/NDVI_Feb2023_Simlipal.tif"

# 📂 All input raster paths to align
input_files = [
    "ForestFirePredictor/data/fire_binary_simlipal_2021.tif",
    "ForestFirePredictor/data/modis_landcover.tif",
    "ForestFirePredictor/data/slope_srtm.tif",
    "ForestFirePredictor/data/elevation_srtm.tif",
    "ForestFirePredictor/data/wind_speed.tif",
    "ForestFirePredictor/data/relative_humidity.tif",
    "ForestFirePredictor/data/Rainfall_Odisha.tif",
    "ForestFirePredictor/data/NDVI_Feb2023_Simlipal.tif",
    "ForestFirePredictor/data/modis_fire_binary.tif"
]

# 📁 Output directory for aligned files
output_dir = "ForestFirePredictor/data/aligned"
os.makedirs(output_dir, exist_ok=True)

# 🧭 Load reference properties
with rasterio.open(ref_file) as ref:
    dst_crs = ref.crs
    dst_transform = ref.transform
    dst_width = ref.width
    dst_height = ref.height

# 🔁 Reproject and save each input file
for file in input_files:
    with rasterio.open(file) as src:
        output_path = os.path.join(output_dir, os.path.basename(file))
        kwargs = src.meta.copy()
        kwargs.update({
            'crs': dst_crs,
            'transform': dst_transform,
            'width': dst_width,
            'height': dst_height
        })

        with rasterio.open(output_path, 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=dst_transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.nearest
                )

        print(f"✅ Aligned and saved: {output_path}")
