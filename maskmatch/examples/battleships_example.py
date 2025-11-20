"""
Example workflow using the new maskmatch API.
- Board → generate mask lists
- Wrap into Problem
- Configure Solver
- Run solve()
"""

from enum import Enum, auto
from maskmatch import Problem, SolverConfig, solve


# ==============================
# Battleship Board Implementation
# ==============================

class CellState(Enum):
    UNKNOWN = auto()
    MISS = auto()
    HIT = auto()
    SUNK = auto()


class Board:
    def __init__(self, width: int, height: int, ship_sizes: list[int]):
        self.width = width
        self.height = height
        self.ship_sizes = ship_sizes
        self.cells = [
            [CellState.UNKNOWN for _ in range(width)] for _ in range(height)
        ]

    def edit_cell(self, x: int, y: int, state: CellState) -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x] = state

    def _generate_valid_placements(self):
        positions = {}
        for ship_size in set(self.ship_sizes):
            positions[ship_size] = []
            for r in range(self.height):
                for c in range(self.width):
                    if c + ship_size <= self.width:
                        positions[ship_size].append(
                            [(r, c + i) for i in range(ship_size)]
                        )
                    if r + ship_size <= self.height:
                        positions[ship_size].append(
                            [(r + i, c) for i in range(ship_size)]
                        )
            # remove invalid placements
            for i in range(len(positions[ship_size]) - 1, -1, -1):
                pos = positions[ship_size][i]
                if any(self.cells[r][c] in [CellState.MISS, CellState.SUNK] for r, c in pos):
                    positions[ship_size].pop(i)
        return positions

    def _generate_bitmasks(self, positions):
        bitmasks = {}
        for ship_size, pos_list in positions.items():
            bitmasks[ship_size] = []
            for pos in pos_list:
                bitmask = 0
                for r, c in pos:
                    bitmask |= 1 << (r * self.width + c)
                    # German no-touch padding
                    for dr, dc in [(1, 0), (0, 1), (1, 1)]:
                        rr, cc = r + dr, c + dc
                        if 0 <= rr < self.height and 0 <= cc < self.width:
                            bitmask |= 1 << (rr * self.width + cc)
                bitmasks[ship_size].append(bitmask)
        return bitmasks

    def generate_mask_lists(self):
        placements = self._generate_valid_placements()
        bitmasks = self._generate_bitmasks(placements)
        return [bitmasks[size] for size in self.ship_sizes]


# ==============================
# Main Workflow Example
# ==============================
if __name__ == "__main__":
    board = Board(10, 10, [6, 4, 4, 3, 3, 3, 2])
    print(f"Board {board.width}x{board.height} initialized.")

    mask_lists = board.generate_mask_lists()
    print(f"Generated {sum(len(lst) for lst in mask_lists)} masks.")

    # Wrap into Problem
    problem = Problem.from_groups(mask_lists)

    # Configure solver (count-only for speed)
    cfg = SolverConfig(return_type="count")

    # Solve
    result = solve(problem, cfg)
    print(f"Valid placements count: {result.count}")