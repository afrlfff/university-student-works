from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "results"
RESULTS_FILE = OUTPUT_DIR / "raw.csv"


def save_plot(data, mode, metric):
    plt.figure(figsize=(6, 4))

    if mode == "original":
        groups = [("N=3*p per process", data)]
    else:
        groups = [
            (f"N={array_size} per process", group)
            for array_size, group in data.groupby("array_size")
        ]

    for label, group in groups:
        valid = group.sort_values("processes").dropna(subset=[metric])
        if metric == "speedup":
            valid = valid[valid[metric] > 0]
        if valid.empty:
            continue

        plt.plot(
            valid["processes"],
            valid[metric],
            marker="o",
            label=label,
        )

    plt.xlabel("Number of MPI processes")
    if metric == "time_ms":
        plt.ylabel("Mean execution time (ms)")
        title = "Execution time"
        filename = f"time_lab3_{mode}.png"
    else:
        plt.axhline(1, color="gray", linestyle="--", label="T(1)/T(p)=1")
        plt.yscale("log", base=10)
        plt.ylabel("Time ratio T(1)/T(p)")
        title = "Time ratio"
        filename = f"speedup_lab3_{mode}.png"

    if mode == "original":
        plt.title(f"{title}: N=3*p")
    else:
        plt.title(f"{title}: fixed array size per process")
    plt.xticks(sorted(data["processes"].unique()))
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / filename, dpi=200)
    plt.close()


def main():
    df = pd.read_csv(RESULTS_FILE)
    summary = (
        df.groupby(["mode", "array_size", "processes"], as_index=False)["time_seconds"]
        .mean()
    )
    summary["time_ms"] = summary["time_seconds"] * 1000

    original = summary[summary["mode"] == "original"].copy()
    original_baseline = original.loc[original["processes"] == 1, "time_seconds"]
    original["baseline"] = (
        original_baseline.iloc[0] if not original_baseline.empty else float("nan")
    )

    fixed = summary[summary["mode"] == "fixed"].copy()
    fixed_baseline = (
        fixed[fixed["processes"] == 1]
        [["array_size", "time_seconds"]]
        .rename(columns={"time_seconds": "baseline"})
    )
    fixed = fixed.merge(fixed_baseline, on="array_size", how="left")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    summaries = []
    for mode, data in [("original", original), ("fixed", fixed)]:
        data["speedup"] = data["baseline"] / data["time_seconds"].replace(0, float("nan"))
        summaries.append(data)
        if not data.empty:
            save_plot(data, mode, "time_ms")
            save_plot(data, mode, "speedup")

    pd.concat(summaries, ignore_index=True).to_csv(
        OUTPUT_DIR / "summary.csv", index=False
    )


if __name__ == "__main__":
    main()
