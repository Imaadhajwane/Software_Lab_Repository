# deutsch_jozsa.py

import numpy as np


def deutsch_jozsa(f, n):
    N = 2 ** n

    # superposition
    state = np.ones(N) / np.sqrt(N)

    # apply oracle phase flip
    for x in range(N):
        if f(x) == 1:
            state[x] *= -1

    # Hadamard (classical equivalent)
    result = np.fft.fft(state)

    if np.allclose(result[1:], 0):
        return "Constant"
    else:
        return "Balanced"
