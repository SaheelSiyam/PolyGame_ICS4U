import random
import sys
import os
import time
import imagebutton
import uno_framework
import pygame

#See uno_framework.py for the game classes used in this game

pygame.init()
pygame.font.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

FPS = 30  # frames per second setting
fpsClock = pygame.time.Clock()


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("POLY GAME - UNO")
screen.fill((255, 255, 255))

#background image is needed for all screens
background = pygame.image.load("UNO_IMG_ASSETS/other_assets/uno_bg.png").convert()
#background needs to be semitransparent
background.set_alpha(180)
background = pygame.transform.scale(background,(900,600))
    

title_font = pygame.font.SysFont("Raleway", 32, bold=True, italic=False)
info_font = pygame.font.SysFont("Raleway", 18, bold=True, italic=False)

info_txt = open("info_file.txt")
info_text = info_txt.readlines()

alerts_txt = open("alerts_file.txt")
alerts_text = alerts_txt.readlines()

#defining colors
colors = ((255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0))
red, green, blue, yellow = colors

# def mainish() is a TEST function that creates a cardfilepath from a current card.
#Basically its a dissected version of the main algorithm

'''
def mainish():
   
    info_font = pygame.font.SysFont("Raleway", 30, bold=False, italic=False)

    
    #Load these lines from a file.
    info_title = title_font.render("Effect: Color Change: New Color: Blue", False, (blue))
    screen.blit(info_title, (300, 388))

    card_back = pygame.image.load("UNO_IMG_ASSETS/other_assets/card_back.png").convert_alpha()
    card_back = pygame.transform.scale(card_back,(70,120))

    n = 7
    for i in range(n):
        x_coord = 260 + 80*i
        print(x_coord)
        screen.blit(card_back, (x_coord, 20))

        
    pygame.display.update()
    
    #Pass your user stuff to the UnoGame, so it can modify user data file accordingly
    game_Instance = uno_framework.UnoGame()
    deck = game_Instance.create_deck()
    (user_hand, ai_hand) = game_Instance.shuffle()

    #sets the start hands within the player and AI, inits them
    player_Instance = uno_framework.Player("John", user_hand)
    ai_Instance = uno_framework.AIPlayer(ai_hand)

    #If start clicked in menu, start the game, and set up
    game_Instance.start_clicked()
    game_on = game_Instance.get_game_status
    game_Instance.setup()

    

    while game_on:
             
            #function to just return the hands of each the
            your_hand = player_Instance.get_hand()
            ai_hand = ai_Instance.get_hand()
            #Gameover case or draw pile runs out cases
            game_Instance.turn_checks(your_hand, ai_hand)
            current_card = game_Instance.get_current_card()
            print(current_card)

            #This RETURN is the only important part of the test function. The card generating can be done elsewhere, normally
            return (card_img_from_text(current_card))
            game_on = False
            
'''

#updates all the background details
def start_bg_update():

    
    #the other background images - empty card slots, the banners, etc.
    #Arrows come later if/when needed

    #two sizes of card slot
    card_slot = pygame.image.load("UNO_IMG_ASSETS/other_assets/empty_card_frame.jpg").convert()
    large_card_slot = pygame.transform.scale(card_slot,(100,160))
    small_card_slot = pygame.transform.scale(card_slot,(70,120))
   
    
    #effect banner
    #convert_alpha() removes the black border on a transparent image
    effect_banner = pygame.image.load("UNO_IMG_ASSETS/other_assets/effect_banner.png").convert_alpha()
    effect_banner = pygame.transform.scale(effect_banner,(570,80))

    #effect banner
    #convert_alpha() removes the black border on a transparent image
    stat_banner = pygame.image.load("UNO_IMG_ASSETS/other_assets/stat_banner.png").convert_alpha()
    stat_banner = pygame.transform.scale(stat_banner,(240, 440))

    uno_btn = pygame.image.load("UNO_IMG_ASSETS/other_assets/uno_button.png").convert_alpha()
    uno_btn = pygame.transform.scale(uno_btn,(100, 80))
    uno_btn = imagebutton.Button(20, 480, uno_btn, 1.5)

    screen.fill((255, 255, 255))
    
    screen.blit(background, (0, 0))
    
    screen.blit(effect_banner, (250, 360))
    screen.blit(stat_banner, (10, 10))

    screen.blit(large_card_slot, (380, 180))
    screen.blit(large_card_slot, (580, 180))

    #blits your card slot and the AI card slots onto the screen 
    for i in range(260, 820, 80):
        screen.blit(small_card_slot, (i, 460))
        screen.blit(small_card_slot, (i, 20))

    uno_btn.draw(screen)

    pygame.display.update()
    time.sleep(3)
    
    #However, these cards need to be buttons (your cards only, the discard, draw and ai cards can be 
    
    '''
    path = mainish()
    test_card = pygame.image.load(f"{path}").convert()
    large_card_slot = pygame.transform.scale(card_slot,(100,160))
    test_small_card = pygame.transform.scale(test_card,(70,120))
    screen.blit(test_small_card , (340, 460))

    
    pygame.display.update()
    '''
    time.sleep(2)

    #The display.update() line comes AFTER youve added stuff on TOP of the background

