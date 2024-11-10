import pygame, Project.game
# #import time

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("Sudoku - Selecciona Dificultad")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

font = pygame.font.Font(None, 74)
# difficulty: str = difficult.main_menu()
num_visibles = {"fácil": 16, "normal": 12, "difícil": 8}

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

def do_actions(pos, buttons: list, callback, *args_callback, **kwargs_callback) -> None:
    for button, action in buttons:
        if button.collidepoint(pos):
            callback(action, args_callback, kwargs_callback)
            break

def game_screen(difficulty):
    sudoku_board = Project.game.StackSudoku()
    sudoku_board.generate_sudoku(num_visibles.get(difficulty.lower()))

    remaining_attempts = 3
    timer = 0
    font = pygame.font.Font(None, 50)
    number_font = pygame.font.Font(None, 40)
    
    GRID_COLOR = BLACK
    TIMER_POS = (20, 20)
    ATTEMPTS_POS = (450, 20)
    DIFFICULTY_POS = (900, 20)
    
    running = True
    while running:
        timer += 1
        screen.fill(WHITE)
        
        timer_text = font.render(f"Tiempo: {get_time(timer)}", True, BLACK)
        attempts_text = font.render(f"Intentos restantes: {remaining_attempts}", True, BLACK)
        difficulty_text = font.render(f"Dificultad: {difficulty}", True, BLACK)
        
        screen.blit(timer_text, TIMER_POS)
        screen.blit(attempts_text, ATTEMPTS_POS)
        screen.blit(difficulty_text, DIFFICULTY_POS)
        
        # Dibujo del tablero
        board_x, board_y = 400, 80
        cell_size = 50
        for i in range(9):
            for j in range(9):
                x = board_x + j * cell_size + 2 * (j // 3)
                y = board_y + i * cell_size + 2 * (i // 3)

                cell = pygame.Rect(x, y, cell_size, cell_size)
                pygame.draw.rect(screen, GRID_COLOR, cell, 1)

                box = lambda i, j: sudoku_board.get_sudoku_board()[f"{chr(ord('A') + j)}{i + 1}"]
                number, visible = box(i, j)["number"], box(i, j)["visible"]
                if visible:
                    number_text = number_font.render(str(number), True, BLACK)
                    screen.blit(number_text, (x + 15, y + 10))
        
        # Opciones de acción
        actions = ["Pista", "Deshacer", "Notas", "Borrar"]
        action_buttons = []
        left = 300
        for action in actions:
            action_text = font.render(action, True, BLACK)
            width = action_text.get_size()[0] + 45
            button_rect = pygame.Rect(left, SCREEN_HEIGHT - 150, width, 60)
            left += width + 15
            pygame.draw.rect(screen, GRAY, button_rect)
            screen.blit(action_text, (button_rect.x + 20, button_rect.y + 10))
            action_buttons.append((button_rect, action))

        number_buttons = []
        for i in range(1, 10):
            button_rect = pygame.Rect(300 + (i - 1) * 75, SCREEN_HEIGHT - 75, 70, 60)  # Posicionar en una fila
            pygame.draw.rect(screen, GRAY, button_rect)
            number_text = font.render(str(i), True, BLACK)
            screen.blit(number_text, (button_rect.x + 25, button_rect.y + 10))
            number_buttons.append((button_rect, i))

        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                do_actions(pos, action_buttons, lambda action, *args, **kwargs: print(f"Has presionado el botón de: {action}"))
                do_actions(pos, number_buttons, lambda number, *args, **kwargs: print(f"Has presionado el botón con el número {number}"))

if __name__ == "__main__":
    game_screen("difícil")