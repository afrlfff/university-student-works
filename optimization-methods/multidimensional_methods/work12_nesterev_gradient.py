import numpy as np

# Nesterev gradient search
def nagsearch(f, df, x0, tol):
    k = 0; kmax = 1000
    coords = [x0]
    neval = 0

    # constants
    al = 0.05
    nu = al / 10
    gamma = 0.75

    # start initialization    
    x = x0
    y = x0
    g = df(x); neval += 1

    while True:
        # update x, y, g
        x_prev = x
        x = y - nu * g
        y = x_prev + gamma * (x - x_prev)
        g = df(x); neval += 1

        # update k and coords
        k += 1
        coords.append(x)

        # end of search
        if not((np.linalg.norm(g) >= tol) and (k < kmax)):
            break

    xmin = x
    fmin = f(x); neval += 1

    return xmin, fmin, neval, coords
