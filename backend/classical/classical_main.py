#!/usr/bin/env python3
"""
Classical algorithms runner script
Runs all classical algorithms with test data
"""
from sklearn.datasets import load_wine
import time
from factorization import classical_factorization
from search import classical_search
from min_max import classical_min_max
from phase_estimation import classical_phase_estimation
from deutsch_jozsa import classical_deutsch_jozsa

def main():
    # Load Wine Dataset
    print("Loading Wine Dataset...")
    wine = load_wine()
    wine_data = wine.data
    
    print(f"\nDataset shape: {wine_data.shape}")
    print(f"Features: {list(wine.feature_names)}")
    print(f"Classes: {wine.target}")
    
    print("\n" + "="*80)
    print("1. Running Classical Factorization")
    print("="*80)
    try:
        test_numbers = [15, 21, 35, 77]
        for N in test_numbers:
            start = time.time()
            result = classical_factorization(N)
            elapsed = time.time() - start
            print(f"N={N}: Factors={result}, Time={elapsed:.6f}s")
    except Exception as e:
        print(f"Error in Classical Factorization: {e}")
    
    print("\n" + "="*80)
    print("2. Running Classical Search")
    print("="*80)
    try:
        test_cases = [
            ([5], 16, "Single item in 16 elements"),
            ([3, 7], 16, "Two items in 16 elements"),
            ([11], 32, "Single item in 32 elements"),
        ]
        for marked_items, space_size, description in test_cases:
            start = time.time()
            result = classical_search(marked_items, space_size)
            elapsed = time.time() - start
            print(f"\n{description}")
            print(f"  Found: {result['found_items']}")
            print(f"  Comparisons: {result['comparisons']}")
            print(f"  Time: {elapsed:.6f}s")
    except Exception as e:
        print(f"Error in Classical Search: {e}")
    
    print("\n" + "="*80)
    print("3. Running Classical Min/Max Finding")
    print("="*80)
    try:
        test_datasets = [
            ([7, 3, 9, 1, 5, 8, 2, 6], "8 random values"),
            ([15, 8, 23, 4, 16, 42, 11, 19], "8 larger values"),
            ([5, 5, 5, 1, 5, 5, 5, 5], "Mostly identical with one min"),
        ]
        
        for data, description in test_datasets:
            print(f"\n{description}: {data}")
            
            # Find Minimum
            start = time.time()
            min_result = classical_min_max(data, find_min=True)
            min_time = time.time() - start
            
            print(f"  Minimum: Value={min_result['value']}, Index={min_result['index']}, Comparisons={min_result['comparisons']}, Time={min_time:.6f}s")
            
            # Find Maximum
            start = time.time()
            max_result = classical_min_max(data, find_min=False)
            max_time = time.time() - start
            
            print(f"  Maximum: Value={max_result['value']}, Index={max_result['index']}, Comparisons={max_result['comparisons']}, Time={max_time:.6f}s")
    except Exception as e:
        print(f"Error in Classical Min/Max: {e}")
    
    print("\n" + "="*80)
    print("4. Running Classical Deutsch-Jozsa")
    print("="*80)
    try:
        test_cases = [
            (3, 'constant', "3 qubits, constant function"),
            (3, 'balanced', "3 qubits, balanced function"),
            (4, 'constant', "4 qubits, constant function"),
            (4, 'balanced', "4 qubits, balanced function"),
            (5, 'balanced', "5 qubits, balanced function"),
        ]
        
        for n_qubits, func_type, description in test_cases:
            start = time.time()
            result = classical_deutsch_jozsa(n_qubits, func_type)
            elapsed = time.time() - start
            print(f"\n{description}")
            print(f"  Detected: {result['detected_type']}")
            print(f"  Correct: {result['correct']}")
            print(f"  Queries: {result['queries']}")
            print(f"  Time: {elapsed:.6f}s")
    except Exception as e:
        print(f"Error in Classical Deutsch-Jozsa: {e}")
    
    print("\n" + "="*80)
    print("5. Running Classical Phase Estimation")
    print("="*80)
    try:
        test_cases = [
            (0.25, 4, "Phase = 1/4, 4 bits"),
            (0.5, 4, "Phase = 1/2, 4 bits"),
            (0.125, 5, "Phase = 1/8, 5 bits"),
            (0.375, 5, "Phase = 3/8, 5 bits"),
            (0.3, 6, "Phase = 0.3 (non-dyadic), 6 bits"),
        ]
        
        for phase, n_bits, description in test_cases:
            start = time.time()
            result = classical_phase_estimation(phase, n_samples=100)
            elapsed = time.time() - start
            print(f"\n{description}")
            print(f"  Estimated phase: {result['estimated_phase']:.6f}")
            print(f"  Error: {result['error']:.6f}")
            print(f"  Precision: {result['precision']:.6f}")
            print(f"  Time: {elapsed:.6f}s")
    except Exception as e:
        print(f"Error in Classical Phase Estimation: {e}")
    
    print("\n" + "="*80)
    print("6. Performance Summary")
    print("="*80)
    
    # Run timing comparisons
    print("\nTiming Comparison:")
    
    # Factorization
    start = time.time()
    for _ in range(100):
        classical_factorization(91)
    factor_time = time.time() - start
    print(f"  Factorization (100 runs): {factor_time:.6f}s")
    
    # Search
    start = time.time()
    for _ in range(100):
        classical_search([5], 16)
    search_time = time.time() - start
    print(f"  Search (100 runs): {search_time:.6f}s")
    
    # Min/Max
    start = time.time()
    for _ in range(100):
        classical_min_max([7, 3, 9, 1, 5, 8, 2, 6], find_min=True)
    minmax_time = time.time() - start
    print(f"  Min/Max (100 runs): {minmax_time:.6f}s")
    
    # Deutsch-Jozsa
    start = time.time()
    for _ in range(100):
        classical_deutsch_jozsa(3, 'constant')
    dj_time = time.time() - start
    print(f"  Deutsch-Jozsa (100 runs): {dj_time:.6f}s")
    
    # Phase Estimation
    start = time.time()
    for _ in range(100):
        classical_phase_estimation(0.25, n_samples=10)
    pe_time = time.time() - start
    print(f"  Phase Estimation (100 runs): {pe_time:.6f}s")
    
    print("\n" + "="*80)
    print("All classical algorithms completed!")
    print("="*80)

if __name__ == "__main__":
    main()
