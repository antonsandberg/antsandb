import random
from enum import IntEnum
from abc import ABC, abstractmethod

def sorts(objekt):
    """"
    Method for sorting PlayingCards in hand or hand + table ex
    """
    for i in range(len(objekt) - 1):
        j = i
        while j <= (len(objekt) - 2):
            j += 1
            if objekt[j].get_value() > objekt[i].get_value():       #compares card 1-6 against the cards further back in
                tmp = objekt[i]                                     #position and moves the cards further back if they're
                objekt[i] = objekt[j]                               #higher
                objekt[j] = tmp
    return objekt

def createtable(amount):
    """
    Creates a table with 5 random PlayingCards for texas Hold'em
    """
    kort = []
    for i in range(amount):
        kort.append(deck.card())
    return kort

class Suits(IntEnum):
    """
    Converts string suits to value
    """
    Hearts = 3
    Spades = 2
    Diamonds = 1
    Clubs = 0

class HandRanks(IntEnum):
    """
    Converts Handranks to values
    """
    straight_flush = 10
    fourofakind = 9
    full_house = 8
    flush = 7
    straight = 6
    threeofakind = 5
    twopair = 4
    pair = 3
    highcard = 2

suits_symb = ["♣","♦","♠" ,"♥"]                             #Unicode for suits symbols
numbers = range(2, 11)                                      #lista med nummer 2-10

class PlayingCard(ABC):
    """
    Class PlayingCard for creating a Card with inputs value, suit for numbered card and suit for J,Q,K,A
    """
    def __init__(self, suit):
        self.suit = suit

    @abstractmethod
    def get_value(self):
        pass

class NumberedCard(PlayingCard):
    """
    Creates a NumberedCard with a suit and value
    """

    def __init__(self, value, suit):
        self.suit = suit
        self.value = value

    def get_value(self):
        return self.value

    def __str__(self):                  #creating a str for Card to be able to be printed nicely
        s = suits_symb[self.suit]
        return str(self.value) +" "+ s.replace("'","")

class JackCard(PlayingCard):
    """
    Creates a JackCard with suit and value 11
    """
    def get_value(self):
        return 11

    def __str__(self):              #creating a str for Card to be able to be printed nicely
        s = suits_symb[self.suit]
        return "J"+" "+ s.replace("'","")

class QueenCard(PlayingCard):
    """
    Creates a QueenCard with suit and value 12
    """
    def get_value(self):
        return 12

    def __str__(self):              #creating a str for Card to be able to be printed nicely
        s = suits_symb[self.suit]
        return "Q"+" "+ s.replace("'", "")

class KingCard(PlayingCard):
    """
    Creates a KingCard with suit and value 13
    """
    def get_value(self):
        return 13

    def __str__(self):              #creating a str for Card to be able to be printed nicely
        s = suits_symb[self.suit]
        return "K"+" " + s.replace("'", "")

class AceCard(PlayingCard):
    """
    Creates an AceCard with suit and value 14
    """
    def get_value(self):
        return 14

    def __str__(self):          #creating a str for Card to be able to be printed nicely
        s = str(suits_symb[self.suit])
        return "A"+" "+ s.replace("'", "")

class StandardDeck:
    """
    Creates a deck with 52 playingcards from numbers + J,Q,K,A in all 4 suits
    The deck has methods for shuffling itself and taking a card
    """
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for suit in Suits:
            for number in numbers:
                self.cards.append(NumberedCard(number, suit.value))
            for k in [JackCard, QueenCard, KingCard, AceCard]:
                self.cards.append(k(suit.value))

    def __str__(self):                  #Creates a layout thats nicely readable for deck
        return " ".join(['[' + str(card) + ']' for card in self.cards])

    def shuffle(self):                  #deck shuffle
        for i in range(3):
            return random.shuffle(self.cards)

    def card(self):                     #to be able to take the card "on top", takes furthest card in list
        return self.cards.pop()

