# deutsch_jozsa.py
import random  

def classical_deutsch_jozsa(n_qubits: int, function_type: str) -> dict:
    """
    Classical algorithm to determine if function is constant or balanced
    Requires checking half the inputs + 1 in worst case
    """
    input_size = 2 ** n_qubits
    queries_needed = (input_size // 2) + 1
    
    # Simulate queries
    if function_type == 'constant':
        # All outputs are the same
        output = random.choice([0, 1])
        outputs = [output] * queries_needed
    else:
        # Balanced: equal 0s and 1s
        outputs = [0] * (queries_needed // 2) + [1] * (queries_needed - queries_needed // 2)
        random.shuffle(outputs)
    
    # Check if constant
    if len(set(outputs)) == 1:
        detected_type = 'constant'
    else:
        detected_type = 'balanced'
    
    return {
        'n_qubits': n_qubits,
        'actual_type': function_type,
        'detected_type': detected_type,
        'queries': queries_needed,
        'correct': detected_type == function_type
    }
