# src/eda.py

import os
import pandas as pd
import matplotlib.pyplot as plt

def load_data() -> pd.DataFrame:
    """
    Load raw insurance CSV into a DataFrame.
    Always looks in the repo's data/ folder.
    """
    # path relative to this script
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, os.pardir, "data", "insurance.csv")
    return pd.read_csv(csv_path)

def summarize_dataframe(df: pd.DataFrame) -> dict:
    """
    Return shape, missing‐value counts, and descriptive stats.
    """
    return {
        "shape": df.shape,
        "missing_counts": df.isna().sum().to_dict(),
        "summary_stats": df.describe().to_dict()
    }

def compute_category_counts(df: pd.DataFrame, cols: list[str]) -> dict:
    """
    Return value_counts for each categorical column in cols.
    """
    return {col: df[col].value_counts().to_dict() for col in cols}

def compute_numeric_corr(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """
    Return Pearson correlation matrix for cols.
    """
    return df[cols].corr()

def plot_histogram(
    series: pd.Series,
    bins: int | None = None,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None
) -> None:
    """
    Plot a histogram of the given series.
    """
    fig, ax = plt.subplots()
    ax.hist(series, bins=bins)
    if title:  ax.set_title(title)
    if xlabel: ax.set_xlabel(xlabel)
    if ylabel: ax.set_ylabel(ylabel)
    ax.grid(True)

def plot_boxplot(
    df: pd.DataFrame,
    column: str,
    title: str | None = None,
    ylabel: str | None = None
) -> None:
    """
    Plot a boxplot of df[column].
    """
    fig, ax = plt.subplots()
    df.boxplot(column=column, ax=ax)
    if title:  ax.set_title(title)
    if ylabel: ax.set_ylabel(ylabel)
    ax.grid(True)

def run_eda() -> None:
    """
    Execute the full EDA:
      1) compute and print key stats
      2) render histograms and boxplot
    """
    df = load_data()
    print("SUMMARY:", summarize_dataframe(df))
    print("\nCATEGORY COUNTS:", compute_category_counts(df, ["sex","smoker","region"]))
    print("\nNUMERIC CORRELATIONS:\n", compute_numeric_corr(df, ["age","bmi","children","charges"]))

    # Visualizations
    plot_histogram(
        df["charges"],
        bins=50,
        title="Charges Distribution",
        xlabel="Charges ($)",
        ylabel="Frequency"
    )
    plot_histogram(
        df["children"],
        bins=df["children"].nunique(),
        title="Children Count",
        xlabel="Number of Children",
        ylabel="Frequency"
    )
    plot_boxplot(
        df,
        "charges",
        title="Boxplot of Charges",
        ylabel="Charges ($)"
    )
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_eda()