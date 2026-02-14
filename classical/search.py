# search.py

def classical_search(marked_items: list, search_space_size: int) -> dict:
    """Classical linear search"""
    comparisons = 0
    found_items = []
    
    for i in range(search_space_size):
        comparisons += 1
        if i in marked_items:
            found_items.append(i)
            if len(found_items) == len(marked_items):
                break
    
    return {
        'found_items': found_items,
        'comparisons': comparisons,
        'average_comparisons': comparisons / len(marked_items) if marked_items else comparisons
    }