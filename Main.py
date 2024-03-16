import pygame
import sys
from moviepy.editor import VideoFileClip
from pygame.locals import *

# Constants
SQUARE_SIZE = 60
SCREEN_WIDTH = SQUARE_SIZE * 21  # 21 squares
SCREEN_HEIGHT = SQUARE_SIZE * 12  # 12 squares
LINE_WIDTH = 2
GRAY = (150, 150, 150)
BLACK = (0, 0, 0)

class Player:
    def __init__(self, images, x, y, initial_image_index):
        self.images = images
        self.image_index = initial_image_index
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * SQUARE_SIZE, y * SQUARE_SIZE)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, dx, dy, obstacles):
        # Save the current position
        old_x, old_y = self.rect.x, self.rect.y

        # Move the player
        self.rect.x += dx * SQUARE_SIZE
        self.rect.y += dy * SQUARE_SIZE

        # Check for collisions with obstacles
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle):
                # If there is a collision, revert to the old position
                self.rect.x, self.rect.y = old_x, old_y
                return False

        # Change the player's image based on the direction
        if dx > 0:
            self.image_index = 3  # Right
        elif dx < 0:
            self.image_index = 2  # Left
        elif dy > 0:
            self.image_index = 1  # Down
        elif dy < 0:
            self.image_index = 0  # Up
        self.image = self.images[self.image_index]  # Set the appropriate image

        return True


def draw_environment(screen, rock_image, tile_img, players, coordinates):
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
        screen.blit(tile_img, (0, i * SQUARE_SIZE))
        screen.blit(tile_img, (SCREEN_WIDTH - SQUARE_SIZE, i * SQUARE_SIZE))
    for i in range(0, SCREEN_WIDTH // SQUARE_SIZE):
        screen.blit(tile_img, (i * SQUARE_SIZE, 0))
        screen.blit(tile_img, (i * SQUARE_SIZE, SCREEN_HEIGHT - SQUARE_SIZE))

    # Draw the inner squares
    for coord in coordinates:
        screen.blit(tile_img, (coord[0] * SQUARE_SIZE, coord[1] * SQUARE_SIZE))

    # Draw boxes
    corner_coordinates = [(13, 1), (5, 9), (18, 5)]

    for coord in corner_coordinates:
        screen.blit(rock_image, (coord[0] * SQUARE_SIZE, coord[1] * SQUARE_SIZE))

    # Draw players
    for player in players:
        player.draw(screen)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Intelligent Shooting Game")

    clip = VideoFileClip("Images/Obstacles/Fire.mp4")
    frame_iterator = clip.iter_frames()  # Get iterator for video frames
    clock = pygame.time.Clock()

    # Define list of coordinates of the stone tiles
    coordinates = [(3, 2), (3, 3), (3, 4), (2, 4), (1, 6), (2, 6), (3, 6), (5, 6), (5, 7), (5, 8), (3, 9), (4, 9),
                   (5, 9), (10, 1), (10, 2), (10, 3), (10, 4), (10, 5), (9, 5), (8, 5), (11, 5), (12, 5), (13, 5),
                   (12, 3), (13, 3), (14, 3), (13, 1), (17, 2), (18, 2), (17, 5), (18, 5), (18, 6), (19, 6), (10, 7),
                   (10, 9), (9, 8), (11, 8), (15, 7), (15, 8), (15, 9), (16, 9), (17, 9), (18, 9), (17, 8), (18, 10)]

    # Define list of coordinates for borders
    borders = [
        # From (0,0) to (0,11)
        [(0, y) for y in range(11)],
        # From (1,0) to (21,0)
        [(x, 0) for x in range(1, 21)],
        # From (20,0) to (20,20)
        [(20, y) for y in range(11)],
        # From (1,11) to (20,11)
        [(x, 11) for x in range(1, 21)],
    ]

    # Combine all border coordinates into one list
    borders = [coord for sublist in borders for coord in sublist]

    # Combine border and obstacle coordinates
    obstacle_coordinates = borders + coordinates

    # Generate obstacle rectangles
    obstacle_rects = [pygame.Rect(coord[0] * SQUARE_SIZE, coord[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                      for coord in obstacle_coordinates]

    # Load player images
    player_images = []

    # Load images for each direction for each player
    for i in range(1, 5):
        images = []
        for j in range(1, 5):
            image_path = f"Images/Players/Player_{i}_{j}.png"
            image = pygame.image.load(image_path)
            image = pygame.transform.scale(image, (50, 50))  # Resize to 50x50
            images.append(image)
        player_images.append(images)

    # Create player objects with fixed positions
    players = [
        Player(player_images[0], 5, 5, 0),
        Player(player_images[1], 13, 2, 2),
        Player(player_images[2], 2, 3, 1),
        Player(player_images[3], 9, 7, 3)
    ]

    # Load images and resize them
    rock_image = pygame.image.load("Images/Obstacles/Box.jpg")
    rock_image = pygame.transform.scale(rock_image, (SQUARE_SIZE, SQUARE_SIZE))

    tile_img = pygame.image.load("Images/Obstacles/Stone_Tile.jpg")  # Load the image
    tile_img = pygame.transform.scale(tile_img, (SQUARE_SIZE, SQUARE_SIZE))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    players[1].move(-1, 0, obstacle_rects)
                elif event.key == pygame.K_RIGHT:
                    players[1].move(1, 0, obstacle_rects)
                elif event.key == pygame.K_UP:
                    players[1].move(0, -1, obstacle_rects)
                elif event.key == pygame.K_DOWN:
                    players[1].move(0, 1, obstacle_rects)

        screen.fill((255, 255, 255))  # Fill the screen with white
        draw_environment(screen, rock_image, tile_img, players, coordinates)  # Draw the environment

        # Reset iterator if video ends
        frame = next(frame_iterator, None)
        if frame is None:
            frame_iterator = clip.iter_frames()
            frame = next(frame_iterator, None)

        # Convert the frame to a Pygame surface
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

        # Resize the frame as the square size
        frame_surface = pygame.transform.scale(frame_surface, (SQUARE_SIZE, SQUARE_SIZE))

        # Position of the fire video
        screen.blit(frame_surface, (10 * SQUARE_SIZE, 8 * SQUARE_SIZE))

        pygame.display.flip()  # For update the entire screen
        clock.tick(30)  # To regulate the speed of display frames
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
