import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap

from modules.systems import lorenz
from modules.basins import attraction_basins, attraction_basins_parallel
from modules.integrate.typing import SOLVER_CD_LORENZ
from utils import COLORS, idx2var, smart_format

# ================================================================================
f = lorenz
params = np.array([10, 28, 4], dtype=np.float64)

var_idxs = [0, 1]
init_var1_range = (-200, 200)
init_var2_range = (-200, 200)
init_var3       = 27

transient_time = 200; record_time = 200
h = 0.01
N = 500

solver=SOLVER_CD_LORENZ

attractor_init_conditions = np.array([
    [-50., -50., 27.],
    [-50., -28., 27.]
], dtype=np.float64)

legends = [Patch(
    facecolor=COLORS[i], 
    label=f"y0 = [{smart_format(attractor_init_conditions[i, 0], 3)}, {smart_format(attractor_init_conditions[i, 1], 3)}, {smart_format(attractor_init_conditions[i, 2], 3)}]") 
    for i in range(len(attractor_init_conditions)
)]
# ================================================================================

def plot_attraction_basins(ax, matches):
    img_labels = matches.reshape(N, N)
    cmap = ListedColormap(COLORS[:matches.max() + 1])

    img = ax.imshow(img_labels, 
        origin='lower', aspect='auto', cmap=cmap,
        extent=(init_var1_range[0], init_var1_range[1], init_var2_range[0], init_var2_range[1])
        )
    ax.set_xlabel(idx2var[var_idxs[0]].upper(), fontsize=14)
    ax.set_ylabel(idx2var[var_idxs[1]].upper(), fontsize=14, rotation=0, ha='right')

    return img

# ================================================================================

def main():
    print("Compiling ...", end=' ')
    # _ = attraction_basins(f, params, np.array([[1, 1, 1]], dtype=np.float64), np.array([[1, 1, 1]], dtype=np.float64), 1, 1, h, solver=solver)
    _ = attraction_basins_parallel(f, params, np.array([[1, 1, 1]], dtype=np.float64), np.array([[1, 1, 1]], dtype=np.float64), 1, 1, h, solver=solver, n_jobs=1)
    print("done")

    n_transient     = round(transient_time / h)
    n_record        = round(record_time / h) + 1
    var1_array      = np.linspace(init_var1_range[0], init_var1_range[1], N)
    var2_array      = np.linspace(init_var2_range[0], init_var2_range[1], N)
    V1, V2          = np.meshgrid(var1_array, var2_array, indexing='ij')
    V3              = np.full_like(V1, init_var3)
    if var_idxs[0] == 0 and var_idxs[1] == 1:
        initial_conditions = np.stack([V1, V2, V3], axis=-1).reshape(-1, 3)
    elif var_idxs[0] == 0 and var_idxs[1] == 2:
        initial_conditions = np.stack([V1, V3, V2], axis=-1).reshape(-1, 3)
    elif var_idxs[0] == 1 and var_idxs[1] == 2:
        initial_conditions = np.stack([V3, V1, V2], axis=-1).reshape(-1, 3)

    start_time = time.time()
    matches = attraction_basins_parallel(f, params, initial_conditions, attractor_init_conditions, n_record, n_transient, h, n_match_points=10, solver=solver, debug=True)
    end_time = time.time()
    elapsed = end_time - start_time
    print(f"Execution time: {elapsed:.3f} seconds")

    fig, ax = plt.subplots(figsize=(10, 6))
    plot_attraction_basins(ax, matches)
    ax.legend(handles=legends, loc='upper right')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.tight_layout()
    plt.show()

    return 0

# ================================================================================

if __name__ == "__main__":
    status = main()
    print(f"Program finished with code {status}")