#This renders the cards onto the screen   
def current_state_render(current_card, your_seven, ai_hand, card_flag, banner="", stats=""):

    #background first
    start_bg_update()
    #then the cards
    card_back = pygame.image.load("UNO_IMG_ASSETS/other_assets/card_back.png").convert_alpha()
    card_back_large = pygame.transform.scale(card_back,(100, 160))
    card_back_small = pygame.transform.scale(card_back,(70, 120))
    
    #blits current card
    curr_card_path = card_img_from_text(current_card)
    curr_card = pygame.image.load(f"{curr_card_path}").convert_alpha()
    curr_card = pygame.transform.scale(curr_card,(100, 160))
    screen.blit(curr_card, (380, 180))

    #blit the discard pile card back-icon if card_flag is NOT false.
    #the card_flag is false if no cards in draw pile 
    if (card_flag == True):
        screen.blit(card_back_large, (580, 180))

    n = len(ai_hand)
    #caps out the length at 7. AI card visibility does NOT matter as you dont see them anyway
    if n > 7:
        n = 7
        
    for i in range(n):
        x_coord = 260 + 80*i
        print(x_coord)
        screen.blit(card_back_small, (x_coord, 20))


    #The "your_seven" is ONLY the chosen 7 cards in your hand passed to this function
    #the arrow button alters this parameter value
    for i in range(len(your_seven)):

        #extracts an image filepath path from the cards iteratively
        your_card_path = card_img_from_text(your_seven[i]) 
        your_card = pygame.image.load(f'{your_card_path}').convert_alpha()
        your_card = pygame.transform.scale(your_card,(70,120))
    
        x_coord = 260 + 80*i
        print(x_coord)
        screen.blit(your_card, (x_coord, 460))

    #then the effect banners, stats
    print("RENDERED")   
    pygame.display.update()  
    
    

    
def info_menu():
    print("INFO")

    home_btn = pygame.image.load("UNO_IMG_ASSETS/other_assets/home_btn.png").convert_alpha()
    home_btn = pygame.transform.scale(home_btn,(80, 80))
    home_btn = imagebutton.Button(20, 460, home_btn, 1.5)
   
    info_running = True
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))

    title_font = pygame.font.SysFont("Raleway", 58, bold=False, italic=False)
    info_font = pygame.font.SysFont("Raleway", 30, bold=False, italic=False)

    
    #Load these lines from a file.
    info_title = title_font.render(f'{info_text[0].rstrip()}', False, (10, 30, 50))
    screen.blit(info_title, (300, 50))

    #read lines 2-8 (index 1-7)
    for i in range(7):  
        rule_msg = info_font.render(f'{info_text[i+1].rstrip()}', False, (10, 30, 50))
        screen.blit(rule_msg, (50, 150 + 50*i))

    info_text_7 = info_font.render(f'{info_text[8].rstrip()}', False, (10, 30, 50))
    screen.blit(info_text_7, (300, 520))
    
    pygame.display.update()

    
    
    while info_running:

        
        if home_btn.draw(screen):

            #call the start if home is pressed
            print("START")
            startup()
            running = False
     
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()

    pygame.quit()
      

