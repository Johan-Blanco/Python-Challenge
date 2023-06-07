from typing import List
from abc import ABC, abstractmethod

"""
This is a interface Class which is going to be used for strategy pattern,
in case more strategies for solving the aligment are implemented
"""

class Aligner(ABC):

    def __init__(self, sequences: List[str], identityValue: int, distinctValue: int, 
                 gapPenaltyValueRight: int, gapPenaltyValueDown: int) -> None:
        self.sequences = sequences
        self.identityValue = identityValue
        self.distinctValue = distinctValue
        self.gapPenaltyValueRight = gapPenaltyValueRight
        self.gapPenaltyValueDown = gapPenaltyValueDown
        self.matrix = []
        self.rowsLength = 0
        self.columLength = 0

    @abstractmethod
    def filloutMatrix(self):
        pass

    @abstractmethod
    def getTraceback(self, fn):
        pass

    @abstractmethod
    def graphTraceback(self, traceback):
        pass

    @abstractmethod
    def getSequenceIdentiry(self, traceback):
        pass

    def setValues(self, identityValue: int, distinctValue: int, 
                 gapPenaltyValueRight: int, gapPenaltyValueDown: int):
        self.identityValue = identityValue
        self.distinctValue = distinctValue
        self.gapPenaltyValueRight = gapPenaltyValueRight
        self.gapPenaltyValueDown = gapPenaltyValueDown

    def getMatrix(self):
        return self.matrix

