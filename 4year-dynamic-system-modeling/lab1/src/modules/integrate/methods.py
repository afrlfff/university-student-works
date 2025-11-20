import numpy as np

# ================================================================================

def euler(df, t, init_conditions):
    y = np.zeros( (len(t), len(init_conditions)) )
    
    y[0] = init_conditions
    for i in range(1, len(t)):
        dt = t[i] - t[i-1]
        y[i] = y[i-1] + dt * df(y[i-1])
    
    return y

# ================================================================================

def runge_kutta_4(df, t, init_conditions):
    y = np.zeros( (len(t), len(init_conditions)) )
    k = np.zeros( (4, len(init_conditions)) )
    
    y[0] = init_conditions
    for i in range(1, len(t)):
        dt = t[i] - t[i-1]

        k[0] = df(y[i-1])
        k[1] = df(y[i-1] + dt * k[0] / 2)
        k[2] = df(y[i-1] + dt * k[1] / 2)
        k[3] = df(y[i-1] + dt * k[2])

        y[i] = y[i-1] + (dt / 6) * (k[0] + 2*k[1] + 2*k[2] + k[3])
    
    return y

# ================================================================================

def midpoint(df, t, init_conditions):
    y = np.zeros( (len(t), len(init_conditions)) )
    y[0] = init_conditions

    for i in range(1, len(t)):
        dt = t[i] - t[i-1]
        y_prev = y[i-1]

        k1 = df(y_prev)
        y_mid = y_prev + (dt / 2) * k1
        k2 = df(y_mid)

        y[i] = y_prev + dt * k2

    return y

# ================================================================================

def euler_cromer(df, t, init_conditions):
    y = np.zeros((len(t), len(init_conditions)))
    y[0] = init_conditions

    for i in range(1, len(t)):
        dt = t[i] - t[i-1]
        y_prev = y[i-1].copy()
        y_curr = y_prev.copy()

        for j in range(len(init_conditions)):
            derivs = df(y_curr)
            y_curr[j] = y_prev[j] + dt * derivs[j]

        y[i] = y_curr

    return y

# ================================================================================

def cd_lorenz(t, init_conditions, args):
    n = len(t)
    y = np.zeros((n, len(args)))
    y[0] = init_conditions

    sigma, rho, beta = args

    dt = t[1] - t[0]
    s = 0.5
    h1 = dt * s
    h2 = dt * (1 - s)

    denom_z = 1.0 + h2 * beta
    denom_y = 1.0 + h2
    denom_x = 1.0 + h2 * sigma

    sigma_h1 = sigma * h1
    sigma_h2 = sigma * h2

    for i in range(n - 1):
        x_i, y_i, z_i = y[i]

        # Explicit half-step
        x_s = x_i + sigma_h1 * (y_i - x_i)
        y_s = y_i + h1 * (x_s * (rho - z_i) - y_i)
        z_s = z_i + h1 * (x_s * y_s - beta * z_i)

        # Implicit half-step (reverse order)
        z_next = (z_s + h2 * x_s * y_s) / denom_z
        y_next = (y_s + h2 * x_s * (rho - z_next)) / denom_y
        x_next = (x_s + sigma_h2 * y_next) / denom_x

        y[i + 1] = [x_next, y_next, z_next]

    return y

# ================================================================================