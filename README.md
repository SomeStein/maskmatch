# maskmatch

`maskmatch` is a Python package for solving **disjoint binary word selection problems**. Given a set of lists of binary words (bitstrings), it efficiently computes combinations where no two selected words overlap in their `1`s. It supports exact counting, retrieving the selected masks, and optional performance optimizations.

---

## Features

- Compute the **number of valid selections** (`count`) or retrieve **actual selections** (`masks` or index tuples).  
- Supports **optional parameters**:  
  - `allow_repetition` — allow repeated words from the same list  
  - `approximate` — Monte Carlo / sampling-based estimation  
  - `parallel` — use multiple cores for large instances  
  - `numba` / `C` / `GPU` — acceleration for performance-critical loops  
  - `exploit_symmetry` — automatically compress identical lists to reduce computation  
- Handles large numbers of lists and sparse binary words efficiently.  

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/SomeStein/maskmatch.git
cd maskmatch
```

### ToDos:
- find appropriate solve/config Parameters
- make better core file structure
- build method selector in solve 
- parallel pool/ tqdm/ heuristics wrappers
- use selected worker
- fill Solution instance
- return Solution
- code method workers
- code viz 
- code saving
- find good graph editor architecture
- code editor

