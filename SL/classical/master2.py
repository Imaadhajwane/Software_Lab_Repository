# ============================================================
# algorithm_runner.py
# Unified Benchmark Runner for All Algorithms
# ============================================================

import time
import os
import tracemalloc
import numpy as np

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

try:
    from tabulate import tabulate
    TABULATE_AVAILABLE = True
except ImportError:
    TABULATE_AVAILABLE = False


from factorization import shor_factor
from search import grover_search
from deutsuch import deutsch_jozsa
from minmax import minimax
from phase import phase_estimation


# ============================================================
# PERFORMANCE MEASUREMENT
# ============================================================

def measure_average_performance(func, runs=100, *args, **kwargs):
    """
    Runs the function multiple times and averages:
        - Execution time
        - Peak memory
    """

    total_time = 0
    total_peak_memory = 0
    final_result = None

    for _ in range(runs):
        tracemalloc.start()

        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        total_time += (end_time - start_time)
        total_peak_memory += peak
        final_result = result

    avg_time = total_time / runs
    avg_memory = total_peak_memory / runs

    return {
        "result": final_result,
        "avg_execution_time_sec": round(avg_time, 6),
        "avg_peak_memory_mb": round(avg_memory / (1024 ** 2), 6)
    }


# ============================================================
# SAMPLE TEST CASES
# ============================================================

def test_factorization():
    return shor_factor(21)   # Try 21 or 35


def test_grover():
    return grover_search(n=6, target_index=45)  # 2^6 = 64 space


def test_deutsch_jozsa():
    def balanced_function(x):
        return x % 2
    return deutsch_jozsa(balanced_function, n=3)


def test_phase_estimation():
    U = np.array([[1, 0], [0, np.exp(2j * np.pi * 0.25)]])
    eigenvector = np.array([0, 1])
    return phase_estimation(U, eigenvector, t=7)   # Increased precision


# ------------------------------------------------------------
# Dummy Game Tree for Minimax
# ------------------------------------------------------------

class DummyNode:
    def __init__(self, value=None, children=None):
        self.value = value
        self.child_nodes = children or []

    def is_terminal(self):
        return len(self.child_nodes) == 0

    def evaluate(self):
        return self.value

    def children(self):
        return self.child_nodes


def test_minimax():
    leaves = [DummyNode(i) for i in [3, 5, 2, 9, 12, 5, 23, 23]]

    level2 = [
        DummyNode(children=[leaves[0], leaves[1]]),
        DummyNode(children=[leaves[2], leaves[3]]),
        DummyNode(children=[leaves[4], leaves[5]]),
        DummyNode(children=[leaves[6], leaves[7]])
    ]

    level1 = [
        DummyNode(children=[level2[0], level2[1]]),
        DummyNode(children=[level2[2], level2[3]])
    ]

    root = DummyNode(children=level1)

    return minimax(
        root,
        depth=4,
        alpha=float('-inf'),
        beta=float('inf'),
        maximizing=True
    )


# ============================================================
# MAIN CONTROLLER
# ============================================================

def run_all():
    algorithms = {
        "Shor Factorization (N=21)": test_factorization,
        "Grover Search (n=6)": test_grover,
        "Deutsch-Jozsa": test_deutsch_jozsa,
        "Minimax (Depth=4)": test_minimax,
        "Phase Estimation (t=7)": test_phase_estimation
    }

    results = []

    print("\n===== ADVANCED BENCHMARK (100 RUN AVEROAGE) =====\n")

    for name, func in algorithms.items():
        print(f"Running {name} 100 times...")
        metrics = measure_average_performance(func, runs=100)

        results.append([
            name,
            metrics["result"],
            metrics["avg_execution_time_sec"],
            metrics["avg_peak_memory_mb"]
        ])

    headers = [
        "Algorithm",
        "Final Result",
        "Avg Execution Time (sec)",
        "Avg Peak Memory (MB)"
    ]

    if TABULATE_AVAILABLE:
        print(tabulate(results, headers=headers, tablefmt="grid"))
    else:
        print("{:<30} {:<15} {:<25} {:<20}".format(*headers))
        print("-" * 100)
        for row in results:
            print("{:<30} {:<15} {:<25} {:<20}".format(*row))

    print("\n===============================================\n")

    return results



if __name__ == "__main__":
    run_all()
