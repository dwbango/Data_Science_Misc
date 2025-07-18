# src/main.py

from download_data import download_data
from eda import run_eda
from modeling import run_modeling
from score import main as run_scoring

# URL for the raw CSV
DATA_URL = "https://raw.githubusercontent.com/stedy/Machine-Learning-with-R-datasets/master/insurance.csv"

def main():
    print("== Step 1: Download raw data ==")
    download_data(DATA_URL)

    print("\n== Step 2: Exploratory Data Analysis ==")
    run_eda()

    print("\n== Step 3: Train & Save Model ==")
    run_modeling()

    print("\n== Step 4: Score & Write Results ==")
    run_scoring()

    print("\nPipeline complete!")

if __name__ == "__main__":
    main()