#Game of UNO
#Supports multiple players on one device
#Option to play with robot players that randomly choose cards to play

import random

class UnoCard:
    '''represents an Uno card
    attributes:
      rank: int from 0 to 9
      color: string'''

    def __init__(self, rank, color):
        '''UnoCard(rank, color) -> UnoCard
        creates an Uno card with the given rank and color'''
        self.rank = rank
        self.color = color

    def __str__(self):
        '''str(Unocard) -> str'''
        return(str(self.color) + ' ' + str(self.rank))

    def is_match(self, other):
        '''UnoCard.is_match(UnoCard) -> boolean
        returns True if the cards match in rank or color, False if not'''
        if self.rank == 'normal wild' or self.rank == 'draw 4 wild' or self.color == '':
            return True
        else:
            return (self.color == other.color) or (self.rank == other.rank)
    

class UnoDeck:
    '''represents a deck of Uno cards
    attribute:
      deck: list of UnoCards'''

    def __init__(self):
        '''UnoDeck() -> UnoDeck
        creates a new full Uno deck'''
        self.deck = []
        for color in ['red', 'blue', 'green', 'yellow']:
            self.deck.append(UnoCard(0, color))  # one 0 of each color
            for i in range(2):
                self.deck.append(UnoCard('reverse', color))   #Two of each action for each color
                self.deck.append(UnoCard('skip', color))
                self.deck.append(UnoCard('draw', color))
                for n in range(1, 10):  # two of each of 1-9 of each color
                    self.deck.append(UnoCard(n, color))
        for i in range(4):
            self.deck.append(UnoCard('normal wild', ''))
            self.deck.append(UnoCard('draw 4 wild', ''))                                
        random.shuffle(self.deck)  # shuffle the deck

    def __str__(self):
        '''str(Unodeck) -> str'''
        return 'An Uno deck with '+ str(len(self.deck)) + ' cards remaining.'

    def is_empty(self):
        '''UnoDeck.is_empty() -> boolean
        returns True if the deck is empty, False otherwise'''
        return len(self.deck) == 0

    def deal_card(self):
        '''UnoDeck.deal_card() -> UnoCard
        deals a card from the deck and returns it
        (the dealt card is removed from the deck)'''
        return self.deck.pop()

    def reset_deck(self, pile):
        '''UnoDeck.reset_deck(pile) -> None
        resets the deck from the pile'''
        if len(self.deck) != 0:
            return
        self.deck = pile.reset_pile() # get cards from the pile
        for card in self.deck:
            if card.rank == 'draw four wild':
                card.color = ''
            if card.rank == 'normal wild':
                card.color = ''
            
        random.shuffle(self.deck)  # shuffle the deck

class UnoPile:
    '''represents the discard pile in Uno
    attribute:
      pile: list of UnoCards'''

    def __init__(self, deck):
        '''UnoPile(deck) -> UnoPile
        creates a new pile by drawing a card from the deck'''
        card = deck.deal_card()
        self.pile = [card]  # all the cards in the pile

    def __str__(self):
        '''str(UnoPile) -> str'''
        return 'The pile has ' + str(self.pile[-1]) + ' on top.'

    def top_card(self):
        '''UnoPile.top_card() -> UnoCard
        returns the top card in the pile'''
        return self.pile[-1]

    def add_card(self, card):
        '''UnoPile.add_card(card) -> None
        adds the card to the top of the pile'''
        self.pile.append(card)

    def reset_pile(self):
        '''UnoPile.reset_pile() -> list
        removes all but the top card from the pile and
          returns the rest of the cards as a list of UnoCards'''
        newdeck = self.pile[:-1]
        self.pile = [self.pile[-1]]
        return newdeck
    
    def get_length(self):        #Used for checking if pile length changed after a turn
        '''UnoPile.pile.get_length() -> int
        Returns the length of the pile'''
        return len(self.pile)

