# Intento de importación de las clases y excepciones necesarias del proyecto
try:
    from Project.sudoku import Sudoku
    from Project.sudokuExceptions import SudokuGameLost, SudokuValueException, SudokuGameWin
except ImportError:
    # Si no se encuentran en el paquete "Project", se busca en la misma carpeta
    from sudoku import Sudoku
    from sudokuExceptions import SudokuGameLost, SudokuValueException, SudokuGameWin

class StackSudoku(Sudoku):
    """
    Clase que extiende la funcionalidad del Sudoku base para añadir un registro
    de acciones realizadas en el tablero. Permite gestionar los valores de las casillas 
    y realizar un seguimiento de las acciones.
    """
    def __init__(self, board=None):
        super().__init__(board)
        # Diccionario que registra las acciones realizadas en el tablero.
        # Clave: coordenada (e.g., "A1"), Valor: diccionario con detalles de la acción
        self.__actions = {}

    def get_sudoku_board(self):
        """Devuelve el tablero actual del Sudoku."""
        return self.get_board()

    def get_actions(self):
        """Devuelve el registro de acciones realizadas en el tablero."""
        return self.__actions
    
    def all_is_visible(self):
        """
        Verifica si todas las casillas del tablero son visibles.
        Retorna True si todas las casillas tienen la propiedad 'visible' como True.
        """
        return all(box['visible'] for box in self.get_sudoku_board().values())

    def is_valid_number(self, row: int, column: str, number: int, attempts: int) -> tuple[bool, int]:
        """
        Verifica si un número es válido para una casilla específica del tablero.
        
        Args:
            row (int): Número de fila.
            column (str): Letra de la columna.
            number (int): Número que se quiere verificar.
            attempts (int): Intentos restantes del jugador.

        Returns:
            tuple[bool, int]: Un booleano indicando validez y los intentos restantes.
        
        Raises:
            SudokuGameLost: Si los intentos llegan a cero.
        """
        box = f"{column}{row}"  # Identificador único de la casilla
        is_valid = self.get_board()[box]['number'] == number
        if not is_valid:
            attempts -= 1

        if attempts == 0:
            raise SudokuGameLost("Lo sentimos, has perdido el juego, más suerte para la próxima")

        return is_valid, attempts

    def push_action(self, row: int | str, column: str, number: int) -> None:
        """
        Registra una acción en el tablero, guardando el número asignado a una casilla.
        
        Args:
            row (int | str): Número de fila o identificador.
            column (str): Letra de la columna.
            number (int): Número que se quiere registrar.
        """
        try:
            box = f"{column}{row}"
            self.__actions[box]
        except KeyError:
            # Se guarda la acción si no existe previamente en el registro
            self.__actions[box] = {'number': number}

    def delete_last_action(self) -> None:
        """
        Elimina la última acción registrada y actualiza el tablero en consecuencia.
        """
        last_action = self.__actions.popitem()[0]  # Recupera la última acción y elimina del registro
        self.delete_box(last_action[1], last_action[0])

    def delete_box_number(self, row: int | str, column: str) -> None:
        """
        Elimina el valor asignado a una casilla específica en el tablero.
        
        Args:
            row (int | str): Número de fila o identificador.
            column (str): Letra de la columna.
        
        Raises:
            SudokuValueException: Si la casilla no tiene un valor definido.
        """
        try:
            box = f"{column}{row}"
            if self.__actions[box]:
                self.__actions.pop(box)
                self.delete_box(row, column)
        except KeyError:
            raise SudokuValueException("La columna y/o fila especificadas no tenían un valor definido")

def render_text_wrapped(text, font, color, max_width):
    """
    Divide un texto largo en varias líneas según un ancho máximo, y renderiza cada línea.
    
    Args:
        text (str): Texto a renderizar.
        font: Fuente utilizada para renderizar el texto.
        color: Color del texto.
        max_width (int): Ancho máximo permitido para una línea.

    Returns:
        list: Lista de superficies renderizadas, una por cada línea de texto.
    """
    words = text.split(' ')
    lines = []
    current_line = []

    for word in words:
        current_line.append(word)
        line_width, _ = font.size(' '.join(current_line))
        
        if line_width > max_width:
            current_line.pop()  # Quitar la palabra que causó el desbordamiento
            lines.append(' '.join(current_line))
            current_line = [word]  # Comenzar una nueva línea con la palabra que causó el desbordamiento

    lines.append(' '.join(current_line))  # Agregar la última línea
    surfaces = [font.render(line, True, color) for line in lines]
    return surfaces

if __name__ == "__main__":
    import random
    # Diccionario de ejemplo para representar un tablero inicial de Sudoku.
    # Clave: coordenada (e.g., "A1"), Valor: número aleatorio entre 0 y 100
    diccionario = {}

    for column in "ABC":
        for row in range(1, 4):
            diccionario[f"{column}{row}"] = {'number': random.randint(0, 100)}

    # Ejemplos de uso del diccionario
    print(diccionario.popitem())  # Elimina y muestra el último elemento
    print(diccionario.popitem())
    print(diccionario.popitem())

    # Elimina elementos específicos por clave
    print(diccionario.pop('A1'))
    print(diccionario.pop('B2'))
