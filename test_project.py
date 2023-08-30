from project import (
    MineSweeper,
    get_neighbors,
    restart_game,
    handle_command_line,
)
from cell import CellFlagState

rows = 4
cols = 6


def test_get_neighbors():
    # testing corners first:
    # top left corner
    assert get_neighbors(0, 0, max_rows=4, max_cols=6) == {(0, 1), (1, 0), (1, 1)}
    # top right
    assert get_neighbors(0, cols - 1, max_rows=rows, max_cols=cols) == {
        (0, cols - 2),
        (1, cols - 2),
        (1, cols - 1),
    }
    assert get_neighbors(rows - 1, 0, max_rows=rows, max_cols=cols) == {
        (rows - 2, 0),
        (rows - 2, 1),
        (rows - 1, 1),
    }
    # bottom right
    assert get_neighbors(rows - 1, cols - 1, max_rows=4, max_cols=6) == {
        (rows - 2, cols - 2),
        (rows - 2, cols - 1),
        (rows - 1, cols - 2),
    }
    # testing cells on the edge but not corner
    # top edge
    assert get_neighbors(0, 1, max_rows=rows, max_cols=cols) == {
        (0, 0),
        (1, 0),
        (1, 1),
        (1, 2),
        (0, 2),
    }
    # left edge
    assert get_neighbors(2, 0, max_rows=rows, max_cols=cols) == {
        (1, 0),
        (1, 1),
        (2, 1),
        (3, 1),
        (3, 0),
    }
    # in middle
    assert get_neighbors(1, 1, max_rows=rows, max_cols=cols) == {
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 0),
        (1, 2),
        (2, 0),
        (2, 1),
        (2, 2),
    }


def test_restart_game():
    game = MineSweeper(rows, cols)
    restart_game(game=game)
    assert game.mine_rows == rows
    assert game.mine_cols == cols
    for row in game.grid:
        for cell in row:
            assert cell.flag_state == CellFlagState.hidden


def test_handle_command_line(capsys):
    test_rows, test_cols = handle_command_line(["-r", "-1"])
    stdout, stderr = capsys.readouterr()
    assert (
        stdout
        == "number of rows specefied not in range [4-9]. Rows changed back to default=8\n"
    )
    assert stderr == ""
    assert test_rows == 8
    assert test_cols == 8

    test_rows, test_cols = handle_command_line(["-c", "10"])
    stdout, stderr = capsys.readouterr()
    assert (
        stdout
        == "number of columns specefied not in range [4-9]. Columns changed back to default=8\n"
    )
    assert stderr == ""
    assert test_rows == 8
    assert test_cols == 8
    # in range cases
    test_rows, test_cols = handle_command_line(["-r", "4"])
    stdout, stderr = capsys.readouterr()
    assert stdout == ""
    assert stderr == ""
    assert test_rows == 4
    assert test_cols == 8
    test_rows, test_cols = handle_command_line(["-c", "6"])
    stdout, stderr = capsys.readouterr()
    assert stdout == ""
    assert stderr == ""
    assert test_rows == 8
    assert test_cols == 6
