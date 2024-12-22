import numpy as np

def goldensectionsearch(f, interval, tol):
    a = interval[0]
    b = interval[1]
    Phi = (1 + np.sqrt(5)) / 2
    L = b - a
    x1 = b - L / Phi
    x2 = a + L / Phi
    y1 = f(x1)
    y2 = f(x2)
    neval = 2
    xmin = x1
    fmin = y1

    # main loop
    while np.abs(L) > tol:
        if y1 > y2:
            a = x1
            xmin = x2
            fmin = y2
            x1 = x2
            y1 = y2
            L = b - a
            x2 = a + L / Phi
            y2 = f(x2)
            neval += 1
        else:
            b = x2
            xmin = x1
            fmin = y1
            x2 = x1
            y2 = y1
            L = b - a
            x1 = b - L / Phi
            y1 = f(x1)
            neval += 1

    answer_ = [xmin, fmin, neval]
    return answer_


def pparam(pU, pB, tau):
    if (tau <= 1):
        p = np.dot(tau, pU)
    else:
        p = pU + (tau - 1) * (pB - pU)
    return p


def doglegsearch(mod, g0, B0, Delta, tol):
    # dogleg local search
    xcv = np.dot(-g0.transpose(), g0) / np.dot(np.dot(g0.transpose(), B0), g0)
    pU = xcv *g0
    xcvb = np.linalg.inv(- B0)
    pB = np.dot(np.linalg.inv(- B0), g0)

    func = lambda x: mod(np.dot(x, pB))
    al = goldensectionsearch(func, [-Delta / np.linalg.norm(pB), Delta / np.linalg.norm(pB)], tol)[0]
    pB = al * pB
    func_pau = lambda x: mod(pparam(pU, pB, x))
    tau = goldensectionsearch(func_pau, [0, 2], tol)[0]
    pmin = pparam(pU, pB, tau)
    if np.linalg.norm(pmin) > Delta:
        pmin_dop = (Delta / np.linalg.norm(pmin))
        pmin = np.dot(pmin_dop, pmin)
    return pmin

# Broyden-Fletcher-Goldfarb-Shanno for non-inverted Hessian matrix
def bfsg_noninv(B, d, y):

    middle = np.dot(np.dot(np.dot(B, d), np.transpose(d)), np.transpose(B)) / \
          np.dot(np.dot(np.transpose(d), B), d)

    right = np.dot(y, np.transpose(y)) / np.dot(np.transpose(y), d)

    return B - middle + right

# Trust regions search
def trustreg(f, df, x0, tol, eta=0.1):
    neval = 0
    k = 0; kmax = 1000
    coords = [x0]
    radii = [1] # array of delta values 

    # initialization
    x = x_prev = x0
    delta = 1 # trust region radius
    delta_max = 1
    B = np.eye(2) # start approximation of Hessian

    while True:
        g = df(x); neval += 1
        f_k = f(x); neval += 1

        # quadric model
        m = lambda p_ : f_k + np.dot(np.transpose(p_), g) + 0.5 * np.dot(np.dot(np.transpose(p_), B), p_)

        # use Dogled to find p 
        p = doglegsearch(m, g, B, delta, tol)    

        # calculate "ro" (reaion between real and predicted decreasing of f)
        ro = (f_k - f(x + p)) / (m(np.zeros(2)) - m(p))

        # update x and g
        if ro > eta:
            x_prev = x
            g_prev = g
            x = x_prev + p
            g = df(x); neval += 1

        # update radius
        if ro < 0.25:
            delta = 0.25 * delta
        elif (ro > 0.75) and (abs(np.linalg.norm(p) - delta) < tol):
            delta = min(2 * delta, delta_max)        
        
        # update B
        B = bfsg_noninv(B, x - x_prev, g - g_prev)

        # update logs 
        radii.append(delta)
        coords.append(x)

        # end of search
        if not((np.linalg.norm(x - x_prev) >= tol) and (k < kmax)):
            break

        k += 1
    
    xmin = x
    fmin = f_k
    
    answer_ = [xmin, fmin, neval, coords, radii]
    return answer_
