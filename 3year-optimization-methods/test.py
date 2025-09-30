import numpy as np
from input_functions import f1, df1, ddf1, f2, df2, fH, dfH, fR, dfR

# ===== Work 1. Test dichotomy
from one_dimensional_methods import bsearch
a = -2
b = 10
interval = [a, b]
tol = 1e-10
answer = bsearch(f1, df1, interval, tol)
print(answer)

# ===== Work 2. Test golden search
""" from one_dimensional_methods import gsearch
a = -2
b = 10
interval = [a, b]
tol = 1e-10
answer = gsearch(f1, interval, tol)
print(answer) """

# ===== Work 2. Test Fibonacci
""" from one_dimensional_methods import fibsearch
a = -2
b = 10
interval = [a, b]
tol = 1e-10
answer = fibsearch(f1, interval, tol)
print(answer) """

# ===== Work 3. Test one-dimensional newton search
""" from one_dimensional_methods import nsearch
x0 = -2
tol = 1e-10
answer = nsearch(f1, df1, ddf1, x0, tol)
print(answer) """

# ===== Work 3. Test secant seacrh
""" from one_dimensional_methods import ssearch
a = -2
b = 10
tol = 1e-10
answer = ssearch(f1, df1, [a, b], tol)
print(answer) """

# ===== Work 4. Test Muller method
""" from one_dimensional_methods import mulsearch
a = -2
b = 5
interval = [a, b]
tol = 1e-10
answer = mulsearch(f2, df2, interval, tol)
print(answer) """

# ===== Work 4. Test Reverse parabolic interpolation method
""" from one_dimensional_methods import iqisearch
a = -2
b = 5
interval = [a, b]
tol = 1e-10
answer = iqisearch(f2, df2, interval, tol)
print(answer) """

# ===== Work 4. Test Brent dekker method
""" from one_dimensional_methods import brent_dekker
a = -2
b = 5
interval = [a, b]
tol = 1e-10
answer = brent_dekker(f2, df2, interval, tol)
print(answer) """

# ===== Work 5. Test gradient descent
""" from multidimensional_methods import grsearch
x0 = np.array([0, 1])
tol = 1e-3
answer = grsearch(fH, dfH, x0, tol)
print(answer[:3]) """

# ===== Work 6. Test steepest descent
""" from multidimensional_methods import sdsearch
x0 = np.array([[1.3], [2.0]])
tol = 1e-3
answer = sdsearch(fH, dfH, x0, tol)
print(answer[:3])
answer = sdsearch(fR, dfR, x0, tol)
print(answer[:3]) """

# ===== Work 7. Test multidimensional newton search
""" from multidimensional_methods import nsearch
x0 = np.array([[-2.0], [-2.0]])
tol = 1e-3
answer_ = nsearch(fH, dfH, x0, tol)
print(answer_[:3])
answer_ = nsearch(fR, dfR, x0, tol)
print(answer_[:3]) """

# ===== Work 8. Test Barzilai-Borwein search
""" from multidimensional_methods import bbsearch
x0 = np.array([[2], [-1]])
tol = 1e-9
answer_ = bbsearch(fR, dfR, x0, tol)
print(answer_[:3]) """

# ===== Work 9. Test Polak-Ribiere search
""" from multidimensional_methods import prsearch
x0 = np.array([[1.0], [0.0]])
tol = 1e-9
answer = prsearch(fH, dfH, x0, tol)
print(answer[:3])
x0 = np.array([[-2], [0]])
tol = 1e-9
answer = prsearch(fR, dfR, x0, tol)
print(answer[:3]) """

# ===== Work 10. Test Davidon-Fletcher-Powell search
""" from multidimensional_methods import dfpsearch
x0 = np.array([[1.0], [0.0]])
tol = 1e-9
answer = dfpsearch(fH, dfH, x0, tol)
print(answer[:3])
x0 = np.array([[-3], [-3]])
tol = 1e-9
answer = dfpsearch(fR, dfR, x0, tol)
print(answer[:3]) """

# ===== Work 11. Test Trust regions search
""" from multidimensional_methods import trustreg
x0 = np.array([[2.0], [1.0]])
tol = 1e-3
answer = trustreg(fH, dfH, x0, tol)
print(answer[:3])
print("Rosenbrock function:")
x0 = np.array([[-1], [-1]])
tol = 1e-3
answer = trustreg(fR, dfR, x0, tol)
print(answer[:3]) """


# ===== Work 12. Test Nesterev accelerated gradient descent
""" from multidimensional_methods import nagsearch
x0 = np.array([[0.0], [1.0]])
tol = 1e-3
[xmin, f, neval, coords] = nagsearch(fH, dfH, x0, tol)
print(xmin, f, neval) """