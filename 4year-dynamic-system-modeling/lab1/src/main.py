from pathlib import Path
import os
import shutil
import numpy as np
from include.input_functions import lorenz
from include.utils import float_to_decimal_str
from modules.integrate import ODESolver

# ==================================================================================================== #

def main() -> int:
    # init variables
    f = lorenz
    args = (10, 28, 8/3)
    tmin = 0; tmax = 10; dt=0.01
    init_conditions = [1.0, 1.0, 1.0]

    # init solver
    solver = ODESolver(f, args, tmin, tmax, dt, init_conditions)

    # init results directory
    results_dir = Path(__file__) / '..' / '..' / 'results'
    target_dir = results_dir / f"{int(tmin)}_{int(tmax)}_{float_to_decimal_str(dt).replace('.', '-')}"

    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    os.makedirs(target_dir)

    # run simulations
    for method in ['euler', 'euler-cromer', 'rk-4', 'midpoint', 'cd-lorenz']:
        # solve
        result = solver.solve(method)
    
        # save results
        np.save(target_dir / f"{method}.npy", result, allow_pickle=False)


    return 0

# ==================================================================================================== #
if __name__ == "__main__":
    status = main()

    if status == 0:
        print("Code finished successfully")
    else:
        print("Code finished with errors")
    