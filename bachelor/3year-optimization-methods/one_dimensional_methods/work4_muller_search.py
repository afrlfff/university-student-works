import numpy as np

# finite differences first order
def fin_diff_1(x0, x1, g0, g1):
    return (g1 - g0) / (x1 - x0)

# finite differences second order
def fin_diff_2(x0, x1, x2, g0, g1, g2):
    return (fin_diff_1(x1, x2, g1, g2) - fin_diff_1(x0, x1, g0, g1)) / (x2 - x0)

def w(x, x_prev, x_prev_prev, g, g_prev, g_prev_prev):
    return fin_diff_1(x_prev, x, g_prev, g) \
            + fin_diff_1(x_prev_prev, x, g_prev_prev, g) \
            - fin_diff_1(x_prev_prev, x_prev, g_prev_prev, g_prev)

# find points of interseption of function with the X-axis
def get_zeros(x, x_prev, x_prev_prev, g, g_prev, g_prev_prev):
    w_ = w(x, x_prev, x_prev_prev, g, g_prev, g_prev_prev)
    fd2_ = fin_diff_2(x_prev_prev, x_prev, x, g_prev_prev, g_prev, g)
    
    return (w_ + np.sqrt(w_**2 - 4*g*fd2_)), \
            (w_ - np.sqrt(w_**2 - 4*g*fd2_))


# Muller search
def mulsearch(f, df, interval, tol, c=None):
    a, b = interval # suppose a - x_prev; b - x_prev_prev
    if c is None: x = (a + b) / 2
    else: x = c

    df_a = df(a); df_b = df(b); df_x = df(x)

    neval = 3
    coords = [b, a, x]
    k = 0; kmax = 1000

    while True:
        # find discriminant
        z1, z2 = get_zeros(x, a, b, df_x, df_a, df_b)

        if (z1 == np.nan) or (z2 == np.nan):
            print('Got nan while solving the quadric equation')
            break

        # update x, a, b
        b = a
        a = x
        if abs(z1) > abs(z2):
            x = x - (2*df_x) / z1
        else:
            x = x - (2*df_x) / z2
        
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