"""
Quantum Phase Estimation (QPE) Algorithm
Estimates the eigenvalue phase of a unitary operator
"""
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import Aer
from qiskit.circuit.library import QFT
import math
import sys
sys.path.append('..')
from base import BaseAlgorithm
from classical.phase_estimation import classical_phase_estimation


class QuantumPhaseEstimation(BaseAlgorithm):
    """Quantum Phase Estimation algorithm"""
    
    def __init__(self):
        super().__init__("Quantum Phase Estimation")
        self.backend = Aer.get_backend('qasm_simulator')
    
    def run(self, phase: float, n_counting_qubits: int = 4) -> dict:
        """
        Estimate the phase of a unitary operator U|ψ> = e^(2πiφ)|ψ>
        
        Args:
            phase: The actual phase φ to estimate (between 0 and 1)
            n_counting_qubits: Number of counting qubits (precision)
        
        Returns:
            Dictionary with estimated phase and accuracy
        """
        if n_counting_qubits > 10:
            return {'error': 'Too many qubits for simulation'}
        
        if phase < 0 or phase >= 1:
            return {'error': 'Phase must be in range [0, 1)'}
        
        # Create quantum circuit
        # Counting qubits + 1 eigenstate qubit
        qr_count = QuantumRegister(n_counting_qubits, 'counting')
        qr_eigen = QuantumRegister(1, 'eigenstate')
        cr = ClassicalRegister(n_counting_qubits, 'c')
        
        qc = QuantumCircuit(qr_count, qr_eigen, cr)
        
        # Prepare eigenstate |1>
        qc.x(qr_eigen[0])
        
        # Initialize counting qubits in superposition
        qc.h(qr_count)
        
        # Apply controlled-U operations
        # U is a phase gate: U|1> = e^(2πiφ)|1>
        for i in range(n_counting_qubits):
            power = 2 ** i
            angle = 2 * np.pi * phase * power
            qc.cp(angle, qr_count[i], qr_eigen[0])
        
        # Apply inverse QFT
        iqft_circuit = QFT(n_counting_qubits, inverse=True).decompose()
        qc.compose(iqft_circuit, qr_count, inplace=True)
        
        # Measure counting qubits
        qc.measure(qr_count, cr)
        
        # Execute circuit
        job = self.backend.run(qc, shots=2048)
        result = job.result()
        counts = result.get_counts()
        
        # Get most frequent measurement
        max_count_state = max(counts, key=counts.get)
        measured_int = int(max_count_state, 2)
        
        # Convert to estimated phase
        estimated_phase = measured_int / (2 ** n_counting_qubits)
        
        # Calculate error
        error = abs(estimated_phase - phase)
        
        # Calculate theoretical precision
        precision = 1 / (2 ** n_counting_qubits)
        
        # Success probability
        success_prob = counts[max_count_state] / 2048
        
        return {
            'actual_phase': phase,
            'estimated_phase': estimated_phase,
            'error': error,
            'precision': precision,
            'n_counting_qubits': n_counting_qubits,
            'success_probability': success_prob,
            'measured_state': max_count_state,
            'measured_int': measured_int,
            'measurements': counts,
            'circuit': qc
        }


if __name__ == "__main__":
    print("=== Quantum Phase Estimation Test ===\n")
    
    qpe = QuantumPhaseEstimation()
    
    # Test cases with different phases
    test_cases = [
        (0.25, 4),   # Phase = 1/4, 4 counting qubits
        (0.5, 4),    # Phase = 1/2
        (0.125, 5),  # Phase = 1/8, 5 counting qubits
        (0.375, 5),  # Phase = 3/8
        (0.3, 6),    # Non-dyadic phase
    ]
    
    for phase, n_qubits in test_cases:
        print(f"Estimating phase φ = {phase} with {n_qubits} counting qubits")
        
        # Quantum estimation
        q_result = qpe.benchmark(phase, n_qubits)
        print(f"Quantum result:")
        print(f"  Estimated phase: {q_result['result']['estimated_phase']:.6f}")
        print(f"  Error: {q_result['result']['error']:.6f}")
        print(f"  Precision: {q_result['result']['precision']:.6f}")
        print(f"  Success probability: {q_result['result']['success_probability']:.2%}")
        print(f"  Time: {q_result['execution_time']:.4f}s")
        
        # Classical estimation
        c_result = classical_phase_estimation(phase, n_samples=100)
        print(f"\nClassical result:")
        print(f"  Estimated phase: {c_result['estimated_phase']:.6f}")
        print(f"  Error: {c_result['error']:.6f}")
        print(f"  Precision: {c_result['precision']:.6f}")
        print(f"  Samples needed: {c_result['samples_needed']:.2e}")
        
        # Compare complexity
        quantum_complexity = n_qubits ** 2
        classical_complexity = 2 ** n_qubits
        speedup = classical_complexity / quantum_complexity
        
        print(f"\nComplexity comparison:")
        print(f"  Quantum: O(n²) ≈ {quantum_complexity}")
        print(f"  Classical: O(2ⁿ) ≈ {classical_complexity}")
        print(f"  Speedup: {speedup:.2f}x")
        print("-" * 60 + "\n")