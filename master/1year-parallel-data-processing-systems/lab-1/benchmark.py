# benchmark.py

import csv
import subprocess
from pathlib import Path


PROCESS_COUNTS = [1, 2, 4, 8, 16, 32]
MESSAGE_COUNTS = [100, 500, 1000]
TASKS = [1, 2]
REPEATS = 30

SCRIPT_DIR = Path(__file__).resolve().parent

EXECUTABLE = SCRIPT_DIR / "../.build/lab-1/Release/mpi_app_1.exe"
RESULTS_FILE = SCRIPT_DIR / "./results/raw.csv"


def main():
    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)

    with RESULTS_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "task",
            "processes",
            "messages",
            "repeat",
            "time_seconds",
        ])

        for processes in PROCESS_COUNTS:
            for messages in MESSAGE_COUNTS:
                for task in TASKS:
                    for repeat in range(1, REPEATS + 1):

                        command = [
                            "mpiexec",
                            "-n",
                            str(processes),
                            str(EXECUTABLE),
                            str(task),
                            "--benchmark",
                            str(messages),
                        ]

                        result = subprocess.run(
                            command,
                            capture_output=True,
                            text=True,
                            check=True,
                        )

                        elapsed = float(result.stdout.strip())

                        writer.writerow([
                            task,
                            processes,
                            messages,
                            repeat,
                            elapsed,
                        ])

                        file.flush()

                        print(
                            f"p={processes}, "
                            f"N={messages}, "
                            f"task={task}, "
                            f"repeat={repeat}: "
                            f"{elapsed:.6f} s"
                        )


if __name__ == "__main__":
    main()
