import random
import sys
import os
import time
import imagebutton
import uno_framework
import pygame

# See uno_framework.py for the game classes used in this game

pygame.init()
pygame.font.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

FPS = 20  # frames per second setting
fpsClock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("POLY GAME - UNO")
screen.fill((255, 255, 255))

# background image is needed for all screens
background = pygame.image.load("UNO_IMG_ASSETS/other_assets/uno_bg.png").convert()
# background needs to be semitransparent
background.set_alpha(180)
background = pygame.transform.scale(background, (900, 600))

title_font = pygame.font.SysFont("Raleway", 32, bold=True, italic=False)
info_font = pygame.font.SysFont("Raleway", 18, bold=True, italic=False)

info_txt = open("info_file.txt")
info_text = info_txt.readlines()

alerts_txt = open("alerts_file.txt")
alerts_text = alerts_txt.readlines()

# defining colors
colors = ((255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0))
red, green, blue, yellow = colors


# updates all the background details in the beginning
def start_bg_update():
    # the other background images - empty card slots, the banners, etc.
    # Arrows come later if/when needed

    # two sizes of card slot
    card_slot = pygame.image.load("UNO_IMG_ASSETS/other_assets/empty_card_frame.jpg").convert()
    large_card_slot = pygame.transform.scale(card_slot, (100, 160))
    small_card_slot = pygame.transform.scale(card_slot, (70, 120))

    # effect banner
    # convert_alpha() removes the black border on a transparent image
    effect_banner = pygame.image.load("UNO_IMG_ASSETS/other_assets/effect_banner.png").convert_alpha()
    effect_banner = pygame.transform.scale(effect_banner, (570, 80))

    # effect banner
    # convert_alpha() removes the black border on a transparent image
    stat_banner = pygame.image.load("UNO_IMG_ASSETS/other_assets/stat_banner.png").convert_alpha()
    stat_banner = pygame.transform.scale(stat_banner, (240, 440))

    screen.fill((255, 255, 255))

    screen.blit(background, (0, 0))

    screen.blit(effect_banner, (250, 360))
    screen.blit(stat_banner, (10, 10))

    screen.blit(large_card_slot, (380, 180))
    screen.blit(large_card_slot, (580, 180))

    # blits your card slot and the AI card slots onto the screen
    for i in range(260, 820, 80):
        screen.blit(small_card_slot, (i, 460))
        screen.blit(small_card_slot, (i, 20))

    pygame.display.update()

    # However, these cards need to be buttons (your cards only, the discard, draw and ai cards can be


