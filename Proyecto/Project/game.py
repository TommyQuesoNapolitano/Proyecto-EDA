from Project.sudoku import Sudoku

def get_sudoku_board(num_visibles: int=16):
    sudoku = Sudoku()
    return sudoku.generate_sudoku(num_visibles)