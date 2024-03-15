import pygame
import sys
from moviepy.editor import VideoFileClip

# Constants
SQUARE_SIZE = 60
SCREEN_WIDTH = SQUARE_SIZE * 21  # 21 square
SCREEN_HEIGHT = SQUARE_SIZE * 12  # 12 square
LINE_WIDTH = 2
GRAY = (150, 150, 150)
BLACK = (0, 0, 0)

class Player:
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect()  #To know the position and size of the player's image.
        self.rect.topleft = (x * SQUARE_SIZE, y * SQUARE_SIZE)

    def draw(self, screen):
        screen.blit(self.image, self.rect)  # Image and position of image
def draw_environment(screen, rock_image, tilemap_image, players):

    # Draw the black squares and the gray lines of the environment
    for y in range(0, SCREEN_HEIGHT, SQUARE_SIZE):
        for x in range(0, SCREEN_WIDTH, SQUARE_SIZE):
            pygame.draw.rect(screen, BLACK, (x, y, SQUARE_SIZE, SQUARE_SIZE))
    for x in range(0, SCREEN_WIDTH, SQUARE_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT), LINE_WIDTH)
    for y in range(0, SCREEN_HEIGHT, SQUARE_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y), LINE_WIDTH)

    # Draw The borders
    for i in range(0, SCREEN_HEIGHT // SQUARE_SIZE):
        screen.blit(tilemap_image, (0, i * SQUARE_SIZE))
        screen.blit(tilemap_image, (SCREEN_WIDTH - SQUARE_SIZE, i * SQUARE_SIZE))
    for i in range(0, SCREEN_WIDTH // SQUARE_SIZE):
        screen.blit(tilemap_image, (i * SQUARE_SIZE, 0))
        screen.blit(tilemap_image, (i * SQUARE_SIZE, SCREEN_HEIGHT - SQUARE_SIZE))


    # Define list of coordinates of the stone tiles
    coordinates = [(3, 2), (3, 3), (3, 4), (2, 4), (1, 6), (2, 6), (3, 6), (5, 6), (5, 7), (5, 8), (3, 9), (4, 9), (5, 9),
                   (10, 1), (10, 2), (10, 3), (10, 4), (10, 5), (9, 5), (8, 5), (11, 5), (12, 5), (13, 5), (12, 3), (13, 3),
                   (14, 3), (13, 1), (17, 2), (18, 2), (17, 5), (18, 5), (18, 6), (19, 6), (10, 7), (10, 9), (9, 8),
                   (11, 8), (15, 7), (15, 8), (15, 9), (16, 9), (17, 9), (18, 9), (17, 8), (18, 10)]

    for coord in coordinates:
        screen.blit(tilemap_image, (coord[0] * SQUARE_SIZE, coord[1] * SQUARE_SIZE))

    # Draw boxes
    corner_coordinates = [(13, 1), (5, 9), (18, 5)]

    for coord in corner_coordinates:
        screen.blit(rock_image, (coord[0] * SQUARE_SIZE, coord[1] * SQUARE_SIZE))

    # Draw players
    for player in players:
        player.draw(screen)

    #screen.blit(pygame.transform.scale(pygame.image.load("Images\BlueFire.png"), (SQUARE_SIZE, SQUARE_SIZE)), (10 * SQUARE_SIZE, 8 * SQUARE_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Intelligent Shooting Game")

    clip = VideoFileClip("Images\Obstacles\Fire.mp4")
    frame_iterator = clip.iter_frames()  # Get iterator for video frames
    clock = pygame.time.Clock()

    # Load player images
    player_images = []

    player_images.append(pygame.image.load("Images\Players\Player_1_2.png"))  # Blue Player
    player_images.append(pygame.image.load("Images\Players\Player_2_3.png"))  # Yellow Player
    player_images.append(pygame.image.load("Images\Players\Player_3_4.png"))  # Red Player
    player_images.append(pygame.image.load("Images\Players\Player_4_2.png"))  # Green Player

    for i in range(0, 4):
        player_images[i] = pygame.transform.scale(player_images[i], (50, 50))  # Resize to 50x50

    # Create player objects with fixed positions
    players = [
        Player(player_images[0], 5, 5),
        Player(player_images[1], 13, 2),
        Player(player_images[2], 2, 3),
        Player(player_images[3], 9, 7)
    ]

    # Load images and resize them
    Box = pygame.image.load("Images\Obstacles\Box.jpg")
    Box = pygame.transform.scale(Box, (SQUARE_SIZE, SQUARE_SIZE))

    tilemap_image = pygame.image.load("Images\Obstacles\Stone_Tile.jpg")  # Load the image
    tilemap_image = pygame.transform.scale(tilemap_image, (SQUARE_SIZE, SQUARE_SIZE))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))  # Fill the screen with white
        draw_environment(screen, Box, tilemap_image, players)  # Draw the environment

        # Get the next frame from the iterator
        frame = next(frame_iterator, None)
        if frame is None:
            frame_iterator = clip.iter_frames()  # Reset iterator if video ends
            frame = next(frame_iterator, None)

        # Convert the frame to a Pygame surface
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))  # Swap axes for correct display

        # Resize the frame as the square size
        frame_surface = pygame.transform.scale(frame_surface, (SQUARE_SIZE, SQUARE_SIZE))

        # Position of the fire video
        screen.blit(frame_surface, (10 * SQUARE_SIZE, 8 * SQUARE_SIZE))

        # Update the display
        pygame.display.flip() # For update the entire screen
        clock.tick(30)  # To regulate the speed of display frames

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
