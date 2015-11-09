import unittest
from common.hand import Hand
from common.card import Card

class HandTestCase(unittest.TestCase):
    Hand([Card(1,21), Card(2,21)])

    def test_validate2Card(self):
        # validate ok

        try:
            self.__hand(1,21, 2,21)
            self.__hand(2,22, 3,22)
            self.__hand(1,13, 4,13)
            self.__hand(2,3, 4,3)
        except:
            self.fail('excepted no exception')

        # validate not ok
        with self.assertRaises(Exception):
            self.__hand(1,4, 1,4)

    def test_validate3Card(self):
        # validate ok
        try:
            self.__hand(1,21, 2,21, 3,21)
            self.__hand(2,22, 3,22, 4,22)
            self.__hand(1,13, 3,13, 4,13)
        except:
            self.fail('excepted no exception')

        # validate not ok
        with self.assertRaises(Exception):
            self.__hand(1,4,3,4,1,4)

    def test_validateStraight(self):
        # validate ok
        try:
            self.__hand(1,22, 2,3, 2,4, 3,5, 4,6)
            self.__hand(3,21, 1,22, 2,3, 2,4, 3,5)
            self.__hand(3,10, 1,11, 2,13, 2,12, 3,21)
            self.__hand(3,4, 1,8, 2,5, 2,7, 3,6)
        except:
            self.fail('excepted no exception')

        # validate not ok
        with self.assertRaises(Exception):
            self.__hand(3,10, 1,11, 2,13, 2,12, 3,22)

        with self.assertRaises(Exception):
            self.__hand(3,6, 1,7, 2,8, 2,9, 3,11)

        with self.assertRaises(Exception):
            self.__hand(3,12, 1,4, 2,5, 2,7, 3,10)

    def test_validateFlush(self):
        # validate ok
        try:
            self.__hand(3,10, 3,11, 3,13, 3,12, 3,22)
            self.__hand(4,6, 4,7, 4,8, 4,9, 4,11)
            self.__hand(2,12, 2,4, 2,5, 2,7, 2,10)
        except:
            self.fail('excepted no exception')

        # validate not ok
        with self.assertRaises(Exception):
            self.__hand(3,10, 1,11, 2,13, 2,12, 3,22)

        with self.assertRaises(Exception):
            self.__hand(3,6, 1,7, 2,8, 2,9, 3,11)

        with self.assertRaises(Exception):
            self.__hand(3,12, 1,4, 2,5, 2,7, 3,10)

    def test_win1Card(self):
        self.assertTrue(self.__hand(3,21).win(self.__hand(1,3)))
        self.assertTrue(self.__hand(3,22).win(self.__hand(1,21)))
        self.assertTrue(self.__hand(3,22).win(self.__hand(1,22)))
        self.assertFalse(self.__hand(1,3).win(self.__hand(3,21)))
        self.assertFalse(self.__hand(1,21).win(self.__hand(3,22)))
        self.assertFalse(self.__hand(1,22).win(self.__hand(3,22)))

    def __hand(self, *arg):
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

        return Hand(cards)

