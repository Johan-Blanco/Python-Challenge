from Aligner import Aligner
from typing import List

ADN = ['A', 'T', 'C', 'G']
ARN = ['C', 'G', 'A', 'U']
AMINO = ['A','R','N','D','C','Q','E','G','H','I','L','K','M','F','P','S','T','W','Y','V']
typeList = {'ADN': ADN, 'ARN': ARN, 'AMINO': AMINO}

class LAB:
    def __init__(self) -> None:
        self.__aligner = None

    def setAligner(self, aligner: Aligner):
        self.__aligner = aligner

    def validateType(self, sequence: str, typeComponets):
        for char in sequence:
            if char not in typeComponets:
                return False
        return True

    def validateSequence(self, sequence: str):
        validList = []
        for type in typeList:
            valid = self.validateType(sequence, typeList[type])
            validList.append((type, valid))

        for value in validList:
            if value[1]:
                return value
            
        return ('ERROR', False)
    
    def areComparableSequences(self, sequence1: str, sequence2: str):
        for typeComponents in typeList:
            if not (self.validateType(sequence1, typeComponents) == self.validateType(sequence1, typeComponents)):
                return False
        return True
    
    def setAlignmentValues(self, valuesTouple):
        if self.__aligner is not None:
            identityValue, distinctValue, gapPenaltyValueDown, gapPenaltyValueRight = valuesTouple
            self.__aligner.setValues(identityValue, distinctValue, gapPenaltyValueDown, gapPenaltyValueRight)

    def alignSequences(self):
        if self.__aligner is not None:
            self.__aligner.filloutMatrix()
            traceback = self.__aligner.getTraceback()
            matrix = self.__aligner.getMatrix()
            tracebackGraph = self.__aligner.graphTraceback(traceback)
            sequenceIdentity = self.__aligner.getSequenceIdentiry(traceback)
            return {'matrix': matrix, 'tracebackGraph': tracebackGraph, 'sequenceIdentity': sequenceIdentity}