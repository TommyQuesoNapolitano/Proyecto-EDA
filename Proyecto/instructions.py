import pygame

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Instrucciones - Sudoku")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
font = pygame.font.Font(None, 40)

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

    while running:
        screen.fill(WHITE)
        
        # Mostrar cada línea de instrucciones
        for i, line in enumerate(instructions):
            instruction_text = font.render(line, True, BLACK)
            screen.blit(instruction_text, (50, 50 + i * 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

if __name__ == "__main__":
    show_instructions()