import numpy as np

def fibsearch(f, interval, tol):
    a, b = interval
    neval = 0
    coords = []
    kmax = 1000

    # find n (number of iterations)
    n = 0
    fibs_arr = [1, 1]
    while not (fibs_arr[-1] > ((b - a) / tol)):
        fibs_arr.append(fibs_arr[-1] + fibs_arr[-2])
        n += 1

    # Initialize starting values
    x1 = a + (fibs_arr[n - 2] / fibs_arr[n]) * (b - a)
    x2 = a + (fibs_arr[n - 1] / fibs_arr[n]) * (b - a)
    f1, f2 = f(x1), f(x2); neval += 2
    coords.append(x1); coords.append(x2)

    # Fibonacci search
    for k in range(n):
        if f1 < f2:
            b = x2
            x2 = x1
            f2 = f1
            x1 = a + (fibs_arr[n - k - 2] / fibs_arr[n - k]) * (b - a)
            f1 = f(x1)
            coords.append(x1)
        else:
            a = x1
            x1 = x2
            f1 = f2
            x2 = a + (fibs_arr[n - k - 1] / fibs_arr[n - k]) * (b - a)
            f2 = f(x2)
            coords.append(x2)

        
        neval += 1
        if (k + 1) == kmax: break
        
    
    xmin = (a + b) / 2
    fmin = f(xmin); neval += 1

    return xmin, fmin, neval, coords