class UnoPlayer:
    '''represents a player of Uno
    attributes:
      name: a string with the player's name
      hand: a list of UnoCards'''

    def __init__(self, name, deck):
        '''UnoPlayer(name, deck) -> UnoPlayer
        creates a new player with a new 7-card hand'''
        self.name = name
        self.hand = [deck.deal_card() for i in range(7)]

    def __str__(self):
        '''str(UnoPlayer) -> UnoPlayer'''
        return str(self.name) + ' has ' + str(len(self.hand)) + ' cards.'

    def get_name(self):
        '''UnoPlayer.get_name() -> str
        returns the player's name'''
        return self.name

    def get_hand(self):
        '''get_hand(self) -> str
        returns a string representation of the hand, one card per line'''
        output = ''
        for card in self.hand:
            output += str(card) + '\n'
        return output

    def has_won(self):
        '''UnoPlayer.has_won() -> boolean
        returns True if the player's hand is empty (player has won)'''
        return len(self.hand) == 0

    def draw_card(self, deck):
        '''UnoPlayer.draw_card(deck) -> UnoCard
        draws a card, adds to the player's hand
          and returns the card drawn'''
        card = deck.deal_card()  # get card from the deck
        self.hand.append(card)   # add this card to the hand
        return card

    def play_card(self, card, pile):
        '''UnoPlayer.play_card(card, pile) -> None
        plays a card from the player's hand to the pile
        CAUTION: does not check if the play is legal!'''
        self.hand.remove(card)
        pile.add_card(card)

    def take_turn_human(self, deck, pile):
        '''UnoPlayer.take_turn(deck, pile) -> None
        takes the human's turn in the game
          deck is an UnoDeck representing the current deck
          pile is an UnoPile representing the discard pile'''

        # print player info
        print(self.name + ", it's your turn.")
        print(pile)
        print("Your hand: ")
        print(self.get_hand())
        # get a list of cards that can be played
        topcard = pile.top_card()
        matches = [card for card in self.hand if card.is_match(topcard)]
        if len(matches) > 0:  # can play
            for index in range(len(matches)):
                # print the playable cards with their number
                print(str(index + 1) + ": " + str(matches[index]))
            # get player's choice of which card to play
            choice = 0
            while choice < 1 or choice > len(matches):
                choicestr = input("Which do you want to play? ")
                if choicestr.isdigit():
                    choice = int(choicestr)
            # play the chosen card from hand, add it to the pile
            self.play_card(matches[choice - 1], pile)

        else:  # can't play
            print("You can't play, so you have to draw.")
            input("Press enter to draw.")
            # check if deck is empty -- if so, reset it
            if deck.is_empty():
                deck.reset_deck(pile)
            # draw a new card from the deck
            newcard = self.draw_card(deck)
            print("You drew: "+str(newcard))
            if newcard.is_match(topcard): # can be played
                print("Good -- you can play that!")
                self.play_card(newcard,pile)

            else:   # still can't play
                print("Sorry, you still can't play.")

            input("Press enter to continue.")


    def take_turn_robot(self, deck, pile):
        '''UnoPlayer.take_turn(deck, pile) -> None
        takes the human's turn in the game
          deck is an UnoDeck representing the current deck
          pile is an UnoPile representing the discard pile'''

        # print robot's info
        print("It is " + str(self.name) + "'s turn" )
        print(self.get_hand())
        # get a list of cards that can be played
        topcard = pile.top_card()
        matches = [card for card in self.hand if card.is_match(topcard)]
        if len(matches) > 0: 
            choice = random.randrange(0, len(matches))
            self.play_card(matches[choice], pile)
            print(str(self.name) + " has played a " + str(matches[choice]))

        else:  # can't play
            if deck.is_empty():
                deck.reset_deck(pile)
            newcard = self.draw_card(deck)
            if newcard.is_match(topcard): # can be played
                self.play_card(newcard,pile)
            else:   
                print(str(self.name) + " cannot play a card.")
            

