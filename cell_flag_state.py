import tkinter as tk
from enum import Enum, auto


class CellFlagState(Enum):
    revealed = auto()
    flagged = auto()
    hidden = auto()


# bool for bomb or not
# int for how many surrounding bombs
# button
# cell_flag_state
# implement right and left clicking while changing state


class Cell:
    def __init__(self, master) -> None:
        self.is_bomb = False
        self.num_neighboring_bombs = 0
        self.flag_state = CellFlagState.hidden
        self.button = tk.Button(
            master=master,
            # image=tk.PhotoImage(),
            width=6,
            height=4,
            relief=tk.RAISED,
            command=self.pressed(),
        )
