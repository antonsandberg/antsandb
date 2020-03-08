""" Oliver Johansson and Anton Sandberg """
""" Computer Assignment 3 """
""" Group 7 """
from PyQt5.QtCore import*
import fortsCardLib
import time

class Player(QObject):
    """ Creating the class for the player(s) that starts the player off """

    def __init__(self, name):
        self.name = name
        self.money = 500
        self.hand = fortsCardLib.Hand()
        self.bet = 0

class TexasHoldemModel(QObject):

    def __init__(self):
        super().__init__()


        # Känns som dessa borde sättas på ställena de ska vara på snarare än i början

        self.num_table_cards = 0    #
        self.players = [Player("Player1"), Player("Player2")]
        self.pot = 0
        self.turn = 0  # Decides whos turn it is, 0 = P1, 1 = P2
        self.players[0].blind = 20  #Player1 starts with small blind
        self.players[1].blind = 40  #Player2 with big blind
        self.round_turn = 0  # decides who starts the next round
        self.check_count = 0  # Counts if both players check
        self.Winner = 0  # The final winner
        self.newRound()




        self.players[0].money += - self.players[0].blind
        self.players[1].money += - self.players[1].blind
        self.pot += self.players[0].blind + self.players[1].blind  # adds the bet to the pot

        new_cards = pyqtSignal()    #Dessa kommer behövas
        new_data = pyqtSignal()
        WinGame = pyqtSignal()


    def WhoWon(self):
        """ A function that checks whos hand is better, who won this round, uses our earlier defined PokerHand
        to determine a winner"""

        player_hand1 = self.players[0].hand.cards + self.table.table        # Adding together cards on hand with table
        player_hand2 = self.players[1].hand.cards + self.table.table        # cards

        check_hand1 = fortsCardLib.PokerHand(player_hand1)
        check_hand2 = fortsCardLib.PokerHand(player_hand2)

        if check_hand1.ranking > check_hand2.ranking:
            time.sleep(5.0)
            self.WinnerofRound(0)

        elif check_hand1.ranking < check_hand2.ranking:
            time.sleep(5.0)
            self.WinnerofRound(1)

        elif check_hand1.ranking == check_hand2.ranking:
            if check_hand1.ranking == 4 | 8:       # Special conditions for twopair and full house
                if check_hand1.value[0] > check_hand2.value[0]:
                    self.WinnerofRound(0)
                elif check_hand1.value[0] < check_hand2.value[0]:
                    self.WinnerofRound(1)
                elif check_hand1.value[0] == check_hand2.value[0]:
                    if check_hand1.value[1] > check_hand2.value[1]:
                        self.WinnerofRound(0)
                    elif check_hand1.value[1] < check_hand2.value[1]:
                        self.WinnerofRound(1)
        else:
            self.draw()









    def WinnerofRound(self, RoundWinner):
        """ Checks the winner of the round, input is either 0 or 1 depending on if it's player 1 or 2 """

        self.players[RoundWinner].money += self.pot
        self.round_winner = RoundWinner + 1  # For the display of winner

        if self.players[0].money == 0:
            self.Winner = 1                  #For the display of game winner
            self.WinGame.emit()

        elif self.players[1].money == 0:
            self.Winner = 0
            self.WinGame.emit()
        self.new_data.emit()
        pass




    def bet(self, amount):
        """ The bet function, needs to be able to check what the user is typing in the input
        aswell as know whos turn it is """

#        if self.turn == 0:



        pass



    def draw(self):
        """ Method that is called when the current round concludes in a draw """

        for player in self.players:
            self.player[player-1].money = self.pot/2

        self.reset()


    def CheckorFold(self):
        """ Function to check or fold dependant on if the user need to call to be able to continue playing the round """
        if self.turn == 0:
            self.WinnerofRound(1)
        else:
            self.WinnerofRound(0)
        pass






    def call(self):
        """ Call function, needs to check how much the player needs to put in to be able to call aswell as if the
         player can afford to """
        pass



    def CardtoTable(self):
        """ Function to insert more card to the table, 3 the first round, 1 and 1 more the other 2, need to call
        on WhoWon when the river card is out and both players made their turns """
        pass

    def newRound(self):
        """ The function that resets the round to able to start the next round """
        self.pot = 0
        self.Deck = fortsCardLib.StandardDeck()
        self.Deck.shuffle()

        for i in self.players:
            newcard = self.Deck.card()
            i.hand.add_card(newcard)

        self.table = []
        self.num_table_cards = 0
