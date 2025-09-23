"""
maskmatch: Disjoint binary word selection package
"""

from .core import solve_disjoint
#from .dp_solver import dp_solve
#from .parallel import parallel_solve
#from .approximation import approx_solve

__all__ = [
    "solve_disjoint",
   # "dp_solve",
   # "parallel_solve",
   # "approx_solve"
]

__version__ = "0.1.0"
__author__ = "Aaron Pumm"