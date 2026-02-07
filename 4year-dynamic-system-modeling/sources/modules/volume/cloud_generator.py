import numpy as np

def generate_cloud(center, n_points, eps=1e-3, seed=42):
    """
    Создаёт облако из n_points точек вокруг center с небольшими случайными возмущениями.
    """
    np.random.seed(seed)
    perturbations = np.random.normal(scale=eps, size=(n_points, 3))
    cloud = center + perturbations
    return cloud  # shape: (n_points, 3)