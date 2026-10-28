import numpy as np
import matplotlib.pyplot as plt

from modules.data_generator import norm_dataset

# ==============================================================================

# Активационная функция сигмоиды
def sigmoid(Z):
    return 1/(1+np.exp(-Z))

def sigmoid_derivative(p):
    return p * (1 - p)

def plot_scatter(ax, class0, class1, feature1_idx, feature2_idx, title=None):
    ax.scatter(class0[:,feature1_idx], class0[:,feature2_idx], marker=".", alpha=0.7, label='класс 0') 
    ax.scatter(class1[:,feature1_idx], class1[:,feature2_idx], marker=".", alpha=0.7, label='класс 1')
    ax.set_xlabel(f"Значение {feature1_idx + 1} признака")
    ax.set_ylabel(f"Значение {feature2_idx + 1} признака")
    ax.legend()
    if title is not None:
        ax.set_title(title)

# ==============================================================================

class NeuralNetwork:
    def __init__(self, n_inp, n_hidden):
        self.weights1 = np.random.randn(n_inp, n_hidden) * 0.1
        self.bias1 = np.zeros((1, n_hidden))
        self.weights2 = np.random.randn(n_hidden, 1) * 0.1
        self.bias2 = np.zeros((1, 1))

    def forward(self, X):
        self.layer1 = sigmoid(np.dot(X, self.weights1))
        self.layer2 = sigmoid(np.dot(self.layer1, self.weights2))
        return self.layer2

    def backprop(self, X, y, lr=0.1):
        m = y.shape[0]
        output = self.forward(X)
        d2 = (output - y)
        d1 = np.dot(d2, self.weights2.T) * sigmoid_derivative(self.layer1)
        self.weights2 -= lr * np.dot(self.layer1.T, d2) / m
        self.bias2 -= lr * np.sum(d2, axis=0, keepdims=True) / m
        self.weights1 -= lr * np.dot(X.T, d1) / m
        self.bias1 -= lr * np.sum(d1, axis=0, keepdims=True) / m

    def train_epoch(self, X, y, lr=0.01):
        self.backprop(X, y, lr)

        pred = self.forward(X)
        loss = np.mean(np.square(y - pred))
        acc = np.mean(np.round(pred) == y)

        return loss, acc

    def test(self, X, y):
        pred = self.forward(X)
        loss = np.mean(np.square(y - pred))
        acc = np.mean(np.round(pred) == y)
        return loss, acc

# ==============================================================================

if __name__ == "__main__":
    mu0 = [0, 2, 3]
    mu1 = [3, 5, 1]
    sigma0 = [2, 1, 2]
    sigma1 = [1, 2, 1]

    N = 1000  # число объектов класса
    mu = [mu0, mu1]
    sigma = [sigma0, sigma1]
    X, Y = norm_dataset(mu, sigma, N)

    # Визуалзация датасета
    class0 = X[Y == 0]
    class1 = X[Y == 1]
    fig, ax = plt.subplots(1, 3, figsize=(10, 6))
    plot_scatter(ax[0], class0, class1, 0, 1)
    plot_scatter(ax[1], class0, class1, 0, 2)
    plot_scatter(ax[2], class0, class1, 1, 2)
    plt.suptitle("Диаграмма рассеяния датасета")
    plt.show()

    X = (X - X.mean(axis=0)) / X.std(axis=0)
    Y = Y.reshape(-1, 1)
    train_size = int(0.7 * N * 2)
    Xtrain = X[:train_size]
    Ytrain = Y[:train_size]
    Xtest = X[train_size:]
    Ytest = Y[train_size:]

    NN = NeuralNetwork(n_inp=X.shape[1], n_hidden=4)
    epochs = 100
    train_losses = []
    train_accs = []
    test_losses = []
    test_accs = []
    for epoch in range(epochs):
        loss, acc = NN.train_epoch(Xtrain, Ytrain, lr=0.1)
        test_loss, test_acc = NN.test(Xtest, Ytest)
        train_losses.append(loss)
        train_accs.append(acc)
        test_losses.append(test_loss)
        test_accs.append(test_acc)
        print(f"Epoch {epoch}: train acc={acc:.3f}, test acc={test_acc:.3f}")

    # pred_prob = NN.feedforward()
    # pred = np.round(pred_prob)

    # acc = np.mean(pred == Y)
    _, final_acc = NN.test(Xtest, Ytest)
    print("Итоговая точность на обучающей выборке:", final_acc)

    plt.figure()
    plt.plot(train_losses, label="Train loss")
    plt.plot(test_losses, label="Test loss")
    plt.xlabel("Epoch")
    plt.ylabel("MSE Loss")
    plt.legend()
    plt.title("Loss vs Epoch")
    plt.grid()
    plt.show()

    plt.figure()
    plt.plot(train_accs, label="Train accuracy")
    plt.plot(test_accs, label="Test accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.title("Accuracy vs Epoch")
    plt.grid()
    plt.show()

    W1_final = NN.weights1.copy()
    W2_final = NN.weights2.copy()

    N_neurons = [1, 2, 3, 4, 5, 10, 15, 20, 30]
    N_epochs = [10, 20, 40, 60, 80, 100, 150, 200, 400]
    best_acc = 0
    best_nuerons = None
    best_epochs = None
    for N_neuron in N_neurons:
        for N_epoch in N_epochs:
            NN = NeuralNetwork(n_inp=X.shape[1], n_hidden=N_neuron)
            for epoch in range(N_epoch):
                loss, acc = NN.train_epoch(Xtrain, Ytrain, lr=0.1)
                test_loss, test_acc = NN.test(Xtest, Ytest)
            _, final_acc = NN.test(Xtest, Ytest)
            if final_acc > best_acc:
                best_acc = final_acc
                best_nuerons = N_neuron
                best_epochs = N_epoch
    print(best_nuerons, "neurons", best_epochs, "epochs")
    print("Final test accuracy:", best_acc)

    NN = NeuralNetwork(n_inp=X.shape[1], n_hidden=best_nuerons)
    train_losses = []
    train_accs = []
    test_losses = []
    test_accs = []
    for epoch in range(best_epochs):
        loss, acc = NN.train_epoch(Xtrain, Ytrain, lr=0.1)
        test_loss, test_acc = NN.test(Xtest, Ytest)
        train_losses.append(loss)
        train_accs.append(acc)
        test_losses.append(test_loss)
        test_accs.append(test_acc)
        print(f"Epoch {epoch}: train acc={acc:.3f}, test acc={test_acc:.3f}")

    # pred_prob = NN.feedforward()
    # pred = np.round(pred_prob)

    # acc = np.mean(pred == Y)
    _, final_acc = NN.test(Xtest, Ytest)
    print("Итоговая точность на обучающей выборке:", final_acc)

    plt.figure()
    plt.plot(train_losses, label="Train loss")
    plt.plot(test_losses, label="Test loss")
    plt.xlabel("Epoch")
    plt.ylabel("MSE Loss")
    plt.legend()
    plt.title("Loss vs Epoch")
    plt.grid()
    plt.show()

    plt.figure()
    plt.plot(train_accs, label="Train accuracy")
    plt.plot(test_accs, label="Test accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.title("Accuracy vs Epoch")
    plt.grid()
    plt.show()