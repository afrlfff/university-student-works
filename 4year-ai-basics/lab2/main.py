from mymulticlass import *
from sklearn.datasets import load_iris, load_wine
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

# ==============================================================================

def plot_decision_boundary(ax, x1, x2, y, theta, xlabel=None, ylabel=None, title=None, target_names_map=None):
    # colors = ['blue', 'green', 'red', 'purple', 'orange']
    cmap = plt.cm.tab10

    h = 0.02
    x_min, x_max = x1.min() - 1, x1.max() + 1
    y_min, y_max = x2.min() - 1, x2.max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), 
                         np.arange(y_min, y_max, h))
    
    grid_points = np.c_[xx.ravel(), yy.ravel()]
    Z = mypredict(theta, grid_points)
    Z = Z.reshape(xx.shape)

    n_classes = len(np.unique(y))
    cmap_truncated = ListedColormap(cmap.colors[:n_classes])

    ax.contourf(xx, yy, Z, alpha=0.3, cmap=cmap_truncated)
    
    for class_idx in np.unique(y):
        mask = y == class_idx
        color = cmap_truncated(class_idx)
        label = target_names_map[class_idx] if target_names_map else f'Class {class_idx}'
        ax.scatter(x1[mask], x2[mask], c=color, edgecolors='k', s=20, label=label)
    
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(loc='upper right')

# ==============================================================================

