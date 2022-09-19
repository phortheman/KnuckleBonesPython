"""
Class: Lane

This class stores up to 3 ints in a list and contains several methods that modify the list

Author: phortheman
"""

MAX_LANE_SIZE: int = 3

class Lane:
    def __init__( self ) -> None:
        self.values = [0] * MAX_LANE_SIZE

    def __str__( self ) -> str:
        return f"{self.values}"

    """
    Sum all the dice together. If there are duplicates (chained dice) then those are 
    multiplied by square root of the count
    Example: 1, 4, 4 = 17 because 1 + ( 4 * 2**2 )
         or: 6, 6, 6 = 54 because 6 * 3**2
         or: 1, 2, 3 = 6 because 1 + 2 + 3
    """
    def calculateLane( self ) -> int:
        sum = 0
        chainValue = 0 # This is the value that has a chain

        for value in self.values:
            # No more values to calculate in the lane
            if value == 0:
                break
            # Chained values are already accounted for
            if value == chainValue:
                continue

            count = self.values.count(value)
            match count:
                case 3:
                    return value * count ** 2
                case 2:
                    chainValue = value
                    sum += chainValue * count ** 2
                case 1:
                    sum += value

        return sum

    """
    Remove the specified value from the lane
    Puts i into a shallow copy of the list if the value doesn't match i
    Then appends zeros to the end until the list is full
    """
    def removeValue( self, value ) -> None:
        self.values[:] = [i for i in self.values if i != value]
        while len( self.values ) != MAX_LANE_SIZE:
            self.values.append( 0 )

    # If a value can be added to a lane then override the first instance of a zero
    def addValue( self, value ) -> bool: 
        if self.canAdd(): # The Lane is full
            for i in range( len( self.values ) ):
                if self.values[i] == 0:
                    self.values[i] = value
                    break
            return True
        
        return False

    # If the lane doesn't have any zeroes then the lane is full
    def canAdd( self ) -> bool:
        if self.values.count(0) == 0:
            return False
        return True
