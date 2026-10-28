import numpy as np
import matplotlib.pyplot as plt
import time

from modules.systems import lorenz
from modules.integrate.typing import SOLVER_CD_LORENZ
from modules.sync import sync_slave_pecora_carrol
from modules.integrate import solve_ode
from utils import idx2var

# ================================================================================
f = lorenz
args = np.array([10, 28, 8/3], dtype=np.float64)

y0_master = np.array([1., 1., 1.], dtype=np.float64)
y0_slave = np.array([15., -10., 20.], dtype=np.float64)

integration_time = 50
h = 0.001

sync_coeff = 100.0
sync_var_idx = 2

solver=SOLVER_CD_LORENZ
# ================================================================================

def plot_attractor_2d(attractor, ax_xy=None, ax_xz=None, ax_yz=None, color='blue', linestyle='solid'):
    if ax_xy is not None:
        ax_xy.plot(attractor[:, 0], attractor[:, 1], c=color, linestyle=linestyle)
        ax_xy.set_xlabel('X', fontsize=14)
        ax_xy.set_ylabel('Y', fontsize=14, rotation=0, ha='right')
        ax_xy.grid(True, linestyle='--')
    
    if ax_xz is not None:
        ax_xz.plot(attractor[:, 0], attractor[:, 2], c=color, linestyle=linestyle)
        ax_xz.set_xlabel('X', fontsize=14)
        ax_xz.set_ylabel('Z', fontsize=14, rotation=0, ha='right')
        ax_xz.grid(True, linestyle='--')
    
    if ax_yz is not None:
        ax_yz.plot(attractor[:, 1], attractor[:, 2], c=color, linestyle=linestyle)
        ax_yz.set_xlabel('Y', fontsize=14)
        ax_yz.set_ylabel('Z', fontsize=14, rotation=0, ha='right')
        ax_yz.grid(True, linestyle='--')

def plot_error(y_master, y_slave, ax_x=None, ax_y=None, ax_z=None):
    t = np.arange(0, integration_time + 1e-6, h)
    loss = abs(y_master - y_slave)
    axes = [ax_x, ax_y, ax_z]

    for i in range(len(axes)):
        if axes[i] is not None:
            axes[i].plot(t, loss[:, i], marker=None, ms=1, color='b')
            axes[i].set_xlabel('t')
            axes[i].set_ylabel(fr'$|{idx2var[i]}_m - {idx2var[i]}_s|$')
            axes[i].set_yscale('log')
            axes[i].grid(True, linestyle='--')

# ================================================================================

def main():
    print("Compiling ...", end=' ')
    _ = sync_slave_pecora_carrol(f, args, np.array([1, 1, 1], dtype=np.float64), 1, h, np.array([[1, 1, 1]], dtype=np.float64), 0, 0, solver=SOLVER_CD_LORENZ)
    print("done")

    n_steps = 1 + round(integration_time / h)
    
    start_time = time.time()
    y_master = solve_ode(f, args, n_steps, h, y0_master, solver=solver)
    y_slave  = sync_slave_pecora_carrol(f, args, y0_slave, n_steps, h, y_master, sync_coeff, sync_var_idx, solver=solver, debug=True)
    end_time = time.time()

    elapsed = end_time - start_time
    print(f"Execution time: {elapsed:.3f} seconds")

    # plot attractors
    fig = plt.figure(figsize=(12, 5))
    ax_xy = fig.add_subplot(1, 3, 1)
    ax_xz = fig.add_subplot(1, 3, 2)
    ax_yz = fig.add_subplot(1, 3, 3)
    plot_attractor_2d(y_master, ax_xy=ax_xy, ax_xz=ax_xz, ax_yz=ax_yz, color='blue', linestyle='solid')
    plot_attractor_2d(y_slave, ax_xy=ax_xy, ax_xz=ax_xz, ax_yz=ax_yz, color='red', linestyle='dashed')

    # plot error
    fig = plt.figure(figsize=(10, 6))
    ax_x = fig.add_subplot(3, 1, 1)
    ax_y = fig.add_subplot(3, 1, 2)
    ax_z = fig.add_subplot(3, 1, 3)
    plot_error(y_master, y_slave, ax_x=ax_x, ax_y=ax_y, ax_z=ax_z)

    plt.tight_layout()
    plt.show()

    return 0

# ================================================================================

if __name__ == "__main__":
    status = main()
    print(f"Program finished with code {status}")