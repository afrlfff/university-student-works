import numpy as np

def goldensectionsearch(f, interval, tol):
    a = interval[0]
    b = interval[1]
    phi = (1 + np.sqrt(5)) / 2
    L = b - a
    x1 = b - L / phi
    x2 = a + L / phi
    f1 = f(x1) 
    f2 = f(x2)
    neval = 2

    while (L > tol):
        if f1 < f2:
            b = x2
            L = b - a
            x2 = x1
            x1 = b - L / phi
            f2 = f1
            f1 = f(x1); neval += 1
        else:
            a = x1  
            L = b - a
            x1 = x2
            x2 = a + L / phi  
            f1 = f2
            f2 = f(x2); neval += 1

    xmin = x1
    fmin = f1

    answer_ = [xmin, fmin, neval]
    return answer_


def bbsearch(f, df, x0, tol):
    neval = 0
    coords = [x0]
    k = 0; kmax = 1000

    # initialization
    x = x0
    D = 0.1 # stabilization parameter
    g = df(x); neval += 1

    # find alpha using golden section search
    alpha, _, neval_ = goldensectionsearch(lambda al : f(x0 - al * g), [0, 1], tol)
    neval += neval_

    # Barzilai-Borwein seacrh
    while True:
        # update x and g
        x_prev = x
        g_prev = g
        x = x_prev - alpha * g_prev
        g = df(x); neval += 1
        
        # update deltas
        deltaX = x - x_prev
        deltaGrad = g - g_prev
        
        # update alpha using formula (1)
        alpha = np.dot(np.transpose(deltaX), deltaX) / np.dot(np.transpose(deltaX), deltaGrad)
        alpha_stab = D / np.linalg.norm(g)
        alpha = min(alpha, alpha_stab)

        # update logs
        coords.append(x)
        k += 1

        # end of search
        if not ((np.linalg.norm(deltaX) >= tol) and (k < kmax)):
            break
        

    xmin = x
    fmin = f(x); neval += 1

    return xmin, fmin, neval, coords