from typing import List, Tuple
from maskmatch.utils import groups_by_duplicates

from tqdm import tqdm

def backtrack_with_progress(result, mask_lists):
    """
    Backtracking over mask_lists with a progress bar on the first index.
    """
    first_masks = mask_lists[0]
    remaining_lists = mask_lists[1:]

    # Wrap only the first index loop with tqdm
    for idx0 in tqdm(range(len(first_masks)), desc="Processing first index"):
        mask0 = first_masks[idx0]
        current_mask = mask0
        current_indices = [idx0]

        # Call the normal recursion starting from the second list
        _backtrack_recursive(result, mask_lists, current_indices, current_mask)

def _backtrack_recursive(result, mask_lists, current_indices, current_mask):
    lidx = len(current_indices)
    m = len(mask_lists) 

    if lidx == m:
        result.append(current_mask)
        return

    masks = mask_lists[lidx]  
    for midx in range(len(masks)):
        mask = masks[midx]
        if (current_mask & mask) == 0:
            _backtrack_recursive(result, mask_lists, current_indices + [midx], current_mask | mask)

def backtrack_multiplicity(
    group_masks, masks, multiplicity, current_indices, current_mask=0, start_idx=0
):
    """
    Enumerate all combinations of 'multiplicity' masks from 'masks' list
    such that no two masks overlap (bitwise AND == 0), and append the
    combined mask to 'group_masks'.

    Parameters:
    - group_masks: list[int], accumulates the combined masks of valid tuples
    - masks: list[int], the candidate masks to combine
    - multiplicity: int, number of masks to select
    - current_indices: list[int], indices of masks chosen so far (for recursion)
    - current_mask: int, OR of currently chosen masks
    - start_idx: int, index in masks to start searching (to avoid duplicates)
    """

    # Base case: desired multiplicity reached
    if len(current_indices) == multiplicity:
        group_masks.append(current_mask)
        return

    # Iterate over remaining masks
    for idx in range(start_idx, len(masks)):
        mask = masks[idx]
        # Only choose if disjoint with current selection
        if (current_mask & mask) == 0:
            # Recursive call, increment start_idx to prevent duplicates
            backtrack_multiplicity(
                group_masks,
                masks,
                multiplicity,
                current_indices + [idx],
                current_mask | mask,
                idx + 1,
            )

def backtrack(valid_masks, mask_lists, current_indices, current_mask=0):
    """
    Enumerate all combinations of 'multiplicity' masks from 'masks' list
    such that no two masks overlap (bitwise AND == 0), and append the
    combined mask to 'group_masks'.

    Parameters:
    - group_masks: list[int], accumulates the combined masks of valid tuples
    - masks: list[int], the candidate masks to combine
    - multiplicity: int, number of masks to select
    - current_indices: list[int], indices of masks chosen so far (for recursion)
    - current_mask: int, OR of currently chosen masks
    """
    lidx = len(current_indices)
    m = len(mask_lists)

    # Base case: desired multiplicity reached
    if lidx == m:
        valid_masks.append(current_mask)
        return

    # Iterate over remaining masks
    masks = mask_lists[lidx]

    for midx in range(len(masks)):
        mask = masks[midx]
        # Only choose if disjoint with current selection
        if (current_mask & mask) == 0:
            # Recursive call, increment start_idx to prevent duplicates
            backtrack(
                valid_masks,
                mask_lists,
                current_indices + [midx],
                current_mask | mask,
            )


def precombine_groups(groups):
    result = []
    for masks, multiplicity in groups:

        group_masks = []
        current_indeces = []

        backtrack_multiplicity(group_masks, masks, multiplicity, current_indeces)

        result.append((group_masks, multiplicity))

    return result


def solve_disjoint(precombined):

    mask_lists = [l for l, m in precombined]
    mask_lists.sort(key=len)

    print([len(l) for l in mask_lists])

    result = []

    backtrack_with_progress(result, mask_lists)

    return result

def generate_singlebit_lookup(precombined):
    
    lookups = []
    for masks, mult in precombined: 
        lookup = dict()
        for bit in range(100):
            singlebitmask = 1 << bit 
            lookup[bit] = set() 
            for mask in masks: 
                if mask & singlebitmask == 0: 
                    lookup[bit].add(mask) 
        lookups.append(lookup)  
    return lookups

def maskmatch(mask_lists):
    
    # generate groups by multiplicity of mask lists
    groups = groups_by_duplicates(mask_lists)
    
    # precombine groups into one mask list of (w x h)-bit integers per group 
    precombined = precombine_groups(groups)
    
    # subset backtrack algorithm 
    result = solve_disjoint(precombined)
    
    return result