# registry.py

from dataclasses import dataclass
from typing import get_type_hints

@dataclass
class TypeInfo:
    name: str
    fields: dict

class FastRegistry:
    """
    Fast type registry using dict.
    Lookups are basically O(1) on average.
    """

    def __init__(self):
        self.table = {}

    def register_type(self, cls):
        # avoid duplicate work
        if cls in self.table:
            return

        try:
            hints = get_type_hints(cls)
        except:
            hints = {}

        fields = {}
        for k, v in hints.items():
            fields[k] = str(v)

        self.table[cls] = TypeInfo(name=cls.__name__, fields=fields)

    def get_type_info(self, cls):
        return self.table.get(cls)


class SlowRegistry:
    """
    Slow version using a list and linear search.
    Lookups are O(n).
    Only used for complexity comparison.
    """

    def __init__(self):
        self.items = []   # list of (cls, TypeInfo)

    def register_type(self, cls):
        # check if already present
        for existing_cls, _ in self.items:
            if existing_cls is cls:
                return

        try:
            hints = get_type_hints(cls)
        except:
            hints = {}

        fields = {}
        for k, v in hints.items():
            fields[k] = str(v)

        self.items.append((cls, TypeInfo(cls.__name__, fields)))

    def get_type_info(self, cls):
        for existing_cls, info in self.items:
            if existing_cls is cls:
                return info
        return None
