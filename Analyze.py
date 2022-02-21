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
    parser.add_argument('-s', '--signatures', action='store_true', default=False, help='Generates a signature pairing of the scrawl(s)')
    
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
    #takes text, cast to a Metadata
    for text in args.text:
        for alphabet in args.alphabet:
            combinations.append(Metadata(text, alphabet))
    
    #queues what is to be printed
    for combo in combinations:
        formatted.append(FormatToString(combo, "scrawl {:2}".format(label), False))
        if(args.signature): formatted.append(FormatToString(combo, "signature {:2}".format(label), True))
        label+=1
    printToOut(args.columns, formatted)


#prints all the combinations of text * alphabets
def printToOut(width, combinations: list):
    
    while(len(combinations) % width != 0):
        combinations.append(' ')
    texts = []
    for combo in combinations:
        texts.append(str(combo).splitlines())
    #calculates which texts are on the row
    for index in range(0, len(texts), width):
        lines=[]
        row = texts[index:index+width]
        
        #finds the max height
        for i in range(0,len(row)):
            lines.append(len(max(row, key=len)))
        gap = ' '
        #prints a row
        for line in range(0, max(lines)):
            for item in range(0, width):
                if (line < len(row[item])):
                    print(row[item][line].ljust(len(row[item][0])), end='')
                    print(gap.center(10), end='')
                else:
                    print(' '.ljust(len(row[item][0])), end='')
                    print(gap.center(10), end='')
            print()

#builds a string/graph out of the meta data
def FormatToString(data: Metadata, label: str, signature: bool):
    leftBorder = 17
    width = 3
    gap = ' '
    #the graph is as tall as the alphabet. Resolution reportions it to fit with the alphabet size
    #if the grapgh is very flat, a floor of 1/2 will prevent over-relativizing the data
    resolution = max(((100*data.metadata['maximum']/data.metadata['length']) / data.metadata['alphabetLength']), 1/2)

    if signature: sortKey = 1
    else: sortKey = 0

    #prints to a string
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout

    #prints the top axis of the graph
    print(label.center(leftBorder , '_'), end='')
    for char in sorted(data.metadata['frequencies'], key=lambda x: x[sortKey]):
        print(char[0].center(width, '_'), end='')
    print()

    #prints body of the graph
    for i in range(0, int(data.metadata['alphabetLength'])):
        line = '|'  
        background = ' ' 
        print("{0} : {1:03}, {2:06.3f}% ".format( data.metadata['frequencies'][i][0], data.metadata['frequencies'][i][1], 100*data.metadata['frequencies'][i][1]/data.metadata['length'] ), end='')
        for char in sorted(data.metadata['frequencies'], key=lambda x: x[sortKey]):
            
            if i * resolution <= 100*data.metadata['medianVal']/data.metadata['length'] < (i + 1) * resolution:
                background = '='
            elif i * resolution <= 100*data.metadata['average']/data.metadata['length']< (i + 1) * resolution:
                background = '-'

            if (100*char[1]/data.metadata['length']) > i * resolution:
                print(line.center(width, background), end='')
            else:
                print(background.center(width, background), end='')
        print()
    
    #statistics on the graph
    print("Tick Resolution: {0:5.5}".format(resolution))
    print(data.statisticsToString().replace(' | ', '\n'))
    print()

    output = new_stdout.getvalue()
    sys.stdout = old_stdout

    return output
    
if __name__ == "__main__":
   main(sys.argv[1:])