from Aligner import Aligner
from SimpleNeedlemanAligner import SimpleNeedleManAligner
from typing import List

DNA = ['A', 'T', 'C', 'G']
RNA = ['C', 'G', 'A', 'U']
AMINO = ['A','R','N','D','C','Q','E','G','H','I','L','K','M','F','P','S','T','W','Y','V']
typeList = {'DNA': DNA, 'RNA': RNA, 'AMINO': AMINO}

class LAB:
    def __init__(self) -> None:
        self.__aligner = SimpleNeedleManAligner()

    def setAligner(self, aligner: Aligner):
        self.__aligner = aligner

    def getAligner(self):
        return self.__aligner

    def validateType(self, sequence: str, typeComponets):
        for char in sequence:
            if char not in typeComponets:
                return False
        return True

    def validateSequence(self, sequence: str):
        for type in typeList:
            valid = self.validateType(sequence, typeList[type])
            if valid:
                return (type, valid)
            
        return ('No valid', False)
    
    def areComparableSequences(self, sequence1: str, sequence2: str):
        for type in typeList:
            if  self.validateType(sequence1, typeList[type]) == self.validateType(sequence2, typeList[type]):
                return True
        return False

    def alignSequences(self):
        self.__aligner.filloutMatrix()
        traceback = self.__aligner.getTraceback()
        matrixGraph = self.__aligner.graphMatrix()
        tracebackGraph = self.__aligner.graphTraceback(traceback)
        sequenceIdentity = self.__aligner.getSequenceIdentiry(traceback)
        alignmentScore = self.__aligner.getAlighmentScore(traceback)
        humaReadable = self.__aligner.humaReadableRepresentation(traceback)
        return {'matrixGraph': matrixGraph, 'tracebackGraph': tracebackGraph, 'sequenceIdentity': sequenceIdentity, 'alignmentScore': alignmentScore, 'humanReadable': humaReadable}