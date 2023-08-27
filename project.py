#! ./.venv/bin/python
import tkinter as tk
import random
import time
from PIL import ImageTk, Image
import argparse
from cell import Cell, CellFlagState

# TODO: document readme well
# TODO: add testing function
# TODO: record video

# TODO: change dims of the cell to change according to size of rows and cols
# TODO: add choosing the number of rows and columns at start of game
# TODO: maybe change the design to make it a bit more like original Mines
# TODO: make an AI that can play the game

MINES_PERCENTAGE = 0.35
BOMB_IMAGE_FILE_PATH = "images/mine.png"
FLAG_IMAGE_FILE_PATH = "images/flag.jpg"
FLAG_IMAGE = Image.open(FLAG_IMAGE_FILE_PATH).resize(Cell.CELL_SIZE)
BOMB_IMAGE = Image.open(BOMB_IMAGE_FILE_PATH).resize(Cell.CELL_SIZE)


class MineSweeper:
    def __init__(self, mine_rows: int, mine_cols: int) -> None:
        self.mine_rows: int = mine_rows
        self.mine_cols: int = mine_cols
        self.num_of_mines: int = int(self.mine_rows * self.mine_cols * MINES_PERCENTAGE)
        self.flags_available: int = self.num_of_mines
        self.window = tk.Tk()
        self.window.configure(bg="white")
        self.window.title("Mine Sweeper")
        self.window.resizable(False, False)  ###maybe change in future to resizable

        # images
        self.flag_photo = ImageTk.PhotoImage(FLAG_IMAGE)
        self.bomb_photo = ImageTk.PhotoImage(BOMB_IMAGE)

        # initialize_game_state
        self.padding: dict = {"padx": 10, "pady": 10}
        self.game_over: bool = False
        self.start_time: float = time.time()
        self.player_pressed_once: bool = False

        # initializing grid if Cells
        self.grid_label: tk.Label = tk.Label(self.window, bg="white")
        self.grid_label.pack(**self.padding)
        self.grid = [
            [Cell(i, j) for j in range(self.mine_cols)] for i in range(self.mine_rows)
        ]
        for i in range(self.mine_rows):
            for j in range(self.mine_cols):
                self.grid[i][j].embed_button_actions(
                    self.grid_label,
                    lambda row=i, col=j: self.left_clicked(row, col),
                    lambda event, row=i, col=j: self.right_clicked(row, col),
                )
        # initializing flag_label and placing it beside the grid
        self.flag_label: tk.Label = tk.Label(
            self.window, text=f"Flags available: {self.flags_available}"
        )
        self.flag_label.pack(padx=2, pady=2)
        # time label
        self.time_label = tk.Label(self.window, text="0s", font=("Helvetica", 48))
        self.time_label.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        # restart button
        self.restart_button = tk.Button(
            master=self.window,
            width=8,
            height=4,
            relief=tk.RAISED,
            text="Restart",
            command=lambda game=self: restart_game(game),
        )
        self.restart_button.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

    def find_mine_positions(self, first_time: (tuple[int, int])) -> None:
        """determines all mine positions for the grid excluding the first_clicked_position
        Args:
            first_time (tuple[int, int]): row and col index of the first pressed cell in the grid.

        Returns:
            list[list[int]]: contains a 2-D list for whether a cell is a bomb (-1 value) or count
            of neighboring bombs(0-8).
        """
        positions: list[list[int]] = [
            [0 for j in range(self.mine_cols)] for i in range(self.mine_rows)
        ]
        first_pos: int = first_time[0] * self.mine_cols + first_time[1]
        not_possible_positions = {
            r * self.mine_cols + c
            for r, c in get_neighbors(
                first_time[0], first_time[1], self.mine_rows, self.mine_cols
            )
        }
        not_possible_positions.add(first_pos)
        pick_from: list[int] = [
            i
            for i in range(self.mine_rows * self.mine_cols)
            if i not in not_possible_positions
        ]
        self.num_of_mines = min(self.num_of_mines, len(pick_from))
        random_mine_positions = random.sample(pick_from, k=self.num_of_mines)
        for pos in random_mine_positions:
            row = pos // self.mine_cols
            col = pos % self.mine_cols
            positions[row][col] = -1
        for i in range(self.mine_rows):
            for j in range(self.mine_cols):
                if positions[i][j] != -1:
                    neigbors = get_neighbors(i, j, self.mine_rows, self.mine_cols)
                    for neighb_row, neighb_col in neigbors:
                        positions[i][j] += (
                            positions[neighb_row][neighb_col] == -1
                        )  # count mines
        for i in range(self.mine_rows):
            for j in range(self.mine_cols):
                self.grid[i][j].num_neighboring_bombs = positions[i][j]
                self.grid[i][j].is_mine = positions[i][j] == -1

    def left_clicked(self, row: int, col: int) -> None:
        """presses the cell
        Args:
            row(int): row of current cell ranging between [0-self.mine_rows]
            col(int): col of current cell ranging between [0-self.mine_cols]
        """
        print(f"left Clicked {self.grid[row][col]}")
        match self.grid[row][col].flag_state:
            case CellFlagState.revealed:
                neighbors = get_neighbors(row, col, self.mine_rows, self.mine_cols)
                cnts = {
                    CellFlagState.flagged: 0,
                    CellFlagState.hidden: 0,
                    CellFlagState.revealed: 0,
                }
                for r, c in neighbors:
                    cnts[self.grid[r][c].flag_state] += 1
                if (
                    cnts[CellFlagState.flagged]
                    == self.grid[row][col].num_neighboring_bombs
                ):
                    for r, c in neighbors:
                        if self.grid[r][c].flag_state == CellFlagState.hidden:
                            self.grid[r][c].button.invoke()
            case CellFlagState.flagged:
                return
            case CellFlagState.hidden:
                if not self.player_pressed_once:
                    self.start_game((row, col))
                self.grid[row][col].reveal(self.bomb_photo)
                if self.grid[row][col].is_mine and not self.game_over:
                    self.end_game()
                elif self.grid[row][col].num_neighboring_bombs == 0:
                    for r, c in get_neighbors(row, col, self.mine_rows, self.mine_cols):
                        self.grid[r][c].button.invoke()

    def right_clicked(self, row: int, col: int) -> None:
        """implements right_click behaviour of button depending on its state"""
        print(f"Right Clicked {self.grid[row][col]}")
        if not self.player_pressed_once:
            return
        match self.grid[row][col].flag_state:
            case CellFlagState.revealed:
                return
            case CellFlagState.flagged:
                self.flags_available += 1
                self.grid[row][col].flag_state = CellFlagState.hidden
                self.grid[row][col].button.configure(
                    image="",
                    width=6,
                    height=4,
                )
            case CellFlagState.hidden:
                if self.flags_available > 0:
                    self.flags_available -= 1
                    self.grid[row][col].flag_state = CellFlagState.flagged
                    self.grid[row][col].button.configure(
                        image=self.flag_photo,
                        width=Cell.CELL_SIZE[1],
                        height=Cell.CELL_SIZE[0],
                    )
        self.flag_label.config(text=f"Flags available: {self.flags_available}")

    def start_game(self, first_time_cell: tuple[int, int]) -> None:
        """initializes bomb positions and clock when a player presses any cell"""
        print("GAME STARTED")
        self.player_pressed_once = True
        self.find_mine_positions(first_time_cell)
        self.start_clock()

    def start_clock(self) -> None:
        self.start_time = time.time()
        self.update_time()

    def update_time(self) -> None:
        if not self.game_over:
            elapsed_time = time.time() - self.start_time
            self.time_label.config(text="{:.0f}s".format(elapsed_time))
            self.time_label.after(50, self.update_time)

    def stop_clock(self) -> None:
        raise NotImplementedError

    def end_game(self) -> None:
        # self.stop_clock()
        self.game_over = True
        self.reveal_all_bombs()
        print("GAME ENDED")

    def reveal_all_bombs(self) -> None:
        """presses all bombs after losing the game. if the bomb is flagged then it changes it to hidden
        to press it."""
        for i in range(self.mine_rows):
            for j in range(self.mine_cols):
                if self.grid[i][j].is_mine:
                    if self.grid[i][j].flag_state == CellFlagState.flagged:
                        self.right_clicked(i, j)
                    self.grid[i][j].button.invoke()

    def run(self) -> None:
        self.window.mainloop()


