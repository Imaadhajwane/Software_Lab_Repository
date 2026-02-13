# factorization.py

import random
import math

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def find_period(a, N):
    r = 1
    while pow(a, r, N) != 1:
        r += 1
    return r

def shor_factor(N):
    if N % 2 == 0:
        return 2

    while True:
        a = random.randint(2, N - 1)
        g = gcd(a, N)
        if g > 1:
            return g

        r = find_period(a, N)

        if r % 2 != 0:
            continue

        x = pow(a, r // 2, N)
        if x == N - 1:
            continue

        p = gcd(x - 1, N)
        q = gcd(x + 1, N)

        if p > 1 and q > 1:
            return p, q
