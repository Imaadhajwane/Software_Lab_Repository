#!/usr/bin/env python3
"""
Main script to run quantum algorithms
"""
from sklearn.datasets import load_wine
import numpy as np
from shor import ShorAlgorithm
from grover import GroverAlgorithm
from deutsch_jozsa import DeutschJozsaAlgorithm
from min_max import QuantumMinMaxAlgorithm
from phase_estimation import QuantumPhaseEstimation

def main():
    # Load Wine Dataset
    print("Loading Wine Dataset...")
    wine = load_wine()
    wine_data = wine.data
    
    print(f"Dataset shape: {wine_data.shape}")
    print(f"Features: {list(wine.feature_names)}")
    print(f"Classes: {wine.target}")
    
    print("\n" + "="*80)
    print("1. Running Shor's Algorithm")
    print("="*80)
    try:
        shor = ShorAlgorithm()
        result = shor.run(15)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*80)
    print("2. Running Grover's Algorithm")
    print("="*80)
    try:
        grover = GroverAlgorithm()
        result = grover.run([5], 16)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*80)
    print("3. Running Deutsch-Jozsa")
    print("="*80)
    try:
        dj = DeutschJozsaAlgorithm()
        result = dj.run(3, 'constant')
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*80)
    print("4. Running Quantum Min/Max")
    print("="*80)
    try:
        qmm = QuantumMinMaxAlgorithm()
        result = qmm.run([7, 3, 9, 1, 5, 8, 2, 6], find_min=True)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*80)
    print("5. Running Quantum Phase Estimation")
    print("="*80)
    try:
        qpe = QuantumPhaseEstimation()
        result = qpe.run(0.25, 4)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*80)
    print("All algorithms completed!")
    print("="*80)

if __name__ == "__main__":
    main()
