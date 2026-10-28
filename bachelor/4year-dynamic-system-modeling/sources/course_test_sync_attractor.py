import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.mplot3d.art3d import Line3DCollection, LineCollection
from matplotlib.colors import LinearSegmentedColormap
from tqdm import tqdm
from multiprocessing import Pool
import functools

from modules.systems import lorenz
from modules.integrate.typing import SOLVER_CD_LORENZ
from modules.integrate import solve_ode
from modules.sync import sync_slave_time_symmetric

# ================================================================================
f = lorenz
params = np.array([10, 28, 8/3], dtype=np.float64)

y0_master = np.array([3., -3., 0.], dtype=np.float64)

transient_time      = 1000
record_time         = 200
slave_offset_time   = 5
window_time         = 0.15

h = 0.001

K_forw = 40
K_back = 40
n_iter = 200

sync_var_idx = 1
decimation = 5

solver=SOLVER_CD_LORENZ
# ================================================================================

def sync_error(master_start, slave_start, master_end, slave_end):
    start_error = np.linalg.norm(master_start - slave_start)
    end_error   = np.linalg.norm(master_end - slave_end)
    return np.log10(end_error) - np.log10(start_error)

def plot_sync_attractor(fig, master_traj, errors, ax_xyz=None, ax_xy=None, ax_xz=None, ax_yz=None, lines=True):
    v_min, v_max = np.floor(errors.min()), np.ceil(errors.max())
    
    if v_min < 0 and v_max > 0:
        n_total = 1000
        n_neg = int(round((-v_min) / (v_max - v_min) * n_total))
        n_pos = n_total - n_neg
        colors_neg = plt.cm.turbo(np.linspace(0, 1, n_neg))
        colors_pos = plt.cm.Blues(np.linspace(1, 0, n_pos))
        colors = np.vstack([colors_neg, colors_pos])
    elif v_min >= 0:
        v_min = 0
        colors = plt.cm.Blues(np.linspace(1, 0, 1000))
    else:  # v_max <= 0
        v_max = 0
        colors = plt.cm.turbo(np.linspace(0, 1, 1000))
    
    custom_cmap = LinearSegmentedColormap.from_list("neg_turbo_pos_blues", colors)
    norm = plt.Normalize(v_min, v_max)
    
    if ax_xyz:
        if lines:
            segments_xyz = np.stack([master_traj[:-1], master_traj[1:]], axis=1)
            lc = Line3DCollection(segments_xyz, cmap=custom_cmap, norm=norm)
            lc.set_array(errors[:-1])
            ax_xyz.add_collection(lc)
            cbar = fig.colorbar(lc, ax=ax_xyz, label=r'$\Delta \log_{10}(\|\mathrm{Error}\|)$', shrink=0.8, pad=0.16)
        else:
            scatter = ax_xyz.scatter(
                master_traj[:, 0],
                master_traj[:, 1],
                master_traj[:, 2],
                c=errors,
                cmap=custom_cmap,
                norm=norm,
                s=1
            )
            cbar = fig.colorbar(scatter, ax=ax_xyz, label=r'$\Delta \log_{10}(\|\mathrm{Error}\|)$', shrink=0.8, pad=0.16)
        
        cbar.ax.tick_params(labelsize=12)
        cbar.set_label(r'$\Delta \log_{10}(\|\mathrm{Error}\|)$', fontsize=14)
        
        ax_xyz.set_xlim(-20, 20)
        ax_xyz.set_ylim(master_traj[:, 1].min(), master_traj[:, 1].max())
        ax_xyz.set_yticks([-20,-10,0,10,20])
        ax_xyz.set_zlim(0, 50)
        
        ax_xyz.set_xlabel(r'$x$', fontsize=14)
        ax_xyz.set_ylabel(r'$y$', fontsize=14)
        ax_xyz.set_zlabel(r'$z$', fontsize=14)
        ax_xyz.view_init(elev=10, azim=135)
    
    if ax_xy:
        if lines:
            segments_xy = np.stack([master_traj[:-1, [0, 1]], master_traj[1:, [0, 1]]], axis=1)
            lc_xy = LineCollection(segments_xy, cmap=custom_cmap, norm=norm)
            lc_xy.set_array(errors[:-1])
            ax_xy.add_collection(lc_xy)
        else:
            ax_xy.scatter(
                master_traj[:, 0],
                master_traj[:, 1],
                c=errors,
                cmap=custom_cmap,
                norm=norm,
                s=1
            )
        ax_xy.set_xlabel('X', fontsize=14)
        ax_xy.set_ylabel('Y', fontsize=14, rotation=0, ha='right')
        ax_xy.grid(True, linestyle='--')
        ax_xy.set_xlim(-20, 20)
        ax_xy.set_ylim(-25, 25)

    if ax_xz:
        if lines:
            segments_xz = np.stack([master_traj[:-1, [0, 2]], master_traj[1:, [0, 2]]], axis=1)
            lc_xz = LineCollection(segments_xz, cmap=custom_cmap, norm=norm)
            lc_xz.set_array(errors[:-1])
            ax_xz.add_collection(lc_xz)
        else:
            ax_xz.scatter(
                master_traj[:, 0],
                master_traj[:, 2],
                c=errors,
                cmap=custom_cmap,
                norm=norm,
                s=1
            )
        ax_xz.set_xlabel('X', fontsize=14)
        ax_xz.set_ylabel('Z', fontsize=14, rotation=0, ha='right')
        ax_xz.grid(True, linestyle='--')
        ax_xz.set_xlim(-20, 20)
        ax_xz.set_ylim(0, 50)

    if ax_yz:
        if lines:
            segments_yz = np.stack([master_traj[:-1, [1, 2]], master_traj[1:, [1, 2]]], axis=1)
            lc_yz = LineCollection(segments_yz, cmap=custom_cmap, norm=norm)
            lc_yz.set_array(errors[:-1])
            ax_yz.add_collection(lc_yz)
        else:
            ax_yz.scatter(
                master_traj[:, 1],
                master_traj[:, 2],
                c=errors,
                cmap=custom_cmap,
                norm=norm,
                s=1
            )
        ax_yz.set_xlabel('Y', fontsize=14)
        ax_yz.set_ylabel('Z', fontsize=14, rotation=0, ha='right')
        ax_yz.grid(True, linestyle='--')
        ax_yz.set_xlim(-25, 25)
        ax_yz.set_ylim(0, 50)

