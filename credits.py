import pygame, Project.game as game

pygame.init()

# Dimensiones de la pantalla
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colores definidos como tuplas RGB
LIGHT_BLUE = (240, 240, 255)  # Fondo: Azul claro suave
DARK_BLUE = (30, 40, 80)  # Título: Azul oscuro
DARK_GRAY = (50, 50, 50)  # Texto explicativo: Gris oscuro
BRIGHT_BLUE = (70, 150, 250)  # Puntos de lista: Azul brillante
VIBRANT_BLUE = (0, 123, 255)  # Fondo de los botones: Azul vibrante
HOVER_BLUE = (0, 153, 255)  # Hover: Azul más claro
WHITE = (255, 255, 255)  # Texto de los botones: Blanco

# Fuentes para el texto (definidas por tamaño)
font = pygame.font.Font(None, 74)  # Fuente grande para títulos
small_font = pygame.font.Font(None, 40)  # Fuente pequeña para texto explicativo

# Estructura de datos para los créditos del proyecto
credits_data = {
    # Lista de desarrolladores (developers)
    "Developers": [
        {
            "name": "Jaziel Abraham Solís Real",  # Nombre del desarrollador
            "role": "Back-end",  # Rol principal
            "age": 19,  # Edad del desarrollador
            "social medias": {  # Redes sociales del desarrollador
                "GitHub": "",
                "Facebook": "",
                "Instagram": "",
                "LinkedIn": "",
                "YouTube": ""
            },
            "alias": "Hugu34"  # Alias del desarrollador
        },
        {
            "name": "Miguel Angel Montes Santos",  # Nombre del desarrollador
            "role": "Front-end",  # Rol principal
            "age": 19,  # Edad del desarrollador
            "social medias": {  # Redes sociales del desarrollador
                "GitHub": "",
                "Facebook": "",
                "Instagram": "",
                "LinkedIn": "",
                "YouTube": ""
            },
            "alias": "Chelo"  # Alias del desarrollador
        }
    ],
    # Información de algoritmos utilizados en el proyecto
    "Algorithms": [
        {
            "name": "Backtracking",  # Nombre del algoritmo
            "description": "Backtracking is a problem-solving algorithmic technique that involves finding a solution incrementally by trying different options and undoing them if they lead to a dead end.",  # Descripción del algoritmo
            "author": "GeeksForGeeks",  # Fuente del algoritmo
            "link": "https://www.geeksforgeeks.org/backtracking-algorithms/"  # Enlace a información adicional
        }
    ]
}

def draw_button(text, rect, base_color, hover_color):
    """
    Dibuja un botón con texto y cambia de color al pasar el cursor.
    - `text`: Texto a mostrar en el botón.
    - `rect`: Rectángulo que define la posición y dimensiones del botón.
    - `base_color`: Color del botón en estado normal.
    - `hover_color`: Color del botón al pasar el cursor.
    """
    mouse_pos = pygame.mouse.get_pos()  # Obtiene la posición actual del mouse
    is_hovered = rect.collidepoint(mouse_pos)  # Verifica si el mouse está sobre el botón
    color = hover_color if is_hovered else base_color  # Cambia el color si está en hover

    # Dibuja el rectángulo del botón
    pygame.draw.rect(screen, color, rect, border_radius=10)

    # Renderiza el texto centrado dentro del botón
    button_text = small_font.render(text, True, WHITE)
    screen.blit(button_text, (rect.x + (rect.width - button_text.get_width()) // 2,
                              rect.y + (rect.height - button_text.get_height()) // 2))
    return is_hovered

def show_credits() -> None:
    """
    Muestra una pantalla con los créditos del proyecto:
    - Desarrolladores con su información detallada.
    - Algoritmos usados en el desarrollo del proyecto.
    """
    running = True
    y_offset = 100  # Espaciado inicial desde el borde superior
    line_spacing = 40  # Espaciado entre líneas
    max_text_width = 1000  # Ancho máximo para ajustar el texto de los créditos

    # Define un botón "Regresar" en la parte inferior central
    back_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50)

    while running:
        screen.fill(LIGHT_BLUE)  # Llena la pantalla con el color de fondo

        # Renderiza el título "Créditos"
        credit_title = font.render("Créditos", True, DARK_BLUE)
        screen.blit(credit_title, (SCREEN_WIDTH // 2 - credit_title.get_width() // 2, 50))

        y = y_offset + line_spacing  # Posición inicial del texto

        # Muestra información de desarrolladores
        for dev in credits_data["Developers"]:
            # Texto principal con información del desarrollador
            dev_text = f"{dev['name']} - {dev['role']} (Alias: {dev['alias']}, Edad: {dev['age']})"
            dev_lines = game.render_text_wrapped(dev_text, small_font, DARK_GRAY, max_text_width)
            for line_surface in dev_lines:
                screen.blit(line_surface, (50, y))
                y += line_spacing

            # Muestra las redes sociales asociadas si tienen contenido
            for platform, link in dev["social medias"].items():
                if link:  # Solo muestra redes sociales con enlaces válidos
                    social_text = f"{platform}: {link}"
                    social_lines = game.render_text_wrapped(social_text, small_font, DARK_GRAY, max_text_width)
                    for line_surface in social_lines:
                        screen.blit(line_surface, (80, y))
                        y += line_spacing
            y += line_spacing  # Espacio adicional entre desarrolladores

        # Muestra información de algoritmos utilizados
        y += line_spacing  # Espacio adicional antes de los algoritmos
        algo_title = small_font.render("Algoritmos:", True, DARK_BLUE)
        screen.blit(algo_title, (50, y))
        y += line_spacing
        for algo in credits_data["Algorithms"]:
            # Texto principal con nombre y descripción del algoritmo
            algo_text = f"{algo['name']}: {algo['description']}"
            algo_lines = game.render_text_wrapped(algo_text, small_font, DARK_GRAY, max_text_width)
            for line_surface in algo_lines:
                screen.blit(line_surface, (50, y))
                y += line_spacing

            # Autor y enlace del algoritmo
            author_text = f"Autor: {algo['author']}, Link: {algo['link']}"
            author_lines = game.render_text_wrapped(author_text, small_font, DARK_GRAY, max_text_width)
            for line_surface in author_lines:
                screen.blit(line_surface, (70, y))
                y += line_spacing

        # Renderiza el botón "Regresar"
        hovered_back = draw_button("Regresar", back_button_rect, VIBRANT_BLUE, HOVER_BLUE)

        pygame.display.flip()  # Actualiza la pantalla

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and hovered_back:
                # Acción de "Regresar" al menú anterior
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

if __name__ == "__main__":
    show_credits()
