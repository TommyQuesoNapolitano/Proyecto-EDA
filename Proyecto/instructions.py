import pygame

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Instrucciones - Sudoku")

# Colores
LIGHT_BLUE = (240, 240, 255)  # Fondo: Azul claro suave
DARK_BLUE = (30, 40, 80)  # Título: Azul oscuro
DARK_GRAY = (50, 50, 50)  # Texto explicativo: Gris oscuro
BRIGHT_BLUE = (70, 150, 250)  # Puntos de lista: Azul brillante
VIBRANT_BLUE = (0, 123, 255)  # Fondo de los botones: Azul vibrante
HOVER_BLUE = (0, 153, 255)  # Hover: Azul más claro
WHITE = (255, 255, 255)  # Texto de los botones: Blanco

font = pygame.font.Font(None, 40)


def draw_button(text, rect, base_color, hover_color):
    """Dibuja un botón con efecto de hover."""
    mouse_pos = pygame.mouse.get_pos()
    is_hovered = rect.collidepoint(mouse_pos)
    color = hover_color if is_hovered else base_color

    # Dibuja el botón
    pygame.draw.rect(screen, color, rect, border_radius=10)

    # Dibuja el texto centrado dentro del botón
    button_text = font.render(text, True, WHITE)
    screen.blit(button_text, (rect.x + (rect.width - button_text.get_width()) // 2,
                              rect.y + (rect.height - button_text.get_height()) // 2))
    return is_hovered


def show_instructions():
    running = True
    instructions = [
        "Bienvenido al Sudoku.",
        "El objetivo es completar la cuadrícula de 9x9 con números del 1 al 9.",
        "Cada fila, columna y cuadrado de 3x3 debe contener los números 1-9 sin repetirse.",
        "",
        "Instrucciones:",
        "- Usa los botones en la pantalla para seleccionar un número y colocarlo.",
        "- No se utiliza el teclado.",
        "- Puedes usar las opciones: Pista, Deshacer, Notas y Borrar.",
        "- Tienes tres intentos para completar el Sudoku."
    ]

    # Botón "Regresar"
    back_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50)

    while running:
        screen.fill(LIGHT_BLUE)  # Fondo azul claro suave

        # Mostrar el título
        title_text = font.render("Instrucciones", True, DARK_BLUE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        # Mostrar cada línea de instrucciones
        for i, line in enumerate(instructions):
            instruction_text = font.render(line, True, DARK_GRAY if i < 4 else BRIGHT_BLUE)
            screen.blit(instruction_text, (50, 100 + i * 40))

        # Dibujar el botón "Regresar"
        hovered_back = draw_button("Regresar", back_button_rect, VIBRANT_BLUE, HOVER_BLUE)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and hovered_back:
                # Si se presiona el botón "Regresar"
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Si se presiona la tecla ESC
                running = False


if __name__ == "__main__":
    show_instructions()