# define board class
from maskmatch.core import maskmatch
from enum import Enum, auto

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
        self.cells = [[CellState.UNKNOWN for _ in range(width)] for _ in range(height)]

    def edit_cell(self, x: int, y: int, state: CellState) -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x] = state

    def _generate_valid_placements(self) -> dict[int, list[list[tuple[int, int]]]]:
        """Generate all valid positions for each ship size."""
        positions = {}

        for ship_size in set(self.ship_sizes):
            positions[ship_size] = []

            for r in range(self.height):
                for c in range(self.width):
                    # Horizontal placement
                    if c + ship_size <= self.width:
                        positions[ship_size].append(
                            [(r, c + i) for i in range(ship_size)]
                        )
                    # Vertical placement
                    if r + ship_size <= self.height:
                        positions[ship_size].append(
                            [(r + i, c) for i in range(ship_size)]
                        )

            # Remove invalid positions (those overlapping with MISS or SUNK cells)
            for pos_index in range(len(positions[ship_size]) - 1, -1, -1):
                pos = positions[ship_size][pos_index]
                if any(
                    self.cells[r][c] in [CellState.MISS, CellState.SUNK] for r, c in pos
                ):
                    positions[ship_size].pop(pos_index)

        return positions

    def _generate_bitmasks(
        self, positions: dict[int, list[list[tuple[int, int]]]]
    ) -> dict[int, list[int]]:
        """Generate bitmasks for each valid position for efficient overlap checking, with positive x/y padding (German no-touch rule)."""
        bitmasks = {}
        for ship_size, pos_list in positions.items():
            bitmasks[ship_size] = []
            for pos in pos_list:
                bitmask = 0
                for r, c in pos:
                    bitmask |= 1 << (r * self.width + c)
                    # Apply padding only in positive x/y directions (right, down, down-right)
                    for dr, dc in [(1, 0), (0, 1), (1, 1)]:
                        rr, cc = r + dr, c + dc
                        if 0 <= rr < self.height and 0 <= cc < self.width:
                            bitmask |= 1 << (rr * self.width + cc)
                bitmasks[ship_size].append(bitmask)
        return bitmasks

    def generate_mask_lists(self):
        # generate valid placements
        placements = board._generate_valid_placements()

        # transform to bitmasks
        bitmasks = board._generate_bitmasks(placements)

        return [bitmasks[ss] for ss in self.ship_sizes]

if __name__ == "__main__":
    
    # Create board and generate mask lists
    #board = Board(10, 10, [6, 4, 4, 3, 3, 3, 2, 2, 2, 2])
    board = Board(10, 10, [6, 4, 4, 3, 3, 2, 2]) #300.000.000 boards pro sekunde
    print(f"\nBoard initialized with width {board.width} and height {board.height}")
    mask_lists = board.generate_mask_lists()
    print(f"\n{sum([len(l) for l in mask_lists])} masks generated")
    
    # Test maskmatch
    result = maskmatch(mask_lists)
    
    
# für battleships 
# - moves tree so tief wie möglich vorberechnen (vsl. tiefe 3-5)
# - danach monte carlo sampling + IEP 
# - bis direkte berechnung möglich (vsl. wenn 5 Platzierungen übrig)
