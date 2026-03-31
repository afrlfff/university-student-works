import numpy as np
import matplotlib.pyplot as plt
from itertools import permutations
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from mylogclass import mylearn, mypredict

# ==============================================================================

def plot_decision_boundary(ax, x1, x2, y, theta, xlabel=None, ylabel=None, title=None, target_names_map=None):
    colors = ['blue', 'green', 'red', 'purple', 'orange']
    unique_classes = np.unique(y)

    # Plot data points
    for i, target in enumerate(unique_classes):
        label = (target_names_map[target]) if (target_names_map is not None) else (f'class "{target}"')
        ax.scatter(x1[y == target], x2[y == target], c=colors[i], label=label)
    
    # Plot decision boundary: theta[0] + theta[1]*x1 + theta[2]*x2 = 0
    x1_vals = np.array([x1.min(), x1.max()])
    t0 = theta[0]
    t1 = theta[1]
    t2 = theta[2]
    x2_vals = -(t0 + t1 * x1_vals) / t2
    ax.plot(x1_vals, x2_vals, 'k-')

    # Set plot labels, title and enable grid
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    if title is not None:
        ax.set_title(title)
    ax.legend()
    ax.grid(True, linestyle='--')

# ==============================================================================

def plot_scatter(ax, x1, x2, y, xlabel=None, ylabel=None, title=None, target_names_map=None):
    colors = ['blue', 'green', 'red', 'purple', 'orange']
    unique_classes = np.unique(y)

    # Plot data points
    for i, target in enumerate(unique_classes):
        label = (target_names_map[target]) if (target_names_map is not None) else (f'class "{target}"')
        ax.scatter(x1[y == target], x2[y == target], c=colors[i], label=label)
    
    # Set plot labels, title and enable grid
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    if title is not None:
        ax.set_title(title)
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.3)

# ==============================================================================

def get_scikit_model_theta(model):
    return np.hstack([model.intercept_.flatten(), model.coef_.flatten()])

# ==============================================================================

