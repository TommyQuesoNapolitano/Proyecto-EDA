import random
try:
    from Project.sudokuExceptions import SudokuValueException
except ImportError:
    from sudokuExceptions import SudokuValueException

class Sudoku:
    __A = ord('A')
    def __init__(self, board=None):
        if board:
            self.__board = board
        else:
            self.__board = [f"{chr(self.__A + j)}{i}" for j in range(9) for i in range(1, 10)]
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

    def __is_valid_movement(self, row: int, column: str, number: int) -> bool:
        """Verifica si \"number\" puede colocarse en \"board[row][col]\" sin romper las reglas de Sudoku"""
        try:
            self.is_valid_row_and_column(row, column)
        except SudokuValueException:
            raise SudokuValueException

        for new_row in range(1, 10):
            new_column = chr(self.__A + new_row - 1)
            box_column = f"{new_column}{row}"
            box_row = f"{column}{new_row}"

            if self.__board[box_row]["number"] == number or self.__board[box_column]["number"] == number:
                return False

        start_row = ((row - 1) // 3) * 3 + 1
        start_column = chr(((ord(column) - self.__A) // 3) * 3 + self.__A)

        for i in range(3):
            for j in range(3):
                current_row = start_row + i
                current_col = chr(ord(start_column) + j)
                box = f"{current_col}{current_row}"
                if self.__board[box]["number"] == number:
                    return False
        return True

    def is_valid_row_and_column(self, row: int | str, column: str) -> bool:
        """Verifica si la fila está entre \"1\" y \"9\" y si la columna está entre \"A\" e \"I\". Si no lo es devuelve una excepción de tipo sudokuValueException"""
        try:
            box = f"{column}{row}"
            self.__board[box]
            return True
        except KeyError:
            raise SudokuValueException("La fila y/o columna especificada no son válidos")

    def __fill_box(self, row: int, column: str) -> None:
        """Rellena una cuadrícula entera usando números aleatorios"""
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        for new_row in range(3):
            for new_column in range(3):
                box = f"{chr(ord(column) + new_column)}{row + new_row}"
                self.__board[box]["number"] = numbers.pop()

    def __fill_diagonal_boxes(self) -> None:
        """Rellena todas las cuadrículas diagonales en una dirección del juego para hacer más fácil el backtracking"""
        for row in range(1, 10, 3):
            self.__fill_box(row, chr(self.__A + row - 1))

    def __solve_board(self) -> None:
        """Rellena los espacios faltantes del sudoku haciendo uso del backtracking y las cuadrículas generadas anteriormente"""
        for column in "ABCDEFGHI":
            for row in range(1, 10):
                if self.__board[f"{column}{row}"]["number"] is None:
                    for number in range(1, 10):
                        if self.__is_valid_movement(row, column, number):
                            self.__board[f"{column}{row}"]["number"] = number
                            if self.__solve_board():
                                return True
                            self.__board[f"{column}{row}"]["number"] = None
                    return False
        return True

    def __remove_numbers(self, num_holes: int) -> None:
        """Oculta la cantidad de números especificados del tablero"""
        while num_holes > 0:
            row, column = random.randint(1, 9), chr(self.__A + random.randint(0, 8))
            box = f"{column}{row}"
            if self.__board[box]["visible"]:
                self.__board[box]["visible"] = False
                self.__board[box]["modifiable"] = True
                num_holes -= 1

    def show_box(self, row: int | str, column: str) -> None:
        self.__board[f"{column}{row}"]["visible"] = True

    def delete_box(self, row: int | str, column: str) -> None:
        self.__board[f"{column}{row}"]["visible"] = False

    def change_modifiable(self, row: int | str, column: str) -> None:
        self.__board[f"{column}{row}"]["modifiable"] = False

    def generate_sudoku(self, num_visibles: int=16):
        """Genera un Sudoku con un número determinado de casillas visibles"""
        self.__fill_diagonal_boxes()
        self.__solve_board()
        num_holes = 81 - num_visibles
        self.__remove_numbers(num_holes)
        return self.get_board()

if __name__ == "__main__":
    sudoku = Sudoku()
    print(sudoku)
    sudoku.generate_sudoku()
    print(sudoku)