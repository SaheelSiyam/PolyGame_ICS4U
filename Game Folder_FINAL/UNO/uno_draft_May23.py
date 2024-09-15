#STAGE 1: AI just picks whatever card matches the pile
#STAGE 2: AI has a tier list of cards via if statements (ie black cards first, if not then ability cards, if not, number cards, if not, draw a card
#Stage 3: You can level select. Easy is Stage 1, Hard is Stage 2

#There is a mechanic where the user gets a penalty of two cards (draw 2) at the next user's turn
# if they dont say uno by the end of their turn if they have one card left
#Introduce this mechanic later, when the UNO button can be programmed in


#TODO: 1. Turn into OOP
#   2: Add level select, harder

#Rule amendment to UNO: Draw 2 does NOT skip your turn

#import pygame
import random
import sys
import time
#UNO TEXT BASED - DRAFT


            
#generates a new deck
def new_deck():
    #Cards list: - 0-9 of each card, plus: uno reverse, skip turn, draw 2
    card_actions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "reverse", "skip", "draw 2"]
    #black cards are: - change color, draw 4. There are two of each those and they are black
    colors = ['red', 'yellow', 'green', 'blue']

    #Ability flag for each card. This flag will be enabled, but the same ability cant run twice
    #Once the ability is used once and it ISNT discarded, then the card ability will be disabled
    #The ability will be re-enabled just before it is discarded
    ability_enabled = True

    specials = [["draw 4", "black", True], ["change color", "black", True]]
    card_set = []

    #Adding regular cards
    for i in range(len(card_actions)):
        current_number = card_actions[i]
        current_color = "blank"
        for c in range(len(colors)):
            current_color = colors[c]
            current_card = [current_number, current_color, ability_enabled]
            card_set.append(current_card)
    for i in range(2):
        for s in range(len(specials)):
            card_set.append(specials[s])

    return card_set      



#Returns a shuffled deck, plus your hand, and the AI's hand
def shuffle(card_set):
    
    random.shuffle(card_set)
    user_cards = []
    ai_cards = []
    
    for i in range(7):
        #takes out the top card
        user_cards.append(card_set.pop(0))
        ai_cards.append(card_set.pop(0))

    return card_set, user_cards, ai_cards
    #https://www.w3schools.com/python/python_tuples_unpack.asp




#returns a list of all cards in the hand which match either parameter of the current card
def validity_check(hand, card):

    valid_cards = []
    valid_card_present = True

    for i in range(len(hand)):

        
        #match action/number is relevant only if its not a draw 4 or a color change
        if card[0] == hand[i][0]:
            valid_cards.append(i)
        #match color
        if card[1] == hand[i][1]:
            valid_cards.append(i)
        #OR black cards. Black cards can match any color or number
        elif hand[i][1] == "black":
            valid_cards.append(i)

    if len(valid_cards) == 0:
        #draw a card function
        #add card to hand
        return None
    else:
        return valid_cards



    
def ai_turn(ai_hand, current_card, new_color):
    
    print("AI turn: \n")

    #forces the AI to match the color if any new color was chosen via Wild/Black cards

    
    #However, we dont want to EXPORT these modified color cards. They are changed back to black in the end
    if new_color != "no":
        current_card[1] = new_color
        print(f"Current color is {new_color}")
        #See: 1A
    
    
    #
    print("AI hand: ")
    for n in range(len(ai_hand)):
        print(f"{n+1}: {ai_hand[n]}")
    #
    
    valid_cards = validity_check(ai_hand, current_card)

    #1A: Changing the color of the current_card back to black
    if new_color != "no":
        current_card[1] = "black"
    
    
    #print(valid_cards)
    
    if valid_cards == None:
        print("AI had no valid cards")
        #skips to next turn
        return None
    
    else:
        
        #AI chooses first card in this list
        card_to_discard = ai_hand.pop(valid_cards[0])
        print(f"AI chose: {card_to_discard}")

        
        if card_to_discard[1] == "black":
            #choose random color

            colors = ['red', 'yellow', 'green', 'blue']
            chosen_color = random.randint(0, 3)
            new_color = colors[chosen_color]
            print(f"The AI has chosen the new color {new_color}")

            
        else:
            new_color = "no"

            

        #AI declare UNO if length is 1. Also calls gameover function if you put last card
        if len(ai_hand) == 1:
            print("AI GETS AN UNO!")


        
        print(f"AI has {len(ai_hand)} cards remaining")
        time.sleep(1)
        return ai_hand, card_to_discard, new_color


