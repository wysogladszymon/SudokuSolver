import pytest
from ..src.Sudoku import Box, Sudoku  

def test_box_initialization():
    box = Box()
    assert box.entropy == 9
    assert not box.isSubmited
    assert not box.isWriten
    assert box.posibilities == {x: True for x in range(1, 10)}
    assert box.number == "-"

def test_box_reset():
    box = Box()
    box.write(5)
    box.reset()
    assert box.entropy == 9
    assert not box.isSubmited
    assert not box.isWriten
    assert box.posibilities == {x: True for x in range(1, 10)}
    assert box.number == "-"

def test_box_write():
    box = Box()
    box.write(5)
    assert box.number == 5
    assert box.isSubmited
    assert box.isWriten

def test_box_eliminate_possibility():
    box = Box()
    box.eliminatePossibility(5)
    assert not box.posibilities[5]
    assert box.entropy == 8


def test_sudoku_initialization():
    fields = {(0, 0): 5, (1, 1): 3}
    sudoku = Sudoku(fields)
    assert sudoku.matrix[0][0].getValue() == 5
    assert sudoku.matrix[1][1].getValue() == 3

def test_sudoku_reset():
    fields = {(0, 0): 5, (1, 1): 3}
    sudoku = Sudoku(fields)
    sudoku.reset()
    assert sudoku.matrix[0][0].getValue() == 5
    assert sudoku.matrix[1][1].getValue() == 3

def test_sudoku_correct_entropies():
    fields = {(0, 0): 5}
    sudoku = Sudoku(fields)
    sudoku.correctEntropies(0, 0, 5)
    for i in range(1, 9):
        assert not sudoku.matrix[i][0].posibilities[5]
        assert sudoku.matrix[i][0].entropy == 8
    for i in range(0, 3):
        for j in range(0,3):
            if i == 0 and j == 0:
                continue
            assert not sudoku.matrix[i][j].posibilities[5]
            assert sudoku.matrix[i][j].entropy == 8

def test_sudoku_find_next():
    fields = {(0, 0): 5, (1, 1): 3}
    sudoku = Sudoku(fields)
    y, x, allSubmited = sudoku.findNext()
    assert (y, x) != (None, None)
    assert not allSubmited

def test_sudoku_submit_box():
    fields = {}
    sudoku = Sudoku(fields)
    sudoku.submitBox(0, 0)
    assert sudoku.matrix[0][0].isTaken()

def test_sudoku_give_solution():
    fields = {(0, 0): 5, (1, 1): 3, (2, 2): 6}
    sudoku = Sudoku(fields)
    solution = sudoku.giveSollution()
    assert solution.shape == (9, 9)
    assert all(1 <= solution[y][x] <= 9 for y in range(9) for x in range(9))

if __name__ == "__main__":
    pytest.main()
