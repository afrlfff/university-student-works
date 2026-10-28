import numpy as np
import matplotlib.pyplot as plt
from modules.data_generator import norm_dataset, nonlinear_dataset_12

# ==============================================================================

def plot_distribution(class0, class1, file_name=""):
    col = class0.shape[1]
    _, axes = plt.subplots(1, col, figsize=(5 * col, 4))

    for i in range(col):
        axes[i].hist(class0[:, i], bins='auto', alpha=0.7, label='класс 0')
        axes[i].hist(class1[:, i], bins='auto', alpha=0.7, label='класс 1')
        axes[i].set_title(f"Распределение датасета ({i + 1}-й признак)")
        axes[i].set_xlabel("Значение признака")
        axes[i].set_ylabel("Количество объектов")
        axes[i].legend()

    if file_name != "":
        plt.savefig(f'images/lab1/{file_name}.png')
    plt.show()

def plot_scatter(class0, class1, feature1_idx, feature2_idx, file_name=""):
    # построение одной скатеррограммы по выбранным признакам 
    plt.scatter(class0[:,feature1_idx], class0[:,feature2_idx], marker=".", alpha=0.7, label='класс 0') 
    plt.scatter(class1[:,feature1_idx], class1[:,feature2_idx], marker=".", alpha=0.7, label='класс 1')
    plt.title(f"Диаграмма рассеяния двух признаков ({feature1_idx + 1} vs {feature2_idx + 1})")
    plt.xlabel(f"Значение {feature1_idx + 1} признака")
    plt.ylabel(f"Значение {feature2_idx + 1} признака")
    plt.legend()
    if file_name != "":
        plt.savefig(f'images/lab1/{file_name}_{feature1_idx + 1}_{feature2_idx + 1}.png') 
    plt.show()

# ==============================================================================

# общий датасет
N = 1000
mu = [ [0, 2, 3],  [3, 5, 1] ] 
sigma = [ [2, 1, 2], [1, 2, 1] ]
X, Y = norm_dataset(mu, sigma, N)

# разделяем данные на 2 подвыборки 
train_count = round(0.7*N*2) # не забываем округлить до целого 
Xtrain = X[0:train_count] 
Xtest = X[train_count:N*2+1] 
Ytrain = Y[0:train_count] 
Ytest = Y[train_count:N*2+1]

# получаем семплы классов
class0 = X[Y == 0]
class1 = X[Y == 1]

# визуализация
plot_distribution(class0, class1, "hist")
plot_scatter(class0, class1, 0, 2, "scatter")

# персональный датасет
X, Y = nonlinear_dataset_12(N, 0, 0, 20, 20)
class0 = X[Y == 0]
class1 = X[Y == 1]

# визуализация
plot_distribution(class0, class1, "hist_personal")
plot_scatter(class0, class1, 0, 1, "scatter_personal")

# ==============================================================================