import pygame

pygame.init()

# Configuración inicial de la pantalla
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sudoku - Selecciona Dificultad")

# Colores definidos como tuplas RGB
WHITE = (245, 245, 245)  # Fondo blanco suave
DARK_GRAY = (34, 34, 34)  # Texto del título
BUTTON_TEXT_COLOR = (255, 255, 255)  # Color del texto en los botones
PASTEL_GREEN = (100, 200, 100)  # Botón fácil
SOFT_ORANGE = (255, 165, 0)  # Botón normal
SOFT_PURPLE = (200, 100, 255)  # Botón difícil
SHADOW = (200, 200, 200)  # Sombra para botones
HOVER_MODIFIER = 20  # Intensidad de cambio de color en hover

# Fuente para los textos
font = pygame.font.Font(None, 74)


def select_difficulty():
    """
    Crea la pantalla inicial para seleccionar la dificultad.
    Genera una lista de botones con posiciones, texto y colores asociados.
    """
    screen.fill(WHITE)  # Limpia la pantalla con el color de fondo

    # Renderiza el título "Selecciona la Dificultad"
    title_text = font.render("Selecciona la Dificultad", True, DARK_GRAY)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

    # Lista de niveles de dificultad
    difficulties = ["Fácil", "Normal", "Difícil"]
    difficulty_buttons = []  # Lista para almacenar los botones generados
    button_colors = [PASTEL_GREEN, SOFT_ORANGE, SOFT_PURPLE]  # Colores correspondientes a cada botón

    # Genera los botones con sus propiedades
    for i, diff in enumerate(difficulties):
        text = font.render(diff, True, BUTTON_TEXT_COLOR)  # Renderiza el texto del botón
        button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 125, 250 + i * 100, 250, 80)  # Posición y tamaño del botón
        difficulty_buttons.append((button_rect, diff, button_colors[i]))  # Almacena el rectángulo, texto y color base

    return difficulty_buttons  # Retorna la lista de botones


def draw_buttons(buttons):
    """
    Dibuja los botones en pantalla con efectos de hover y sombra.
    - `buttons`: Lista de botones en formato (rect, texto, color base).
    """
    mouse_pos = pygame.mouse.get_pos()  # Obtiene la posición actual del mouse

    for button_rect, diff, base_color in buttons:
        # Detecta si el mouse está sobre el botón y ajusta el color
        is_hovered = button_rect.collidepoint(mouse_pos)
        color = tuple(min(255, c + HOVER_MODIFIER) if is_hovered else c for c in base_color)

        # Dibuja una sombra detrás del botón
        shadow_rect = pygame.Rect(button_rect.x + 5, button_rect.y + 5, button_rect.width, button_rect.height)
        pygame.draw.rect(screen, SHADOW, shadow_rect, border_radius=15)

        # Dibuja el botón con el color calculado
        pygame.draw.rect(screen, color, button_rect, border_radius=15)

        # Dibuja el texto centrado dentro del botón
        text = font.render(diff, True, BUTTON_TEXT_COLOR)
        screen.blit(text, (button_rect.x + (button_rect.width - text.get_width()) // 2,
                           button_rect.y + (button_rect.height - text.get_height()) // 2))


def main_menu():
    """
    Menú principal que permite seleccionar la dificultad del juego.
    Gestiona eventos y devuelve la dificultad seleccionada.
    """
    running = True
    difficulty = None  # Almacena la dificultad seleccionada
    difficulty_buttons = select_difficulty()  # Genera los botones de dificultad

    while running:
        screen.fill(WHITE)  # Limpia la pantalla con el color de fondo

        # Renderiza el título "Selecciona la Dificultad"
        title_text = font.render("Selecciona la Dificultad", True, DARK_GRAY)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

        # Dibuja los botones
        draw_buttons(difficulty_buttons)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Finaliza el programa si se cierra la ventana
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Verifica si se hizo clic en algún botón
                pos = event.pos
                for button, diff, _ in difficulty_buttons:
                    if button.collidepoint(pos):
                        difficulty = diff  # Guarda la dificultad seleccionada
                        running = False  # Cierra el menú

        pygame.display.flip()  # Actualiza la pantalla

    return difficulty  # Retorna la dificultad seleccionada


if __name__ == "__main__":
    # Inicia el menú principal y muestra la dificultad seleccionada en consola
    difficulty = main_menu()
    print(f"Dificultad seleccionada: {difficulty}")
