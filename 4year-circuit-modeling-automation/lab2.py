import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
import pandas as pd
from modules.data_generator import norm_dataset, nonlinear_dataset_12

# ==============================================================================

def plot_predicition_hist(prediciton_proba, y_test):
    plt.figure(figsize=(10, 6))
    # Вероятности принадлежности к классу 1 для истинных единиц и истинных нулей
    # Y_test используется как маска
    plt.hist(prediciton_proba[y_test == 1, 1], bins='auto', alpha=0.7, label='Класс 1 (True)')
    plt.hist(prediciton_proba[y_test == 0, 1], bins='auto', alpha=0.7, label='Класс 0 (True)')
    plt.title(f"Результаты классификации")
    plt.xlabel("Вероятность принадлежности к классу 1")
    plt.ylabel("Количество объектов")
    plt.legend()
    plt.grid(axis='y', alpha=0.5)
    plt.show()

def plot_scatter(class0, class1):
    # построение одной скатеррограммы по выбранным признакам 
    plt.scatter(class0[:,0], class0[:,1], marker=".", alpha=0.7, label='класс 0') 
    plt.scatter(class1[:,0], class1[:,1], marker=".", alpha=0.7, label='класс 1')
    plt.title(f"Диаграмма рассеяния двух признаков")
    plt.xlabel(f"Значение 1 признака")
    plt.ylabel(f"Значение 2 признака")
    plt.legend()
    plt.show()

def calculate_metrics(clf, X_train, Y_train, X_test, Y_test, Pred_test):
    acc_train = clf.score(X_train, Y_train) 
    acc_test = clf.score(X_test, Y_test) 
    acc_test_manual = sum(Pred_test==Y_test) / len(Y_test) 

    TP = sum((Pred_test == 1) & (Y_test == 1)) # True Positive
    TN = sum((Pred_test == 0) & (Y_test == 0)) # True Negative
    FP = sum((Pred_test == 1) & (Y_test == 0)) # False Positive
    FN = sum((Pred_test == 0) & (Y_test == 1)) # False Negative

    sensitivity = TP / (TP + FN) if (TP + FN) > 0 else 0 # Чувствительность
    specificity = TN / (TN + FP) if (TN + FP) > 0 else 0 # Специфичность

    return acc_train, acc_test, acc_test_manual, sensitivity, specificity

def split_dataset(X, Y, n_samples):
    train_count = round(0.7*n_samples)
    X_train = X[0:train_count] 
    X_test = X[train_count:n_samples+1] 
    Y_train = Y[0:train_count] 
    Y_test = Y[train_count:n_samples+1]

    return X_train, Y_train, X_test, Y_test

def process(N_var, X_train, X_test, Y_train, Y_test):
    clf = LogisticRegression(random_state=N_var, solver='saga', max_iter=1000)
    clf.fit(X_train, Y_train)

    Pred_test = clf.predict(X_test)
    Pred_test_proba = clf.predict_proba(X_test)

    acc_train, acc_test, acc_test_manual, sensitivity, specificity = calculate_metrics(clf, X_train, Y_train, X_test, Y_test, Pred_test)

    metrics = acc_train, acc_test, acc_test_manual, sensitivity, specificity
    return Pred_test, Pred_test_proba, metrics

def print_accuracies(title, acc_train, acc_test, acc_test_manual, sensitivity, specificity):
    print(f"==================== {title} ====================")
    print(f"Точность (Train): {acc_train:.4f}")
    print(f"Точность (Test, sklearn): {acc_test:.4f}")
    print(f"Точность (Test, вручную): {acc_test_manual:.4f}")
    print(f"\nМетрики качества (Test):")
    print(f"Чувствительность (Sensitivity): {sensitivity:.4f}")
    print(f"Специфичность (Specificity): {specificity:.4f}")
    print("==================================================\n")

# ==============================================================================

N_VAR = 12
N_SAMPLES = 1000

mu1 = [ [0, 2],  [4, 8] ] 
sigma1 = [ [1, 1], [1, 1] ]

mu2 = [ [0, 2],  [3, 5] ] 
sigma2 = [ [2, 2], [2, 2] ]

X, Y = norm_dataset(mu1, sigma1, N_SAMPLES)
X_train1, Y_train1, X_test1, Y_test1 = split_dataset(X, Y, N_SAMPLES * 2)
pred_test1, pred_test_proba1, metrics1 = process(N_VAR, X_train1, X_test1, Y_train1, Y_test1)
acc_train1, acc_test1, acc_test_manual1, sensitivity1, specificity1 = metrics1
class0 = X[Y == 0]
class1 = X[Y == 1]
plot_scatter(class0, class1)

X, Y = norm_dataset(mu2, sigma2, N_SAMPLES)
X_train2, Y_train2, X_test2, Y_test2 = split_dataset(X, Y, N_SAMPLES * 2)
pred_test2, pred_test_proba2, metrics2 = process(N_VAR, X_train2, X_test2, Y_train2, Y_test2)
acc_train2, acc_test2, acc_test_manual2, sensitivity2, specificity2 = metrics2
class0 = X[Y == 0]
class1 = X[Y == 1]
plot_scatter(class0, class1)

X, Y = nonlinear_dataset_12(N_SAMPLES * 2, 0, 0, 20, 20)
X_train3, Y_train3, X_test3, Y_test3 = split_dataset(X, Y, N_SAMPLES)
pred_test3, pred_test_proba3, metrics3 = process(N_VAR, X_train3, X_test3, Y_train3, Y_test3)
acc_train3, acc_test3, acc_test_manual3, sensitivity3, specificity3 = metrics3
class0 = X[Y == 0]
class1 = X[Y == 1]
plot_scatter(class0, class1)

print_accuracies("Test (good)", acc_train1, acc_test1, acc_test_manual1, sensitivity1, specificity1)
print_accuracies("Test (bad)", acc_train2, acc_test2, acc_test_manual2, sensitivity2, specificity2)
print_accuracies("Test (nonlinear)", acc_train3, acc_test3, acc_test_manual3, sensitivity3, specificity3)

plot_predicition_hist(pred_test_proba1, Y_test1)
plot_predicition_hist(pred_test_proba2, Y_test2)
plot_predicition_hist(pred_test_proba3, Y_test3)

results = {
    'Число объектов': [len(Y_train1), len(Y_test1), len(Y_test2), len(Y_test3)],
    'Точность, %': [acc_train1 * 100, acc_test1 * 100, acc_test2 * 100, acc_test3 * 100],
    'Чувствительность, %': ["-", sensitivity1 * 100, sensitivity2 * 100, sensitivity3 * 100],
    'Специфичность, %': ["-", specificity1 * 100, specificity2 * 100, specificity3 * 100]
}

df_results = pd.DataFrame(results, index=['Train', 'Test (good)', 'Test (bad)', "Test (nonlinear)"])
print(df_results)

# ==============================================================================