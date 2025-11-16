# ==============================
# file: core/backtracking.py
# ==============================

from typing import List, Dict, Any
from ..model.problem import Problem
from ..model.config import SolverConfig
from ..utils import _precombine_groups, _split_hi_lo_arr, _candidate_mask
import numpy as np
from numba import njit


@njit(cache=True)
def _bt_count(hi_sets, lo_sets, idx, mask_hi, mask_lo):
    if idx == len(hi_sets):
        return 1
    total = 0
    hi_arr = hi_sets[idx]
    lo_arr = lo_sets[idx]
    for i in range(hi_arr.shape[0]):
        if _candidate_mask(hi_arr[i], lo_arr[i], mask_hi, mask_lo):
            total += _bt_count(
                hi_sets, lo_sets, idx + 1,
                mask_hi | hi_arr[i], mask_lo | lo_arr[i]
            )
    return total


def solve_backtracking(problem: Problem, config: SolverConfig, mode: str) -> Dict[str, Any]:
    """
    Wrapper around existing high-performance backend.
    Supports three modes: count, combined_masks, indices.
    """

    groups = problem.groups
    precombined = _precombine_groups(groups)
    sets = [set(masks) for masks, _ in precombined]
    hi_sets, lo_sets = _split_hi_lo_arr(sets)

    if mode == "count":
        total = 0
        for first_idx in range(len(hi_sets[0])):
            hi0 = hi_sets[0][first_idx]
            lo0 = lo_sets[0][first_idx]
            total += _bt_count(hi_sets[1:], lo_sets[1:], 0, hi0, lo0)
        return {"count": int(total)}

    # Modes below require storing data → slower
    results = []
    index_results = []

    def recurse(idx, mask_hi, mask_lo, path):
        if idx == len(hi_sets):
            if mode == "combined_masks":
                results.append(int(mask_hi << 64 | mask_lo))
            elif mode == "indices":
                index_results.append(path.copy())
            return

        hi_arr = hi_sets[idx]
        lo_arr = lo_sets[idx]

        for i in range(hi_arr.shape[0]):
            if (hi_arr[i] & mask_hi) == 0 and (lo_arr[i] & mask_lo) == 0:
                recurse(
                    idx + 1,
                    mask_hi | hi_arr[i],
                    mask_lo | lo_arr[i],
                    path + [i]
                )

    for first_idx in range(len(hi_sets[0])):
        hi0 = hi_sets[0][first_idx]
        lo0 = lo_sets[0][first_idx]
        recurse(1, hi0, lo0, [first_idx])

    if mode == "combined_masks":
        return {"count": len(results), "combined_masks": results}
    if mode == "indices":
        return {"count": len(index_results), "indices": index_results}

    raise ValueError(f"Unknown backtracking mode {mode}")