def restart_game(game: MineSweeper) -> None:
    """kills current app and reinitializes it."""
    game.window.destroy()
    game = MineSweeper(game.mine_rows, game.mine_cols)


def get_neighbors(
    row: int, col: int, max_rows: int, max_cols: int
) -> list[tuple[int, int]]:
    """gets all neighboring cells for a given cell.

    Args:
        row(int): row of current cell ranging between [0-self.mine_rows]
        col(int): col of current cell ranging between [0-self.mine_cols]
        max_rows(int): num of rows in the grid
        max_cols(int): num of cols in the grid
    Returns:
        list[tupele[int,int]]: all neighboring cells within grid bounds.
    """
    neighbors = []
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if (dy == 0) and (dx == 0):
                continue
            if (0 <= row + dy < max_rows) and (0 <= col + dx < max_cols):
                neighbors.append((row + dy, col + dx))
    return neighbors


def check_game_rows_and_cols(rows: int, cols: int) -> tuple[int, int]:
    """returns rows and cols after checking if they have values in specefied range or not."""
    raise NotImplementedError


# def start_of_game(game: MineSweeper) -> bool:
#     """check for start of game state"""
#     # also test that you can't lose from first move and neighboring cells are also not bombs
#     if game.game_over:
#         return False
#     return True


# def check_all_bombs_revealed(game: MineSweeper) -> bool:
#     """makes sure that all bombs have been revealed"""
#     if not game.game_over:
#         return False
#     for r in range(game.mine_rows):
#         for c in range(game.mine_cols):
#             cur_cell = game.grid[r][c]
#             if cur_cell.is_mine and cur_cell.flag_state != CellFlagState.revealed:
#                 return False
#     return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--rows", type=int, default=8)
    parser.add_argument("-c", "--columns", type=int, default=8)
    args = parser.parse_args()
    rows = args.rows
    cols = args.columns
    # TODO: check that input is always entered correctly otherwise set to default.
    print(args)
    game = MineSweeper(rows, cols)
    game.run()


if __name__ == "__main__":
    main()
