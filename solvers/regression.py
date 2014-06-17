import numpy as np

def compute_alpha(y, P, X, lmbda):
    A = P.T.dot(X.dot(P))
    A = np.vstack((A, lmbda*np.eye(P.shape[1])))
    y = np.hstack((y, np.zeros(P.shape[1])))
    return np.linalg.lstsq(A, y)
