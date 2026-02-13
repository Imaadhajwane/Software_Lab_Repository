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

def measure_performance(func, *args, **kwargs):
    """
    Measures:
        - Execution time
        - CPU usage (if psutil available)
        - Peak memory usage
        - Result
    """

    process = psutil.Process(os.getpid()) if PSUTIL_AVAILABLE else None

    # Warm up CPU measurement
    if PSUTIL_AVAILABLE:
        process.cpu_percent(interval=None)

    tracemalloc.start()

    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    execution_time = end_time - start_time

    cpu_usage = process.cpu_percent(
        interval=None) if PSUTIL_AVAILABLE else None

    return {
        "result": result,
        "execution_time_sec": round(execution_time, 6),
        "cpu_usage_percent": cpu_usage,
        "peak_memory_mb": round(peak / (1024 ** 2), 6)
    }


# ============================================================
# SAMPLE TEST CASES
# ============================================================

def test_factorization():
    return shor_factor(15)


def test_grover():
    return grover_search(n=3, target_index=5)


def test_deutsch_jozsa():
    def balanced_function(x):
        return x % 2
    return deutsch_jozsa(balanced_function, n=3)


def test_phase_estimation():
    U = np.array([[1, 0], [0, np.exp(2j * np.pi * 0.25)]])
    eigenvector = np.array([0, 1])
    return phase_estimation(U, eigenvector, t=5)


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
    leaf1 = DummyNode(3)
    leaf2 = DummyNode(5)
    leaf3 = DummyNode(2)
    leaf4 = DummyNode(9)

    node1 = DummyNode(children=[leaf1, leaf2])
    node2 = DummyNode(children=[leaf3, leaf4])

    root = DummyNode(children=[node1, node2])

    return minimax(
        root,
        depth=3,
        alpha=float('-inf'),
        beta=float('inf'),
        maximizing=True
    )


# ============================================================
# MAIN CONTROLLER
# ============================================================

def run_all():
    algorithms = {
        "Shor Factorization": test_factorization,
        "Grover Search": test_grover,
        "Deutsch-Jozsa": test_deutsch_jozsa,
        "Minimax": test_minimax,
        "Phase Estimation": test_phase_estimation
    }

    results = []

    print("\n===== ALGORITHM BENCHMARK RESULTS =====\n")

    for name, func in algorithms.items():
        metrics = measure_performance(func)

        results.append([
            name,
            metrics["result"],
            metrics["execution_time_sec"],
            metrics["cpu_usage_percent"],
            metrics["peak_memory_mb"]
        ])

    headers = [
        "Algorithm",
        "Result",
        "Execution Time (sec)",
        "CPU Usage (%)",
        "Peak Memory (MB)"
    ]

    if TABULATE_AVAILABLE:
        print(tabulate(results, headers=headers, tablefmt="grid"))
    else:
        # Manual fallback formatting
        print("{:<20} {:<15} {:<20} {:<15} {:<15}".format(*headers))
        print("-" * 90)
        for row in results:
            print("{:<20} {:<15} {:<20} {:<15} {:<15}".format(*row))

    print("\n========================================\n")

    return results



if __name__ == "__main__":
    run_all()
