# ==============================
# file: core/solve.py
# ==============================

from typing import Any, Dict
from .backtracking import solve_backtracking  
from ..model.problem import Problem
from ..model.config import SolverConfig


class Solution:
    def __init__(self, count: int = 0, selections=None, combined_masks=None, indices=None, profiling=None):
        self.count = count
        self.selections = selections
        self.combined_masks = combined_masks
        self.indices = indices
        self.profiling = profiling or {}

    def __repr__(self):
        return (
            f"Solution(count={self.count}, "
            f"selections={None if self.selections is None else len(self.selections)}, "
            f"combined_masks={None if self.combined_masks is None else len(self.combined_masks)}, "
            f"indices={None if self.indices is None else len(self.indices)})"
        )


# Dispatcher

def solve(problem: Problem, config: SolverConfig) -> Solution:
    """
    Dispatches to backend in the *most efficient* mode:
    - count-only: backend only computes count
    - combined_masks: backend returns OR-combined masks
    - indices: backend returns index lists
    """
    mode = config.return_type

    raw = solve_backtracking(problem, config, mode=mode)

    if mode == "count":
        return Solution(count=raw.get("count", 0))

    if mode == "combined_masks":
        return Solution(
            count=raw.get("count", 0),
            combined_masks=raw.get("combined_masks"),
        )

    if mode == "indices":
        return Solution(
            count=raw.get("count", 0),
            indices=raw.get("indices"),
        )

    raise ValueError(f"Unknown return_type: {mode}")