class Hand:
    """
    Creates a Hand for a Player which can add cards, sort, discard and calculate best poker hand
    with cards on a potential table
    """
    def __init__(self, amount=None, position=None, table=None):
        self.cards = []
        if amount is None:
            self.amount = 0
        if position is None:
            self.index = []
        if table is None:
            self.table = []

    def addcard(self, card):
        self.cards.append(card)

    def __str__(self):                  #layout for printing the Hand
        return " ".join(['[' + str(card) + ']' for card in self.cards])

    def order(self):
        for i in range(len(self.cards)-1):
            j = i
            while j <= (len(self.cards)-2):
                j += 1
                if self.cards[j].get_value() > self.cards[i].get_value():
                    tmp = self.cards[i]
                    self.cards[i] = self.cards[j]
                    self.cards[j] = tmp

        return self.cards

    def discard(self, position):
        self.index = position
        for i in range(len(self.index)):
            self.cards[self.index[i]] = 0

        for i in range(len(self.index)):
            self.cards.remove(0)
        return self.cards

    def best_poker_hand(self, table):           #calculates best possible PokerHand of available cards.
        pokercards = table + self.cards
        return PokerHand(pokercards)


from collections import Counter
class PokerHand:
    """
    PokerHand, can calculate all the available pokerhands with players' cards + table, returns the best
    available pokerhand for those cards with a pokerhand ranking and potential value + suit
    """
    @staticmethod
    def check_straight_flush(cards):
        """
        :param cards: puts in the cards for potential pokerhands
        Goes through the cards and sees if there are 5 numbers in a row with the same suit
        :return: The value of the highest card in the straight flush
        """
        vals = [(c.get_value(), c.suit) for c in cards] + [(1, c.suit) for c in cards if c.get_value == 14]
        for c in reversed(cards):
            found_straight = True
            for k in range(1, 5):
                if (c.get_value() - k, c.suit) not in vals:
                    found_straight = False
                    break
            if found_straight:
                return c.get_value()

    @staticmethod
    def check_full_house(cards):
        """
        :param cards: Puts in the cards for potential pokerhands
        Goes through the cards and looks for three of the same number and thereafter two of the same number
        Sorts the numbers in descending order to get highest pairs and thereafte checks to see if the
        three of a kind is unique to the pair.
        :return: A list with two integers, first place for three of a kind and seconds place with the pair
        """
        value_count = Counter()
        for c in cards:
            value_count[c.get_value()] += 1
        # Find the card ranks that have at least three of a kind
        threes = [v[0] for v in value_count.items() if v[1] >= 3]
        threes.sort()
        # Find the card ranks that have at least a pair
        twos = [v[0] for v in value_count.items() if v[1] >= 2]
        twos.sort()

        # Threes are dominant in full house, lets check that value first:
        for three in reversed(threes):
            for two in reversed(twos):
                if two != three:
                    return three, two

    @staticmethod
    def check_flush(cards):
        """
        :param cards: Puts in the cards for potential pokerhands
        Check among the cards if there are five cards of the same suit and if so sorts them in descending order
        so it can give you the highest value in the flush
        :return: An integer with the highest value in the flush
        """

        suits_count = Counter()
        for c in cards:
            suits_count[c.suit] += 1
        suits = [v[0] for v in suits_count.items() if v[1] >= 5]
        suits.sort(reverse=True)

        flush = []
        if len(suits) > 0:
            flush = suits[0]

        cards = sorts(cards)        #sorts the cards available to be able to return the highest card of the flush

        for c in cards:
            if c.suit == flush:
                return c.get_value(), c.suit

    @staticmethod
    def check_straight(cards):
        """
        :param cards: Puts in the cards for potential pokerhands
        Goes through the cards to see if there are any 5 cards with values in a row
        :return: An integer with the highest value in the straight
        """

        vals = [(c.get_value()) for c in cards] + [1 for c in cards if c.get_value == 14]
        for c in reversed(cards):
            found_straight = True
            for k in range(1, 5):
                if (c.get_value() - k) not in vals:
                    found_straight = False
                    break
            if found_straight:
                return c.get_value()

    @staticmethod
    def check_fourofakind(cards):
        """
        :param cards: Puts in the cards for potential pokerhands
        Counts among the cards to see if there are four of the same of any kind
        :return: An integer with the value of the card there is four of the same of
        """
        count = Counter()
        for c in cards:
            count[c.get_value()] += 1
        fours = [v[0] for v in count.items() if v[1] == 4]
        if len(fours) > 0:
            return fours[0]

    @staticmethod
    def check_threeofakind(cards):
        """
        :param cards: Puts in the cards for potential pokerhands
        Counts through the cards to see if there are any cards with three of the same value
        :return: An integer with the value of the highest available three of a kind
        """
        count = Counter()
        for c in cards:
            count[c.get_value()] += 1
        threes = [v[0] for v in count.items() if v[1] == 3]
        if len(threes) > 0:
            return max(threes)

    @staticmethod
    def check_twopair(cards):
        """
        :param cards: Puts in the cards for potential pokerhands
        Counts among the cards to see if there are any pair of cards
        Stores the pairs and thereafter takes of the two highest pairs if there are two pairs in the list
        :return: A list with two integers, first place is highest pair
        """
        count = Counter()
        for c in cards:
            count[c.get_value()] += 1
        twopair = [v[0] for v in count.items() if v[1] == 2]
        if len(twopair) > 0:
            if (len(twopair) >=2):          #takes out the highest two pairs of all the available
                max1 = max(twopair)
                twopair.remove(max1)
                max2 = max(twopair)
                twopair.clear()
                twopair = [max1, max2]
                return twopair              #returns highest two pairs

    @staticmethod
    def check_pair(cards):
        """
        :param cards: Puts in the cards for potential pokerhands
        Counts among the cards to see if there are any pair of cards, stores all pairs
        :return: Returns the highest pair
        """
        count = Counter()
        for c in cards:
            count[c.get_value()] += 1
        twos = [v[0] for v in count.items() if v[1] == 2]
        if len(twos) > 0:
            return max(twos)                #returns highest pair

    @staticmethod
    def check_highcard(cards):
        """
        :param cards: Puts in the cards for potential pokerhands
        Takes the value and suit of each card that is available and sorts them in descending order
        :return: A list with two integers, first comes the value and second is the suits value
        """
        vals = [(c.get_value(), c.suit) for c in cards]
        vals.sort(reverse=True)
        return vals[0]

    def __init__(self, pokercards):
        pokercards = pokercards
        self.ranking = []

        if PokerHand.check_straight_flush(pokercards) is not None:
            value = PokerHand.check_straight_flush(pokercards)
            self.ranking = HandRanks.straight_flush.value
            self.value = value

        elif PokerHand.check_fourofakind(pokercards) is not None:
            value = PokerHand.check_fourofakind(pokercards)
            self.ranking = HandRanks.fourofakind.value
            self.value = value

        elif PokerHand.check_full_house(pokercards) is not None:
            value = PokerHand.check_full_house(pokercards)
            self.ranking = HandRanks.full_house.value
            self.value = value

        elif PokerHand.check_flush(pokercards) is not None:
            value, suit = PokerHand.check_flush(pokercards)
            self.ranking = HandRanks.flush.value
            self.value = value
            self.suit = suit

        elif PokerHand.check_straight(pokercards) is not None:
            value = PokerHand.check_straight(pokercards)
            self.ranking = HandRanks.straight.value
            self.value = value

        elif PokerHand.check_threeofakind(pokercards) is not None:
            value = PokerHand.check_threeofakind(pokercards)
            self.ranking = HandRanks.threeofakind.value
            self.value = value

        elif PokerHand.check_twopair(pokercards) is not None:
            value = PokerHand.check_twopair(pokercards)
            self.ranking = HandRanks.twopair.value
            self.value = value

        elif PokerHand.check_pair(pokercards) is not None:
            value = PokerHand.check_pair(pokercards)
            self.ranking = HandRanks.pair.value
            self.value = value

        else:
            value, suit = PokerHand.check_highcard(pokercards)
            self.ranking = HandRanks.highcard.value
            self.value = value
            self.suit = suit




deck = StandardDeck()
deck.shuffle()

table = createtable(5)
print(" ".join(['[' + str(card) + ']' for card in table]))

print("--------")
hand = Hand()
for i in range(2):
    hand.addcard(deck.card())
print(hand)

x = hand.best_poker_hand(table)

print("--------")
print(x.ranking)
print(x.value)

