import pygame
from moviepy.editor import VideoFileClip
import sys
import os
import subprocess

# Initialize Pygame
pygame.init()

# Set the screen dimensions
SCREEN_WIDTH = 675
SCREEN_HEIGHT = 450

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Poly Game")

# Load images and videos
base_dir = os.path.dirname(__file__)
image_dir = os.path.join(base_dir, "gui png files")
video_dir = os.path.join(base_dir, "gui mp4 files")

images = [
    os.path.join(image_dir, "2 user type.png"),
    os.path.join(image_dir, "3 sign in.png"),
    os.path.join(image_dir, "4 sign up.png"),
    os.path.join(image_dir, "5 select mode.png"),
    os.path.join(image_dir, "6 one player.png"),
    os.path.join(image_dir, "7 two player.png"),
    os.path.join(image_dir, "8 you vs ai.png"),
    os.path.join(image_dir, "9 polycash info.png"),
    os.path.join(image_dir, "10 about devs.png"),
    os.path.join(image_dir, "12 ad finished.png"),
    os.path.join(image_dir, "13 coming soon.png"),
]

videos = [
    os.path.join(video_dir, "1 start up.mp4"),
    os.path.join(video_dir, "2 user type.mp4"),
    os.path.join(video_dir, "3 sign in.mp4"),
    os.path.join(video_dir, "4 sign up.mp4"),
    os.path.join(video_dir, "5 select mode.mp4"),
    os.path.join(video_dir, "6 one player.mp4"),
    os.path.join(video_dir, "7 two player.mp4"),
    os.path.join(video_dir, "8 you vs ai.mp4"),
    os.path.join(video_dir, "9 polycash.mp4"),
    os.path.join(video_dir, "10 about devs.mp4"),
    os.path.join(video_dir, "11 rick roll.mp4"),
    os.path.join(video_dir, "13 coming soon.mp4"),
]

# Load screens
screens = [
    [videos[0], images[0]],
    [videos[1], images[0]],
    [videos[2], images[1]],
    [videos[3], images[2]],
    [videos[4], images[3]],
    [videos[5], images[4]],
    [videos[6], images[5]],
    [videos[7], images[6]],
    [videos[8], images[7]],
    [videos[9], images[8]],
    [videos[10], images[9]],
    [videos[11], images[10]],
]

# Updated Buttons
buttons = [
    # Screen 0 button(s) #
    # New User               # Returning User
    [[132, 171, 134, 200, 3], [406, 171, 134, 200, 2]],

    # Screen 1 button(s) #
    # New User               # Returning User
    [[132, 171, 134, 200, 3], [406, 171, 134, 200, 2]],

    # Screen 2 button(s) #
    # Back Button            # Go home page
    [[42, 89, 39, 39, 1], [293, 370, 88, 35, 4]],

    # Screen 3 button(s) #
    # Back Button            # Go sign in
    [[42, 89, 39, 39, 1], [293, 370, 88, 35, 2]],

    # Screen 4 button(s) #
    # PolyCash Info       # Log Out
    [[9, 18, 137, 20, 8], [594, 19, 72, 20, 1],
     # Two Player            # You vs AI              # Single Player
     [107, 172, 132, 201, 6], [269, 172, 132, 201, 7], [432, 172, 132, 201, 5],
     # About Devs        # Ad
     [370, 402, 156, 39, 9], [544, 402, 121, 39, 10]],

    # Screen 5 button(s) #
    # Back Button         # PolyCash Info       # Log Out
    [[42, 89, 39, 39, 4], [9, 18, 137, 20, 8], [594, 19, 72, 20, 1],
     # Territory Invaders     # Duel                   # UNO
     [107, 172, 132, 201, 5], [269, 172, 132, 201, 11], [432, 172, 132, 201, 5],
     # About Devs        # Ad                # Store
     [370, 402, 156, 39, 9], [544, 402, 121, 39, 10], [237, 402, 120, 39, 5]],

    # Screen 6 button(s) #
    # Back Button         # PolyCash Info       # Log Out
    [[42, 89, 39, 39, 4], [9, 18, 137, 20, 8], [594, 19, 72, 20, 1],
     # Territory Invaders     # Duel                   # UNO
     [107, 172, 132, 201, 6], [269, 172, 132, 201, 6], [432, 172, 132, 201, 11],
     # About Devs        # Ad                # Store
     [370, 402, 156, 39, 9], [544, 402, 121, 39, 10], [237, 402, 120, 39, 6]],

    # Screen 7 button(s) #
    # Back Button         # PolyCash Info       # Log Out
    [[42, 89, 39, 39, 4], [9, 18, 137, 20, 8], [594, 19, 72, 20, 1],
     # Territory Invaders     # Duel                   # UNO
     [107, 172, 132, 201, 7], [269, 172, 132, 201, 7], [432, 172, 132, 201, 7],
     # About Devs        # Ad                # Store
     [370, 402, 156, 39, 9], [544, 402, 121, 39, 10], [237, 402, 120, 39, 7]],

    # Screen 8 button(s) #
    # Back Button         # PolyCash Info       # Log Out
    [[42, 89, 39, 39, 4], [9, 18, 137, 20, 8], [594, 19, 72, 20, 1]],

    # Screen 9 button(s) #
    # Back Button         # PolyCash Info       # Log Out
    [[42, 89, 39, 39, 4], [9, 18, 137, 20, 8], [594, 19, 72, 20, 1]],

    # Screen 10 button(s) #
    # Back Button         # PolyCash Info       # Log Out
    [[42, 89, 39, 39, 4], [9, 18, 137, 20, 8], [594, 19, 72, 20, 1], [260, 142, 155, 70, 10]],

    # Screen 11 button(s) #
    [[42, 89, 39, 39, 4]],
]

