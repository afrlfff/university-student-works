import numpy as np
from numpy.typing import NDArray
import matplotlib.pyplot as plt


def show_attractors(y:  NDArray[np.float32], title=None):
    _, axes = plt.subplots(1, 3, figsize=(10, 6))

    axes[0].plot(y[:, 0], y[:, 1], color='blue')
    if title is not None:
        axes[0].set_title(f"{title} (X-Y)")
    axes[0].set_xlabel('X')
    axes[0].set_ylabel('Y')

    axes[1].plot(y[:, 0], y[:, 2], color='green')
    if title is not None:
        axes[1].set_title(f"{title} (X-Z)")
    axes[1].set_xlabel('X')
    axes[1].set_ylabel('Z')

    axes[2].plot(y[:, 1], y[:, 2], color='red')
    if title is not None:
        axes[2].set_title(f"{title} (Y-Z)")
    axes[2].set_xlabel('Y')
    axes[2].set_ylabel('Z')

    plt.tight_layout()

    plt.show()
