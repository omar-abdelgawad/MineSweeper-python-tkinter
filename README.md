# tk-Minesweeper

#### Video Demo: https://youtu.be/98Y7Qg1k6lk 

#### Description:

- Created the famous Minesweeper game as a CS50P final project.
- Entire gui is made using Tkinter.
### table of contents
- [How to Install](#how-to-install)
- [Usage](#usage)

## How to Install
1. Navigate to the main page of the [repository](https://github.com/omar-abdelgawad/MineSweeper-python-tkinter).
1. Click <> **Code**.
<div align="center">
<img src="images/repo_code_image.png" alt="green code box in repo image">
</div>

1. Copy the url for the repository using any method.
1. open Terminal on you local machine and navigate to the directory in which you want to download this repo.
1. Type `git clone` and then paste the url you just copied. When you press enter this repository will be cloned to your local machine.
    ```bash
    git clone url_you_just_copied
    ```
1. navigate to the directory using `cd`.
1. Type the following command to install the requirements using pip.
    ```bash
    pip install -r requirements.txt
    ```  
1. Now you should be able to run the game. To use default settings run the following command.
    ```bash
    python3 project.py
    ```

1. To choose number of rows and/or columns you can use command line arguments.
    ```
    python3 project.py -rows 4 - columns 9
    ```
## Usage

The app mimicks the famous Minesweeper game where the starting grid contains cells that are either mines or not (which is hidden ofc). You can expect to have an open window very similar to this one.
<div align="center">
<img src="images/game_at_start.png",alt="image of game at start">
</div>

You can start by pressing any cell you like to reveal it. **Don't worry** you can't lose from the first move. Once you hit a cell a **number** will be displayed on it. That number tells you how many mines are diagonally and/or adjacent to it. If you are lucky enough to hit a 0 then all neighboring cells to it are unlocked automatically.

Once you hit the first cell you will probably see a number of cells getting unlocked like the following image.

<div align="center">
<img src="images/first_pressed_cell.png",alt="image of first pressed cell">
</div>
Note that the first pressed cell always has 0 neighboring mines.

The goal is to unlock all non-mine cells in the shortest amount of time.