import numpy as np

# ==============================================================================

def norm_dataset(mu, sigma, N):
    # векторы мат ожиданий
    mu0 = mu[0]
    mu1 = mu[1]
    # векторы среднеквадратических отклонений
    sigma0 = sigma[0]
    sigma1 = sigma[1]

    col = len(mu0)  # количество столбцов-признаков
    
    # инициализируем первый столбец
    class0 = np.random.normal(mu0[0],sigma0[0],[N,1])
    class1 = np.random.normal(mu1[0],sigma1[0],[N,1]) 
    # инициализируем оставишеся столбцы
    for i in range(1, col):
        v0 = np.random.normal(mu0[i],sigma0[i],[N,1]) 
        class0 = np.hstack((class0,v0)) 
        v1 = np.random.normal(mu1[i],sigma1[i],[N,1]) 
        class1 = np.hstack((class1,v1))

    # инициализруем матрицу признаков и вектор меток
    Y1 = np.ones((N, 1), dtype=bool)
    Y0 = np.zeros((N, 1), dtype=bool)
    X = np.vstack((class0,class1)) 
    Y = np.vstack((Y0,Y1)).ravel()

    # перемешиваем данные 
    rng = np.random.default_rng() 
    arr = np.arange(2*N) #индексы для перемешивания 
    rng.shuffle(arr)
    X = X[arr] 
    Y = Y[arr]

    return X, Y

# ==============================================================================

def nonlinear_dataset_12(N, xmin, ymin, xmax, ymax, circle_on_top=False):
    w = abs(xmax - xmin)
    h = abs(ymax - ymin)

    N_curve         = int(0.7 * N)
    N_circle        = N - N_curve

    # радиус круга
    R = min(np.abs(xmax - xmin) / 6, np.abs(ymax - ymin) / 6)
    circle_center = (xmin + w / 2, (ymax - R) if (circle_on_top) else (ymin + R))
    curve_center_x = xmin + w / 2

    # галочка
    curve_x = np.random.uniform(xmin, xmax, N_curve)
    curve_y = -np.abs(curve_x - curve_center_x) * (2*h / w) + ymax

    # круг
    circle_x = np.random.normal(circle_center[0], R/2, N_circle)
    circle_y = np.random.normal(circle_center[1], R/2, N_circle)

    # сохраняем в классы и добавляем шум
    class0 = np.hstack((curve_x.reshape(-1, 1), curve_y.reshape(-1, 1)))
    class1 = np.hstack((circle_x.reshape(-1, 1), circle_y.reshape(-1, 1)))
    class0 = class0 + np.random.normal(0, 0.05 * w, class0.shape)

    # метки классов
    Y0 = np.zeros(N_curve, dtype=bool)
    Y1 = np.ones(N_circle, dtype=bool)
    
    # объединение данных
    X = np.vstack((class0, class1))  # семплы (N, 2)
    Y = np.hstack((Y0, Y1))          # метки (N,)
    
    # перемешивание
    rng = np.random.default_rng()
    arr = np.arange(N)
    rng.shuffle(arr)
    X = X[arr]
    Y = Y[arr]
    
    return X, Y

# ==============================================================================