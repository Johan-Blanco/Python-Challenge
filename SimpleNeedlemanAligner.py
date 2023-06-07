from typing import List
from Aligner import Aligner

"""
This is a class has the logic to solve the aligment as Chris explained at the
beginnig of the challenge
"""

class SimpleNeedleManAligner(Aligner):

    def __init__(self, sequences: List[str]= ['GAATTCAGTTA', 'GGATCGA'], identityValue: int = 2, distinctValue: int = -1, gapPenaltyValueRight: int = -2, gapPenaltyValueDown: int = -2) -> None:
        super().__init__(sequences, identityValue, distinctValue, gapPenaltyValueRight, gapPenaltyValueDown)
        self.shortest = sequences[0]
        self.longest = sequences[1]
        self.matrix = []

    """
    Before filling out the matrix some stuff need to be arranged first
    such as creating the matrix and selecting which one is going to be
    the longest and which one the shortest, in order to have always
    the decired results
    """
    def arrangeBeferoFillout(self):
        self.matrix = []
        if len(self.shortest) > len(self.longest):
            self.longest = self.sequences[0]
            self.shortest = self.sequences[1]
        self.rowsLength = len(self.shortest)
        self.columLength = len(self.longest)

        for _ in range(self.rowsLength):
            self.matrix.append([])

    """
    This method calculates the value that is going to have every position in the matrix
    following the rules, explained by Chris
    """
    def getCellValue(self, i, j):

        valueList = []

        # Diagonal Value
        temp = 0
        position = (i-1, j-1)
        if i != 0 and j != 0:
            temp = self.matrix[position[0]][position[1]]
        diagonal  = temp + self.identityValue if self.shortest[i] == self.longest[j] else temp + self.distinctValue
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
    
    """
    This function fills out the matrix and calls the funtion that calculates the value for every position
    in the matrix
    """
    def filloutMatrix(self):
        self.arrangeBeferoFillout()    
        for i in range(self.rowsLength):
            for j in range(self.columLength):
                value = self.getCellValue(i, j)[0]
                self.matrix[i].append(value)

    """
    This funtion gets the max value between diagnal, left and up values based on the current
    position in the matrix, this max value is the one that tells the program
    which one is going to be the next one in order to complete the traceback
    """
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
        
    """
    This funtions keeps the logic that is needed to get the traceback
    following the rules presented by Chris
    """
    def getTraceback(self):
        i = self.rowsLength - 1
        j = self.columLength - 1

        traceback = []

        while i > 0 and j > 0:
            info = {'position': (i,j), 'value': self.matrix[i][j]}
            if self.shortest[i] == self.longest[j]:
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
            traceback.append(info)

        # check leftside
        while j > 0:
            info = {'position': (0,j), 'value': self.matrix[0][j]}
            info['gap-in'] = 'shortest'
            info['indentity'] = False
            j -= 1
            traceback.append(info)

        # check upside
        while i > 0:
            info = {'position': (i,0), 'value': self.matrix[i][0]}
            info['gap-in'] = 'longest'
            info['indentity'] = False
            i -= 1
            traceback.append(info)

        # 0,0 position
        info = {'position': (i,j), 'value': self.matrix[i][j]}
        info['indentity'] = self.shortest[0] == self.longest[j]
        info['gap-in'] = 'N/A'
        
        traceback.append(info)
        return traceback

    """
    This funtion graphs a human readable representation of the traceback
    """
    def humaReadableRepresentation(self, traceback): #WRONG
        traceback.reverse()
        line1 = ''
        line2 = ''
        line3 = ''
        shortest = [*self.shortest[::-1]]
        longest = [*self.longest[::-1]]

        for info in traceback:
            line1 += '_\t' if info['gap-in'] == 'longest' else longest.pop() + '\t'
            line2 += '|\t' if info['indentity'] else ' \t'
            line3 += '_\t' if info['gap-in'] == 'shortest' else shortest.pop() + '\t'
            
        
        return line1 + '\n' + line2 + '\n' + line3
        
        
    """
    This funtion graphs a matrix and adds the two sequences to make it more
    understandable
    """
    def graphMatrix(self):
        graph = '\t'
        space = '\t'

        for char in self.longest:
            graph += ' ' + char + space
        graph += '\n'

        for i in range(self.rowsLength):
            graph += self.shortest[i] + space
            for j in range(self.columLength):
                if self.matrix[i][j] >= 0:
                    graph += ' ' + str(self.matrix[i][j]) + space
                else:
                    graph += str(self.matrix[i][j]) + space
            graph += '\n'

        return graph
    

    """
    This funtion graphs the matrix but prints out just the positions
    that were collected in the traceback
    """
    def graphTraceback(self, traceback):
        graph = ''
        space = '\t'

        positions = [info['position'] for info in traceback]

        for char in self.longest:
            graph += space + ' ' + char
        graph += '\n'

        for i in range(self.rowsLength):
            graph += self.shortest[i] + space
            for j in range(self.columLength):
                if (i,j) in positions:
                    if self.matrix[i][j] >= 0:
                        graph += ' ' + str(self.matrix[i][j]) + space
                    else:
                        graph += str(self.matrix[i][j]) + space
                else:
                    graph += ' ' + space
            graph += '\n'

        return graph
                
    """
    This funtion calculates the alignment Score for a given traceback
    it just accumulate all the matrix values collected in the traceback
    """
    def getAlighmentScore(self, traceback):
        score = 0
        for info in traceback:
            score += info['value']
        return score
    
    """
    This funtion calculates the sequence Identity for a given traceback
    """
    def getSequenceIdentiry(self, traceback):
        identicalPairCounter = 0
        for info in traceback:
            if info['indentity']:
                identicalPairCounter += 1

        sequenceIdentity =  identicalPairCounter / len(self.longest) * 100
        return round(sequenceIdentity, 2)
    

    """
    This funtion has the steps to make the whole analisis
    following the rules presented by Chris
    """
    def alignSequences(self):
        self.filloutMatrix()
        matrixGraph = self.graphMatrix()
        alignmentList = []
        
        traceback = self.getTraceback()
        tracebackGraph = self.graphTraceback(traceback)
        sequenceIdentity = self.getSequenceIdentiry(traceback)
        alignmentScore = self.getAlighmentScore(traceback)
        humaReadable = self.humaReadableRepresentation(traceback)
        alignment = {'traceback': traceback,'tracebackGraph': tracebackGraph, 'sequenceIdentity': sequenceIdentity, 'alignmentScore': alignmentScore, 'humanReadable': humaReadable}
        alignmentList.append(alignment)
        return matrixGraph, alignmentList