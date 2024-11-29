try:
    from Project.sudoku import Sudoku
    from Project.sudokuExceptions import SudokuGameLost, SudokuValueException, SudokuGameWin
except ImportError:
    from sudoku import Sudoku
    from sudokuExceptions import SudokuGameLost, SudokuValueException, SudokuGameWin

class StackSudoku(Sudoku):
    def __init__(self, board=None):
        super().__init__(board)
        self.__actions = {}

    def get_sudoku_board(self):
        return self.get_board()

    def get_actions(self):
        return self.__actions
    
    def all_is_visible(self):
        return all(box['visible'] for box in self.get_sudoku_board().values())

    def is_valid_number(self, row: int, column: str, number: int, attempts: int) -> tuple[bool, int]:
        box = f"{column}{row}"
        is_valid = self.get_board()[box]['number'] == number
        if not is_valid:
            attempts -= 1

        if attempts == 0:
            raise SudokuGameLost("Lo sentimos, has perdido el juego, más suerte para la próxima")

        return is_valid, attempts

    def push_action(self, row: int | str, column: str, number: int) -> None:
        try:
            box = f"{column}{row}"
            self.__actions[box]
        except KeyError:
            self.__actions[box] = {'number': number}

    def delete_last_action(self) -> None:
        last_action = self.__actions.popitem()[0]
        self.delete_box(last_action[1], last_action[0])

    def delete_box_number(self, row: int | str, column: str) -> None:
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