import pygame

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sudoku - Selecciona Dificultad")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

font = pygame.font.Font(None, 74)

def select_difficulty():
    screen.fill(WHITE)
    # Títulos
    title_text = font.render("Selecciona la Dificultad", True, BLACK)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))
    
    # Botones de dificultad
    difficulties = ["Fácil", "Normal", "Difícil"]
    difficulty_buttons = []
    for i, diff in enumerate(difficulties):
        text = font.render(diff, True, BLACK)
        button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 250 + i * 100, 250, 80)
        pygame.draw.rect(screen, GRAY, button_rect)
        screen.blit(text, (button_rect.x + 50, button_rect.y + 10))
        difficulty_buttons.append((button_rect, diff))

    pygame.display.flip()
    return difficulty_buttons

def main_menu():
    running = True
    difficulty = None
    difficulty_buttons = select_difficulty()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                for button, diff in difficulty_buttons:
                    if button.collidepoint(pos):
                        difficulty = diff
                        running = False

        pygame.display.flip()

    return difficulty

if __name__ == "__main__":
    difficulty = main_menu()
    print(difficulty)