from collections import defaultdict
from typing import List, Tuple


def groups_by_duplicates(mask_lists: List[List[int]]) -> List[Tuple[List[int], int]]:
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
