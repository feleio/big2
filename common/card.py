class Card:
    suit = ""
    num = 0
    def __init__(self, suit, num):
        if not ( ( num >= 3 and num <= 13 ) or num == 21 or num == 22 ):
            raise ValueError, 'invalid number'

        if suit < 1 or suit > 4:
            raise ValueError, 'invalid suit'
        self.suit = suit
        self.num = num

    def toString(self):
        return  "%s %s" % ( self.suit, self.num )


