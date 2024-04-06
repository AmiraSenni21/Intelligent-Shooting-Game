import pygame
import sys
import random
import time
import math

# Constants
SQUARE_SIZE = 60
SCREEN_WIDTH = SQUARE_SIZE * 21  # 21 squares
SCREEN_HEIGHT = SQUARE_SIZE * 12  # 12 squares
LINE_WIDTH = 2
GRAY = (150, 150, 150)
BLACK = (0, 0, 0)
NPCs_MOVE_DELAY = 0.5  # Speed of NPCs
PLAYER_MOVE_DELAY = 0.2  # The speed of player movement
Bullet_Time = 0.3  # Time between shots (in seconds)
ANGLE_OF_VIEW = 120  # in degrees
NUM_SENSORS = 6
Obstacles = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9),
            (0, 10), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0),
            (10, 0), (11, 0), (12, 0), (13, 0), (14, 0), (15, 0), (16, 0), (17, 0), (18, 0),
            (19, 0), (20, 0), (20, 0), (20, 1), (20, 2), (20, 3), (20, 4), (20, 5), (20, 6),
            (20, 7), (20, 8), (20, 9), (20, 10), (1, 11), (2, 11), (3, 11), (4, 11), (5, 11),
            (6, 11), (7, 11), (8, 11), (9, 11), (10, 11), (11, 11), (12, 11), (13, 11), (14, 11),
            (15, 11), (16, 11), (17, 11), (18, 11), (19, 11), (20, 11), (13, 1), (5, 9), (18, 5),
            (10, 8), (3, 2), (3, 3), (3, 4), (2, 4), (1, 6), (2, 6), (3, 6), (5, 6), (5, 7), (5, 8),
            (3, 9), (4, 9), (5, 9), (10, 1), (10, 2), (10, 3), (10, 4), (10, 5), (9, 5), (8, 5), (11, 5),
            (12, 5), (13, 5), (12, 3), (13, 3), (14, 3), (13, 1), (17, 2), (18, 2), (17, 5), (18, 5),
            (18, 6), (19, 6), (10, 7), (10, 9), (9, 8), (11, 8), (15, 7), (15, 8), (15, 9), (16, 9),
            (17, 9), (18, 9), (17, 8), (18, 10)]
