"""
A simple dice game I'm replicating from the video game "Cult of Lamb"

Players rolls a die and puts the die in one of three lanes
Chained dice in a lane are multiplied by the count of them
If the oponent puts the same number in the same lane it removes your dice
Only 3 dice can be put into a lane

Author: phortheman

"""
import random

from classes.Board import *
from classes.Lane import *

import display.terminal as term

def rollDie() -> int:
    return random.randint( 1, 6 )

def validateAIChoice( board: Board ) -> int:
    bValid: bool = False

    while not bValid:
        lane = random.randint(1,MAX_LANE_SIZE) - 1
        bValid = board.LANES[lane].canAdd()

    return lane


def play() -> None:
    playerBoard = Board()
    cpuBoard = Board()
    cpuRoll = None
    
    while True:
        playerRoll = rollDie()
        term.refreshTerminal(playerBoard=playerBoard, cpuBoard=cpuBoard, playerRoll=playerRoll, cpuRoll=cpuRoll)

        playerInput = term.validateInput( playerBoard, playerRoll )
    
        if playerInput == -1: # Q was inputted
            quit()
        
        playerBoard.LANES[playerInput].addValue(playerRoll)
        cpuBoard.LANES[playerInput].removeValue(playerRoll)

        if playerBoard.isBoardFull():
            term.refreshTerminal(playerBoard=playerBoard, cpuBoard=cpuBoard, playerRoll=playerRoll, cpuRoll=cpuRoll)
            if term.gameOver(playerBoard=playerBoard, cpuBoard=cpuBoard):
                playerBoard.clearBoard()
                cpuBoard.clearBoard()
                cpuRoll = None
                continue
            else:
                quit()

        cpuRoll = rollDie()
        cpuChoice = validateAIChoice( cpuBoard )

        cpuBoard.LANES[cpuChoice].addValue(cpuRoll)
        playerBoard.LANES[cpuChoice].removeValue(cpuRoll)

        if cpuBoard.isBoardFull():
            term.refreshTerminal(playerBoard=playerBoard, cpuBoard=cpuBoard, playerRoll=playerRoll, cpuRoll=cpuRoll)
            if term.gameOver(playerBoard=playerBoard, cpuBoard=cpuBoard):
                playerBoard.clearBoard()
                cpuBoard.clearBoard()
                cpuRoll = None
                continue
            else:
                quit()

if __name__ == "__main__":
    play()