# Points
points = 0
font = pygame.font.Font("freesansbold.ttf", 12)
textX = 96
textY = 24

# Display Points
def display_points(x, y):
    current_points = font.render(str(points), True, (255, 255, 255))
    screen.blit(current_points, (x, y))

# TextBox Class
class TextBox:
    def __init__(self, x, y, w, h, font, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('dodgerblue2')
        self.text = text
        self.font = font
        self.txt_surface = font.render(self.text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = pygame.Color('black') if self.active else pygame.Color('dodgerblue2')
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        width = max(150, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

# Display Screen
class Screen:
    def __init__(self, video_path, image_path):
        self.video_path = video_path
        self.image_path = image_path
        self.image = pygame.image.load(self.image_path)
        self.buttons = []
        self.text_boxes = []

    def play_video(self):
        clip = VideoFileClip(self.video_path)
        clip.preview()
        clip.close()

    def display_image(self):
        screen.blit(self.image, (0, 0))

    def add_button(self, x, y, w, h, action=None):
        button = Button(x, y, w, h, action)
        self.buttons.append(button)

    def add_text_box(self, x, y, w, h):
        text_box = TextBox(x, y, w, h, font)
        self.text_boxes.append(text_box)

    def draw_text_boxes(self):
        for text_box in self.text_boxes:
            text_box.draw(screen)

# Create Button
class Button:
    def __init__(self, x, y, w, h, action=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.action = action

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Initialize Screen objects
screen_objects = []
for video, image in screens:
    screen_object = Screen(video, image)
    screen_objects.append(screen_object)

# Add buttons to screen_objects using the buttons list
for idx in range(len(buttons)):
    btn_list = buttons[idx]
    for btn in btn_list:
        x = btn[0]
        y = btn[1]
        w = btn[2]
        h = btn[3]
        action = btn[4]
        screen_objects[idx].add_button(x, y, w, h, action=action)

# Add text boxes to screens 2 and 3
screen_objects[2].add_text_box(180, 210, 342, 26)
screen_objects[2].add_text_box(180, 300, 342, 26)
screen_objects[3].add_text_box(180, 210, 342, 26)
screen_objects[3].add_text_box(180, 300, 342, 26)

current_screen_index = 0
show_image = False
points_incremented = False
user_index = None

# Function to launch Territory Invaders game
def launch_territory_invaders(mode, user_index):
    subprocess.Popen(['python', 'Territory Invaders 4.py', mode, str(user_index)])

# Function to launch Duel game
def launch_duel_game(mode, user_index):
    subprocess.Popen(['python', 'DUEL GUI V1.py', str(mode), str(user_index)])

def launch_uno_game(user_index):
    subprocess.Popen(['python', 'uno_code_v3_graphics.py', str(user_index)])

def launch_store(user_index):
    subprocess.Popen(['python', 'STORE_GUI_V2.py', str(user_index)])

# Function to read user data from the database file
def read_user_data(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
    return lines

# Function to write new user data to the database file
def write_user_data(file_path, username, password):
    with open(file_path, 'a') as file:
        file.write(f"{username}\n{password}\n")
        file.write("50\n0.5\n1.5\n1\n1\n1\n1\n")

# Function to validate username and password
def validate_user(username, password, user_data):
    if username in user_data:
        index = user_data.index(username)
        if index + 1 < len(user_data) and user_data[index + 1] == password:
            return index
    return None

# Function to get user points from the database file
def get_user_points(index, user_data):
    if index + 2 < len(user_data):
        return int(user_data[index + 2])
    return 0

# Function to update user points in the database file
def update_user_points(index, new_points, file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    lines[index + 2] = f"{new_points}\n"
    with open(file_path, 'w') as file:
        file.writelines(lines)

# Game loop for GUI
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and show_image:
            for button in screen_objects[current_screen_index].buttons:
                if button.is_clicked(event.pos):
                    # Check if it's the button to confirm text input on Sign-In screen (Screen 2)
                    if current_screen_index == 2 and button.rect.topleft == (293, 370):
                        username = screen_objects[current_screen_index].text_boxes[0].text
                        password = screen_objects[current_screen_index].text_boxes[1].text
                        user_data = read_user_data("database.txt")
                        user_index = validate_user(username, password, user_data)
                        if user_index is not None:
                            points = get_user_points(user_index, user_data)
                            with open("user_index.txt", "w") as f:
                                f.write(str(user_index))
                            current_screen_index = 5
                            show_image = False
                            points_incremented = False
                        else:
                            current_screen_index = 3
                            show_image = False
                            screen_objects[3].play_video()
                            show_image = True
                            screen_objects[3].display_image()
                            screen_objects[3].draw_text_boxes()
                            continue

                    elif current_screen_index == 3 and button.rect.topleft == (293, 370):
                        username = screen_objects[current_screen_index].text_boxes[0].text
                        password = screen_objects[current_screen_index].text_boxes[1].text
                        write_user_data("database.txt", username, password)
                        current_screen_index = 4

                    if current_screen_index == 5 and button.rect.topleft == (107, 172):
                        launch_territory_invaders("single_player", user_index)
                    elif current_screen_index == 6 and button.rect.topleft == (107, 172):
                        launch_territory_invaders("two_player", user_index)
                    elif current_screen_index == 7 and button.rect.topleft == (107, 172):
                        launch_territory_invaders("player_vs_ai", user_index)

                    if current_screen_index == 6 and button.rect.topleft == (269, 172):
                        launch_duel_game("1", user_index)
                    elif current_screen_index == 7 and button.rect.topleft == (269, 172):
                        launch_duel_game("2", user_index)

                    if current_screen_index == 5 and button.rect.topleft == (432, 172):
                        launch_uno_game(user_index)

                    if current_screen_index == 7 and button.rect.topleft == (432, 172):
                        launch_uno_game(user_index)

                    if current_screen_index in [5, 6, 7] and button.rect.topleft == (237, 402):
                        launch_store(user_index)

                    current_screen_index = button.action
                    show_image = False
                    points_incremented = False
        for text_box in screen_objects[current_screen_index].text_boxes:
            text_box.handle_event(event)

    screen.fill((0, 0, 0))

    if show_image:
        screen_objects[current_screen_index].display_image()
        screen_objects[current_screen_index].draw_text_boxes()

        if current_screen_index == 10:
            if not points_incremented:
                points += 50
                update_user_points(user_index, points, "database.txt")
                points_incremented = True

        if current_screen_index in [0, 3, 4, 5, 6, 7, 8, 9, 10]:
            display_points(textX, textY)
    else:
        screen_objects[current_screen_index].play_video()
        show_image = True

    pygame.display.flip()

pygame.quit()
