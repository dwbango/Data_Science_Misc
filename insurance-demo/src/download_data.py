import requests
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(DATA_DIR, exist_ok=True)

url = "https://raw.githubusercontent.com/stedy/Machine-Learning-with-R-datasets/master/insurance.csv"
dst = os.path.join(DATA_DIR, "insurance.csv")

print(f"Downloading to {dst} …")
r = requests.get(url)
r.raise_for_status()
with open(dst, "wb") as f:
    f.write(r.content)
print("Download complete.")
