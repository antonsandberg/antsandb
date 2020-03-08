import pytest
from CardLib import NumberedCard, Suits, HandRanks
from CardLib import AceCard, KingCard, QueenCard, JackCard
from CardLib import PokerHand, Hand, StandardDeck


def test_cards():
 assert NumberedCard(10, Suits.Diamonds).suit == Suits.Diamonds
 assert NumberedCard(10, Suits.Diamonds).value == 10
 assert JackCard(Suits.Hearts).get_value() == 11
 assert JackCard(Suits.Hearts).suit == Suits.Hearts
 assert AceCard(Suits.Spades).get_value() == 14
 assert AceCard(Suits.Spades).suit == Suits.Spades

def test_deck():
 deck = StandardDeck()
 assert len(deck.cards) == 52

def test_add_new_card():
 deck = StandardDeck()
 hand = Hand()
 hand.addcard(deck.card())
 assert len(hand.cards) == 1
 assert len(deck.cards) == 51

def test_card_discard():
 deck = StandardDeck()
 hand = Hand()
 hand.addcard(deck.card())
 assert len(hand.cards) == 1
 hand.discard([0])
 assert len(hand.cards) == 0

def test_highcard():
 cards = [NumberedCard(9, Suits.Hearts), NumberedCard(9, Suits.Clubs), KingCard(Suits.Spades)]
 highcard = PokerHand.check_highcard(cards)
 assert highcard[0] == 13 and highcard[1] == 2


def test_check_pair():
 cards = [JackCard(Suits.Hearts), JackCard(Suits.Diamonds),
          NumberedCard(10, Suits.Spades)]
 Pair = PokerHand.check_pair(cards)
 assert Pair == 11


def test_check_double_pair():
 cards = [NumberedCard(7, Suits.Clubs), NumberedCard(7, Suits.Diamonds),
          NumberedCard(8, Suits.Hearts), NumberedCard(8, Suits.Clubs), KingCard(Suits.Spades)]
 twopair = PokerHand.check_twopair(cards)
 assert twopair[0] == 8 and twopair[1] == 7


def test_threeofakind():
 cards = [NumberedCard(9, Suits.Hearts), NumberedCard(9, Suits.Clubs), QueenCard(Suits.Spades), QueenCard(Suits.Hearts),
          QueenCard(Suits.Diamonds)]
 threeofakind = PokerHand.check_threeofakind(cards)
 assert threeofakind == 12


def test_fourofakind():
 cards = [NumberedCard(9, Suits.Hearts), NumberedCard(9, Suits.Clubs), QueenCard(Suits.Spades), QueenCard(Suits.Hearts),
          QueenCard(Suits.Diamonds), QueenCard(Suits.Clubs)]
 fourofakind = PokerHand.check_fourofakind(cards)
 assert fourofakind == 12


def test_straight():
 cards = [NumberedCard(9, Suits.Hearts), NumberedCard(10, Suits.Clubs), QueenCard(Suits.Spades), JackCard(Suits.Spades),
          NumberedCard(8, Suits.Hearts), AceCard(Suits.Clubs)]
 straight = PokerHand.check_straight(cards)
 assert straight == 12


def test_flush():
 cards = [NumberedCard(9, Suits.Hearts), NumberedCard(9, Suits.Spades), QueenCard(Suits.Spades), QueenCard(Suits.Hearts),
          AceCard(Suits.Diamonds), NumberedCard(2, Suits.Spades), NumberedCard(4, Suits.Spades), NumberedCard(5, Suits.Spades)]
 flush = PokerHand.check_flush(cards)
 assert flush[0] == 12 and flush[1] == 2  #highest card is Queen in flush and spades == 2

def test_full_house():
 cards = [NumberedCard(9, Suits.Hearts), NumberedCard(9, Suits.Clubs), QueenCard(Suits.Spades), QueenCard(Suits.Hearts),
          QueenCard(Suits.Diamonds), AceCard(Suits.Spades)]
 fullhouse = PokerHand.check_full_house(cards)
 assert fullhouse[0] == 12 and fullhouse[1] == 9   #three of queen and two of nines

def test_straight_flush():
 cards = [NumberedCard(8, Suits.Hearts), NumberedCard(9, Suits.Hearts), QueenCard(Suits.Hearts), NumberedCard(10, Suits.Hearts),
          JackCard(Suits.Hearts), AceCard(Suits.Spades)]
 straightflush = PokerHand.check_straight_flush(cards)
 assert straightflush == 12 #highest card in straightflush is queen of hearts

def test_check_best_pokerhand():
 cards = [NumberedCard(9, Suits.Hearts), NumberedCard(8, Suits.Clubs), QueenCard(Suits.Spades), QueenCard(Suits.Hearts),
          QueenCard(Suits.Diamonds), JackCard(Suits.Hearts), AceCard(Suits.Spades)]
 pokerhand = PokerHand(cards)
 assert pokerhand.ranking == 5 and pokerhand.value == 12 #threeofakind ranking is 5 and queen is value 12




