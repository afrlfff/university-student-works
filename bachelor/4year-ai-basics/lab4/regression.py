# regression.py
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


def calculate_metrics(y_true, y_pred):
    mse = mean_squared_error(y_true, y_pred)
    return {
        'MSE': mse,
        'RMSE': np.sqrt(mse),
        'MAE': mean_absolute_error(y_true, y_pred),
        'R2': r2_score(y_true, y_pred)
    }


def train_linear_models(X_train, y_train, X_test, scaler=None):
    models = {}
    
    if scaler is not None:
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
    else:
        X_train_scaled = X_train
        X_test_scaled = X_test
    
    models['Linear Regression'] = LinearRegression()
    models['Linear Regression'].fit(X_train_scaled, y_train)
    
    models['Ridge'] = Ridge(alpha=1.0)
    models['Ridge'].fit(X_train_scaled, y_train)
    
    models['Lasso'] = Lasso(alpha=0.1)
    models['Lasso'].fit(X_train_scaled, y_train)
    
    return models, X_train_scaled, X_test_scaled


def train_tree_models(X_train, y_train):
    models = {}
    
    models['Decision Tree'] = DecisionTreeRegressor(random_state=42)
    models['Decision Tree'].fit(X_train, y_train)
    
    models['Random Forest'] = RandomForestRegressor(random_state=42)
    models['Random Forest'].fit(X_train, y_train)
    
    return models


def predict_models(models, X_test, X_test_scaled=None, tree_models=None):
    predictions = {}
    
    for name, model in models.items():
        if name in ['Linear Regression', 'Ridge', 'Lasso']:
            predictions[name] = model.predict(X_test_scaled)
        else:
            predictions[name] = model.predict(X_test)
    
    return predictions


def plot_feature_importance(dt_model, rf_model, feature_names):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    dt_importance = dt_model.feature_importances_
    rf_importance = rf_model.feature_importances_
    
    # индексы сортировки по убыванию
    dt_sorted_idx = np.argsort(dt_importance)[::-1]
    rf_sorted_idx = np.argsort(rf_importance)[::-1]
    # сортируем важности
    dt_importance_sorted = dt_importance[dt_sorted_idx]
    rf_importance_sorted = rf_importance[rf_sorted_idx]
    # отсортированные имена признаков
    dt_feature_names_sorted = np.array(feature_names)[dt_sorted_idx]
    rf_feature_names_sorted = np.array(feature_names)[rf_sorted_idx]
    
    positions = np.arange(len(feature_names))
    
    # decision tree
    axes[0].bar(positions, dt_importance_sorted, color='skyblue')
    axes[0].set_xticks(positions)
    axes[0].set_xticklabels(dt_feature_names_sorted, rotation=45, ha='right')
    axes[0].set_ylabel('Importance')
    axes[0].set_title('Decision Tree - Feature Importance')
    
    # random forest
    axes[1].bar(positions, rf_importance_sorted, color='lightgreen')
    axes[1].set_xticks(positions)
    axes[1].set_xticklabels(rf_feature_names_sorted, rotation=45, ha='right')
    axes[1].set_ylabel('Importance')
    axes[1].set_title('Random Forest - Feature Importance')
    
    fig.tight_layout()
    plt.show()


def plot_predicted_vs_actual(y_test, y_pred, X_test, feature_names, best_feature_idx, model_name):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.scatter(X_test[:, best_feature_idx], y_test, alpha=0.5, label='Actual values', color='blue')
    ax.scatter(X_test[:, best_feature_idx], y_pred, alpha=0.5, label='Predicted values', color='red')
    
    z = np.polyfit(X_test[:, best_feature_idx], y_pred, 1)
    p = np.poly1d(z)
    ax.plot(X_test[:, best_feature_idx], p(X_test[:, best_feature_idx]), 
            "g--", label=f'Trend line (slope: {z[0]:.2f})')
    
    ax.set_xlabel(feature_names[best_feature_idx])
    ax.set_ylabel('Disease progression')
    ax.set_title(f'Target Variable vs {feature_names[best_feature_idx]} with {model_name} Predictions')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.show()


def plot_regularization_effect(X_train, y_train, X_test, y_test, scaler):
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    alphas = np.logspace(-4, 4, 50)
    
    ridge_mse = []
    ridge_r2 = []
    lasso_mse = []
    lasso_r2 = []
    
    for alpha in alphas:
        ridge = Ridge(alpha=alpha)
        ridge.fit(X_train_scaled, y_train)
        y_pred_ridge = ridge.predict(X_test_scaled)
        ridge_mse.append(mean_squared_error(y_test, y_pred_ridge))
        ridge_r2.append(r2_score(y_test, y_pred_ridge))
        
        lasso = Lasso(alpha=alpha, max_iter=10000)
        lasso.fit(X_train_scaled, y_train)
        y_pred_lasso = lasso.predict(X_test_scaled)
        lasso_mse.append(mean_squared_error(y_test, y_pred_lasso))
        lasso_r2.append(r2_score(y_test, y_pred_lasso))
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    axes[0].plot(alphas, ridge_mse, 'b-', label='Ridge', linewidth=2)
    axes[0].plot(alphas, lasso_mse, 'r-', label='Lasso', linewidth=2)
    axes[0].set_xscale('log')
    axes[0].set_xlabel('Alpha (log scale)')
    axes[0].set_ylabel('MSE')
    axes[0].set_title('MSE vs Regularization Strength')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    axes[1].plot(alphas, ridge_r2, 'b-', label='Ridge', linewidth=2)
    axes[1].plot(alphas, lasso_r2, 'r-', label='Lasso', linewidth=2)
    axes[1].set_xscale('log')
    axes[1].set_xlabel('Alpha (log scale)')
    axes[1].set_ylabel('R² Score')
    axes[1].set_title('R² vs Regularization Strength')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()