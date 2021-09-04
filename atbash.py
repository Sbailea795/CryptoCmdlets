#!/usr/bin/python

import argparse
import sys
import typing

def main(argv):

    #parse args
    parser = argparse.ArgumentParser(description='Performs a letter shift on text.')
    parser.add_argument('texts', nargs='+', type=str,
                        help='text strings to be shifted', metavar='Text')
    try:               
        args = parser.parse_args()
    except argparse.ArgumentError:
        sys.exit('Error Parsing Args')

    for sentence in getattr(args,"texts"):
        sentence = sentence.lower()
        #print(sentence)
        for c in sentence:
            #find index of letter in alphabet, increment, and mod by length. Add 97 and Upper() to offest to 'a'
            #print( alphabet.index(c.lower()) )
            if  97 <= ord(c) <= 122:
                print( chr((122 - ord(c.lower())) % 26 + 97).upper(), end='')
            else:
                print(c, end='')
        print('')

if __name__ == "__main__":
   main(sys.argv[1:])