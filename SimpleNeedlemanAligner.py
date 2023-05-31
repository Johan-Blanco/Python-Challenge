from typing import List
from Aligner import Aligner

class SimpleNeedleManAligner(Aligner):

    def __init__(self, sequences: List[str], identityValue: int = 2, distinctValue: int = -1, gapPenaltyValueRight: int = -2, gapPenaltyValueDown: int = -2) -> None:
        super().__init__(sequences, identityValue, distinctValue, gapPenaltyValueRight, gapPenaltyValueDown)
        self.shotter = sequences[0]
        self.longer = sequences[1]
    

    def arrangeBeferoFillout(self):
        if len(self.shotter) > len(self.longer):
            self.longer = self.sequences[0]
            self.shotter = self.sequences[1]

        self.matrix = []
        self.rowsLength = len(self.shotter)
        self.columLength = len(self.longer)

        for _ in range(self.rowsLength):
            self.matrix.append([])

    def getMaxValue(self, i, j):

        valueList = []

        # Diagonal Value
        temp = 0
        position = (i-1, j-1)
        if i != 0 and j != 0:
            temp = self.matrix[position[0]][position[1]]
        diagonal  = temp + self.identityValue if self.shotter[i] == self.longer[j] else temp + self.distinctValue
        valueList.append( (diagonal, position) )

        # Up Value
        temp = 0
        position = (i-1, j)
        if i != 0:    
            temp = self.matrix[position[0]][position[1]]
        upValue  = temp + self.gapPenaltyValueDown
        valueList.append( (upValue, position) )

         # Left Value
        temp = 0 
        position = (i, j-1)
        if j != 0:
            temp = self.matrix[position[0]][position[1]]
        leftValue  = temp + self.gapPenaltyValueDown
        valueList.append( (leftValue, position) )

        return max(valueList, key=lambda item: item[0])

    def filloutMatrix(self):
        self.arrangeBeferoFillout()    
        for i in range(self.rowsLength):
            for j in range(self.columLength):
                value = self.getMaxValue(i, j)[0]
                self.matrix[i].append(value)

    def getTraceback(self):
        i = self.rowsLength - 1
        j = self.columLength - 1

        traceback = []

        while i >= 0 and j >= 0:
            info = {'position': (i,j) }
            if self.shotter[i] == self.longer[j]:
                info['gap'] = False
                info['indentity'] = True
                i,j = i-1, j-1
            else:
                maxValuePosition = self.getMaxValue(i, j)[1]
                info['gap'] = not maxValuePosition == (i-1,j-1)
                info['indentity'] = False
                i,j = maxValuePosition
            traceback.append(info)

        return traceback


    def graphTraceback(self, traceback):
        displayLines = []
        traceback.reverse()

        line = ''
        for char in self.longer:
            line += char + '\t'
        displayLines.append(line)

        line = ''
        for info in traceback:
            line += '|' + '\t' if info['indentity'] else ' ' + '\t'
        displayLines.append(line)

        line = ''
        i  = 0
        for info in traceback:
            if info['gap'] and not info['indentity']:
                line += '-' + '\t' 
            else:
                line += self.shotter[i] + '\t'
                i += 1
        displayLines.append(line)

        return displayLines
    
    def getSequenceIdentiry(self, traceback):
        identicalPairCounter = 0
        for info in traceback:
            if info['indentity']:
                identicalPairCounter += 1
        return identicalPairCounter / len(self.longer) * 100
    
    def setSequences(self, sequences: List[str]):
        self.shotter = sequences[0]
        self.longer = sequences[1]