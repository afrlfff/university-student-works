import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import time
from tqdm import tqdm

from modules.systems import lorenz
from modules.integrate.typing import SOLVER_CD_LORENZ
from modules.sync import sync_slave_time_symmetric
from modules.integrate import solve_ode
from utils import idx2var

# ================================================================================
f = lorenz
args = np.array([10, 28, 8/3], dtype=np.float64)

# ===== ЕСТЬ СХОДИМОСТЬ:
y0_master = np.array([-9.6, -15.6, 12.5], dtype=np.float64)
y0_slave = np.array([-4.6, -10.6, 17.5], dtype=np.float64)

transient_time  = 0
record_time     = 10
window_time     = 0.15

h = 0.01

K_forw = 40
K_back = 40
n_iter = 100

sync_var_idx = 1

# ===== НЕТ СХОДИМОСТИ:
# y0_master = np.array([-4.05, -8., 6.65405], dtype=np.float64)
# y0_slave = np.array([-9.05, -13., 11.65405], dtype=np.float64)

# transient_time  = 0
# record_time     = 10
# window_time     = 0.15

# h = 0.01

# K_forw = 40
# K_back = 40
# n_iter = 100

# sync_var_idx = 1

solver=SOLVER_CD_LORENZ
# ================================================================================

def plot_attractor_2d(attractor, ax_xy=None, ax_xz=None, ax_yz=None, color='blue', linestyle='solid', marker=None, ms=None):
    if ax_xy is not None:
        ax_xy.plot(attractor[:, 0], attractor[:, 1], c=color, linestyle=linestyle, marker=marker, ms=ms)
        ax_xy.set_xlabel('X', fontsize=14)
        ax_xy.set_ylabel('Y', fontsize=14, rotation=0, ha='right')
        ax_xy.grid(True, linestyle='--')
    
    if ax_xz is not None:
        ax_xz.plot(attractor[:, 0], attractor[:, 2], c=color, linestyle=linestyle, marker=marker, ms=ms)
        ax_xz.set_xlabel('X', fontsize=14)
        ax_xz.set_ylabel('Z', fontsize=14, rotation=0, ha='right')
        ax_xz.grid(True, linestyle='--')
    
    if ax_yz is not None:
        ax_yz.plot(attractor[:, 1], attractor[:, 2], c=color, linestyle=linestyle, marker=marker, ms=ms)
        ax_yz.set_xlabel('Y', fontsize=14)
        ax_yz.set_ylabel('Z', fontsize=14, rotation=0, ha='right')
        ax_yz.grid(True, linestyle='--')

def plot_error(t, y_master, y_slave, ax_x=None, ax_y=None, ax_z=None, color='blue', marker=None, label=None, xlabel='t'):
    axes = [ax_x, ax_y, ax_z]
    loss = abs(y_master - y_slave)

    for i in range(len(axes)):
        if axes[i] is not None:
            axes[i].plot(t, loss[:, i], marker=marker, color=color, label=label)
            axes[i].set_xlabel(xlabel, fontsize=14)
            axes[i].set_ylabel(fr'$|{idx2var[i]}_m - {idx2var[i]}_s|$', fontsize=14)
            axes[i].set_yscale('log')
            axes[i].grid(True, linestyle='--')
            axes[i].set_xlim(t[0], t[-1])

# ================================================================================

