# search.py

import numpy as np


def grover_search(n, target_index):
    N = 2 ** n
    state = np.ones(N) / np.sqrt(N)

    def oracle(state):
        state[target_index] *= -1
        return state

    def diffusion(state):
        mean = np.mean(state)
        return 2 * mean - state

    iterations = int(np.pi/4 * np.sqrt(N))

    for _ in range(iterations):
        state = oracle(state)
        state = diffusion(state)

    return np.argmax(np.abs(state))
