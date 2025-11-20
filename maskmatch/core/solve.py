# ==============================
# file: core/solve.py
# ==============================

from typing import Any, Dict
from .backtracking import solve_backtracking  
from ..model.problem import Problem
from ..model.config import SolverConfig
from ..model.solution import Solution


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
