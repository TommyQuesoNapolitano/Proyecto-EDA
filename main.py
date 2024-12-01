import pygame, Project.game, random, json, os
from Project.game import StackSudoku
from Project.sudokuExceptions import SudokuValueException, SudokuGameLost, SudokuGameWin
from typing import Callable, Any

pygame.init()

# Tamaño de la ventana del juego
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colores para los elementos del juego
WHITE = (245, 245, 245)
DARK_GRAY = (34, 34, 34)
SOFT_BLUE = (50, 150, 200)
BUTTON_TEXT_COLOR = (255, 255, 255)
PASTEL_GREEN = (100, 200, 100)
SOFT_ORANGE = (255, 165, 0)
SOFT_PURPLE = (200, 100, 255)
SHADOW = (200, 200, 200)
NUMBER_COLOR = (0, 0, 0)
GENERATED_NUMBER_COLOR = (255, 32, 32)
GRID_COLOR = (180, 180, 180)
LINE_WIDTH = 2
HOVER_MODIFIER = 20

# Tipado para botones y posiciones
TYPE_BUTTON = tuple[pygame.Rect, Any]  # Un botón es un rectángulo junto con su acción asociada
POSITIONS = tuple[int, int]  # Representa una posición (x, y)

# Número de intentos restantes del jugador
remaining_attempts = 3

# Temporizador global
timer = 0

# Fuentes para los textos del juego
font = pygame.font.Font(None, 74)  # Fuente principal
button_font = pygame.font.Font(None, 50)  # Fuente para los botones
number_font = pygame.font.Font(None, 40)  # Fuente para los números del tablero

# Número de casillas visibles en el tablero según la dificultad
num_visibles = {"fácil": 24, "normal": 18, "difícil": 12}

# Diccionario para almacenar las posiciones de las casillas del tablero
# Clave: Identificador único de la casilla (e.g., "A1"), Valor: pygame.Rect (posición en pantalla)
box_positions: dict[str, pygame.Rect] = {}

# Estados dinámicos de los botones
button_states = {
    "Notas": False,  # Botón para activar el modo de notas
    "Borrar": False,  # Botón para borrar una casilla
    **{i: False for i in range(1, 10)}  # Estados para los botones numéricos (1-9)
}

