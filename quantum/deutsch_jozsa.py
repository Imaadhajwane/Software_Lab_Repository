"""
Deutsch-Jozsa Algorithm
Determines if a function is constant or balanced in a single query
"""
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import Aer
import random
import sys
sys.path.append('..')
from base import BaseAlgorithm
from classical.deutsch_jozsa import classical_deutsch_jozsa


class DeutschJozsaAlgorithm(BaseAlgorithm):
    """Deutsch-Jozsa quantum algorithm"""
    
    def __init__(self):
        super().__init__("Deutsch-Jozsa Algorithm")
        self.backend = Aer.get_backend('qasm_simulator')
    
    def run(self, n_qubits: int, function_type: str = 'balanced') -> dict:
        """
        Determine if function is constant or balanced
        
        Args:
            n_qubits: Number of input qubits
            function_type: 'constant' or 'balanced'
        
        Returns:
            Dictionary with result and circuit info
        """
        if n_qubits > 10:
            return {'error': 'Too many qubits for simulation'}
        
        # Create quantum circuit
        qr = QuantumRegister(n_qubits + 1, 'q')  # +1 for ancilla
        cr = ClassicalRegister(n_qubits, 'c')
        qc = QuantumCircuit(qr, cr)
        
        # Initialize ancilla to |1>
        qc.x(qr[n_qubits])
        
        # Apply Hadamard gates to all qubits
        qc.h(range(n_qubits + 1))
        
        # Apply oracle
        self._oracle(qc, qr, n_qubits, function_type)
        
        # Apply Hadamard gates to input qubits
        qc.h(range(n_qubits))
        
        # Measure input qubits
        qc.measure(range(n_qubits), range(n_qubits))
        
        # Execute circuit
        job = self.backend.run(qc, shots=1024)
        result = job.result()
        counts = result.get_counts()
        
        # Analyze results
        # If all zeros, function is constant
        # Otherwise, function is balanced
        all_zeros = '0' * n_qubits
        
        if all_zeros in counts and counts[all_zeros] > 900:  # High probability
            detected_type = 'constant'
        else:
            detected_type = 'balanced'
        
        is_correct = detected_type == function_type
        
        return {
            'n_qubits': n_qubits,
            'actual_type': function_type,
            'detected_type': detected_type,
            'correct': is_correct,
            'measurements': counts,
            'circuit': qc,
            'queries': 1  # Deutsch-Jozsa uses only 1 query
        }
    
    def _oracle(self, qc, qr, n_qubits, function_type):
        """
        Oracle implementation for constant or balanced function
        """
        if function_type == 'constant':
            # Constant function: f(x) = 0 or f(x) = 1 for all x
            if random.random() < 0.5:
                # f(x) = 1 for all x
                qc.x(qr[n_qubits])
            # else: f(x) = 0 for all x (do nothing)
        
        elif function_type == 'balanced':
            # Balanced function: f(x) = 1 for exactly half the inputs
            # Create a random balanced oracle
            
            # One simple balanced function: parity
            # f(x) = XOR of all input bits
            for i in range(n_qubits):
                qc.cx(qr[i], qr[n_qubits])
        
        else:
            raise ValueError("function_type must be 'constant' or 'balanced'")

if __name__ == "__main__":
    print("=== Deutsch-Jozsa Algorithm Test ===\n")
    
    dj = DeutschJozsaAlgorithm()
    
    # Test cases
    test_cases = [
        (3, 'constant'),
        (3, 'balanced'),
        (4, 'constant'),
        (4, 'balanced'),
        (5, 'balanced'),
    ]
    
    for n_qubits, func_type in test_cases:
        print(f"Testing {func_type} function with {n_qubits} qubits")
        
        # Quantum algorithm
        q_result = dj.benchmark(n_qubits, func_type)
        print(f"Quantum result: {q_result['result']}")
        print(f"Quantum queries: {q_result['result']['queries']}")
        print(f"Quantum time: {q_result['execution_time']:.4f}s")
        
        # Classical algorithm
        c_result = classical_deutsch_jozsa(n_qubits, func_type)
        print(f"Classical result: {c_result}")
        print(f"Classical queries: {c_result['queries']}")
        
        speedup = c_result['queries'] / q_result['result']['queries']
        print(f"Query speedup: {speedup:.0f}x")
        print("-" * 50 + "\n")