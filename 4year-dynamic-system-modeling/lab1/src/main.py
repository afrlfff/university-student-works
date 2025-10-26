from pathlib import Path
import os
import shutil
import numpy as np
from input_functions import lorenz
from integrator import Integrator, IntegratorCacher

# ==================================================================================================== #

def main() -> int:
    # init variables
    f = lorenz
    parameters = (10, 28, 8/3)
    tmin = 0; tmax = 100; dt=0.01
    init_conditions = [1.0, 1.0, 1.0]

    # init integrator
    integrator = Integrator(
        lambda state : f(state=state, parameters=parameters), 
        tmin, tmax, dt, init_conditions
        )
    
    # init cacher
    cache_dir = Path(__file__) / '..' / '..' / 'cache'
    cacher = IntegratorCacher(cache_dir)

    # init results directory
    results_dir = Path(__file__) / '..' /'..' / 'results'
    if os.path.exists(results_dir):
        shutil.rmtree(results_dir)
    os.makedirs(results_dir)

    # run simulations
    for method in ['euler-cromer', 'euler', 'runge-kutta-2', 'runge-kutta-4', 'midpoint', 'cd-lorenz']:
    #for method in ['runge-kutta-2']:
        integrator.set_method(method)

        result = cacher.get(integrator)
        if result is None:
            result = integrator.run()
            cacher.save(integrator=integrator, result=result)
    
        # save results
        np.save(results_dir / f"{method}.npy", result, allow_pickle=False)


    return 0

# ==================================================================================================== #
if __name__ == "__main__":
    status = main()

    if status == 0:
        print("Code finished successfully")
    else:
        print("Code finished with errors")
    