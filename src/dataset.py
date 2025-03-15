import os
import json
import requests
import zipfile

# Define dataset URL and paths
CUAD_URL = "https://github.com/TheAtticusProject/cuad/raw/main/data.zip"
DATA_DIR = "data"
CUAD_ZIP_PATH = os.path.join(DATA_DIR, "cuad.zip")
EXTRACTED_DIR = os.path.join(DATA_DIR, "cuad")

# Ensure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

def download_dataset():
    """Download the CUAD dataset from GitHub."""
    print("Downloading CUAD dataset...")
    response = requests.get(CUAD_URL, stream=True)

    if response.status_code == 200:
        with open(CUAD_ZIP_PATH, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print("Download complete.")
    else:
        print("Failed to download dataset. Status code:", response.status_code)
        return False
    return True

def extract_dataset():
    """Extract CUAD dataset ZIP file."""
    print("Extracting dataset...")
    with zipfile.ZipFile(CUAD_ZIP_PATH, "r") as zip_ref:
        zip_ref.extractall(EXTRACTED_DIR)
    print("Extraction complete.")

    # Remove the ZIP file after extraction
    os.remove(CUAD_ZIP_PATH)


if __name__ == "__main__":
    if download_dataset():
        extract_dataset()
