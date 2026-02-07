import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.gridspec as gridspec
import time
from modules.systems import lorenz
from modules.integrate import solve_ode
from modules.integrate.typing import SOLVER_CD_LORENZ
from modules.attractors import find_attractors, find_attractors_parallel, match_trajectory_to_attractor
from modules.attractors.typing import METHOD_CENTROID, METHOD_DIAMETER
from utils import COLORS, to_latex, idx2param, smart_format

# ================================================================================
f       = lorenz
params  = np.array([10, 28, 8/3], dtype=np.float64)

init_x_range = (-50, 50)
init_y_range = (-50, 50)
init_z = 27
N = 50 + 1

transient_time  = 200
record_time     = 200
h               = 0.01

eps = 5.0

solver = SOLVER_CD_LORENZ
method = METHOD_CENTROID
# ================================================================================

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

def calculate_and_plot_attractors(init_conditions, n_record, n_transient, h):
    fig = plt.figure(figsize=(10, 6))
    gs = gridspec.GridSpec(3, 2, height_ratios=[1, 1, 1], width_ratios=[2, 1], hspace=0.3, wspace=0.3)
    ax_xyz = fig.add_subplot(gs[:, 0], projection='3d')
    ax_xy  = fig.add_subplot(gs[0, 1])
    ax_xz  = fig.add_subplot(gs[1, 1])
    ax_yz  = fig.add_subplot(gs[2, 1])

    for i, init_condition in enumerate(init_conditions):
        result = solve_ode(f, params, n_transient + n_record, h, init_condition, solver=SOLVER_CD_LORENZ)
        result = result[n_transient:]

        plot_attractor_3d(ax_xyz, result, color=COLORS[i])
        plot_attractor_2d(result, ax_xy=ax_xy, ax_xz=ax_xz, ax_yz=ax_yz, color=COLORS[i])
    
    legend_elements = [
        Line2D([0], [0], color=COLORS[i], lw=4, label=f'y0 = [{smart_format(init_conditions[i, 0], 3)}, {smart_format(init_conditions[i, 1], 3)}, {smart_format(init_conditions[i, 2], 3)}]')
        for i in range(len(init_conditions))
    ]
    ax_xyz.legend(handles=legend_elements, loc='upper left')

    title="Поиск аттракторов ("
    for i in range(len(params)):
        title += f"{to_latex("\\" + idx2param[i])} = {smart_format(params[i], 3)}"
        if i < len(params) - 1:
            title += ", "
        else:
            title += ")"
    fig.suptitle(title, fontsize=16)
    
    plt.show()

# ================================================================================

def main():
    print("Compiling ...", end=' ')
    _ = find_attractors(f, params, np.array([[1., 1., 1.]], dtype=np.float64), 1, 0, h, eps=eps, solver=solver, method=method)
    _ = find_attractors_parallel(f, params, np.array([[1., 1., 1.]], dtype=np.float64), 1, 0, h, eps=eps, solver=solver, method=method, n_jobs=1)
    print("done")
    
    # constants
    n_transient     = round(transient_time / h)
    n_record        = round(record_time / h) + 1
    init_x_array    = np.linspace(init_x_range[0], init_x_range[1], N)
    init_y_array    = np.linspace(init_y_range[0], init_y_range[1], N)
    X, Y            = np.meshgrid(init_x_array, init_y_array, indexing='ij')
    Z               = np.full_like(X, init_z)
    initial_conditions = np.stack([X, Y, Z], axis=-1).reshape(-1, 3)

    # exclude (0, 0, 27)
    initial_conditions = initial_conditions[(initial_conditions[:, 0] != 0) | (initial_conditions[:, 1] != 0)]

    # find
    start_time = time.time()
    attractors = find_attractors(f, params, initial_conditions, n_record, n_transient, h, eps=eps, solver=solver, debug=True, method=method)
    end_time = time.time()
    elapsed = end_time - start_time
    print(f"Execution time: {elapsed:.3f} seconds")

    # print
    print("Found attractors: [")
    for attractor in attractors:
        print(f"\t[{smart_format(attractor[0], 3)}, {smart_format(attractor[1], 3)}, {smart_format(attractor[2], 3)}],")
    print("]")

    # plot
    calculate_and_plot_attractors(attractors, 2000, 10000, h)

    return 0

# ================================================================================

if __name__ == "__main__":
    status = main()
    print(f"Program finished with code {status}")
    