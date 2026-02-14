import math

def classical_factorization(N: int) -> list:
    """Classical trial division factorization"""
    if N < 2:
        return []
    
    factors = []
    
    # Check for factor of 2
    while N % 2 == 0:
        factors.append(2)
        N //= 2
    
    # Check odd factors up to sqrt(N)
    i = 3
    while i * i <= N:
        while N % i == 0:
            factors.append(i)
            N //= i
        i += 2
    
    # If N is still greater than 1, it's prime
    if N > 1:
        factors.append(N)
    
    return factors