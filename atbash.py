#!/usr/bin/python

import argparse
import sys
import typing

def main(argv):

    #parse args
    parser = argparse.ArgumentParser(description='Performs a letter shift on text.')
    parser.add_argument('texts', nargs='+', type=str,
                        help='text strings to be shifted', metavar='Text')
    parser.add_argument('-a', '--alphabet', default='abcdefghijklmnopqrstuvwxyz',
                        nargs=1, help='provide an alphabet to shift over.', metavar='Alphabet')
    parser.add_argument('-s', '--shift', default=3, type=int,
                        help='shifts text by specified amount.', metavar='Shift')
    parser.add_argument('-r', '--range', default=1, type=int, choices=range(1, 100),
                        help='modifies shift to iterate over incrementing shifts r - 1 times.', metavar='Range')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Adds supplemental details. WARNING Will not pipe properly.')
    try:               
        args = parser.parse_args()
    except argparse.ArgumentError:
        sys.exit('Error Parsing Args')

    #assign args attributes to variables
    alphabet = getattr(args, "alphabet")
    shift = getattr(args, "shift")
    iterations = getattr(args, "range")
    sentenceCount = 0
    for i in range(iterations):
        for sentence in getattr(args,"texts"):
            sentenceCount +=1
            if getattr(args, "verbose"):
                print('text', sentenceCount, 'Shift by:', shift ,'',end='')
            for c in sentence:
                #find index of letter in alphabet, increment, and mod by length. Add 97 and Upper() to offest to 'a'
                #print( alphabet.index(c.lower()) )
                print( chr((alphabet.index(c.lower()) + shift) % len(alphabet) + 97).upper(), end='' )
            print('')
        shift += 1

if __name__ == "__main__":
   main(sys.argv[1:])