import tkinter as tk
import random
from PIL import ImageTk, Image
from cell_flag_state import CellFlagState

# TODO: add clock functionality
# TODO: change theme/style to have more colors
# TODO: change cell to a seperate object
# TODO: add press on cell that has same number of flags around it to clear all other cells feature.


FLAGS = 20
PERCENTAGE_OF_MINES = 0.15
BOMB_IMAGE_FILE_PATH = r"images/mine.png"
FLAG_IMAGE_FILE_PATH = r"images/flag.jpg"
CELL_SIZE = (80, 80)
FLAG_IMAGE = Image.open(FLAG_IMAGE_FILE_PATH).resize(CELL_SIZE)
BOMB_IMAGE = Image.open(BOMB_IMAGE_FILE_PATH).resize(CELL_SIZE, Image.ANTIALIAS)


class MineSweeper:
    def __init__(self, mine_rows: int, mine_cols: int) -> None:
        self.mine_rows = mine_rows
        self.mine_cols = mine_cols
        self.num_of_mines = int(self.mine_rows * self.mine_cols * PERCENTAGE_OF_MINES)
        self.window = tk.Tk()
        self.window.title("Mine Sweeper")
        self.window.resizable(False, False)  ###maybe change in future to resizable
        # self.window.geometry(f"{WIDTH}x{HEIGHT}")

        # images
        self.flag_photo = ImageTk.PhotoImage(FLAG_IMAGE)
        self.bomb_photo = ImageTk.PhotoImage(BOMB_IMAGE)

        # initialize
        self.padding: dict = {"padx": 1, "pady": 1}
        self.game_over = False
        self.player_pressed_once = False
        # grid
        self.mine_positions: list[list[int]] = [[]]
        self.grid: list[list[tk.Button]] = self.draw_grid()
        self.grid_flag_state: list[list[CellFlagState]] = [
            [CellFlagState.not_flagged_nor_pressed for j in range(self.mine_cols)]
            for i in range(self.mine_rows)
        ]
        self.initialize_flag_label()

    def initialize_flag_label(self) -> None:
        """Initializes flag_label and positions it beside grid"""
        self.flag_label: tk.Label = tk.Label(
            self.window, text=f"Flags available: {FLAGS}"
        )
        self.flag_label.grid(row=0, column=self.mine_cols, **self.padding)

    def draw_grid(self) -> list[list[tk.Button]]:
        grid = [
            [
                tk.Button(
                    self.window,
                    # image=tk.PhotoImage(),
                    width=6,
                    height=4,
                    relief=tk.RAISED,
                    command=lambda row=i, col=j: self.pressed(row, col),
                )
                for j in range(self.mine_cols)
            ]
            for i in range(self.mine_rows)
        ]
        for i in range(self.mine_rows):
            for j in range(self.mine_rows):
                grid[i][j].grid(row=i, column=j, **self.padding)
                grid[i][j].bind(
                    "<Button-3>",
                    lambda event, row=i, col=j: self.button_right_click(
                        row=row, col=col
                    ),
                )
        return grid

    def get_mine_positions(
        self, first_time: (tuple[int, int] | None) = None
    ) -> list[list[int]]:
        positions = [[0 for j in range(self.mine_cols)] for i in range(self.mine_rows)]
        if first_time:
            first_pos = first_time[0] * self.mine_rows + first_time[1]
            not_possible_positions = [
                r * self.mine_rows + c
                for r, c in self.get_neighbors(first_time[0], first_time[1])
            ]
            not_possible_positions.append(first_pos)
            pick_from = [
                i
                for i in range(self.mine_rows * self.mine_cols)
                if i not in not_possible_positions
            ]
            random_mine_positions = random.sample(pick_from, k=self.num_of_mines)
        else:
            random_mine_positions = random.sample(
                range(self.mine_rows * self.mine_cols), k=self.num_of_mines
            )
        for pos in random_mine_positions:
            row = pos // self.mine_rows
            col = pos % self.mine_cols
            positions[row][col] = -1
        for i in range(len(positions)):
            for j in range(len(positions[0])):
                if positions[i][j] != -1:
                    neigbors = self.get_neighbors(i, j)
                    for neighbor in neigbors:
                        positions[i][j] += (
                            positions[neighbor[0]][neighbor[1]] == -1
                        )  # count mines
        return positions

    def get_neighbors(self, row: int, col: int):
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

    def pressed(self, row: int, col: int):
        if self.grid_flag_state[row][col] == CellFlagState.flagged:
            return
        self.grid_flag_state[row][col] = CellFlagState.pressed
        if not self.player_pressed_once:
            self.mine_positions: list[list[int]] = self.get_mine_positions(
                first_time=(row, col)
            )
            self.player_pressed_once = True
        text = str(self.mine_positions[row][col])
        self.grid[row][col].configure(text=text, relief=tk.SUNKEN, state="disabled")
        if text == "-1":
            self.game_over = True
            self.grid[row][col].configure(
                image=self.bomb_photo,
                width=CELL_SIZE[1],
                height=CELL_SIZE[0],
            )
            self.press_all_bombs()
        elif text == "0":
            for r, c in self.get_neighbors(row, col):
                if self.mine_positions[r][c] != -1:
                    self.grid[r][c].invoke()

    def press_all_bombs(self):
        for i in range(self.mine_rows):
            for j in range(self.mine_cols):
                if self.mine_positions[i][j] == -1:
                    self.grid[i][j].invoke()

    def button_right_click(self, row: int, col: int) -> None:
        if not self.player_pressed_once:
            return
        global FLAGS
        print("right_clicked", FLAGS)
        match self.grid_flag_state[row][col]:
            case CellFlagState.pressed:
                pass
            case CellFlagState.flagged:
                FLAGS += 1
                self.grid_flag_state[row][col] = CellFlagState.not_flagged_nor_pressed
                self.grid[row][col].configure(
                    image="",
                    width=6,
                    height=4,
                )
            case CellFlagState.not_flagged_nor_pressed:
                if FLAGS > 0:
                    FLAGS -= 1
                    self.grid_flag_state[row][col] = CellFlagState.flagged
                    self.grid[row][col].configure(
                        image=self.flag_photo,
                        width=CELL_SIZE[1],
                        height=CELL_SIZE[0],
                    )
        self.flag_label.config(text=f"Flags available: {FLAGS}")

    def run(self):
        self.window.mainloop()


def main():
    game = MineSweeper(10, 10)
    game.run()


if __name__ == "__main__":
    main()
