import numpy as np
import json
import time
from datetime import datetime
from pathlib import Path

from modules.systems import lorenz
from modules.integrate.typing import SOLVER_CD_LORENZ
from modules.bifurcation import bifurcation1D

# ================================================================================
f = lorenz
params = np.array([10, 28, 8/3], dtype=np.float64)
y0 = np.array([1., 1., 1.], dtype=np.float64)

record_time = 200; transient_time = 200
h = 0.01

param_idx = 0
param_range = (5.0, 20.0)
N = 1000

var_idx = 0

solver=SOLVER_CD_LORENZ
# ================================================================================

def save_to_file(file_base_name, result):
    metadata = {
        "record_time": record_time,
        "transient_time": transient_time,
        "h": h,
        "param_idx": param_idx,
        "param_range": param_range,
        "N": N,
        "var_idx": var_idx,
    }

    meta_bytes = json.dumps(metadata).encode('utf-8')
    meta_array = np.frombuffer(meta_bytes, dtype='S1')

    results_dir = (Path(__file__) / '..' / '..' / 'results' / 'bifurcation1D').resolve()
    results_dir.mkdir(parents=True, exist_ok=True)

    np.savez(results_dir / f'{file_base_name}.npz', data=result, metadata=meta_array)

# ================================================================================

def main():
    print("Compiling ...")
    _ = bifurcation1D(f, params, y0, 1, 1, h, param_idx, param_range, 1, var_idx, solver=solver)

    print("Program started")

    num_transient   = round(transient_time / h)
    num_record      = round(record_time / h) + 1

    start_time = time.time()
    result = bifurcation1D(f, params, y0, num_record, num_transient, h, param_idx, param_range, N, var_idx, solver=solver)
    end_time = time.time()

    elapsed = end_time - start_time
    print(f"Execution time: {elapsed:.3f} seconds")

    file_base_name = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    save_to_file(file_base_name, result)

    return 0

# ================================================================================

if __name__ == "__main__":
    status = main()
    print(f"Program finished with code {status}")