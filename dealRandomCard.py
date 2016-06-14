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


def dumpCreateCard(i, player):
    template = '        self.players[%s].deal(self.__createCards(%s))\n'
    print template % (i, player.createCardDump(player.holdingCards))

nums = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 21, 22]
suits = [1, 2, 3, 4]

allCards = []

for suit in suits:
    for num in nums:
        allCards.append(Card(suit, num))

players = []
for i in range(4):
    player = SimpleFelix()
    cards = random.sample(allCards, 13)
    player.deal(cards)

    for card in cards:
        allCards.remove(card)
    players.append(player)

for i in range(4):
    dumpCreateCard(i, players[i])

