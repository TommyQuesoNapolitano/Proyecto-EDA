import pygame
from Project.game import render_text_wrapped  # Función para renderizar texto con ajuste de líneas

pygame.init()

# Configuración de la pantalla
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Instrucciones - Sudoku")  # Título de la ventana

# Colores definidos como tuplas RGB
LIGHT_BLUE = (240, 240, 255)  # Fondo azul claro
DARK_BLUE = (30, 40, 80)  # Texto del título
DARK_GRAY = (50, 50, 50)  # Texto explicativo
BRIGHT_BLUE = (70, 150, 250)  # Puntos destacados
VIBRANT_BLUE = (0, 123, 255)  # Fondo del botón "Regresar"
HOVER_BLUE = (0, 153, 255)  # Color de hover del botón
WHITE = (255, 255, 255)  # Color del texto en los botones

# Fuente principal
font = pygame.font.Font(None, 40)


def draw_button(text, rect, base_color, hover_color):
    """
    Dibuja un botón con efecto de hover.
    - `text`: Texto del botón.
    - `rect`: Rectángulo que define la posición y tamaño del botón.
    - `base_color`: Color normal del botón.
    - `hover_color`: Color al pasar el mouse por encima del botón.
    """
    mouse_pos = pygame.mouse.get_pos()  # Obtiene la posición del mouse
    is_hovered = rect.collidepoint(mouse_pos)  # Detecta si el mouse está sobre el botón
    color = hover_color if is_hovered else base_color  # Cambia el color si está en hover

    # Dibuja el rectángulo del botón
    pygame.draw.rect(screen, color, rect, border_radius=10)

    # Dibuja el texto centrado en el botón
    button_text = font.render(text, True, WHITE)
    screen.blit(button_text, (rect.x + (rect.width - button_text.get_width()) // 2,
                              rect.y + (rect.height - button_text.get_height()) // 2))
    return is_hovered  # Devuelve True si el mouse está sobre el botón


def show_instructions():
    """
    Pantalla que muestra las instrucciones del juego Sudoku.
    Renderiza texto explicativo y un botón para regresar.
    """
    running = True  # Control del bucle principal

    # Lista de instrucciones
    instructions = [
        "Bienvenido al Sudoku.",
        "El objetivo es completar la cuadrícula de 9x9 con números del 1 al 9.",
        "Cada fila, columna y cuadrado de 3x3 debe contener los números 1-9 sin repetirse.",
        "",
        "Instrucciones:",
        "- Usa los botones en la pantalla para seleccionar un número y colocarlo.",
        "- Cuando selecciones una de los botones y este sea Borrar, Notas o un número del 1 al 9 la única forma para poder cambiar de opción es apretando la letra de escape (ESC).",
        "- Puedes usar las opciones: Pista, Deshacer, Notas y Borrar.",
        "- Tienes tres intentos para completar el Sudoku."
    ]
    # Cada elemento es una línea de texto. Algunas líneas están vacías para separar secciones.

    # Botón "Regresar"
    back_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50)

    while running:
        screen.fill(LIGHT_BLUE)  # Fondo de color azul claro

        # Título de la pantalla
        title_text = font.render("Instrucciones", True, DARK_BLUE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        k = 0  # Contador para ajustar líneas al usar render_text_wrapped
        # Renderiza cada línea de las instrucciones
        for i, line in enumerate(instructions):
            # Cambia el color según el contexto (texto normal o destacado)
            color = DARK_GRAY if i < 4 else BRIGHT_BLUE
            instruction_texts = render_text_wrapped(line, font, color, 1250)  # Ajusta el texto al ancho máximo
            for j, instruction_text in enumerate(instruction_texts):
                if j:  # Si la línea es una continuación, incrementa el desplazamiento vertical
                    k += 1
                screen.blit(instruction_text, (50, 100 + (i + k) * 40))

        # Dibuja el botón "Regresar" y verifica si está en hover
        hovered_back = draw_button("Regresar", back_button_rect, VIBRANT_BLUE, HOVER_BLUE)

        pygame.display.flip()  # Actualiza la pantalla

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Finaliza el programa
            elif event.type == pygame.MOUSEBUTTONDOWN and hovered_back:
                # Regresa al menú principal si se presiona el botón
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Permite salir con la tecla ESC
                running = False


# Punto de entrada del programa
if __name__ == "__main__":
    show_instructions()
