import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
window_width = 675
window_height = 450
window_size = (window_width, window_height)

# Create the window
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Pygame Window")

# Define button text color
button_text_color = (255, 255, 255)  # White

# Load the database
database_path = "database.txt"

# Read the database contents
def read_database():
    with open(database_path, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

# Write the database contents
def write_database(lines):
    with open(database_path, 'w') as file:
        for line in lines:
            file.write(line + '\n')

# Extract user data from the database
def get_user_data(username, lines):
    try:
        index = lines.index(username)
        polycash = int(lines[index + 2])
        quantities = [float(lines[index + 3 + i]) for i in range(6)]
        return polycash, quantities
    except ValueError:
        return None, None

# Update user data in the database
def update_user_data(username, lines, polycash, quantities):
    try:
        index = lines.index(username)
        lines[index + 2] = str(polycash)
        for i in range(6):
            lines[index + 3 + i] = str(quantities[i])
    except ValueError:
        pass

# Initialize user data
username = "gg"  # Replace this with the actual username
database_lines = read_database()
PolyCash, quantities = get_user_data(username, database_lines)
if PolyCash is None:
    print("Username not found in the database")
    sys.exit()

# Initialize error message flag
error_message_displayed = False

# Define the button class
class Button:
    def __init__(self, x, y, width, height, text, button_color, button_hover_color, quantity_index):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.default_color = button_color
        self.hover_color = button_hover_color
        self.color = button_color
        self.amount = quantities[quantity_index]  # Initialize amount
        self.quantity_index = quantity_index
        self.cost = 50  # Default cost, can be customized for each button

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.SysFont(None, 36)
        text_surf = font.render(self.text, True, button_text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_hovered(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        return self.is_hovered() and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1

    def update_color(self):
        if self.is_hovered():
            self.color = self.hover_color
        else:
            self.color = self.default_color

def display_text(text, font_size, color, position, surface):
    # Create a font object
    font = pygame.font.Font(None, font_size)  # None specifies the default system font

    # Render text onto a surface
    text_surface = font.render(text, True, color)

    # Get the rectangle containing the text
    text_rect = text_surface.get_rect()

    # Set the text position
    text_rect.topleft = position

    # Blit the text surface onto the specified surface
    surface.blit(text_surface, text_rect)

# Create button instances with custom colors
buttons = [
    Button(5, 150, 200, 50, "Tank Speed 50P", (255, 0, 0), (155, 0, 0), 0),  # Red
    Button(5, 250, 200, 50, "Bullet Speed 50P", (255, 0, 0), (155, 0, 0), 1),  # Red
    Button(230, 150, 200, 50, "DMG+5 50P", (0, 255, 0), (0, 155, 0), 2),  # Green
    Button(230, 250, 200, 50, "DMG+10 100P", (0, 255, 0), (0, 155, 0), 3),  # Green
    Button(230, 350, 200, 50, "DMG+25 250P", (0, 255, 0), (0, 155, 0), 4),  # Green
    Button(455, 150, 200, 50, "Draw 4 50P", (0, 0, 255), (0, 0, 155), 5)  # Blue
]

# Create an Exit button
ExitButton = Button(575, 0, 100, 50, "Exit", (128, 128, 128), (64, 64, 64), -1)  # Grey

def click(button, string):
    global PolyCash, error_message_displayed
    if button.is_clicked(event):
        print(string)
        if PolyCash < button.cost:
            error_message_displayed = True  # Set the error message flag to True
        else:
            PolyCash -= button.cost
            button.amount += 1
            quantities[button.quantity_index] = button.amount
            update_user_data(username, database_lines, PolyCash, quantities)
            write_database(database_lines)
            print("Amount", button.amount)
            error_message_displayed = False  # Reset the error message flag

# Main loop
running = True
while running:
    # Fill the screen with a color
    screen.fill((0, 0, 0))  # RGB color: black

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        for button in buttons:
            click(button, f"{button.text} Clicked")

        if ExitButton.is_clicked(event):
            running = False

    for button in buttons:
        button.update_color()
        button.draw(screen)

    ExitButton.update_color()
    ExitButton.draw(screen)

    display_text("PolyStore", 75, (0, 255, 0), (10, 10), screen)

    display_text("PolyCash:", 50, (255, 255, 255), (300, 20), screen)
    display_text(str(PolyCash), 50, (255, 255, 255), (475, 20), screen)

    display_text("Territory", 50, (255, 0, 0), (45, 65), screen)
    display_text("Invaders", 50, (255, 0, 0), (50, 100), screen)
    display_text(str(buttons[0].amount), 30, (255, 0, 0), (215, 165), screen)
    display_text(str(buttons[1].amount), 30, (255, 0, 0), (215, 265), screen)

    display_text("Duel", 60, (0, 255, 0), (280, 90), screen)
    display_text(str(buttons[2].amount), 30, (0, 255, 0), (435, 165), screen)
    display_text(str(buttons[3].amount), 30, (0, 255, 0), (435, 265), screen)
    display_text(str(buttons[4].amount), 30, (0, 255, 0), (435, 365), screen)

    display_text("Uno", 60, (0, 0, 255), (500, 90), screen)
    display_text(str(buttons[5].amount), 30, (0, 0, 255), (660, 165), screen)

    # Display error message if the flag is True
    if error_message_displayed:
        display_text("Cannot Afford Item", 30, (255, 0, 0), (350, 60), screen)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