def your_turn(your_hand, current_card, new_color):

    #However, we dont want to EXPORT these modified color cards. They are changed back to black in the end. See 1A
    if new_color != "no":
        current_card[1] = new_color
        print(f"Current color is {new_color}")

    
    print("Your turn: \n")
    
    print("Your hand: ")
    for n in range(len(your_hand)):
        print(f"{n+1}: {your_hand[n]}")
    valid_cards = validity_check(your_hand, current_card)


    #1A: Changing the color of the current_card back to black
    if new_color != "no":
        current_card[1] = "black"

    
    if valid_cards == None:
        print("You had no valid cards")
        return None

    
    else:
        print('\n')
        for index in valid_cards:
            print(f"Card number {index+1} is valid")
        #Lets you choose a VALID card as a number. The cards are ordered in the list

        choice_valid = False
        print('\n')
        choice = (int(input("Choose a card number: ")))-1
        
        if choice in valid_cards:
            choice_valid = True
            
        while not choice_valid:
            choice = int(input("\nChoose a valid card number: "))
            
            if choice in valid_cards:
                choice_valid = True

                
        card_to_discard = your_hand.pop(choice)
        print(f"You chose: {card_to_discard}")

        #Lets user choose a color if the card drawn is black. The exported card becomes a "draw 4" or a "color change" 
        if card_to_discard[1] == "black":

            
            choice_valid = False
            print('\n')
            chosen_color = input("Choose a color (red, yellow, green, blue) CASE AND SPELLING SENSITIVE!: ")
            colors = ['red', 'yellow', 'green', 'blue']
            
            if chosen_color in colors:
                choice_valid = True
                new_color = chosen_color
                
                
            while not choice_valid:
                choice = int(input("Choose a VALID color (red, yellow, green, blue) CASE AND SPELLING SENSITIVE!: "))
                
                if choice in colors:
                    choice_valid = True
                    new_color = chosen_color

            #Changes the color back to black, so we dont get mutated wild cards
            #current_card[1] = "black"
            
            print(f"You have chosen the color: {chosen_color}")
        else:
            new_color = "no"  
            
        #Allows user to declare UNO if length is 1. Also calls gameover function if you put last card
        if len(your_hand) == 1:
            print("YOU GET AN UNO!")

        #remember that we need the objects to be globally altered without using global designation
        time.sleep(1)
        return your_hand, card_to_discard, new_color



