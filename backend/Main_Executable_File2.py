"""
Dynamic Dataset Generator and Algorithm Executor
Enhanced with research-grade performance metrics
"""

# Standard libraries
import json
import time
import os
import psutil
from datetime import datetime
from typing import Dict, Any, Callable

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


# ================= PERFORMANCE MEASUREMENT CORE ================= #

def measure(func: Callable, *args, repeat: int = 3, **kwargs) -> (Any, Dict):
    """
    Measures wall time, CPU time, CPU %, memory usage.
    Runs multiple times for stability.
    """
    process = psutil.Process(os.getpid())

    wall_times = []
    cpu_times = []
    mem_deltas = []
    result = None

    for _ in range(repeat):

        mem_before = process.memory_info().rss
        cpu_before = process.cpu_times()
        cpu_percent_before = psutil.cpu_percent(interval=None)

        start = time.perf_counter()

        result = func(*args, **kwargs)

        end = time.perf_counter()

        cpu_after = process.cpu_times()
        mem_after = process.memory_info().rss
        cpu_percent_after = psutil.cpu_percent(interval=None)

        wall_times.append(end - start)

        cpu_used = (
            (cpu_after.user - cpu_before.user)
            + (cpu_after.system - cpu_before.system)
        )

        cpu_times.append(cpu_used)
        mem_deltas.append((mem_after - mem_before) / (1024 * 1024))

    avg_wall = sum(wall_times) / repeat
    variance = sum((t - avg_wall) ** 2 for t in wall_times) / repeat

    metrics = {
        "wall_time_avg": avg_wall,
        "wall_time_variance": variance,
        "cpu_time_avg": sum(cpu_times) / repeat,
        "memory_mb_avg": sum(mem_deltas) / repeat,
        "repeat_runs": repeat
    }

    return result, metrics


# ================= ALGORITHM RUNNER ================= #

