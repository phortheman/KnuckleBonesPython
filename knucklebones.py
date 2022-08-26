"""
A simple dice game I'm replicating from the video game "Cult of Lamb"

Players rolls a die and puts the die in one of three lanes
Chained dice in a lane are multiplied by the count of them
If the oponent puts the same number in the same lane it removes your dice
Only 3 dice can be put into a lane

Author: phortheman

"""
import random

CELL_SIZE: int = 5
LINE_LENGTH: int = 21

# Function to clear the terminal
def refresh():
    print("\033c\033[3J", end='')

# Function that mimics rolling a die
def rollDie() -> int:
    return random.randint( 1, 6 )


# This class stores up to 3 ints in a list and contains several methods that modify the list
class Lane:
    MAX_SIZE: int = 3
    def __init__( self ) -> None:
        self.values = []

    def __str__( self ) -> str:
        return f"{self.values}"

    # Sum all the dice together. If there are duplicates (chained dice) then those are 
    # separately added then multiplied by the count of those dice in the lane.
    # Example: 1, 4, 4 = 17 because 1 + ( ( 4+4 ) * 2 )
    #      or: 6, 6 = 24 because 0 + ( ( 6+6 ) * 2 )
    #      or: 1, 2, 3 = 6 because 1 + 2 + 3 ( ( 0 ) * 1 )
    def calculateLane( self ) -> int:
        sum = 0
        count = 0
        chainValue = 0 # This is the value that has a chain
        for i in self.values:
            count = self.values.count(i)
            if count == Lane.MAX_SIZE:
                return i * Lane.MAX_SIZE * Lane.MAX_SIZE
            elif chainValue == 0 and count > 1:
                chainValue = i
            elif i != chainValue:
                sum += i

        return sum + ( chainValue * count * count )

    # Remove the specified value from the lane
    # Puts i into a shallow copy of the list if the value doesn't match i
    def removeValue( self, value ) -> None:
        self.values[:] = [i for i in self.values if i != value]

    def addValue( self, value ) -> bool: 
        if self.canAdd(): # The Lane is full
            self.values.append( value )
            return True
        
        return False

    def canAdd( self ) -> bool:
        if len( self.values ) < Lane.MAX_SIZE:
            return True
        return False

class Board:
    laneA: Lane
    laneB: Lane
    laneC: Lane

    def __init__( self ) -> None:
        self.laneA = Lane()
        self.laneB = Lane()
        self.laneC = Lane()

    def drawBoard( self ) -> str:
        lanes = [self.laneA, self.laneB, self.laneC]
        output: str = ""
        for i in range(Lane.MAX_SIZE):
            for j in lanes:
                try:
                    output += f"[{j.values[i]:^{CELL_SIZE}}]"
                except IndexError:
                    output += f"[{'':^{CELL_SIZE}}]"
            output += "\n"

        output += "-"*LINE_LENGTH
        output += "\n"

        for k in lanes:
            output += f"[{k.calculateLane():^{CELL_SIZE}}]"

        output += "\n"
        output += "="*LINE_LENGTH
        output += "\n"
        print( output )

    def isBoardFull( self ) -> bool:

        if len(self.laneA.values) == Lane.MAX_SIZE and len(self.laneB.values) == Lane.MAX_SIZE and len(self.laneC.values) == Lane.MAX_SIZE:
            return True
        else:
            return False

    def calculateBoardScore( self ) -> int:
        score: int = 0

        score += self.laneA.calculateLane()
        score += self.laneB.calculateLane()
        score += self.laneC.calculateLane()
        return score

def refreshScreen( playerBoard: Board, cpuBoard: Board ):
    refresh()
    print( f"{'Player':^{LINE_LENGTH}}")
    playerBoard.drawBoard()
    print( f"{'CPU':^{LINE_LENGTH}}")
    cpuBoard.drawBoard()

def gameOver( playerBoard: Board, cpuBoard: Board ):
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

    quit()

def validateInput( board: Board ) -> str:
    bValid: bool = False
    while not bValid:
        userInput = input( "-> " ).upper()
        if userInput == "A" and board.laneA.canAdd():
            bValid = True
        elif userInput == "B" and board.laneB.canAdd():
            bValid = True
        elif userInput == "C" and board.laneC.canAdd():
            bValid = True
        elif userInput == "Q":
            bValid = True
        else: 
            print( "Please select a valid lane!" )
    return userInput

def validateAIChoice( board: Board ) -> int:
    bValid: bool = False
    while not bValid:
        lane = random.randint(1,Lane.MAX_SIZE)
        match lane:
            case 1: # A
                bValid = board.laneA.canAdd()
            case 2: # B
                bValid = board.laneB.canAdd()
            case 3: # C
                bValid = board.laneC.canAdd()
    return lane


def play() -> None:
    playerBoard = Board()
    cpuBoard = Board()
    
    refreshScreen(playerBoard=playerBoard, cpuBoard=cpuBoard)
    while True:
        playerRoll = rollDie()
        print( f"You rolled: {playerRoll}" )
        print( f"Select a lane to put {playerRoll}: A, B, C" )

        playerInput = validateInput( playerBoard )
    
        if playerInput == "Q":
            break
        elif playerInput == "A":
            playerBoard.laneA.addValue(playerRoll)
            cpuBoard.laneA.removeValue(playerRoll)
        elif playerInput == "B":
            playerBoard.laneB.addValue(playerRoll)
            cpuBoard.laneB.removeValue(playerRoll)
        elif playerInput == "C":
            playerBoard.laneC.addValue(playerRoll)
            cpuBoard.laneB.removeValue(playerRoll)

        if playerBoard.isBoardFull():
            refreshScreen(playerBoard=playerBoard, cpuBoard=cpuBoard)
            gameOver(playerBoard=playerBoard, cpuBoard=cpuBoard)

        cpuRoll = rollDie()
        cpuChoise = validateAIChoice( cpuBoard )
        
        match cpuChoise:
            case 1: # A
                cpuBoard.laneA.addValue(cpuRoll)
                playerBoard.laneA.removeValue(cpuRoll)
            case 2: # B
                cpuBoard.laneB.addValue(cpuRoll)
                playerBoard.laneB.removeValue(cpuRoll)
            case 3: # C
                cpuBoard.laneC.addValue(cpuRoll)
                playerBoard.laneC.removeValue(cpuRoll)

        refreshScreen(playerBoard=playerBoard, cpuBoard=cpuBoard)
        print( "-"* LINE_LENGTH )
        print( f"CPU rolled: {cpuRoll}" )

        if cpuBoard.isBoardFull():
            refreshScreen(playerBoard=playerBoard, cpuBoard=cpuBoard)
            print( "-"* LINE_LENGTH )
            print( f"CPU rolled: {cpuRoll}" )
            gameOver(playerBoard=playerBoard, cpuBoard=cpuBoard)

if __name__ == "__main__":
    play()
