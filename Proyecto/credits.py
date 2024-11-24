import pygame, Project.game as game

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colores
LIGHT_BLUE = (240, 240, 255)  # Fondo: Azul claro suave
DARK_BLUE = (30, 40, 80)  # Título: Azul oscuro
DARK_GRAY = (50, 50, 50)  # Texto explicativo: Gris oscuro
BRIGHT_BLUE = (70, 150, 250)  # Puntos de lista: Azul brillante
VIBRANT_BLUE = (0, 123, 255)  # Fondo de los botones: Azul vibrante
HOVER_BLUE = (0, 153, 255)  # Hover: Azul más claro
WHITE = (255, 255, 255)  # Texto de los botones: Blanco

font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 40)

credits_data = {
    "Developers": [
        {
            "name": "Jaziel Abraham Solís Real",
            "role": "Back-end",
            "age": 19,
            "social medias": {
                "GitHub": "",
                "Facebook": "",
                "Instagram": "",
                "LinkedIn": "",
                "YouTube": ""
            },
            "alias": "Hugu34"
        },
        {
            "name": "Miguel Angel Montes Santos",
            "role": "Front-end",
            "age": 19,
            "social medias": {
                "GitHub": "",
                "Facebook": "",
                "Instagram": "",
                "LinkedIn": "",
                "YouTube": ""
            },
            "alias": "Chelo"
        }
    ],
    "Algorithms": [
        {
            "name": "Backtracking",
            "description": "Backtracking is a problem-solving algorithmic technique that involves finding a solution incrementally by trying different options and undoing them if they lead to a dead end.",
            "author": "GeeksForGeeks",
            "link": "https://www.geeksforgeeks.org/backtracking-algorithms/"
        }
    ]
}


def draw_button(text, rect, base_color, hover_color):
    """Dibuja un botón con efecto de hover."""
    mouse_pos = pygame.mouse.get_pos()
    is_hovered = rect.collidepoint(mouse_pos)
    color = hover_color if is_hovered else base_color

    # Dibuja el botón
    pygame.draw.rect(screen, color, rect, border_radius=10)

    # Dibuja el texto centrado dentro del botón
    button_text = small_font.render(text, True, WHITE)
    screen.blit(button_text, (rect.x + (rect.width - button_text.get_width()) // 2,
                              rect.y + (rect.height - button_text.get_height()) // 2))
    return is_hovered


def show_credits() -> None:
    running = True
    y_offset = 100  # Espacio inicial desde el borde superior
    line_spacing = 40
    max_text_width = 1000  # Ancho máximo para el texto de los créditos

    # Botón "Regresar"
    back_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50)

    while running:
        screen.fill(LIGHT_BLUE)  # Fondo azul claro suave

        # Título de créditos
        credit_title = font.render("Créditos", True, DARK_BLUE)  # Título en azul oscuro
        screen.blit(credit_title, (SCREEN_WIDTH // 2 - credit_title.get_width() // 2, 50))

        y = y_offset + line_spacing

        # Mostrar Desarrolladores
        for dev in credits_data["Developers"]:
            dev_text = f"{dev['name']} - {dev['role']} (Alias: {dev['alias']}, Edad: {dev['age']})"
            dev_lines = game.render_text_wrapped(dev_text, small_font, DARK_GRAY, max_text_width)
            for line_surface in dev_lines:
                screen.blit(line_surface, (50, y))
                y += line_spacing

            for platform, link in dev["social medias"].items():
                if link:
                    social_text = f"{platform}: {link}"
                    social_lines = game.render_text_wrapped(social_text, small_font, DARK_GRAY, max_text_width)
                    for line_surface in social_lines:
                        screen.blit(line_surface, (80, y))
                        y += line_spacing
            y += line_spacing

        # Mostrar Algoritmos
        y += line_spacing  # Separador extra
        algo_title = small_font.render("Algoritmos:", True, DARK_BLUE)
        screen.blit(algo_title, (50, y))
        y += line_spacing
        for algo in credits_data["Algorithms"]:
            algo_text = f"{algo['name']}: {algo['description']}"
            algo_lines = game.render_text_wrapped(algo_text, small_font, DARK_GRAY, max_text_width)
            for line_surface in algo_lines:
                screen.blit(line_surface, (50, y))
                y += line_spacing

            author_text = f"Autor: {algo['author']}, Link: {algo['link']}"
            author_lines = game.render_text_wrapped(author_text, small_font, DARK_GRAY, max_text_width)
            for line_surface in author_lines:
                screen.blit(line_surface, (70, y))
                y += line_spacing

        # Dibujar el botón "Regresar"
        hovered_back = draw_button("Regresar", back_button_rect, VIBRANT_BLUE, HOVER_BLUE)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and hovered_back:
                # Regresar al menú anterior
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False


if __name__ == "__main__":
    show_credits()