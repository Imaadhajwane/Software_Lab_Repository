# classical_min_max.py
def classical_min_max(data: list, find_min: bool = True) -> dict:
    """Classical algorithm for finding min/max"""
    if not data:
        return {'error': 'Empty data list'}
    
    comparisons = 0
    
    if find_min:
        target = data[0]
        target_idx = 0
        
        for i in range(1, len(data)):
            comparisons += 1
            if data[i] < target:
                target = data[i]
                target_idx = i
    else:
        target = data[0]
        target_idx = 0
        
        for i in range(1, len(data)):
            comparisons += 1
            if data[i] > target:
                target = data[i]
                target_idx = i
    
    return {
        'data': data,
        'find_min': find_min,
        'value': target,
        'index': target_idx,
        'comparisons': comparisons
    }