# main.py
import numpy as np
import pandas as pd
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from regression import (
    calculate_metrics, train_linear_models, train_tree_models,
    predict_models, plot_feature_importance, plot_predicted_vs_actual,
    plot_regularization_effect
)


if __name__ == '__main__':
    TEST_SIZE = 0.2
    RANDOM_STATE = 42
    
    data = load_diabetes()
    X = data.data
    y = data.target
    feature_names = data.feature_names
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )
    
    scaler = StandardScaler()
    
    linear_models, X_train_scaled, X_test_scaled = train_linear_models(
        X_train, y_train, X_test, scaler
    )
    
    tree_models = train_tree_models(X_train, y_train)
    
    all_models = {**linear_models, **tree_models}
    
    predictions = predict_models(
        linear_models, X_test, X_test_scaled, tree_models
    )
    
    for name, model in tree_models.items():
        predictions[name] = model.predict(X_test)
    
    results = {}
    for name, model in all_models.items():
        y_pred = predictions[name]
        metrics = calculate_metrics(y_test, y_pred)
        results[name] = metrics
        print(f"\n{name}:")
        print(f"  MSE:  {metrics['MSE']:.4f}")
        print(f"  RMSE: {metrics['RMSE']:.4f}")
        print(f"  MAE:  {metrics['MAE']:.4f}")
        print(f"  R²:   {metrics['R2']:.4f}")
    
    df = pd.DataFrame(results).T.round(4)
    print("\n" + "="*60)
    print("SUMMARY TABLE")
    print("="*60)
    print(df.to_string())
    
    best_model_name = max(results.items(), key=lambda x: x[1]['R2'])[0]
    best_model = all_models[best_model_name]
    best_predictions = predictions[best_model_name]
    print(f"Best model: {best_model_name}")
    
    # Определение лучшего признака по лучшей модели (в даннном случае это Lasso)
    # if best_model_name in ['Decision Tree', 'Random Forest']:
    #     importances = best_model.feature_importances_
    # else:
    #     importances = np.abs(best_model.coef_)
    # best_feature_idx = np.argmax(importances)

    # Определение лучшего признака по древовидным моделям (в соответствии с МУ)
    best_feature_idx = np.argmax(tree_models['Random Forest'].feature_importances_)
    
    plot_feature_importance(
        tree_models['Decision Tree'],
        tree_models['Random Forest'],
        feature_names
    )
    
    plot_predicted_vs_actual(
        y_test, best_predictions, X_test,
        feature_names, best_feature_idx, best_model_name
    )
    
    plot_regularization_effect(X_train, y_train, X_test, y_test, scaler)