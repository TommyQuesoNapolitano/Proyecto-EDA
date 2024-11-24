import pygame

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sudoku - Selecciona Dificultad")

# Colores
WHITE = (245, 245, 245)
DARK_GRAY = (34, 34, 34)
BUTTON_TEXT_COLOR = (255, 255, 255)
PASTEL_GREEN = (100, 200, 100)
SOFT_ORANGE = (255, 165, 0)
SOFT_PURPLE = (200, 100, 255)
SHADOW = (200, 200, 200)
HOVER_MODIFIER = 20  # Incremento para el hover

font = pygame.font.Font(None, 74)


def select_difficulty():
    screen.fill(WHITE)
    # Título
    title_text = font.render("Selecciona la Dificultad", True, DARK_GRAY)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

    # Botones de dificultad
    difficulties = ["Fácil", "Normal", "Difícil"]
    difficulty_buttons = []
    button_colors = [PASTEL_GREEN, SOFT_ORANGE, SOFT_PURPLE]  # Colores para los botones

    for i, diff in enumerate(difficulties):
        text = font.render(diff, True, BUTTON_TEXT_COLOR)
        button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 125, 250 + i * 100, 250, 80)
        difficulty_buttons.append((button_rect, diff, button_colors[i]))  # Almacena el rect, texto y color base

    return difficulty_buttons


def draw_buttons(buttons):
    mouse_pos = pygame.mouse.get_pos()  # Obtiene la posición actual del mouse
    for button_rect, diff, base_color in buttons:
        # Detectar si el mouse está sobre el botón
        is_hovered = button_rect.collidepoint(mouse_pos)
        color = tuple(min(255, c + HOVER_MODIFIER) if is_hovered else c for c in base_color)

        # Dibuja la sombra
        shadow_rect = pygame.Rect(button_rect.x + 5, button_rect.y + 5, button_rect.width, button_rect.height)
        pygame.draw.rect(screen, SHADOW, shadow_rect, border_radius=15)

        # Dibuja el botón
        pygame.draw.rect(screen, color, button_rect, border_radius=15)

        # Dibuja el texto del botón
        text = font.render(diff, True, BUTTON_TEXT_COLOR)
        screen.blit(text, (button_rect.x + (button_rect.width - text.get_width()) // 2,
                           button_rect.y + (button_rect.height - text.get_height()) // 2))


def main_menu():
    running = True
    difficulty = None
    difficulty_buttons = select_difficulty()

    while running:
        screen.fill(WHITE)

        # Título
        title_text = font.render("Selecciona la Dificultad", True, DARK_GRAY)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

        # Dibujar botones
        draw_buttons(difficulty_buttons)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                for button, diff, _ in difficulty_buttons:
                    if button.collidepoint(pos):
                        difficulty = diff
                        running = False

        pygame.display.flip()

    return difficulty


if __name__ == "__main__":
    difficulty = main_menu()
    print(f"Dificultad seleccionada: {difficulty}")