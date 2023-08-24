import tkinter as tk
from enum import Enum, auto


class CellFlagState(Enum):
    revealed = auto()
    flagged = auto()
    hidden = auto()


class Cell:
    CELL_SIZE = (80, 80)
    flag_states_str = {
        CellFlagState.revealed: "revealed",
        CellFlagState.flagged: "flagged",
        CellFlagState.hidden: "hidden",
    }

    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col
        self.is_mine = False
        self.num_neighboring_bombs = 0
        self.flag_state = CellFlagState.hidden
        self.button = tk.Button()
        self.padding: dict = {"padx": 3, "pady": 3}

    def __str__(self):
        return f"Cell at row {self.row}, col {self.col}, and its state is {Cell.flag_states_str[self.flag_state]}"

    def embed_button_actions(self, master, left_click, right_click):
        """embeds the right and left click actions to the buttons"""
        self.button = tk.Button(
            master=master,
            width=6,
            height=4,
            relief=tk.RAISED,
            command=left_click,
        )
        self.button.grid(row=self.row, column=self.col, **self.padding)
        self.button.bind("<Button-3>", right_click)

    def reveal(self, photo):
        """Reveals current Cell to either show num_neighboring_mines or show image of bomb."""
        self.flag_state = CellFlagState.revealed
        text = str(self.num_neighboring_bombs)
        self.button.configure(
            text=text, relief=tk.SUNKEN
        )  # changed from disabled to add a feature
        if self.is_mine:
            self.button.configure(
                image=photo,
                width=Cell.CELL_SIZE[1],
                height=Cell.CELL_SIZE[0],
            )
