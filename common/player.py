import logging
import sys
import os

from card import Card
from hand import Hand
from collections import defaultdict
from sets import Set

logging.basicConfig( stream=sys.stderr )
logging.getLogger( "common.simpleFelix" ).setLevel( logging.DEBUG )

class Player:
    __log = logging.getLogger( "common.player" )

    def __init__(self):
        self.cards = []

    def deal(self, cards):
        self.holdingCards = cards[:]

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
        self.pairs = []
        self.threeKinds = []
        self.fiveCardHands = []

        self.fourKindsTemp = []

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        result = '\n'
        result += '\nself.highs:\n'
        for hand in self.highs:
            result +=  unicode(hand) + '\n'

        result += '\nself.pairs:\n'
        for hand in self.pairs:
            result +=  unicode(hand) + '\n'

        result += '\nself.threeKinds:\n'
        for hand in self.threeKinds:
            result +=  unicode(hand) + '\n'
            
        result += '\nself.fiveCardHands:\n'
        for hand in self.fiveCardHands:
            result +=  unicode(hand) + '\n'
            
        result += '\ncards:\n'
        result +=  ', '.join(unicode(x) for x in self.cards) + '\n'

        result += '\nholding cards:\n'
        result +=  ', '.join(unicode(x) for x in self.holdingCards) + '\n'

        result += '\ncards Stat:\n'

        suitDict = defaultdict(list)
        numDict = defaultdict(list)

        for card in self.holdingCards:
            suitDict[card.suit].append(card)
            numDict[card.num].append(card)

        result += '\nsuit Stat:\n'
        for suit in range (1,5):
            result += '%s : %s' % (suit , unicode(', '.join(unicode(x) for x in suitDict[suit])))  + '\n'

        result += '\nnum Stat:\n'
        for num in sorted(numDict.keys()):
            result += '%s : %s' % (num, ', '.join(unicode(x) for x in numDict[num])) + '\n'

        return result

    def dumpTestAssert(self):
        lenTemplate = '        self.assertEquals(len(player.%s), %s )\n'
        handsTemplate = '        self.assertTrue(self.__checkCards(player.%s[%s].cards, self.__createCards(%s)))\n'
        result = '\n'

        result += '\n        #self.fiveCardHands:\n'
        result += lenTemplate % ('fiveCardHands', len(self.fiveCardHands))
        for i in range(len(self.fiveCardHands)):
            result += handsTemplate % ('fiveCardHands', i, self.__createCardDump(self.fiveCardHands[i].cards))

        result += '\n        #self.threeKinds:\n'
        result += lenTemplate % ('threeKinds', len(self.threeKinds))
        for i in range(len(self.threeKinds)):
            result += handsTemplate % ('threeKinds', i, self.__createCardDump(self.threeKinds[i].cards))

        result += '\n        #self.pairs:\n'
        result += lenTemplate % ('pairs', len(self.pairs))
        for i in range(len(self.pairs)):
            result += handsTemplate % ('pairs', i, self.__createCardDump(self.pairs[i].cards))

        result += '\n        #self.highs:\n'
        result += lenTemplate % ('highs', len(self.highs))
        for i in range(len(self.highs)):
            result += handsTemplate % ('highs', i, self.__createCardDump(self.highs[i].cards))

        return result

    def __createCardDump(self, cards):
        return ', '.join ((str(card.suit) + ',' + str(card.num)) for card in cards)

    def deal(self, cards):
        Player.deal(self, cards)
        self.cards = cards[:]

        self.highs = []
        self.pairs = []
        self.threeKinds = []
        self.fiveCardHands = []

        self.fourKindsTemp = []

        self.__findRFlush()
        self.__findAllTwo()
        self.__find4Kind()
        self.__findFullHouse()
        self.__findAcePairs()
        self.__findFlush()
        self.__findStright()
        self.__findPairs()
        self.__findHighs()
        self.__findSingleForFourKinds()

        #self.__log.debug(self)
        

    def play(self, playHistory):
        pass

    def allPassPlay(self, playHistory):
        pass

    def firstPlay(self):
        pass

    def __findRFlush(self):
        suitDict = defaultdict(list)

        for card in self.cards:
            suitDict[card.suit].append(card)

        for suit in suitDict.keys():
            if len(suitDict[suit]) >= 5:
                cardsInSuit = suitDict[suit]
                cardsInSuit.sort(key=lambda x: x.num)

                foundHands = []

                foundStrightContinues = self.__findStrightContinues(cardsInSuit)
                for foundContinCards in foundStrightContinues:
                    if foundContinCards[0].num == 21 or foundContinCards[0].num == 22 or foundContinCards[0].num == 10:
                        foundHands.append(Hand(foundContinCards))
                    else:
                        while len(foundContinCards) >= 5:
                            foundHands.append(Hand(foundContinCards[-5:]))
                            self.__removeFromCards(foundContinCards, foundContinCards[-5:])

                for foundHand in foundHands:
                    self.__addToHands(self.fiveCardHands, foundHand)
                    self.__removeFromCards(self.cards, foundHand.cards)


    def __findAllTwo(self):
        for card in self.cards:
            if card.num == 22:
                self.__addToHands(self.highs, Hand([card]))
                self.__removeFromCards(self.cards, [card])

    def __find4Kind(self):
        numDict = defaultdict(list)

        for card in self.cards:
            numDict[card.num].append(card)

        for num in reversed(sorted(numDict.keys())):
            if len(numDict[num]) == 4 and len(self.fourKindsTemp) < 2:
                self.fourKindsTemp.append(numDict[num])
                self.__removeFromCards(self.cards, numDict[num])

    def __findFullHouse(self):
        numDict = defaultdict(list)

        for card in self.cards:
            numDict[card.num].append(card)

        threeKinds = []
        pairs = []

        for num in reversed(sorted(numDict.keys())):
            if len(numDict[num]) >= 3:
                threeKinds.append(numDict[num][0:3])

        for num in sorted(numDict.keys()):
            if len(numDict[num]) == 2:
                if len(pairs) < len(threeKinds):
                    pairs.append(numDict[num])
                else:
                    break

        for i in range(len(threeKinds)):
            threeKind = threeKinds[i]
            if i < len(pairs):
                pair = pairs[i]
                fullHouseHand = Hand(threeKind + pair)
                self.__addToHands(self.fiveCardHands, fullHouseHand)
                self.__removeFromCards(self.cards, fullHouseHand.cards)
            else:
                threeKindHand = Hand(threeKind)
                self.__addToHands(self.threeKinds, threeKindHand)
                self.__removeFromCards(self.cards, threeKindHand.cards)

    def __findAcePairs(self):
        aceCards = []
        for card in self.cards:
            if card.num == 21:
                aceCards.append(card)

        aceCards.sort(key=lambda x: x.suit)
        while len(aceCards) > 1:
            acePair = [aceCards[0], aceCards[-1]]
            self.__addToHands(self.pairs, Hand(acePair))
            self.__removeFromCards(self.cards, acePair)
            self.__removeFromCards(aceCards, acePair)

    def __findFlush(self):
        suitDict = defaultdict(list)

        for card in self.cards:
            suitDict[card.suit].append(card)

        for suit in suitDict.keys():
            if len(suitDict[suit]) >= 5:

                cardsInSuit = suitDict[suit]
                cardsInSuit.sort(key=lambda x: x.num)
                flushHands = []

                if len(cardsInSuit) == 10:
                    self.__addToHands(self.fiveCardHands, Hand(cardsInSuit[0:4] + cardsInSuit[-2:-1]))
                    self.__removeFromCards(self.cards, cardsInSuit[0:4] + cardsInSuit[-2:-1])
                    self.__addToHands(self.fiveCardHands, Hand(cardsInSuit[4:8] + cardsInSuit[-1:]))
                    self.__removeFromCards(self.cards, cardsInSuit[4:8] + cardsInSuit[-1:])
                elif len(cardsInSuit) == 5:
                    self.__addToHands(self.fiveCardHands, Hand(cardsInSuit[0:4] + cardsInSuit[-1:]))
                    self.__removeFromCards(self.cards, cardsInSuit[0:4] + cardsInSuit[-1:])
                else:
                    while len(cardsInSuit) >= 5:
                        numStat = defaultdict(int)
                        for card in self.cards:
                            numStat[card.num] += 1

                        strightCardsList = self.__findStrightContinues(self.__getUniqueNumCards(self.cards))

                        numSet = Set()

                        for strightCards in strightCardsList:
                            for card in strightCards:
                                numSet.add(card.num)

                        okCards = []
                        notPreferCards = []

                        flushCards = cardsInSuit[-1:]
                        cardsInSuit = cardsInSuit[0:-1]

                        for card in cardsInSuit:
                            if numStat[card.num] > 1 or card.num not in numSet:
                                okCards.append(card)
                            else:
                                notPreferCards.append(card)
                                
                        for i in range(4):
                            if okCards:
                                addCard = okCards.pop(0)
                                flushCards.append(addCard)
                                cardsInSuit.remove(addCard)
                            elif notPreferCards:
                                addCard = notPreferCards.pop(0)
                                flushCards.append(addCard)
                                cardsInSuit.remove(addCard)

                        self.__addToHands(self.fiveCardHands, Hand(flushCards))
                        self.__removeFromCards(self.cards, flushCards)

    def __findStright(self):
        strightCardsList = self.__findStrightContinues(self.__getUniqueNumCards(self.cards))

        while strightCardsList:
            for strightCards in strightCardsList:
                if strightCards[0].num == 21 or strightCards[0].num == 22 or strightCards[0].num == 10:
                    self.__addToHands(self.fiveCardHands, Hand(strightCards))
                    self.__removeFromCards(self.cards, strightCards)
                else:
                    while len(strightCards) >= 5:
                        self.__addToHands(self.fiveCardHands, Hand(strightCards[-5:]))
                        self.__removeFromCards(self.cards, strightCards[-5:])
                        self.__removeFromCards(strightCards, strightCards[-5:])

            strightCardsList = self.__findStrightContinues(self.__getUniqueNumCards(self.cards))

    def __findPairs(self):
        numDict = defaultdict(list)

        for card in self.cards:
            numDict[card.num].append(card)

        for num in reversed(numDict.keys()):
            if len(numDict[num]) == 2:
                self.__addToHands(self.pairs, Hand(numDict[num]))
                self.__removeFromCards(self.cards, numDict[num])

    def __findHighs(self):
        for card in self.cards:
            self.__addToHands(self.highs, Hand([card]))
        
        self.cards = []

    def __getUniqueNumCards(self, cards):
        numDict = defaultdict(list)

        for card in self.cards:
            numDict[card.num].append(card)

        uniqueNumCards = []
        for num in sorted(numDict.keys()):
            uniqueNumCards.append(numDict[num][0])

        return uniqueNumCards

    def __findSingleForFourKinds(self):
        numDict = defaultdict(list)

        for card in self.cards:
            numDict[card.num].append(card)

        for fourKind in self.fourKindsTemp:
            singleCard = self.__grapSingleCardFromExistingHands()
            self.__addToHands(self.fiveCardHands, Hand( fourKind + [singleCard]))

    def __grapSingleCardFromExistingHands(self):
        if len(self.highs) > 0:
            singleCardHand = self.highs[0]
            singleCard = singleCardHand.cards[0]
            self.highs.remove(singleCardHand)
            return singleCard

        if len(self.pairs) > 0:
            pairHand = self.pairs[0]
            singleCard = pairHand.cards[0]
            self.__addToHands(self.highs, Hand([pairHand.cards[0]]))
            self.pairs.remove(pairHand)
            return singleCard

        if len(self.threeKinds) > 0:
            threeKindsHand = self.threeKinds[0]
            singleCard = threeKindsHand.cards[0]
            self.__addToHands(self.pairs, Hand(threeKindsHand.cards[1:]))
            self.threeKinds.remove(threeKindsHand)
            return singleCard

        raise Exception('cannot grap single card for 4 kinds')

    def __findStrightContinues(self, cards):
        foundContinueCardsList = []

        if len(cards) >= 5 :
            # 21, 22, 3, 4, 5 or 22, 3, 4, 5, 6 or 10, 11, 12, 13 ,21 
            if cards[-1].num == 22:
                if (cards[0].num== 3 and cards[1].num== 4 and cards[2].num== 5):
                    if cards[-2].num == 21:
                        #21, 22, 3, 4, 5
                        foundContinueCardsList.append([cards[-1], cards[-2], cards[0], cards[1], cards[2]])
                        self.__removeFromCards(cards, foundContinueCardsList[-1])
                    elif cards[3].num == 6:
                        #22, 3, 4, 5, 6
                        foundContinueCardsList.append([cards[-1], cards[0], cards[1], cards[2], cards[3]])
                        self.__removeFromCards(cards, foundContinueCardsList[-1])
                else:
                    if cards[-2].num == 21 and len(cards) >= 6: 
                        if (cards[-6].num == 10 and 
                            cards[-5].num == 11 and 
                            cards[-4].num == 12 and 
                            cards[-3].num == 13 ):
                            #10, 11, 12, 13 ,21
                            foundContinueCardsList.append([cards[-6], cards[-5], cards[-4], cards[-3], cards[-2]])
                            self.__removeFromCards(cards, foundContinueCardsList[-1])
            elif cards[-1].num == 21: 
                if (cards[-5].num == 10 and 
                    cards[-4].num == 11 and 
                    cards[-3].num == 12 and 
                    cards[-2].num == 13 ):
                    #10, 11, 12, 13 ,21
                    foundContinueCardsList.append([cards[-5], cards[-4], cards[-3], cards[-2], cards[-1]])
                    self.__removeFromCards(cards, foundContinueCardsList[-1])

            #other stright
            continues = self.__findContinues(list(card.num for card in cards))
            for contin in continues:
                resultContin = []
                for i in range(contin[0], contin[1]):
                    resultContin.append(cards[i])
                foundContinueCardsList.append(resultContin)

        return foundContinueCardsList        

    def __addToHands(self, hands, hand):
        if hands:
            for i in range(len(hands)):
                if not hand.win(hands[i]):
                    hands.insert(i, hand)
                    return

        hands.append(hand)

    def __removeFromCards(self, cards, removeCards):
        for card in removeCards:
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
    #cards = createCards(2,21, 2,22, 2,3, 2,4, 2,5, 2,6, 2,7, 2,8, 2,9, 2,10, 2,11, 2,12, 2,13)
    cards = createCards(2,21, 1,3, 2,3, 3,3, 4,3, 1,4, 2,4, 3,4, 4,4, 2,6, 2,7, 2,8, 1,8)

    s.deal(cards)
