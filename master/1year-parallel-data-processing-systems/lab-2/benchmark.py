import csv
import subprocess
from pathlib import Path


PROCESS_COUNTS = [1, 2, 4, 8, 16, 32]
ARRAY_SIZES = [1_000, 10_000, 100_000, 1_000_000, 10_000_000]
REPEATS = 30

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
EXECUTABLE = PROJECT_DIR / ".build/lab-2/Release/mpi_app_2.exe"
RESULTS_FILE = SCRIPT_DIR / "results/raw.csv"


def main():
    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)

    with RESULTS_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "processes",
            "array_size",
            "repeat",
            "time_seconds",
        ])

        for processes in PROCESS_COUNTS:
            for array_size in ARRAY_SIZES:
                for repeat in range(1, REPEATS + 1):
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

                    elapsed = float(result.stdout.strip())

                    writer.writerow([
                        processes,
                        array_size,
                        repeat,
                        elapsed,
                    ])

                    file.flush()

                    print(
                        f"p={processes}, "
                        f"N={array_size}, "
                        f"repeat={repeat}: "
                        f"{elapsed:.6f} s"
                    )


if __name__ == "__main__":
    main()
