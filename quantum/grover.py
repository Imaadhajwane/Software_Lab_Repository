"""
Grover's Algorithm for Unstructured Search
Quantum algorithm that searches for marked items in O(√N) time
"""
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import Aer
import math
import sys
sys.path.append('..')
from base import BaseAlgorithm
from classical.search import classical_search


class GroverAlgorithm(BaseAlgorithm):
    """Grover's quantum search algorithm"""
    
    def __init__(self):
        super().__init__("Grover's Algorithm")
        self.backend = Aer.get_backend('qasm_simulator')
    
    def run(self, marked_items: list, search_space_size: int) -> dict:
        """
        Search for marked items in an unstructured database
        
        Args:
            marked_items: List of indices to search for
            search_space_size: Size of search space (should be power of 2)
        
        Returns:
            Dictionary with found items and success rate
        """
        if search_space_size == 0 or not (search_space_size & (search_space_size - 1) == 0):
            return {'error': 'Search space must be a power of 2'}
        
        n_qubits = int(math.log2(search_space_size))
        
        if n_qubits > 10:
            return {'error': 'Search space too large for simulation'}
        
        # Calculate optimal number of Grover iterations
        n_iterations = int(math.floor(math.pi / 4 * math.sqrt(search_space_size / len(marked_items))))
        
        # Create quantum circuit
        qr = QuantumRegister(n_qubits, 'q')
        cr = ClassicalRegister(n_qubits, 'c')
        qc = QuantumCircuit(qr, cr)
        
        # Initialize superposition
        qc.h(qr)
        
        # Apply Grover iterations
        for _ in range(n_iterations):
            # Oracle
            self._oracle(qc, qr, marked_items, n_qubits)
            
            # Diffusion operator
            self._diffusion(qc, qr, n_qubits)
        
        # Measure
        qc.measure(qr, cr)
        
        # Execute circuit
        job = self.backend.run(qc, shots=1000)
        result = job.result()
        counts = result.get_counts()
        
        # Analyze results
        found_items = []
        success_count = 0
        
        for bitstring, count in counts.items():
            value = int(bitstring, 2)
            if value in marked_items:
                found_items.append(value)
                success_count += count
        
        success_rate = success_count / 1000
        
        return {
            'marked_items': marked_items,
            'found_items': list(set(found_items)),
            'success_rate': success_rate,
            'iterations': n_iterations,
            'measurements': counts,
            'circuit': qc
        }
    
    def _oracle(self, qc, qr, marked_items, n_qubits):
        """
        Oracle that marks the target items by flipping their phase
        """
        for marked in marked_items:
            # Convert marked item to binary
            binary = format(marked, f'0{n_qubits}b')
            
            # Apply X gates to qubits that should be 0
            for i, bit in enumerate(reversed(binary)):
                if bit == '0':
                    qc.x(qr[i])
            
            # Multi-controlled Z gate
            if n_qubits == 1:
                qc.z(qr[0])
            elif n_qubits == 2:
                qc.cz(qr[0], qr[1])
            else:
                # Use multi-controlled Z
                qc.h(qr[n_qubits - 1])
                qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
                qc.h(qr[n_qubits - 1])
            
            # Undo X gates
            for i, bit in enumerate(reversed(binary)):
                if bit == '0':
                    qc.x(qr[i])
    
    def _diffusion(self, qc, qr, n_qubits):
        """
        Grover diffusion operator (inversion about average)
        """
        # Apply H gates
        qc.h(qr)
        
        # Apply X gates
        qc.x(qr)
        
        # Multi-controlled Z gate
        if n_qubits == 1:
            qc.z(qr[0])
        elif n_qubits == 2:
            qc.cz(qr[0], qr[1])
        else:
            qc.h(qr[n_qubits - 1])
            qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
            qc.h(qr[n_qubits - 1])
        
        # Apply X gates
        qc.x(qr)
        
        # Apply H gates
        qc.h(qr)


if __name__ == "__main__":
    print("=== Grover's Algorithm Test ===\n")
    
    grover = GroverAlgorithm()
    
    # Test cases
    test_cases = [
        ([5], 16),      # Search for single item in 16-element space
        ([3, 7], 16),   # Search for two items
        ([11], 32),     # Larger search space
    ]
    
    for marked_items, space_size in test_cases:
        print(f"Searching for {marked_items} in space of size {space_size}")
        
        # Quantum search
        q_result = grover.benchmark(marked_items, space_size)
        print(f"Quantum result: {q_result['result']}")
        print(f"Quantum time: {q_result['execution_time']:.4f}s")
        
        # Classical search
        c_result = classical_search(marked_items, space_size)
        print(f"Classical result: {c_result}")
        
        print(f"\nSpeedup: {c_result['average_comparisons'] / q_result['result']['iterations']:.2f}x")
        print("-" * 50 + "\n")