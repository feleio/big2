# from common.hand import Hand
from common.card import Card

# from collections import defaultdict

# numDict = defaultdict(list)

# cards = [ Card(1,21), Card(1,4), Card(1,5), Card(1,11), Card(1,22)]
# for card in cards:
#     numDict[card.num].append(card)

cards = [Card(1,4) , Card(2,5) , Card(4,3)]
cards2 = cards[:]
print cards
for card in cards:
    print card

print ""
print cards2
for card in cards2:
    print card
print ""
cards2.remove(cards[-1])

print cards
for card in cards:
    print card

print " d"
print cards2
for card in cards2:
    print card