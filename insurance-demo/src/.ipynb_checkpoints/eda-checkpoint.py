import pandas as pd
import matplotlib.pyplot as plt
from data_utils import (
    load_data,
    summarize_dataframe,
    compute_category_counts,
    compute_numeric_corr,
    plot_histogram,
    plot_boxplot
)

def run_eda():
    df = load_data("../data/insurance.csv")
    print("Summary:", summarize_dataframe(df))
    print("Category counts:", compute_category_counts(df, ["sex","smoker","region"]))
    print("Numeric correlations:\n", compute_numeric_corr(df, ["age","bmi","children","charges"]))
    # plots
    plot_histogram(df["charges"], bins=50, title="Charges distribution", xlabel="Charges", ylabel="Freq")
    plot_histogram(df["children"], bins=df["children"].nunique(), title="Children count", xlabel="Children", ylabel="Freq")
    plot_boxplot(df, "charges", title="Charges boxplot", ylabel="Charges")
    plt.show()

if __name__ == "__main__":
    run_eda()
