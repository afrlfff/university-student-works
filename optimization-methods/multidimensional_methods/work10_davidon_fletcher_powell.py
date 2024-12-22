import numpy as np

def zoom(phi, dphi, alo, ahi, c1, c2):
    j = 1
    jmax = 1000
    while j < jmax:
        a = cinterp(phi, dphi, alo, ahi)
        if phi(a) > phi(0) + c1 * a * dphi(0) or phi(a) >= phi(alo):
            ahi = a
        else:
            if abs(dphi(a)) <= -c2 * dphi(0):
                return a  # a is found
            if dphi(a) * (ahi - alo) >= 0:
                ahi = alo
            alo = a
        j += 1
    return a


def cinterp(phi, dphi, a0, a1):
    if np.isnan(dphi(a0) + dphi(a1) - 3 * (phi(a0) - phi(a1))) or (a0 - a1) == 0:
        a = a0
        return a
 
    d1 = dphi(a0) + dphi(a1) - 3 * (phi(a0) - phi(a1)) / (a0 - a1)
    if np.isnan(np.sign(a1 - a0) * np.sqrt(d1 ** 2 - dphi(a0) * dphi(a1))):
        a = a0
        return a
    d2 = np.sign(a1 - a0) * np.sqrt(d1 ** 2 - dphi(a0) * dphi(a1))
    a = a1 - (a1 - a0) * (dphi(a1) + d2 - d1) / (dphi(a1) - dphi(a0) + 2 * d2)

    return a


def wolfesearch(f, df, x0, p0, amax, c1, c2):
    a = amax
    aprev = 0
    phi = lambda x: f(x0 + x * p0)
    dphi = lambda x: np.dot(p0.transpose(), df(x0 + x * p0))

    phi0 = phi(0)
    dphi0 = dphi(0)
    i = 1
    imax = 1000
    while i < imax:
        if (phi(a) > phi0 + c1 * a * phi0) or ((phi(a) >= phi(aprev)) and (i > 1)):
            a = zoom(phi, dphi, aprev, a, c1, c2)
            return a

        if abs(dphi(a)) <= -c2 * dphi0:
            return a  # a is found already

        if dphi(a) >= 0:
            a = zoom(phi, dphi, a, aprev, c1, c2)
            return a

        a = cinterp(phi, dphi, a, amax)
        i += 1


    return a


# Davidon-Fletcher-Powell search
def dfpsearch(f, df, x0, tol):
    k = 0; kmax = 1000
    coords = [x0]
    neval = 0
    
    # wolf search constants
    amax = 3
    c1 = tol
    c2 = 0.1
    
    # initialize start values 
    x = x0
    g = df(x); neval += 1
    H = I = np.eye(2)

    while True:
        # update direction
        p = - np.dot(H, g)

        # calculate alpha 
        alpha = wolfesearch(f, df, x, p, amax, c1, c2)

        # update x and g
        x_prev = x
        g_prev = g
        x = x_prev + alpha * p
        g = df(x); neval += 1
        
        # update d and y
        d = x - x_prev
        y = g - g_prev

        # davidon-fletcher-powell method
        H = H \
            + np.dot(d, np.transpose(d)) / np.dot(np.transpose(d), y) \
            - ( np.dot(np.dot(np.dot(H,  y), np.transpose(y)), H) \
                / np.dot(np.dot(np.transpose(y), H), y) )

        # update coords and k
        k += 1
        coords.append(x)

        # end of search
        if not((np.linalg.norm(d) >= tol) and (k < kmax)):
            break

    xmin = x
    fmin = f(x); neval += 1
    
    answer_ = [xmin, fmin, neval, coords]
    return answer_