import os
import tkinter.filedialog
from LAB import LAB
from SimpleNeedlemanAligner import SimpleNeedleManAligner
from MultplePathsNeedlemanAligner import MultplePathsNeedlemanAligner

lab = LAB()

def validateInput(options, message = '\n * ERROR: Invalid Option, try again... '):
        length = len(options)
        title()
        print(' > Select an option')
        validOptions = [*range(1, length+1)]
        for i in validOptions:
             print(f'   [{i}] ', options[i-1])
        option = input('\n\n > Option: ')
        if option.isdigit():
             option = int(option)
        while option not in validOptions:
            title()
            print(' > Select an option')
            for i in validOptions:
                print(f'   [{i}] ', options[i-1])
            print(message)
            option = input(' > Option: ')
            if option.isdigit():
                option = int(option)
        return int(option)

def title():
    os.system('cls')
    print('______________________________________________')
    print('         Sequences Aligner Menu')
    print('______________________________________________')

def fileInputOptions():
    options = ['Copy and Paste 2 sequences', 'Select 2 files']
    option = validateInput(options)
    if option == 1:
        sequence1 = input(' > First Sequence: ')
        sequence2 = input(' > Second Sequence: ')
    else:
        print(' > Select the first file ')
        sequence1 = tkinter.filedialog.askopenfile().read()
        print(' > Select the second file ')
        sequence2 = tkinter.filedialog.askopenfile().read()
    return sequence1, sequence2

def alignmentOptions():
    aligner = lab.getAligner()
    matrixGraph, alignmentList = aligner.alignSequences()
    print(matrixGraph)

    fileContent = ''
    os.system('cls')
    fileContent += ' Table\n'
    fileContent += '-------\n'
    fileContent += matrixGraph +'\n\n'

    for aligment in alignmentList:
        fileContent += ' Traceback\n'
        fileContent += '-----------\n'
        fileContent += aligment['tracebackGraph']+'\n\n'
        fileContent += ' Human-Readable Representation\n'
        fileContent += '-------------------------------\n'
        fileContent += '\n' + aligment['humanReadable']+'\n'
        fileContent += '\nAligment Score: ' + str(aligment['alignmentScore'])+'\n'
        fileContent += 'Sequence Identity Score: ' + str(aligment['sequenceIdentity']) + '%\n\n'

    print(fileContent)
    storeInFile(fileContent)


def storeInFile(input):
    file = open("NeedlemanWunsch.txt", 'w')
    file.write(input)
    file.close()

def run():
    repeat = True

    while repeat:
        while repeat:
            sequence1, sequence2 = fileInputOptions()
            type1, valid1 = lab.validateSequence(sequence1)
            type2, valid2 = lab.validateSequence(sequence2)
            if not ( valid1 and valid2 ):
                print('\n * ERROR: Ivalid Sequences, select an option again... ')
            elif not lab.areComparableSequences(sequence1, sequence2):
                print('\n * ERROR: No Comparable Sequences, select an option again... ')
            else:
                # print('\n * INFO: Sequences are Comparable and Valid!! ')
                repeat =  False
            print(' > First Sequence: ', sequence1)
            print('   Type:', type1)
            print('   Valid: ', valid1)
            print(' > Second Sequence: ', sequence2)
            print('   Type:', type2)
            print('   Valid: ', valid2)
            os.system("pause")

        options = ['Show Needleman Wunsch Aligment results (following Chris Presentation)', 
                   'Show Multiverse Needleman Wunsch Aligment results']
        option = validateInput(options)

        if option == 1:
            lab.setAligner(SimpleNeedleManAligner([sequence1, sequence2]))
        elif option == 2:
            lab.setAligner(MultplePathsNeedlemanAligner([sequence1, sequence2]))
        
        alignmentOptions()
        print('\nNOTE: File NeedlemanWunsch.txt was created whith the whole run info, check it out!! \n')
        while repeat not in ['Y', 'N', 'y', 'n']:
            repeat = input('Start Again? Y/N ... ')

        repeat = repeat in ['Y', 'y']