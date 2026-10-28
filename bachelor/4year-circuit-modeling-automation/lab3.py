import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, auc, confusion_matrix, roc_auc_score
from modules.data_generator import norm_dataset, nonlinear_dataset_12

# ==============================================================================

def plot_predicition_hist(ax, prediciton_proba, y_test, title=None):
    ax.hist(prediciton_proba[y_test == 1, 1], bins='auto', alpha=0.7, label='Класс 1 (True)')
    ax.hist(prediciton_proba[y_test == 0, 1], bins='auto', alpha=0.7, label='Класс 0 (False)')
    ax.set_xlabel("Вероятность принадлежности к классу 1")
    ax.set_ylabel("Количество объектов")
    ax.legend()
    ax.grid(axis='y', alpha=0.5)
    if title is not None:
        ax.set_title(title)

def plot_scatter(ax, class0, class1, title=None):
    ax.scatter(class0[:,0], class0[:,1], marker=".", alpha=0.7, label='класс 0') 
    ax.scatter(class1[:,0], class1[:,1], marker=".", alpha=0.7, label='класс 1')
    ax.set_xlabel(f"Значение 1 признака")
    ax.set_ylabel(f"Значение 2 признака")
    ax.legend()
    if title is not None:
        ax.set_title(title)

def calculate_metrics(clf, X, Y, pred):
    accuracy = clf.score(X, Y)
    accuracy_manual = sum(pred==Y) / len(Y) 

    TP = sum((pred == 1) & (Y == 1)) # True Positive
    TN = sum((pred == 0) & (Y == 0)) # True Negative
    FP = sum((pred == 1) & (Y == 0)) # False Positive
    FN = sum((pred == 0) & (Y == 1)) # False Negative

    sensitivity = TP / (TP + FN) if (TP + FN) > 0 else 0 # Чувствительность
    specificity = TN / (TN + FP) if (TN + FP) > 0 else 0 # Специфичность

    return accuracy, accuracy_manual, sensitivity, specificity

def split_dataset(X, Y, n_samples):
    train_count = round(0.7*n_samples)
    X_train = X[0:train_count] 
    X_test = X[train_count:n_samples+1] 
    Y_train = Y[0:train_count] 
    Y_test = Y[train_count:n_samples+1]

    return X_train, Y_train, X_test, Y_test

def process(clf, X_train, X_test, Y_train, Y_test):
    clf.fit(X_train, Y_train)

    pred_train = clf.predict(X_train)
    pred_test = clf.predict(X_test)
    pred_train_proba = clf.predict_proba(X_train)
    pred_test_proba = clf.predict_proba(X_test)

    acc_train, acc_train_manual, sensitivity_train, specificity_train = calculate_metrics(clf, X_train, Y_train, pred_train)
    acc_test, acc_test_manual, sensitivity_test, specificity_test = calculate_metrics(clf, X_test, Y_test, pred_test)

    metrics_train = acc_train, acc_train_manual, sensitivity_train, specificity_train
    metrics_test = acc_test, acc_test_manual, sensitivity_test, specificity_test

    return pred_train, pred_test, pred_train_proba, pred_test_proba, metrics_train, metrics_test

def get_metrics_table(name, n_samples, accuracy, sensitivity, specificity):
    results = {
        'Число объектов': [n_samples],
        'Точность, %': [accuracy * 100],
        'Чувствительность, %': [sensitivity * 100],
        'Специфичность, %': [specificity * 100]
    }
    
    df_results = pd.DataFrame(results, index=[name])
    return df_results

def plot_roc(ax, Y_test, pred_proba, title=None):
    fpr, tpr, _ = roc_curve(Y_test, pred_proba[:, 1])
    roc_auc = auc(fpr, tpr)
    ax.plot(fpr, tpr, label=f'ROC (AUC = {roc_auc:.3f})', linestyle='solid')
    ax.plot([0, 1], [0, 1], 'k--', label='Random Guess')
    if title is not None:
        ax.set_title(title)
    ax.set_xlabel("FPR")
    ax.set_ylabel("TPR")
    ax.legend()

# ==============================================================================

N_VAR = 12
N_SAMPLES = 1000

# ==============================================================================

