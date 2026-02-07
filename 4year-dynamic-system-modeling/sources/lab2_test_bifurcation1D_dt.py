import numpy as np
import json
import time
from datetime import datetime
from pathlib import Path
from tqdm import tqdm

from modules.integrate import solve_ode
from modules.integrate.typing import SOLVER_CD_LORENZ
from modules.systems import lorenz

# ================================================================================
f = lorenz
params = np.array([10, 28, 8/3], dtype=np.float64)
y0 = np.array([1., 1., 1.], dtype=np.float64)

record_time = 200
transient_time = 200

h_range = (0.001, 0.1)
N = 250

var_idx = 0

solver=SOLVER_CD_LORENZ
# ================================================================================

def save_to_file(file_base_name, result):
    metadata = {
        "record_time": record_time,
        "transient_time": transient_time,
        "params": params.tolist(),
        "h_range": h_range,
        "N": N,
        "var_idx": var_idx,
    }

    meta_bytes = json.dumps(metadata).encode('utf-8')
    meta_array = np.frombuffer(meta_bytes, dtype='S1')

    results_dir = (Path(__file__) / '..' / '..' / 'results' / 'bifurcation1D_dt').resolve()
    results_dir.mkdir(parents=True, exist_ok=True)

    np.savez(results_dir / f'{file_base_name}.npz', data=result, metadata=meta_array)

# ================================================================================

def main():
    print("Compiling ...")
    _ = solve_ode(f, params, 1, 0.01, y0, solver=solver)

    print("Program started")

    h_values = np.logspace(np.log10(h_range[0]), np.log10(h_range[1]), num=N, base=10)
    results = np.empty(N, dtype=object)
    
    start_time = time.time()
    for i, h in enumerate(tqdm(h_values, desc="Processing ...")):    
        num_transient   = round(transient_time / h)
        num_record      = round(record_time / h) + 1
        y = solve_ode(f, params, num_transient + num_record, h, y0, solver=solver)
        y = y[num_transient::, var_idx]
        results[i] = y
    end_time = time.time()
    elapsed = end_time - start_time
    print(f"Execution time: {elapsed:.3f} seconds")

    file_base_name = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    save_to_file(file_base_name, results)

    return 0

# ================================================================================

if __name__ == "__main__":
    status = main()
    print(f"Code finished with code {status}")