from SimpleNeedlemanAligner import SimpleNeedleManAligner
from LAB import LAB

if __name__ == '__main__':
    sequence1 = 'GAATTCAGTTA'
    sequence2 = 'GGATCGA'
    amino = 'CGAU'
    sequences = [sequence1, sequence2]
    aligner = SimpleNeedleManAligner(sequences=sequences)
    lab = LAB()
    print("Is sequence 1 valid: ", lab.validateSequence(sequence1))
    print("Is sequence 2 valid: ", lab.validateSequence(amino))
    # print("Are Comparable: ", lab.areComparableSequences(sequence1, amino))
    

    