def play_uno(numHumans, numRobots):
    '''play_uno(numPlayers) -> None
    plays a game of Uno with numPlayers'''
    # set up full deck and initial discard pile
    deck = UnoDeck()
    pile = UnoPile(deck)
    # set up the players
    numPlayers = numHumans + numRobots
    playerList = []
    playerDict = {}
    for n in range(numHumans):
        # get each player's name, then create an UnoPlayer
        name = input('Player #' + str(n + 1) + ', enter your name: ')
        playerDict[name] = "human"
        playerList.append(UnoPlayer(name,deck))
    for n in range(numRobots):
        playerList.append(UnoPlayer("Robot #" + str(n+1), deck))
        playerDict["Robot #" + str(n+1)] = "robot"
    # randomly assign who goes first
    currentPlayerNum = random.randrange(numHumans + numRobots)
    # play the game
    while True:
        # print the game status
        print('-------')
        for player in playerList:
            print(player)
        print('-------')
        # take a turn
        oldPileLength = pile.get_length()
        if playerDict[playerList[currentPlayerNum].name] == "human":
            playerList[currentPlayerNum].take_turn_human(deck, pile)  #Normal turn
        else:
            playerList[currentPlayerNum].take_turn_robot(deck, pile)  #Robot turn
        newPileLength = pile.get_length()

        if newPileLength != oldPileLength and newPileLength != 1:   #Check if a new card was added (pile changed length)
                                                                    #Don't count case where the new pile length is 1 because that means a card was drawn, pile was reset, and the card was not played
            if pile.top_card().rank == 'reverse':    #Check if it's an action card
                print(str(playerList[currentPlayerNum].name)+ " has reversed the order!")
                playerList.reverse()   #Reverse the list of players
                currentPlayerNum = len(playerList) - currentPlayerNum - 1  #Set position of current player to new adjusted position
       
            if pile.top_card().rank == 'draw':
                # check if deck is empty -- if so, reset it
                print(str(playerList[(currentPlayerNum + 1) % numPlayers].name)+ " must draw two cards!")
                for i in range(2):
                    if deck.is_empty():
                        deck.reset_deck(pile)
                    playerList[(currentPlayerNum + 1) % numPlayers].draw_card(deck)    #Draw twice
                currentPlayerNum = (currentPlayerNum + 1) % numPlayers  #After drawing, skip

            if pile.top_card().rank == 'skip':
                print(str(playerList[currentPlayerNum].name) + " has skipped " + str(playerList[(currentPlayerNum + 1) % numPlayers].name)+ "'s turn!")
                currentPlayerNum = (currentPlayerNum + 1) % numPlayers  #Go to next player, then later in code it goes to next player again effectively skipping a player
        
            if pile.top_card().rank == 'normal wild':
                colorChoice = ''
                if playerDict[playerList[currentPlayerNum].name] == "human":   #If player is human
                    while colorChoice not in ['green', 'red', 'blue', 'yellow']:
                        colorChoice = input("Which color do you want to play? (red, blue, green, or yellow)")   #Ask which color to change it to
                    pile.top_card().color = colorChoice    #Adjust color of wild card
                    print(str(playerList[currentPlayerNum].name)+ " has changed the color to " + str(colorChoice) + "!")
                else:       #If player is robot
                    cardDict = {
                        "yellow": 0,
                        "red": 0,
                        "green": 0,
                        "blue": 0
                    }
                    for card in playerList[currentPlayerNum].hand:
                        if card.color in ["yellow", "red", "green", "blue"]:
                            cardDict[card.color] += 1
                    maxKey = max(cardDict, key=cardDict.get)
                    pile.top_card().color = maxKey
                    print(str(playerList[currentPlayerNum].name)+ " has changed the color to " + str(maxKey) + "!")


            if pile.top_card().rank == 'draw 4 wild':
                colorChoice = ''
                if playerDict[playerList[currentPlayerNum].name] == "human":   #If player is human
                    while colorChoice not in ['green', 'red', 'blue', 'yellow']:
                        colorChoice = input("Which color do you want to play? (red, blue, green, or yellow)")   #Ask which color to change it to
                    pile.top_card().color = colorChoice    #Adjust color of wild card
                    print(str(playerList[currentPlayerNum].name)+ " has changed the color to " + str(colorChoice) + " and " + str(playerList[(currentPlayerNum + 1) % numPlayers].name) + " has to draw 4!")
                    for i in range(4):
                        if deck.is_empty():
                            deck.reset_deck(pile)
                            playerList[(currentPlayerNum + 1) % numPlayers].draw_card(deck)

                else:       #If player is robot
                    cardDict = {
                        "yellow": 0,
                        "red": 0,
                        "green": 0,
                        "blue": 0
                    }
                    for card in playerList[currentPlayerNum].hand:
                        if card.color in ["yellow", "red", "green", "blue"]:
                            cardDict[card.color] += 1
                    maxKey = max(cardDict, key=cardDict.get)
                    pile.top_card().color = maxKey
                    print(str(playerList[currentPlayerNum].name)+ " has changed the color to " + str(maxKey) + " and " + str(playerList[(currentPlayerNum + 1) % numPlayers].name) + " has to draw 4!")
                    for i in range(4):
                        if deck.is_empty():
                            deck.reset_deck(pile)
                        playerList[(currentPlayerNum + 1) % numPlayers].draw_card(deck)


        # check for a winner
        if playerList[currentPlayerNum].has_won():
            print(playerList[currentPlayerNum].get_name() + " wins!")
            print("Thanks for playing!")
            break

        # go to the next player
        currentPlayerNum = (currentPlayerNum + 1) % numPlayers

#

numHumans = input("How many human players do you want? (Best gameplay if less than 8)")
numRobots = input("How many robot players do you want? (Best gameplay if less than 3)")
play_uno(int(numHumans), int(numRobots))
