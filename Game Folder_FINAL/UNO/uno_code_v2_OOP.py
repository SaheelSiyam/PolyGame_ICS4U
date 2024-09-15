import random
import sys
import time


#Main game loop occurs outside the classes

class UnoGame():

    #The card set could be a self attribute, as well as score. 
    def __init__(self):
        
        self.deck = []

        self.turn = "you"

        #Starts as false until the startup occurs when
        #user clicks start
        #To True when game starts, false when game ends
        self.game_status = False

        self.current_card = []
        self.draw_pile = []
        self.discard_pile = []

        self.new_color = "no"
        
        print(self.deck)

    def get_game_status(self):
        return self.game_status
    
    
    #To see what the turn is currently
    def get_turn(self):
        return self.turn
        
    #Turn value toggles at the end of each turn
    def set_turn(self, turn):
        self.turn = turn

    #for turn methods in Player() and AI() classes
    def get_current_card(self):
        return self.current_card
        
    #Card changes after each turn
    def set_current_card(self, current_card):
        self.current_card = current_card

    #New_color is a flag for wild card abilities.
    def get_new_color(self):
        return self.new_color
    
    def set_new_color(self, new_color):
        self.new_color = new_color


    #returns a card from the draw pile,
    def draw_card(self):
        return self.draw_pile.pop()

    
    #discards a card
    def discard_card(self, card):
        self.discard_pile.insert(0, card)
    

        
    #Call a menu function when the GUI development starts
    def startup(self):
        #calls the menu
        print("MENU")


    #On start button clicked
    def start_clicked(self):
        self.game_status = True
        self.turn = "you"
    
             
    def create_deck(self):
        
        #print("TEST")

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
        
        self.deck = card_set
        return self.deck


    #Returns a shuffled deck as a tuple, plus your hand, and the AI's hand
    def shuffle(self):

        #shuffle the deck
        random.shuffle(self.deck)
        user_cards = []
        ai_cards = []
        
        for i in range(7):
            #takes out the top card
            user_cards.append(self.deck.pop(0))
            ai_cards.append(self.deck.pop(0))

        self.draw_pile = self.deck

        #Dont need to return self.deck anymore, its global within the class, an instance variable
        return user_cards, ai_cards
        #https://www.w3schools.com/python/python_tuples_unpack.asp

    def turn_checks(self, your_hand, ai_hand):
        
         #Checks if draw pile runs out
        if len(self.draw_pile) == 0:
            print("No cards remaining in draw pile! Shuffling discard pile")
            
            start_pile = random.shuffle(discard_pile())
            discard_pile = []

        
        #checks length of the hand for gameover cases
        if len(your_hand) == 0:
            self.gameover(True)
        elif len(ai_hand) == 0:
            self.gameover(False)

        #Proceeds
        print(f"\nCurrent card: {self.current_card}")

        
    
    def setup(self):
         #options
    
    
        #This works if create_deck() and shuffle() is called before setup()
        
        self.current_card = self.draw_pile.pop()

        valid_current_card = False

        #Cant have wild card OR ability card as the start card
        while not valid_current_card:
            if isinstance(self.current_card[0], int):
                valid_current_card = True
            else:
                print(f"The card was {self.current_card}")
                print("Cannot have a wild card or ability card as start. Drawing again: ")
                self.current_card = self.draw_pile.pop()
        
        self.discard_pile.append(self.current_card)
        self.new_color = "no"
        print(f"Start card: {self.current_card}")

    
    
    #returns a list of all cards in the hand which match either parameter of the current card
    def validity_check(self, hand, card):

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
    

     #Gameover method
    def gameover(self, won):

        self.game_status = False

        if won:
            print("You won")
        else:
            print("AI won")
        sys.exit()