class AlgorithmRunner:
    """Runs all algorithms on dynamically generated data with full metrics"""

    def __init__(self, datasets: Dict):
        self.datasets = datasets
        self.results = {}

    def run_all_algorithms(self):
        print("\n" + "=" * 80)
        print("RUNNING ALL ALGORITHMS ON DYNAMIC DATA (WITH METRICS)")
        print("=" * 80)

        self.run_shor()
        self.run_grover()
        self.run_deutsch_jozsa()
        self.run_min_max()
        self.run_phase_estimation()

        self.print_summary()
        return self.results

    # ---------------- SHOR ---------------- #

    def run_shor(self):
        print("\n" + "=" * 80)
        print("TEST 1: SHOR'S ALGORITHM")
        print("=" * 80)

        shor = ShorAlgorithm()
        results = []

        for N in self.datasets['shor']:
            print(f"\nFactoring N = {N}")
            print("-" * 40)

            q_result, q_metrics = measure(shor.benchmark, N)
            c_result, c_metrics = measure(classical_factorization, N)

            print(f"Quantum result: {q_result['result']}")
            print(f"Quantum time: {q_metrics['wall_time_avg']:.6f}s")

            print(f"Classical result: {c_result}")
            print(f"Classical time: {c_metrics['wall_time_avg']:.6f}s")

            speedup = c_metrics['wall_time_avg'] / \
                max(q_metrics['wall_time_avg'], 1e-9)

            results.append({
                "N": N,
                "quantum": q_result,
                "classical": c_result,
                "metrics": {
                    "quantum": q_metrics,
                    "classical": c_metrics,
                    "time_speedup": speedup
                }
            })

        self.results['shor'] = results

    # ---------------- GROVER ---------------- #

    def run_grover(self):
        print("\n" + "=" * 80)
        print("TEST 2: GROVER'S ALGORITHM")
        print("=" * 80)

        grover = GroverAlgorithm()
        results = []

        for marked_items, space_size, description in self.datasets['grover']:
            print(f"\n{description}")
            print("-" * 40)

            q_result, q_metrics = measure(
                grover.benchmark, marked_items, space_size)
            c_result, c_metrics = measure(
                classical_search, marked_items, space_size)

            iterations = q_result['result'].get('iterations', 1) or 1
            speedup = c_metrics['wall_time_avg'] / \
                max(q_metrics['wall_time_avg'], 1e-9)

            print(f"Quantum success: {q_result['result']['success_rate']:.2%}")
            print(f"Speedup: {speedup:.2f}x")

            results.append({
                "space_size": space_size,
                "marked_items": marked_items,
                "quantum": q_result,
                "classical": c_result,
                "metrics": {
                    "quantum": q_metrics,
                    "classical": c_metrics,
                    "time_speedup": speedup
                }
            })

        self.results['grover'] = results

    # ---------------- DEUTSCH JOZSA ---------------- #

    def run_deutsch_jozsa(self):
        print("\n" + "=" * 80)
        print("TEST 3: DEUTSCH-JOZSA")
        print("=" * 80)

        dj = DeutschJozsaAlgorithm()
        results = []

        for n_qubits, func_type, description in self.datasets['deutsch_jozsa']:
            print(f"\n{description}")
            print("-" * 40)

            q_result, q_metrics = measure(dj.benchmark, n_qubits, func_type)
            c_result, c_metrics = measure(
                classical_deutsch_jozsa, n_qubits, func_type)

            speedup = c_metrics['wall_time_avg'] / \
                max(q_metrics['wall_time_avg'], 1e-9)

            results.append({
                "n_qubits": n_qubits,
                "function_type": func_type,
                "quantum": q_result,
                "classical": c_result,
                "metrics": {
                    "quantum": q_metrics,
                    "classical": c_metrics,
                    "time_speedup": speedup
                }
            })

        self.results['deutsch_jozsa'] = results

    # ---------------- MIN MAX ---------------- #

    def run_min_max(self):
        print("\n" + "=" * 80)
        print("TEST 4: QUANTUM MIN/MAX")
        print("=" * 80)

        qmm = QuantumMinMaxAlgorithm()
        results = []

        for data, description in self.datasets['min_max']:
            print(f"\n{description}")
            print("-" * 40)

            q_result, q_metrics = measure(qmm.benchmark, data, True)
            c_result, c_metrics = measure(classical_min_max, data, True)

            speedup = c_metrics['wall_time_avg'] / \
                max(q_metrics['wall_time_avg'], 1e-9)

            results.append({
                "data_size": len(data),
                "quantum": q_result,
                "classical": c_result,
                "metrics": {
                    "quantum": q_metrics,
                    "classical": c_metrics,
                    "time_speedup": speedup
                }
            })

        self.results['min_max'] = results

    # ---------------- PHASE ESTIMATION ---------------- #

    def run_phase_estimation(self):
        print("\n" + "=" * 80)
        print("TEST 5: PHASE ESTIMATION")
        print("=" * 80)

        qpe = QuantumPhaseEstimation()
        results = []

        for phase, n_qubits, description in self.datasets['phase_estimation']:
            print(f"\n{description}")
            print("-" * 40)

            q_result, q_metrics = measure(qpe.benchmark, phase, n_qubits)
            c_result, c_metrics = measure(
                classical_phase_estimation, phase, 100)

            speedup = c_metrics['wall_time_avg'] / \
                max(q_metrics['wall_time_avg'], 1e-9)

            results.append({
                "phase": phase,
                "n_qubits": n_qubits,
                "quantum": q_result,
                "classical": c_result,
                "metrics": {
                    "quantum": q_metrics,
                    "classical": c_metrics,
                    "time_speedup": speedup
                }
            })

        self.results['phase_estimation'] = results

    # ---------------- SUMMARY ---------------- #

    def print_summary(self):
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)

        for algo, runs in self.results.items():
            speeds = [r["metrics"]["time_speedup"] for r in runs]
            avg_speed = sum(speeds) / len(speeds)
            print(f"{algo.upper()} avg speedup: {avg_speed:.2f}x")

        print("=" * 80)


# ================= MAIN ================= #

def main():
    import sys

    seed = None
    if len(sys.argv) > 1:
        try:
            seed = int(sys.argv[1])
            print(f"Using seed: {seed}")
        except ValueError:
            pass

    generator = DatasetGenerator(seed=seed)
    generator.generate_all_datasets()

    output_dir = DatasetGenerator.get_output_dir()
    dataset_file = f"{output_dir}/datasets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(dataset_file, "w") as f:
        json.dump(generator.datasets, f, indent=2)

    print(f"📁 Datasets saved to: {dataset_file}\n")

    runner = AlgorithmRunner(generator.datasets)
    results = runner.run_all_algorithms()

    os.makedirs("results", exist_ok=True)

    results_file = f"results/dynamic_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(results_file, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "seed": seed,
            "datasets": generator.datasets,
            "results": results
        }, f, indent=2, default=str)


    print(f"\n📁 Results saved to: {results_file}")


if __name__ == "__main__":
    main()