# code: DEF is default, COL is color, EFF is EFFECT, CHA is change color, INV is invalid
def status_update(color, turn, current_card, your_hand, ai_hand, draw_pile, discard_pile, code="DEF"):
    # effect banner
    # convert_alpha() removes the black border on a transparent image
    effect_banner = pygame.image.load("UNO_IMG_ASSETS/other_assets/effect_banner.png").convert_alpha()
    effect_banner = pygame.transform.scale(effect_banner, (570, 80))

    # effect banner
    # convert_alpha() removes the black border on a transparent image
    stat_banner = pygame.image.load("UNO_IMG_ASSETS/other_assets/stat_banner.png").convert_alpha()
    stat_banner = pygame.transform.scale(stat_banner, (240, 440))

    # refreshes the two banners
    screen.blit(effect_banner, (250, 360))
    screen.blit(stat_banner, (10, 10))

    # title_font = pygame.font.SysFont("Raleway", 58, bold=False, italic=False)
    effect_bar_font = pygame.font.SysFont("Calibri", 20, bold=False, italic=False)
    stat_bar_font = pygame.font.SysFont("Arial", 30, bold=False, italic=False)

    # this handles the length cant be None exception thrown when draw_pile is empty
    draw_size = 0
    if draw_pile == None or len(draw_pile) == 0:
        draw_size = 0
    else:
        draw_size = len(draw_pile)

    # Load these lines from a file.
    stat_title = stat_bar_font.render(f'{alerts_text[12].rstrip()}', False, (255, 255, 255))
    stat_your_hand = stat_bar_font.render(f'{alerts_text[13].rstrip()} {len(your_hand)}', False, (255, 255, 255))
    stat_ai_hand = stat_bar_font.render(f'{alerts_text[14].rstrip()} {len(ai_hand)}', False, (255, 255, 255))
    stat_draw_pile = stat_bar_font.render(f'{alerts_text[15].rstrip()} {draw_size}', False, (255, 255, 255))
    stat_discard_pile = stat_bar_font.render(f'{alerts_text[16].rstrip()} {len(discard_pile)}', False, (255, 255, 255))
    stat_total = stat_bar_font.render(f'{alerts_text[17].rstrip()}', False, (255, 255, 255))

    screen.blit(stat_title, (30, 60))
    screen.blit(stat_your_hand, (30, 90))
    screen.blit(stat_ai_hand, (30, 120))
    screen.blit(stat_draw_pile, (30, 150))
    screen.blit(stat_discard_pile, (30, 180))
    screen.blit(stat_total, (30, 210))

    effect_bar_text = None
    txtcolor = (255, 255, 255)
    text = ""

    if code == "DEF":

        if turn == "you":
            text = f'{alerts_text[20].rstrip()}'
        elif turn == "ai":
            text = f'{alerts_text[21].rstrip()}'

    # invalid card chosen
    elif code == "INV":

        text = f'{alerts_text[22].rstrip()}'

    # no valid cards available
    elif code == "NOMAT":

        text = f'{alerts_text[23].rstrip()}'

    # effect has expired
    elif code == "EXP":

        text = f'{alerts_text[24].rstrip()}'

    # new color is in effect
    elif code == "COL":

        colors_text = ["red", "yellow", "green", "blue"]
        index = colors_text.index(color) + 1
        color_hex = ((255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0))
        text = f'{alerts_text[index].rstrip()}'
        color = color_hex[index - 1]

    # an effect is in effect
    elif code == "EFF":

        effect = current_card[0]

        effect_text = ["draw 4", "color change", "draw 2", "skip", "reverse"]
        index = effect_text.index(effect) + 6
        text = f'{alerts_text[index].rstrip()}'

        # recursion here, color must be called after the effect IF its a color changer
        time.sleep(2)
        if (effect == "draw 4" or effect == "color change"):
            status_update("COL", color, turn, current_card, your_hand, ai_hand, draw_pile, discard_pile)

    # you must choose a color
    elif code == "CHA":

        text = f'{alerts_text[25].rstrip()}'
        effect_bar_text = stat_bar_font.render(text, False, txtcolor)
        screen.blit(effect_bar_text, (285, 385))
        pygame.display.update()
        time.sleep(2)
        new_color = color_change()
        start_bg_update()
        return new_color

    effect_bar_text = stat_bar_font.render(text, False, txtcolor)
    screen.blit(effect_bar_text, (285, 385))

    pygame.display.update()


def color_change():
    red_btn = pygame.image.load("UNO_IMG_ASSETS/other_assets/red_btn.png").convert_alpha()
    red_btn = pygame.transform.scale(red_btn, (80, 80))
    red_btn = imagebutton.Button(120, 480, red_btn, 1)

    yellow_btn = pygame.image.load("UNO_IMG_ASSETS/other_assets/yellow_btn.png").convert_alpha()
    yellow_btn = pygame.transform.scale(yellow_btn, (80, 80))
    yellow_btn = imagebutton.Button(120, 390, yellow_btn, 1)

    green_btn = pygame.image.load("UNO_IMG_ASSETS/other_assets/green_btn.png").convert_alpha()
    green_btn = pygame.transform.scale(green_btn, (80, 80))
    green_btn = imagebutton.Button(20, 480, green_btn, 1)

    blue_btn = pygame.image.load("UNO_IMG_ASSETS/other_assets/blue_btn.png").convert_alpha()
    blue_btn = pygame.transform.scale(blue_btn, (80, 80))
    blue_btn = imagebutton.Button(20, 390, blue_btn, 1)

    new_color = ""

    color_chosen = False

    while not color_chosen:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        if red_btn.draw(screen):
            new_color = "red"
            color_chosen = True

        elif yellow_btn.draw(screen):
            new_color = "yellow"
            color_chosen = True

        elif green_btn.draw(screen):
            new_color = "green"
            color_chosen = True


        elif blue_btn.draw(screen):
            new_color = "blue"
            color_chosen = True

        pygame.display.update()

    time.sleep(1)
    return new_color

    # call this in the main function, with new_color as the color parameter
    # status_update(color, turn, current_card, your_hand, ai_hand, draw_pile, discard_pile, "COL"):