class AIPlayer():
    def __init__(self, hand):
         self.hand = hand

    def setup_turn(self, current_card, new_color):
        
        print("###")


    def get_hand(self):
        return self.hand

    def set_hand(self, hand):
         self.hand = hand

    
    def ai_turn_setup(self, current_card, new_color):

        #forces the AI to match the color if any new color was chosen via Wild/Black cards
        print("AI turn: \n")
         
        #However, we dont want to EXPORT these modified color cards. They are changed back to black in the end
        if new_color != "no":
            current_card[1] = new_color
            print(f"Current color is {new_color}")
            #See: 1A
         
        #
        print("AI hand: ")
        for n in range(len(self.hand)):
            print(f"{n+1}: {ai_hand[n]}")
    
        #This is where the method exits the class and transfers this to the main game class method
        return self.hand, current_card
        #valid_cards = validity_check(self.hand, current_card)

       
    #This is ONCE we have a set of valid cards. current card doesnt matter
  
    def ai_choose_card(self, valid_cards, current_card, new_color):
        
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
            card_to_discard = self.hand.pop(valid_cards[0])
            print(f"AI chose: {card_to_discard}")

            
            if card_to_discard[1] == "black":
                #choose random color

                colors = ['red', 'yellow', 'green', 'blue']
                chosen_color = random.randint(0, 3)
                new_color = colors[chosen_color]
                print(f"The AI has chosen the new color {new_color}")

                
            else:
                new_color = "no"

                

            #AI declare UNO if length is 1. 
            if len(self.hand) == 1:
                print("AI GETS AN UNO!")


            
            print(f"AI has {len(self.hand)} cards remaining")
            time.sleep(1)
            return card_to_discard, new_color
            
            
'''           
class HarderAIPlayer(AIPlayer):
    def __init__(self, hand):
    super().__init__(self, hand)
'''
    

class Player():
    
    def __init__(self, userID, hand):


        self.userID = userID
        
        self.hand = hand
        

    '''
    def get_user_data(self):
        #Search through file for user data, add upgrades before game, etc
    def set_user_data(self):
        #Search through file for user data, set data like scores, at end of game
        #or set data when the upgrades were used up.
    '''
    
    def get_hand(self):
        return self.hand

    def set_hand(self, hand):
        self.hand = hand


    def turn_setup(self, current_card, new_color):

        #In this player object, we "turn" the current card into the new color
        if new_color != "no":
            current_card[1] = new_color
            print(f"Current color is {new_color}")

        print("Your turn: \n")
        
        print("Your hand: ")
        for n in range(len(self.hand)):
            print(f"{n+1}: {self.hand[n]}")

        #VALIDITY CHECK! EXIT FUNCTION!
            
        return self.hand, current_card
    

    #Once you have a list of valid cards that is NOT: NONE    
    def your_turn(self, valid_cards, current_card, new_color):

        #changing the card back to black, once the validity check is over
        if new_color != "no":
            current_card[1] = "black"
        
        print('\n')
        for index in valid_cards:
            print(f"Card number {index+1} is valid")
        #Lets you choose a VALID card as a number.
        #The cards are ordered in the list

        choice_valid = False
        print('\n')
        # -1 because of index starting at 0
        choice = (int(input("Choose a card number: ")))-1
        
        if choice in valid_cards:
            choice_valid = True
            
        while not choice_valid:
            choice = int(input("\nChoose a valid card number: "))
            
            if choice in valid_cards:
                choice_valid = True

                
        card_to_discard = self.hand.pop(choice)
        print(f"You chose: {card_to_discard}")

        #Lets user choose a color if the card drawn is black.
        #The exported card becomes a "draw 4" or a "color change" 
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

           
            
            print(f"You have chosen the color: {chosen_color}")
            
        else:
            new_color = "no"  
            
        #Allows user to declare UNO if length is 1.

        #Penalty function introduced later. On click event,
        #if not clicked by end of turn, then penalty
        if len(self.hand) == 1:
            print("YOU GET AN UNO!")

        #remember that we need the objects to be globally altered without using global designation
        time.sleep(1)

        #We run the discard_card() method, and set_new_color() methods
        return card_to_discard, new_color


      
   

#Pass your user stuff to the UnoGame, so it can modify user data file accordingly
game_Instance = UnoGame()
deck = game_Instance.create_deck()
(user_hand, ai_hand) = game_Instance.shuffle()

#sets the start hands within the player and AI, inits them
player_Instance = Player("John", user_hand)
ai_Instance = AIPlayer(ai_hand)

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
        #put current card to top of discard pile 
        game_Instance.discard_card(current_card)

        #New_color is a flag for wild card abilities - changing color
        new_color = game_Instance.get_new_color()
        
        turn = game_Instance.get_turn()
        
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
               
