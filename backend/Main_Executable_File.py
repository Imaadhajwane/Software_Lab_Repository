"""
Dynamic Dataset Generator and Algorithm Executor
Automatically generates test data and runs all quantum & classical algorithms
"""
# Standard libraries
import json
from datetime import datetime
from typing import Dict

# Import dataset generator
from dynamic.data_generator import DatasetGenerator

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


class AlgorithmRunner:
    """Runs all algorithms on dynamically generated data"""
    
    def __init__(self, datasets: Dict):
        self.datasets = datasets
        self.results = {}
    
    def run_all_algorithms(self):
        """Execute all algorithms with generated datasets"""
        print("\n" + "=" * 80)
        print("RUNNING ALL ALGORITHMS ON DYNAMIC DATA")
        print("=" * 80)
        print()
        
        self.run_shor()
        self.run_grover()
        self.run_deutsch_jozsa()
        self.run_min_max()
        self.run_phase_estimation()
        
        self.print_summary()
        
        return self.results
    
    def run_shor(self):
        """Run Shor's algorithm on generated data"""
        print("\n" + "=" * 80)
        print("TEST 1: SHOR'S ALGORITHM - DYNAMIC DATA")
        print("=" * 80)
        
        shor = ShorAlgorithm()
        results = []
        
        for N in self.datasets['shor']:
            print(f"\nFactoring N = {N}")
            print("-" * 40)
            
            # Quantum
            q_result = shor.benchmark(N)
            print(f"Quantum: {q_result['result']}")
            print(f"Time: {q_result['execution_time']:.6f}s")
            
            # Classical
            c_result = classical_factorization(N)
            print(f"Classical: {c_result}")
            
            results.append({
                'N': N,
                'quantum': q_result['result'],
                'classical': c_result
            })
        
        self.results['shor'] = results
    
    def run_grover(self):
        """Run Grover's algorithm on generated data"""
        print("\n" + "=" * 80)
        print("TEST 2: GROVER'S ALGORITHM - DYNAMIC DATA")
        print("=" * 80)
        
        grover = GroverAlgorithm()
        results = []
        
        for marked_items, space_size, description in self.datasets['grover']:
            print(f"\n{description}")
            print(f"Marked: {marked_items}, Space: {space_size}")
            print("-" * 40)
            
            # Quantum
            q_result = grover.benchmark(marked_items, space_size)
            print(f"Quantum: Found {q_result['result']['found_items']}")
            print(f"Success rate: {q_result['result']['success_rate']:.2%}")
            print(f"Iterations: {q_result['result']['iterations']}")
            
            # Classical
            c_result = classical_search(marked_items, space_size)
            print(f"Classical: {c_result['comparisons']} comparisons")
            
            iterations = q_result['result'].get('iterations', 1) or 1
            speedup = c_result['average_comparisons'] / iterations
            print(f"Speedup: {speedup:.2f}x")
            
            results.append({
                'marked_items': marked_items,
                'space_size': space_size,
                'success_rate': q_result['result']['success_rate'],
                'speedup': speedup
            })
        
        self.results['grover'] = results
    
    def run_deutsch_jozsa(self):
        """Run Deutsch-Jozsa algorithm on generated data"""
        print("\n" + "=" * 80)
        print("TEST 3: DEUTSCH-JOZSA ALGORITHM - DYNAMIC DATA")
        print("=" * 80)
        
        dj = DeutschJozsaAlgorithm()
        results = []
        
        for n_qubits, func_type, description in self.datasets['deutsch_jozsa']:
            print(f"\n{description}")
            print("-" * 40)
            
            # Quantum
            q_result = dj.benchmark(n_qubits, func_type)
            print(f"Quantum: Detected '{q_result['result']['detected_type']}'")
            print(f"Correct: {q_result['result']['correct']}")
            print(f"Queries: {q_result['result']['queries']}")
            
            # Classical
            c_result = classical_deutsch_jozsa(n_qubits, func_type)
            print(f"Classical: {c_result['queries']} queries")
            
            speedup = c_result['queries'] / q_result['result']['queries']
            print(f"Speedup: {speedup:.0f}x")
            
            results.append({
                'n_qubits': n_qubits,
                'function_type': func_type,
                'correct': q_result['result']['correct'],
                'speedup': speedup
            })
        
        self.results['deutsch_jozsa'] = results
    
    def run_min_max(self):
        """Run min/max finding on generated data"""
        print("\n" + "=" * 80)
        print("TEST 4: QUANTUM MIN/MAX FINDING - DYNAMIC DATA")
        print("=" * 80)
        
        qmm = QuantumMinMaxAlgorithm()
        results = []
        
        for data, description in self.datasets['min_max']:
            print(f"\n{description}")
            print(f"Data: {data}")
            print("-" * 40)
            
            # Quantum
            q_result = qmm.benchmark(data, find_min=True)
            print(f"Quantum MIN: {q_result['result']['found_value']} at index {q_result['result']['found_index']}")
            print(f"Success rate: {q_result['result']['success_rate']:.2%}")
            
            # Classical
            c_result = classical_min_max(data, find_min=True)
            print(f"Classical MIN: {c_result['value']} at index {c_result['index']}")
            print(f"Comparisons: {c_result['comparisons']}")
            
            iterations = q_result['result'].get('iterations', 1) or 1
            speedup = c_result['comparisons'] / iterations
            print(f"Speedup: {speedup:.2f}x")
            
            results.append({
                'data': data,
                'min_value': q_result['result']['found_value'],
                'success_rate': q_result['result']['success_rate'],
                'speedup': speedup
            })
        
        self.results['min_max'] = results
    
    def run_phase_estimation(self):
        """Run phase estimation on generated data"""
        print("\n" + "=" * 80)
        print("TEST 5: QUANTUM PHASE ESTIMATION - DYNAMIC DATA")
        print("=" * 80)
        
        qpe = QuantumPhaseEstimation()
        results = []
        
        for phase, n_qubits, description in self.datasets['phase_estimation']:
            print(f"\n{description}")
            print("-" * 40)
            
            # Quantum
            q_result = qpe.benchmark(phase, n_qubits)
            print(f"Quantum: Estimated {q_result['result']['estimated_phase']:.6f}")
            print(f"Error: {q_result['result']['error']:.6f}")
            print(f"Success: {q_result['result']['success_probability']:.2%}")
            
            # Classical
            c_result = classical_phase_estimation(phase, n_samples=100)
            print(f"Classical: Estimated {c_result['estimated_phase']:.6f}")
            print(f"Error: {c_result['error']:.6f}")
            
            results.append({
                'phase': phase,
                'n_qubits': n_qubits,
                'quantum_error': q_result['result']['error'],
                'success_probability': q_result['result']['success_probability']
            })
        
        self.results['phase_estimation'] = results
    
    def print_summary(self):
        """Print summary of all results"""
        print("\n" + "=" * 80)
        print("SUMMARY - DYNAMIC DATA RESULTS")
        print("=" * 80)
        print()
        
        # Shor's
        if 'shor' in self.results:
            successful = sum(1 for r in self.results['shor'] if r['quantum'].get('factors'))
            total = len(self.results['shor'])
            print(f"Shor's Algorithm: {successful}/{total} successful factorizations")
        
        # Grover's
        if 'grover' in self.results:
            avg_success = sum(r['success_rate'] for r in self.results['grover']) / len(self.results['grover'])
            avg_speedup = sum(r['speedup'] for r in self.results['grover']) / len(self.results['grover'])
            print(f"Grover's Algorithm: {avg_success:.1%} avg success, {avg_speedup:.2f}x avg speedup")
        
        # Deutsch-Jozsa
        if 'deutsch_jozsa' in self.results:
            correct = sum(1 for r in self.results['deutsch_jozsa'] if r['correct'])
            total = len(self.results['deutsch_jozsa'])
            avg_speedup = sum(r['speedup'] for r in self.results['deutsch_jozsa']) / total
            print(f"Deutsch-Jozsa: {correct}/{total} correct, {avg_speedup:.0f}x avg speedup")
        
        # Min/Max
        if 'min_max' in self.results:
            avg_success = sum(r['success_rate'] for r in self.results['min_max']) / len(self.results['min_max'])
            avg_speedup = sum(r['speedup'] for r in self.results['min_max']) / len(self.results['min_max'])
            print(f"Min/Max Finding: {avg_success:.1%} avg success, {avg_speedup:.2f}x avg speedup")
        
        # Phase Estimation
        if 'phase_estimation' in self.results:
            avg_error = sum(r['quantum_error'] for r in self.results['phase_estimation']) / len(self.results['phase_estimation'])
            avg_success = sum(r['success_probability'] for r in self.results['phase_estimation']) / len(self.results['phase_estimation'])
            print(f"Phase Estimation: {avg_error:.6f} avg error, {avg_success:.1%} avg success")
        
        print("\n" + "=" * 80)
        print("All dynamic tests completed!")
        print("=" * 80)


