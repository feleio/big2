import unittest
import logging
import sys
from common.hand import Hand
from common.card import Card
from common.player import SimpleFelix

logger = logging.getLogger("common.player.PlayerTestCase")
logger.level = logging.DEBUG

class PlayerTestCase(unittest.TestCase):
    logger = logging.getLogger("common.player.PlayerTestCase")

    def test_dealRFlushLargest(self):
        player = SimpleFelix()
        cards = self.__createCards(2,21, 2,22, 2,3, 2,4, 2,5, 2,6, 2,7, 2,8, 2,9, 2,10, 2,11, 2,12, 2,13)

        player.deal(cards)

        self.assertEqual(len(player.fiveCardHands), 2)
        self.assertTrue(self.__checkCards(player.fiveCardHands[0].cards, self.__createCards(2,9, 2,10, 2,11, 2,12, 2,13)))
        self.assertTrue(self.__checkCards(player.fiveCardHands[1].cards, self.__createCards(2,21, 2,22, 2,3, 2,4, 2,5)))
        self.assertTrue(self.__checkCards(player.cards, self.__createCards(2,6, 2,7, 2,8)))

    def test_dealRFlushSecondLargest(self):
        player = SimpleFelix()
        cards = self.__createCards(1,5, 3,22, 3,3, 3,4, 3,5, 3,6, 3,7, 3,8, 3,9, 3,10, 3,11, 3,12, 3,13)

        player.deal(cards)

        self.assertEqual(len(player.fiveCardHands), 2)
        self.assertTrue(self.__checkCards(player.fiveCardHands[0].cards, self.__createCards(3,9, 3,10, 3,11, 3,12, 3,13)))
        self.assertTrue(self.__checkCards(player.fiveCardHands[1].cards, self.__createCards(3,22, 3,3, 3,4, 3,5, 3,6)))
        self.assertTrue(self.__checkCards(player.cards, self.__createCards(1,5, 3,7, 3,8)))

    def test_dealRFlushThirdLargest(self):
        player = SimpleFelix()
        cards = self.__createCards(3,21, 4,7, 3,3, 3,4, 3,5, 3,6, 3,7, 3,8, 3,9, 3,10, 3,11, 3,12, 3,13)

        player.deal(cards)

        self.assertEqual(len(player.fiveCardHands), 2)
        self.assertTrue(self.__checkCards(player.fiveCardHands[0].cards, self.__createCards(3,5, 3,6, 3,7, 3,8, 3,9)))
        self.assertTrue(self.__checkCards(player.fiveCardHands[1].cards, self.__createCards(3,21, 3,10, 3,11, 3,12, 3,13)))
        self.assertTrue(self.__checkCards(player.cards, self.__createCards(4,7, 3,3, 3,4)))

    def test_dealRFlushTwoDifferentSuit(self):
        player = SimpleFelix()
        cards = self.__createCards(3,21, 4,7, 3,3, 3,4, 2,5, 2,6, 2,7, 2,8, 2,9, 3,10, 3,11, 3,12, 3,13)

        player.deal(cards)

        self.assertEqual(len(player.fiveCardHands), 2)
        self.assertTrue(self.__checkCards(player.fiveCardHands[0].cards, self.__createCards(2,5, 2,6, 2,7, 2,8, 2,9)))
        self.assertTrue(self.__checkCards(player.fiveCardHands[1].cards, self.__createCards(3,21, 3,10, 3,11, 3,12, 3,13)))
        self.assertTrue(self.__checkCards(player.cards, self.__createCards(4,7, 3,3, 3,4)))

    def test_dealRFlushSingleFlush(self):
        player = SimpleFelix()
        cards = self.__createCards(3,21, 4,7, 3,3, 2,4, 4,5, 2,6, 2,7, 2,8, 2,9, 3,10, 3,11, 3,12, 3,13)

        player.deal(cards)

        self.assertEqual(len(player.fiveCardHands), 1)
        self.assertTrue(self.__checkCards(player.fiveCardHands[0].cards, self.__createCards(3,21, 3,10, 3,11, 3,12, 3,13)))
        self.assertTrue(self.__checkCards(player.cards, self.__createCards(4,7, 3,3, 2,4, 4,5, 2,6, 2,7, 2,8, 2,9,)))

    def __checkCards(self, actualCards, expectedCards):
        if len(actualCards) != len(expectedCards):
            return False
        else:
            #self.logger.debug(actualHand.cards)
            #self.logger.debug(expectedCards)
            for card in expectedCards:
                if not self.__inCards(card, actualCards):
                    return False

        return True

    def __inCards(self, expCard, cards):
        for card in cards:
            if card.suit == expCard.suit and card.num == expCard.num:
                return True

        return False

    def __createCards(self, *arg):
        if len(arg) % 2 != 0:
            raise Exception('number of parameters must be even: %s')

        cards = []
        i = 0
        while i < len(arg):
            suit = arg[i]
            i += 1
            num = arg[i]
            i += 1
            cards.append(Card(suit, num))

        return cards