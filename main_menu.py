import pygame, difficult, instructions, main, credits
from Project.sudokuExceptions import SudokuGameLost, SudokuGameWin

pygame.init()

# Configuración de pantalla
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

# Fuentes para los textos
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)

def do_actions(pos, buttons, callback):
    """
    Itera sobre los botones y ejecuta una acción si el mouse colisiona con alguno.

    Parámetros:
    - pos: Coordenadas del mouse al hacer clic.
    - buttons: Lista de botones en el formato (pygame.Rect, acción asociada).
    - callback: Función a ejecutar con la acción como parámetro.
    """
    for button, action in buttons:
        if button.collidepoint(pos):  # Si el mouse está sobre el botón
            callback(action)  # Ejecuta la función con la acción
            break

def main_menu():
    """
    Pantalla principal del menú del juego.
    """
    try:
        running = True
        while running:
            # Fondo blanco
            screen.fill(WHITE)

            # Título del menú
            title_text = font.render("Sudoku", True, DARK_GRAY)
            screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

            # Opciones del menú
            options = ["Seleccionar Dificultad", "Créditos", "Cómo Jugar"]
            buttons = []  # Lista de botones con sus rectángulos y acciones
            button_colors = [PASTEL_GREEN, SOFT_ORANGE, SOFT_PURPLE]  # Colores de los botones
            left = SCREEN_WIDTH // 2 - 200  # Posición inicial horizontal
            mouse_pos = pygame.mouse.get_pos()  # Obtener posición del mouse

            for idx, option in enumerate(options):
                # Crear rectángulo del botón
                button_rect = pygame.Rect(left, 250 + idx * 120, 400, 80)

                # Efecto hover (cambia el brillo del botón)
                color = tuple(
                    min(255, c + HOVER_MODIFIER) if button_rect.collidepoint(mouse_pos) else c
                    for c in button_colors[idx]
                )

                # Sombra para el botón
                shadow_rect = pygame.Rect(button_rect.x + 5, button_rect.y + 5, button_rect.width, button_rect.height)
                pygame.draw.rect(screen, SHADOW, shadow_rect, border_radius=15)

                # Dibujar el botón principal con el color
                pygame.draw.rect(screen, color, button_rect, border_radius=15)

                # Texto del botón
                option_text = button_font.render(option, True, BUTTON_TEXT_COLOR)
                screen.blit(option_text, (button_rect.x + (button_rect.width - option_text.get_width()) // 2, 
                                          button_rect.y + (button_rect.height - option_text.get_height()) // 2))
                
                # Guardar botón y su acción
                buttons.append((button_rect, option))

            pygame.display.flip()  # Actualizar la pantalla

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Cerrar el programa
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:  # Detectar clics
                    pos = event.pos  # Posición del clic
                    do_actions(pos, buttons, lambda action: handle_option(action))
    except SudokuGameLost:
        # Manejo de la excepción si el jugador pierde
        main.lose_screen()
    except SudokuGameWin:
        # Manejo de la excepción si el jugador gana
        main.win_screen()

def handle_option(action):
    """
    Maneja las acciones seleccionadas desde el menú principal.

    Parámetro:
    - action: Opción seleccionada por el usuario.
    """
    if action == "Seleccionar Dificultad":
        difficulty = difficult.main_menu()  # Muestra el menú de selección de dificultad
        main.game_screen(difficulty)  # Inicia el juego con la dificultad seleccionada
    elif action == "Créditos":
        credits.show_credits()  # Muestra los créditos
    elif action == "Cómo Jugar":
        instructions.show_instructions()  # Muestra las instrucciones del juego

main_menu()
