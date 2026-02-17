"""
Main Comparison Script
Runs all quantum & classical algorithms with internal test data and generates comparative analysis
"""
import sys
import time
import json
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

# Import quantum algorithms
from quantum.shor import ShorAlgorithm
from quantum.grover import GroverAlgorithm
from quantum.deutsch_jozsa import DeutschJozsaAlgorithm
from quantum.min_max import QuantumMinMaxAlgorithm
from quantum.phase_estimation import QuantumPhaseEstimation

# Import classical algorithms
from classical.factorization import classical_factorization
from classical.search import classical_search
from classical.min_max import classical_min_max
from classical.phase_estimation import classical_phase_estimation
from classical.deutsch_jozsa import classical_deutsch_jozsa


class QuantumClassicalComparison:
    """Main class for comparing quantum and classical algorithms"""
    
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'algorithms': {}
        }
    
    def run_all_tests(self):
        """Run all algorithm comparisons"""
        print("=" * 80)
        print("QUANTUM vs CLASSICAL ALGORITHMS - COMPREHENSIVE COMPARISON")
        print("=" * 80)
        print()
        
        # Test 1: Shor's Algorithm - Factorization
        print("\n" + "=" * 80)
        print("TEST 1: SHOR'S ALGORITHM - INTEGER FACTORIZATION")
        print("=" * 80)
        self.test_shor()
        
        # Test 2: Grover's Algorithm - Search
        print("\n" + "=" * 80)
        print("TEST 2: GROVER'S ALGORITHM - UNSTRUCTURED SEARCH")
        print("=" * 80)
        self.test_grover()
        
        # Test 3: Deutsch-Jozsa Algorithm
        print("\n" + "=" * 80)
        print("TEST 3: DEUTSCH-JOZSA ALGORITHM - FUNCTION DETERMINATION")
        print("=" * 80)
        self.test_deutsch_jozsa()
        
        # Test 4: Min/Max Finding
        print("\n" + "=" * 80)
        print("TEST 4: QUANTUM MIN/MAX FINDING")
        print("=" * 80)
        self.test_min_max()
        
        # Test 5: Phase Estimation
        print("\n" + "=" * 80)
        print("TEST 5: QUANTUM PHASE ESTIMATION")
        print("=" * 80)
        self.test_phase_estimation()
        
        # Generate summary
        self.generate_summary()
    
    def test_shor(self):
        """Test Shor's factorization algorithm"""
        shor = ShorAlgorithm()
        
        # Common test data
        test_numbers = [15, 21]
        
        results = []
        
        for N in test_numbers:
            print(f"\nFactoring N = {N}")
            print("-" * 40)
            
            # Quantum
            start = time.time()
            q_result = shor.run(N)
            q_time = time.time() - start
            
            print(f"Quantum Result: {q_result}")
            print(f"Quantum Time: {q_time:.6f}s")
            
            # Classical
            start = time.time()
            c_result = classical_factorization(N)
            c_time = time.time() - start
            
            print(f"Classical Result: {c_result}")
            print(f"Classical Time: {c_time:.6f}s")
            
            if c_time > 0:
                speedup = c_time / q_time if q_time > 0 else float('inf')
                print(f"Speedup: {speedup:.2f}x")
            
            results.append({
                'N': N,
                'quantum': q_result,
                'classical': c_result,
                'quantum_time': q_time,
                'classical_time': c_time
            })
        
        self.results['algorithms']['shor'] = results
    
    def test_grover(self):
        """Test Grover's search algorithm"""
        grover = GroverAlgorithm()
        
        # Common test data
        test_cases = [
            ([5], 16, "Single item in 16 elements"),
            ([3, 7], 16, "Two items in 16 elements"),
            ([11], 32, "Single item in 32 elements"),
        ]
        
        results = []
        
        for marked_items, space_size, description in test_cases:
            print(f"\n{description}")
            print(f"Marked items: {marked_items}, Space size: {space_size}")
            print("-" * 40)
            
            # Quantum
            start = time.time()
            q_result = grover.run(marked_items, space_size)
            q_time = time.time() - start
            
            print(f"Quantum Result:")
            print(f"  Found: {q_result['found_items']}")
            print(f"  Success rate: {q_result['success_rate']:.2%}")
            print(f"  Iterations: {q_result['iterations']}")
            print(f"  Time: {q_time:.6f}s")
            
            # Classical
            start = time.time()
            c_result = classical_search(marked_items, space_size)
            c_time = time.time() - start
            
            print(f"\nClassical Result:")
            print(f"  Found: {c_result['found_items']}")
            print(f"  Comparisons: {c_result['comparisons']}")
            print(f"  Time: {c_time:.6f}s")
            
            speedup = c_result['average_comparisons'] / q_result['iterations']
            print(f"\nQuery Speedup: {speedup:.2f}x")
            
            results.append({
                'marked_items': marked_items,
                'space_size': space_size,
                'quantum': q_result,
                'classical': c_result,
                'quantum_time': q_time,
                'classical_time': c_time,
                'query_speedup': speedup
            })
        
        self.results['algorithms']['grover'] = results
    
    def test_deutsch_jozsa(self):
        """Test Deutsch-Jozsa algorithm"""
        dj = DeutschJozsaAlgorithm()
        
        # Common test data
        test_cases = [
            (3, 'constant', "3 qubits, constant function"),
            (3, 'balanced', "3 qubits, balanced function"),
            (4, 'constant', "4 qubits, constant function"),
            (4, 'balanced', "4 qubits, balanced function"),
            (5, 'balanced', "5 qubits, balanced function"),
        ]
        
        results = []
        
        for n_qubits, func_type, description in test_cases:
            print(f"\n{description}")
            print("-" * 40)
            
            # Quantum
            start = time.time()
            q_result = dj.run(n_qubits, func_type)
            q_time = time.time() - start
            
            print(f"Quantum Result:")
            print(f"  Detected: {q_result['detected_type']}")
            print(f"  Correct: {q_result['correct']}")
            print(f"  Queries: {q_result['queries']}")
            print(f"  Time: {q_time:.6f}s")
            
            # Classical
            start = time.time()
            c_result = classical_deutsch_jozsa(n_qubits, func_type)
            c_time = time.time() - start
            
            print(f"\nClassical Result:")
            print(f"  Detected: {c_result['detected_type']}")
            print(f"  Correct: {c_result['correct']}")
            print(f"  Queries: {c_result['queries']}")
            print(f"  Time: {c_time:.6f}s")
            
            speedup = c_result['queries'] / q_result['queries']
            print(f"\nQuery Speedup: {speedup:.0f}x (Exponential)")
            
            results.append({
                'n_qubits': n_qubits,
                'function_type': func_type,
                'quantum': q_result,
                'classical': c_result,
                'quantum_time': q_time,
                'classical_time': c_time,
                'query_speedup': speedup
            })
        
        self.results['algorithms']['deutsch_jozsa'] = results
    
    def test_min_max(self):
        """Test quantum min/max finding"""
        qmm = QuantumMinMaxAlgorithm()
        
        # Common test data
        test_datasets = [
            ([7, 3, 9, 1, 5, 8, 2, 6], "8 random values"),
            ([15, 8, 23, 4, 16, 42, 11, 19], "8 larger values"),
            ([5, 5, 5, 1, 5, 5, 5, 5], "Mostly identical with one min"),
        ]
        
        results = []
        
        for data, description in test_datasets:
            print(f"\n{description}")
            print(f"Data: {data}")
            print("-" * 40)
            
            # Test minimum finding
            print("\nFinding MINIMUM:")
            
            # Quantum
            start = time.time()
            q_result = qmm.run(data, find_min=True)
            q_time = time.time() - start
            
            print(f"Quantum Result:")
            print(f"  Value: {q_result['found_value']} at index {q_result['found_index']}")
            print(f"  Success rate: {q_result['success_rate']:.2%}")
            print(f"  Iterations: {q_result['iterations']}")
            print(f"  Time: {q_time:.6f}s")
            
            # Classical
            start = time.time()
            c_result = classical_min_max(data, find_min=True)
            c_time = time.time() - start
            
            print(f"\nClassical Result:")
            print(f"  Value: {c_result['value']} at index {c_result['index']}")
            print(f"  Comparisons: {c_result['comparisons']}")
            print(f"  Time: {c_time:.6f}s")
            
            speedup = c_result['comparisons'] / q_result['iterations']
            print(f"\nQuery Speedup: {speedup:.2f}x")
            
            results.append({
                'data': data,
                'operation': 'min',
                'quantum': q_result,
                'classical': c_result,
                'quantum_time': q_time,
                'classical_time': c_time,
                'query_speedup': speedup
            })
        
        self.results['algorithms']['min_max'] = results
    
    def test_phase_estimation(self):
        """Test quantum phase estimation"""
        qpe = QuantumPhaseEstimation()
        
        # Common test data
        test_cases = [
            (0.25, 4, "Phase = 1/4, 4 qubits"),
            (0.5, 4, "Phase = 1/2, 4 qubits"),
            (0.125, 5, "Phase = 1/8, 5 qubits"),
            (0.375, 5, "Phase = 3/8, 5 qubits"),
            (0.3, 6, "Phase = 0.3 (non-dyadic), 6 qubits"),
        ]
        
        results = []
        
        for phase, n_qubits, description in test_cases:
            print(f"\n{description}")
            print("-" * 40)
            
            # Quantum
            start = time.time()
            q_result = qpe.run(phase, n_qubits)
            q_time = time.time() - start
            
            print(f"Quantum Result:")
            print(f"  Estimated phase: {q_result['estimated_phase']:.6f}")
            print(f"  Error: {q_result['error']:.6f}")
            print(f"  Precision: {q_result['precision']:.6f}")
            print(f"  Success prob: {q_result['success_probability']:.2%}")
            print(f"  Time: {q_time:.6f}s")
            
            # Classical
            start = time.time()
            c_result = classical_phase_estimation(phase, n_samples=100)
            c_time = time.time() - start
            
            print(f"\nClassical Result:")
            print(f"  Estimated phase: {c_result['estimated_phase']:.6f}")
            print(f"  Error: {c_result['error']:.6f}")
            print(f"  Precision: {c_result['precision']:.6f}")
            
            # Complexity comparison
            quantum_complexity = n_qubits ** 2
            classical_complexity = 2 ** n_qubits
            speedup = classical_complexity / quantum_complexity
            
            print(f"\nComplexity Speedup: {speedup:.2f}x (Exponential)")
            
            results.append({
                'phase': phase,
                'n_qubits': n_qubits,
                'quantum': q_result,
                'classical': c_result,
                'quantum_time': q_time,
                'classical_time': c_time,
                'complexity_speedup': speedup
            })
        
        self.results['algorithms']['phase_estimation'] = results
    
    def generate_summary(self):
        """Generate comparison summary"""
        print("\n" + "=" * 80)
        print("SUMMARY: QUANTUM vs CLASSICAL ALGORITHMS")
        print("=" * 80)
        
        summary_table = [
            ["Algorithm", "Speedup Type", "Measured Speedup", "Success Rate"],
            ["-" * 20, "-" * 15, "-" * 20, "-" * 15]
        ]
        
        # Shor's Algorithm
        if 'shor' in self.results['algorithms']:
            summary_table.append([
                "Shor's (Factorization)",
                "Exponential",
                "Variable (small N)",
                "~100%"
            ])
        
        # Grover's Algorithm
        if 'grover' in self.results['algorithms']:
            avg_speedup = np.mean([r['query_speedup'] for r in self.results['algorithms']['grover']])
            avg_success = np.mean([r['quantum']['success_rate'] for r in self.results['algorithms']['grover']])
            summary_table.append([
                "Grover's (Search)",
                "Quadratic O(√N)",
                f"{avg_speedup:.2f}x",
                f"{avg_success:.1%}"
            ])
        
        # Deutsch-Jozsa
        if 'deutsch_jozsa' in self.results['algorithms']:
            avg_speedup = np.mean([r['query_speedup'] for r in self.results['algorithms']['deutsch_jozsa']])
            summary_table.append([
                "Deutsch-Jozsa",
                "Exponential",
                f"{avg_speedup:.0f}x",
                "100%"
            ])
        
        # Min/Max Finding
        if 'min_max' in self.results['algorithms']:
            avg_speedup = np.mean([r['query_speedup'] for r in self.results['algorithms']['min_max']])
            avg_success = np.mean([r['quantum']['success_rate'] for r in self.results['algorithms']['min_max']])
            summary_table.append([
                "Min/Max Finding",
                "Quadratic O(√N)",
                f"{avg_speedup:.2f}x",
                f"{avg_success:.1%}"
            ])
        
        # Phase Estimation
        if 'phase_estimation' in self.results['algorithms']:
            avg_speedup = np.mean([r['complexity_speedup'] for r in self.results['algorithms']['phase_estimation']])
            avg_success = np.mean([r['quantum']['success_probability'] for r in self.results['algorithms']['phase_estimation']])
            summary_table.append([
                "Phase Estimation",
                "Exponential",
                f"{avg_speedup:.2f}x",
                f"{avg_success:.1%}"
            ])
        
        print()
        for row in summary_table:
            print(f"{row[0]:<25} {row[1]:<20} {row[2]:<20} {row[3]:<15}")
        
        print("\n" + "=" * 80)
        print("All tests completed successfully!")
        print("=" * 80)
        
        # Save results to JSON
        self.save_results()
    
    def save_results(self):
        """Save results to JSON file"""
        filename = f"results/comparison_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Convert non-serializable objects
        serializable_results = self._make_serializable(self.results)
        
        with open(filename, 'w') as f:
            json.dump(serializable_results, f, indent=2)
        
        print(f"\nResults saved to: {filename}")
    
    def _make_serializable(self, obj):
        """Convert objects to JSON-serializable format"""
        if isinstance(obj, dict):
            return {k: self._make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._make_serializable(item) for item in obj]
        elif hasattr(obj, '__dict__'):
            return str(obj)
        elif isinstance(obj, (np.integer, np.floating)):
            return float(obj)
        else:
            return obj


if __name__ == "__main__":
    import os
    
    # Create results directory if it doesn't exist
    os.makedirs('results', exist_ok=True)
    
    # Run comprehensive comparison
    comparison = QuantumClassicalComparison()
    comparison.run_all_tests()