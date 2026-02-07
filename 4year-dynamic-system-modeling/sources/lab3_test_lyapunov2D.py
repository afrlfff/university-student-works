import numpy as np
import json
import time
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
from utils import to_latex, idx2param

from modules.systems import lorenz
from modules.lyapunov import lyapunov2D, lyapunov2D_parallel
from modules.integrate.typing import SOLVER_CD_LORENZ

# ================================================================================
f = lorenz
params = np.array([10, 28, 8/3], dtype=np.float64)
y0 = np.array([1., 1., 1.], dtype=np.float64)

record_time = 200; transient_time = 200
h = 0.01

param_idxs = (1, 2)
param1_range = (0, 400)
param2_range = (0, 10)
N = 100

pert_var_idx = 2

solver=SOLVER_CD_LORENZ

# ================================================================================

def save_to_file(file_base_name, result):
    metadata = {
        "record_time": record_time,
        "transient_time": transient_time,
        "h": h,
        "param_idxs": param_idxs,
        "param1_range": param1_range,
        "param2_range": param2_range,
        "N": N,
        "var_idx": pert_var_idx,
    }

    meta_bytes = json.dumps(metadata).encode('utf-8')
    meta_array = np.frombuffer(meta_bytes, dtype='S1')

    results_dir = (Path(__file__) / '..' / '..' / 'results' / 'lyapunov2D').resolve()
    results_dir.mkdir(parents=True, exist_ok=True)

    np.savez(results_dir / f'{file_base_name}.npz', data=result, metadata=meta_array)

# ================================================================================

def plot_lyapunov_2d(ax, LLE_values):
    img = ax.imshow(LLE_values, 
              origin='lower', cmap='plasma', aspect='auto',
              extent=(param1_range[0], param1_range[1], param2_range[0], param2_range[1])
              )
    ax.set_xlabel(to_latex("\\" + idx2param[param_idxs[0]]), fontsize=14)
    ax.set_ylabel(to_latex("\\" + idx2param[param_idxs[1]]), fontsize=14)
    ax.set_xlim(param1_range[0], param1_range[1])
    ax.set_ylim(param2_range[0], param2_range[1])

    return img

# ================================================================================

def main():
    print("Compiling ...")
    _, _, _ = lyapunov2D_parallel(f, params, y0, 2, 1, h, param_idxs, param1_range, param2_range, 1, pert_var_idx, solver=solver, L=1, n_jobs=1)

    print("Program started")

    num_transient   = round(transient_time / h)
    num_record      = round(record_time / h) + 1

    start_time = time.time()
    _, _, LLE_values = lyapunov2D_parallel(f, params, y0, num_record, num_transient, h, param_idxs, param1_range, param2_range, N, pert_var_idx, solver=solver)
    end_time = time.time()

    elapsed = end_time - start_time
    print(f"Execution time: {elapsed:.3f} seconds")

    file_base_name = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    save_to_file(file_base_name, LLE_values)

    fig, axes = plt.subplots(figsize=(10, 6))
    img = plot_lyapunov_2d(axes, LLE_values)
    fig.colorbar(img, ax=axes, shrink=0.9)
    plt.show()

    return 0

# ================================================================================

if __name__ == "__main__":
    status = main()
    print(f"Program finished with code {status}")