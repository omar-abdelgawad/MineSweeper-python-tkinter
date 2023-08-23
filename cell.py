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
    def __init__(self, master, row: int, col: int, left_click, right_click) -> None:
        self.row = row
        self.col = col
        self.is_mine = False
        self.num_neighboring_bombs = 0
        self.flag_state = CellFlagState.hidden
        self.button = tk.Button(
            master=master,
            # image=tk.PhotoImage(),
            width=6,
            height=4,
            relief=tk.RAISED,
            command=left_click,
        )
        self.button.bind(
            "<Button-3>",
            lambda event: right_click(),
        )

    # def left_clicked(self):
    #     ###change to a function that is passed in the initializer
    #     raise NotImplementedError
    #     match self.flag_state:
    #         case CellFlagState.flagged:
    #             return
    #         case CellFlagState.revealed:
    #             # TODO: implement feature of revealing all neighboring cells if it has flagged neighbors = num_neighboring_bombs
    #             return
    #         case CellFlagState.hidden:
    #             self.flag_state = CellFlagState.revealed
    #             if not Cell.pressed_once:
    #                 self.mine_positions: list[list[int]] = self.get_mine_positions(
    #                     first_time=(row, col)
    #                 )
    #                 self.player_pressed_once = True
    #                 text = str(self.mine_positions[row][col])
    #                 self.grid[row][col].configure(
    #                     text=text, relief=tk.SUNKEN, state="disabled"
    #                 )
    #                 # if pressed cell is a bomb end game
    #                 if text == "-1":
    #                     self.game_over = True
    #                     self.grid[row][col].configure(
    #                         image=self.bomb_photo,
    #                         width=CELL_SIZE[1],
    #                         height=CELL_SIZE[0],
    #                     )
    #                     self.reveal_all_bombs()
    #                 # if it is has no neighboring bombs press all of them.
    #                 elif text == "0":
    #                     for r, c in self.get_neighbors(row, col):
    #                         if self.mine_positions[r][c] != -1:
    #                             self.grid[r][c].invoke()

    # def right_clicked(self) -> None:
    #     raise NotImplementedError
    #     if not Cell.pressed_once:
    #         return
    #     match self.flag_state:
    #         case CellFlagState.revealed:
    #             return
    #         case CellFlagState.flagged:
    #             return