if __name__ == '__main__':
    # load data
    data = load_iris()
    X = data.data
    y = data.target

    # constants
    TARGET_CLASS_IDX = 2 # viriginica
    FEATURE_1_IDX = 2
    FEATURE_2_IDX = 3
    TARGET_NAMES_MAP = {i: data.target_names[i] for i in np.unique(y)}

    # get target binary (viriginica)
    y_binary = (y == TARGET_CLASS_IDX).astype(int)
    y_binary_target_names = [
        f"{data.target_names[TARGET_CLASS_IDX]}" if (i == TARGET_CLASS_IDX) else (f"Not {data.target_names[TARGET_CLASS_IDX]}")
                             for i in sorted(np.unique(y))]
    

    # Visualize dataset
    fig, axes = plt.subplots(4, 3, figsize=(12, 8))
    colors = ['blue', 'green', 'red']
    feature_pairs = list(permutations(range(4), 2))[:12]
    for ax, (i, j) in zip(axes.flatten(), feature_pairs):
        plot_scatter(ax, X[:, i], X[:, j], y,
                     xlabel=data.feature_names[i], ylabel=data.feature_names[j], 
                     target_names_map=TARGET_NAMES_MAP)
    plt.suptitle('Диаграммы рассеяния - Ирисы Фишера', fontsize=14)
    plt.tight_layout()
    plt.show()

    # Visualize only necessary
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    colors = ['blue', 'green', 'red']
    plot_scatter(axes[0], X[:, FEATURE_1_IDX], X[:, FEATURE_2_IDX], y, 
                 xlabel=data.feature_names[FEATURE_1_IDX], ylabel=data.feature_names[FEATURE_2_IDX], 
                 target_names_map=TARGET_NAMES_MAP)
    plot_scatter(axes[1], X[:, FEATURE_2_IDX], X[:, FEATURE_1_IDX], y, 
                 xlabel=data.feature_names[FEATURE_2_IDX], ylabel=data.feature_names[FEATURE_1_IDX], 
                 target_names_map=TARGET_NAMES_MAP)
    plt.suptitle('Диаграмма рассеяния исследуемых признаков', fontsize=14)
    plt.tight_layout()
    plt.show()
    
    # scale for gradient descent
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # get features
    target_feature_idxs = [FEATURE_1_IDX, FEATURE_2_IDX]
    X_2feat = X_scaled[:, target_feature_idxs]
    X_4feat = X_scaled
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # 1: Custom implementation (2 features)
    print("Обучение своей модели (2 признака)...")
    theta_2 = mylearn(X_2feat, y_binary, eta=0.5, T=3000) # Eta увеличен для scaled данных
    plot_decision_boundary(axes[0, 0], X_scaled[:, FEATURE_1_IDX], X_scaled[:, FEATURE_2_IDX], y, theta_2, 
                           target_names_map=TARGET_NAMES_MAP,
                           xlabel=data.feature_names[FEATURE_1_IDX], ylabel=data.feature_names[FEATURE_2_IDX], title="Own Model (2 Features)")
    
    # 2: Custom implementation (4 features)
    print("Обучение своей модели (4 признака)...")
    theta_4 = mylearn(X_4feat, y_binary, eta=0.5, T=3000)
    theta_2dim = [theta_4[0], theta_4[1 + FEATURE_1_IDX], theta_4[1 + FEATURE_2_IDX]]
    plot_decision_boundary(axes[0, 1], X_scaled[:, FEATURE_1_IDX], X_scaled[:, FEATURE_2_IDX], y, theta_2dim, 
                           target_names_map=TARGET_NAMES_MAP,
                           xlabel=data.feature_names[FEATURE_1_IDX], ylabel=data.feature_names[FEATURE_2_IDX], title="Own Model (4 Features)")
    
    # 3: Scikit-learn (2 features)
    print("Обучение sklearn модели (2 признака)...")
    model_sk_2 = LogisticRegression(solver='lbfgs', max_iter=1000)
    model_sk_2.fit(X_2feat, y_binary)
    theta_sk_2 = get_scikit_model_theta(model_sk_2)
    plot_decision_boundary(axes[1, 0], X_scaled[:, FEATURE_1_IDX], X_scaled[:, FEATURE_2_IDX], y, theta_sk_2, 
                           target_names_map=TARGET_NAMES_MAP,
                           xlabel=data.feature_names[FEATURE_1_IDX], ylabel=data.feature_names[FEATURE_2_IDX], title="Sklearn Model (2 Features)")
    
    # 4: Scikit-learn (4 features)
    print("Обучение sklearn модели (4 признака)...")
    model_sk_4 = LogisticRegression(solver='lbfgs', max_iter=1000)
    model_sk_4.fit(X_4feat, y_binary)
    theta_sk_4 = get_scikit_model_theta(model_sk_4)
    theta_2dim = [theta_sk_4[0], theta_sk_4[1 + FEATURE_1_IDX], theta_sk_4[1 + FEATURE_2_IDX]]
    plot_decision_boundary(axes[1, 1], X_scaled[:, FEATURE_1_IDX], X_scaled[:, FEATURE_2_IDX], y, theta_2dim, 
                           target_names_map=TARGET_NAMES_MAP,
                           xlabel=data.feature_names[FEATURE_1_IDX], ylabel=data.feature_names[FEATURE_2_IDX], title="Sklearn Model (4 Features)")
    
    plt.suptitle('Learning results', fontsize=14)
    plt.tight_layout()
    plt.show()

    # Accuracy comparison
    ypred_own_2, _ = mypredict(theta_2, X_2feat)
    acc_own_2 = np.mean(ypred_own_2 == y_binary)
    acc_sk_2 = model_sk_2.score(X_2feat, y_binary)

    ypred_own_4, _ = mypredict(theta_4, X_4feat)
    acc_own_4 = np.mean(ypred_own_4 == y_binary)
    acc_sk_4 = model_sk_4.score(X_4feat, y_binary)
    
    print(f"\nТочность своей модели (2 признака): {acc_own_2:.4f}")
    print(f"Точность sklearn (2 признака): {acc_sk_2:.4f}")

    print(f"\nТочность своей модели (4 признака): {acc_own_4:.4f}")
    print(f"Точность sklearn (4 признака): {acc_sk_4:.4f}")