def lose_screen() -> None:
    """
    Pantalla mostrada cuando el jugador pierde la partida.
    """
    running = True
    while running:
        screen.fill(WHITE)

        # Texto de "Juego perdido"
        lose_text = font.render("¡Juego Perdido!", True, DARK_GRAY)
        screen.blit(lose_text, ((SCREEN_WIDTH - lose_text.get_width()) // 2, SCREEN_HEIGHT // 3))

        # Botón para cerrar el juego
        close_text = button_font.render("Cerrar", True, BUTTON_TEXT_COLOR)
        close_button = pygame.Rect((SCREEN_WIDTH - close_text.get_width() - 40) // 2, SCREEN_HEIGHT // 2, close_text.get_width() + 40, 60)
        pygame.draw.rect(screen, SOFT_ORANGE, close_button, border_radius=10)
        screen.blit(close_text, (close_button.x + 20, close_button.y + 10))

        # Eventos para cerrar el juego
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if close_button.collidepoint(event.pos):
                    running = False

        pygame.display.flip()

def win_screen() -> None:
    time_data = {"time": get_time(timer)}
    file_path = "times.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            try:
                times = json.load(file)
            except json.JSONDecodeError:
                times = []
    else:
        times = []

    times.append(time_data)
    with open(file_path, "w") as file:
        json.dump(times, file, indent=4)

    # Pantalla de victoria
    running = True
    while running:
        screen.fill(WHITE)

        # Texto de "Juego ganado"
        win_text = font.render("¡Felicidades, ganaste!", True, DARK_GRAY)
        screen.blit(win_text, ((SCREEN_WIDTH - win_text.get_width()) // 2, SCREEN_HEIGHT // 3))

        # Texto del tiempo
        time_text = button_font.render(f"Tu tiempo: {get_time(timer)}", True, DARK_GRAY)
        screen.blit(time_text, ((SCREEN_WIDTH - time_text.get_width()) // 2, SCREEN_HEIGHT // 3 + 100))

        # Botón para reiniciar
        restart_text = button_font.render("Reiniciar", True, BUTTON_TEXT_COLOR)
        restart_button = pygame.Rect((SCREEN_WIDTH - restart_text.get_width() - 40) // 2, SCREEN_HEIGHT // 2 + 50, restart_text.get_width() + 40, 60)
        pygame.draw.rect(screen, PASTEL_GREEN, restart_button, border_radius=10)
        screen.blit(restart_text, (restart_button.x + 20, restart_button.y + 10))

        # Botón para cerrar
        close_text = button_font.render("Cerrar", True, BUTTON_TEXT_COLOR)
        close_button = pygame.Rect((SCREEN_WIDTH - close_text.get_width() - 40) // 2, SCREEN_HEIGHT // 2 + 150, close_text.get_width() + 40, 60)
        pygame.draw.rect(screen, SOFT_ORANGE, close_button, border_radius=10)
        screen.blit(close_text, (close_button.x + 20, close_button.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    return
                if close_button.collidepoint(event.pos):
                    running = False

        pygame.display.flip()

def get_time(time: int) -> str:
    """
    Convierte el tiempo en ticks a un formato legible de horas, minutos y segundos.
    """
    seconds = time // 500
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    text = ""
    if hours:
        text += f"{hours} h "
    if minutes:
        text += f"{minutes} min "
    text += f"{seconds} seg"
    return text

def update_ui(remaining_attempts: int, difficulty: str, TIMER_POS: POSITIONS, ATTEMPTS_POS: POSITIONS, DIFFICULTY_POS: POSITIONS, sudoku_board: StackSudoku, timer: int = 0) -> tuple[list[TYPE_BUTTON], list[TYPE_BUTTON], int]:
    """
    Actualiza la interfaz del juego, incluyendo el tablero, botones y estado.
    """
    timer += 1
    screen.fill(WHITE)

    # Mostrar tiempo, intentos restantes y dificultad
    timer_text = button_font.render(f"Tiempo: {get_time(timer)}", True, DARK_GRAY)
    attempts_text = button_font.render(f"Intentos restantes: {remaining_attempts}", True, DARK_GRAY)
    difficulty_text = button_font.render(f"Dificultad: {difficulty}", True, DARK_GRAY)

    screen.blit(timer_text, TIMER_POS)
    screen.blit(attempts_text, ATTEMPTS_POS)
    screen.blit(difficulty_text, DIFFICULTY_POS)

    # Dibujo del tablero de Sudoku
    board_x, board_y = 400, 80  # Posición inicial del tablero
    cell_size = 50  # Tamaño de cada celda
    for i in range(9):  # Iterar por las filas
        for j in range(9):  # Iterar por las columnas
            x = board_x + j * cell_size + 2 * (j // 3)  # Posición x con márgenes
            y = board_y + i * cell_size + 2 * (i // 3)  # Posición y con márgenes

            # Dibujar la celda
            cell = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(screen, GRID_COLOR, cell, LINE_WIDTH)

            # Guardar la posición de la casilla en el diccionario
            box_positions[f"{chr(ord('A') + j)}{i + 1}"] = cell

            # Obtener datos de la casilla desde el tablero
            box = lambda i, j: sudoku_board.get_sudoku_board()[f"{chr(ord('A') + j)}{i + 1}"]
            number, visible, modifiable = box(i, j)["number"], box(i, j)["visible"], box(i, j)["modifiable"]

            # Dibujar el número si es visible
            if visible:
                color = GENERATED_NUMBER_COLOR if not modifiable else NUMBER_COLOR
                number_text = number_font.render(str(number), True, color)
                screen.blit(number_text, (x + 15, y + 10))

    # Crear botones de acciones (Pista, Deshacer, etc.)
    actions = ["Pista", "Deshacer", "Notas", "Borrar"]
    action_buttons = []
    left = 300
    action_button_colors = [SOFT_BLUE, PASTEL_GREEN, SOFT_ORANGE, SOFT_PURPLE]
    for idx, action in enumerate(actions):
        action_text = button_font.render(action, True, BUTTON_TEXT_COLOR)
        width = action_text.get_size()[0] + 45
        button_rect = pygame.Rect(left, SCREEN_HEIGHT - 150, width, 60)
        left += width + 15

        # Dibujar botón
        base_color = action_button_colors[idx]
        pygame.draw.rect(screen, base_color, button_rect, border_radius=15)
        screen.blit(action_text, (button_rect.x + 20, button_rect.y + 10))
        action_buttons.append((button_rect, action))

    # Crear botones numéricos (1-9)
    number_buttons = []
    for i in range(1, 10):
        button_rect = pygame.Rect(300 + (i - 1) * 75, SCREEN_HEIGHT - 75, 70, 60)
        pygame.draw.rect(screen, SOFT_BLUE, button_rect)
        number_text = button_font.render(str(i), True, BUTTON_TEXT_COLOR)
        screen.blit(number_text, (button_rect.x + 25, button_rect.y + 10))
        number_buttons.append((button_rect, i))

    pygame.display.flip()
    return action_buttons, number_buttons, timer

def get_selected_box(pos: int):
    for box, Button in box_positions.items():
        if Button.collidepoint(pos):
            return box
    else:
        raise SudokuValueException

def do_actions(pos: int, buttons: list[TYPE_BUTTON], callback: Callable):
    for button, action in buttons:
        if button.collidepoint(pos):
            result = callback(action)
            return result
    else:
        return remaining_attempts, timer + 1

def handle_option(option, *args, **kwargs) -> Any:
    sudoku: StackSudoku
    for arg in args:
        if isinstance(arg, StackSudoku):
            sudoku = arg
            break
    else:
        raise SudokuValueException("No se pasó ningún tablero")

    try:
        attempts: int = kwargs['attempts']
        difficult: str = kwargs['difficulty']
        timer_pos: tuple[int, int] = kwargs['timer_pos']
        attempt_pos: tuple[int, int] = kwargs['attempt_pos']
        difficult_pos: tuple[int, int] = kwargs["difficulty_pos"]
        timer: int = kwargs["timer"]
    except KeyError:
        raise SudokuValueException

    if option not in ["Pista", "Deshacer"]:
        button_states[option] = True

    match option:
        case "Pista":
            boxes = list(box[0] for box in sudoku.get_sudoku_board().items() if not box[1]["visible"] and box[0] not in sudoku.get_actions().keys())
            try:
                box = random.choice(boxes)
                sudoku.show_box(box[1], box[0])
                sudoku.change_modifiable(box[1], box[0])
                if sudoku.all_is_visible():
                    win_screen()
                return attempts, timer + 1
            except IndexError:
                quit()
        case "Deshacer":
            try:
                sudoku.delete_last_action()
            except KeyError:
                print("No hay acciones que deshacer")
            finally:
                return attempts, timer + 1
        case "Notas":
            timer = update_ui(attempts, difficult, timer_pos, attempt_pos, difficult_pos, sudoku, timer)[2]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    button_states[option] = False
                    return attempts, timer + 1
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    button_states[option] = False
                    return attempts, timer + 1
        case "Borrar":
            while True:
                timer = update_ui(attempts, difficult, timer_pos, attempt_pos, difficult_pos, sudoku, timer)[2]
                try:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            button_states[option] = False
                            return attempts, timer + 1
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                            button_states[option] = False
                            return attempts, timer + 1
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            pos = event.pos
                            board = sudoku.get_board()
                            actions = sudoku.get_actions()
                            box = get_selected_box(pos)
                            if board[box]["modifiable"] and board[box]["visible"] and box in actions.keys():
                                sudoku.delete_box_number(box[1], box[0])
                                break
                            else:
                                raise SudokuValueException
                except SudokuValueException:
                    print("En esa posición no hay una casilla para borrar o la casilla no es borrable o la casilla no tiene número")
        case _:
            if 1 <= option <= 9:
                while True:
                    timer = update_ui(attempts, difficult, timer_pos, attempt_pos, difficult_pos, sudoku, timer)[2]
                    try:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                button_states[option] = False
                                return attempts, timer + 1
                            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                button_states[option] = False
                                return attempts, timer + 1
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                pos = event.pos
                                box = get_selected_box(pos)
                                is_valid, attempts = sudoku.is_valid_number(int(box[1]), box[0], option, attempts)
                                if is_valid:
                                    sudoku.push_action(box[1], box[0], option)
                                    sudoku.show_box(box[1], box[0])
                                    if sudoku.all_is_visible():
                                        raise SudokuGameWin
                    except SudokuValueException:
                        pass
                    except SudokuGameLost:
                        raise SudokuGameLost
                    except SudokuGameWin:
                        raise SudokuGameWin

def game_screen(difficulty):
    global remaining_attempts, timer
    sudoku_board = Project.game.StackSudoku()
    sudoku_board.generate_sudoku(num_visibles.get(difficulty.lower()))
    
    TIMER_POS = (20, 20)
    ATTEMPTS_POS = (450, 20)
    DIFFICULTY_POS = (900, 20)
    
    running = True
    while running:
        action_buttons, number_buttons, timer = update_ui(remaining_attempts, difficulty, TIMER_POS, ATTEMPTS_POS, DIFFICULTY_POS, sudoku_board, timer)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                kwargs = {'attempts': remaining_attempts, 'difficulty': difficulty, 'timer_pos': TIMER_POS, 'difficulty_pos': DIFFICULTY_POS, 'attempt_pos': ATTEMPTS_POS, 'timer': timer}
                remaining_attempts, timer = do_actions(pos, action_buttons + number_buttons, lambda action: handle_option(action, sudoku_board, **kwargs))

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Resetear estados
                for key in button_states:
                    button_states[key] = False

if __name__ == "__main__":
    try:
        game_screen("difícil")
    except KeyboardInterrupt:
        print("\nSudoku finalizado")
        #print(box_positions)