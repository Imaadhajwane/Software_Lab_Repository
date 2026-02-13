# phase_estimation.py

import numpy as np


def phase_estimation(U, eigenvector, t):
    N = 2 ** t

    state = np.zeros(N, dtype=complex)

    for k in range(N):
        phase = np.linalg.matrix_power(U, k).dot(eigenvector)
        state[k] = phase[0]

    # inverse QFT via FFT
    result = np.fft.ifft(state)

    index = np.argmax(np.abs(result))
    phi = index / N

    return phi