def startup():

    title_txt = pygame.image.load("UNO_IMG_ASSETS/other_assets/title_text.png").convert_alpha()
    title_txt = pygame.transform.scale(title_txt,(300,300))
    

    start_btn = pygame.image.load("UNO_IMG_ASSETS/other_assets/start_btn.png").convert_alpha()
    start_btn = pygame.transform.scale(start_btn,(120, 80))
    start_btn = imagebutton.Button(350, 300, start_btn, 2)

    info_btn = pygame.image.load("UNO_IMG_ASSETS/other_assets/info_btn.png").convert_alpha()
    info_btn = pygame.transform.scale(info_btn,(80, 80))
    info_btn = imagebutton.Button(750, 460, info_btn, 1.5)
    
    
    running = True
    #The main start screen to start the game

    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    screen.blit(title_txt, (300, 40))

    pygame.display.update()
   
    while running:
   
        if start_btn.draw(screen):

            #call the start
            print("START")
            start_bg_update()
            running = False

        if info_btn.draw(screen):

            #call the info function
            info_menu()
            running = False
            
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False


        pygame.display.update()
        
    


#this function returns the appropriate card filepath when provided a card
def card_img_from_text(card):

    #keeps adding to the file path once
    cardfilepath = "UNO_IMG_ASSETS"

    #first use the color parameter, which is card[2] to select a subfolder
    #the subfolders are the same name as the color
    cardfilepath = cardfilepath + f"/{card[1]}"
    #then use the appropriate effect/number
    cardfilepath = cardfilepath + f"/{card[0]}"
    
    cardfilepath = cardfilepath + f".png"
    print(cardfilepath)
    return cardfilepath


startup()


#Pass your user stuff to the UnoGame, so it can modify user data file accordingly
game_Instance = uno_framework.UnoGame()
deck = game_Instance.create_deck()
(user_hand, ai_hand) = game_Instance.shuffle()

#sets the start hands within the player and AI, inits them
player_Instance = uno_framework.Player("John", user_hand)
ai_Instance = uno_framework.AIPlayer(ai_hand)

#If start clicked in menu, start the game, and set up
game_Instance.start_clicked()
game_on = game_Instance.get_game_status
game_Instance.setup()


#TODO: MERGE GAMELOOP INTO MAIN PROGRAM
#The only different thing is choosing the cards. That is done from event sensing in your turn.
#you are kept in a while loop (once validity check for your turn ends)
#until one of the cards are clicked