if __name__ == "__main__":
    # хорошая линейная разделимость
    mu1 = [ [0, 2],  [4, 8] ] 
    sigma1 = [ [1, 1], [1, 1] ]

    # плохая линейная разделимость
    mu2 = [ [0, 2],  [3, 5] ] 
    sigma2 = [ [2, 2], [2, 2] ]

    # генерация датасетов
    X, Y = norm_dataset(mu1, sigma1, N_SAMPLES)
    X_train1, Y_train1, X_test1, Y_test1 = split_dataset(X, Y, N_SAMPLES * 2)
    class01 = X[Y == 0]
    class11 = X[Y == 1]

    X, Y = norm_dataset(mu2, sigma2, N_SAMPLES)
    X_train2, Y_train2, X_test2, Y_test2 = split_dataset(X, Y, N_SAMPLES * 2)
    class02 = X[Y == 0]
    class12 = X[Y == 1]
    
    X, Y = nonlinear_dataset_12(N_SAMPLES * 2, 0, 0, 20, 20, circle_on_top=False)
    X_train3, Y_train3, X_test3, Y_test3 = split_dataset(X, Y, N_SAMPLES * 2)
    class03 = X[Y == 0]
    class13 = X[Y == 1]
    
    X, Y = nonlinear_dataset_12(N_SAMPLES * 2, 0, 0, 20, 20, circle_on_top=True)
    X_train4, Y_train4, X_test4, Y_test4 = split_dataset(X, Y, N_SAMPLES * 2)
    class04 = X[Y == 0]
    class14 = X[Y == 1]
    
    # визуализация датасетов
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    plot_scatter(axes[0][0], class01, class11, title="1. good")
    plot_scatter(axes[0][1], class02, class12, title="2. bad")
    plot_scatter(axes[1][0], class03, class13, title="3. nonlinear")
    plot_scatter(axes[1][1], class04, class14, title="4. nonlinear-intersect")
    plt.suptitle("Диаграммы рассеяния сгенерированных датасетов", fontsize=16)
    plt.tight_layout()
    plt.show()

    # 1. наивное дерево решений (максимальная глубина)
    clf = DecisionTreeClassifier(random_state=N_VAR, max_depth=5)

    # получение предсказаний
    pred_train1, pred_test1, pred_train_proba1, pred_test_proba1, metrics_train, metrics_test = process(clf, X_train1, X_test1, Y_train1, Y_test1)
    acc_train1, acc_train_manual1, sensitivity_train1, specificity_train1 = metrics_train
    acc_test1, acc_test_manual1, sensitivity_test1, specificity_test1 = metrics_test

    pred_train2, pred_test2, pred_train_proba2, pred_test_proba2, metrics_train, metrics_test = process(clf, X_train2, X_test2, Y_train2, Y_test2)
    acc_train2, acc_train_manual2, sensitivity_train2, specificity_train2 = metrics_train
    acc_test2, acc_test_manual2, sensitivity_test2, specificity_test2 = metrics_test
    
    pred_train3, pred_test3, pred_train_proba3, pred_test_proba3, metrics_train, metrics_test = process(clf, X_train3, X_test3, Y_train3, Y_test3)
    acc_train3, acc_train_manual3, sensitivity_train3, specificity_train3 = metrics_train
    acc_test3, acc_test_manual3, sensitivity_test3, specificity_test3 = metrics_test

    pred_train4, pred_test4, pred_train_proba4, pred_test_proba4, metrics_train, metrics_test = process(clf, X_train4, X_test4, Y_train4, Y_test4)
    acc_train4, acc_train_manual4, sensitivity_train4, specificity_train4 = metrics_train
    acc_test4, acc_test_manual4, sensitivity_test4, specificity_test4 = metrics_test
    
    # визуализация результатов предсказаний (гистограммы вероятностей распределений между классами)
    fig, axes = plt.subplots(4, 2, figsize=(12, 8))
    plot_predicition_hist(axes[0][0], pred_train_proba1, Y_train1, title="1. Train (good)")
    plot_predicition_hist(axes[0][1], pred_test_proba1, Y_test1, title="1. Test (good)")
    plot_predicition_hist(axes[1][0], pred_train_proba2, Y_train2, title="2. Train (bad)")
    plot_predicition_hist(axes[1][1], pred_test_proba2, Y_test2, title="2. Test (bad)")
    plot_predicition_hist(axes[2][0], pred_train_proba3, Y_train3, title="3. Train (nonlinear)")
    plot_predicition_hist(axes[2][1], pred_test_proba3, Y_test3, title="3. Test (nonlinear)")
    plot_predicition_hist(axes[3][0], pred_train_proba4, Y_train4, title="4. Train (nonlinear-intersect)")
    plot_predicition_hist(axes[3][1], pred_test_proba4, Y_test4, title="4. Test (nonlinear-intersect)")
    plt.suptitle("Decision Tree. Результаты классификации", fontsize=16)
    plt.tight_layout()
    plt.show()

    # визуалзация ROC
    fig, axes = plt.subplots(4, 2, figsize=(12, 8))
    plot_roc(axes[0][0], Y_train1, pred_train_proba1, "1. Train (good)")
    plot_roc(axes[0][1], Y_test1, pred_test_proba1, "1. Test (good)")
    plot_roc(axes[1][0], Y_train2, pred_train_proba2, "2. Train (bad)")
    plot_roc(axes[1][1], Y_test2,  pred_test_proba2, "2. Test (bad)")
    plot_roc(axes[2][0], Y_train3, pred_train_proba3, "3. Train (nonlinear)")
    plot_roc(axes[2][1], Y_test3, pred_test_proba3, "3. Test (nonlinear)")
    plot_roc(axes[3][0], Y_train4, pred_train_proba4, "4. Train (nonlinear-intersect)")
    plot_roc(axes[3][1], Y_test4, pred_test_proba4, "4. Test (nonlinear-intersect)")
    plt.suptitle("Decision Tree. ROC", fontsize=16)
    plt.tight_layout()
    plt.show()
    
    # генерация таблицы результатов
    df_results_train_good                   = get_metrics_table("Train (good)", len(Y_train1), acc_train1, sensitivity_train1, specificity_train1)
    df_results_train_bad                    = get_metrics_table("Train (bad)", len(Y_train2), acc_train2, sensitivity_train2, specificity_train2)
    df_results_train_nonlinear              = get_metrics_table("Train (nonlinear)", len(Y_train3), acc_train3, sensitivity_train3, specificity_train3)
    df_results_train_nonlinear_intersect    = get_metrics_table("Train (nonlinear-intersect)", len(Y_train4), acc_train4, sensitivity_train4, specificity_train4)
    df_results_test_good                    = get_metrics_table("Test (good)", len(Y_test1), acc_test1, sensitivity_test1, specificity_test1)
    df_results_test_bad                     = get_metrics_table("Test (bad)", len(Y_test2), acc_test2, sensitivity_test2, specificity_test2)
    df_results_test_nonlinear               = get_metrics_table("Test (nonlinear)", len(Y_test3), acc_test3, sensitivity_test3, specificity_test3)
    df_results_test_nonlinear_intersect     = get_metrics_table("Test (nonlinear-intersect)", len(Y_test4), acc_test4, sensitivity_test4, specificity_test4)
    df_results = pd.concat([
        df_results_train_good, df_results_train_bad, df_results_train_nonlinear, df_results_train_nonlinear_intersect, 
        df_results_test_good, df_results_test_bad, df_results_test_nonlinear, df_results_test_nonlinear_intersect
    ], axis=0, ignore_index=False)
    print(df_results)

    # 2. Случайный лес
    clf = RandomForestClassifier(random_state=N_VAR, n_estimators=100)

    # получение предсказаний
    pred_train1, pred_test1, pred_train_proba1, pred_test_proba1, metrics_train, metrics_test = process(clf, X_train1, X_test1, Y_train1, Y_test1)
    acc_train1, acc_train_manual1, sensitivity_train1, specificity_train1 = metrics_train
    acc_test1, acc_test_manual1, sensitivity_test1, specificity_test1 = metrics_test

    pred_train2, pred_test2, pred_train_proba2, pred_test_proba2, metrics_train, metrics_test = process(clf, X_train2, X_test2, Y_train2, Y_test2)
    acc_train2, acc_train_manual2, sensitivity_train2, specificity_train2 = metrics_train
    acc_test2, acc_test_manual2, sensitivity_test2, specificity_test2 = metrics_test
    
    pred_train3, pred_test3, pred_train_proba3, pred_test_proba3, metrics_train, metrics_test = process(clf, X_train3, X_test3, Y_train3, Y_test3)
    acc_train3, acc_train_manual3, sensitivity_train3, specificity_train3 = metrics_train
    acc_test3, acc_test_manual3, sensitivity_test3, specificity_test3 = metrics_test

    pred_train4, pred_test4, pred_train_proba4, pred_test_proba4, metrics_train, metrics_test = process(clf, X_train4, X_test4, Y_train4, Y_test4)
    acc_train4, acc_train_manual4, sensitivity_train4, specificity_train4 = metrics_train
    acc_test4, acc_test_manual4, sensitivity_test4, specificity_test4 = metrics_test
    
    # визуализация результатов предсказаний (гистограммы вероятностей распределений между классами)
    fig, axes = plt.subplots(4, 2, figsize=(12, 8))
    plot_predicition_hist(axes[0][0], pred_train_proba1, Y_train1, title="1. Train (good)")
    plot_predicition_hist(axes[0][1], pred_test_proba1, Y_test1, title="1. Test (good)")
    plot_predicition_hist(axes[1][0], pred_train_proba2, Y_train2, title="2. Train (bad)")
    plot_predicition_hist(axes[1][1], pred_test_proba2, Y_test2, title="2. Test (bad)")
    plot_predicition_hist(axes[2][0], pred_train_proba3, Y_train3, title="3. Train (nonlinear)")
    plot_predicition_hist(axes[2][1], pred_test_proba3, Y_test3, title="3. Test (nonlinear)")
    plot_predicition_hist(axes[3][0], pred_train_proba4, Y_train4, title="4. Train (nonlinear-intersect)")
    plot_predicition_hist(axes[3][1], pred_test_proba4, Y_test4, title="4. Test (nonlinear-intersect)")
    plt.suptitle("Random Forest. Результаты классификации", fontsize=16)
    plt.tight_layout()
    plt.show()

    # визуалзация ROC
    fig, axes = plt.subplots(4, 2, figsize=(12, 8))
    plot_roc(axes[0][0], Y_train1, pred_train_proba1, "1. Train (good)")
    plot_roc(axes[0][1], Y_test1, pred_test_proba1, "1. Test (good)")
    plot_roc(axes[1][0], Y_train2, pred_train_proba2, "2. Train (bad)")
    plot_roc(axes[1][1], Y_test2,  pred_test_proba2, "2. Test (bad)")
    plot_roc(axes[2][0], Y_train3, pred_train_proba3, "3. Train (nonlinear)")
    plot_roc(axes[2][1], Y_test3, pred_test_proba3, "3. Test (nonlinear)")
    plot_roc(axes[3][0], Y_train4, pred_train_proba4, "4. Train (nonlinear-intersect)")
    plot_roc(axes[3][1], Y_test4, pred_test_proba4, "4. Test (nonlinear-intersect)")
    plt.suptitle("Random Forest. ROC", fontsize=16)
    plt.tight_layout()
    plt.show()
    
    # генерация таблицы результатов
    df_results_train_good                   = get_metrics_table("Train (good)", len(Y_train1), acc_train1, sensitivity_train1, specificity_train1)
    df_results_train_bad                    = get_metrics_table("Train (bad)", len(Y_train2), acc_train2, sensitivity_train2, specificity_train2)
    df_results_train_nonlinear              = get_metrics_table("Train (nonlinear)", len(Y_train3), acc_train3, sensitivity_train3, specificity_train3)
    df_results_train_nonlinear_intersect    = get_metrics_table("Train (nonlinear-intersect)", len(Y_train4), acc_train4, sensitivity_train4, specificity_train4)
    df_results_test_good                    = get_metrics_table("Test (good)", len(Y_test1), acc_test1, sensitivity_test1, specificity_test1)
    df_results_test_bad                     = get_metrics_table("Test (bad)", len(Y_test2), acc_test2, sensitivity_test2, specificity_test2)
    df_results_test_nonlinear               = get_metrics_table("Test (nonlinear)", len(Y_test3), acc_test3, sensitivity_test3, specificity_test3)
    df_results_test_nonlinear_intersect     = get_metrics_table("Test (nonlinear-intersect)", len(Y_test4), acc_test4, sensitivity_test4, specificity_test4)
    df_results = pd.concat([
        df_results_train_good, df_results_train_bad, df_results_train_nonlinear, df_results_train_nonlinear_intersect, 
        df_results_test_good, df_results_test_bad, df_results_test_nonlinear, df_results_test_nonlinear_intersect
    ], axis=0, ignore_index=False)
    print(df_results)