import numpy as np

# ==============================================================================

def softmax(logits):
    exp_logits = np.exp(logits - np.max(logits, axis=1, keepdims=True))
    return exp_logits / np.sum(exp_logits, axis=1, keepdims=True)

# ==============================================================================

def mylearn(X, y, eta=0.1, T=1000):
    m, n = X.shape
    K = len(np.unique(y))
    X_bias = np.hstack([np.ones((m, 1)), X])
    W = np.zeros((n + 1, K))
    y_onehot = np.zeros((m, K))
    y_onehot[np.arange(m), y] = 1
    
    for _ in range(T):
        logits = X_bias @ W
        probs = softmax(logits)
        gradient = X_bias.T @ (probs - y_onehot) / m
        W -= eta * gradient
    
    return W

# ==============================================================================

def mypredict(W, X):
    X_bias = np.hstack([np.ones((X.shape[0], 1)), X])
    logits = X_bias @ W
    probs = softmax(logits)
    return np.argmax(probs, axis=1)

# ==============================================================================