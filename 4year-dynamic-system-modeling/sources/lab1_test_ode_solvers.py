from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import time
from datetime import datetime
from modules.systems import lorenz
from modules.integrate import solve_ode
from modules.integrate.typing import SOLVER_EULER, SOLVER_EULER_CROMER, SOLVER_MIDPOINT, SOLVER_RK4, SOLVER_CD

# ================================================================================
f       = lorenz
params  = np.array([10, 28, 8/3], dtype=np.float64)
y0      = np.array([1., 20., 1.], dtype=np.float64)

record_time = 100
h           = 0.01

solvers = [SOLVER_EULER, SOLVER_EULER_CROMER, SOLVER_MIDPOINT, SOLVER_RK4, SOLVER_CD]
# ================================================================================

def save_to_file(file_base_name, results):
    metadata = {
        "record_time": record_time,
        "h": round(float(h), 6),
        "solvers": [int(solver) for solver in solvers]
    }

    meta_bytes = json.dumps(metadata).encode('utf-8')
    meta_array = np.frombuffer(meta_bytes, dtype='S1')

    results_dir = (Path(__file__) / '..' / '..' / 'results' / 'ode_solvers').resolve()
    results_dir.mkdir(parents=True, exist_ok=True)

    np.savez(results_dir / f'{file_base_name}.npz', data=results, metadata=meta_array)

def plot_attractor_3d(ax, attractor, color='blue'):
    ax.plot(attractor[:, 0], attractor[:, 1], attractor[:, 2], c=color)

    ax.set_xlabel('X', fontsize=14)
    ax.set_ylabel('Y', fontsize=14)
    ax.set_zlabel('Z', fontsize=14)

def plot_attractor_2d(attractor, ax_xy=None, ax_xz=None, ax_yz=None, color='blue'):
    if ax_xy is not None:
        ax_xy.plot(attractor[:, 0], attractor[:, 1], c=color)
        ax_xy.set_xlabel('X', fontsize=14)
        ax_xy.set_ylabel('Y', fontsize=14, rotation=0, ha='right')
        ax_xy.grid(True, linestyle='--')
    
    if ax_xz is not None:
        ax_xz.plot(attractor[:, 0], attractor[:, 2], c=color)
        ax_xz.set_xlabel('X', fontsize=14)
        ax_xz.set_ylabel('Z', fontsize=14, rotation=0, ha='right')
        ax_xz.grid(True, linestyle='--')
    
    if ax_yz is not None:
        ax_yz.plot(attractor[:, 1], attractor[:, 2], c=color)
        ax_yz.set_xlabel('Y', fontsize=14)
        ax_yz.set_ylabel('Z', fontsize=14, rotation=0, ha='right')
        ax_yz.grid(True, linestyle='--')

# ================================================================================

def main():
    print("Compiling ...", end=' ')
    _ = solve_ode(f, params, 1, h, y0, solver=solvers[0])
    print("done")
    
    num_steps = 1 + round(record_time / h)
    results = np.zeros( (len(solvers), num_steps, 3), dtype=np.float64 )

    # solve
    for i, solver in enumerate(solvers):
        start_time = time.time()
        result = solve_ode(f, params, num_steps, h, y0, solver=solver)
        end_time = time.time()
        
        elapsed = end_time - start_time
        print(f"({solver}) Execution time: {elapsed:.3f} seconds")

        results[i] = result

    # plot
    fig = plt.figure(figsize=(10, 6))
    gs = gridspec.GridSpec(3, 2, height_ratios=[1, 1, 1], width_ratios=[2, 1], hspace=0.3, wspace=0.3)

    ax_xyz = fig.add_subplot(gs[:, 0], projection='3d')
    ax_xy  = fig.add_subplot(gs[0, 1])
    ax_xz  = fig.add_subplot(gs[1, 1])
    ax_yz  = fig.add_subplot(gs[2, 1])

    plot_attractor_3d(ax_xyz, results[-1])
    plot_attractor_2d(results[-1], ax_xy=ax_xy, ax_xz=ax_xz, ax_yz=ax_yz)

    plt.show()

    # save
        # file_base_name = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        # save_to_file(file_base_name, results)

    return 0

# ================================================================================

if __name__ == "__main__":
    status = main()
    print(f"Program finished with code {status}")
    