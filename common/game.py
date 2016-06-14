import logging
import sys
import os
import random

from player import SimpleFelix
from card import Card

playerDirection = {0:'^', 1:'>', 2:'v', 3:'<'}

class Game:
    __log = logging.getLogger( "common.game" )

    def start(self, players, lastWinTurn):  

        if len(players) != 4:
            raise Exception('There must be 4 players')

        self.players = players[:]
        self.__dealCards()
        history = []

        #decide which player start first
        isAnyPlayerWin = False
        if lastWinTurn != None:
            turn = lastWinTurn
        else:
            turn = random.randint(0,3)

        print self.players[turn]
        #first play
        hand = self.players[turn].firstPlay()

        roundNum = 1
        print '############## round %s : player %s played : %s %s##############' % (roundNum, turn, playerDirection[turn], hand)
        if hand != None:
            history.append(hand)
        else:
            raise Exception('first player must not pass')

        roundLimit = 100
        #loop play until win
        while((not isAnyPlayerWin) and roundNum < roundLimit ):
            #next player
            turn = ( turn + 1 ) % 4
            roundNum += 1

            player = self.players[turn]
            print player

            #check if all three player passed
            if self.__isAllThreePass(history):
                print '##all three pass'
                hand = player.allPassPlay(history)
            else:
                print '##play'
                hand = player.play(history)

                #check if hand played win previous
                if hand != None:
                    if not self.__isWin(history, hand):
                        raise Exception('played hand cannot win previous hand')
            isWinning = '(Winning)' if player.isWinning else ''
            print '############## round %s : player %s %s played : %s %s##############' % (roundNum, turn, isWinning, playerDirection[turn], hand)

            #print 'round %s : player %s played : %s %s' % (roundNum, turn, playerDirection[turn], hand)

            history.append(hand)

    def __dealCards(self):      
        # nums = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 21, 22]
        # suits = [1, 2, 3, 4]

        # allCards = []

        # for suit in suits:
        #     for num in nums:
        #         allCards.append(Card(suit, num))

        # for i in range(4):
        #     cards = random.sample(allCards, 13)
        #     self.players[i].deal(cards)
        #     for card in cards:
        #         allCards.remove(card)

        self.players[0].deal(self.__createCards(3,10, 1,5, 3,9, 2,9, 2,21, 4,4, 1,9, 2,3, 3,4, 3,7, 2,8, 2,4, 1,6))

        self.players[1].deal(self.__createCards(2,10, 2,5, 4,22, 2,22, 2,12, 3,11, 4,21, 4,8, 1,4, 2,13, 4,7, 1,13, 4,13))

        self.players[2].deal(self.__createCards(3,22, 1,10, 3,6, 4,9, 4,10, 4,12, 3,3, 3,21, 4,11, 4,3, 1,3, 2,11, 2,7))

        self.players[3].deal(self.__createCards(3,12, 1,8, 3,5, 1,21, 1,12, 3,13, 4,6, 1,11, 3,8, 1,7, 1,22, 2,6, 4,5))


    def __isAllThreePass(self, history):
        for hand in history[-3:]:
            if hand != None:
                return False

        return True

    def __isWin(self, history, playedHand):
        for hand in reversed(history[-3:]):
            if hand != None:
                if playedHand.win(hand):
                    return True
                else:
                    break

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

if __name__ == '__main__':
    game = Game()
    players = []
    for i in range(4):
        player = SimpleFelix()
        players.append(player)

    game.start(players, 0)
