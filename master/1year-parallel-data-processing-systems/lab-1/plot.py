from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

SCRIPT_DIR = Path(__file__).resolve().parent
RESULTS_FILE = SCRIPT_DIR / "results/raw.csv"
OUTPUT_DIR = SCRIPT_DIR / "results"


def save_time_plot(data, task):
    """Plot execution time for all N values of one task."""
    data = data[data["task"] == task]

    plt.figure(figsize=(6, 4))

    for messages, group in data.groupby("messages"):
        group = group.sort_values("processes")
        valid = group.dropna(subset=["time_ms"])

        if valid.empty:
            continue

        plt.plot(
            valid["processes"],
            valid["time_ms"],
            marker="o",
            label=f"N={messages}"
        )

    plt.xlabel("Number of MPI processes")
    plt.ylabel("Mean execution time (ms)")
    plt.title(f"Execution time vs processes (Task {task})")
    plt.xticks(sorted(data["processes"].unique()))
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    plt.savefig(OUTPUT_DIR / f"time_task{task}.png", dpi=200)
    plt.close()


def save_speedup_plot(data, task):
    """Plot speedup for all N values of one task."""
    data = data[data["task"] == task]

    plt.figure(figsize=(6, 4))

    for messages, group in data.groupby("messages"):
        group = group.sort_values("processes")
        valid = group.dropna(subset=["speedup"])
        valid = valid[valid["speedup"] > 0]

        if valid.empty:
            continue

        plt.plot(
            valid["processes"],
            valid["speedup"],
            marker="o",
            label=f"N={messages}"
        )

    plt.axhline(1, color="gray", linestyle="--", label="No speedup")
    plt.yscale("log", base=10)

    plt.xlabel("Number of MPI processes")
    plt.ylabel("Speedup")
    plt.title(f"Speedup vs processes (Task {task})")
    plt.xticks(sorted(data["processes"].unique()))
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    plt.savefig(OUTPUT_DIR / f"speedup_task{task}.png", dpi=200)
    plt.close()


def main():
    df = pd.read_csv(RESULTS_FILE)
    summary = (
        df.groupby(["task", "messages", "processes"], as_index=False)["time_seconds"]
        .mean()
    )
    summary["time_ms"] = summary["time_seconds"] * 1000

    baseline = (
        summary[summary["processes"] == 1]
        [["task", "messages", "time_seconds"]]
        .rename(columns={"time_seconds": "baseline"})
    )
    summary = summary.merge(baseline, on=["task", "messages"], how="left")
    summary["speedup"] = summary["baseline"] / summary["time_seconds"].replace(0, float("nan"))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for task in sorted(summary["task"].unique()):
        save_time_plot(summary, task)
        save_speedup_plot(summary, task)


if __name__ == "__main__":
    main()