def plot_error(ax, errors):
    t = np.arange(0, record_time + 1e-6, h)
    t = t[:: decimation]

    ax.scatter(t, errors, color='blue', s=1)
    ax.axhline(y=0, color='black', linestyle='--', linewidth=1)
    ax.set_xlabel("t", fontsize=14)
    ax.set_ylabel(r'$\Delta \log_{10}(\|\mathrm{Error}\|)$', fontsize=14)
    ax.grid(True, linestyle='--')
    ax.set_xlim(0, record_time)

    if not(np.isnan(errors.min())) and not(np.isnan(errors.max())): 
        ax.set_ylim(np.floor(errors.min()), np.ceil(errors.max()))

# ================================================================================

def _process_one(y_master, n_slave_offset, n_window, index):
    # 1) either shift on 5 point by each coordiante
    y0_slave = y_master[index] + 5
    # 2) or move to 5 seconds forward
    # y0_slave = y_master[index + n_slave_offset]

    y_slave = sync_slave_time_symmetric(f, params, y0_slave, h, y_master[index: index + n_window], n_iter, n_window, K_forw, K_back, sync_var_idx=sync_var_idx, solver=solver)
    
    return sync_error(y_master[index], y0_slave, y_master[index + n_window - 1], y_slave[n_window - 1])

# ================================================================================

def main():
    print("Compiling ...", end=' ')
    _ = sync_slave_time_symmetric(f, params, np.array([1, 1, 1], dtype=np.float64), h, np.array([[1, 1, 1]], dtype=np.float64), 1, 1, 0, 0, solver=solver)
    print("done")

    n_transient         = round(transient_time / h)
    n_record            = round(record_time / h) + 1
    n_slave_offset      = round(slave_offset_time / h)
    n_window            = round(window_time / h)   
    decimation_idxs     = np.arange(0, n_record - 1 + 1e-6, decimation, dtype=int)

    start_time  = time.time()
    
    # INTEGRATING
    print("Integrate master ...", end=' ')
    y_master    = solve_ode(f, params, n_transient + n_record + n_window + n_slave_offset, h, y0_master, solver=solver)
    y_master    = y_master[n_transient :]
    print("done")
    
    # PROCESS PARALLEL:
    worker = functools.partial(_process_one, y_master, n_slave_offset, n_window)
    with Pool(processes=None) as pool:
        errors = list(tqdm(pool.imap(worker, decimation_idxs), total=len(decimation_idxs), desc="Synchroniztion for each master point ..."))
    errors = np.array(errors, dtype=np.float64)
    
    end_time    = time.time()
    elapsed     = end_time - start_time
    print(f"Execution time: {elapsed:.3f} seconds")

    # PLOTTING
    print("Plot ...", end=' ')
    fig = plt.figure(figsize=(18, 9))
    gs = gridspec.GridSpec(2, 3, height_ratios=[1, 1], width_ratios=[1, 1, 1], hspace=0.0, wspace=0.1)

    idxs_non_nan  = np.flatnonzero(~np.isnan(errors))
    idxs_positive = np.where(errors >= 0)
    idxs_negative = np.where(errors <= 0)

    ax_xyz = fig.add_subplot(gs[0, 0], projection='3d')
    plot_sync_attractor(fig, y_master[decimation_idxs][idxs_non_nan], errors[idxs_non_nan], ax_xyz=ax_xyz)
    ax_xyz = fig.add_subplot(gs[0, 1], projection='3d')
    plot_sync_attractor(fig, y_master[decimation_idxs][idxs_positive], errors[idxs_positive], ax_xyz=ax_xyz, lines=False)
    ax_xyz = fig.add_subplot(gs[0, 2], projection='3d')
    plot_sync_attractor(fig, y_master[decimation_idxs][idxs_negative], errors[idxs_negative], ax_xyz=ax_xyz, lines=False)
    ax_xy = fig.add_subplot(gs[1, :])
    plot_error(ax_xy, errors)
    
    # Plot only attractor:     
    fig = plt.figure(figsize=(15, 9))
    gs = gridspec.GridSpec(3, 2, height_ratios=[1, 1, 1], width_ratios=[2, 1], hspace=0.3, wspace=0.15)

    ax_xyz = fig.add_subplot(gs[:, 0], projection='3d')
    ax_xy  = fig.add_subplot(gs[0, 1])
    ax_xz  = fig.add_subplot(gs[1, 1])
    ax_yz  = fig.add_subplot(gs[2, 1])
    plot_sync_attractor(fig, y_master[decimation_idxs][idxs_non_nan], errors[idxs_non_nan], ax_xyz=ax_xyz, ax_xy=ax_xy, ax_xz=ax_xz, ax_yz=ax_yz)

    #
    print("done")
    plt.show()

    return 0

# ================================================================================

if __name__ == "__main__":
    status = main()
    print(f"Program finished with code {status}")