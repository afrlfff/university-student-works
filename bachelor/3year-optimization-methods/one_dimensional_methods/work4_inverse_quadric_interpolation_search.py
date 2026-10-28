import numpy as np

# Reverse parabolic interpolation search
def iqisearch(f, df, interval, tol=1e-6, c=None):
    a, b = interval # suppose a - x_prev; b - x_prev_prev
    if c is None: x = (a + b) / 2
    else: x = c

    df_a = df(a)
    df_b = df(b)
    df_x = df(x)

    neval = 3
    coords = [b, a, x]
    k = 0; kmax = 1000

    while True:
        x_new = \
            b * (df_a * df_x) / ((df_b - df_a) * (df_b - df_x)) + \
            a * (df_b * df_x) / ((df_a - df_b) * (df_a - df_x)) + \
            x * (df_b * df_a) / ((df_x - df_b) * (df_x - df_a))

        # update x, a, b
        b = a
        a = x
        x = x_new

        # update gradients
        df_b = df_a
        df_a = df_x
        df_x = df(x)

        # update logs
        neval += 1
        k += 1
        coords.append(x)
        
        # end of search    
        if (abs(x - a) <= tol) or (k == kmax):
            break
    
    xmin = x
    fmin = f(xmin); neval += 1

    return xmin, fmin, neval, coords