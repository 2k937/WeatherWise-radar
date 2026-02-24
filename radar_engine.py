import sys
import os
import matplotlib.pyplot as plt
import pyart
import boto3
from botocore import UNSIGNED
from botocore.client import Config
import numpy as np

AWS_BUCKET = "noaa-nexrad-level2"

def download_latest_radar(radar):
    """Download latest Level II file from AWS S3"""
    s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
    # List recent files
    response = s3.list_objects_v2(Bucket=AWS_BUCKET, Prefix=radar+'/')
    files = [f['Key'] for f in response.get('Contents', []) if f['Key'].endswith('.gz')]
    if not files:
        raise Exception("No radar files found for "+radar)
    latest_file = sorted(files)[-1]
    local_path = os.path.join("tiles", latest_file.split('/')[-1])
    if not os.path.exists("tiles"):
        os.makedirs("tiles")
    s3.download_file(AWS_BUCKET, latest_file, local_path)
    return local_path

def render_radar(file_path, radar, product, output_file):
    """Render radar reflectivity or velocity to PNG"""
    radar_data = pyart.io.read(file_path)
    plt.figure(figsize=(5,5))
    
    if product.upper() == "REF0":
        display = pyart.graph.RadarDisplay(radar_data)
        display.plot('reflectivity', 0, colorbar_label='dBZ', cmap='pyart_NWSRef')
    elif product.upper() == "VEL0":
        display = pyart.graph.RadarDisplay(radar_data)
        display.plot('velocity', 0, colorbar_label='m/s', cmap='pyart_NWSVel')
    else:
        # fallback to reflectivity
        display = pyart.graph.RadarDisplay(radar_data)
        display.plot('reflectivity', 0, colorbar_label='dBZ', cmap='pyart_NWSRef')

    plt.title(f"{radar} {product}")
    plt.axis("off")
    plt.savefig(os.path.join("tiles", output_file))
    plt.close()
    print(f"Saved {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python radar_engine.py RADAR PRODUCT OUTPUT_FILE")
        sys.exit(1)
    
    radar = sys.argv[1]
    product = sys.argv[2]
    output_file = sys.argv[3]

    local_file = download_latest_radar(radar)
    render_radar(local_file, radar, product, output_file)