# avoid refreshing the ENTIRE SCREEN

# However, do make sure to blit the empty card slots
# when either your hand or ai hand is less than 7
def refresh_banners(your_seven, ai_hand):
    card_slot = pygame.image.load("UNO_IMG_ASSETS/other_assets/empty_card_frame.jpg").convert()
    large_card_slot = pygame.transform.scale(card_slot, (100, 160))
    small_card_slot = pygame.transform.scale(card_slot, (70, 120))

    print(f"Your hand: {your_seven}")

    if (len(your_seven) < 7):
        # blit the small card slots in reverse order up to the current card
        # start from the end and step backwards

        n = len(your_seven)

        for i in range(6, n - 1, -1):
            x_coord = 260 + 80 * i

            screen.blit(small_card_slot, (x_coord, 460))

    if (len(ai_hand) < 7):
        # blit the small card slots in reverse order up to the current card
        # start from the end and step backwards

        n = len(ai_hand)

        # print(f"AI CARD SLOTS: {n}")

        for i in range(6, n - 1, -1):
            x_coord = 260 + 80 * i

            screen.blit(small_card_slot, (x_coord, 20))


# This renders the cards onto the screen.
# Also needs start pile and discard pile so it can do stats

def current_state_render(current_card, your_seven, ai_hand, draw_pile, discard_pile, position=0):
    print('Your seven: ')
    print(your_seven)

    # background and empty slots first
    # your_seven = []
    if ((len(your_seven)) > 7):
        your_seven = your_seven[0:7]
    else:
        your_seven = your_seven

    # your seven will be same as your hand if your hand < 7
    refresh_banners(your_seven, ai_hand)

    card_slot = pygame.image.load("UNO_IMG_ASSETS/other_assets/empty_card_frame.jpg").convert()
    large_card_slot = pygame.transform.scale(card_slot, (100, 160))
    small_card_slot = pygame.transform.scale(card_slot, (70, 120))

    # then the cards
    card_back = pygame.image.load("UNO_IMG_ASSETS/other_assets/card_back.png").convert_alpha()
    card_back_large = pygame.transform.scale(card_back, (100, 160))
    card_back_small = pygame.transform.scale(card_back, (70, 120))

    # blits current card
    curr_card_path = card_img_from_text(current_card)
    curr_card = pygame.image.load(f"{curr_card_path}").convert_alpha()
    curr_card = pygame.transform.scale(curr_card, (100, 160))
    screen.blit(curr_card, (380, 180))

    # blit the discard pile card back-icon if card_flag is NOT false.
    # the card_flag is false if no cards in draw pile

    if (draw_pile == None):
        screen.blit(large_card_slot, (580, 180))
    else:
        screen.blit(card_back_large, (580, 180))

    n = len(ai_hand)
    # caps out the length at 7. AI card visibility does NOT matter as you dont see them anyway
    if n > 7:
        n = 7

    for i in range(n):
        x_coord = 260 + 80 * i

        screen.blit(card_back_small, (x_coord, 20))

    # card_btns = {}
    card_btns = []
    card_texts = []
    button_iter = None

    # Only blit the first seven cards in your hand (if less than 7, blit available cards only)
    # the arrow button alters this parameter value
    for i in range(len(your_seven)):
        print(f"Length of your seven: {len(your_seven)}")
        card_text = your_seven[i]

        # extracts an image filepath path from the cards iteratively
        your_card_path = card_img_from_text(card_text)
        your_card = pygame.image.load(f'{your_card_path}').convert_alpha()
        your_card = pygame.transform.scale(your_card, (70, 120))
        print(your_card_path)
        x_coord = 260 + 80 * i

        color = str(card_text[0])
        suit = str(card_text[1])

        card_texts.append(color + "_" + suit)
        # dictionary of card button objects
        button_iter = imagebutton.Button(x_coord, 460, your_card, 1)
        button_iter.draw(screen)
        card_btns.append(button_iter)

    # then the effect banners, stats

    pygame.display.update()
    return (card_btns, card_texts)


