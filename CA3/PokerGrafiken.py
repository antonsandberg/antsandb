""" Oliver Johansson and Anton Sandberg """
""" Computer Assignment 3 """
""" Group 7 """

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *
import sys

class PlayerView(QGroupBox):
    def __init__(self, player, cards, money):

        super().__init__()

        self.player = player
        self.cards = cards
        self.money = money
        self.playerlayout = QHBoxLayout()

        # Player button displayed right of players cards
        self.playerbuttons = QGridLayout()

        self.call = QPushButton(self)
        self.call.setText("Call")
        self.call.setStyleSheet("background-color:none;")
        self.bet = QPushButton(self)
        self.bet.setText("Bet")
        self.betamount = QSpinBox(self)
        self.betamount.setMaximum(self.money)
        self.checkfold = QPushButton(self)
        self.checkfold.setText("Check/fold")

        self.placeholder = QLabel(self)

        self.playerbuttons.addWidget(self.call, 1, 1)
        self.playerbuttons.addWidget(self.bet, 2, 1)
        self.playerbuttons.addWidget(self.betamount, 3, 1)
        self.playerbuttons.addWidget(self.checkfold, 4, 1)
        self.playerbuttons.addWidget(self.placeholder, 4, 2)

        # Player cards
        self.playercards = QHBoxLayout()
        self.FirstCard = QLabel(self)
        self.SecondCard = QLabel(self)
        self.playercards.addWidget(self.FirstCard)
        self.playercards.addWidget(self.SecondCard)


        # Info about player will be displayed left of players cards
        self.playerinfo = QGridLayout()

        self.playername = QLabel(self)
        self.playername.setText(self.player)
        self.currentmoney = QLabel(self)
        self.currentmoney.setText("Current Money:\n{}$".format(self.money))
        self.showcards = QPushButton(self)
        self.showcards.setText("Show Cards")

        self.playerinfo.addWidget(self.playername, 1, 2)
        self.playerinfo.addWidget(self.currentmoney, 3, 2)
        self.playerinfo.addWidget(self.showcards, 2, 2)
        self.playerinfo.addWidget(self.placeholder, 4, 1)

        # Creating a players layout
        self.playerlayout.addWidget(self.placeholder)
        self.playerlayout.addLayout(self.playerinfo)
        self.playerlayout.addLayout(self.playercards)
        self.playerlayout.addLayout(self.playerbuttons)
        self.playerlayout.addWidget(self.placeholder)

    def PlayerCards(self, cards):
        self.FirstCard.setPixmap(QPixmap(cards[0]))
        self.SecondCard.setPixmap(QPixmap(cards[1]))



class CardView(QGroupBox):
    """ A View widget that represents the table area displaying a players cards. """

    # We read all the card graphics as static class variables
    back_card = QSvgRenderer('cards/Red_Back_2.svg')

    def __init__(self, card_model):
        """
        Initializes the view to display the content of the given model
        :param cards_model: A model that represents a set of cards. Needs to support the CardModel interface.
        """
        super().__init__()
        self.cards = []
        self.CurrentCards(card_model)

    def read_cards(self):
        """
        Reads all the 52 cards from files.
        :return: Dictionary of SVG renderers
        """
        all_cards = dict()  # Dictionaries let us have convenient mappings between cards and their images
        for suit_file, suit in zip('HDSC', range(4)):  # Check the order of the suits here!!!
            for value_file, value in zip(['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'],
                                         range(2, 15)):
                file = value_file + suit_file
                key = (value, suit)  # I'm choosing this tuple to be the key for this dictionary
                all_cards[key] = QSvgRenderer('cards/' + file + '.svg')
        return all_cards

    def CurrentCards(self, cards):

        cardlist = list(map(lambda card: (card.get_value(), card.suit), cards))
        all_cards = self.read_cards()

        # Makes a "handlist" of actual cardimages
        for i in range(len(cards)):
            self.cards.append(all_cards[cardlist[i]])


class GameInfo(QGroupBox):

    def __init__(self, pot=10, currentbet=10, whosturn=1, winner=1):
        super().__init__()
        # Current poty and last round winner info
        self.pot_winner = QVBoxLayout()

        self.pot = QLabel(self)
        self.pot.setText("Current Pot:\n{}".format(pot))

        self.winner = QLabel(self)
        self.winner.setText("Last Round Winner Was:\n{}".format(winner))

        self.pot_winner.addWidget(self.pot)
        self.pot_winner.addWidget(self.winner)

        # Current bet and whos turn info
        self.currentbet_whosturn = QVBoxLayout()

        self.currentbet = QLabel(self)
        self.currentbet.setText("Current Bet:\n{}".format(currentbet))

        self.whosturn = QLabel(self)
        self.whosturn.setText("It's {}'s turn".format(whosturn))

        self.currentbet_whosturn.addWidget(self.currentbet)
        self.currentbet_whosturn.addWidget(self.whosturn)


