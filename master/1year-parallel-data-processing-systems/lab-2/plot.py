from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "results"
RESULTS_FILE = OUTPUT_DIR / "raw.csv"


def save_time_plot(data):
    """Plot execution time for all array sizes."""
    plt.figure(figsize=(6, 4))

    for array_size, group in data.groupby("array_size"):
        group = group.sort_values("processes")
        valid = group.dropna(subset=["time_ms"])

        if valid.empty:
            continue

        plt.plot(
            valid["processes"],
            valid["time_ms"],
            marker="o",
            label=f"N={array_size}"
        )

    plt.xlabel("Number of MPI processes")
    plt.ylabel("Mean execution time (ms)")
    plt.title("Execution time vs processes (Lab 2)")
    plt.xticks(sorted(data["processes"].unique()))
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    plt.savefig(OUTPUT_DIR / "time_lab2.png", dpi=200)
    plt.close()


def save_speedup_plot(data):
    """Plot speedup for all array sizes."""
    plt.figure(figsize=(6, 4))

    for array_size, group in data.groupby("array_size"):
        group = group.sort_values("processes")
        valid = group.dropna(subset=["speedup"])
        valid = valid[valid["speedup"] > 0]

        if valid.empty:
            continue

        plt.plot(
            valid["processes"],
            valid["speedup"],
            marker="o",
            label=f"N={array_size}"
        )

    plt.axhline(1, color="gray", linestyle="--", label="No speedup")
    plt.yscale("log", base=10)

    plt.xlabel("Number of MPI processes")
    plt.ylabel("Speedup")
    plt.title("Speedup vs processes (Lab 2)")
    plt.xticks(sorted(data["processes"].unique()))
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    plt.savefig(OUTPUT_DIR / "speedup_lab2.png", dpi=200)
    plt.close()


def main():
    df = pd.read_csv(RESULTS_FILE)
    summary = (
        df.groupby(["array_size", "processes"], as_index=False)["time_seconds"]
        .mean()
    )
    summary["time_ms"] = summary["time_seconds"] * 1000

    baseline = (
        summary[summary["processes"] == 1]
        [["array_size", "time_seconds"]]
        .rename(columns={"time_seconds": "baseline"})
    )
    summary = summary.merge(baseline, on="array_size", how="left")
    summary["speedup"] = summary["baseline"] / summary["time_seconds"].replace(0, float("nan"))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    save_time_plot(summary)
    save_speedup_plot(summary)


if __name__ == "__main__":
    main()