class Player:
    def __init__(self, images, x, y, initial_image_index):
        self.images = images
        self.image_index = initial_image_index
        self.image = self.images[self.image_index]  # Initial image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * SQUARE_SIZE, y * SQUARE_SIZE)
        self.last_move_time = time.time()
        self.last_shot_time = time.time()
        self.shooting = False

        # Sensor properties
        self.angle = 0  # Initialize angle
        self.sensor_range = 120  # Set the initial range of the sensors
        self.sensor_angles = [i * ANGLE_OF_VIEW / (NUM_SENSORS - 1) - ANGLE_OF_VIEW / 2 for i in
                              range(NUM_SENSORS)]  # Calculate sensor angles
        self.sensors = [self.sensor_range] * NUM_SENSORS  # List to store sensor lengths
        self.sensor_color = (255, 255, 0)

    def update_sensors(self, obstacles):
        for i, angle in enumerate(self.sensor_angles):
            sensor_length = self.sensors[i]
            sensor_direction = pygame.Vector2(1, 0).rotate(self.angle + angle)
            end_point = self.rect.center + sensor_direction * self.sensor_range
            min_distance = self.sensor_range
            for obstacle in obstacles:
                closest_point = obstacle.clipline(self.rect.center, end_point)
                if closest_point:
                    distance = math.sqrt((closest_point[0][0] - self.rect.centerx) ** 2 +
                                         (closest_point[0][1] - self.rect.centery) ** 2)
                    min_distance = min(min_distance, distance)
            self.sensors[i] = min_distance
    def draw(self, screen, obstacles):
        obstacle_rects = [pygame.Rect(coord[0] * SQUARE_SIZE, coord[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                          for coord in obstacles]
        self.update_sensors(obstacle_rects)
        for i, angle in enumerate(self.sensor_angles):
            sensor_length = self.sensors[i]
            sensor_direction = pygame.Vector2(1, 0).rotate(self.angle + angle)
            end_point = self.rect.center + sensor_direction * sensor_length
            # Determine color based on sensor length
            if sensor_length < self.sensor_range:
                sensor_color = (255, 0, 0)  # Red if sensor gets smaller
            else:
                sensor_color = (255, 255, 0)  # else Yellow
            # Draw sensor line
            pygame.draw.line(screen, sensor_color, self.rect.center, end_point, 2)
            # Draw player image
            screen.blit(self.image, self.rect)

    def move(self, dx, dy, obstacles):
        current_time = time.time()
        if current_time - self.last_move_time >= PLAYER_MOVE_DELAY:
            # Calculate the new position
            new_x, new_y = self.rect.x + dx * SQUARE_SIZE, self.rect.y + dy * SQUARE_SIZE

            # Check if the new position is not colliding with obstacles
            if pygame.Rect(new_x, new_y, SQUARE_SIZE, SQUARE_SIZE) not in obstacles:
                # Update the position
                self.rect.x, self.rect.y = new_x, new_y

                # Update the image based on the direction of movement
                if dx > 0:
                    self.image_index = 3  # Right
                elif dx < 0:
                    self.image_index = 2  # Left
                elif dy > 0:
                    self.image_index = 1  # Down
                elif dy < 0:
                    self.image_index = 0  # Up

                self.image = self.images[self.image_index]
                self.last_move_time = current_time  # Update the last move time
                # Update the player's angle
                if dx != 0 or dy != 0:
                    self.angle = math.degrees(math.atan2(dy, dx))

    def random_move(self, obstacles):
        current_time = time.time()
        if current_time - self.last_move_time >= NPCs_MOVE_DELAY:
            # Choose a random direction
            dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            self.move(dx, dy, obstacles)

    def can_shoot(self):
        current_time = time.time()
        return current_time - self.last_shot_time >= Bullet_Time

    def last_shoot(self):
        self.last_shot_time = time.time()


class Bullet:
    def __init__(self, x, y, dx, dy, image):
        self.rect = image.get_rect()
        self.rect.center = (x, y)
        self.dx = dx
        self.dy = dy
        self.image = image

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def draw(self, screen):
        screen.blit(self.image, self.rect)

def shoot(player, bullets, bullet_image):
    if player.can_shoot():
        # Determine bullet direction based on player direction
        if player.image_index == 0:  # Up
            dx, dy = 0, -1
        elif player.image_index == 1:  # Down
            dx, dy = 0, 1
        elif player.image_index == 2:  # Left
            dx, dy = -1, 0
        elif player.image_index == 3:  # Right
            dx, dy = 1, 0

        # Create a bullet and add it to the bullets list
        bullet = Bullet(player.rect.centerx, player.rect.centery, dx * 25, dy * 25, bullet_image)
        bullets.append(bullet)  # This list is used to keep track of all the bullets currently active in the game.
        player.last_shoot()

def get_shooting_player(players):
    for player in players:
        if player.shooting:
            players.remove(player)
    return None  # Return None if no player is shooting

def check_bullet_collision(bullets, players, obstacle_rects):
    # Iterate through bullets
    for bullet in bullets[:]:
        # Check collision with players
        for player in players[1:]:
            if bullet.rect.colliderect(player.rect):
                # Remove bullet if it hits a player
                bullets.remove(bullet)
                #player.change_image("Images/Players/Blood.png")
                player.shooting = True
                get_shooting_player(players)
                break  # Break out of the inner loop to avoid checking other players

        # Check collision with obstacles
        for obstacle_rect in obstacle_rects:
            if bullet.rect.colliderect(obstacle_rect):
                # Remove bullet if it hits an obstacle
                bullets.remove(bullet)
                break  # Break out of the inner loop to avoid unnecessary checks

def draw_environment(screen, box_img, tile_img, players, Obstacles, bullets):

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

    for coord in Obstacles:
        screen.blit(tile_img, (coord[0] * SQUARE_SIZE, coord[1] * SQUARE_SIZE))

    #Draw Boxes
    boxes_coordinates = [(13,1), (5, 9), (18, 5), (10, 8)]
    for coord in boxes_coordinates:
        screen.blit(box_img, (coord[0] * SQUARE_SIZE, coord[1] * SQUARE_SIZE))

    # Draw players
    for player in players:
        player.draw(screen, Obstacles)

    # Draw bullets
    for bullet in bullets:
        bullet.draw(screen)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Intelligent Shooting Game")

    obstacle_rects = [pygame.Rect(coord[0] * SQUARE_SIZE, coord[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                      for coord in Obstacles]

    # Load player images
    player_images = []

    # Load images for each direction for each player
    for i in range(1, 6):

        images = []
        for j in range(1, 5):
            image_path = f"Images/Players/Player_{i}_{j}.png"
            image = pygame.image.load(image_path)
            image = pygame.transform.scale(image, (50, 50))  # Resize to 50x50
            images.append(image)
        player_images.append(images)

    # Create player objects with fixed positions
    players = [
        Player(player_images[0], 5, 5, 3),
        Player(player_images[1], 13, 2, 2),
        Player(player_images[2], 2, 3, 1),
        Player(player_images[3], 9, 7, 3),
        Player(player_images[4], 16, 8, 0)
    ]

    # Load images and resize them
    box_img = pygame.image.load("Images/Obstacles/Box.jpg")
    box_img = pygame.transform.scale(box_img, (SQUARE_SIZE, SQUARE_SIZE))

    tile_img = pygame.image.load("Images/Obstacles/Stone_Tile.jpg")  # Load the image
    tile_img = pygame.transform.scale(tile_img, (SQUARE_SIZE, SQUARE_SIZE))

    # Load bullet image
    bullet_image = pygame.image.load("Images/Obstacles/Bullet.png")
    bullet_image = pygame.transform.scale(bullet_image, (10, 10))

    # List to store bullets
    bullets = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Control player 1 with arrow keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            players[0].move(-1, 0, obstacle_rects)
        elif keys[pygame.K_RIGHT]:
            players[0].move(1, 0, obstacle_rects)
        elif keys[pygame.K_UP]:
            players[0].move(0, -1, obstacle_rects)
        elif keys[pygame.K_DOWN]:
            players[0].move(0, 1, obstacle_rects)


        # Random movement for NPCs players
        for player in players[1:]:
            player.random_move(obstacle_rects)

        # If user press F key
        if keys[pygame.K_f]:
            shoot(players[0], bullets, bullet_image)


        # Check bullet collision with players and obstacles
        check_bullet_collision(bullets, players, obstacle_rects)

        # Move and draw bullets
        for bullet in bullets:
            bullet.move()
            bullet.draw(screen)

        screen.fill((255, 255, 255))
        draw_environment(screen, box_img, tile_img, players, Obstacles, bullets)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()