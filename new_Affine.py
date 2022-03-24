#!/usr/bin/env python

import argparse
import sys
from Crypto_Utilities import sanitizeText
from Metadata import Metadata
from Language import Alphabet

def main(argv):
    #parse args
    parser = argparse.ArgumentParser(description='Performs a letter shift on text.')
    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('text', nargs='*', type=str,
                        help='text strings to be affined', metavar='text')
    parser.add_argument('-a', '--alphabet', default=Alphabet, type=str,
                        help='provide an alphabet to shift over.', metavar='alphabet')
    parser.add_argument('-c', '--constant', default=0, type=int,
                        help='Constant of the Affine; default is 0 and thus it becomes a decimation cipher', metavar='constant')
    group.add_argument('-k', '--key', type=int, 
                        help='key of the Affine; key must be relatively prime to the modulus. By default the modulus is the length of the alphabet: 26.', metavar='key') 
    parser.add_argument('-m', '--modulo', default=-1, type=int,
                        help='Modulo of the Affine; it will take the alphabet length, unless otherwise specified', metavar='modulo')
    group.add_argument('-b', '--brute', action='store_true', help='Brute Froces across all values of the affine')
    
    #Error try-catch
    try:               
        args = parser.parse_args()
        args.text[:] = [sanitizeText(text) for text in args.text]
        metaTexts = []
        for text in args.text:
            metaTexts.append(Metadata(text, args.alphabet))
        if (args.modulo == -1):
            args.modulo = len(args.alphabet)
    except:
        sys.exit('Error: ArgumentParser failed to parse the arguments')
    
    
    affines = []
    for texts in metaTexts:
        affines.append(affine(args.constant, args.key, args.modulo, texts.string, texts.metadata['alphabet']))
    

def brute(text: str, alphabet: list, modulo: int)
    affined = ''
    return affined
        
def affine(offset: int, multiplier: int, modulo: int, text: str, alphabet: list):
    affined = ''    
    for ch in text:  
        num = alphabet.index(ch)
        affined += (num * multiplier + offset) % modulo
    return affined





    
if __name__ == "__main__":
   main(sys.argv[1:])