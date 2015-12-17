class Card:
    toCharacter = {3:'3', 4:'4', 5:'5', 6:'6', 7:'7', 8:'8', 9:'9', 10:'10',
        11:'J', 12:'Q', 13:'K', 21:'A', 22:'2'}

    toSuit = {1:u'\u2666', 2:u'\u2663', 3:u'\u2665', 4:u'\u2660'}

    def __init__(self, suit, num):
        self.suit = ""
        self.num = 0

        if not ( ( num >= 3 and num <= 13 ) or num == 21 or num == 22 ):
            raise ValueError, 'invalid number'

        if suit < 1 or suit > 4:
            raise ValueError, 'invalid suit'
        self.suit = suit
        self.num = num
    
    def __repr__(self):
        return str(self)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return ( '%s%s' % ( Card.toSuit[self.suit], Card.toCharacter[self.num]) )