def main():
    """Main execution function"""
    import sys
    
    # Allow optional seed from command line
    seed = None
    if len(sys.argv) > 1:
        try:
            seed = int(sys.argv[1])
            print(f"Using seed: {seed}")
        except ValueError:
            print("Invalid seed, using random")
    
    # Generate datasets
    generator = DatasetGenerator(seed=seed)
    generator.generate_all_datasets()
    
    # Save generated datasets
    output_dir = DatasetGenerator.get_output_dir()
    dataset_file = f"{output_dir}/datasets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(dataset_file, 'w') as f:
        json.dump(generator.datasets, f, indent=2)
    print(f"📁 Datasets saved to: {dataset_file}\n")
    
    # Run algorithms
    runner = AlgorithmRunner(generator.datasets)
    results = runner.run_all_algorithms()
    
    # Save results
    results_file = f"results/dynamic_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    result_data = {
        'timestamp': datetime.now().isoformat(),
        'seed': seed,
        'datasets': generator.datasets,
        'results': results
    }
    
    with open(results_file, 'w') as f:
        json.dump(result_data, f, indent=2)
    print(f"\n📁 Results saved to: {results_file}")


if __name__ == "__main__":
    import os
    
    # Create results directory
    os.makedirs('results', exist_ok=True)
    
    # Run with dynamic data
    main()