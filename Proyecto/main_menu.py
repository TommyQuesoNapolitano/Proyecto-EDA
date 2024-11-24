import pygame, difficult, instructions, main, credits

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sudoku - Menú Principal")

# Colores
WHITE = (245, 245, 245)
DARK_GRAY = (34, 34, 34)
SOFT_BLUE = (50, 150, 200)
BUTTON_TEXT_COLOR = (255, 255, 255)
PASTEL_GREEN = (100, 200, 100)
SOFT_ORANGE = (255, 165, 0)
SOFT_PURPLE = (200, 100, 255)
SHADOW = (200, 200, 200)
HOVER_MODIFIER = 20  # Intensidad del hover

font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)


def do_actions(pos, buttons, callback):
    for button, action in buttons:
        if button.collidepoint(pos):
            callback(action)
            break


def main_menu():
    running = True
    while running:
        screen.fill(WHITE)

        # Título
        title_text = font.render("Sudoku", True, DARK_GRAY)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

        # Botones de opciones
        options = ["Seleccionar Dificultad", "Créditos", "Cómo Jugar"]
        buttons = []
        button_colors = [PASTEL_GREEN, SOFT_ORANGE, SOFT_PURPLE]
        left = SCREEN_WIDTH // 2 - 200
        mouse_pos = pygame.mouse.get_pos()  # Obtener posición del mouse

        for idx, option in enumerate(options):
            button_rect = pygame.Rect(left, 250 + idx * 120, 400, 80)
            
            # Detectar hover
            color = tuple(min(255, c + HOVER_MODIFIER) if button_rect.collidepoint(mouse_pos) else c for c in button_colors[idx])

            # Sombra
            shadow_rect = pygame.Rect(button_rect.x + 5, button_rect.y + 5, button_rect.width, button_rect.height)
            pygame.draw.rect(screen, SHADOW, shadow_rect, border_radius=15)

            # Dibujar botón con el color correspondiente
            pygame.draw.rect(screen, color, button_rect, border_radius=15)

            # Texto
            option_text = button_font.render(option, True, BUTTON_TEXT_COLOR)
            screen.blit(option_text, (button_rect.x + (button_rect.width - option_text.get_width()) // 2, 
                                      button_rect.y + (button_rect.height - option_text.get_height()) // 2))
            
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