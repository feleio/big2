import logging
import sys
import os

from collections import defaultdict

FiveCardRank = ['straight', 'flush', 'full', 'fourkind', 'rflush']

logging.basicConfig( stream=sys.stderr )
logging.getLogger( "common.hand" ).setLevel( logging.DEBUG )

# 3,4,5,6,7,8,9,10, J, Q, K, A, 2
# 3,4,5,6,7,8,9,10,11,12,13,21,22

class Hand:
    __log = logging.getLogger( "common.hand" )

    def __init__(self, cards):
        self.cards = []
        self.cardCount = 0
        self.fiveCardRank = 0

        self.properties = []

        # count at position [0] is ignored
        self.suitStat = defaultdict(int)
        self.numStat = defaultdict(int)

        self.cards = cards
        self.cardCount = len(cards)
        self.__calStat(cards)
        self.__validate(cards)

    # cal count of suit and num
    def __validate(self, cards):
        if self.cardCount == 1:
            pass # 1 card no need to validate as it must be correct 
        elif self.cardCount == 2:
            self.__validate2Card(cards)
        elif self.cardCount == 3:
            self.__validate3Card(cards)
        elif self.cardCount == 5:
            self.__validateAndRank5Card(cards)
        else:
            raise Exception('invalid number of card in a hand')

    def __validate2Card(self, cards):
        if not( len(self.numStat) == 1 and len(self.suitStat) == 2 ):
            raise Exception('validate 2 cards failed')

    def __validate3Card(self, cards):
        if not ( len(self.numStat) == 1 and len(self.suitStat) == 3 ):
            raise Exception('validate 3 cards failed')

    def __validateAndRank5Card(self, cards):
        numStatKeys = self.numStat.keys()

        # straight, flush or rflush
        if len(numStatKeys) == 5:
            self.__validateStraightFlush()
        # full or fourkind
        elif len(numStatKeys) == 2:
            self.__validateFull4Kind(numStatKeys)
        else:   
            raise Exception("validate 5 cards failed")

    def __validateStraightFlush(self):
        self.cards.sort(key=lambda x: x.num)

        isConsecutive = self.__isConsecutive()
        isSameSuit = ( len(self.suitStat) == 1 )

        if isConsecutive:
            # royal flush
            if isSameSuit:
                self.fiveCardRank = 5
            # straight
            else:
                self.fiveCardRank = 1
        else:
            # flush
            if isSameSuit:
                self.fiveCardRank = 2
            else:
                raise Exception('validate Straight or Flush failed')

    def __validateFull4Kind(self, numStatKeys):
        group1NumCount = self.numStat[numStatKeys[0]]
        group2NumCount = self.numStat[numStatKeys[1]]

        if ( group1NumCount + group2NumCount ) != 5:
            raise Exception('validate full or 4 kind failed')

        # full house
        if group1NumCount == 2 or group1NumCount == 3:
            self.fiveCardRank = 3
        # four of a kind
        elif group1NumCount == 1 or group1NumCount == 4:
            self.fiveCardRank = 4

    def __isConsecutive(self):
        # cards is sorted by their num
        for i in range(0,4):
            if self.cards[i].num + 1 != self.cards[i+1].num:
                if ( ( i == 2 and self.cards[2].num == 5 and self.cards[3].num == 21 and self.cards[4].num == 22 )
                    or ( i == 3 and self.cards[3].num == 13 and self.cards[4].num == 21 )
                    or ( i == 3 and self.cards[3].num == 6 and self.cards[4].num == 22 ) ):
                    return True
                else:
                    return False
        return True

    def __calStat(self, cards):
        for card in cards:
            self.suitStat[card.suit] += 1;
            self.numStat[card.num] += 1;

    def win(self, hand):
        if self.cardCount == hand.cardCount:
            if self.cardCount == 1:
                return self.__win1Card(hand)
            elif self.cardCount == 2:   
                return self.__win2card(hand)
            elif self.cardCount == 3:
                return self.__win3card(hand)
            elif self.cardCount == 5:
                return self.__win5card(hand)
        else:
            raise Exception('number of card does not match')

    def __win1Card(self, hand):
        if self.cards[0].num == hand.cards[0].num:
            return self.cards[0].suit > hand.cards[0].suit
        else:
            return self.cards[0].num > hand.cards[0].num

    def __win2card(self, hand):
        if self.cards[0].num == hand.cards[0].num:
            selfSuit = self.cards[0].suit if self.cards[0].suit > self.cards[1].suit else self.cards[1].suit
            otherSuit = hand.cards[0].suit if hand.cards[0].suit > hand.cards[1].suit else hand.cards[1].suit

            return selfSuit > otherSuit
        else:
            return self.cards[0].num > hand.cards[0].num

    def __win3card(self, hand):
        return self.cards[0].num > hand.cards[0].num

    def __win5card(self, hand):
        if self.fiveCardRank == hand.fiveCardRank:
            # straight
            if self.fiveCardRank == 1:
                return self.__winStraight(hand)
            # flush
            elif self.fiveCardRank == 2:
                return self.__winFlush(hand)

            # full house
            elif self.fiveCardRank == 3:
                return self.__winFullHouse(hand)

            # four kind
            elif self.fiveCardRank == 4:
                return self.__win4Kind(hand)

            # royal flush
            elif self.fiveCardRank == 5:
                return self.__winRFlush(hand)
        else:
            return self.fiveCardRank > hand.fiveCardRank

    def __winStraight(self, hand):
        return self.__getStraightRank(self.cards) > self.__getStraightRank(hand.cards)

    def __winFlush(self, hand):
        for i in reversed(range(0,5)):
            if self.cards[i].num != hand.cards[i].num:
                return self.cards[i].num > hand.cards[i].num

        return self.cards[i].suit > hand.cards[i].suit

    def __winFullHouse(self, hand):
        return self.__getSameKindNum(self.numStat, 3) > self.__getSameKindNum(hand.numStat, 3)

    def __win4Kind(self, hand):
        return self.__getSameKindNum(self.numStat, 4) > self.__getSameKindNum(hand.numStat, 4)

    def __winRFlush(self, hand):
        selfRank = self.__getStraightRank(self.cards)
        handRank = self.__getStraightRank(hand.cards)

        if selfRank == handRank:
            return self.cards[0].suit > hand.cards[0].suit
        else:
            return selfRank > handRank

    def __getSameKindNum(self, numStat, count):
        for i in numStat.keys():
            if numStat[i] == count:
                return i

    def __getStraightRank(self, cards):
        if cards[3].num == 21 and cards[4].num == 22:
            return 16
        elif cards[3].num == 6 and cards[4].num == 22:
            return 15
        elif cards[3].num == 13 and cards[4].num == 21:
            return 14
        else:
            return cards[4].num