def main():

    
    #options
    print("MENU")
    #Call a menu function when the GUI development starts

    game_on = True
    turn = "you"
    
    #Imported tuple from shuffle()
    start_deck = new_deck()
    megadata = shuffle(start_deck)
    (start_pile, your_hand, ai_hand) = megadata
    current_card = []
    discard_pile = []
    new_card = []

    turn_reverse_flag = False
    
    
    current_card = start_pile.pop()

    valid_current_card = False

    #Cant have wild card OR ability card as the start card
    while not valid_current_card:
        if isinstance(current_card[0], int):
            valid_current_card = True
        else:
            print(f"The card was {current_card}")
            print("Cannot have a wild card or ability card as start. Drawing again: ")
            current_card = start_pile.pop()
    
    discard_pile.append(current_card)
    new_color = "no"
    print(f"Start card: {current_card}")


    #Main game loop

    
    while game_on:

        
        #Checks if draw pile runs out
        if len(start_pile) == 0:
            print("No cards remaining in draw pile! Shuffling discard pile")
            
            start_pile = random.shuffle(discard_pile())
            discard_pile = []


        #checks length of the hand for gameover cases
        if len(your_hand) == 0:
            gameover(True)
        elif len(ai_hand) == 0:
            gameover(False)

        print(f"\nCurrent card: {current_card}")


        
        if turn == "you":

            if current_card[0] == "draw 2" :
                print("Drawing 2 cards!")
                for i in range(2):
                    your_hand.append(start_pile.pop())
                    
            elif current_card[0] == "draw 4":
                print("Drawing 4 cards!")
                for i in range(4):
                    your_hand.append(start_pile.pop())


            if (current_card[0] == "reverse" or current_card[0] == "skip" or current_card[0] == "draw 4") \
               and (current_card[2] == True):
                
                current_card[2] = False
                
                print("Turn skip! AI turn!")
                #runs the AI turn instead
                turn = "ai"

                print(f"\nCurrent card: {current_card}")
                
                #the tuple is the return of the turn function
                turn_data = ai_turn(ai_hand, current_card, new_color)

                
                if turn_data is not None:
                    #the tuple is unpacked if any valid cards present
                    (ai_hand, current_card, new_color) = turn_data

                    print(f"{current_card} has been discarded")
                    discard_pile.insert(0, current_card)
                    
                else:
                    print("AI is drawing a card")
                    ai_hand.append(start_pile.pop())

               
                turn = "you"

            else:

                if (current_card[0] == "reverse" or current_card[0] == "skip" or current_card[0] == "draw 4") \
                   and (current_card[2] == False):

                    print(f"The turn skipping effect of the {current_card[0]} card has expired. It is in effect for only one turn.")

                   
                     
                
                #the tuple is the return of the turn function
                turn_data = your_turn(your_hand, current_card, new_color)
                if turn_data is not None:
                    #the tuple is unpacked if any valid cards present
                    (your_hand, current_card, new_color) = turn_data

                    #The card's ability will be re enabled
                    current_card[2] = True
                     
                    print(f"{current_card} has been discarded")
                    discard_pile.insert(0, current_card)

                    
                else:
                    print("Drawing a card for you")
                    your_hand.append(start_pile.pop())

                    
               

                
                turn = "ai"
                
        elif turn == "ai":


            if current_card[0] == "draw 2" :
                print("AI drawing 2 cards!")
                for i in range(2):
                    ai_hand.append(start_pile.pop())
            elif current_card[0] == "draw 4":
                print("AI drawing 4 cards!")
                for i in range(4):
                    ai_hand.append(start_pile.pop())


            if (current_card[0] == "reverse" or current_card[0] == "skip" or current_card[0] == "draw 4") \
               and (current_card[2] == True):
                
                current_card[2] = False
                
                print("Turn skip! Your turn!")
                #runs the your turn instead
                turn = "you"

                print(f"\nCurrent card: {current_card}")
                
                #the tuple is the return of the turn function
                turn_data = your_turn(your_hand, current_card, new_color)
                
                if turn_data is not None:
                    #the tuple is unpacked if any valid cards present
                    (your_hand, current_card, new_color) = turn_data
                    
                    print(f"{current_card} has been discarded")
                    discard_pile.insert(0, current_card)
                    
                else:
                    print("Drawing a card for you")
                    your_hand.append(start_pile.pop())
               
                    
                turn = "ai"

            else:

                if (current_card[0] == "reverse" or current_card[0] == "skip" or current_card[0] == "draw 4") \
                    and (current_card[2] == False):

                    print(f"The turn skipping effect of the {current_card[0]} card has expired. It is in effect for only one turn.")

                    
                     
                
                #the tuple is the return of the turn function
                turn_data = ai_turn(ai_hand, current_card, new_color)
                
                if turn_data is not None:
                    #the tuple is unpacked if any valid cards present
                    (ai_hand, current_card, new_color) = turn_data

                    #The card's ability will be re enabled
                    current_card[2] = True
                    
                    #
                    print(f"{current_card} has been discarded")
                    discard_pile.insert(0, current_card)
                    #
                    
                else:
                    print("AI is drawing a card")
                    ai_hand.append(start_pile.pop())

                turn = "you"

        

 #Every victory gives you 500 points for every victory 
def gameover(won):

    if won:
        print("You won")
    else:
        print("AI won")
        

    print("Game Over")
    sys.exit()




main()

