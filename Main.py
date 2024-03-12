import pygame
import sys

# Constants
SCREEN_WIDTH = 1080  # 17 square * 60
SCREEN_HEIGHT = 660  # 11 square * 60
SQUARE_SIZE = 60
LINE_WIDTH = 2
GRAY = (150, 150, 150)
BLACK = (0, 0, 0)

def draw_environment(screen):
    for y in range(0, SCREEN_HEIGHT, SQUARE_SIZE):
        for x in range(0, SCREEN_WIDTH, SQUARE_SIZE):
            pygame.draw.rect(screen, BLACK, (x, y, SQUARE_SIZE, SQUARE_SIZE))
    for x in range(0, SCREEN_WIDTH, SQUARE_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT), LINE_WIDTH)
    for y in range(0, SCREEN_HEIGHT, SQUARE_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y), LINE_WIDTH)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Shooting Game")

    # Load image and resize it
    image = pygame.image.load("Images\Rock1.jpg")
    image = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((255, 255, 255))  # Fill the screen with white
        draw_environment(screen)

        # Blit the image onto the screen at position (3, 7)
        screen.blit(image, (3 * SQUARE_SIZE, 7 * SQUARE_SIZE))
        screen.blit(image, (7 * SQUARE_SIZE, 2 * SQUARE_SIZE))

        pygame.display.flip()

if __name__ == "__main__":
    main()
