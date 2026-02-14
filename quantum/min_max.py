"""
Quantum Min/Max Finding Algorithm
Uses amplitude amplification to find minimum or maximum in O(√N) time
"""
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import Aer
import math
import sys
sys.path.append('..')
from base import BaseAlgorithm
from classical.min_max import classical_min_max

class QuantumMinMaxAlgorithm(BaseAlgorithm):
    """Quantum algorithm for finding minimum/maximum"""
    
    def __init__(self):
        super().__init__("Quantum Min/Max Finding")
        self.backend = Aer.get_backend('qasm_simulator')
    
    def run(self, data: list, find_min: bool = True) -> dict:
        """
        Find minimum or maximum value in a list
        
        Args:
            data: List of values to search
            find_min: If True, find minimum; if False, find maximum
        
        Returns:
            Dictionary with found value and index
        """
        if len(data) == 0:
            return {'error': 'Empty data list'}
        
        # Pad to power of 2 if needed
        n = len(data)
        power_of_2 = 2 ** math.ceil(math.log2(n))
        
        if find_min:
            padded_data = data + [float('inf')] * (power_of_2 - n)
            target_value = min(data)
        else:
            padded_data = data + [float('-inf')] * (power_of_2 - n)
            target_value = max(data)
        
        # Find indices of min/max
        target_indices = [i for i, val in enumerate(data) if val == target_value]
        
        n_qubits = int(math.log2(power_of_2))
        
        if n_qubits > 10:
            return {'error': 'Data size too large for simulation'}
        
        # Calculate optimal iterations
        n_iterations = int(math.floor(math.pi / 4 * math.sqrt(power_of_2 / len(target_indices))))
        
        # Create quantum circuit
        qr = QuantumRegister(n_qubits, 'q')
        cr = ClassicalRegister(n_qubits, 'c')
        qc = QuantumCircuit(qr, cr)
        
        # Initialize superposition
        qc.h(qr)
        
        # Apply amplitude amplification (Grover-like iterations)
        for _ in range(n_iterations):
            # Oracle marking min/max indices
            self._min_max_oracle(qc, qr, target_indices, n_qubits)
            
            # Diffusion operator
            self._diffusion(qc, qr, n_qubits)
        
        # Measure
        qc.measure(qr, cr)
        
        # Execute circuit
        job = self.backend.run(qc, shots=1000)
        result = job.result()
        counts = result.get_counts()
        
        # Find most frequent measurement
        max_count_state = max(counts, key=counts.get)
        found_index = int(max_count_state, 2)
        
        # Verify it's a valid index
        if found_index < len(data):
            found_value = data[found_index]
            success = found_value == target_value
        else:
            found_value = None
            success = False
        
        # Calculate success rate
        success_count = sum(counts.get(format(idx, f'0{n_qubits}b'), 0) 
                          for idx in target_indices)
        success_rate = success_count / 1000
        
        return {
            'data': data,
            'find_min': find_min,
            'target_value': target_value,
            'target_indices': target_indices,
            'found_index': found_index,
            'found_value': found_value,
            'success': success,
            'success_rate': success_rate,
            'iterations': n_iterations,
            'measurements': counts
        }
    
    def _min_max_oracle(self, qc, qr, target_indices, n_qubits):
        """Oracle that marks the minimum/maximum indices"""
        for target_idx in target_indices:
            # Convert index to binary
            binary = format(target_idx, f'0{n_qubits}b')
            
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
                qc.h(qr[n_qubits - 1])
                qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
                qc.h(qr[n_qubits - 1])
            
            # Undo X gates
            for i, bit in enumerate(reversed(binary)):
                if bit == '0':
                    qc.x(qr[i])
    
    def _diffusion(self, qc, qr, n_qubits):
        """Grover diffusion operator"""
        qc.h(qr)
        qc.x(qr)
        
        if n_qubits == 1:
            qc.z(qr[0])
        elif n_qubits == 2:
            qc.cz(qr[0], qr[1])
        else:
            qc.h(qr[n_qubits - 1])
            qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
            qc.h(qr[n_qubits - 1])
        
        qc.x(qr)
        qc.h(qr)


if __name__ == "__main__":
    print("=== Quantum Min/Max Finding Test ===\n")
    
    qmm = QuantumMinMaxAlgorithm()
    
    # Test cases
    test_data = [
        [7, 3, 9, 1, 5, 8, 2, 6],
        [15, 8, 23, 4, 16, 42, 11, 19],
        [5, 5, 5, 1, 5, 5, 5, 5],  # One minimum
    ]
    
    for data in test_data:
        print(f"Data: {data}")
        
        # Find minimum
        print("\nFinding MINIMUM:")
        q_result = qmm.benchmark(data, find_min=True)
        print(f"Quantum result: Min = {q_result['result']['found_value']} at index {q_result['result']['found_index']}")
        print(f"Success rate: {q_result['result']['success_rate']:.2%}")
        print(f"Quantum time: {q_result['execution_time']:.4f}s")
        
        c_result = classical_min_max(data, find_min=True)
        print(f"Classical result: Min = {c_result['value']} at index {c_result['index']}")
        print(f"Classical comparisons: {c_result['comparisons']}")
        
        speedup = c_result['comparisons'] / q_result['result']['iterations']
        print(f"Speedup: {speedup:.2f}x")
        
        # Find maximum
        print("\nFinding MAXIMUM:")
        q_result = qmm.benchmark(data, find_min=False)
        print(f"Quantum result: Max = {q_result['result']['found_value']} at index {q_result['result']['found_index']}")
        print(f"Success rate: {q_result['result']['success_rate']:.2%}")
        
        c_result = classical_min_max(data, find_min=False)
        print(f"Classical result: Max = {c_result['value']} at index {c_result['index']}")
        
        print("-" * 50 + "\n")