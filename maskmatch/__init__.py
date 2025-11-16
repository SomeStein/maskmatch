"""
maskmatch: A modular solver framework for disjoint mask selection
"""

# Public API: high-level, clean, stable
from .model.problem import Problem
from .model.config import SolverConfig
from .core.solve import solve

__all__ = [
    "Problem",
    "SolverConfig",
    "solve",
]

__version__ = "0.1.1"
__author__ = "Aaron Pumm"