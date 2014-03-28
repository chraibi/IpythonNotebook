import numpy as np
from numba.decorators import autojit
import time

X = np.random.random((1000, 3))

def pairwise_python(X):
    M = X.shape[0]
    N = X.shape[1]
    D = np.empty((M, M), dtype=np.float)
    for i in range(M):
        for j in range(M):
            d = 0.0
            for k in range(N):
                tmp = X[i, k] - X[j, k]
                d += tmp * tmp
            D[i, j] = np.sqrt(d)
    return D


# numba
pairwise_numba = autojit(pairwise_python)


start = time.time()
pairwise_python(X)
t_py = time.time()-start


start = time.time()
pairwise_numba(X)
t_na = time.time()-start

print "time Python: %.3f /s"%t_py
print "time Numba: %.3f /s"%t_na
print "Speedup: %.3f"%(t_py/t_na)
