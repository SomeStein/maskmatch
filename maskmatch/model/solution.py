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