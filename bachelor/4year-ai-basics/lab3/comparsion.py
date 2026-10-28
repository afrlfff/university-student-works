# comparison.py
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix, roc_curve, auc
from sklearn.preprocessing import label_binarize


def train_models(models, X_train, y_train, X_test, y_test, X_train_scaled=None, X_test_scaled=None):
    results = {}
    y_preds = {}
    y_probas = {}
    
    for name, model in models.items():
        if name in ['SVM', 'Logistic Regression']:
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
            y_proba = model.predict_proba(X_test_scaled) if hasattr(model, 'predict_proba') else None
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            y_proba = model.predict_proba(X_test) if hasattr(model, 'predict_proba') else None
        
        y_preds[name] = y_pred
        y_probas[name] = y_proba
        
        results[name] = {
            'Accuracy': accuracy_score(y_test, y_pred),
            'Precision': precision_score(y_test, y_pred, average='micro'),
            'Recall': recall_score(y_test, y_pred, average='micro'),
            'F1-score': f1_score(y_test, y_pred, average='micro')
        }
    
    return results, y_preds, y_probas


def plot_roc_curves(y_test, y_probas):
    y_test_bin = label_binarize(y_test, classes=[0, 1, 2])
    n_classes = y_test_bin.shape[1]
    
    plt.figure(figsize=(10, 8))
    colors = ['blue', 'red', 'green', 'orange', 'purple']
    
    for idx, (name, y_proba) in enumerate(y_probas.items()):
        if y_proba is None:
            continue
        
        fpr = dict()
        tpr = dict()
        roc_auc = dict()
        
        for i in range(n_classes):
            fpr[i], tpr[i], _ = roc_curve(y_test_bin[:, i], y_proba[:, i])
            roc_auc[i] = auc(fpr[i], tpr[i])
        
        all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))
        mean_tpr = np.zeros_like(all_fpr)
        
        for i in range(n_classes):
            mean_tpr += np.interp(all_fpr, fpr[i], tpr[i])
        
        mean_tpr /= n_classes
        mean_auc = auc(all_fpr, mean_tpr)
        
        plt.plot(all_fpr, mean_tpr, color=colors[idx % len(colors)], linewidth=2,
                label=f'{name} (AUC = {mean_auc:.3f})')
    
    plt.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Random baseline')
    plt.xlabel('False Positive Rate', fontsize=12)
    plt.ylabel('True Positive Rate', fontsize=12)
    plt.title('ROC Curves Comparison', fontsize=14)
    plt.legend(loc='lower right')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_confusion_matrices(y_test, y_preds, target_names):
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    colors = ['Blues', 'Reds', 'Greens', 'Oranges', 'Purples']
    
    for idx, (name, y_pred) in enumerate(y_preds.items()):
        cm = confusion_matrix(y_test, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap=colors[idx], 
                   xticklabels=target_names, yticklabels=target_names,
                   ax=axes[idx], cbar_kws={'label': 'Count'})
        axes[idx].set_title(f'{name}', fontsize=12, fontweight='bold')
        axes[idx].set_xlabel('Predicted', fontsize=10)
        axes[idx].set_ylabel('Actual', fontsize=10)
    
    axes[5].axis('off')
    plt.tight_layout()
    plt.show()


def plot_accuracy_bar(results):
    names = list(results.keys())
    accuracies = [results[name]['Accuracy'] for name in names]
    colors = ['blue', 'red', 'green', 'orange', 'purple']
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(names, accuracies, color=colors)
    
    for bar, acc in zip(bars, accuracies):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{acc:.3f}', ha='center', va='bottom', fontsize=11)
    
    plt.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, label='Random baseline')
    plt.ylabel('Accuracy', fontsize=12)
    plt.title('Accuracy Comparison Across Classifiers', fontsize=14)
    plt.ylim(0, 1.05)
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.show()


def create_results_table(results):
    df = pd.DataFrame(results).T
    df = df[['Accuracy', 'Precision', 'Recall', 'F1-score']]
    df.loc['MEAN'] = df.mean()
    return df.round(4)