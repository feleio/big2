import logging
import sys
import os

from card import Card

class Player:
    __log = logging.getLogger( "common.player" )

    def __init__(self):
        self.cards = []

    def deal(self, cards):
        self.cards = cards
        self.cards.sort(key=lambda x: x.num)

    def play(self, LastHand):
        pass

    def allPassPlay(self):
        pass

class SimpleFelix(Player):
    __log = logging.getLogger( "common.simpleFelix" )
    def __init__(self):
        Player.__init__(self)
        self.highs = []
        self.Pairs = []
        self.threeKinds = []
        self.fiveHands = []

    def deal(self, cards):
        Player.deal(self, cards)
        self.cards

    def play(self, LastHand):
        

    def allPassPlay(self):
        pass

    def firstPlay(self):
        pass


def createCards(*arg):
    if len(arg) % 2 != 0:
        raise Exception('number of parameters must be even')

    cards = []
    i = 0
    while i < len(arg):
        suit = arg[i]
        i += 1
        num = arg[i]
        i += 1
        cards.append(Card(suit, num))

    return cards

if __name__ == '__main__':
    s = SimpleFelix()
    cards = createCards(1,22, 3,22, 1,21, 2,21, 4,5, 3,5, 1,6, 1,7, 2,7, 2,11, 3,11, 1,11, 4,13)
    s.deal(cards)
    print len(s.cards)