# also pass the arrow btn objects
def your_turn(card_btns, card_texts, your_hand, position=0):
    # by default the code is TOGG. It only changes to CARD, when a card has been clicked
    code = "TOGG"

    # using list comprehension to break up the hand into groups of seven
    n = 7
    hand_groups = [your_hand[i * n:(i + 1) * n] for i in range((len(your_hand) + n - 1) // n)]
    for hand in hand_groups:
        print(hand)

    print(f"Sets of 7 cards: {len(hand_groups)}")
    print(f"Position: {position}")

    hand_to_use = []
    # the default position is zero.
    master_index = 0

    left_btn = pygame.image.load("UNO_IMG_ASSETS/other_assets/left_btn.png").convert_alpha()
    left_btn = pygame.transform.scale(left_btn, (80, 80))
    left_btn = imagebutton.Button(180, 480, left_btn, 1)

    right_btn = pygame.image.load("UNO_IMG_ASSETS/other_assets/right_btn.png").convert_alpha()
    right_btn = pygame.transform.scale(right_btn, (80, 80))
    right_btn = imagebutton.Button(800, 480, right_btn, 1)

    # color_chosen = False

    # while not color_chosen:

    # when click arrow btns
    # return the side of hand u want

    your_turn = True

    while your_turn:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        # this is only necessary to blit arrows if you have more than one group of seven
        if (len(hand_groups) > 1):

            if left_btn.draw(screen):

                position -= 1

                if position < 0:
                    position = 0
                print("LEFT")
                print(f"Sets of 7 cards: {len(hand_groups)}")
                print(f"Position: {position}")
                hand_to_use = hand_groups[position]

                return (code, hand_to_use, position)

            if right_btn.draw(screen):

                position += 1

                if position < len(hand_groups) - 1:
                    position = len(hand_groups) - 1
                print("RIGHT")
                print(f"Sets of 7 cards: {len(hand_groups)}")
                print(f"Position: {position}")
                hand_to_use = hand_groups[position]

                return (code, hand_to_use, position)

        for index in range(len(card_btns)):

            card_gui = card_btns[index]

            if card_gui.draw(screen):
                # code that converts the card btn object key back to a list
                path = card_texts[index].split("_")

                # index is needed for valid card checking
                code = "CARD"
                print("MATCHING INDEX VALUE: ")
                print(index)

                master_index = 7 * position + index
                print(f"Position: {position}")
                print(f"SUBINDEX: {index}")
                print(f"MASTER INDEX: {master_index}")
                path.append(True)
                your_turn = False
                return (code, path, master_index)


def info_menu():
    print("INFO")

    home_btn = pygame.image.load("UNO_IMG_ASSETS/other_assets/home_btn.png").convert_alpha()
    home_btn = pygame.transform.scale(home_btn, (80, 80))
    home_btn = imagebutton.Button(20, 460, home_btn, 1.5)

    info_running = True
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))

    title_font = pygame.font.SysFont("Raleway", 58, bold=False, italic=False)
    info_font = pygame.font.SysFont("Raleway", 30, bold=False, italic=False)

    # Load these lines from a file.
    info_title = title_font.render(f'{info_text[0].rstrip()}', False, (10, 30, 50))
    screen.blit(info_title, (300, 50))

    # read lines 2-8 (index 1-7)
    for i in range(7):
        rule_msg = info_font.render(f'{info_text[i + 1].rstrip()}', False, (10, 30, 50))
        screen.blit(rule_msg, (50, 150 + 50 * i))

    info_text_7 = info_font.render(f'{info_text[8].rstrip()}', False, (10, 30, 50))
    screen.blit(info_text_7, (300, 520))

    pygame.display.update()

    while info_running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        if home_btn.draw(screen):
            # call the start if home is pressed
            print("START")
            startup()
            info_running = False

        pygame.display.update()


