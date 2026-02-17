"""
Base classes for quantum and classical algorithms
"""
from abc import ABC, abstractmethod
from typing import Any, Dict
import time


class BaseAlgorithm(ABC):
    """Abstract base class for all algorithms"""
    
    def __init__(self, name: str):
        self.name = name
        self.execution_time = 0.0
        self.results = None
    
    @abstractmethod
    def run(self, *args, **kwargs) -> Any:
        """Execute the algorithm"""
        pass
    
    def benchmark(self, *args, **kwargs) -> Dict[str, Any]:
        """Run algorithm and collect metrics"""
        start_time = time.time()
        result = self.run(*args, **kwargs)
        end_time = time.time()
        
        self.execution_time = end_time - start_time
        self.results = result
        
        return {
            'algorithm': self.name,
            'execution_time': self.execution_time,
            'result': result
        }