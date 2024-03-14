import pygame
import sys

# Constants
SQUARE_SIZE = 60
SCREEN_WIDTH = SQUARE_SIZE * 21  # 21 square
SCREEN_HEIGHT = SQUARE_SIZE * 12  # 12 square
LINE_WIDTH = 2
GRAY = (150, 150, 150)
BLACK = (0, 0, 0)


def draw_environment(screen, rock_image, tilemap_image):
    for y in range(0, SCREEN_HEIGHT, SQUARE_SIZE):
        for x in range(0, SCREEN_WIDTH, SQUARE_SIZE):
            pygame.draw.rect(screen, BLACK, (x, y, SQUARE_SIZE, SQUARE_SIZE))
    for x in range(0, SCREEN_WIDTH, SQUARE_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT), LINE_WIDTH)
    for y in range(0, SCREEN_HEIGHT, SQUARE_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y), LINE_WIDTH)

    # Draw Tilemap1 image on borders except for the corners
    for i in range(1, SCREEN_HEIGHT // SQUARE_SIZE - 1): #Handle with the left and right borders (excluding corners)
        screen.blit(tilemap_image, (0, i * SQUARE_SIZE))
        screen.blit(tilemap_image, (SCREEN_WIDTH - SQUARE_SIZE, i * SQUARE_SIZE))
    for i in range(1, SCREEN_WIDTH // SQUARE_SIZE - 1): #Handle with the top and bottom borders (excluding corners).
        screen.blit(tilemap_image, (i * SQUARE_SIZE, 0))
        screen.blit(tilemap_image, (i * SQUARE_SIZE, SCREEN_HEIGHT - SQUARE_SIZE))


    # Define list of coordinates
    coordinates = [(0, 0), (0, 11), (20, 0), (20, 11), (3, 2), (3, 3), (3, 4), (2, 4), (1, 6), (2, 6), (3, 6), (5, 6), (5, 7), (5, 8), (3, 9), (4, 9), (5, 9),
                   (10, 1), (10, 2), (10, 3), (10, 4), (10, 5), (9, 5), (8, 5), (11, 5), (12, 5), (13, 5), (12, 3), (13, 3),
                   (14, 3), (13, 1), (17, 2), (18, 2), (17, 5), (18, 5), (18, 6), (19, 6), (10, 7), (10, 9), (9, 8),
                   (11, 8), (15, 7), (15, 8), (15, 9), (16, 9), (17, 9), (18, 9), (17, 8), (18, 10)]

    for coord in coordinates:
        screen.blit(tilemap_image, (coord[0] * SQUARE_SIZE, coord[1] * SQUARE_SIZE))

    # Draw Fire Image
    corner_coordinates = [(13, 1), (5, 9), (18, 5)]

    for coord in corner_coordinates:
        screen.blit(rock_image, (coord[0] * SQUARE_SIZE, coord[1] * SQUARE_SIZE))

    screen.blit(pygame.transform.scale(pygame.image.load("Images\BlueFire.png"), (SQUARE_SIZE, SQUARE_SIZE)), (10 * SQUARE_SIZE, 8 * SQUARE_SIZE))
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Shooting Game")

    # Load images and resize them
    rock_image = pygame.image.load("Images\Box1.jpg")
    rock_image = pygame.transform.scale(rock_image, (SQUARE_SIZE, SQUARE_SIZE))

    tilemap_image = pygame.image.load("Images\StoneTilemap2.jpg")  # Load the image
    tilemap_image = pygame.transform.scale(tilemap_image, (SQUARE_SIZE, SQUARE_SIZE))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_environment(screen, rock_image, tilemap_image)
        pygame.display.flip()


if __name__ == "__main__":
    main()
