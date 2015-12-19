from common.card import Card
import sys

toCharacter = {3:'3', 4:'4', 5:'5', 6:'6', 7:'7', 8:'8', 9:'9', 10:'10',
        11:'J', 12:'Q', 13:'K', 21:'A', 22:'2'}
toSuit = {1:u'\u2666', 2:u'\u2663', 3:u'\u2665', 4:u'\u2660'}

def createCards(*arg):
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

cards = createCards(1,21, 2,22, 4,11, 1,12, 1,13, 2,8, 2,3, 3,10, 4,9, 2,9, 2,11, 2,12, 2,5)

cardMap = {1:{}, 2:{}, 3:{}, 4:{}}   


for card in cards:
    cardMap[card.suit][card.num] = card

for suit in toSuit.keys():
    suitLine = ''
    for num in toCharacter.keys():
        if num in cardMap[suit]:
            suitLine += str(cardMap[suit][num])
        else:
            suitLine += '  '
        suitLine += ','
    print suitLine




