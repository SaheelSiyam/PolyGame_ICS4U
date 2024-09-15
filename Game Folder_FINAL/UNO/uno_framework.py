import random
import sys
import time

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




    #New_color is a flag for wild card abilities.
    def get_discard_pile(self):
        return self.discard_pile

    def get_draw_pile(self):
        return self.draw_pile
   


        

    #returns a card from the draw pile,
    def draw_card(self):

        #Checks if draw pile runs out in the middle of a draw
        #empty lists evaluate to None
        if self.draw_pile == None or len(self.draw_pile) == 0:
            print("No cards remaining in draw pile! Shuffling discard pile")
            
            self.draw_pile = random.shuffle(self.discard_pile)
            self.discard_pile = []
        card = self.draw_pile.pop()
        if card[2] == False:
            card[2] = True
        return card
  
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
        if self.draw_pile == None:
            print("No cards remaining in draw pile! Shuffling discard pile")
            
            self.draw_pile = random.shuffle(self.discard_pile)
            self.discard_pile = []

        
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
            print(f"{n+1}: {self.hand[n]}")
    
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
    def your_turn(self, index, current_card, new_color):

        #changing the card back to black, once the validity check is over
        if new_color != "no":
            current_card[1] = "black"

        print(index)
        print(self.hand)
        card_to_discard = self.hand.pop(index)
        print(f"You chose: {card_to_discard}")
        
        #Lets user choose a color if the card drawn is black.
        #The exported card becomes a "draw 4" or a "color change" 
        if card_to_discard[1] == "black":

            #code = "CHA"
            #return code


                        
            choice_valid = False
            print('\n')
            chosen_color = input("Choose a color (red, yellow, green, blue) CASE AND SPELLING SENSITIVE!: ")
            colors = ['red', 'yellow', 'green', 'blue']
            
            if chosen_color in colors:
                choice_valid = True
                new_color = chosen_color
                
                
            while not choice_valid:
                choice = input("Choose a VALID color (red, yellow, green, blue) CASE AND SPELLING SENSITIVE!: ")
                
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


