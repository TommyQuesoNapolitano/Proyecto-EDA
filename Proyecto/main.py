import pygame, Project.game, random
from Project.game import StackSudoku
from Project.sudokuExceptions import SudokuValueException, SudokuGameLost
from typing import Callable, Any
#import time

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colores
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

TYPE_BUTTON = tuple[pygame.Rect, Any]
POSITIONS = tuple[int, int]
remaining_attempts = 3
timer = 0

font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)
number_font = pygame.font.Font(None, 40)

num_visibles = {"fácil": 16, "normal": 12, "difícil": 8}

box_positions: dict[str, pygame.Rect] = {}

def get_time(time: int) -> str:
    seconds = time // 500
    minutes = seconds // 60
    hours = minutes // 60
    minutes %= 60
    seconds %= 60
    text = ""

    if hours:
        text += f"{hours} h "

    if minutes:
        text += f"{minutes} min "
    
    text += f"{seconds} seg"

    return text

def update_ui(remaining_attempts: int, difficulty: str, TIMER_POS: POSITIONS, ATTEMPTS_POS: POSITIONS, DIFFICULTY_POS: POSITIONS, sudoku_board: StackSudoku, timer: int = 0) -> tuple[list[TYPE_BUTTON], list[TYPE_BUTTON], int]:
    timer += 1
    screen.fill(WHITE)

    # Mostrar tiempo, intentos y dificultad
    timer_text = button_font.render(f"Tiempo: {get_time(timer)}", True, DARK_GRAY)
    attempts_text = button_font.render(f"Intentos restantes: {remaining_attempts}", True, DARK_GRAY)
    difficulty_text = button_font.render(f"Dificultad: {difficulty}", True, DARK_GRAY)

    screen.blit(timer_text, TIMER_POS)
    screen.blit(attempts_text, ATTEMPTS_POS)
    screen.blit(difficulty_text, DIFFICULTY_POS)

    # Dibujo del tablero (cuadrícula)
    board_x, board_y = 400, 80
    cell_size = 50
    for i in range(9):
        for j in range(9):
            x = board_x + j * cell_size + 2 * (j // 3)
            y = board_y + i * cell_size + 2 * (i // 3)

            cell = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(screen, GRID_COLOR, cell, LINE_WIDTH)

            box = lambda i, j: sudoku_board.get_sudoku_board()[f"{chr(ord('A') + j)}{i + 1}"]
            box_positions[f"{chr(ord('A') + j)}{i + 1}"] = cell
            number, visible, modifiable = box(i, j)["number"], box(i, j)["visible"], box(i, j)["modifiable"]
            if visible:
                color = GENERATED_NUMBER_COLOR if not modifiable else NUMBER_COLOR
                number_text = number_font.render(str(number), True, color)
                screen.blit(number_text, (x + 15, y + 10))

    # Opciones de acción (botones)
    actions = ["Pista", "Deshacer", "Notas", "Borrar"]
    action_buttons: list[TYPE_BUTTON] = []
    left = 300
    action_button_colors = [SOFT_BLUE, PASTEL_GREEN, SOFT_ORANGE, SOFT_PURPLE]
    for idx, action in enumerate(actions):
        action_text = button_font.render(action, True, BUTTON_TEXT_COLOR)
        width = action_text.get_size()[0] + 45
        button_rect = pygame.Rect(left, SCREEN_HEIGHT - 150, width, 60)
        left += width + 15

        # Detectar hover
        mouse_pos = pygame.mouse.get_pos()
        color = tuple(min(255, c + HOVER_MODIFIER) if button_rect.collidepoint(mouse_pos) else c for c in action_button_colors[idx])

        # Sombra y color del botón
        shadow_rect = pygame.Rect(button_rect.x + 5, button_rect.y + 5, button_rect.width, button_rect.height)
        pygame.draw.rect(screen, SHADOW, shadow_rect, border_radius=15)
        pygame.draw.rect(screen, color, button_rect, border_radius=15)

        # Texto del botón
        screen.blit(action_text, (button_rect.x + 20, button_rect.y + 10))
        action_buttons.append((button_rect, action))

    # Botones de números (1-9)
    number_buttons: list[TYPE_BUTTON] = []
    for i in range(1, 10):
        button_rect = pygame.Rect(300 + (i - 1) * 75, SCREEN_HEIGHT - 75, 70, 60)

        # Detectar hover
        color = tuple(min(255, c + HOVER_MODIFIER) if button_rect.collidepoint(mouse_pos) else c for c in SOFT_BLUE)

        pygame.draw.rect(screen, color, button_rect)
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

    match option:
        case "Pista":
            boxes = list(box[0] for box in sudoku.get_sudoku_board().items() if not box[1]["visible"] and box[0] not in sudoku.get_actions().keys())

            try:
                box = random.choice(boxes)
                sudoku.show_box(box[1], box[0])
                sudoku.change_modifiable(box[1], box[0])
            except IndexError:
                print("No hay cajas ocultas para mostrar la pista")
            finally:
                return attempts, timer + 1
        case "Deshacer":
            try:
                sudoku.delete_last_action()
            except KeyError:
                print("No hay acciones que deshacer")
            finally:
                return attempts, timer + 1
        case "Notas":
            return attempts, timer + 1
        case "Borrar":
            while True:
                timer = update_ui(attempts, difficult, timer_pos, attempt_pos, difficult_pos, sudoku, timer)[2]
                try:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
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
                                return attempts, timer + 1
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                pos = event.pos
                                box = get_selected_box(pos)
                                is_valid, attempts = sudoku.is_valid_number(int(box[1]), box[0], option, attempts)
                                if is_valid:
                                    sudoku.push_action(box[1], box[0], option)
                                    sudoku.show_box(box[1], box[0])
                    except SudokuValueException:
                        pass
                    except SudokuGameLost:
                        raise SudokuGameLost

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

if __name__ == "__main__":
    try:
        game_screen("difícil")
    except KeyboardInterrupt:
        print("\nSudoku finalizado")
        #print(box_positions)