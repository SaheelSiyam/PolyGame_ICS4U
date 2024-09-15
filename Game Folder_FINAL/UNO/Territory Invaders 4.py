import pygame
import random
import time
import subprocess
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 675  # Screen width
SCREEN_HEIGHT = 450  # Screen height
ENEMY_SPEED = 2.0  # Speed of the enemy
WAVE_TIME = 50  # Time per wave in seconds
ENEMIES_PER_TYPE = 60  # Number of enemies of each type per wave

# Function to read user data from the database file
def read_user_data(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
    return lines

# Read user data from the database
user_data = read_user_data("database.txt")

if __name__ == "__main__":  # Check if the script is being run directly (not imported)
    if len(sys.argv) > 1:
        # Get user index from command line argument
        user_index = int(sys.argv[2])

        # Get PLAYER_SPEED and BULLET_SPEED from the user data
        PLAYER_SPEED = float(user_data[user_index + 3])  # Speed of the player
        BULLET_SPEED = float(user_data[user_index + 4])  # Speed of the bullet
    else:
        PLAYER_SPEED = 0.5
        BULLET_SPEED = 0.75

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Set up the screen
pygame.display.set_caption("Territory Invaders")  # Set the game title
font = pygame.font.Font("freesansbold.ttf", 32)  # Font for text
small_font = pygame.font.Font("freesansbold.ttf", 16)  # Font for small text
game_over_font = pygame.font.Font("freesansbold.ttf", 100)  # Font for game over text


class GameObject:
    def __init__(self, image_path, x, y, speed_x=0, speed_y=0):
        self.image = pygame.image.load(image_path)  # Load image
        self.x = x  # X position
        self.y = y  # Y position
        self.speed_x = speed_x  # Speed in X direction
        self.speed_y = speed_y  # Speed in Y direction
        self.width = self.image.get_width()  # Width of the image
        self.height = self.image.get_height()  # Height of the image

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))  # Draw the object on the screen

    def move(self):
        self.x += self.speed_x  # Move the object in X direction
        self.y += self.speed_y  # Move the object in Y direction

    def check_boundaries(self, width_limit):
        if self.x <= 0:  # Check left boundary
            self.x = 0
        elif self.x >= (width_limit - self.width):  # Check right boundary
            self.x = (width_limit - self.width)


class Player(GameObject):
    def __init__(self, image_path, x, y, controls, label):
        super().__init__(image_path, x, y)  # Initialize base class
        self.controls = controls  # Controls for the player
        self.bullets = []  # List to hold bullets
        self.label = label  # Label for the player

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:  # Key down event
            if event.key == self.controls.get('left'):  # Move left
                self.speed_x = -PLAYER_SPEED
            elif event.key == self.controls.get('right'):  # Move right
                self.speed_x = PLAYER_SPEED
            elif event.key == self.controls.get('shoot'):  # Shoot bullet
                self.shoot()
        elif event.type == pygame.KEYUP:  # Key up event
            if event.key == self.controls.get('left') or event.key == self.controls.get('right'):  # Stop moving
                self.speed_x = 0

    def shoot(self):
        bullet = GameObject("bullet.png", self.x, self.y, speed_y=-BULLET_SPEED)  # Create bullet object
        bullet_x = self.x + (self.width / 2) - (bullet.width / 2)  # Center bullet on tank
        bullet_y = self.y
        bullet.x = bullet_x  # Set bullet x position
        bullet.y = bullet_y  # Set bullet y position
        self.bullets.append(bullet)  # Add bullet to list

    def draw(self, screen):
        super().draw(screen)  # Draw the player
        for bullet in self.bullets:  # Draw all bullets
            bullet.draw(screen)
        label_surface = small_font.render(self.label, True, (255, 255, 255))  # Render label text
        screen.blit(label_surface, (self.x + self.width / 2 - label_surface.get_width() / 2, self.y + self.height + 5))  # Draw label under tank

    def move(self):
        super().move()  # Move the player
        for bullet in self.bullets:  # Move all bullets
            bullet.move()

    def update_bullets(self):
        updated_bullets = []
        for bullet in self.bullets:
            if bullet.y > 0:  # Keep only on-screen bullets
                updated_bullets.append(bullet)
        self.bullets = updated_bullets


