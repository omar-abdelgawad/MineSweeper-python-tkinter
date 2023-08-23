import tkinter as tk
import random
from PIL import ImageTk, Image
from cell import Cell, CellFlagState

# TODO: document readme well
# TODO: add clock functionality
# TODO: add restart button
# TODO: add press on cell that has same number of flags around it to clear all other cells feature.
# TODO: add choosing the number of rows and columns at start of game
# TODO: change the design to make it a bit more like original mines
# TODO: make an AI that can play the game
# TODO: change dims of the cell to change according to size of rows and cols
# TODO: add some padding to the grid to make it make it cleaner

MINES_PERCENTAGE = 0.25
BOMB_IMAGE_FILE_PATH = r"images/mine.png"
FLAG_IMAGE_FILE_PATH = r"images/flag.jpg"
FLAG_IMAGE = Image.open(FLAG_IMAGE_FILE_PATH).resize(Cell.CELL_SIZE)
BOMB_IMAGE = Image.open(BOMB_IMAGE_FILE_PATH).resize(Cell.CELL_SIZE)


class MineSweeper:
    def __init__(self, mine_rows: int, mine_cols: int) -> None:
        self.mine_rows: int = mine_rows
        self.mine_cols: int = mine_cols
        self.num_of_mines: int = int(self.mine_rows * self.mine_cols * MINES_PERCENTAGE)
        self.flags_available: int = self.num_of_mines
        self.window = tk.Tk()
        self.window.title("Mine Sweeper")
        self.window.resizable(False, False)  ###maybe change in future to resizable

        # images
        self.flag_photo = ImageTk.PhotoImage(FLAG_IMAGE)
        self.bomb_photo = ImageTk.PhotoImage(BOMB_IMAGE)

        # initialize_game_state
        self.padding: dict = {"padx": 1, "pady": 1}
        self.game_over: bool = False
        self.player_pressed_once: bool = False

        # initializing flag_label and placing it beside the grid
        self.flag_label: tk.Label = tk.Label(
            self.window, text=f"Flags available: {self.flags_available}"
        )
        self.flag_label.grid(row=0, column=self.mine_cols, **self.padding)

        # initializing grid if Cells
        self.grid = [
            [Cell(i, j) for j in range(self.mine_cols)] for i in range(self.mine_rows)
        ]
        for i in range(self.mine_rows):
            for j in range(self.mine_cols):
                self.grid[i][j].embed_button_actions(
                    self.window,
                    lambda row=i, col=j: self.left_clicked(row, col),
                    lambda event, row=i, col=j: self.right_clicked(row, col),
                )

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
            for r, c in self.get_neighbors(first_time[0], first_time[1])
        }
        not_possible_positions.add(first_pos)
        pick_from: list[int] = [
            i
            for i in range(self.mine_rows * self.mine_cols)
            if i not in not_possible_positions
        ]
        random_mine_positions = random.sample(pick_from, k=self.num_of_mines)

        for pos in random_mine_positions:
            row = pos // self.mine_cols
            col = pos % self.mine_cols
            positions[row][col] = -1
        for i in range(self.mine_rows):
            for j in range(self.mine_cols):
                if positions[i][j] != -1:
                    neigbors = self.get_neighbors(i, j)
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
        match self.grid[row][col].flag_state:
            case CellFlagState.revealed:
                # TODO: implement click on it feature to reveal neighbors
                return
            case CellFlagState.flagged:
                return
            case CellFlagState.hidden:
                if not self.player_pressed_once:
                    self.find_mine_positions((row, col))
                    self.player_pressed_once = True
                self.grid[row][col].reveal(self.bomb_photo)
                if self.grid[row][col].is_mine:
                    self.game_over = True
                    self.reveal_all_bombs()
                elif self.grid[row][col].num_neighboring_bombs == 0:
                    for r, c in self.get_neighbors(row, col):
                        self.grid[r][c].button.invoke()

    def right_clicked(self, row: int, col: int) -> None:
        """implements right_click behaviour of button depending on its state"""
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

    def get_neighbors(self, row: int, col: int) -> list[tuple[int, int]]:
        """gets all neighboring cells to a given cell.

        Args:
            row(int): row of current cell ranging between [0-self.mine_rows]
            col(int): col of current cell ranging between [0-self.mine_cols]
        Returns:
            list[tupele[int,int]]: all neighboring cells within grid bounds.
        """
        neighbors = []
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if (dy == 0) and (dx == 0):
                    continue
                if (0 <= row + dy < self.mine_rows) and (
                    0 <= col + dx < self.mine_cols
                ):
                    neighbors.append((row + dy, col + dx))
        return neighbors

    def reveal_all_bombs(self) -> None:
        """presses all bombs after losing the game."""
        for i in range(self.mine_rows):
            for j in range(self.mine_cols):
                if self.grid[i][j].is_mine:
                    self.grid[i][j].button.invoke()

    def run(self):
        self.window.mainloop()


def main():
    game = MineSweeper(10, 10)
    game.run()


if __name__ == "__main__":
    main()
