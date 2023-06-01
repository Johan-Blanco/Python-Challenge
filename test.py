from LAB import LAB
from SimpleNeedlemanAlignerMultplePaths import SimpleNeedlemanAlignerMultplePaths

if __name__ == '__main__':
    lab = LAB()
    sequences = ['GAATTCAGTTA', 'GGATCGA']
    lab.setAligner(SimpleNeedlemanAlignerMultplePaths(sequences))
    aligner = lab.getAligner()
    aligner.filloutMatrix()

    
    # traceback = aligner.getTraceback()
    # print(aligner.graphMatrix())
    # print(aligner.graphTraceBack(traceback))
    # print(aligner.getSequenceIdentiry(traceback))
    # print(aligner.getAlighmentScore(traceback))