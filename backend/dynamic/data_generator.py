"""Data generator for quantum algorithms
Generates random test data for Shor's, Grover's, Deutsch-Jozsa, Min/Max, and Phase Estimation algorithms        
"""
import random
import math
import os
from datetime import datetime   
from typing import List, Tuple

class DatasetGenerator:
    """Generates random test data for all quantum algorithms"""
    
    OUTPUT_DIR = 'generated_datasets'
    
    def __init__(self, seed: int = None):
        """
        Initialize dataset generator
        
        Args:
            seed: Random seed for reproducibility (None for random)
        """
        if seed is not None:
            random.seed(seed)
        
        # Ensure output directory exists
        self._ensure_output_dir()
        
        self.datasets = {}
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'seed': seed,
            'datasets': {},
            'results': {}
        }
    
    @classmethod
    def _ensure_output_dir(cls):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(cls.OUTPUT_DIR):
            os.makedirs(cls.OUTPUT_DIR)
    
    @classmethod
    def get_output_dir(cls):
        """Get the output directory path"""
        cls._ensure_output_dir()
        return cls.OUTPUT_DIR
    
    def generate_all_datasets(self):
        """Generate datasets for all algorithms"""
        print("=" * 80)
        print("DYNAMIC DATASET GENERATION")
        print("=" * 80)
        print()
        
        self.datasets['shor'] = self.generate_shor_data()
        self.datasets['grover'] = self.generate_grover_data()
        self.datasets['deutsch_jozsa'] = self.generate_deutsch_jozsa_data()
        self.datasets['min_max'] = self.generate_min_max_data()
        self.datasets['phase_estimation'] = self.generate_phase_estimation_data()
        
        # Save datasets
        self.results['datasets'] = self.datasets
        
        print("\n✅ All datasets generated successfully!")
        print("=" * 80)
        print()
    
    def generate_shor_data(self, count: int = 5) -> List[int]:
        """
        Generate random composite numbers for Shor's algorithm
        
        Args:
            count: Number of test cases to generate
        
        Returns:
            List of composite numbers
        """
        print("📊 Generating Shor's Algorithm Data...")
        
        # Generate composite numbers (product of two primes)
        primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
        composites = []
        
        for _ in range(count):
            # Select two different primes
            p1, p2 = random.sample(primes[:7], 2)  # Use smaller primes to keep N < 100
            N = p1 * p2
            
            # Ensure uniqueness and reasonable size
            if N not in composites and N < 100 and N > 10:
                composites.append(N)
        
        # Sort for consistency
        composites = sorted(list(set(composites)))[:count]
        
        print(f"  Generated {len(composites)} composite numbers: {composites}")
        print()
        
        return composites
    
    def generate_grover_data(self, num_cases: int = 4) -> List[Tuple]:
        """
        Generate random search scenarios for Grover's algorithm
        
        Args:
            num_cases: Number of test cases
        
        Returns:
            List of (marked_items, search_space_size, description) tuples
        """
        print("📊 Generating Grover's Algorithm Data...")
        
        test_cases = []
        
        # Available search space sizes (powers of 2)
        space_sizes = [16, 32, 64, 128]
        
        for i in range(num_cases):
            space_size = random.choice(space_sizes)
            
            # Random number of marked items (1-3)
            num_marked = random.randint(1, 3)
            
            # Generate random marked items
            marked_items = sorted(random.sample(range(space_size), num_marked))
            
            description = f"{num_marked} item{'s' if num_marked > 1 else ''} in {space_size} elements"
            
            test_cases.append((marked_items, space_size, description))
            print(f"  Case {i+1}: {description} - {marked_items}")
        
        print()
        return test_cases
    
    def generate_deutsch_jozsa_data(self, num_cases: int = 6) -> List[Tuple]:
        """
        Generate random function types for Deutsch-Jozsa algorithm
        
        Args:
            num_cases: Number of test cases
        
        Returns:
            List of (n_qubits, function_type, description) tuples
        """
        print("📊 Generating Deutsch-Jozsa Algorithm Data...")
        
        test_cases = []
        
        # Qubit range (3-6 for good simulation performance)
        qubit_range = [3, 4, 5, 6]
        function_types = ['constant', 'balanced']
        
        for i in range(num_cases):
            n_qubits = random.choice(qubit_range)
            func_type = random.choice(function_types)
            
            description = f"{n_qubits} qubits, {func_type} function"
            test_cases.append((n_qubits, func_type, description))
            print(f"  Case {i+1}: {description}")
        
        print()
        return test_cases
    
    def generate_min_max_data(self, num_datasets: int = 4, array_size: int = 8) -> List[Tuple]:
        """
        Generate random arrays for min/max finding
        
        Args:
            num_datasets: Number of test datasets
            array_size: Size of each array (must be power of 2)
        
        Returns:
            List of (data_array, description) tuples
        """
        print("📊 Generating Min/Max Finding Data...")
        
        # Ensure array_size is power of 2
        if array_size & (array_size - 1) != 0:
            array_size = 2 ** math.ceil(math.log2(array_size))
            print(f"  Adjusted array size to {array_size} (power of 2)")
        
        datasets = []
        
        for i in range(num_datasets):
            dataset_type = random.choice([
                'random_small',
                'random_large', 
                'unique_min',
                'unique_max',
                'mixed'
            ])
            
            if dataset_type == 'random_small':
                data = [random.randint(1, 20) for _ in range(array_size)]
                desc = f"Random values 1-20"
            
            elif dataset_type == 'random_large':
                data = [random.randint(10, 100) for _ in range(array_size)]
                desc = f"Random values 10-100"
            
            elif dataset_type == 'unique_min':
                value = random.randint(5, 10)
                data = [value] * array_size
                data[random.randint(0, array_size-1)] = 1
                desc = f"Mostly {value}s with unique min"
            
            elif dataset_type == 'unique_max':
                value = random.randint(5, 10)
                data = [value] * array_size
                data[random.randint(0, array_size-1)] = 99
                desc = f"Mostly {value}s with unique max"
            
            else:  # mixed
                data = [random.randint(1, 50) for _ in range(array_size)]
                desc = f"Mixed random values"
            
            datasets.append((data, desc))
            print(f"  Dataset {i+1}: {desc} - {data}")
        
        print()
        return datasets
    
    def generate_phase_estimation_data(self, num_cases: int = 6) -> List[Tuple]:
        """
        Generate random phases for phase estimation
        
        Args:
            num_cases: Number of test cases
        
        Returns:
            List of (phase, n_qubits, description) tuples
        """
        print("📊 Generating Phase Estimation Data...")
        
        test_cases = []
        
        # Generate both dyadic and non-dyadic phases
        dyadic_phases = [0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875]
        
        for i in range(num_cases):
            # 70% dyadic, 30% non-dyadic
            if random.random() < 0.7:
                phase = random.choice(dyadic_phases)
                phase_type = "dyadic"
            else:
                phase = round(random.uniform(0.1, 0.9), 3)
                phase_type = "non-dyadic"
            
            # Number of counting qubits (4-7 for good precision)
            n_qubits = random.randint(4, 7)
            
            # Convert phase to fraction if dyadic
            if phase_type == "dyadic":
                from fractions import Fraction
                frac = Fraction(phase).limit_denominator(16)
                desc = f"Phase = {frac} ({phase}), {n_qubits} qubits"
            else:
                desc = f"Phase = {phase} ({phase_type}), {n_qubits} qubits"
            
            test_cases.append((phase, n_qubits, desc))
            print(f"  Case {i+1}: {desc}")
        
        print()
        return test_cases