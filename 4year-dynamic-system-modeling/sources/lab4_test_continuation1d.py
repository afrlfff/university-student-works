import numpy as np
import time
import matplotlib.pyplot as plt
from utils import to_latex, idx2param

from modules.systems import lorenz
from modules.continuation import continuation1d
from modules.integrate.typing import SOLVER_CD_LORENZ

# ================================================================================
f = lorenz
params = np.array([10, 28, 8/3], dtype=np.float64)
y0 = np.array([1., 1., 1.], dtype=np.float64)

record_time = 200; transient_time = 200
h = 0.01

param_idx = 2
param_range = (0.0, 4.0)
N = 1000

var_idx = 0

solver=SOLVER_CD_LORENZ

# ================================================================================

def plot_continuation_1d(ax, param_values, maxima):
    for i, param_value in enumerate(param_values):
        ax.plot(np.full_like(maxima[i], param_value), maxima[i], ',b')
    ax.set_xlabel(to_latex("\\" + idx2param[param_idx]), fontsize=14)
    ax.set_ylabel("Maxima", fontsize=14)
    ax.set_xlim(param_range[0], param_range[1])
    ax.set_xticks(np.arange(param_range[0], param_range[1] + 1e-5, 0.5))
    ax.grid(True, linestyle='--')

# ================================================================================

def main():
    print("Compiling ...")
    _, _ = continuation1d(f, params, y0, 1, 1, h, param_idx, param_range, N, var_idx, solver=solver)

    print("Program started")

    num_transient   = round(transient_time / h)
    num_record      = round(record_time / h) + 1

    start_time = time.time()
    param_values, maxima = continuation1d(f, params, y0, num_record, num_transient, h, param_idx, param_range, N, var_idx, solver=solver)
    end_time = time.time()

    elapsed = end_time - start_time
    print(f"Execution time: {elapsed:.3f} seconds")

    fig, axes = plt.subplots(figsize=(10, 6))
    plot_continuation_1d(axes, param_values, maxima)
    plt.show()

    return 0

# ================================================================================

if __name__ == "__main__":
    status = main()
    print(f"Program finished with code {status}")