def startup():
    title_txt = pygame.image.load("UNO_IMG_ASSETS/other_assets/title_text.png").convert_alpha()
    title_txt = pygame.transform.scale(title_txt, (300, 300))

    start_btn = pygame.image.load("UNO_IMG_ASSETS/other_assets/start_btn.png").convert_alpha()
    start_btn = pygame.transform.scale(start_btn, (120, 80))
    start_btn = imagebutton.Button(350, 300, start_btn, 2)

    info_btn = pygame.image.load("UNO_IMG_ASSETS/other_assets/info_btn.png").convert_alpha()
    info_btn = pygame.transform.scale(info_btn, (80, 80))
    info_btn = imagebutton.Button(750, 460, info_btn, 1.5)

    running = True
    # The main start screen to start the game

    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    screen.blit(title_txt, (300, 40))

    pygame.display.update()
    print("ENTERED HOME")
    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        if info_btn.draw(screen):
            # call the info function
            info_menu()
            running = False

        if start_btn.draw(screen):
            # call the start
            print("START")
            start_bg_update()
            time.sleep(1)
            running = False

        pygame.display.update()


# this function returns the appropriate card filepath when provided a card
def card_img_from_text(card):
    # keeps adding to the file path once
    cardfilepath = "UNO_IMG_ASSETS"

    # first use the color parameter, which is card[2] to select a subfolder
    # the subfolders are the same name as the color

    # for the image path
    if (((card[0] == "change color") or (card[0] == "draw 4")) and card[1] != "black"):
        card[1] = "black"

    cardfilepath = cardfilepath + f"/{card[1]}"
    # then use the appropriate effect/number
    cardfilepath = cardfilepath + f"/{card[0]}"

    cardfilepath = cardfilepath + f".png"
    # print(cardfilepath)
    return cardfilepath


startup()

# Pass your user stuff to the UnoGame, so it can modify user data file accordingly
game_Instance = uno_framework.UnoGame()
deck = game_Instance.create_deck()
(user_hand, ai_hand) = game_Instance.shuffle()

# sets the start hands within the player and AI, inits them
player_Instance = uno_framework.Player("John", user_hand)
ai_Instance = uno_framework.AIPlayer(ai_hand)

# If start clicked in menu, start the game, and set up
game_Instance.start_clicked()
game_on = game_Instance.get_game_status
game_Instance.setup()

# TODO: MERGE GAMELOOP INTO MAIN PROGRAM
# The only different thing is choosing the cards. That is done from event sensing in your turn.
# you are kept in a while loop (once validity check for your turn ends)
# until one of the cards are clicked

