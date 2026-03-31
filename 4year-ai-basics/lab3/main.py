# main.py
from comparsion import train_models, plot_roc_curves, plot_confusion_matrices, plot_accuracy_bar, create_results_table
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
import xgboost as xgb

if __name__ == '__main__':
    RANDOM_STATE = 42
    TEST_SIZE = 0.3
    
    data = load_iris()
    X, y = data.data, data.target
    target_names = data.target_names
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    models = {
        'Logistic Regression': LogisticRegression(random_state=RANDOM_STATE, max_iter=1000),
        'SVM': SVC(kernel='linear', random_state=RANDOM_STATE, probability=True),
        'Random Forest': RandomForestClassifier(
            random_state=RANDOM_STATE,
            n_estimators=20,
            max_depth=5,
            min_samples_leaf=5
            ),
        'Naive Bayes': GaussianNB(),
        'XGBoost': xgb.XGBClassifier(random_state=RANDOM_STATE, use_label_encoder=False, 
                                     eval_metric='mlogloss', verbosity=0)
    }
    
    results, y_preds, y_probas = train_models(
        models, X_train, y_train, X_test, y_test, 
        X_train_scaled, X_test_scaled
    )
    
    df_results = create_results_table(results)
    
    print("\n" + "="*70)
    print("SUMMARY TABLE")
    print("="*70)
    print(df_results.to_string())
    print(f"\nBest classifier by Accuracy: {df_results['Accuracy'].idxmax()} ({df_results['Accuracy'].max():.4f})")
    
    plot_roc_curves(y_test, y_probas)
    
    plot_confusion_matrices(y_test, y_preds, target_names)
    
    plot_accuracy_bar(results)