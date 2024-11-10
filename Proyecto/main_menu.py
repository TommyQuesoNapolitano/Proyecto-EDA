import pygame, difficult, instructions, main, credits

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sudoku - Menú Principal")

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
font = pygame.font.Font(None, 74)

def do_actions(pos, buttons, callback):
    for button, action in buttons:
        if button.collidepoint(pos):
            callback(action)
            break

def main_menu():
    running = True
    while running:
        screen.fill(WHITE)

        title_text = font.render("Sudoku", True, BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

        # Botones de opciones
        options = ["Seleccionar Dificultad", "Créditos", "Cómo Jugar"]
        buttons = []
        for idx, option in enumerate(options):
            option_text = font.render(option, True, BLACK)
            button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 250 + idx * 120, 400, 80)
            pygame.draw.rect(screen, GRAY, button_rect)
            screen.blit(option_text, (button_rect.x + 20, button_rect.y + 10))
            buttons.append((button_rect, option))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                do_actions(pos, buttons, lambda action: handle_option(action))

def handle_option(action):
    if action == "Seleccionar Dificultad":
        difficulty = difficult.main_menu()  # Asume que tienes una función para seleccionar dificultad
        main.game_screen(difficulty)  # Llama al juego con la dificultad seleccionada
    elif action == "Créditos":
        credits.show_credits()
    elif action == "Cómo Jugar":
        instructions.show_instructions()  # Llama a las instrucciones

main_menu()