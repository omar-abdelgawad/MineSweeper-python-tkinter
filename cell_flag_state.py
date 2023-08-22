from enum import Enum, auto


class CellFlagState(Enum):
    pressed = auto()
    flagged = auto()
    not_flagged_nor_pressed = auto()
