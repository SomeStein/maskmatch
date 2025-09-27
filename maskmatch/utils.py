from collections import defaultdict
from typing import List, Tuple
import numpy as np


def _groups_by_duplicates(mask_lists: List[List[int]]) -> List[Tuple[List[int], int]]:
    """
    Group identical lists together.
    Returns a list of tuples: (unique_masks_in_list, multiplicity)
    """
    canonical_lists = [tuple(sorted(lst)) for lst in mask_lists]
    group_map = defaultdict(list)
    for idx, canon in enumerate(canonical_lists):
        group_map[canon].append(idx)

    grouped = []
    for canon, idxs in group_map.items():
        grouped.append((list(canon), len(idxs)))
    return grouped

def _backtrack_multiplicity(
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
            _backtrack_multiplicity(
                group_masks,
                masks,
                multiplicity,
                current_indices + [idx],
                current_mask | mask,
                idx + 1,
            )

def _precombine_groups(groups):
    result = []
    for masks, multiplicity in groups:

        group_masks = []
        current_indeces = []

        _backtrack_multiplicity(group_masks, masks, multiplicity, current_indeces)

        result.append((group_masks, multiplicity))

    return result

def _generate_lookups(precombined):
    
    # for each group create dict (set bit -> np.array(indices of masks with set bit))
    
    lookups = []
    
    for group in precombined:
        masks, mult = group
        max_index = len(masks)
        max_bit = max(n.bit_length() for n in masks)
        lookup = dict()
        
        for bit in range(max_bit):
            lookup[bit] = np.array([idx for idx in range(max_index) if masks[idx]&1<<bit != 0], dtype=np.uint32)
            
        lookups.append(lookup)
        
    return lookups
        
def _bit_indices(n):
    indices = set()
    index = 0
    while n:
        if n & 1:  # check if the least significant bit is 1
            indices.add(index)
        n >>= 1  # shift right by 1
        index += 1
    return indices