class AIPlayer(Player):
    def __init__(self, image_path, x, y, label):
        controls = {}  # No controls needed for AI
        super().__init__(image_path, x, y, controls, label)
        self.shoot_interval = random.randint(60, 120)  # Interval for AI shooting
        self.move_interval = random.randint(30, 60)  # Interval for AI moving
        self.frame_count = 0

    def update(self):
        self.frame_count += 1
        if self.frame_count % self.move_interval == 0:
            self.speed_x = random.choice([-PLAYER_SPEED, PLAYER_SPEED])
            self.move_interval = random.randint(30, 60)
        if self.frame_count % self.shoot_interval == 0:
            self.shoot()
            self.shoot_interval = random.randint(60, 120)


class Enemy(GameObject):
    def __init__(self, image_path, x, y):
        speed_x = random.choice([-ENEMY_SPEED, ENEMY_SPEED])  # Random speed direction
        super().__init__(image_path, x, y, speed_x=speed_x, speed_y=70)  # Initialize base class

    def move(self, screen_width):
        self.x += self.speed_x  # Move enemy in X direction
        if self.x <= 0 or self.x >= (screen_width - self.width):  # Change direction at screen edge
            self.speed_x = -self.speed_x
            self.y += self.speed_y  # Move enemy down


class Game:
    def __init__(self, waves, mode="single_player"):
        self.mode = mode
        tank_y_position = SCREEN_HEIGHT - 70  # Y position for tanks, adjusted 20 pixels lower
        if mode == "single_player":
            player_x_position = SCREEN_WIDTH / 2 - 32  # Center position for single-player mode
            self.players = [
                Player("tank.png", player_x_position, tank_y_position, {
                    'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'shoot': pygame.K_UP
                }, "P1")
            ]
        elif mode == "two_player":
            player1_x_position = SCREEN_WIDTH / 2 - 100  # Left position for P1 in two-player mode
            player2_x_position = SCREEN_WIDTH / 2 + 68  # Right position for P2 in two-player mode
            self.players = [
                Player("tank.png", player1_x_position, tank_y_position, {
                    'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'shoot': pygame.K_UP
                }, "P1"),
                Player("tank.png", player2_x_position, tank_y_position, {
                    'left': pygame.K_a, 'right': pygame.K_d, 'shoot': pygame.K_w
                }, "P2")
            ]
        elif mode == "player_vs_ai":
            player_x_position = SCREEN_WIDTH / 2 - 100  # Left position for player
            ai_x_position = SCREEN_WIDTH / 2 + 68  # Right position for AI
            self.players = [
                Player("tank.png", player_x_position, tank_y_position, {
                    'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'shoot': pygame.K_UP
                }, "P1"),
                AIPlayer("tank.png", ai_x_position, tank_y_position, "AI")
            ]
        self.waves = waves  # Number of waves
        self.enemies = []  # List to hold enemies
        self.wave_start_time = time.time()  # Start time for waves
        self.current_wave = 1  # Current wave number
        self.score = [0, 0]  # Scores for players
        self.running = True  # Game running state
        self.is_game_over = False  # Game over state
        self.game_over_message = ""  # Game over message
        self.spawn_enemies()  # Spawn initial enemies

    def spawn_enemies(self):
        self.enemies = []
        self._spawn_wave_enemies(self.current_wave, 0, 0)

    def _spawn_wave_enemies(self, current_wave, enemy_type_index, count):
        enemy_types = ['ogre', 'alien', 'monster']

        if count >= ENEMIES_PER_TYPE:
            if enemy_type_index < min(current_wave, 3) - 1:
                self._spawn_wave_enemies(current_wave, enemy_type_index + 1, 0)
            return

        if enemy_type_index < min(current_wave, 3):
            enemy_type = enemy_types[enemy_type_index]
            enemy_x = random.randint(0, SCREEN_WIDTH - 64)
            enemy_y = random.randint(50, 160)
            self.enemies.append(Enemy(f"{enemy_type}.png", enemy_x, enemy_y))
            self._spawn_wave_enemies(current_wave, enemy_type_index, count + 1)

    def draw_text(self, text, x, y, font, color=(255, 255, 255)):
        text_surface = font.render(text, True, color)  # Render text
        screen.blit(text_surface, (x, y))  # Draw text on screen

    def check_collisions(self):
        remaining_enemies = self.enemies.copy()

        for player in self.players:
            updated_bullets = []
            for bullet in player.bullets:
                bullet_hit = False
                for enemy in remaining_enemies:
                    if bullet_collision(bullet, enemy):
                        self.score[self.players.index(player)] += 1
                        remaining_enemies.remove(enemy)
                        bullet_hit = True
                        break
                if not bullet_hit:
                    updated_bullets.append(bullet)
            player.bullets = updated_bullets

        self.enemies = remaining_enemies

    def display_winner(self):
        if self.mode == "single_player":
            self.game_over_message = f"Your Score: {self.score[0]}"
        else:
            if self.score[0] > self.score[1]:
                self.game_over_message = "P1 Wins!"
            elif self.score[1] > self.score[0]:
                self.game_over_message = "P2 Wins!" if self.mode == "two_player" else "AI Wins!"
            else:
                self.game_over_message = "It's a Tie!"
        self.game_over_screen()

    def game_over_screen(self):
        message_surface = game_over_font.render(self.game_over_message, True, (255, 255, 255))  # Render game over message
        message_x = (SCREEN_WIDTH - message_surface.get_width()) / 2  # Center the message horizontally
        message_y = (SCREEN_HEIGHT - message_surface.get_height()) / 2  # Center the message vertically
        screen.blit(message_surface, (message_x, message_y))  # Display game over message
        pygame.display.flip()  # Update display

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

    def game_over_check(self):
        for enemy in self.enemies:
            if enemy.y >= SCREEN_HEIGHT - 95:  # Check if enemy reached the bottom
                self.is_game_over = True
                self.game_over_message = "GAME OVER"
                self.display_winner()
                return True
        return False

    def run(self):
        while self.running:
            screen.fill((0, 0, 0))  # Clear the screen
            screen.blit(pygame.image.load("Territory 1.png"), (0, 0))  # Draw background

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Quit event
                    self.running = False
                for player in self.players:
                    if not isinstance(player, AIPlayer):  # Only handle events for human players
                        player.handle_event(event)  # Handle player events

            if not self.is_game_over:
                for player in self.players:
                    player.move()  # Move player
                    player.update_bullets()  # Update bullets
                    if isinstance(player, AIPlayer):  # Update AI player
                        player.update()

                self.check_collisions()  # Check for collisions

                for enemy in self.enemies:
                    enemy.move(SCREEN_WIDTH)  # Move enemies

                for player in self.players:
                    player.draw(screen)  # Draw players

                for enemy in self.enemies:
                    enemy.draw(screen)  # Draw enemies

                self.draw_text(f"Score P1: {self.score[0]}", 10, 10, font)  # Draw score for P1
                if len(self.players) > 1:
                    self.draw_text(f"Score P2: {self.score[1]}", 10, 50, font)  # Draw score for P2 or AI

                elapsed_time = time.time() - self.wave_start_time  # Calculate elapsed time
                remaining_time = max(0, WAVE_TIME - elapsed_time)  # Calculate remaining time
                self.draw_text(f"Time: {int(remaining_time)}", SCREEN_WIDTH - 150, 10, font)  # Draw time

                if remaining_time == 0 or len(self.enemies) == 0:  # Check if wave is over
                    self.current_wave += 1
                    if self.current_wave > self.waves:  # Check if all waves are completed
                        self.is_game_over = True
                        self.display_winner()
                        break
                    self.wave_start_time = time.time()  # Reset wave start time
                    self.spawn_enemies()  # Spawn new enemies

                if self.game_over_check():  # Check for game over
                    break
            else:
                self.game_over_screen()  # Display the game over screen if the game is over

            pygame.display.flip()  # Update the display
            pygame.time.Clock().tick(60)  # Limit frame rate


def bullet_collision(bullet, enemy):
    return (
            bullet.x < enemy.x + enemy.width and
            bullet.x + bullet.width > enemy.x and
            bullet.y < enemy.y + enemy.height and
            bullet.y + bullet.height > enemy.y
    )


if __name__ == "__main__":  # Check if the script is being run directly (not imported)
    if len(sys.argv) > 1:  # Check if there are command line arguments passed to the script
        mode = sys.argv[1]  # If there is an argument, use it to set the game mode
    else:  # If no arguments are passed
        mode = "single_player"  # Default to "single_player" mode
    game = Game(waves=3, mode=mode)  # Initialize the game with 3 waves and the selected mode
    game.run()  # Run the game
