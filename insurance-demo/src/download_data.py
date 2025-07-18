# src/download_data.py

import os
import requests

def download_data(url: str, dst_dir: str = None) -> str:
    """
    Download the insurance.csv from the given URL into dst_dir/data.
    
    Parameters
    ----------
    url : str
        Web address of the CSV to download.
    dst_dir : str, optional
        Directory to save the file in. Defaults to '../data' relative to this script.
    
    Returns
    -------
    str
        Full path to the downloaded file.
    """
    # Determine destination directory
    base_dir = os.path.dirname(__file__)
    data_dir = dst_dir or os.path.join(base_dir, '..', 'data')
    os.makedirs(data_dir, exist_ok=True)

    # Download
    dst_path = os.path.join(data_dir, "insurance.csv")
    print(f"Downloading to {dst_path} …")
    response = requests.get(url)
    response.raise_for_status()

    # Write to disk
    with open(dst_path, "wb") as f:
        f.write(response.content)
    print("Download complete.")
    return dst_path

if __name__ == "__main__":
    DATA_URL = "https://raw.githubusercontent.com/stedy/Machine-Learning-with-R-datasets/master/insurance.csv"
    download_data(DATA_URL)