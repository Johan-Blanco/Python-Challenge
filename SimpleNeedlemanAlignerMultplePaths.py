from typing import List
from SimpleNeedlemanAligner import SimpleNeedleManAligner

class SimpleNeedlemanAlignerMultplePaths(SimpleNeedleManAligner):

    def __init__(self, sequences: List[str] = ['GAATTCAGTTA', 'GGATCGA'], identityValue: int = 2, distinctValue: int = -1, gapPenaltyValueRight: int = -2, gapPenaltyValueDown: int = -2) -> None:
        super().__init__(sequences, identityValue, distinctValue, gapPenaltyValueRight, gapPenaltyValueDown)
  
    
    
    
    def getTraceback(self):
        i = self.rowsLength - 1
        j = self.columLength - 1

        traceback = []

        while i >= 0 and j >= 0:
            info = {'position': (i,j), 'value': self.matrix[i][j]}
            if self.shotter[i] == self.longer[j]:
                info['gap'] = False
                info['indentity'] = True
                i,j = i-1, j-1
            else:
                maxValuePosition = self.getMaxValue(i, j)[1] # returns all the values
                info['gap'] = not maxValuePosition == (i-1,j-1)
                info['indentity'] = False
                i,j = maxValuePosition
            traceback.append(info)

        return traceback

    