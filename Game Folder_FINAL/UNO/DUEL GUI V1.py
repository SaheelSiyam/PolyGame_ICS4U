import pygame
import sys
import time
import random

# Initialize Pygame
pygame.init()

# Function to read user data from the database file
def read_user_data(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
    return lines

# Get user index from command line argument
user_index = int(sys.argv[2])

# Read user data from the database
user_data = read_user_data("database.txt")

# Function to safely convert a string to an integer
def safe_int(value):
    try:
        return int(value)
    except ValueError:
        return int(float(value))

# Get Duel1, Duel2, and Duel3 from the user data
Duel1 = safe_int(user_data[user_index + 5])  # 5th line after username
Duel2 = safe_int(user_data[user_index + 6])  # 6th line after username
Duel3 = safe_int(user_data[user_index + 7])  # 7th line after username

# Set the dimensions of the window
window_width = 675
window_height = 450
window_size = (window_width, window_height)

# Create the window
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Duel Game")

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# Define fonts
font = pygame.font.Font(None, 25)

# Define Augment/Upgrade Class
class Augment:
    def __init__(self, name: str, damage: int):
        self.name = name
        self.damage = damage

# Augment bought
if Duel3 >= 1:
    Selected_Augment = Augment(name="Lacertus", damage=25)
    Duel3 -= 1
    print("Lacertus selected")
else:
    if Duel2 >= 1:
        Selected_Augment = Augment(name="Fortitudo", damage=10)
        Duel2 -= 1
        print("Fortitudo selected")
    else:
        if Duel1 >= 1:
            Selected_Augment = Augment(name="Potentia", damage=5)
            Duel1 -= 1
            print("Potentia selected")
        else:
            Selected_Augment = Augment(name="None", damage=0)
            print("None selected")

# Define the Character class
class Character:
    def __init__(self, name, hp, atk, defense, energy):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.defense = defense
        self.energy = energy
        self.augment_dmg = Selected_Augment.damage
        self.augment_name = Selected_Augment.name

    def basic_attack(self, target):
        atk_dmg = self.atk + self.augment_dmg
        target.hp -= max(atk_dmg - target.defense, 0)
        self.energy += 2
        target.energy += 1

    def ultimate_1(self, target):
        if self.energy >= 5:
            self.energy -= 5
            target.hp -= max(50 - target.defense, 0)
            return "Wind", "Ventus Furor"
        return "", ""

    def ultimate_2(self):
        if self.energy >= 5:
            self.energy -= 5
            self.defense += 15
            return "Water", "Aqua Tegumentum"
        return "", ""

    def ultimate_3(self):
        if self.energy >= 5:
            self.energy -= 5
            self.atk += 25
            return "Fire", "Ignis Auctio"
        return "", ""

    def ultimate_4(self):
        if self.energy >= 5:
            self.energy -= 5
            self.atk += 10
            self.hp += 40
            return "Ground", "Terrae Fortitudinis"
        return "", ""

# Create the characters
PA = Character(name="Aurum", hp=100, atk=1, defense=0, energy=0)
PB = Character(name="Caligo", hp=100, atk=1, defense=0, energy=1)

# Function to draw the character stats
def draw_character_stats(character, x, y):
    name_text = font.render(f"Name: {character.name}", True, white)
    hp_text = font.render(f"HP: {character.hp}", True, white)
    atk_text = font.render(f"ATK: {character.atk}", True, white)
    def_text = font.render(f"DEF: {character.defense}", True, white)
    energy_text = font.render(f"Energy: {character.energy}", True, white)
    augment_text = font.render(f"Augment: {character.augment_name}", True, white)

    screen.blit(name_text, (x, y))
    screen.blit(hp_text, (x, y + 20))
    screen.blit(atk_text, (x, y + 40))
    screen.blit(def_text, (x, y + 60))
    screen.blit(energy_text, (x, y + 80))
    screen.blit(augment_text, (x, y + 100))

# Function to draw buttons
def draw_button(text, x, y, width, height, color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    button_text = font.render(text, True, black)
    text_rect = button_text.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(button_text, text_rect)

# Function to handle player actions
def player_action(player, opponent, button_color):
    # Define button properties
    button_positions = [(70, 395), (140, 395), (250, 395), (360, 395), (470, 395)]
    button_sizes = [(60, 50), (100, 50), (100, 50), (100, 50), (120, 50)]
    button_texts = ["BA", "U1: Wind", "U2: Water", "U3: Fire", "U4: Ground"]

    # Draw buttons
    for pos, size, text in zip(button_positions, button_sizes, button_texts):
        draw_button(text, pos[0], pos[1], size[0], size[1], button_color)

    action_taken = False
    ultimate_element = ""
    ultimate_name = ""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for i, (x, y) in enumerate(button_positions):
                if x < mouse_pos[0] < x + button_sizes[i][0] and y < mouse_pos[1] < y + button_sizes[i][1]:
                    if i == 0:
                        player.basic_attack(opponent)
                    else:
                        if i == 1:
                            ultimate_element, ultimate_name = player.ultimate_1(opponent)
                        elif i == 2:
                            ultimate_element, ultimate_name = player.ultimate_2()
                        elif i == 3:
                            ultimate_element, ultimate_name = player.ultimate_3()
                        elif i == 4:
                            ultimate_element, ultimate_name = player.ultimate_4()
                    action_taken = True

    return action_taken, ultimate_element, ultimate_name

# Function to display the ultimate move name
def display_ultimate_name(element, name):
    screen.fill(black)
    ultimate_text = font.render(f"{element} Ultimate: {name}!", True, white)
    screen.blit(ultimate_text, (window_width // 2 - ultimate_text.get_width() // 2, window_height // 2 - ultimate_text.get_height() // 2))
    pygame.display.flip()
    time.sleep(2)

def game_over(winner):
    screen.fill(black)
    game_over_text = font.render(f"Game Over! {winner} wins!", True, white)
    screen.blit(game_over_text, (window_width // 2 - game_over_text.get_width() // 2, window_height // 2 - game_over_text.get_height() // 2))
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()

# Load character images
player1_image = pygame.image.load("Reshiram.png")
player2_image = pygame.image.load("Zekrom.png")
arena_image = pygame.image.load("Arena_Animated.gif")

# Resize character images
player1_image = pygame.transform.scale(player1_image, (250, 250))  # Adjust size as needed
player2_image = pygame.transform.scale(player2_image, (250, 250))  # Adjust size as needed
arena_image = pygame.transform.scale(arena_image, (800, window_height))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        mode = int(sys.argv[1])
    else:
        mode = 2  # Default mode

    # Main loop
    running = True
    player_turn = True  # True for Player 1's turn, False for Player 2's turn

    if mode == 1:
        while running:
            screen.fill(black)

            # Draw images
            screen.blit(arena_image, (-75, 0))  # Draw arena background
            screen.blit(player1_image, (0, 150))  # Draw Player 1 image
            screen.blit(player2_image, (425, 150))  # Draw Player 2 image

            draw_character_stats(PA, 10, 10)
            draw_character_stats(PB, 505, 10)

            if player_turn:
                action_taken, ultimate_element, ultimate_name = player_action(PA, PB, green)
            else:
                action_taken, ultimate_element, ultimate_name = player_action(PB, PA, red)

            if action_taken:
                if ultimate_element and ultimate_name:
                    display_ultimate_name(ultimate_element, ultimate_name)
                else:
                    if player_turn:
                        energy_text = font.render("ENERGY LOW", True, green)
                        screen.blit(energy_text, (260, 345))
                    else:
                        energy_text = font.render("ENERGY LOW", True, red)
                        screen.blit(energy_text, (260, 345))
                player_turn = not player_turn

            # Check for game over condition
            if PA.hp <= 0:
                game_over("Caligo")
            elif PB.hp <= 0:
                game_over("Aurum")

            pygame.display.flip()

            pygame.time.delay(100)

    if mode == 2:
        while running:
            screen.fill(black)

            # Draw images
            screen.blit(arena_image, (-75, 0))  # Draw arena background
            screen.blit(player1_image, (0, 150))  # Draw Player 1 image
            screen.blit(player2_image, (425, 150))  # Draw Player 2 image

            draw_character_stats(PA, 10, 10)
            draw_character_stats(PB, 505, 10)

            if player_turn:
                action_taken, ultimate_element, ultimate_name = player_action(PA, PB, green)
            else:
                # Simple AI: Randomly choose between basic attack and ultimate
                if PB.energy >= 5:
                    # Use ultimate if energy is sufficient
                    ultimate_choice = random.randint(1, 4)
                    if ultimate_choice == 1:
                        ultimate_element, ultimate_name = PB.ultimate_1(PA)
                    elif ultimate_choice == 2:
                        ultimate_element, ultimate_name = PB.ultimate_2()
                    elif ultimate_choice == 3:
                        ultimate_element, ultimate_name = PB.ultimate_3()
                    elif ultimate_choice == 4:
                        ultimate_element, ultimate_name = PB.ultimate_4()
                    action_taken = True
                else:
                    # Use basic attack if energy is low
                    PB.basic_attack(PA)
                    action_taken = True

            if action_taken:
                if ultimate_element and ultimate_name:
                    display_ultimate_name(ultimate_element, ultimate_name)
                else:
                    if player_turn:
                        energy_text = font.render("ENERGY LOW", True, green)
                        screen.blit(energy_text, (260, 345))
                    else:
                        energy_text = font.render("ENERGY LOW", True, red)
                        screen.blit(energy_text, (260, 345))
                player_turn = not player_turn

            # Check for game over condition
            if PA.hp <= 0:
                game_over("Caligo")
            elif PB.hp <= 0:
                game_over("Aurum")

            pygame.display.flip()

            pygame.time.delay(100)
