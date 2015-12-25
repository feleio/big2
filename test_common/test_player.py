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

    # RFlush

    def test_dealRFlushLargest(self):
        player = SimpleFelix()
        cards = self.__createCards(2,21, 2,22, 2,3, 2,4, 2,5, 2,6, 2,7, 2,8, 2,9, 2,10, 2,11, 2,12, 2,13)

        player.deal(cards)

        self.assertEqual(len(player.fiveCardHands), 2)
        self.assertTrue(self.__checkCards(player.fiveCardHands[0].cards, self.__createCards(2,9, 2,10, 2,11, 2,12, 2,13)))
        self.assertTrue(self.__checkCards(player.fiveCardHands[1].cards, self.__createCards(2,21, 2,22, 2,3, 2,4, 2,5)))
        #self.logger.debug(player)
        self.assertTrue(self.__checkCards(player.highs[0].cards, self.__createCards(2,6)))
        self.assertTrue(self.__checkCards(player.highs[1].cards, self.__createCards(2,7)))
        self.assertTrue(self.__checkCards(player.highs[2].cards, self.__createCards(2,8)))

    def test_dealRFlushSecondLargest(self):
        player = SimpleFelix()
        cards = self.__createCards(1,5, 3,22, 3,3, 3,4, 3,5, 3,6, 3,7, 3,8, 3,9, 3,10, 3,11, 3,12, 3,13)

        player.deal(cards)

        self.assertEqual(len(player.fiveCardHands), 2)
        self.assertTrue(self.__checkCards(player.fiveCardHands[0].cards, self.__createCards(3,9, 3,10, 3,11, 3,12, 3,13)))
        self.assertTrue(self.__checkCards(player.fiveCardHands[1].cards, self.__createCards(3,22, 3,3, 3,4, 3,5, 3,6)))
        self.assertTrue(self.__checkCards(player.highs[0].cards, self.__createCards(1,5)))
        self.assertTrue(self.__checkCards(player.highs[1].cards, self.__createCards(3,7)))
        self.assertTrue(self.__checkCards(player.highs[2].cards, self.__createCards(3,8)))

    def test_dealRFlushThirdLargest(self):
        player = SimpleFelix()
        cards = self.__createCards(3,21, 4,7, 3,3, 3,4, 3,5, 3,6, 3,7, 3,8, 3,9, 3,10, 3,11, 3,12, 3,13)

        player.deal(cards)

        self.assertEqual(len(player.fiveCardHands), 2)
        self.assertTrue(self.__checkCards(player.fiveCardHands[0].cards, self.__createCards(3,5, 3,6, 3,7, 3,8, 3,9)))
        self.assertTrue(self.__checkCards(player.fiveCardHands[1].cards, self.__createCards(3,21, 3,10, 3,11, 3,12, 3,13)))
        self.assertTrue(self.__checkCards(player.highs[0].cards, self.__createCards(3,3)))
        self.assertTrue(self.__checkCards(player.highs[1].cards, self.__createCards(3,4)))
        self.assertTrue(self.__checkCards(player.highs[2].cards, self.__createCards(4,7)))

    def test_dealRFlushTwoDifferentSuit(self):
        player = SimpleFelix()
        cards = self.__createCards(3,21, 4,7, 3,3, 3,4, 2,5, 2,6, 2,7, 2,8, 2,9, 3,10, 3,11, 3,12, 3,13)

        player.deal(cards)

        self.assertEqual(len(player.fiveCardHands), 2)
        self.assertTrue(self.__checkCards(player.fiveCardHands[0].cards, self.__createCards(2,5, 2,6, 2,7, 2,8, 2,9)))
        self.assertTrue(self.__checkCards(player.fiveCardHands[1].cards, self.__createCards(3,21, 3,10, 3,11, 3,12, 3,13)))

        self.assertTrue(self.__checkCards(player.highs[0].cards, self.__createCards(3,3)))
        self.assertTrue(self.__checkCards(player.highs[1].cards, self.__createCards(3,4)))
        self.assertTrue(self.__checkCards(player.highs[2].cards, self.__createCards(4,7)))

    def test_dealRFlushSingleFlush(self):
        player = SimpleFelix()
        cards = self.__createCards(3,21, 4,7, 3,3, 1,4, 4,4, 2,6, 2,7, 2,8, 2,9, 3,10, 3,11, 3,12, 3,13)

        player.deal(cards)

        self.assertEqual(len(player.fiveCardHands), 1)
        self.assertTrue(self.__checkCards(player.fiveCardHands[0].cards, self.__createCards(3,21, 3,10, 3,11, 3,12, 3,13)))
        self.assertTrue(self.__checkCards(player.highs[0].cards, self.__createCards(3,3)))
        self.assertTrue(self.__checkCards(player.highs[1].cards, self.__createCards(2,6)))
        self.assertTrue(self.__checkCards(player.highs[2].cards, self.__createCards(2,8)))
        self.assertTrue(self.__checkCards(player.highs[3].cards, self.__createCards(2,9)))
        self.assertTrue(self.__checkCards(player.pairs[0].cards, self.__createCards(1,4, 4,4)))
        self.assertTrue(self.__checkCards(player.pairs[1].cards, self.__createCards(2,7, 4,7)))

    # 4 kinds

    def test_dealRFlushSingleFlush(self):
        player = SimpleFelix()
        cards = self.__createCards(3,21, 4,7, 3,3, 1,4, 4,4, 2,6, 2,7, 2,8, 2,9, 3,10, 3,11, 3,12, 3,13)

        player.deal(cards)

        self.assertEqual(len(player.fiveCardHands), 1)
        self.assertTrue(self.__checkCards(player.fiveCardHands[0].cards, self.__createCards(3,21, 3,10, 3,11, 3,12, 3,13)))
        self.assertTrue(self.__checkCards(player.highs[0].cards, self.__createCards(3,3)))
        self.assertTrue(self.__checkCards(player.highs[1].cards, self.__createCards(2,6)))
        self.assertTrue(self.__checkCards(player.highs[2].cards, self.__createCards(2,8)))
        self.assertTrue(self.__checkCards(player.highs[3].cards, self.__createCards(2,9)))
        self.assertTrue(self.__checkCards(player.pairs[0].cards, self.__createCards(1,4, 4,4)))
        self.assertTrue(self.__checkCards(player.pairs[1].cards, self.__createCards(2,7, 4,7)))

    def test_dealFourKind(self):
        player = SimpleFelix()
        cards = self.__createCards(3,21, 2,4, 3,4, 1,4, 4,4, 2,6, 3,7, 1,8, 2,9, 3,10, 3,11, 3,12, 3,13)

        player.deal(cards)
        
        #self.logger.debug(player.dumpTestAssert())
        #self.logger.debug(player)

        #self.fiveCardHands:
        self.assertEquals(len(player.fiveCardHands), 2 )
        self.assertTrue(self.__checkCards(player.fiveCardHands[0].cards, self.__createCards(2,4, 3,4, 1,4, 4,4, 2,6)))
        self.assertTrue(self.__checkCards(player.fiveCardHands[1].cards, self.__createCards(3,10, 3,11, 3,12, 3,13, 3,21)))

        #self.threeKinds:
        self.assertEquals(len(player.threeKinds), 0 )

        #self.pairs:
        self.assertEquals(len(player.pairs), 0 )

        #self.highs:
        self.assertEquals(len(player.highs), 3 )
        self.assertTrue(self.__checkCards(player.highs[0].cards, self.__createCards(3,7)))
        self.assertTrue(self.__checkCards(player.highs[1].cards, self.__createCards(1,8)))
        self.assertTrue(self.__checkCards(player.highs[2].cards, self.__createCards(2,9)))

    def test_dealFourKindSkipPairs(self):
        player = SimpleFelix()
        cards = self.__createCards(3,21, 2,4, 3,4, 1,4, 4,4, 2,6, 3,6, 1,8, 2,9, 3,10, 3,11, 3,12, 3,13)

        player.deal(cards)
        
        self.logger.debug(player.dumpTestAssert())
        self.logger.debug(player)

        #self.fiveCardHands:
        self.assertEquals(len(player.fiveCardHands), 2 )
        self.assertTrue(self.__checkCards(player.fiveCardHands[0].cards, self.__createCards(2,4, 3,4, 1,4, 4,4, 1,8)))
        self.assertTrue(self.__checkCards(player.fiveCardHands[1].cards, self.__createCards(3,10, 3,11, 3,12, 3,13, 3,21)))

        #self.threeKinds:
        self.assertEquals(len(player.threeKinds), 0 )

        #self.pairs:
        self.assertEquals(len(player.pairs), 1 )
        self.assertTrue(self.__checkCards(player.pairs[0].cards, self.__createCards(2,6, 3,6)))

        #self.highs:
        self.assertEquals(len(player.highs), 1 )
        self.assertTrue(self.__checkCards(player.highs[0].cards, self.__createCards(2,9)))

    def test_dealFourKindSkipPairs(self):
        player = SimpleFelix()
        cards = self.__createCards(3,21, 2,4, 3,4, 1,4, 4,4, 2,6, 3,6, 1,8, 2,9, 3,10, 3,11, 3,12, 3,13)

        player.deal(cards)
        
        #self.logger.debug(player.dumpTestAssert())
        #self.logger.debug(player)

        #self.fiveCardHands:
        self.assertEquals(len(player.fiveCardHands), 2 )
        self.assertTrue(self.__checkCards(player.fiveCardHands[0].cards, self.__createCards(2,4, 3,4, 1,4, 4,4, 1,8)))
        self.assertTrue(self.__checkCards(player.fiveCardHands[1].cards, self.__createCards(3,10, 3,11, 3,12, 3,13, 3,21)))

        #self.threeKinds:
        self.assertEquals(len(player.threeKinds), 0 )

        #self.pairs:
        self.assertEquals(len(player.pairs), 1 )
        self.assertTrue(self.__checkCards(player.pairs[0].cards, self.__createCards(2,6, 3,6)))

        #self.highs:
        self.assertEquals(len(player.highs), 1 )
        self.assertTrue(self.__checkCards(player.highs[0].cards, self.__createCards(2,9)))

    def test_dealFourKindSeparatePairs(self):
        player = SimpleFelix()
        cards = self.__createCards(3,21, 2,4, 3,4, 1,4, 4,4, 2,6, 3,6, 1,9, 2,9, 3,10, 3,11, 3,12, 3,13)

        player.deal(cards)
        
        #self.logger.debug(player.dumpTestAssert())
        #self.logger.debug(player)

        #self.fiveCardHands:
        self.assertEquals(len(player.fiveCardHands), 2 )
        self.assertTrue(self.__checkCards(player.fiveCardHands[0].cards, self.__createCards(2,4, 3,4, 1,4, 4,4, 2,6)))
        self.assertTrue(self.__checkCards(player.fiveCardHands[1].cards, self.__createCards(3,10, 3,11, 3,12, 3,13, 3,21)))

        #self.threeKinds:
        self.assertEquals(len(player.threeKinds), 0 )

        #self.pairs:
        self.assertEquals(len(player.pairs), 1 )
        self.assertTrue(self.__checkCards(player.pairs[0].cards, self.__createCards(1,9, 2,9)))

        #self.highs:
        self.assertEquals(len(player.highs), 1 )
        self.assertTrue(self.__checkCards(player.highs[0].cards, self.__createCards(2,6)))

    def test_dealFourKindx3(self):
        player = SimpleFelix()
        cards = self.__createCards(3,22, 2,4, 3,4, 1,4, 4,4, 1,6, 3,6, 2,6, 4,6, 4,21, 3,21, 2,21, 1,21)

        player.deal(cards)
        
        #self.logger.debug(player.dumpTestAssert())
        #self.logger.debug(player)

        #self.fiveCardHands:
        self.assertEquals(len(player.fiveCardHands), 2 )
        self.assertTrue(self.__checkCards(player.fiveCardHands[0].cards, self.__createCards(1,6, 3,6, 2,6, 4,6, 2,4)))
        self.assertTrue(self.__checkCards(player.fiveCardHands[1].cards, self.__createCards(4,21, 3,21, 2,21, 1,21, 4,4)))

        #self.threeKinds:
        self.assertEquals(len(player.threeKinds), 0 )

        #self.pairs:
        self.assertEquals(len(player.pairs), 1 )
        self.assertTrue(self.__checkCards(player.pairs[0].cards, self.__createCards(3,4, 1,4)))

        #self.highs:
        self.assertEquals(len(player.highs), 0 )

        #self.big2Highs:
        self.assertEquals(len(player.big2Highs), 1 )
        self.assertTrue(self.__checkCards(player.big2Highs[0].cards, self.__createCards(3,22)))



    def test_dealFullHouse(self):
        player = SimpleFelix()
        cards = self.__createCards(3,22, 2,3, 3,3, 1,4, 4,4, 1,7, 3,7, 2,6, 4,6, 4,21, 2,5, 2,21, 1,21)

        player.deal(cards)
        
        #self.logger.debug(player.dumpTestAssert())
        #self.logger.debug(player)

        #self.fiveCardHands:
        self.assertEquals(len(player.fiveCardHands), 1 )
        self.assertTrue(self.__checkCards(player.fiveCardHands[0].cards, self.__createCards(4,21, 2,21, 1,21, 2,3, 3,3)))

        #self.threeKinds:
        self.assertEquals(len(player.threeKinds), 0 )

        #self.pairs:
        self.assertEquals(len(player.pairs), 3 )
        self.assertTrue(self.__checkCards(player.pairs[0].cards, self.__createCards(1,4, 4,4)))
        self.assertTrue(self.__checkCards(player.pairs[1].cards, self.__createCards(2,6, 4,6)))
        self.assertTrue(self.__checkCards(player.pairs[2].cards, self.__createCards(1,7, 3,7)))

        #self.highs:
        self.assertEquals(len(player.highs), 1 )
        self.assertTrue(self.__checkCards(player.highs[0].cards, self.__createCards(2,5)))

        #self.big2Highs:
        self.assertEquals(len(player.big2Highs), 1 )
        self.assertTrue(self.__checkCards(player.big2Highs[0].cards, self.__createCards(3,22)))


    def test_dealTwoFullHouse(self):
        player = SimpleFelix()
        cards = self.__createCards(1,3, 2,3, 3,3, 1,4, 4,4, 1,7, 3,7, 2,6, 4,6, 4,21, 2,5, 2,21, 1,21)

        player.deal(cards)
        
        #self.logger.debug(player.dumpTestAssert())
        #self.logger.debug(player)

        #self.fiveCardHands:
        self.assertEquals(len(player.fiveCardHands), 2 )
        self.assertTrue(self.__checkCards(player.fiveCardHands[0].cards, self.__createCards(1,3, 2,3, 3,3, 2,6, 4,6)))
        self.assertTrue(self.__checkCards(player.fiveCardHands[1].cards, self.__createCards(4,21, 2,21, 1,21, 1,4, 4,4)))

        #self.threeKinds:
        self.assertEquals(len(player.threeKinds), 0 )

        #self.pairs:
        self.assertEquals(len(player.pairs), 1 )
        self.assertTrue(self.__checkCards(player.pairs[0].cards, self.__createCards(1,7, 3,7)))

        #self.highs:
        self.assertEquals(len(player.highs), 1 )
        self.assertTrue(self.__checkCards(player.highs[0].cards, self.__createCards(2,5)))

    def test_dealThreeKindx3(self):
        player = SimpleFelix()
        cards = self.__createCards(1,8, 2,8, 3,8, 1,4, 4,4, 1,7, 3,7, 2,6, 4,6, 4,21, 3,6, 2,21, 1,21)

        player.deal(cards)
        
        #self.logger.debug(player.dumpTestAssert())
        #self.logger.debug(player)

        #self.fiveCardHands:
        self.assertEquals(len(player.fiveCardHands), 2 )
        self.assertTrue(self.__checkCards(player.fiveCardHands[0].cards, self.__createCards(1,8, 2,8, 3,8, 1,7, 3,7)))
        self.assertTrue(self.__checkCards(player.fiveCardHands[1].cards, self.__createCards(4,21, 2,21, 1,21, 1,4, 4,4)))

        #self.threeKinds:
        self.assertEquals(len(player.threeKinds), 1 )
        self.assertTrue(self.__checkCards(player.threeKinds[0].cards, self.__createCards(2,6, 4,6, 3,6)))

        #self.pairs:
        self.assertEquals(len(player.pairs), 0 )

        #self.highs:
        self.assertEquals(len(player.highs), 0 )

    def test_dealFlush(self):
        player = SimpleFelix()
        cards = self.__createCards(4,10 ,3,7 ,1,4 ,4,9 ,4,21 ,1,10 ,2,10 ,4,3 ,3,4 ,3,13 ,4,5 ,3,22 ,4,6 )

        player.deal(cards)
        
        #self.logger.debug(player.dumpTestAssert())
        #self.logger.debug(player)

        #self.fiveCardHands:
        self.assertEquals(len(player.fiveCardHands), 2 )
        self.assertTrue(self.__checkCards(player.fiveCardHands[0].cards, self.__createCards(4,3, 4,5, 4,6, 4,9, 4,21)))
        self.assertTrue(self.__checkCards(player.fiveCardHands[1].cards, self.__createCards(4,10, 1,10, 2,10, 1,4, 3,4)))

        #self.threeKinds:
        self.assertEquals(len(player.threeKinds), 0 )

        #self.pairs:
        self.assertEquals(len(player.pairs), 0 )

        #self.highs:
        self.assertEquals(len(player.highs), 2 )
        self.assertTrue(self.__checkCards(player.highs[0].cards, self.__createCards(3,7)))
        self.assertTrue(self.__checkCards(player.highs[1].cards, self.__createCards(3,13)))

        #self.big2Highs:
        self.assertEquals(len(player.big2Highs), 1 )
        self.assertTrue(self.__checkCards(player.big2Highs[0].cards, self.__createCards(3,22)))
 

    def test_dealTwoFlushDiffSuit(self):
        player = SimpleFelix()
        cards = self.__createCards(3,21 ,4,8 ,3,11 ,3,10 ,4,5 ,1,3 ,4,9 ,2,3 ,4,6 ,2,22 ,3,12 ,4,4 ,3,8)

        player.deal(cards)
        
        #self.logger.debug(player.dumpTestAssert())
        #self.logger.debug(player)

        #self.fiveCardHands:
        self.assertEquals(len(player.fiveCardHands), 2 )
        self.assertTrue(self.__checkCards(player.fiveCardHands[0].cards, self.__createCards(4,4, 4,5, 4,6, 4,8, 4,9)))
        self.assertTrue(self.__checkCards(player.fiveCardHands[1].cards, self.__createCards(3,8, 3,10, 3,11, 3,12, 3,21)))

        #self.threeKinds:
        self.assertEquals(len(player.threeKinds), 0 )

        #self.pairs:
        self.assertEquals(len(player.pairs), 1 )
        self.assertTrue(self.__checkCards(player.pairs[0].cards, self.__createCards(1,3, 2,3)))

        #self.highs:
        self.assertEquals(len(player.highs), 0 )

        #self.big2Highs:
        self.assertEquals(len(player.big2Highs), 1 )
        self.assertTrue(self.__checkCards(player.big2Highs[0].cards, self.__createCards(2,22)))


    def test_dealTwoFlushSameSuit(self):
        player = SimpleFelix()
        cards = self.__createCards(4,21 ,4,8 ,4,11 ,4,10 ,4,5 ,1,3 ,4,9 ,2,3 ,4,6 ,2,22 ,4,13 ,4,4 ,4,8)

        player.deal(cards)
        
        #self.logger.debug(player.dumpTestAssert())
        #self.logger.debug(player)

        #self.fiveCardHands:
        self.assertEquals(len(player.fiveCardHands), 2 )
        self.assertTrue(self.__checkCards(player.fiveCardHands[0].cards, self.__createCards(4,4, 4,5, 4,6, 4,8, 4,13)))
        self.assertTrue(self.__checkCards(player.fiveCardHands[1].cards, self.__createCards(4,8, 4,9, 4,10, 4,11, 4,21)))

        #self.threeKinds:
        self.assertEquals(len(player.threeKinds), 0 )

        #self.pairs:
        self.assertEquals(len(player.pairs), 1 )
        self.assertTrue(self.__checkCards(player.pairs[0].cards, self.__createCards(1,3, 2,3)))

        #self.highs:
        self.assertEquals(len(player.highs), 0 )

        #self.big2Highs:
        self.assertEquals(len(player.big2Highs), 1 )
        self.assertTrue(self.__checkCards(player.big2Highs[0].cards, self.__createCards(2,22)))


    def test_dealFlushSkipForStright(self):
        player = SimpleFelix()
        cards = self.__createCards(4,10 ,3,7 ,1,12 ,4,9 ,4,21 ,1,8 ,2,10 ,4,3 ,3,12 ,2,11 ,4,5 ,3,22 ,4,6)

        player.deal(cards)
        
        #self.logger.debug(player.dumpTestAssert())
        #self.logger.debug(player)

        #self.fiveCardHands:
        self.assertEquals(len(player.fiveCardHands), 2 )
        self.assertTrue(self.__checkCards(player.fiveCardHands[0].cards, self.__createCards(1,8, 4,9, 2,10, 2,11, 1,12)))
        self.assertTrue(self.__checkCards(player.fiveCardHands[1].cards, self.__createCards(4,3, 4,5, 4,6, 4,10, 4,21)))

        #self.threeKinds:
        self.assertEquals(len(player.threeKinds), 0 )

        #self.pairs:
        self.assertEquals(len(player.pairs), 0 )

        #self.highs:
        self.assertEquals(len(player.highs), 2 )
        self.assertTrue(self.__checkCards(player.highs[0].cards, self.__createCards(3,7)))
        self.assertTrue(self.__checkCards(player.highs[1].cards, self.__createCards(3,12)))

        #self.big2Highs:
        self.assertEquals(len(player.big2Highs), 1 )
        self.assertTrue(self.__checkCards(player.big2Highs[0].cards, self.__createCards(3,22)))

    def test_dealStright(self):
        player = SimpleFelix()
        cards = self.__createCards(1,13 ,1,21 ,2,6 ,3,21 ,3,13 ,1,22 ,3,3 ,3,9 ,3,6 ,1,12 ,4,8 ,1,10 ,4,11 )

        player.deal(cards)
        
        #self.logger.debug(player.dumpTestAssert())
        #self.logger.debug(player)

        #self.fiveCardHands:
        self.assertEquals(len(player.fiveCardHands), 1 )
        self.assertTrue(self.__checkCards(player.fiveCardHands[0].cards, self.__createCards(3,9, 1,10, 4,11, 1,12, 1,13)))

        #self.threeKinds:
        self.assertEquals(len(player.threeKinds), 0 )

        #self.pairs:
        self.assertEquals(len(player.pairs), 2 )
        self.assertTrue(self.__checkCards(player.pairs[0].cards, self.__createCards(2,6, 3,6)))
        self.assertTrue(self.__checkCards(player.pairs[1].cards, self.__createCards(1,21, 3,21)))

        #self.highs:
        self.assertEquals(len(player.highs), 3 )
        self.assertTrue(self.__checkCards(player.highs[0].cards, self.__createCards(3,3)))
        self.assertTrue(self.__checkCards(player.highs[1].cards, self.__createCards(4,8)))
        self.assertTrue(self.__checkCards(player.highs[2].cards, self.__createCards(3,13)))

        #self.big2Highs:
        self.assertEquals(len(player.big2Highs), 1 )
        self.assertTrue(self.__checkCards(player.big2Highs[0].cards, self.__createCards(1,22)))


    # Test SimpleFelix.AceBig2Memory
    def test_aceBig2Memory(self):
        cards = self.__createCards(1,22, 3,22, 3,21)
        aceBig2Memory = SimpleFelix.AceBig2Memory(cards)

        self.assertFalse(aceBig2Memory.isMustWin(Hand([Card(3,21)])))
        self.assertFalse(aceBig2Memory.isMustWin(Hand([Card(1,22)])))
        self.assertFalse(aceBig2Memory.isMustWin(Hand([Card(3,22)])))

        aceBig2Memory.remember(Hand([Card(4,22)]))

        self.assertFalse(aceBig2Memory.isMustWin(Hand([Card(3,21)])))
        self.assertFalse(aceBig2Memory.isMustWin(Hand([Card(1,22)])))
        self.assertTrue(aceBig2Memory.isMustWin(Hand([Card(3,22)])))

        aceBig2Memory.remember(Hand([Card(2,22)]))

        self.assertFalse(aceBig2Memory.isMustWin(Hand([Card(3,21)])))
        self.assertTrue(aceBig2Memory.isMustWin(Hand([Card(1,22)])))
        self.assertTrue(aceBig2Memory.isMustWin(Hand([Card(3,22)])))

        aceBig2Memory.remember(Hand([Card(1,21)]))

        self.assertFalse(aceBig2Memory.isMustWin(Hand([Card(3,21)])))
        self.assertTrue(aceBig2Memory.isMustWin(Hand([Card(1,22)])))
        self.assertTrue(aceBig2Memory.isMustWin(Hand([Card(3,22)])))

        aceBig2Memory.remember(Hand([Card(4,21)]))

        self.assertTrue(aceBig2Memory.isMustWin(Hand([Card(3,21)])))
        self.assertTrue(aceBig2Memory.isMustWin(Hand([Card(1,22)])))
        self.assertTrue(aceBig2Memory.isMustWin(Hand([Card(3,22)])))

    def test_aceBig2MemoryWithBiggest2(self):
        cards = self.__createCards(1,22, 3,22, 4,22, 4,21)
        aceBig2Memory = SimpleFelix.AceBig2Memory(cards)

        self.assertFalse(aceBig2Memory.isMustWin(Hand([Card(4,21)])))
        self.assertFalse(aceBig2Memory.isMustWin(Hand([Card(1,22)])))
        self.assertTrue(aceBig2Memory.isMustWin(Hand([Card(3,22)])))
        self.assertTrue(aceBig2Memory.isMustWin(Hand([Card(4,22)])))

        aceBig2Memory.remember(Hand([Card(2,22)]))

        self.assertTrue(aceBig2Memory.isMustWin(Hand([Card(4,21)])))
        self.assertTrue(aceBig2Memory.isMustWin(Hand([Card(1,22)])))
        self.assertTrue(aceBig2Memory.isMustWin(Hand([Card(3,22)])))
        self.assertTrue(aceBig2Memory.isMustWin(Hand([Card(4,22)])))

    def test_aceBig2MemoryWithAllAceBig2(self):
        cards = self.__createCards(1,22, 3,22, 4,22, 2,22, 1,21, 3,21, 4,21, 2,21)
        aceBig2Memory = SimpleFelix.AceBig2Memory(cards)

        self.assertTrue(aceBig2Memory.isMustWin(Hand([Card(1,21)])))
        self.assertTrue(aceBig2Memory.isMustWin(Hand([Card(2,21)])))
        self.assertTrue(aceBig2Memory.isMustWin(Hand([Card(3,21)])))
        self.assertTrue(aceBig2Memory.isMustWin(Hand([Card(4,21)])))
        self.assertTrue(aceBig2Memory.isMustWin(Hand([Card(1,22)])))
        self.assertTrue(aceBig2Memory.isMustWin(Hand([Card(2,22)])))
        self.assertTrue(aceBig2Memory.isMustWin(Hand([Card(3,22)])))
        self.assertTrue(aceBig2Memory.isMustWin(Hand([Card(4,22)])))

    def test_aceBig2MemoryIsAcePairMustWin(self):
        cards = self.__createCards(1,22, 3,22, 3,21, 2,21)
        aceBig2Memory = SimpleFelix.AceBig2Memory(cards)

        self.assertFalse(aceBig2Memory.isMustWin(Hand(self.__createCards(3,21, 2,21))))

        aceBig2Memory.remember(Hand([Card(4,22)]))

        self.assertFalse(aceBig2Memory.isMustWin(Hand(self.__createCards(3,21, 2,21))))

        aceBig2Memory.remember(Hand([Card(4,21)]))

        self.assertTrue(aceBig2Memory.isMustWin(Hand(self.__createCards(3,21, 2,21))))

    def test_aceBig2MemoryIsBig2PairMustWin(self):
        cards = self.__createCards(1,22, 3,22, 3,21, 2,21)
        aceBig2Memory = SimpleFelix.AceBig2Memory(cards)

        self.assertFalse(aceBig2Memory.isMustWin(Hand(self.__createCards(1,22, 3,22))))

        aceBig2Memory.remember(Hand([Card(4,22)]))

        self.assertTrue(aceBig2Memory.isMustWin(Hand(self.__createCards(1,22, 3,22))))

        aceBig2Memory.remember(Hand([Card(4,21)]))

        self.assertTrue(aceBig2Memory.isMustWin(Hand(self.__createCards(1,22, 3,22))))


    def test_aceBig2MemoryIsBiggest2PairMustWin(self):
        cards = self.__createCards(1,22, 4,22, 3,21, 2,21)
        aceBig2Memory = SimpleFelix.AceBig2Memory(cards)

        self.assertTrue(aceBig2Memory.isMustWin(Hand(self.__createCards(1,22, 4,22))))

        aceBig2Memory.remember(Hand([Card(4,22)]))

        self.assertTrue(aceBig2Memory.isMustWin(Hand(self.__createCards(1,22, 4,22))))

        aceBig2Memory.remember(Hand([Card(4,21)]))

        self.assertTrue(aceBig2Memory.isMustWin(Hand(self.__createCards(1,22, 4,22))))

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