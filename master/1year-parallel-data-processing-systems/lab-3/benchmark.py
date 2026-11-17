import csv
import subprocess
from pathlib import Path


PROCESS_COUNTS = [1, 2, 4, 8, 16, 32]
ARRAY_SIZES = [1_024, 10_240, 102_400, 1_024_000, 10_240_000]
REPEATS = 30
WARMUP_RUNS = 3

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
EXECUTABLE = PROJECT_DIR / ".build/lab-3/Release/mpi_app_3.exe"
RESULTS_FILE = SCRIPT_DIR / "results/raw.csv"


def main():
    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)

    with RESULTS_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "mode",
            "processes",
            "array_size",
            "repeat",
            "time_seconds",
        ])

        for mode in ["original", "fixed"]:
            for processes in PROCESS_COUNTS:
                array_sizes = [3 * processes] if mode == "original" else ARRAY_SIZES
                for array_size in array_sizes:
                    for iteration in range(1, WARMUP_RUNS + REPEATS + 1):
                        command = [
                            "mpiexec",
                            "-n",
                            str(processes),
                            str(EXECUTABLE),
                            str(array_size),
                            "--benchmark",
                        ]

                        result = subprocess.run(
                            command,
                            capture_output=True,
                            text=True,
                            check=True,
                        )
                        if iteration <= WARMUP_RUNS:
                            print(
                                f"mode={mode}, p={processes}, N={array_size}, "
                                f"warmup={iteration}/{WARMUP_RUNS}"
                            )
                            continue

                        repeat = iteration - WARMUP_RUNS
                        elapsed = float(result.stdout.strip())

                        writer.writerow([
                            mode,
                            processes,
                            array_size,
                            repeat,
                            elapsed,
                        ])
                        file.flush()

                        print(
                            f"mode={mode}, "
                            f"p={processes}, "
                            f"N={array_size}, "
                            f"repeat={repeat}: "
                            f"{elapsed:.6f} s"
                        )


if __name__ == "__main__":
    main()
