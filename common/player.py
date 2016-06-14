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

    def largestPlay(self):
        pass

class SimpleFelix(Player):
    __log = logging.getLogger( "common.simpleFelix" )
    def __init__(self):
        Player.__init__(self)
        self.highs = []
        self.big2Highs = []
        self.pairs = []
        self.threeKinds = []
        self.fiveCardHands = []

        self.fourKindsTemp = []

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        result = '\n'
        if self.isWinning:
            result += 'winning mode\n'

        if self.highs:
            result += 'self.highs:\n'
            for hand in self.highs:
                result +=  unicode(hand) + '\n'

        if self.big2Highs:
            result += 'self.big2Highs:\n'
            for hand in self.big2Highs:
                result +=  unicode(hand) + '\n'

        if self.pairs:
            result += 'self.pairs:\n'
            for hand in self.pairs:
                result +=  unicode(hand) + '\n'

        if self.threeKinds:
            result += 'self.threeKinds:\n'
            for hand in self.threeKinds:
                result +=  unicode(hand) + '\n'
            
        if self.fiveCardHands:
            result += 'self.fiveCardHands:\n'
            for hand in self.fiveCardHands:
                result +=  unicode(hand) + '\n'


        if self.confidentHighs:
            result += 'self.confidentHighs:\n'
            for hand in self.confidentHighs:
                result +=  unicode(hand) + '\n'            
        if self.confidentPairs:
            result += 'self.confidentPairs:\n'
            for hand in self.confidentPairs:
                result +=  unicode(hand) + '\n'            
        if self.confidentThreeKinds:
            result += 'self.confidentThreeKinds:\n'
            for hand in self.confidentThreeKinds:
                result +=  unicode(hand) + '\n'            
        if self.confidentFiveCardHands:
            result += 'self.confidentFiveCardHands:\n'
            for hand in self.confidentFiveCardHands:
                result +=  unicode(hand) + '\n'

        # result += '\ncards:\n'
        # result +=  ', '.join(unicode(x) for x in self.cards) + '\n'

        result += '\nholding cards:\n'
        result +=  ', '.join(unicode(x) for x in self.holdingCards) + '\n'



        # result += '\ncards Stat:\n'

        # suitDict = defaultdict(list)
        # numDict = defaultdict(list)

        # for card in self.holdingCards:
        #     suitDict[card.suit].append(card)
        #     numDict[card.num].append(card)

        # result += '\nsuit Stat:\n'
        # for suit in range (1,5):
        #     result += '%s : %s' % (suit , unicode(', '.join(unicode(x) for x in suitDict[suit])))  + '\n'

        # result += '\nnum Stat:\n'
        # for num in sorted(numDict.keys()):
        #     result += '%s : %s' % (num, ', '.join(unicode(x) for x in numDict[num])) + '\n'

        return result

    class AceBig2Memory:
        __log = logging.getLogger( "common.simpleFelix" )
        def __init__(self, haveCards):
            self.cardDict = defaultdict(dict)
            self.mustWinDict = defaultdict(dict)

            for num in range(21,23):
                for suit in range(1, 5):
                    self.cardDict[num][suit] = False

            for card in haveCards:
                if card.num == 21 or card.num == 22:
                    self.cardDict[card.num][card.suit] = True
                    self.mustWinDict[card.num][card.suit] = False

            self.__reCalHighsMustWin()

        def __reCalHighsMustWin(self):
            for num in range(21,23):
                for suit in self.mustWinDict[num].keys():
                    if not self.mustWinDict[num][suit] and self.__isAllWinCardAppeared(num, suit):
                        self.mustWinDict[num][suit] = True

        def __isAllWinCardAppeared(self, checkNum, checkSuit):
            if checkNum == 21:
                for suit in range(checkSuit+1,5):
                    if not self.cardDict[21][suit]:
                        return False

                for suit in range(1,5):
                    if not self.cardDict[22][suit]:
                        return False

            elif checkNum == 22:
                for suit in range(checkSuit+1,5):
                    if not self.cardDict[22][suit]:
                        return False
            else:
                raise Exception('num must be 21 or 22')

            return True

        def remember(self, hand):
            for card in hand.cards:
                if card.num == 21 or card.num == 22:
                    self.cardDict[card.num][card.suit] = True
            self.__reCalHighsMustWin()

        def isMustWin(self, hand):
            if hand.cardCount == 1:
                return self.mustWinDict[hand.cards[0].num][hand.cards[0].suit]
            elif hand.cardCount == 2:
                return self.__isPairMustWin(hand)
            else:
                raise Exception('check must win must be high or pair')

        def __isPairMustWin(self, hand, ):
            aceNotAppearCount = self.__notAppearCount(21)
            big2NotAppearCount = self.__notAppearCount(22)

            if hand.cards[0].num == 21:
                return (self.__isLargerPair(hand) or aceNotAppearCount < 2 ) and big2NotAppearCount < 2
            elif hand.cards[0].num == 22:
                return self.__isLargerPair(hand) or big2NotAppearCount < 2
            else:
                raise Exception('check must win must be ace or big2')

        def __is3KindMustWin(self, hand):
            aceNotAppearCount = self.__notAppearCount(21)
            big2NotAppearCount = self.__notAppearCount(22)

            if hand.cards[0].num == 21:
                return big2NotAppearCount < 3
            elif hand.cards[0].num == 22:
                return true
            else:
                raise Exception('check must win must be ace or big2')

        def __notAppearCount(self, checkNum):
            count = 0
            for suit in range(1,5):
                if self.cardDict[checkNum][suit] == False:
                    count += 1
            return count

        def __isLargerPair(self, hand):
            for card in hand.cards:
                if card.suit == 4:  
                    return True
            return False

    def dumpTestAssert(self):
        lenTemplate = '        self.assertEquals(len(player.%s), %s )\n'
        handsTemplate = '        self.assertTrue(self.__checkCards(player.%s[%s].cards, self.__createCards(%s)))\n'
        result = '\n'

        result += '\n        #self.fiveCardHands:\n'
        result += lenTemplate % ('fiveCardHands', len(self.fiveCardHands))
        for i in range(len(self.fiveCardHands)):
            result += handsTemplate % ('fiveCardHands', i, self.createCardDump(self.fiveCardHands[i].cards))

        result += '\n        #self.threeKinds:\n'
        result += lenTemplate % ('threeKinds', len(self.threeKinds))
        for i in range(len(self.threeKinds)):
            result += handsTemplate % ('threeKinds', i, self.createCardDump(self.threeKinds[i].cards))

        result += '\n        #self.pairs:\n'
        result += lenTemplate % ('pairs', len(self.pairs))
        for i in range(len(self.pairs)):
            result += handsTemplate % ('pairs', i, self.createCardDump(self.pairs[i].cards))

        result += '\n        #self.highs:\n'
        result += lenTemplate % ('highs', len(self.highs))
        for i in range(len(self.highs)):
            result += handsTemplate % ('highs', i, self.createCardDump(self.highs[i].cards))

        result += '\n        #self.big2Highs:\n'
        result += lenTemplate % ('big2Highs', len(self.big2Highs))
        for i in range(len(self.big2Highs)):
            result += handsTemplate % ('big2Highs', i, self.createCardDump(self.big2Highs[i].cards))

        return result

    def createCardDump(self, cards):
        return ', '.join ((str(card.suit) + ',' + str(card.num)) for card in cards)

    def deal(self, cards):
        Player.deal(self, cards)
        self.cards = cards[:]

        self.highs = []
        self.big2Highs = []
        self.pairs = []
        self.threeKinds = []
        self.fiveCardHands = []

        self.confidentHighs = []
        self.confidentPairs = []
        self.confidentThreeKinds = []
        self.confidentFiveCardHands = []

        self.fourKindsTemp = []

        self.isWinning = False
        self.isPanic = False

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

        self.aceBig2Memory = self.AceBig2Memory(hand.cards[0] for hand in self.big2Highs)

        #self.__log.debug(self)
        
    def play(self, playHistory):
        previousHands = playHistory[-3:]

        for previousHand in reversed(previousHands):
            if previousHand:
                lasthand = previousHand
                break

        self.__cal(previousHands)

        if lasthand.cardCount == 1:
            handToPlay = self.__getJustWinHand(lasthand, self.highs, [])
            if not handToPlay:
                handToPlay = self.__getJustWinBig2(lasthand)
        elif lasthand.cardCount == 2:
            handToPlay = self.__getJustWinHand(lasthand, self.pairs, self.confidentPairs)
        elif lasthand.cardCount == 3:
            handToPlay = self.__getJustWinHand(lasthand, self.threeKinds, self.confidentThreeKinds)
        elif lasthand.cardCount == 5:
            handToPlay = self.__getJustWinHand(lasthand, self.fiveCardHands, self.confidentFiveCardHands)
        else:
            raise Exception('invalid hand')

        self.__removeFromHolding(handToPlay)
        return handToPlay

    def allPassPlay(self, playHistory):
        previousHands = playHistory[-3:]
        self.__cal(previousHands)

        handToPlay = None
        if self.isWinning:
            if self.fiveCardHands:
                handToPlay = self.__getConfidentHand(self.fiveCardHands, self.confidentFiveCardHands)
            elif self.threeKinds:
                handToPlay = self.__getConfidentHand(self.threeKinds, self.confidentThreeKinds)
            elif self.pairs:
                handToPlay = self.__getConfidentHand(self.pairs, self.confidentPairs)
            elif self.big2Highs:
                handToPlay = self.__getConfidentHand(self.big2Highs, self.confidentHighs)
        else:
            if self.fiveCardHands and self.fiveCardHands[0].fiveCardRank == 1:
                handToPlay = self.fiveCardHands[0]
            if not handToPlay and self.highs:
                handToPlay = self.__getNonConfidentHand(self.highs, [])
            if not handToPlay and self.pairs:
                handToPlay = self.__getNonConfidentHand(self.pairs, self.confidentPairs)
            if not handToPlay and self.threeKinds:
                handToPlay = self.__getNonConfidentHand(self.threeKinds, self.confidentThreeKinds)
            if not handToPlay and self.fiveCardHands:
                handToPlay = self.__getNonConfidentHand(self.fiveCardHands, self.confidentFiveCardHands)
            if not handToPlay and self.big2Highs:
                handToPlay = self.__getNonConfidentHand(self.big2Highs, self.confidentHighs)
            if not handToPlay:
                raise Exception('all pass play must play a card')

        self.__removeFromHolding(handToPlay)
        return handToPlay

    def firstPlay(self):
        handToPlay = None
        if self.fiveCardHands and self.fiveCardHands[0].fiveCardRank == 1:
            handToPlay = self.fiveCardHands[0]
        if not handToPlay and self.highs:
            handToPlay = self.__getNonConfidentHand(self.highs, [])
        if not handToPlay and self.pairs:
            handToPlay = self.__getNonConfidentHand(self.pairs, self.confidentPairs)
        if not handToPlay and self.threeKinds:
            handToPlay = self.__getNonConfidentHand(self.threeKinds, self.confidentThreeKinds)
        if not handToPlay and self.fiveCardHands:
            handToPlay = self.__getNonConfidentHand(self.fiveCardHands, self.confidentFiveCardHands)
        if not handToPlay:
                raise Exception('first play must play a card')

        self.__removeFromHolding(handToPlay)
        return handToPlay

    def largestPlay(self):
        pass

    def __removeFromHolding(self, hand):
        if hand != None:
            try:
                for card in hand.cards:
                    self.holdingCards.remove(card)
            except ValueError:
                pass

    def __cal(self, previousHands):
        for hand in previousHands:
            if hand:
                self.aceBig2Memory.remember(hand)

        self.__markConfident()

        #isWinning
        holdingCount = len(self.highs)+len(self.big2Highs)+len(self.pairs)+len(self.threeKinds)+len(self.fiveCardHands)
        confidentCount = len(self.confidentHighs)+len(self.confidentPairs)+len(self.confidentThreeKinds)+len(self.confidentFiveCardHands)

        if holdingCount - confidentCount <= 1:
            self.isWinning = True

    def __markConfident(self):
        for hand in reversed(self.big2Highs):
            if hand not in self.confidentHighs and self.aceBig2Memory.isMustWin(hand):
                self.confidentHighs.append(hand)
            else:
                break

        for hand in reversed(self.pairs):
            if hand.cards[0].num == 21 and hand not in self.confidentHighs and self.aceBig2Memory.isPairMustWin(hand):
                self.confidentPairs.append(hand)
            else:
                break

        for hand in reversed(self.threeKinds):
            if hand not in self.confidentThreeKinds and hand.cards[0].num >= 12:
                self.confidentThreeKinds.append(hand)
            else:
                break

        for hand in reversed(self.fiveCardHands):
            if ( hand not in self.confidentFiveCardHands and 
                ((hand.fiveCardRank == 3 and hand.getFullHouseNum() >= 11) or hand.fiveCardRank > 4 )):
                self.confidentFiveCardHands.append(hand)
            else:
                break

    def __getJustWinHand(self, lastHand, holdingHands, confidentHands):
        if self.isWinning:
            hands = confidentHands
        else:
            hands = holdingHands

        playHand = None
        for hand in hands:
            if lastHand == None or hand.win(lastHand):
                playHand = hand
                break

        if playHand:
            try:
                confidentHands.remove(playHand)
            except ValueError:
                pass
            
            holdingHands.remove(playHand)

        return playHand

    def __getJustWinBig2(self, lastHand):
        if self.isWinning:
            hands = self.confidentHighs
        else:
            hands = self.big2Highs[:-1]

        playHand = None
        for hand in hands:
            if lastHand == None or hand.win(lastHand):
                playHand = hand
                break

        if playHand:
            try:
                self.confidentHighs.remove(playHand)
            except ValueError:
                pass
            self.big2Highs.remove(playHand)

        return playHand

    def __getConfidentHand(self, holdingHands, confidentHands):
        playHand = None
        if confidentHands:
            playHand = confidentHands[0]

            confidentHands.remove(playHand)
            holdingHands.remove(playHand)

        return playHand

    def __getNonConfidentHand(self, holdingHands, confidentHands):
        playHand = None
        if holdingHands and holdingHands[0] not in confidentHands:
            playHand = holdingHands[0]

            holdingHands.remove(playHand)

        return playHand

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
        cardToAdd = []
        for card in self.cards:
            if card.num == 22:
                cardToAdd.append(card)

        for card in cardToAdd:
            self.__addToHands(self.big2Highs, Hand([card]))
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
