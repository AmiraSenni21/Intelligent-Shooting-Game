import pygame
import sys
import random
import time
import math
import numpy as np

# Constants
SQUARE_SIZE = 60
SCREEN_WIDTH = SQUARE_SIZE * 21  # 21 squares
SCREEN_HEIGHT = SQUARE_SIZE * 12  # 12 squares
LINE_WIDTH = 2
GRAY = (150, 150, 150)
BLACK = (0, 0, 0)
NPCs_MOVE_DELAY = 0.4  # Speed of NPCs
PLAYER_MOVE_DELAY = 0.4  # The speed of player movement
Bullet_Time = 0.3  # Time between shots (in seconds)
ANGLE_OF_VIEW = 120  # in degrees
NUM_SENSORS = 6
bullets = []
bullet_image = pygame.image.load("Images/Obstacles/Bullet.png")
bullet_image = pygame.transform.scale(bullet_image, (10, 10))
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
obstacle_rects = [pygame.Rect(coord[0] * SQUARE_SIZE, coord[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                      for coord in Obstacles]
num_input_features = len(Obstacles) * 4
Neural_angle = 0
class NeuralNetwork:
    def __init__(self, num_input_features):
        # Initialize weights and biases for:
        # first hidden layer have 4 neurons
        self.weights1 = np.random.randn(num_input_features, 4)
        self.bias1 = np.random.randn(4)

        # second hidden layer have 5 neurons
        self.weights2 = np.random.randn(4, 5)
        self.bias2 = np.random.randn(5)

        # third hidden layer have 4 neurons
        self.weights3 = np.random.randn(5, 4)
        self.bias3 = np.random.randn(4)

        # angle output
        self.weights_angle = np.random.randn(4)
        self.bias_angle = np.random.randn()

        # direction output
        self.weights_direction = np.random.randn(4)
        self.bias_direction = np.random.randn()

        # shoot output
        self.weights_shoot = np.random.randn(4)
        self.bias_shoot = np.random.randn()

    # sigmoid function outputs values between 0 and 1.
    def sigmoid(self, x):
        x = np.clip(x, -500, 500)
        return 1 / (1 + np.exp(-x))

    def predict(self, obstacles, friends, enemies):
        # Convert each input list into numpy array
        obstacles = np.array(obstacles)
        friends = np.array(friends)
        enemies = np.array(enemies)

        # Flatten and concatenate the arrays
        inputs = np.concatenate((obstacles.flatten(), friends.flatten(), enemies.flatten()))

        # Calculate weighted sum of inputs and add bias for each neuron in first hidden layer
        layer1_outputs = self.sigmoid(np.dot(inputs, self.weights1) + self.bias1)

        # Calculate weighted sum of first hidden layer outputs and add bias for each neuron in second hidden layer
        layer2_outputs = self.sigmoid(np.dot(layer1_outputs, self.weights2) + self.bias2)

        # Calculate weighted sum of second hidden layer outputs and add bias for each neuron in third hidden layer
        layer3_outputs = self.sigmoid(np.dot(layer2_outputs, self.weights3) + self.bias3)

        # Calculate weighted sum of third hidden layer outputs and add bias for each action
        output_angle = self.sigmoid(np.dot(layer3_outputs, self.weights_angle) + self.bias_angle)
        output_direction = self.sigmoid(np.dot(layer3_outputs, self.weights_direction) + self.bias_direction)
        output_shoot = self.sigmoid(np.dot(layer3_outputs, self.weights_shoot) + self.bias_shoot)

        # Convert output to game actions
        angles = [-60, -36, -12, 0, 12, 36, 60]
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        angle = angles[int(output_angle * len(angles))]  # Convert to one of the angles
        direction = directions[int(output_direction * len(directions))]  # Convert to one of the directions
        shoot = round(output_shoot)  # Round to nearest integer (0 or 1)

        return angle, direction, shoot



class Player:
    def __init__(self, images, x, y, initial_image_index, team):
        self.network = NeuralNetwork(num_input_features)
        self.images = images
        self.image_index = initial_image_index
        self.image = self.images[self.image_index]  # Initial image
        self.image = pygame.transform.rotate(self.images[self.image_index], 0)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * SQUARE_SIZE, y * SQUARE_SIZE)
        self.last_move_time = time.time()
        self.last_shot_time = time.time()
        self.shooting = False
        self.x = x
        self.y = y
        self.last_rotation_time = time.time()
        self.team = team

        # Sensor properties
        self.angle = 0  # Initialize angle
        self.sensor_range = 120  # Set the initial range of the sensors
        self.sensor_angles = [i * ANGLE_OF_VIEW / (NUM_SENSORS - 1) - ANGLE_OF_VIEW / 2 for i in
                              range(NUM_SENSORS)]  # Calculate sensor angles
        self.sensors = [self.sensor_range] * NUM_SENSORS  # List to store sensor lengths
        self.sensor_color = (255, 255, 0)

        # Create a separate rectangle for collision detection
        self.collision_rect = pygame.Rect(self.rect.left, self.rect.top, SQUARE_SIZE, SQUARE_SIZE)

    def update_sensors(self, obstacles, players):
        for i, angle in enumerate(self.sensor_angles):
            sensor_length = self.sensor_range
            sensor_direction = pygame.Vector2(1, 0).rotate(self.angle + angle)
            closest_collision_distance = self.sensor_range
            closest_collision_type = None

            # Check for obstacles collision
            for obstacle in obstacles:
                closest_point = obstacle.clipline(self.rect.center,self.rect.center + sensor_direction * self.sensor_range)
                if closest_point:
                    distance = math.sqrt((closest_point[0][0] - self.rect.centerx) ** 2 +
                                         (closest_point[0][1] - self.rect.centery) ** 2)
                    if distance < closest_collision_distance:
                        closest_collision_distance = distance
                        closest_collision_type = 'obstacle'



            # Check for player collision
            for player in players:
                if player != self:  # Avoid checking collision with self
                    closest_point = player.rect.clipline(self.rect.center,
                                                         self.rect.center + sensor_direction * self.sensor_range)
                    if closest_point:
                        distance = math.sqrt((closest_point[0][0] - self.rect.centerx) ** 2 +
                                             (closest_point[0][1] - self.rect.centery) ** 2)
                        if distance < closest_collision_distance:
                            closest_collision_distance = distance
                            closest_collision_type = 'player'

                        # Only allow shooting if the closest collision is with a player
                        if closest_collision_type == 'player':
                            angle_image = 0
                            if self.sensor_angles[i] == -60:
                                angle_image = 60
                            elif self.sensor_angles[i] == -36:
                                angle_image = 36
                            elif self.sensor_angles[i] == 12 or self.sensor_angles[i] == -12:
                                angle_image = 0
                            elif self.sensor_angles[i] == 36:
                                angle_image = -36
                            elif self.sensor_angles[i] == 60:
                                angle_image = -60
                            else:
                                print("No case !")

                            if player.team != self.team:
                                center = self.rect.center
                                self.image = pygame.transform.rotate(self.images[self.image_index], Neural_angle)
                                self.rect = self.image.get_rect()
                                self.rect.center = center
                                # print("Shoooot")
                                # shoot(self, bullets, bullet_image, player.x, player.y,-Neural_angle)

            # Update sensor length
            self.sensors[i] = closest_collision_distance

            # Update sensor color based on length
            if closest_collision_distance < self.sensor_range:
                self.sensor_color = (255, 0, 0)  # Red if sensor gets smaller
            else:
                self.sensor_color = (255, 255, 0)  # Yellow if no intersection


    def draw(self, screen, obstacles, players):
        obstacle_rects = [pygame.Rect(coord[0] * SQUARE_SIZE, coord[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)for coord in obstacles]
        self.update_sensors(obstacle_rects, players)
        for i, angle in enumerate(self.sensor_angles):
            sensor_length = self.sensors[i]
            sensor_direction = pygame.Vector2(1, 0).rotate(self.angle + angle)
            end_point = self.collision_rect.center + sensor_direction * sensor_length

            # Determine color based on sensor length and player-player collision
            if sensor_length < self.sensor_range or sensor_length == 0:
                sensor_color = (255, 0, 0)  # Red if collision occurs
            # elif self.sensor_angles[i] > 0:
            #     sensor_color = (0, 255, 0) # Green if no collision
            else:
                sensor_color = (255, 255, 0)  # Yellow if no collision

            # Draw sensor line
            pygame.draw.line(screen, sensor_color, self.collision_rect.center, end_point, 2)

            # Draw green boxes around the player
            pygame.draw.rect(screen, (0, 255, 0), self.collision_rect, 2)

            # Draw player image
            screen.blit(self.image, self.collision_rect)

    def move(self, dx, dy, obstacles):
        current_time = time.time()
        if current_time - self.last_move_time >= PLAYER_MOVE_DELAY:
            # Calculate the new position
            new_x, new_y = self.collision_rect.x + dx * SQUARE_SIZE, self.collision_rect.y + dy * SQUARE_SIZE

            # Create a temporary rectangle for the new position
            new_rect = pygame.Rect(new_x, new_y, SQUARE_SIZE, SQUARE_SIZE)

            # Check if the new position is not colliding with obstacles
            if not any(new_rect.colliderect(obstacle) for obstacle in obstacle_rects):
                # Update the position
                self.collision_rect.x, self.collision_rect.y = new_x, new_y
                self.rect.center = self.collision_rect.center  # Keep the image centered on the collision rectangle

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

    def can_shoot(self):
        current_time = time.time()
        return current_time - self.last_shot_time >= Bullet_Time

    def last_shoot(self):
        self.last_shot_time = time.time()


class Bullet:
    def __init__(self, x, y, dx, dy, image, angle):
        self.rect = image.get_rect()
        self.rect.center = (x, y)

        # Convert angle to radians and rotate dx and dy
        rad = math.radians(angle)
        self.dx = dx * math.cos(rad) - dy * math.sin(rad)
        self.dy = dx * math.sin(rad) + dy * math.cos(rad)

        # Reduce speed of bullet
        speed_factor = 1.5  # Adjust this value to change the speed
        self.dx *= speed_factor
        self.dy *= speed_factor

        self.image = image

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def draw(self, screen):
        screen.blit(self.image, self.rect)


def shoot(player, bullets, bullet_image, dx, dy, angle):
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
        bullet = Bullet(player.rect.centerx, player.rect.centery, dx * 25, dy * 25, bullet_image, angle)
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
        for player in players[0:]:
            if bullet.rect.colliderect(player.rect):
                # Remove bullet if it hits a player
                bullets.remove(bullet)
                # player.change_image("Images/Players/Blood.png")
                player.shooting = True
                # get_shooting_player(players)
                break

        # Check collision with obstacles
        for obstacle_rect in obstacle_rects:
            if bullet.rect.colliderect(obstacle_rect):
                # Remove bullet if it hits an obstacle
                bullets.remove(bullet)
                break


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

    # Draw Boxes
    boxes_coordinates = [(13, 1), (5, 9), (18, 5), (10, 8)]
    for coord in boxes_coordinates:
        screen.blit(box_img, (coord[0] * SQUARE_SIZE, coord[1] * SQUARE_SIZE))

    # Draw players
    for player in players:
        player.draw(screen, Obstacles, players)

    # Draw bullets
    for bullet in bullets:
        bullet.draw(screen)



def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Intelligent Shooting Game")

    # Load player images
    player_images = []
    Team_1 = []
    Team_2 = []

    friends = []
    enemies = []

    # Load images for each direction for each player
    for i in range(1, 6):  # 5 players
        images = []
        for j in range(1, 5): # 4 positions
            image_path = f"Images/Players/Player_{i}_{j}.png"
            image = pygame.image.load(image_path)
            image = pygame.transform.scale(image, (50, 50))  # Resize to 50x50
            images.append(image)
        player_images.append(images)


    # Create player objects with fixed positions
    players = [
        Player(player_images[0], 5, 5, 3, 1),
        Player(player_images[1], 8, 2, 2, 2),
        Player(player_images[2], 2, 3, 1, 1),
        Player(player_images[3], 9, 7, 3, 2),
        Player(player_images[4], 16, 8, 0, 1)
    ]


    # Load images and resize them
    box_img = pygame.image.load("Images/Obstacles/Box.jpg")
    box_img = pygame.transform.scale(box_img, (SQUARE_SIZE, SQUARE_SIZE))

    tile_img = pygame.image.load("Images/Obstacles/Stone_Tile.jpg")  # Load the image
    tile_img = pygame.transform.scale(tile_img, (SQUARE_SIZE, SQUARE_SIZE))



    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for player in players:
            if player.team == 1:
                friends = [p.rect.center for p in Team_1 if p != player]  # Extract positions of friendly players
                enemies = [p.rect.center for p in Team_2]  # Extract positions of enemy players
            elif player.team == 2:
                friends = [p.rect.center for p in Team_2 if p != player]  # Extract positions of friendly players
                enemies = [p.rect.center for p in Team_1]  # Extract positions of enemy players

                # Use the network to predict the game actions
                angle, direction, shooting = player.network.predict(obstacle_rects, friends, enemies)

                # Update player's direction continuously
                player.x = direction[0]
                player.y = direction[1]
                player.move(player.x, player.y, Obstacles)
                Neural_angle = angle

                # Check if the neural network predicts shooting
                if shooting == 1:
                    shoot(player, bullets, bullet_image, player.x, player.y, -Neural_angle)


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


