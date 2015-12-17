import logging
import sys
import os

from card import Card
from hand import Hand
from collections import defaultdict

class Player:
    __log = logging.getLogger( "common.player" )

    def __init__(self):
        self.cards = []

    def deal(self, cards):
        self.HodingCards = cards[:]

    def play(self, playHistory):
        pass

    def allPassPlay(self, playHistory):
        pass

    def firstPlay(self):
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
        self.cards = cards[:]

        self.highs = []
        self.Pairs = []
        self.threeKinds = []
        self.fiveCardHands = []

        self.__findRFlush()

    def play(self, playHistory):
        pass

    def allPassPlay(self, playHistory):
        pass

    def firstPlay(self):
        pass

    def __findRFlush(self):
        self.suitDict = defaultdict(list)
        self.numDict = defaultdict(list)

        for card in self.cards:
            self.suitDict[card.suit].append(card)

        for suit in self.suitDict.keys():
            if len(self.suitDict[suit]) >= 5:
                cardsInSuit = self.suitDict[suit]
                cardsInSuit.sort(key=lambda x: x.num)
                foundHands = self.__findStrightHands(cardsInSuit)

                for foundHand in foundHands:
                    self.__addToHands(self.fiveCardHands, foundHand)
                    self.__removeFromCards(self.cards, foundHand)


    def __findStrightHands(self, cards):
        foundHands = []

        if len(cards) >= 5 :
            # 21, 22, 3, 4, 5 or 22, 3, 4, 5, 6 or 10, 11, 12, 13 ,21 
            if cards[-1].num == 22:
                if (cards[0].num== 3 and cards[1].num== 4 and cards[2].num== 5):
                    if cards[-2].num == 21:
                        #21, 22, 3, 4, 5
                        foundHands.append(Hand([cards[-1], cards[-2], cards[0], cards[1], cards[2]]))
                        self.__removeFromCards(cards, foundHands[-1])
                    elif cards[3].num == 6:
                        #22, 3, 4, 5, 6
                        foundHands.append(Hand([cards[-1], cards[0], cards[1], cards[2], cards[3]]))
                        self.__removeFromCards(cards, foundHands[-1])
                else:
                    if cards[-2].num == 21 and len(cards) >= 6: 
                        print cards
                        if (cards[-6].num == 10 and 
                            cards[-5].num == 11 and 
                            cards[-4].num == 12 and 
                            cards[-3].num == 13 ):
                            #10, 11, 12, 13 ,21
                            foundHands.append(Hand([cards[-2], cards[-3], cards[-4], cards[-5], cards[-6]]))
                            self.__removeFromCards(cards, foundHands[-1])
            elif cards[-1].num == 21: 
                if (cards[-5].num == 10 and 
                    cards[-4].num == 11 and 
                    cards[-3].num == 12 and 
                    cards[-2].num == 13 ):
                    #10, 11, 12, 13 ,21
                    foundHands.append(Hand([cards[-1], cards[-2], cards[-3], cards[-4], cards[-5]]))
                    self.__removeFromCards(cards, foundHands[-1])

            #other stright
            while len(cards) >= 5:
                continues = self.__findContinues(list(card.num for card in cards))
                if continues:
                    largestContinues = continues[-1]
                    foundHands.append(Hand(cards[largestContinues[1] - 5 : largestContinues[1]]))
                    self.__removeFromCards(cards, foundHands[-1])
                else:
                    break

        return foundHands

    def __addToHands(self, hands, hand):
        if not hands:
            hands.append(hand)
        else:
            for i in range(len(hands)):
                if not hand.win(hands[i]):
                    hands.insert(i, hand)
                    break

    def __removeFromCards(self, cards, hand):
        for card in hand.cards:
            cards.remove(card)

    def __findContinues(self, nums):
        start = -1
        end = -1

        continues = []

        isContinueNow = False
        for i in range(len(nums)):
            a = nums[i] + 1 
            if not isContinueNow:
                if not ( 
                    i+1 == len(nums) 
                    ) and ( nums[i] + 1 
                    == nums[i+1] ):
                    isContinueNow = True
                    start = i
            else:
                if ( i+1 == len(nums) ) or ( nums[i] + 1 != nums[i+1] ):
                    isContinueNow = False
                    end = i+1
                    if end - start >= 5:
                        continues.append((start, end))
                    start = -1
                    end = -1
        return continues

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
    #cards = createCards(1,22, 3,22, 1,21, 2,21, 4,5, 3,5, 1,6, 1,7, 2,7, 2,11, 3,11, 1,11, 4,13)
    cards = createCards(2,21, 2,22, 2,3, 2,4, 2,5, 2,6, 2,7, 2,8, 2,9, 2,10, 2,11, 2,12, 2,13)

    s.deal(cards)
    for hand in s.fiveCardHands:
        print( hand )