if __name__ == '__main__':
    LEARNING_RATE = 0.1
    NUM_ITERATIONS = 1000
    
    # Indices for visualization
    IRIS_FEAT_IDX = [2, 3]  # petal length, petal width
    WINE_FEAT_NAMES = ['proline', 'hue']
    
    # ========== IRIS DATASET ==========
    data = load_iris()
    X_iris = data.data
    y_iris = data.target
    fnames_iris = data.feature_names
    TARGET_NAMES_MAP_IRIS = {i: data.target_names[i] for i in np.unique(y_iris)}
    
    # Scale iris data
    scaler_iris = StandardScaler()
    X_iris_scaled = scaler_iris.fit_transform(X_iris)
    
    # Custom Iris - 2 features
    W_custom_iris_2 = mylearn(X_iris_scaled[:, IRIS_FEAT_IDX], y_iris, 
                              eta=LEARNING_RATE, T=NUM_ITERATIONS)
    y_pred_custom_2 = mypredict(W_custom_iris_2, X_iris_scaled[:, IRIS_FEAT_IDX])
    acc_custom_2 = np.mean(y_pred_custom_2 == y_iris) * 100
    print(f'Custom Softmax Iris (2 features) accuracy: {acc_custom_2:.2f}%')
    
    # Custom Iris - 4 features
    W_custom_iris_4_full = mylearn(X_iris_scaled, y_iris, 
                                   eta=LEARNING_RATE, T=NUM_ITERATIONS)
    W_custom_iris_4 = W_custom_iris_4_full[[0, 3, 4], :]
    y_pred_custom_4 = mypredict(W_custom_iris_4_full, X_iris_scaled)
    acc_custom_4 = np.mean(y_pred_custom_4 == y_iris) * 100
    print(f'Custom Softmax Iris (4 features) accuracy: {acc_custom_4:.2f}%')
    
    # Sklearn Iris - 2 features
    model_sklearn_iris_2 = LogisticRegression(max_iter=1000, solver='lbfgs')
    model_sklearn_iris_2.fit(X_iris_scaled[:, IRIS_FEAT_IDX], y_iris)
    W_sklearn_iris_2 = np.hstack([model_sklearn_iris_2.intercept_.reshape(-1, 1), 
                                   model_sklearn_iris_2.coef_]).T
    y_pred_sklearn_2 = model_sklearn_iris_2.predict(X_iris_scaled[:, IRIS_FEAT_IDX])
    acc_sklearn_2 = np.mean(y_pred_sklearn_2 == y_iris) * 100
    print(f'Sklearn Iris (2 features) accuracy: {acc_sklearn_2:.2f}%')
    
    # Sklearn Iris - 4 features
    model_sklearn_iris_4 = LogisticRegression(max_iter=1000, solver='lbfgs')
    model_sklearn_iris_4.fit(X_iris_scaled, y_iris)
    W_sklearn_iris_4_full = np.hstack([model_sklearn_iris_4.intercept_.reshape(-1, 1), 
                                        model_sklearn_iris_4.coef_]).T
    W_sklearn_iris_4 = W_sklearn_iris_4_full[[0, 3, 4], :]
    y_pred_sklearn_4 = model_sklearn_iris_4.predict(X_iris_scaled)
    acc_sklearn_4 = np.mean(y_pred_sklearn_4 == y_iris) * 100
    print(f'Sklearn Iris (4 features) accuracy: {acc_sklearn_4:.2f}%')
    
    # ========== WINE DATASET ==========
    wine_data = load_wine()
    X_wine = wine_data.data
    y_wine = wine_data.target
    wine_fnames = wine_data.feature_names
    TARGET_NAMES_MAP_WINE = {i: wine_data.target_names[i] for i in np.unique(y_wine)}
    
    # Scale wine data
    scaler_wine = StandardScaler()
    X_wine_scaled = scaler_wine.fit_transform(X_wine)
    
    # Get wine feature indices
    wine_feat_idx = [wine_fnames.index(name) for name in WINE_FEAT_NAMES]
    
    # Custom Wine - 2 features
    W_custom_wine_2 = mylearn(X_wine_scaled[:, wine_feat_idx], y_wine, 
                              eta=LEARNING_RATE, T=NUM_ITERATIONS)
    y_pred_wine_2 = mypredict(W_custom_wine_2, X_wine_scaled[:, wine_feat_idx])
    acc_wine_2 = np.mean(y_pred_wine_2 == y_wine) * 100
    print(f'Custom Softmax Wine (2 features) accuracy: {acc_wine_2:.2f}%')
    
    # Custom Wine - all features
    W_custom_wine_full = mylearn(X_wine_scaled, y_wine, 
                                 eta=LEARNING_RATE, T=NUM_ITERATIONS)
    W_custom_wine_2_viz = W_custom_wine_full[[0, wine_feat_idx[0]+1, wine_feat_idx[1]+1], :]
    y_pred_wine_full = mypredict(W_custom_wine_full, X_wine_scaled)
    acc_wine_full = np.mean(y_pred_wine_full == y_wine) * 100
    print(f'Custom Softmax Wine (all features) accuracy: {acc_wine_full:.2f}%')
    
    # Sklearn Wine - 2 features
    model_sklearn_wine_2 = LogisticRegression(max_iter=1000, solver='lbfgs')
    model_sklearn_wine_2.fit(X_wine_scaled[:, wine_feat_idx], y_wine)
    W_sklearn_wine_2 = np.hstack([model_sklearn_wine_2.intercept_.reshape(-1, 1), 
                                   model_sklearn_wine_2.coef_]).T
    y_pred_wine_sklearn_2 = model_sklearn_wine_2.predict(X_wine_scaled[:, wine_feat_idx])
    acc_wine_sklearn_2 = np.mean(y_pred_wine_sklearn_2 == y_wine) * 100
    print(f'Sklearn Wine (2 features) accuracy: {acc_wine_sklearn_2:.2f}%')
    
    # Sklearn Wine - all features
    model_sklearn_wine_full = LogisticRegression(max_iter=1000, solver='lbfgs')
    model_sklearn_wine_full.fit(X_wine_scaled, y_wine)
    W_sklearn_wine_full_mat = np.hstack([model_sklearn_wine_full.intercept_.reshape(-1, 1), 
                                          model_sklearn_wine_full.coef_]).T
    W_sklearn_wine_2_viz = W_sklearn_wine_full_mat[[0, wine_feat_idx[0]+1, wine_feat_idx[1]+1], :]
    y_pred_wine_sklearn_full = model_sklearn_wine_full.predict(X_wine_scaled)
    acc_wine_sklearn = np.mean(y_pred_wine_sklearn_full == y_wine) * 100
    print(f'Sklearn Wine (all features) accuracy: {acc_wine_sklearn:.2f}%')
    
    # ========== PLOTTING ==========
    # Get visualization data
    X_iris_viz = X_iris_scaled[:, IRIS_FEAT_IDX]
    X_wine_viz = X_wine_scaled[:, wine_feat_idx]
    
    # Figure 1: Iris (2x2)
    fig_iris, axes_iris = plt.subplots(2, 2, figsize=(12, 8))
    plt.suptitle("Learning results: Iris dataset", fontsize=18)
    
    plot_decision_boundary(axes_iris[0, 0], X_iris_viz[:, 0], X_iris_viz[:, 1], y_iris, W_custom_iris_2,
                          xlabel=fnames_iris[IRIS_FEAT_IDX[0]], ylabel=fnames_iris[IRIS_FEAT_IDX[1]], 
                          title=f'Own model (2 feat) - {acc_custom_2:.1f}%',
                          target_names_map=TARGET_NAMES_MAP_IRIS)
    
    plot_decision_boundary(axes_iris[0, 1], X_iris_viz[:, 0], X_iris_viz[:, 1], y_iris, W_custom_iris_4,
                          xlabel=fnames_iris[IRIS_FEAT_IDX[0]], ylabel=fnames_iris[IRIS_FEAT_IDX[1]], 
                          title=f'Own model (4 feat) - {acc_custom_4:.1f}%',
                          target_names_map=TARGET_NAMES_MAP_IRIS)
    
    plot_decision_boundary(axes_iris[1, 0], X_iris_viz[:, 0], X_iris_viz[:, 1], y_iris, W_sklearn_iris_2,
                          xlabel=fnames_iris[IRIS_FEAT_IDX[0]], ylabel=fnames_iris[IRIS_FEAT_IDX[1]], 
                          title=f'Sklearn model (2 feat) - {acc_sklearn_2:.1f}%',
                          target_names_map=TARGET_NAMES_MAP_IRIS)
    
    plot_decision_boundary(axes_iris[1, 1], X_iris_viz[:, 0], X_iris_viz[:, 1], y_iris, W_sklearn_iris_4,
                          xlabel=fnames_iris[IRIS_FEAT_IDX[0]], ylabel=fnames_iris[IRIS_FEAT_IDX[1]], 
                          title=f'Sklearn model (4 feat) - {acc_sklearn_4:.1f}%',
                          target_names_map=TARGET_NAMES_MAP_IRIS)
    
    plt.tight_layout()
    plt.show()
    
    # Figure 2: Wine (2x2)
    fig_wine, axes_wine = plt.subplots(2, 2, figsize=(12, 8))
    plt.suptitle("Learning results: Wine dataset", fontsize=18)
    
    plot_decision_boundary(axes_wine[0, 0], X_wine_viz[:, 0], X_wine_viz[:, 1], y_wine, W_custom_wine_2,
                          xlabel=WINE_FEAT_NAMES[0] + ' (scaled)', ylabel=WINE_FEAT_NAMES[1] + ' (scaled)', 
                          title=f'Own model (2 features) - {acc_wine_2:.1f}%',
                          target_names_map=TARGET_NAMES_MAP_WINE)
    
    plot_decision_boundary(axes_wine[0, 1], X_wine_viz[:, 0], X_wine_viz[:, 1], y_wine, W_custom_wine_2_viz,
                          xlabel=WINE_FEAT_NAMES[0] + ' (scaled)', ylabel=WINE_FEAT_NAMES[1] + ' (scaled)', 
                          title=f'Own model (all features) - {acc_wine_full:.1f}%',
                          target_names_map=TARGET_NAMES_MAP_WINE)
    
    plot_decision_boundary(axes_wine[1, 0], X_wine_viz[:, 0], X_wine_viz[:, 1], y_wine, W_sklearn_wine_2,
                          xlabel=WINE_FEAT_NAMES[0] + ' (scaled)', ylabel=WINE_FEAT_NAMES[1] + ' (scaled)', 
                          title=f'Sklearn model (2 features) - {acc_wine_sklearn_2:.1f}%',
                          target_names_map=TARGET_NAMES_MAP_WINE)
    
    plot_decision_boundary(axes_wine[1, 1], X_wine_viz[:, 0], X_wine_viz[:, 1], y_wine, W_sklearn_wine_2_viz,
                          xlabel=WINE_FEAT_NAMES[0] + ' (scaled)', ylabel=WINE_FEAT_NAMES[1] + ' (scaled)', 
                          title=f'Sklearn model (all features) - {acc_wine_sklearn:.1f}%',
                          target_names_map=TARGET_NAMES_MAP_WINE)
    
    plt.tight_layout()
    plt.show()
    
    print('\nAll plots displayed!')