from common.card import Card
import random
import os
from common.player import SimpleFelix

def printCardStr(cards):
    cardStrs = []
    for card in cards:
        cardStrs.append('%s,%s ' % (card.suit, card.num))

    cardStr = ','.join(cardStrs)
    print 'cards = self.__createCards(%s)' % cardStr



nums = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 21, 22]
suits = [1, 2, 3, 4]

allCards = []

for suit in suits:
    for num in nums:
        allCards.append(Card(suit, num))


#printCardStr(cards)

i = 0
while 1:
    i += 1
    os.system('clear')
    print i

    cards = random.sample(allCards, 13)
    print cards

    felix = SimpleFelix()

    try:
        felix.deal(cards)
        print (felix)
        if i == 999:
            raise Exception('fucn')
    except Exception, e:
        print e
        print (felix)

        raw_input('press enter to continue')
