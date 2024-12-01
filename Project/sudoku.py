import random
# Intento de importar las excepciones personalizadas desde el proyecto
try:
    from Project.sudokuExceptions import SudokuValueException
except ImportError:
    from sudokuExceptions import SudokuValueException

class Sudoku:
    """
    Clase base para un juego de Sudoku. 
    Administra un tablero representado como un diccionario, donde las claves son
    identificadores de casillas (e.g., "A1") y los valores son diccionarios con propiedades.
    """
    __A = ord('A')  # Representa el valor ASCII de la letra 'A'

    def __init__(self, board=None):
        """
        Inicializa un tablero de Sudoku.
        Args:
            board (dict, opcional): Un tablero predefinido. Si no se proporciona, 
            se genera un tablero vacío con claves de "A1" a "I9".
        """
        if board:
            self.__board = board
        else:
            # Genera claves para las casillas (e.g., "A1", "B2") y las inicializa con valores predeterminados.
            self.__board = [f"{chr(self.__A + j)}{i}" for j in range(9) for i in range(1, 10)]
            self.__board = {
                box: {
                    "visible": True,       # Indica si la casilla es visible
                    "number": None,        # Número asignado a la casilla (None si está vacía)
                    "modifiable": False    # Si el valor de la casilla puede modificarse
                } for box in self.__board
            }

    def __str__(self):
        """
        Representa el tablero como un string, mostrando los números organizados en filas y columnas.
        """
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
        """Devuelve el tablero actual del Sudoku como un diccionario."""
        return self.__board

    def __is_valid_movement(self, row: int, column: str, number: int) -> bool:
        """
        Verifica si un número puede colocarse en una casilla sin romper las reglas del Sudoku.
        Args:
            row (int): Fila de la casilla.
            column (str): Columna de la casilla.
            number (int): Número a colocar.
        Returns:
            bool: True si el movimiento es válido, False en caso contrario.
        """
        try:
            self.is_valid_row_and_column(row, column)
        except SudokuValueException:
            raise SudokuValueException

        # Verificación de conflictos en la fila y la columna
        for new_row in range(1, 10):
            new_column = chr(self.__A + new_row - 1)
            box_column = f"{new_column}{row}"
            box_row = f"{column}{new_row}"
            if self.__board[box_row]["number"] == number or self.__board[box_column]["number"] == number:
                return False

        # Verificación de conflictos en la subcuadrícula 3x3
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
        """
        Verifica si las coordenadas de fila y columna son válidas.
        Args:
            row (int | str): Fila de la casilla.
            column (str): Columna de la casilla.
        Returns:
            bool: True si las coordenadas son válidas.
        Raises:
            SudokuValueException: Si las coordenadas son inválidas.
        """
        try:
            box = f"{column}{row}"
            self.__board[box]
            return True
        except KeyError:
            raise SudokuValueException("La fila y/o columna especificada no son válidos")

    def __fill_box(self, row: int, column: str) -> None:
        """
        Rellena una subcuadrícula 3x3 con números aleatorios del 1 al 9.
        """
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        for new_row in range(3):
            for new_column in range(3):
                box = f"{chr(ord(column) + new_column)}{row + new_row}"
                self.__board[box]["number"] = numbers.pop()

    def __fill_diagonal_boxes(self) -> None:
        """
        Rellena las subcuadrículas diagonales (e.g., A1-C3, D4-F6, G7-I9) para facilitar el backtracking.
        """
        for row in range(1, 10, 3):
            self.__fill_box(row, chr(self.__A + row - 1))

    def __solve_board(self) -> None:
        """
        Rellena el tablero utilizando backtracking para resolverlo completamente.
        """
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
        """
        Oculta una cantidad especificada de números en el tablero, marcándolos como modificables.
        Args:
            num_holes (int): Número de casillas a ocultar.
        """
        while num_holes > 0:
            row, column = random.randint(1, 9), chr(self.__A + random.randint(0, 8))
            box = f"{column}{row}"
            if self.__board[box]["visible"]:
                self.__board[box]["visible"] = False
                self.__board[box]["modifiable"] = True
                num_holes -= 1

    def show_box(self, row: int | str, column: str) -> None:
        """Hace visible el valor de una casilla específica."""
        self.__board[f"{column}{row}"]["visible"] = True

    def delete_box(self, row: int | str, column: str) -> None:
        """Oculta el valor de una casilla específica."""
        self.__board[f"{column}{row}"]["visible"] = False

    def change_modifiable(self, row: int | str, column: str) -> None:
        """Establece la casilla como no modificable."""
        self.__board[f"{column}{row}"]["modifiable"] = False

    def generate_sudoku(self, num_visibles: int=16):
        """
        Genera un Sudoku con un número especificado de casillas visibles.
        Args:
            num_visibles (int): Número de casillas visibles en el tablero generado.
        """
        self.__fill_diagonal_boxes()
        self.__solve_board()
        num_holes = 81 - num_visibles
        self.__remove_numbers(num_holes)
        return self.get_board()

if __name__ == "__main__":
    sudoku = Sudoku()
    print(sudoku)  # Muestra el tablero inicial vacío
    sudoku.generate_sudoku()  # Genera un Sudoku con valores ocultos
    print(sudoku)  # Muestra el tablero generado