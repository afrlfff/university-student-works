import numpy as np
import sys
from input_functions import f1, df1, ddf1, f2, df2, fH, dfH, fR, dfR

sys.path.append('..\\optimization-methods') # to be able to import methods 


# ===== Work 1. Test dichotomy
""" from one_dimensional_methods.work1_dichotomy_search import bsearch
a = -2
b = 10
interval = [a, b]
tol = 1e-10
answer = bsearch(f1, df1, interval, tol)
print(answer) """

# ===== Work 2. Test golden search
""" from one_dimensional_methods.work2_golden_search import gsearch
a = -2
b = 10
interval = [a, b]
tol = 1e-10
answer = gsearch(f1, interval, tol)
print(answer) """

# ===== Work 3. Test one-dimensional newton search
""" from one_dimensional_methods.work3_newton_search import nsearch
x0 = -2
tol = 1e-10
answer = nsearch(f1, df1, ddf1, x0, tol)
print(answer) """

# ===== Work 4. Test secant seacrh
""" from one_dimensional_methods.work4_secant_search import ssearch
a = -2
b = 10
tol = 1e-10
answer = ssearch(f1, df1, [a, b], tol)
print(answer) """

# ===== Work 5. Test gradient descent
""" from multidimensional_methods.work5_gradient_descent import grsearch
x0 = np.array([0, 1])
tol = 1e-3
answer = grsearch(fH, dfH, x0, tol)
print(answer[:3]) """

# ===== Work 6. Test steepest descent
""" from multidimensional_methods.work6_steepest_descent import sdsearch
x0 = np.array([[1.3], [2.0]])
tol = 1e-3
answer = sdsearch(fH, dfH, x0, tol)
print(answer[:3])
answer = sdsearch(fR, dfR, x0, tol)
print(answer[:3]) """

# ===== Work 7. Test multidimensional newton search
""" from multidimensional_methods.work7_newton_search import nsearch
x0 = np.array([[-2.0], [-2.0]])
tol = 1e-3
answer_ = nsearch(fH, dfH, x0, tol)
print(answer_[:3])
answer_ = nsearch(fR, dfR, x0, tol)
print(answer_[:3]) """

# ===== Work 8. Test Barzilai-Borwein search
""" from multidimensional_methods.work8_barzilai_borwein import bbsearch
x0 = np.array([[2], [-1]])
tol = 1e-9
answer_ = bbsearch(fR, dfR, x0, tol)
print(answer_[:3]) """

# ===== Work 9. Test Polak-Ribiere search
""" from multidimensional_methods.work9_polak_ribiere import prsearch
x0 = np.array([[1.0], [0.0]])
tol = 1e-9
answer = prsearch(fH, dfH, x0, tol)
print(answer[:3])
x0 = np.array([[-2], [0]])
tol = 1e-9
answer = prsearch(fR, dfR, x0, tol)
print(answer[:3]) """

# ===== Work 10. Test Davidon-Fletcher-Powell search
""" from multidimensional_methods.work10_davidon_fletcher_powell import dfpsearch
x0 = np.array([[1.0], [0.0]])
tol = 1e-9
answer = dfpsearch(fH, dfH, x0, tol)
print(answer[:3])
x0 = np.array([[-3], [-3]])
tol = 1e-9
answer = dfpsearch(fR, dfR, x0, tol)
print(answer[:3]) """

# ===== Work 11. Test Trust regions search
""" from multidimensional_methods.work11_trust_regions import trustreg
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
from multidimensional_methods.work12_nesterev_gradient import nagsearch
x0 = np.array([[0.0], [1.0]])
tol = 1e-3
[xmin, f, neval, coords] = nagsearch(fH, dfH, x0, tol)
print(xmin, f, neval)