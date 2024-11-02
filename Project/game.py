try:
    from Project.sudoku import Sudoku
    from Project.sudokuExceptions import SudokuGameLost
except ImportError:
    from sudoku import Sudoku
    from sudokuExceptions import SudokuGameLost

class StackSudoku(Sudoku):
    def __init__(self, board=None):
        super().__init__(board)
        self.__actions = []

    """Returns a sudoku's board, using Sudoku's class"""
    def get_sudoku_board(self):
        return self.get_board()

    """Check if the number already exists in the row or column, if not the user lost an attempt. If user doesn't have any attempt it'll raise an exception of tye SudokuLostGame"""
    def is_valid_number(self, *args, attempts: int, row: int, column: str, number: int):
        is_valid = self.is_valid_movement(row, column, number)
        if not is_valid:
            attempts -= 1
        else:
            self.show_box(row, column)
            self.__push_action(row, column)

        if attempts == 0:
            raise SudokuGameLost("Lo sentimos, has perdido el juego, más suerte para la próxima")

        return is_valid

    def __push_action(self, row: int, column: str):
        self.__actions.append(f"{column}{row}")

    def delete_action(self):
        last_action = self.__actions.pop()
        self.delete_box(last_action)