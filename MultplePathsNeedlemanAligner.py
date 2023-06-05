from typing import List
from SimpleNeedlemanAligner import SimpleNeedleManAligner

class MultplePathsNeedlemanAligner(SimpleNeedleManAligner):

    def __init__(self, sequences: List[str] = ['GAATTCAGTTA', 'GGATCGA'], identityValue: int = 2, distinctValue: int = -1, gapPenaltyValueRight: int = -2, gapPenaltyValueDown: int = -2) -> None:
        super().__init__(sequences, identityValue, distinctValue, gapPenaltyValueRight, gapPenaltyValueDown)
  
    def getMaxValueForTraceback(self, i, j):
        if i > 0 and j > 0:
            diagonal = (self.matrix[i-1][j-1], (i-1,j-1))
            left = (self.matrix[i][j-1], (i, j-1))
            up = (self.matrix[i-1][j], (i-1, j))
            maxValue =  max(diagonal, left, up)
            return diagonal if maxValue[0] == diagonal[0] else maxValue
        elif i == 0:
            left = self.matrix[i][j-1], (i, j-1)
            return left
        elif j == 0:
            up = self.matrix[i-1][j], (i-1, j)
            return up

    def getTraceBackInfo(self, i, j):
        info = {'position': (i,j), 'value': self.matrix[i][j]}
        if self.shortest[i] == self.longest[j]:
            if i == 0 and j != 0:
                info['gap-in'] = 'shortest'
                info['indentity'] = False
            elif j == 0 and j != 0:
                info['gap-in'] = 'longest'
                info['indentity'] = False
            else:
                info['gap-in'] = 'N/A'
                info['indentity'] = True
            i,j = i-1, j-1
        else:
            maxValuePosition = self.getMaxValueForTraceback(i, j)[1] # use different function
            if not maxValuePosition == (i-1,j-1) and info['position'] != (0,0):
                info['gap-in'] = 'shortest' if maxValuePosition[1] == j-1 else 'longest'
            else:
                info['gap-in'] = 'N/A'
            info['indentity'] = False
            i,j = maxValuePosition
        return info, i, j

    def getTraceback(self):
        i = self.rowsLength - 1
        j = self.columLength - 1

        traceback = []

        while i >= 0 and j >= 0:
            info, i, j = self.getTraceBackInfo(i, j)
            traceback.append(info)
        
        if info['position'] != (0,0):
            if i < 0:
                # check to the left
                while j >= 0:
                    info, i, j = self.getTraceBackInfo(0, j)
                    traceback.append(info)
            elif j < 0:
                # check up
                while i >= 0:
                    info, i, j = self.getTraceBackInfo(i, 0)
                    traceback.append(info)

        return traceback
    
    def getFullAnalisis(self):
        multiverse = []


    