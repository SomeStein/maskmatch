# ==============================
# file: model/problem.py
# ==============================

from typing import List, Optional


class Problem:
    def __init__(self, groups: Optional[List[List[int]]] = None):
        """
        groups: List of lists of bitmasks (ints)
        Each inner list = allowed pieces for this group.
        """
        self.groups = groups or []

    @classmethod
    def from_groups(cls, groups):
        return cls(groups=groups)

    def add_group(self, masks: List[int]):
        self.groups.append(masks)

    def num_groups(self):
        return len(self.groups)

    def __repr__(self):
        return f"Problem(groups={len(self.groups)})"