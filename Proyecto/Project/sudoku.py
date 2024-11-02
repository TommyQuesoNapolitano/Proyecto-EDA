import random
try:
    from Project.sudokuExceptions import SudokuValueException
except ImportError:
    from sudokuExceptions import SudokuValueException

class Sudoku:
    def __init__(self, board=None):
        if board:
            self.__board = board
        else:
            self.__board = [f"{chr(ord('A') + j)}{i}" for j in range(9) for i in range(1, 10)]
            self.__board = {
                box: {
                    "visible": True,
                    "number": None,
                    "modifiable": False
                } for box in self.__board
            }

    def __str__(self):
        text = ""
        for column in "ABCDEFGHI":
            text += "[ "
            for row in range(1, 10):
                text += str(self.__board[f"{column}{row}"]["number"])
                if row == 9:
                    text += " ]"
                elif row % 3 == 0:
                    text += " ][ "
                else:
                    text += " | "
            text += "\n"
        return text

    def get_board(self):
        return self.__board

    """Verifica si \"number\" puede colocarse en \"board[row][col]\" sin romper las reglas de Sudoku"""
    def is_valid_movement(self, row: int, column: str, number: int) -> bool:
        try:
            self.is_valid_row_and_column(row, column)
        except SudokuValueException:
            raise SudokuValueException

        for new_row in range(1, 10):
            new_column = chr(ord('A') + new_row - 1)
            if self.__board[f"{column}{new_row}"]["number"] == number or self.__board[f"{new_column}{row}"]["number"] == number:
                return False
        
        start_row = ((row - 1) // 3) * 3 + 1
        start_column = chr(((ord(column) - ord('A')) // 3) * 3 + ord('A'))
        
        for i in range(3):
            for j in range(3):
                current_row = start_row + i
                current_col = chr(ord(start_column) + j)
                if self.__board[f"{current_col}{current_row}"]["number"] == number:
                    return False
        return True
    
    """Verifica si la fila está entre \"1\" y \"9\" y si la columna está entre \"A\" e \"I\". Si no lo es devuelve una excepción de tipo sudokuValueException"""
    def is_valid_row_and_column(self, row: int, column: str):
        try:
            self.__board[f"{column}{row}"]
            return True
        except KeyError:
            raise SudokuValueException("La fila y/o columna especificada no son válidos")

    """Rellena una cuadrícula entera usando números aleatorios"""
    def __fill_box(self, row: int, column: str):
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        for new_row in range(3):
            for new_column in range(3):
                self.__board[f"{chr(ord(column) + new_column)}{row + new_row}"]["number"] = numbers.pop()

    """Rellena todas las cuadrículas diagonales en una dirección del juego para hacer más fácil el backtracking"""
    def __fill_diagonal_boxes(self):
        for row in range(1, 10, 3):
            self.__fill_box(row, chr(ord('A') + row - 1))

    """Rellena los espacios faltantes del sudoku haciendo uso del backtracking y las cuadrículas generadas anteriormente"""
    def __solve_board(self):
        for column in "ABCDEFGHI":
            for row in range(1, 10):
                if self.__board[f"{column}{row}"]["number"] is None:
                    for number in range(1, 10):
                        if self.is_valid_movement(row, column, number):
                            self.__board[f"{column}{row}"]["number"] = number
                            if self.__solve_board():
                                return True
                            self.__board[f"{column}{row}"]["number"] = None
                    return False
        return True

    """Oculta la cantidad de números especificados del tablero"""
    def __remove_numbers(self, num_holes):
        while num_holes > 0:
            row, column = random.randint(1, 9), chr(ord('A') + random.randint(0, 8))
            if self.__board[f"{column}{row}"]["visible"]:
                self.__board[f"{column}{row}"]["visible"] = False
                self.__board[f"{column}{row}"]["modifiable"] = True
                num_holes -= 1

    def show_box(self, row: int, column: str):
        self.__board[f"{column}{row}"]["visible"] = True

    def delete_box(self, last_action: str):
        self.__board[last_action]["visible"] = False

    """Genera un Sudoku con un número determinado de casillas visibles"""
    def generate_sudoku(self, num_visibles: int=16):
        self.__fill_diagonal_boxes()
        self.__solve_board()
        num_holes = 81 - num_visibles
        self.__remove_numbers(num_holes)
        return self.get_board()

if __name__ == "__main__":
    sudoku = Sudoku()
    print(sudoku)
    #print(sudoku.get_board())
    sudoku.generate_sudoku()
    print(sudoku)
    #print(sudoku.get_board())