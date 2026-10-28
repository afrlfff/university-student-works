import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from modules.systems import lorenz
from modules.volume import generate_cloud, phase_volume, geometric_volume
from modules.integrate.typing import SOLVER_CD_LORENZ

# ================================================================================
f = lorenz
params = np.array([10, 28, 8/3], dtype=np.float64)
y0 = np.array([1., 1., 1.], dtype=np.float64)
integrate_time = 50
h = 0.01
solver=SOLVER_CD_LORENZ
# ================================================================================

def plot_phase_volume(ax, t, volumes):
    ax.plot(t, volumes, color='blue')
    ax.set_xlabel('t', fontsize=14)
    ax.set_ylabel('V', fontsize=14)
    ax.set_title("Фазовый объем", fontsize=16)

    ax.set_yscale('log')
    ax.grid(True, ls="--")

def plot_geometric_volume(ax, t, volumes):
    ax.plot(t, volumes, color='blue')
    ax.set_xlabel('t', fontsize=14)
    ax.set_ylabel('V', fontsize=14)
    ax.set_title("Геометрический объем", fontsize=16)

    ax.set_yscale('log')
    ax.grid(True, ls="--")

def plot_cloud(ax, cloud):
    ax.scatter(cloud[:, 0], cloud[:, 1], cloud[:, 2], c='blue', alpha=1.0, s=10)
    ax.set_xlabel('X', fontsize=14)
    ax.set_ylabel('Y', fontsize=14)
    ax.set_zlabel('Z', fontsize=14)
    ax.set_title("Начальное облако", fontsize=16)

# ================================================================================

def main():
    print("Compiling ...")
    _ = phase_volume(f, params, 1, h, np.random.normal(scale=1e-3, size=(3, 3)), solver=SOLVER_CD_LORENZ)
    _ = geometric_volume(f, params, 1, h, np.random.normal(scale=1e-3, size=(3, 3)), solver=SOLVER_CD_LORENZ)
    print("done")

    num_integrate   = round(integrate_time / h) + 1
    t               = np.linspace(0, integrate_time, num_integrate)

    start_time = time.time()
    cloud = generate_cloud(y0, 1000, eps=1e-3)
    phase_volumes = phase_volume(f, params, num_integrate, h, cloud, solver=SOLVER_CD_LORENZ)
    geom_volumes = geometric_volume(f, params, num_integrate, h, cloud, solver=SOLVER_CD_LORENZ)
    end_time = time.time()

    elapsed = end_time - start_time
    print(f"Execution time: {elapsed:.3f} seconds")

    fig = plt.figure(figsize=(10, 6))

    gs = gridspec.GridSpec(2, 2, height_ratios=[1, 1], hspace=0.3, wspace=0.3)
    ax0 = fig.add_subplot(gs[:, 0], projection='3d')
    ax_phase = fig.add_subplot(gs[0, 1])
    ax_geom = fig.add_subplot(gs[1, 1])

    num_phase_volume_points = round(1 / h) + 1

    plot_cloud(ax0, cloud)
    plot_phase_volume(ax_phase, t[:num_phase_volume_points], phase_volumes[:num_phase_volume_points])
    plot_geometric_volume(ax_geom, t, geom_volumes)
    plt.tight_layout()
    plt.show()

    return 0

# ================================================================================

if __name__ == "__main__":
    status = main()
    print(f"Program finished with code {status}")