def main():
    print("Compiling ...", end=' ')
    _ = sync_slave_time_symmetric(f, args, np.array([1, 1, 1], dtype=np.float64), h, np.array([[1, 1, 1]], dtype=np.float64), 1, 1, 0, 0, solver=SOLVER_CD_LORENZ)
    print("done")

    n_window    = round(window_time / h)
    n_transient = round(transient_time / h)
    n_record    = round(record_time / h) + 1

    start_time = time.time()
    print("Integrate master ...", end=' ')
    y_master    = solve_ode(f, args, n_transient + n_record, h, y0_master, solver=solver)
    y_master    = y_master[n_transient: ]
    y_slave     = solve_ode(f, args, n_transient + 1, h, y0_slave, solver=solver)
    y_slave     = y_slave[n_transient: ]
    print('done')

    slave_trajectories = np.array([
        sync_slave_time_symmetric(f, args, y_slave[0], h, y_master, iters, n_window, K_forw, K_back, sync_var_idx=sync_var_idx, solver=solver, debug=False)
        for iters in tqdm(range(1, n_iter + 1), desc="Integrate slave for all iterations ...")], dtype=np.float64)

    end_time = time.time()
    elapsed = end_time - start_time
    print(f"Execution time: {elapsed:.3f} seconds")

    # PLOT ATTRACTORS
    fig = plt.figure(figsize=(17, 5))
    ax_xy = fig.add_subplot(1, 3, 1)
    ax_xz = fig.add_subplot(1, 3, 2)
    ax_yz = fig.add_subplot(1, 3, 3)
    plot_attractor_2d(y_master, ax_xy=ax_xy, ax_xz=ax_xz, ax_yz=ax_yz, color='blue', linestyle='solid')
    plot_attractor_2d(y_master[: n_window], ax_xy=ax_xy, ax_xz=ax_xz, ax_yz=ax_yz, color='blue', linestyle='dashed', marker='o', ms=8)
    plot_attractor_2d(slave_trajectories[0], ax_xy=ax_xy, ax_xz=ax_xz, ax_yz=ax_yz, color='red', linestyle='dashed', marker='o', ms=4)
    plot_attractor_2d(slave_trajectories[-1], ax_xy=ax_xy, ax_xz=ax_xz, ax_yz=ax_yz, color='limegreen', linestyle='dashed', marker='o', ms=4)

    legend_elements = [
        Line2D([0], [0], color='blue', linestyle='solid', label='Master (full)'),
        Line2D([0], [0], color='blue', linestyle='dashed', marker='o', label='Master (window)'),
        Line2D([0], [0], color='red', linestyle='dashed', marker='o', label='Slave (window, 1 iteration)'),
        Line2D([0], [0], color='limegreen', linestyle='dashed', marker='o', label=f'Slave (window, {n_iter} iteration)')
    ]

    fig.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, 1.0), ncol=4, fontsize=12)
    plt.tight_layout(rect=[0, 0, 1, 0.9])  # оставить место под легенду

    # PLOT ERROR
    fig = plt.figure(figsize=(12, 6))
    ax_x = fig.add_subplot(3, 1, 1)
    ax_y = fig.add_subplot(3, 1, 2)
    ax_z = fig.add_subplot(3, 1, 3)

    t = np.linspace(0, window_time, n_window)
    plot_error(t, y_master[: n_window], slave_trajectories[0], ax_x=ax_x, ax_y=ax_y, ax_z=ax_z, color='red')
    plot_error(t, y_master[: n_window], slave_trajectories[-1], ax_x=ax_x, ax_y=ax_y, ax_z=ax_z, color='limegreen')

    legend_elements = [
        Line2D([0], [0], color='red', linestyle='solid', label='1 iteration'),
        Line2D([0], [0], color='limegreen', linestyle='solid', label=f'{n_iter} iteration')
    ]

    fig.legend(handles=legend_elements, loc='center right', bbox_to_anchor=(1.0, 0.5), ncols=1, fontsize=12)
    plt.tight_layout(rect=[0, 0, 0.85, 1])  # уменьшить правую границу для места под легенду

    # PLOT CONVERGENCE
    fig = plt.figure(figsize=(12, 6))
    ax_x = fig.add_subplot(3, 1, 1)
    ax_y = fig.add_subplot(3, 1, 2)
    ax_z = fig.add_subplot(3, 1, 3)

    t = np.linspace(0, n_iter, n_iter)
    plot_error(t, np.repeat([y_master[n_window - 1]], n_iter, axis=0), slave_trajectories[:, -1], ax_x=ax_x, ax_y=ax_y, ax_z=ax_z, color='blue', marker='o', xlabel='Iteration')

    # show
    plt.show()

    return 0

# ================================================================================

if __name__ == "__main__":
    status = main()
    print(f"Program finished with code {status}")