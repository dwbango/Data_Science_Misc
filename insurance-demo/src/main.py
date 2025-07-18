# src/main.py

def main():
    """
    Orchestrate the end-to-end pipeline:
      1) Download raw data
      2) Run EDA
      3) Train & save model
      4) Score new data
    """
    print("Step 1: download data")
    # download_data(...)

    print("Step 2: exploratory data analysis")
    # run_eda()

    print("Step 3: modeling")
    # run_modeling(...)

    print("Step 4: scoring")
    # run_scoring(...)

    print("Pipeline complete.")

if __name__ == "__main__":
    main()
