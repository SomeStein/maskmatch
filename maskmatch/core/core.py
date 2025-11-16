from maskmatch.core.utils import _precombine_groups, _generate_lookups, _bit_indices, _split_hi_lo_arr, _candidate_mask
import itertools
import numpy as np
from tqdm import tqdm
from numba import njit
from multiprocessing import Pool, cpu_count
from typing import List, Set

def _recursion_on_lookups(precombined):
    total_result = 0
    mask_lists = [masks for masks, mult in precombined]
    # Generate lookups
    lookups = _generate_lookups(precombined)
    print(f"lookups generated!")

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

@njit(cache=True)
def count_combinations(hi_sets, lo_sets, idx, mask_hi, mask_lo):
    # Recursively search for valid combinations.
    if idx == len(hi_sets):
        return 1
    total = 0
    hi_arr = hi_sets[idx]
    lo_arr = lo_sets[idx]
    for i in range(hi_arr.shape[0]):
        if _candidate_mask(hi_arr[i], lo_arr[i], mask_hi, mask_lo):
            total += count_combinations(
                hi_sets,
                lo_sets,
                idx+1,
                mask_hi | hi_arr[i],
                mask_lo | lo_arr[i])
    return total

def _worker_first_choice(args):
    hi_sets, lo_sets, first_idx = args
    hi0, lo0 = hi_sets[0][first_idx], lo_sets[0][first_idx]
    return count_combinations(
        hi_sets[1:], lo_sets[1:], 0, hi0, lo0)

def calculate_valid_combinations(sets: List[Set[int]]) -> int:
    hi_sets, lo_sets = _split_hi_lo_arr(sets)
    first_len = len(hi_sets[0])
    # Prepare work: one job per first number
    jobs = [(hi_sets, lo_sets, idx) for idx in range(first_len)]
    # Use tqdm for progress bar
    with Pool(processes=max(1,min(cpu_count(), first_len))) as pool:
        results = []
        for res in tqdm(pool.imap_unordered(_worker_first_choice, jobs), total=first_len, desc="Solving..."):
            results.append(res)
    return sum(results)

def maskmatch(mask_lists):

    # Preprocessing
    precombined = _precombine_groups(mask_lists)    

    # Recursion 
    # result = _recursion_on_lookups(precombined)
    result = calculate_valid_combinations([set(masks) for masks, mult in precombined])
    
    # Result
    print(f"Result is: {result}")
    
# ToDos 
# - disgard memory
# - recurse over indices not bitmasks directly (uint64)
# - use vectorized SIMD if possible 
# - debug info and visualization
# - c and gpu implementation
# - edge cases abdecken + unittests
# - approximate (Monte Carlo/ IEP)
# - count/ indices/ masks
