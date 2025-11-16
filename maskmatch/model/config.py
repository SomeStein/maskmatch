
# ==============================
# file: model/config.py
# ==============================

from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class SolverConfig:
    method: str = "backtracking"  # "backtracking", "approximate", "parallel"
    symmetry: bool = True
    allow_repetition: bool = False
    approximate: bool = False
    parallel: bool = False
    return_type: str = "count"  # "count", "combined_masks", "indices"
    heuristics: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_kwargs(cls, kwargs: Dict[str, Any]):
        return cls(**kwargs)
