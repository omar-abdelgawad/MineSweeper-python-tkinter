from enum import Enum, auto


class CellFlagState(Enum):
    revealed = auto()
    flagged = auto()
    hidden = auto()


class Cell:
    pass
