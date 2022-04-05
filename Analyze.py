#!/usr/bin/env python

import argparse
import textwrap
from collections import OrderedDict
import io
import sys
from Crypto_Utilities import sanitizeText
from Metadata import Metadata
from Language import Alphabet

leftBorder = 18
width = 3
gap = ' '

def main(argv):  
    #parse args
    parser = argparse.ArgumentParser(description='Analysis on frequency of letters in a given text')
    group = parser.add_mutually_exclusive_group()

    parser.add_argument('text', nargs='*', type=str,
                        help='text to be analyzed', metavar='text')
    parser.add_argument('-n', '--noGraphs', action='store_true', help='will skip displaying of graphs.')
    parser.add_argument('-c', '--columns', default='1', type=int, choices=[1,2,3,4],
                        help='How many columns to display the data.mdata in', metavar='Columns')
    parser.add_argument('-a', '--alphabet', default=Alphabet, type=str, help='Alphabet used to analyze the text.', metavar='Alphabet')
    group.add_argument('-l', '--lowerOnly', action='store_true', help='Cast text to lowercase and analyze only the lowercase letters.')
    group.add_argument('-u', '--upperOnly', action='store_true', help='Cast text to uppercase and analyze only the uppercase letters.')
    parser.add_argument('-s', '--signatures', action='store_true', default=False, help='Generates a signature pairing of the scrawl(s).')
    
    #Error try-catch
    try:               
        args = parser.parse_args()
        #args.text[:] = [sanitizeText(text, args.alphabet) for text in args.text]
        # -lu arg formatting
        if (args.lowerOnly is True):
            args.text[:] = [a.lower() for a in args.text]
            args.alphabet[:] = [a.lower() for a in args.alphabet]
            #Orders Alphabet and preserves unique entries in occuring order; cuts extraneous case's entries
            args.alphabet[:] = [''.join(OrderedDict.fromkeys(a).keys()) for a in args.alphabet]
        elif (args.upperOnly is True):
            args.text[:] = [a.upper() for a in args.text]
            args.alphabet[:] = [a.upper() for a in args.alphabet]
            #Orders Alphabet and preserves unique entries in occuring order; cuts extraneous case's entries
            args.alphabet[:] = [''.join(OrderedDict.fromkeys(a).keys()) for a in args.alphabet]
        
    except argparse.ArgumentError:
        sys.exit('Error: ArgumentParser failed to parse the arguments')
    
    label = 1
    combinations = []
    formatted = []
    #takes text, cast to a Metadata
    for text in args.text:
        #for alphabet in args.alphabet:
            combinations.append(Metadata(text, args.alphabet, text))
    
    #queues what is to be printed
    for combo in combinations:
        formatted.append(FormatToString(combo, "scrawl {:02}".format(label), False, args.noGraphs))
        if(args.signatures): 
            formatted.append(FormatToString(combo, "signature {:02}".format(label), True, args.noGraphs))
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
def FormatGraph(data: Metadata, label: str, signature: bool):
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
    for char in sorted(data.metadata['frequencies'], key=lambda x: x[sortKey], reverse=True):
        print(char[0].center(width, '_'), end='')
    print()

    #prints body of the graph
    for i in range(0, int(data.metadata['alphabetLength'])):
        line = '|'  
        background = ' ' 
        print("{0} : {1:04}, {2:06.3f}% ".format( data.metadata['frequencies'][i][0], data.metadata['frequencies'][i][1], 100*data.metadata['frequencies'][i][1]/data.metadata['length'] ), end='')
        for char in sorted(data.metadata['frequencies'], key=lambda x: x[sortKey], reverse=True):
            
            if i * resolution <= 100*data.metadata['medianVal']/data.metadata['length'] < (i + 1) * resolution:
                background = '='
            elif i * resolution <= 100*data.metadata['average']/data.metadata['length']< (i + 1) * resolution:
                background = '-'

            if (100*char[1]/data.metadata['length']) > i * resolution:
                print(line.center(width, background), end='')
            else:
                print(background.center(width, background), end='')
        print()

    output = new_stdout.getvalue()
    sys.stdout = old_stdout

    return output


def FormatToString(data: Metadata, label: str, signature: bool, noGraphs: bool):
    #the graph is as tall as the alphabet. Resolution reportions it to fit with the alphabet size
    #if the grapgh is very flat, a floor of 1/2 will prevent over-relativizing the data
    resolution = max(((100*data.metadata['maximum']/data.metadata['length']) / data.metadata['alphabetLength']), 1/2)

    #prints to a string
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    for lines in textwrap.wrap(data.string, leftBorder + width * data.metadata['alphabetLength'], max_lines=5):
        print(lines.ljust(leftBorder + width * data.metadata['alphabetLength']))
    #print((textwrap.wrap(data.string, leftBorder + width * data.metadata['alphabetLength'], max_lines=5)).ljust(leftBorder + width * data.metadata['alphabetLength']))
    print()
    if noGraphs is False:
        print(FormatGraph(data, label, signature))

    #statistics on the graph
    if (leftBorder + width * data.metadata['alphabetLength'] > 2 * leftBorder):
        print(textwrap.fill("Tick Resolution: {0:5.5} | ".format(resolution) + data.statisticsToString(), leftBorder + width * data.metadata['alphabetLength']))
    else:
        print("Tick Resolution: {0:5.5}\n".format(resolution) + data.statisticsToString().replace(' | ', '\n'))
    print()

    output = new_stdout.getvalue()
    sys.stdout = old_stdout

    return output
    
if __name__ == "__main__":
   main(sys.argv[1:])