import os
import sys
import boto3
import pyart
import matplotlib.pyplot as plt
from datetime import datetime
from botocore import UNSIGNED
from botocore.client import Config

AWS_BUCKET = "noaa-nexrad-level2"
OUTPUT_DIR = "tiles"

s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

def get_latest_file(radar):
    today = datetime.utcnow()
    prefix = f"{today.year}/{today.month:02d}/{today.day:02d}/{radar}/"
    response = s3.list_objects_v2(Bucket=AWS_BUCKET, Prefix=prefix)
    files = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].endswith(".gz")]
    if not files:
        return None
    return sorted(files)[-1]

def download_file(key):
    local_path = key.split("/")[-1]
    s3.download_file(AWS_BUCKET, key, local_path)
    return local_path

def render_product(file_path, radar, product):
    radar_data = pyart.io.read_nexrad_archive(file_path)

    field_map = {
        "REF0": "reflectivity",
        "VEL0": "velocity",
        "SRV0": "velocity",
        "CC0": "cross_correlation_ratio",
        "ZDR0": "differential_reflectivity"
    }

    field = field_map.get(product, "reflectivity")

    display = pyart.graph.RadarDisplay(radar_data)
    fig = plt.figure(figsize=(8,8))
    display.plot_ppi(field, sweep=0)

    radar_dir = os.path.join(OUTPUT_DIR, radar, product)
    os.makedirs(radar_dir, exist_ok=True)

    output_path = os.path.join(radar_dir, "latest.png")
    plt.savefig(output_path)
    plt.close(fig)

    os.remove(file_path)

if __name__ == "__main__":
    radar = sys.argv[1]
    product = sys.argv[2]
    key = get_latest_file(radar)
    if key:
        file_path = download_file(key)
        render_product(file_path, radar, product)
