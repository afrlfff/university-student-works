import numpy as np

from .work1_dichotomy_search import bsearch
from .work3_secant_search import ssearch
from .work4_inverse_quadric_interpolation_search import iqisearch

# Inverse quadric interpolation search
def brent_dekker(f, df, interval, tol):
    a, b = interval
    x = a

    f_a = f(a)
    f_b = f(b)
    f_x = f(x)

    neval = 3
    coords = []
    k = 0; kmax = 1000

    while True:
        flag = 0
        # Brent Dekker search
        if (f_a != f_x) and (f_b != f_x):
            s, f_x, neval_, _ = iqisearch(f, df, [a, b], tol, x)
            flag = 1
        elif f(a) != f(b):
            s, f_x, neval_, _ = ssearch(f, df, [a, b], tol)
            flag = 2
        elif (not((  ((3*a + b) / 4) <= s <= b)  or (b <= s <= (3*a + b) / 4)  )) \
            or ((1 <= flag <= 2) and (tol < abs(a - b)) and (abs(s - x) < 0.5 * abs(a - b))) \
            or ((flag == 3) and (tol < abs(x - a)) and (abs(s - x) < 0.5 * (x - a))):
            s, f_x, neval_, _ = bsearch(f, df, [a, b], tol)
            flag = 3
        
        # update x, a, b
        b = a
        a = x
        x = s

        # update logs
        k += 1
        coords.append(x)
        neval += neval_

        # end of search
        if (k == kmax) or (flag == 0):
            break
    
    xmin = x
    fmin = f_x

    return xmin, fmin, neval, coords