#!/usr/bin/env python3
# /// script
# dependencies = ["seaborn", "pandas", "matplotlib", "numpy"]
# ///
"""
Generate a seaborn bar plot of customer satisfaction by product category.
Saves `customer_satisfaction_by_category.png` by default.

Usage:
    python plot_satisfaction.py
    python plot_satisfaction.py --output myplot.png --samples 400
"""

import argparse
from textwrap import fill
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configuration object provided by the user
CONFIG = {
    "title": "Customer Satisfaction by Product Category",
    "description": "compare average customer satisfaction score across different product categories",
    "x_var": "product_category",
    "y_var": "satisfaction_score",
    "context": "product performance insights",
}


def generate_synthetic_data(categories, samples=500, random_state=42):
    rng = np.random.default_rng(random_state)

    # Give each category a different true mean to simulate performance differences
    base_means = {
        "Electronics": 3.8,
        "Home": 4.2,
        "Clothing": 3.6,
        "Beauty": 4.4,
        "Toys": 3.9,
        "Sports": 4.0,
    }

    # If a category isn't in base_means, give it the global mean
    global_mean = np.mean(list(base_means.values()))

    rows = []
    for _ in range(samples):
        cat = rng.choice(categories)
        mean = base_means.get(cat, global_mean)
        # sample around the mean with small variance, clamp to [1,5]
        score = rng.normal(loc=mean, scale=0.5)
        score = float(np.clip(score, 1.0, 5.0))
        rows.append({"product_category": cat, "satisfaction_score": score})

    return pd.DataFrame(rows)


def plot_avg_satisfaction(df, x_var, y_var, title, description, output_path, show=True):
    sns.set_theme(style="whitegrid")

    # Order categories by descending mean satisfaction (helps performance insights)
    order = (
        df.groupby(x_var)[y_var]
        .mean()
        .sort_values(ascending=False)
        .index
        .tolist()
    )

    # Set figure to be square so saved image can be exactly 512x512 pixels
    # figsize is in inches, so 5.12 inches at 100 DPI -> 512 pixels
    plt.figure(figsize=(5.12, 5.12))
    ax = sns.barplot(
        data=df,
        x=x_var,
        y=y_var,
        order=order,
        estimator=np.mean,
        ci=95,
        capsize=0.08,
        palette="rocket",
    )

    # Annotate mean values on bars
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(
            f"{height:.2f}",
            (p.get_x() + p.get_width() / 2.0, height),
            ha="center",
            va="bottom",
            fontsize=9,
            color="#111111",
        )

    ax.set_xlabel(x_var.replace("_", " ").title())
    ax.set_ylabel(f"Average {y_var.replace('_', ' ').title()}")
    wrapped_desc = fill(description, width=80)
    ax.set_title(title, fontsize=14, weight="bold")
    plt.suptitle(wrapped_desc, y=0.92, fontsize=9)
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    # Ensure output is a 512x512 PNG regardless of current DPI/display
    plt.savefig(output_path, dpi=100, format="png")
    if show:
        plt.show()
    plt.close()


def main():
    parser = argparse.ArgumentParser(description=CONFIG["description"])
    parser.add_argument("--output", "-o", default="chart.png", help="Output image path")
    parser.add_argument("--samples", "-n", type=int, default=500, help="Number of synthetic rows to generate")
    parser.add_argument("--no-show", action="store_true", help="Do not display the plot interactively")
    args = parser.parse_args()

    categories = ["Electronics", "Home", "Clothing", "Beauty", "Toys", "Sports"]

    df = generate_synthetic_data(categories, samples=args.samples)

    print("Sample of generated data:")
    print(df.head())
    print()

    plot_avg_satisfaction(
        df,
        x_var=CONFIG["x_var"],
        y_var=CONFIG["y_var"],
        title=CONFIG["title"],
        description=CONFIG["description"],
        output_path=args.output,
        show=(not args.no_show),
    )

    print(f"Saved plot to: {args.output}")


if __name__ == "__main__":
    main()
