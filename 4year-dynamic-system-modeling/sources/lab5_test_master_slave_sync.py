import numpy as np
import json
import time
from datetime import datetime
from pathlib import Path

from modules.systems import lorenz
from modules.integrate.typing import SOLVER_CD_LORENZ
from modules.sync import sync_master_slave_system

# ================================================================================
f = lorenz
args = np.array([10, 28, 8/3], dtype=np.float64)

y0_master = np.array([1., 1., 1.], dtype=np.float64)
y0_slave = np.array([15., -10., 20.], dtype=np.float64)

intergration_time = 100
h = 0.001

sync_coeff = 100.0
sync_var_idx = 2

solver=SOLVER_CD_LORENZ
# ================================================================================

def save_to_file(file_base_name, result):
    metadata = {
        "f": str(f.__name__),
        "args": args.tolist(),
        "y0_master": y0_master.tolist(),
        "y0_slave": y0_slave.tolist(),
        "integration_time": intergration_time,
        "h": h,
        "sync_coeff": sync_coeff,
        "sync_var_idx": sync_var_idx,
    }

    meta_bytes = json.dumps(metadata).encode('utf-8')
    meta_array = np.frombuffer(meta_bytes, dtype='S1')

    results_dir = (Path(__file__) / '..' / '..' / 'results' / 'sync_bidirectional').resolve()
    results_dir.mkdir(parents=True, exist_ok=True)

    np.savez(results_dir / f'{file_base_name}.npz', data=result, metadata=meta_array)

# ================================================================================

def main():
    print("Program started")

    num_steps = 1 + round(intergration_time / h)

    start_time = time.time()
    result  = sync_master_slave_system(f, args, y0_slave, y0_master, num_steps, h, sync_coeff, sync_var_idx, solver)
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