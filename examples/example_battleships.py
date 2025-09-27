# define board class
from maskmatch.core import groups_by_duplicates, precombine_groups, solve_disjoint, generate_singlebit_lookup
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
        self.ship_sizes = sorted(ship_sizes)[::-1]
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


# create board
#board = Board(10, 10, [6, 4, 4, 3, 3, 3, 2, 2, 2, 2])
board = Board(10, 10, [6, 4, 4, 3, 3])
print(f"\nBoard initialized with width {board.width} and height {board.height}")

mask_lists = board.generate_mask_lists()
print(f"\n{sum([len(l) for l in mask_lists])} masks generated")

groups = groups_by_duplicates(mask_lists)
print(f"\n{len(groups)} groups found:")
for group in groups:
    print(f".  num masks: {len(group[0])}, multiplicity: {group[1]}")

precombined = precombine_groups(groups)
print(f"\ngroups precombined:")
for masks, mult in precombined:
    print(f".  num masks: {len(masks)}, multiplicity: {mult}")
    
    
lookups = generate_singlebit_lookup(precombined)

for idx, lookup in enumerate(lookups):
    print(f"\n\nlookup table for index {idx}: ")
    for bit in lookup:
        print(f"\n  {bit}-bit set:", len(lookup[bit]))
        
        # for mask in lookup[bit]:
        #     print(format(mask, f"0{100}b"))

# print(f"\nrun solver...")
# result = solve_disjoint(precombined)

# import random as rd

# l = len(result)
# n = 100

# print(f"{l} valid combinatons found")

# print(f" for example: {format(result[rd.randint(0,l-1)], f"0{n}b")}")
