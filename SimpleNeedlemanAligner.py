from typing import List
from Aligner import Aligner

class SimpleNeedleManAligner(Aligner):

    def __init__(self, sequences: List[str]= ['GAATTCAGTTA', 'GGATCGA'], identityValue: int = 2, distinctValue: int = -1, gapPenaltyValueRight: int = -2, gapPenaltyValueDown: int = -2) -> None:
        super().__init__(sequences, identityValue, distinctValue, gapPenaltyValueRight, gapPenaltyValueDown)
        self.shotter = sequences[0]
        self.longer = sequences[1]
    

    def arrangeBeferoFillout(self):
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

        return valueList

    def filloutMatrix(self):
        self.arrangeBeferoFillout()    
        for i in range(self.rowsLength):
            for j in range(self.columLength):
                valueList = self.getMaxValue(i, j)
                value = max(valueList, key=lambda item: item[0])[0]
                self.matrix[i].append(value)

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
                valueList = self.getMaxValue(i, j)
                maxValuePosition = max(valueList, key=lambda item: item[0])[1]
                info['gap'] = not maxValuePosition == (i-1,j-1)
                info['indentity'] = False
                i,j = maxValuePosition
            traceback.append(info)

        return traceback


    def humaReadableRepresentation(self, traceback):
        traceback.reverse()
        graph = ''

        if len(self.shotter) > len(self.longer):
            longer = self.shotter
            shotter = self.longer
        else:
            longer = self.longer
            shotter = self.shotter

        for char in longer:
            graph += char + '\t'
        graph += '\n'


        for info in traceback:
            graph += '|' + '\t' if info['indentity'] else ' ' + '\t'
        graph += '\n'

        i  = 0
        for info in traceback:
            if info['gap'] and not info['indentity']:
                graph += '-' + '\t' 
            else:
                graph += shotter[i] + '\t'
                i += 1

        return graph
    
    def graphMatrix(self):
        graph = '\t'
        space = '\t'

        for char in self.longer:
            graph += ' ' + char + space
        graph += '\n'

        for i in range(self.rowsLength):
            graph += self.shotter[i] + space
            for j in range(self.columLength):
                if self.matrix[i][j] >= 0:
                    graph += ' ' + str(self.matrix[i][j]) + space
                else:
                    graph += str(self.matrix[i][j]) + space
            graph += '\n'

        return graph
    
    def graphTraceback(self, traceback):
        graph = ''
        space = '\t'

        positions = [info['position'] for info in traceback]

        for char in self.longer:
            graph += space + char
        graph += '\n'

        for i in range(self.rowsLength):
            graph += self.shotter[i] + space
            for j in range(self.columLength):
                if (i,j) in positions:
                    graph += str(self.matrix[i][j]) + space
                else:
                    graph += ' ' + space
            graph += '\n'

        return graph
                

    def getAlighmentScore(self, traceback):
        score = 0
        for info in traceback:
            score += info['value']
        return score
    
    def getSequenceIdentiry(self, traceback):
        identicalPairCounter = 0
        for info in traceback:
            if info['indentity']:
                identicalPairCounter += 1

        if len(self.shotter) > len(self.longer):
            longer = self.shotter
        else:
            longer = self.longer

        return identicalPairCounter / len(longer) * 100
    
    def setSequences(self, sequences: List[str]):
        self.shotter = sequences[0]
        self.longer = sequences[1]