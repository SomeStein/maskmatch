from maskmatch.utils import _groups_by_duplicates, _precombine_groups, _generate_lookups, _bit_indices
import numpy as np
from tqdm import tqdm

def _recursion_on_lookups(precombined, lookups):
    total_result = 0
    mask_lists = [masks for masks, mult in precombined]

    def recurse(depth, current_mask):
        nonlocal total_result
        bits = _bit_indices(current_mask)
        indices_arrays = [lookups[depth][bit] for bit in bits]
        
        union_indices = np.unique(np.concatenate(indices_arrays))
            
        full_set = np.arange(len(mask_lists[depth]))
        valid_indices = np.setdiff1d(full_set, union_indices, assume_unique=True)
        
        if depth == len(lookups) - 1:
            total_result += len(valid_indices)
        else:
            for idx in valid_indices:
                mask = mask_lists[depth][idx]
                recurse(depth + 1, current_mask | mask)

    for i in tqdm(range(len(mask_lists[0]))):
        recurse(1, mask_lists[0][i])

    return total_result

def maskmatch(mask_lists):
    
    # Input checking
    if not mask_lists:
        return 0
    print(f"Input checked!")

    # Grouping 
    groups = _groups_by_duplicates(mask_lists)
    print(f"groups detected!")

    # Precombine
    precombined = _precombine_groups(groups)
    print(f"groups precombined!")

    # Generate lookups
    lookups = _generate_lookups(precombined)
    print(f"lookups generated!")

    # Recursion on lookups
    result = _recursion_on_lookups(precombined, lookups)
    print(f"Result is: {result}")