while game_on:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    # function to just return the hands of each the
    your_hand = player_Instance.get_hand()
    ai_hand = ai_Instance.get_hand()
    # Gameover case or draw pile runs out cases
    game_Instance.turn_checks(your_hand, ai_hand)
    current_card = game_Instance.get_current_card()
    print(current_card)

    discard_pile = game_Instance.get_discard_pile()
    draw_pile = game_Instance.get_draw_pile()

    '''
    #Generally, unless its your turn and you toggle, only first seven of your cards are displayed
    your_seven = []
    if ((len(your_hand))>7):
        your_seven = your_hand[0:7]
    else:
        your_seven = your_hand
    '''

    '''
    #put current card to top of discard pile

    #no need to discard twice, drawing a card already discards it
    #game_Instance.discard_card(current_card)
    '''

    # New_color is a flag for wild card abilities - changing color
    new_color = game_Instance.get_new_color()

    turn = game_Instance.get_turn()
    color = new_color
    status_update(color, turn, current_card, your_hand, ai_hand, draw_pile, discard_pile)
    current_state_render(current_card, your_hand, ai_hand, draw_pile, discard_pile)

    if turn == "you":

        if current_card[0] == "draw 2" and current_card[2] == True:
            status_update(color, turn, current_card, your_hand, ai_hand, draw_pile, discard_pile, "EFF")
            time.sleep(2)
            print("Drawing 2 cards!")

            for i in range(2):
                your_hand.append(game_Instance.draw_card())
            player_Instance.set_hand(your_hand)

            current_card[2] = False


        elif current_card[0] == "draw 4" and current_card[2] == True:
            status_update(color, turn, current_card, your_hand, ai_hand, draw_pile, discard_pile, "EFF")
            time.sleep(2)
            print("Drawing 4 cards!")
            for i in range(4):
                your_hand.append(game_Instance.draw_card())
            player_Instance.set_hand(your_hand)
            current_card[2] = False
        '''
        #will need to recheck after hand size increases
        if ((len(your_hand))>7):
            your_seven = your_hand[0:7]
        else:
            your_seven = your_hand
        '''
        if (current_card[0] == "draw 4" or current_card[0] == "change color"):
            status_update(color, turn, current_card, your_hand, ai_hand, draw_pile, discard_pile, "COL")

            current_card[2] = False

        current_state_render(current_card, your_hand, ai_hand, draw_pile, discard_pile)

        if (current_card[0] == "reverse" or current_card[0] == "skip" or current_card[0] == "draw 4") \
                and (current_card[2] == True):

            status_update(color, turn, current_card, your_hand, ai_hand, draw_pile, discard_pile, "EFF")
            time.sleep(2)
            current_card[2] = False

            print("Turn skip! AI turn!")
            # runs the AI turn instead
            # have an effect update for your turn
            status_update(color, turn, current_card, your_hand, ai_hand, draw_pile, discard_pile, "EFF")
            turn = "ai"
            status_update(color, turn, current_card, your_hand, ai_hand, draw_pile, discard_pile)

            print(f"\nCurrent card: {current_card}")

            # the tuple is the return of the turn function
            (ai_hand, current_card) = ai_Instance.ai_turn_setup(current_card, new_color)
            valid_cards = game_Instance.validity_check(ai_hand, current_card)

            if valid_cards is not None:
                # the tuple is unpacked if any valid cards present

                (current_card, new_color) = ai_Instance.ai_choose_card(valid_cards, current_card, new_color)

                game_Instance.set_new_color(new_color)
                game_Instance.discard_card(current_card)
                game_Instance.set_current_card(current_card)
                print(f"{current_card} has been discarded")

            else:
                print("AI is drawing a card")
                ai_hand.append(game_Instance.draw_card())

            current_state_render(current_card, your_hand, ai_hand, draw_pile, discard_pile)
            game_Instance.set_turn("you")



        else:

            if (current_card[0] == "reverse" or current_card[0] == "skip" or current_card[0] == "draw 4") \
                    and (current_card[2] == False):
                print(
                    f"The turn skipping effect of the {current_card[0]} card has expired. It is in effect for only one turn.")
                game_Instance.set_turn("you")
                status_update(color, turn, current_card, your_hand, ai_hand, draw_pile, discard_pile, "EXP")

            (your_hand, current_card) = player_Instance.turn_setup(current_card, new_color)
            valid_cards = game_Instance.validity_check(your_hand, current_card)

            # the tuple is unpacked if any valid cards present
            if valid_cards is not None:

                print(f"Valid cards: {valid_cards}")

                valid_card_clicked = False

                while not valid_card_clicked:

                    for index in valid_cards:
                        print(f"Card number {index + 1} is valid")

                    # start with the first seven
                    # FLAG 33 FLAG 33
                    (card_btns, card_texts) = current_state_render(current_card, your_hand, ai_hand, draw_pile,
                                                                   discard_pile)
                    # here the toggle loop starts

                    card_clicked = False
                    index = 0
                    position = 0
                    while not card_clicked:

                        return_values = your_turn(card_btns, card_texts, your_hand, position)

                        if return_values[0] == "CARD":
                            chosen_card = return_values[1]
                            index = return_values[2]
                            print("CARD CHOSEN")
                            print(f"INDEX OF CARD: {index}")
                            card_clicked = True

                        elif return_values[0] == "TOGG":
                            hand_shown = return_values[1]
                            position = return_values[2]
                            print(hand_shown)
                            # position
                            (card_btns, card_texts) = current_state_render(current_card, hand_shown, ai_hand, draw_pile,
                                                                           discard_pile)

                    print(chosen_card)
                    print(f"VALID CARDS: {valid_cards}")
                    print(index)
                    print(f"INDEX: {index}")

                    if index in valid_cards:
                        print("YES")
                        valid_card_clicked = True


                    else:

                        # banner update() with the flag -INV
                        status_update(color, turn, current_card, your_hand, ai_hand, draw_pile, discard_pile, "INV")

                        print("Card invalid, try again")

                # FLAG 32! FLAG 32
                card_to_discard = your_hand.pop(index)
                player_Instance.set_hand(your_hand)
                current_card = card_to_discard

                if card_to_discard[1] == "black":
                    new_color = status_update(color, turn, current_card, your_hand, ai_hand, draw_pile, discard_pile,
                                              "CHA")
                    # code = "CHA"
                    # return code
                    # new color = ..(chosen color)

                # (current_card, new_color) = player_Instance.your_turn(index, current_card, new_color)

                # The card's ability will be re enabled
                current_card[2] = True
                game_Instance.set_new_color(new_color)
                game_Instance.discard_card(current_card)
                game_Instance.set_current_card(current_card)
                print(f"{current_card} has been discarded")

            # if no valid cards, drawing a card constitutes your turn
            else:

                status_update(color, turn, current_card, your_hand, ai_hand, draw_pile, discard_pile, "NOMAT")
                time.sleep(2)
                print("You had no valid cards")
                print("Drawing a card for you")
                your_hand.append(game_Instance.draw_card())

            current_state_render(current_card, your_hand, ai_hand, draw_pile, discard_pile)
            game_Instance.set_turn("ai")


    elif turn == "ai":

        if current_card[0] == "draw 2" and current_card[2] == True:
            print("AI drawing 2 cards!")
            for i in range(2):
                ai_hand.append(game_Instance.draw_card())
            current_card[2] = False
        elif current_card[0] == "draw 4" and current_card[2] == True:
            print("AI drawing 4 cards!")
            for i in range(4):
                ai_hand.append(game_Instance.draw_card())
            current_card[2] = False
        '''
        #will need to recheck after hand size increases
        if ((len(your_hand))>7):
            your_seven = your_hand[0:7]
        else:
            your_seven = your_hand
        '''
        if (current_card[0] == "draw 4" or current_card[0] == "change color"):
            status_update(color, turn, current_card, your_hand, ai_hand, draw_pile, discard_pile, "COL")

        current_state_render(current_card, your_hand, ai_hand, draw_pile, discard_pile)

        if (current_card[0] == "reverse" or current_card[0] == "skip" or current_card[0] == "draw 4") \
                and (current_card[2] == True):

            current_card[2] = False

            print("Turn skip! Your turn!")
            # runs the your turn instead
            turn = "you"
            status_update(color, turn, current_card, your_hand, ai_hand, draw_pile, discard_pile)
            print(f"\nCurrent card: {current_card}")

            # the tuple is the return of the turn function
            (your_hand, current_card) = player_Instance.turn_setup(current_card, new_color)
            valid_cards = game_Instance.validity_check(your_hand, current_card)

            # the tuple is unpacked if any valid cards present
            if valid_cards is not None:

                print(f"Valid cards: {valid_cards}")

                valid_card_clicked = False

                while not valid_card_clicked:

                    for index in valid_cards:
                        print(f"Card number {index + 1} is valid")

                    # start with the first seven
                    # FLAG 33 FLAG 33
                    (card_btns, card_texts) = current_state_render(current_card, your_hand, ai_hand, draw_pile,
                                                                   discard_pile)
                    # here the toggle loop starts

                    card_clicked = False
                    index = 0
                    position = 0
                    while not card_clicked:

                        return_values = your_turn(card_btns, card_texts, your_hand, position)

                        if return_values[0] == "CARD":
                            chosen_card = return_values[1]
                            index = return_values[2]
                            print("CARD CHOSEN")
                            print(f"INDEX OF CARD: {index}")
                            card_clicked = True

                        elif return_values[0] == "TOGG":
                            hand_shown = return_values[1]
                            position = return_values[2]
                            print('HAND SHOWN: ')
                            print(hand_shown)
                            (card_btns, card_texts) = current_state_render(current_card, hand_shown, ai_hand, draw_pile,
                                                                           discard_pile)

                    print(chosen_card)
                    print(f"VALID CARDS: {valid_cards}")
                    print(index)
                    print(f"INDEX: {index}")
                    print("2")

                    if index in valid_cards:
                        print("YES")
                        valid_card_clicked = True


                    else:

                        # banner update() with the flag -INV
                        status_update(color, turn, current_card, your_hand, ai_hand, draw_pile, discard_pile, "INV")

                        print("Card invalid, try again")

                card_to_discard = your_hand.pop(index)
                player_Instance.set_hand(your_hand)
                current_card = card_to_discard

                if card_to_discard[1] == "black":
                    new_color = status_update(color, turn, current_card, your_hand, ai_hand, draw_pile, discard_pile,
                                              "CHA")
                    # code = "CHA"
                    # return code
                    # new color = ..(chosen color)

                # (current_card, new_color) = player_Instance.your_turn(index, current_card, new_color)

                # The card's ability will be re enabled
                current_card[2] = True
                game_Instance.set_new_color(new_color)
                game_Instance.discard_card(current_card)
                game_Instance.set_current_card(current_card)
                print(f"{current_card} has been discarded")

            # if no valid cards, drawing a card constitutes your turn
            else:

                status_update(color, turn, current_card, your_hand, ai_hand, draw_pile, discard_pile, "NOMAT")
                time.sleep(2)
                print("You had no valid cards")
                print("Drawing a card for you")
                your_hand.append(game_Instance.draw_card())

            current_state_render(current_card, your_hand, ai_hand, draw_pile, discard_pile)
            game_Instance.set_turn("ai")


        else:

            if (current_card[0] == "reverse" or current_card[0] == "skip" or current_card[0] == "draw 4") \
                    and (current_card[2] == False):
                print(
                    f"The turn skipping effect of the {current_card[0]} card has expired. It is in effect for only one turn.")

                status_update(color, turn, current_card, your_hand, ai_hand, draw_pile, discard_pile, "EXP")

            (ai_hand, current_card) = ai_Instance.ai_turn_setup(current_card, new_color)
            valid_cards = game_Instance.validity_check(ai_hand, current_card)

            if valid_cards is not None:
                # the tuple is unpacked if any valid cards present
                (current_card, new_color) = ai_Instance.ai_choose_card(valid_cards, current_card, new_color)

                # The card's ability will be re enabled
                current_card[2] = True

                game_Instance.set_new_color(new_color)
                game_Instance.discard_card(current_card)
                game_Instance.set_current_card(current_card)
                print(f"{current_card} has been discarded")


            else:
                print("AI is drawing a card")
                ai_hand.append(game_Instance.draw_card())

            current_state_render(current_card, your_hand, ai_hand, draw_pile, discard_pile)
            game_Instance.set_turn("you")
        game_on = game_Instance.get_game_status

    pygame.display.update()
