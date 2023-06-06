import os
import tkinter.filedialog
import sys
from LAB import LAB
from SimpleNeedlemanAligner import SimpleNeedleManAligner

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
    print('          Sequence Aligner Menu')
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
    options = ['Show Aligment Scoring Table', 'Show Alignment Score',
               'Show Sequence Identity Score', 'Show Human-Readable Representation of the Alignment','Show Complete Analisis']
    results = lab.alignSequences()
    fileContent = ''
    os.system('cls')
    fileContent += ' Table\n'
    fileContent += '-------\n'
    fileContent += results['matrixGraph']+'\n\n'
    fileContent += ' Traceback\n'
    fileContent += '-----------\n'
    fileContent += results['tracebackGraph']+'\n\n'
    fileContent += ' Human-Readable Representation\n'
    fileContent += '-------------------------------\n'
    fileContent += '\n' + results['humanReadable']+'\n'
    fileContent += '\nAligment Score: ' + str(results['alignmentScore'])+'\n'
    fileContent += 'Sequence Identity Score: ' + str(results['sequenceIdentity']) + '%'
    print(fileContent)
    storeInFile(fileContent)


def storeInFile(input):
    file = open("NeedlemanWunsch.txt", 'w')
    file.write(input)
    file.close()

def workflow():
    repeat = True

    while repeat:
        while repeat:
            sequence1, sequence2 = fileInputOptions()
            type1, valid1 = lab.validateSequence(sequence1)
            type2, valid2 = lab.validateSequence(sequence2)
            if not ( valid1 and valid2 and lab.areComparableSequences(sequence1, sequence2)):
                print('\n * ERROR: Ivalid Sequences, select an option again... ')
            else:
                repeat =  False
            print(' > First Sequence: ', sequence1)
            print('   Type:', type1)
            print('   Valid: ', valid1)
            print(' > Second Sequence: ', sequence2)
            print('   Type:', type2)
            print('   Valid: ', valid2)
            os.system("pause")

        lab.setAligner(SimpleNeedleManAligner([sequence1, sequence2]))
        alignmentOptions()

        while repeat not in ['Y', 'N', 'y', 'n']:
            repeat = input('Start Again? Y/N ... ')

        repeat = repeat in ['Y', 'y']
workflow()
