import numpy as np

# ==============================================================================

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# ==============================================================================

def mylearn(X, y, eta=0.1, T=5000):
    m, n = X.shape
    
    X_bias = np.hstack((np.ones((m, 1)), X))
    theta = np.zeros(n + 1)
    
    for t in range(T):
        # forward pass
        z = np.dot(X_bias, theta)
        h = sigmoid(z)
        
        # gradient
        gradient = np.dot(X_bias.T, (h - y)) / m
        
        # update
        theta -= eta * gradient
        
    return theta

# ==============================================================================

def mypredict(theta, X):
    k, n = X.shape
    
    X_bias = np.hstack((np.ones((k, 1)), X))
    z = np.dot(X_bias, theta)
    
    p = sigmoid(z)
    y_pred = (p > 0.5).astype(int)
    
    return y_pred, p

# ==============================================================================