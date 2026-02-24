from flask import Flask, send_from_directory, jsonify
import subprocess
import os

app = Flask(__name__)
TILES_DIR = "tiles"

@app.route("/tiles/<filename>")
def serve_tile(filename):
    return send_from_directory(TILES_DIR, filename)

@app.route("/update/<radar>/<product>")
def update_radar(radar, product):
    output_file = f"{radar}_{product}.png"
    try:
        subprocess.run(["python3", "radar_engine.py", radar, product, output_file], check=True)
        return jsonify({"status": "updated", "file": output_file})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
