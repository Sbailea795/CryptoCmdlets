#!/usr/bin/env python

import argparse
import io
from statistics import mean, median, stdev, variance
import sys
import Crypto_Utilities
from Metadata import Metadata

def main(argv):  
    #parse args
    parser = argparse.ArgumentParser(description='Analysis on frequency of letters in a given text')
    parser.add_argument('text', nargs='*', type=str,
                        help='text to be analyzed', metavar='text')
    parser.add_argument('-c', '--columns', default='1', type=int, choices=[1,2,3,4],
                        help='How many columns to display the data.mdata in', metavar='Columns')
    parser.add_argument('-a', '--alphabet', nargs='*', default=str(Crypto_Utilities.lowerAlphabet), type=str, help='Alphabet(s) used to analyze the text', metavar='Alphabet')
    parser.add_argument('-s', '--signature', default=False, help='Generates a signature pairing of the scrawl(s)', metavar='signature')
    
    #Error try-catch
    try:               
        args = parser.parse_args()
        for texts in args.text:
            Crypto_Utilities.sanitizeText(texts)
    except argparse.ArgumentError:
        sys.exit('Error: ArgumentParser failed to parse the arguments')
    label = 1
    combinations = []
    formatted = []
    for text in args.text:
        for alphabet in args.alphabet:
            combinations.append(Metadata(text, alphabet))
    for combo in combinations:
        formatted.append(FormatToString(combo, "graph #: {:2}".format(label), False))
        formatted.append(FormatToString(combo, "graph #: {:2}".format(label), True))
        label+=1
    printToOut(args.columns, formatted)

def printToOut(width, combinations: list):
    
    while(len(combinations) % width != 0):
        combinations.append(' ')
    texts = []
    for combo in combinations:
        texts.append(str(combo).splitlines())

    for index in range(0, len(texts), width):
        lines=[]
        row = texts[index:index+width]
        for i in range(0,len(row)):
            lines.append(len(max(row, key=len)))
        gap = ' '

        for line in range(0, max(lines)):
            for item in range(0, width):
                if (line < len(row[item])):
                    print(row[item][line].ljust(len(row[item][0])), end='')
                    print(gap.center(10), end='')
                else:
                    print(' '.ljust(len(row[item][0])), end='')
                    print(gap.center(10), end='')
            print()

def FormatToString(data: Metadata, label: str, signature: bool):
    leftBorder = 17
    width = 3
    gap = ' '
    resolution = max(((100*data.mdata['maximum']/data.mdata['length']) / data.mdata['alphabetLength']), 1/2)
    if signature:
        sortKey = 1
    else:
        sortKey = 0
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout

    print(label.center(leftBorder , '_'), end='')
    for char in sorted(data.mdata['frequencies'], key=lambda x: x[sortKey]):
        print(char[0].center(width, '_'), end='')
    print()

    for i in range(0, int(data.mdata['alphabetLength'])):
        line = '|'  
        background = ' ' 
        print("{0} : {1:03}, {2:06.3f}% ".format( data.mdata['frequencies'][i][0], data.mdata['frequencies'][i][1], 100*data.mdata['frequencies'][i][1]/data.mdata['length'] ), end='')
        for char in sorted(data.mdata['frequencies'], key=lambda x: x[sortKey]):
            
            if i * resolution <= 100*data.mdata['medianVal']/data.mdata['length'] < (i + 1) * resolution:
                background = '='
            elif i * resolution <= 100*data.mdata['average']/data.mdata['length']< (i + 1) * resolution:
                background = '-'

            if (100*char[1]/data.mdata['length']) > i * resolution:
                print(line.center(width, background), end='')
            else:
                print(background.center(width, background), end='')
        print()
    print("Concavity: {0:-5.5f}".format(data.mdata['relConcavity']))
    print("Tick Resolution: {0:5.5}".format(resolution))
    print("Median: {0:03}, {1:05.2f}%".format(data.mdata['medianVal'], 100*(data.mdata['medianVal']/data.mdata['length'])))
    print("Average: {0:05.2f}, {1:05.2f}%".format(data.mdata['average'], 100*(data.mdata['average']/data.mdata['length'])))
    print("Max-to-Min Slope: {0:-1.3f}, {1:-2.3f}%".format(data.mdata['minimum'] - data.mdata['maximum']/data.mdata['alphabetLength'], 100*(data.mdata['minimum'] - data.mdata['maximum'])/data.mdata['alphabetLength']/data.mdata['length']))
    print()

    output = new_stdout.getvalue()
    sys.stdout = old_stdout

    return output
    
if __name__ == "__main__":
   main(sys.argv[1:])