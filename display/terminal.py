""""
Contains all the terminal drawing logic

Author: phortheman
"""

CELL_SIZE: int = 5
LINE_LENGTH: int = 21

from classes.Board import *
from classes.Lane import *


# Clear the terminal
def clearTerminal():
    print("\033c\033[3J", end='')

# Redraw the board
def refreshTerminal( playerBoard: Board, cpuBoard: Board, playerRoll: int = None, cpuRoll: int = None ):
    clearTerminal()
    print( f"{'Player':^{LINE_LENGTH}}")
    drawBoard( playerBoard )
    print( f"{'CPU':^{LINE_LENGTH}}")
    drawBoard( cpuBoard )
    print( "-"* LINE_LENGTH )
    print( f"CPU rolled: {'' if cpuRoll == None else cpuRoll}" )
    print( f"You rolled: {playerRoll}" )

def drawBoard( board: Board ) -> None:
        output: str = ""
        for i in range(MAX_LANE_SIZE):
            for j in board.LANES:
                cell = j.values[i]
                if cell == 0:
                    cell = ""

                output += f"[{cell:^{CELL_SIZE}}]"
                
            output += "\n"

        output += "-"*LINE_LENGTH
        output += "\n"

        for k in board.LANES:
            output += f"[{k.calculateLane():^{CELL_SIZE}}]"

        output += "\n"
        output += "="*LINE_LENGTH
        output += "\n"
        print( output )

def validateInput( board: Board, playerRoll: int ) -> int:
    print( f"Select a lane to put {playerRoll}: A, B, C" )
    while True:
        userInput = input( "-> " ).upper()
        if userInput in ["1", "2", "3"]:
            evaluatedInput = int(userInput) - 1
        else: 
            match userInput:
                case "A":
                    evaluatedInput = 0
                case "B":
                    evaluatedInput = 1
                case "C":
                    evaluatedInput = 2
                case "Q":
                    return -1
                case _:
                    print( "Please select a valid lane!" )
                    continue
        
        if ( board.LANES[evaluatedInput].canAdd() ):
            return evaluatedInput
        else:
            print( "Lane is already full!" )

def gameOver( playerBoard: Board, cpuBoard: Board ) -> bool:
    playerScore = playerBoard.calculateBoardScore()
    cpuScore = cpuBoard.calculateBoardScore()
    print( f"Player Score: {playerScore}")
    print( f"CPU Score: {cpuScore}")
    if playerScore > cpuScore:
        print( "The player wins!" )
    elif playerScore < cpuScore: 
        print( "The CPU wins!" )
    else:
        print( "Its a draw!" )
    
    print( "Play again? [Y/N]" )

    userInput = input( "-> " ).upper()
    match userInput:
            case "Y":
                return True
            case _:
                return False