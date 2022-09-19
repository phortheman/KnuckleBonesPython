"""
Class: Board

This class stores up to 3 lanes in a list and contains several methods that modify the list

Author: phortheman
"""


from classes.Lane import *

CELL_SIZE: int = 5
LINE_LENGTH: int = 21

class Board:
    def __init__( self ) -> None:
        self.LANES = []
        for i in range( MAX_LANE_SIZE ):
            self.LANES.append( Lane() )

    def __str__( self ) -> str:
        output = []
        for i in self.LANES:
            output.append( i.values )
        return f"{output}"

    def isBoardFull( self ) -> bool:
        for lane in self.LANES:
            if lane.canAdd():
                return False
        return True

    def calculateBoardScore( self ) -> int:
        score: int = 0

        for lane in self.LANES:
            score += lane.calculateLane()

        return score

    def clearBoard( self ) -> None:
        for lane in self.LANES:
            for i in range( len( lane.values ) ):
                lane.values[i] = 0
