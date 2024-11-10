try:
    from Project.sudoku import Sudoku
    from Project.sudokuExceptions import SudokuGameLost, SudokuValueException
except ImportError:
    from sudoku import Sudoku
    from sudokuExceptions import SudokuGameLost, SudokuValueException

class StackSudoku(Sudoku):
    def __init__(self, board=None):
        super().__init__(board)
        self.__actions = {}

    """Returns a sudoku's board, using Sudoku's class"""
    def get_sudoku_board(self):
        return self.get_board()

    """Check if the number already exists in the row or column, if not the user lost an attempt. If user doesn't have any attempt it'll raise an exception of tye SudokuLostGame"""
    def is_valid_number(self, *args, attempts: int, row: int, column: str, number: int) -> bool:
        is_valid = self.is_valid_movement(row, column, number)
        if not is_valid:
            attempts -= 1
        else:
            self.show_box(row, column)
            self.__push_action(row, column)

        if attempts == 0:
            raise SudokuGameLost("Lo sentimos, has perdido el juego, más suerte para la próxima")

        return is_valid

    def __push_action(self, row: int, column: str, number: int) -> None:
        try:
            box = f"{column}{row}"
            if self.__actions[box]:
                return
            self.__actions[box] = {'number': number}
        except KeyError:
            pass

    def delete_last_action(self) -> None:
        last_action = self.__actions.popitem()[0]
        self.delete_box(last_action[1], last_action[0])
    
    def delete_box_number(self, row: int, column: str) -> None:
        try:
            box = f"{column}{row}"
            if self.__actions[box]:
                self.__actions.pop(box)
                self.delete_box(row, column)
        except KeyError:
            raise SudokuValueException("La columna y/o fila especificadas no tenían un valor definido")

def render_text_wrapped(text, font, color, max_width):
    words = text.split(' ')
    lines = []
    current_line = []

    for word in words:
        # Añadir la palabra a la línea actual y verificar si supera el ancho máximo
        current_line.append(word)
        line_width, _ = font.size(' '.join(current_line))
        
        if line_width > max_width:
            # Si supera el ancho, agregar la línea actual a 'lines' y empezar una nueva línea
            current_line.pop()  # Quitar la palabra que causó el desbordamiento
            lines.append(' '.join(current_line))
            current_line = [word]  # Comenzar una nueva línea con la palabra que causó el desbordamiento

    # Agregar la última línea
    lines.append(' '.join(current_line))

    # Renderizar cada línea como una superficie
    surfaces = [font.render(line, True, color) for line in lines]
    return surfaces

if __name__ == "__main__":
    import random
    diccionario = {}

    for column in "ABC":
        for row in range(1, 4):
            diccionario[f"{column}{row}"] = {'number': random.randint(0, 100)}

    print(diccionario.popitem())
    print(diccionario.popitem())
    print(diccionario.popitem())

    print(diccionario.pop('A1'))
    print(diccionario.pop('B2'))