# classical_phase_estimation.py
import numpy as np

def classical_phase_estimation(phase: float, n_samples: int = 1000) -> dict:
    """
    Classical phase estimation using sampling
    Requires exponentially many samples for good precision
    """
    # Simulate measuring the phase through repeated sampling
    # This is a simplified classical version
    
    samples_needed = 2 ** n_samples  # Exponential in precision required
    
    # In practice, we'd need to sample the unitary multiple times
    # Here we simulate the complexity
    
    # For a fair comparison, estimate precision achievable with n_samples
    precision = 1 / n_samples
    
    # Simulate noisy estimation
    noise = np.random.normal(0, precision / 2)
    estimated_phase = phase + noise
    estimated_phase = max(0, min(estimated_phase, 0.999))  # Clamp to valid range
    
    error = abs(estimated_phase - phase)
    
    return {
        'actual_phase': phase,
        'estimated_phase': estimated_phase,
        'error': error,
        'precision': precision,
        'samples_needed': samples_needed,
        'method': 'classical_sampling'
    }