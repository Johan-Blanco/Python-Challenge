from typing import List
from SimpleNeedlemanAligner import SimpleNeedleManAligner

class MultplePathsNeedlemanAligner(SimpleNeedleManAligner):

    def __init__(self, sequences: List[str] = ['GAATTCAGTTA', 'GGATCGA'], identityValue: int = 2, distinctValue: int = -1, gapPenaltyValueRight: int = -2, gapPenaltyValueDown: int = -2) -> None:
        super().__init__(sequences, identityValue, distinctValue, gapPenaltyValueRight, gapPenaltyValueDown)
        self.multiverse = []
        self.completedTracebacks = []

    """
    This funtion gets the max value between diagnal, left and up values based on the current
    position in the matrix, this max value is the one that tells the program
    which one is going to be the next one in order to complete the traceback

    In this case it allso calls a funtions that tracks all the possibilities
    when moving on through the traceback
    """
    def getMaxValueForTraceback(self, i, j, matrix):
        if i > 0 and j > 0:
            diagonal = (matrix[i-1][j-1], (i-1,j-1))
            left = (matrix[i][j-1], (i, j-1))
            up = (matrix[i-1][j], (i-1, j))
            valueList = [diagonal, left, up]
            maxValue = max(valueList, key=lambda item: item[0])
            return maxValue, valueList
        elif i == 0:
            left = matrix[i][j-1], (i, j-1)
            return left
        elif j == 0:
            up = matrix[i-1][j], (i-1, j)
            return up
        
    """
    This funtion collects all the possible paths to continue with the traceback
    and adds those possibilities to a list
    """
    def checkForNewAlternatives(self, listValues, maxValue, traceback, info, i, j):
        alternatives = [value for value in listValues if value[0] ==  maxValue[0] and value[1] !=  maxValue[1]]
        if len(alternatives) > 0:
            for alternative in alternatives:
                info['started-at'] = {f'{str(self.matrix[i][j])}': (i,j)}
                maxValue = alternative
                i, j, info = self.gapIn(i,j, info, maxValue)
                traceback.append(info)
                newUniverse = { 'traceback': traceback, 'nextStepPosition': maxValue[1]}
                self.multiverse.append(newUniverse)

    """
    
    """
    def gapIn(self, i, j, info, maxValue):
        maxValuePosition = maxValue[1]
        diagonalPosition = (i-1,j-1)
        leftPosition = (i, j-1)
        if maxValuePosition == diagonalPosition:
            info['gap-in'] = 'N/A'
        elif maxValuePosition == leftPosition:
            info['gap-in'] = 'shortest'
        else:
            info['gap-in'] = 'longest'
        info['indentity'] = False
        
        i,j = maxValuePosition

        return i, j, info
    """
    It was neccesary to overwrite this funtions due to some modifications
    in order to don't affect the funtion in the SimpleNeedlemanAligner File
    """
    def getTraceback(self, traceback = None, i = None, j = None):
        if i == j == traceback == None:
            i = self.rowsLength - 1
            j = self.columLength - 1
            traceback = []
        else:
            traceback = traceback

        while i > 0 and j > 0:
            info = {'position': (i,j), 'value': self.matrix[i][j], 'vs': (self.shortest[i], self.longest[j])}
            if self.shortest[i] == self.longest[j]:
                info['gap-in'] = 'N/A'
                info['indentity'] = True
                i,j = i-1, j-1
            else:
                maxValue, valueList = self.getMaxValueForTraceback(i, j, self.matrix)
                iAux, jAux = i, j
                i, j, info = self.gapIn(i,j, info, maxValue)
                self.checkForNewAlternatives(valueList, maxValue, traceback[:], info.copy(), iAux, jAux)
            traceback.append(info)
        

        # check to the left
        while j > 0:
            info = {'position': (i,j), 'value': self.matrix[i][j], 'vs': (self.shortest[i], self.longest[j])}
            info['gap-in'] = 'shortest'
            info['indentity'] = False
            j -= 1
            traceback.append(info)

        # check upside
        while i > 0:
            info = {'position': (i,j), 'value': self.matrix[i][j], 'vs': (self.shortest[i], self.longest[j])}
            info['gap-in'] = 'longest'
            info['indentity'] = False
            i -= 1
            traceback.append(info)

        # 0,0 position
        info = {'position': (i,j), 'value': self.matrix[i][j], 'vs': (self.shortest[i], self.longest[j])}
        info['gap-in'] = 'N/A'
        info['indentity'] = self.shortest[i] == self.longest[j]
        traceback.append(info)
        return traceback
    
    """
    This funtion keeps the logic that collects all the possible
    tracebacks
    """
    def multipathAlignment(self):
        self.filloutMatrix()
        traceback = self.getTraceback()
        self.completedTracebacks.append(traceback)

        while len(self.multiverse) > 0:
            parallelUniverse = self.multiverse.pop(0)
            traceback = parallelUniverse['traceback']
            i, j = parallelUniverse['nextStepPosition']
            traceback = self.getTraceback(traceback[:], i, j)
            self.completedTracebacks.append(traceback)

    """
    This funtion has the steps to make the whole analisis
    but it this case collecting all the possibilities
    """
    def alignSequences(self):
        self.multipathAlignment()
        matrixGraph = self.graphMatrix()
        alignmentList = []

        for traceback in self.completedTracebacks:
            tracebackGraph = self.graphTraceback(traceback)
            sequenceIdentity = self.getSequenceIdentiry(traceback)
            alignmentScore = self.getAlighmentScore(traceback)
            humaReadable = self.humaReadableRepresentation(traceback)
            alignment =  {'traceback': traceback,'tracebackGraph': tracebackGraph, 'sequenceIdentity': sequenceIdentity, 'alignmentScore': alignmentScore, 'humanReadable': humaReadable}
            alignmentList.append(alignment)
        return matrixGraph, alignmentList