while game_on:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
         
        #function to just return the hands of each the
        your_hand = player_Instance.get_hand()
        ai_hand = ai_Instance.get_hand()
        #Gameover case or draw pile runs out cases
        game_Instance.turn_checks(your_hand, ai_hand)
        current_card = game_Instance.get_current_card()
        print(current_card)

        print(card_img_from_text(current_card))
        #put current card to top of discard pile 
        game_Instance.discard_card(current_card)

        #New_color is a flag for wild card abilities - changing color
        new_color = game_Instance.get_new_color()
        
        turn = game_Instance.get_turn()

        if ((len(your_hand))>7):
            your_seven = your_hand[0:7]
        else:
            your_seven = your_hand
            
        #banner="", stats=""
        card_flag = True
        current_state_render(current_card, your_seven, ai_hand, card_flag)
        if turn == "you":

            if current_card[0] == "draw 2" :
                print("Drawing 2 cards!")

                
                for i in range(2):
                    your_hand.append(game_Instance.draw_card())
                player_Instance.set_hand(your_hand)
                    
            elif current_card[0] == "draw 4":
                print("Drawing 4 cards!")
                for i in range(4):
                    your_hand.append(game_Instance.draw_card())
                player_Instance.set_hand(your_hand)




            if (current_card[0] == "reverse" or current_card[0] == "skip" or current_card[0] == "draw 4") \
               and (current_card[2] == True):
                
                current_card[2] = False
                
                print("Turn skip! AI turn!")
                #runs the AI turn instead
                turn = "ai"

                print(f"\nCurrent card: {current_card}")
                
                #the tuple is the return of the turn function
                (ai_hand, current_card) = ai_Instance.ai_turn_setup(current_card, new_color)
                valid_cards = game_Instance.validity_check(ai_hand, current_card)

                
                if valid_cards is not None:
                    #the tuple is unpacked if any valid cards present
                   
                    (current_card, new_color) = ai_Instance.ai_choose_card(valid_cards, current_card, new_color)

                    game_Instance.set_new_color(new_color)
                    game_Instance.discard_card(current_card)
                    game_Instance.set_current_card(current_card)
                    print(f"{current_card} has been discarded")

                else:
                    print("AI is drawing a card")
                    ai_hand.append(game_Instance.draw_card())


                game_Instance.set_turn("you")
             


            else:

                if (current_card[0] == "reverse" or current_card[0] == "skip" or current_card[0] == "draw 4") \
                   and (current_card[2] == False):

                    print(f"The turn skipping effect of the {current_card[0]} card has expired. It is in effect for only one turn.")

    
                (your_hand, current_card) = player_Instance.turn_setup(current_card, new_color)
                valid_cards = game_Instance.validity_check(your_hand, current_card)    
                
                #the tuple is unpacked if any valid cards present
                if valid_cards is not None:
                    
                    (current_card, new_color) = player_Instance.your_turn(valid_cards, current_card, new_color)
                    #The card's ability will be re enabled
                    current_card[2] = True
                    game_Instance.set_new_color(new_color)
                    game_Instance.discard_card(current_card)
                    game_Instance.set_current_card(current_card)
                    print(f"{current_card} has been discarded")

                #if no valid cards, drawing a card constitutes your turn 
                else:
                    print("You had no valid cards")
                    print("Drawing a card for you")
                    your_hand.append(game_Instance.draw_card())


                game_Instance.set_turn("ai")   
                
                
        elif turn == "ai":


            if current_card[0] == "draw 2" :
                print("AI drawing 2 cards!")
                for i in range(2):
                    ai_hand.append(game_Instance.draw_card())
            elif current_card[0] == "draw 4":
                print("AI drawing 4 cards!")
                for i in range(4):
                    ai_hand.append(game_Instance.draw_card())


            if (current_card[0] == "reverse" or current_card[0] == "skip" or current_card[0] == "draw 4") \
               and (current_card[2] == True):
                
                current_card[2] = False
                
                print("Turn skip! Your turn!")
                #runs the your turn instead
                turn = "you"

                print(f"\nCurrent card: {current_card}")
                
                #the tuple is the return of the turn function
                (your_hand, current_card) = player_Instance.turn_setup(current_card, new_color)
                valid_cards = game_Instance.validity_check(your_hand, current_card)
                
               
                
                if valid_cards is not None:
                    #the tuple is unpacked if any valid cards present
                    (current_card, new_color) = player_Instance.your_turn(valid_cards,current_card, new_color)
                    game_Instance.set_new_color(new_color)
                    game_Instance.discard_card(current_card)
                    game_Instance.set_current_card(current_card)
                    print(f"{current_card} has been discarded")
                   
                    
                else:
                    print("You had no valid cards")
                    print("Drawing a card for you")
                    your_hand.append(game_Instance.draw_card())
               
                game_Instance.set_turn("ai")   
                

            else:

                if (current_card[0] == "reverse" or current_card[0] == "skip" or current_card[0] == "draw 4") \
                    and (current_card[2] == False):

                    print(f"The turn skipping effect of the {current_card[0]} card has expired. It is in effect for only one turn.")

                     
                (ai_hand, current_card) = ai_Instance.ai_turn_setup(current_card, new_color)
                valid_cards = game_Instance.validity_check(ai_hand, current_card)
                
                if valid_cards is not None:
                    #the tuple is unpacked if any valid cards present
                    (current_card, new_color) = ai_Instance.ai_choose_card(valid_cards, current_card, new_color)

                    #The card's ability will be re enabled
                    current_card[2] = True

                    game_Instance.set_new_color(new_color)
                    game_Instance.discard_card(current_card)
                    game_Instance.set_current_card(current_card)
                    print(f"{current_card} has been discarded")
                   
                    
                else:
                    print("AI is drawing a card")
                    ai_hand.append(game_Instance.draw_card())

    
                game_Instance.set_turn("you")
                game_on = game_Instance.get_game_status

        
        pygame.display.update()


               