class TableView(QGroupBox):
    """
    Class for table display of cards
    """

    def __init__(self):

        super().__init__()
        self.card1 = QLabel(self)
        self.card2 = QLabel(self)
        self.card3 = QLabel(self)
        self.card4 = QLabel(self)
        self.card5 = QLabel(self)

        self.tablerow = QHBoxLayout()
        self.tablerow.addWidget(self.card1)
        self.tablerow.addWidget(self.card2)
        self.tablerow.addWidget(self.card3)
        self.tablerow.addWidget(self.card4)
        self.tablerow.addWidget(self.card5)

    def table_card_change(self, cards):
        """
        updating cards on table depending on turn
        :param cards: cards on pokertable

        """
        self.Cardimage = (["cards/Red_Back_2.svg", "cards/Red_Back_2.svg", "cards/Red_Back_2.svg", "cards/Red_Back_2.svg", "cards/Red_Back_2.svg"])

        if len(cards) == 0:
            self.card1.setPixmap(QPixmap(self.Cardimage[0]))
            self.card2.setPixmap(QPixmap(self.Cardimage[0]))
            self.card3.setPixmap(QPixmap(self.Cardimage[0]))
            self.card4.setPixmap(QPixmap(self.Cardimage[0]))
            self.card5.setPixmap(QPixmap(self.Cardimage[0]))
        elif len(cards) == 3:
            self.Cardimage[0] = cards[0]
            self.Cardimage[1] = cards[1]
            self.Cardimage[2] = cards[2]
            self.card1.setPixmap(QPixmap(self.Cardimage[0]))
            self.card2.setPixmap(QPixmap(self.Cardimage[1]))
            self.card3.setPixmap(QPixmap(self.Cardimage[2]))
            self.card4.setPixmap(QPixmap(self.Cardimage[3]))
            self.card5.setPixmap(QPixmap(self.Cardimage[4]))
        elif len(cards) == 4:
            self.Cardimage[0] = cards[0]
            self.Cardimage[1] = cards[1]
            self.Cardimage[2] = cards[2]
            self.Cardimage[3] = cards[3]
            self.card1.setPixmap(QPixmap(self.Cardimage[0]))
            self.card2.setPixmap(QPixmap(self.Cardimage[1]))
            self.card3.setPixmap(QPixmap(self.Cardimage[2]))
            self.card4.setPixmap(QPixmap(self.Cardimage[3]))
            self.card5.setPixmap(QPixmap(self.Cardimage[4]))
        elif len(cards) == 5:
            self.Cardimage[0] = cards[0]
            self.Cardimage[1] = cards[1]
            self.Cardimage[2] = cards[2]
            self.Cardimage[3] = cards[3]
            self.Cardimage[4] = cards[4]
            self.card1.setPixmap(QPixmap(self.Cardimage[0]))
            self.card2.setPixmap(QPixmap(self.Cardimage[1]))
            self.card3.setPixmap(QPixmap(self.Cardimage[2]))
            self.card4.setPixmap(QPixmap(self.Cardimage[3]))
            self.card5.setPixmap(QPixmap(self.Cardimage[4]))



class PokerTable(QMainWindow):

    def __init__(self, gamestate):

        super().__init__()

        # giving the window a name and background
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.setWindowTitle("Poker - Texas Hold'Em")
        self.centralwidget.setStyleSheet("background-image: url(cards/table.png);")

        # MainWindow
        self.MainWindow = QVBoxLayout(self.centralwidget)


        # Gamestate model
        self.state = gamestate


        # Rendering the cards
        self.cards = [CardView(self.state.players[0].hand.cards), CardView(self.state.players[1].hand.cards)]
        self.tablecards = CardView(self.state.table)

        # Getting the pokertable and info about round
        self.table = TableView()
        self.info = GameInfo()
        """^^^^^^Här ska variabler in från gamestaten med vems tur etc och pengar/pot/current bet"""

        # Displaying table cards
        self.table.table_card_change(self.tablecards.cards)

        # Running the Player Class for player cards and info
        self.players = [PlayerView("Name", self.cards[0].cards, self.state.players[0].money),
                        PlayerView("Name2", self.cards[1].cards, self.state.players[1].money)]

        self.players[0].PlayerCards(["cards/Red_Back_2.svg", "cards/Red_Back_2.svg"])     # Not showing cards at first.
        self.players[1].PlayerCards(["cards/Red_Back_2.svg", "cards/Red_Back_2.svg"])

        # Mapping buttons for each player
        self.players[0].call.clicked.connect(self.call)
        self.players[0].bet.clicked.connect(self.bet)
        self.players[0].checkfold.clicked.connect(self.check_fold)
        self.players[0].showcards.clicked.connect(self.Player1Cards)
        self.players[1].call.clicked.connect(self.call)
        self.players[1].bet.clicked.connect(self.bet)
        self.players[1].checkfold.clicked.connect(self.check_fold)
        self.players[1].showcards.clicked.connect(self.Player2Cards)

        self.tablehbox = QHBoxLayout()
        self.tablehbox.addLayout(self.info.pot_winner)
        self.tablehbox.addLayout(self.table.tablerow)
        self.tablehbox.addLayout(self.info.currentbet_whosturn)

        self.MainWindow.addLayout(self.players[0].playerlayout)
        self.MainWindow.addLayout(self.tablehbox)
        self.MainWindow.addLayout(self.players[1].playerlayout)
        self.setLayout(self.MainWindow)



    def call(self):
        self.state.call()

    def bet(self):
        self.state.bet()

    def check_fold(self):
        #self.state.check_fold()
        pass
    def CardUpdate(self):
        #self.tablecards = CardView(self.state.table)
        #self.table.change_cards(self.tablecards.cards)
        pass
    def NewRound(self):
        pass

    def Player1Cards(self):
        pass

    def Player2Cards(self):
        pass

    def Winner(self):
        pass









