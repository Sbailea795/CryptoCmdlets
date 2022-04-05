#!/usr/bin/env python

import argparse
from math import gcd
import sys
from Crypto_Utilities import sanitizeText
from Metadata import Metadata
from Language import Alphabet
import Analyze
def main(argv):
    #parse args
    parser = argparse.ArgumentParser(description='Performs a letter shift on text.')
    #group = parser.add_mutually_exclusive_group(required=True)
    groups = parser.add_argument_group()
    group = parser.add_mutually_exclusive_group()
    parser.add_argument('text', nargs='*', type=str,
                        help='text strings to be affined', metavar='text')
    parser.add_argument('-a', '--alphabet', default=Alphabet, type=str,
                        help='provide an alphabet to shift over.', metavar='alphabet')
    groups.add_argument('-c', '--constant', default=0, type=int,
                        help='Constant of the Affine; default is 0 and thus it becomes a decimation cipher', metavar='constant')
    groups.add_argument('-k', '--key', type=int, 
                        help='key of the Affine; key must be relatively prime to the modulus. By default the modulus is the length of the alphabet: 26.', metavar='key') 
    group.add_argument('-b', '--brute', action='store_true', help='Brute Froces across all values of the affine')
    group.add_argument('-e', '--encrypt', action='store_true', help='encrypt with affine')
    group.add_argument('-d', '--decrypt', action='store_true', help='decrypt with affine')

    #Error try-catch
    try:  git             
        args = parser.parse_args()
        if not(args.brute or args.encrypt or args.decrypt):
            sys.exit('Error: ArgumentParser failed to parse the arguments')
        args.text[:] = [sanitizeText(text, args.alphabet) for text in args.text]
        metaTexts = []
        for text in args.text:
            metaTexts.append(Metadata(text, args.alphabet, "text"))
    except:
        sys.exit('Error: ArgumentParser failed to parse the arguments')
    
    if(args.brute):
        for texts in metaTexts:
            bruteList = brute(texts.languageReducedString, texts.metadata["alphabet"])
        bruteList.sort(key=cust_key, reverse=True)
        string = ''
        for index in range(0, 10):
            string +=Analyze.FormatToString(bruteList[index], bruteList[index].note, False, False)
        print("\n"+string)
    elif(args.encrypt):
        affines = []
        test = ''
        for texts in metaTexts:
            affines.append(affine(args.constant, args.key, len(args.alphabet), texts.string, texts.metadata['alphabet']))
            test += Analyze.FormatToString(affines[-1], 'test', False, False)
        print("\n"+test)
    elif(args.decrypt):
        affines = []
        test = ''
        for texts in metaTexts:
            affines.append(deaffine(args.constant, args.key, len(args.alphabet), texts.string, texts.metadata['alphabet']))
            test += Analyze.FormatToString(affines[-1], 'test', False, False)
        print("\n"+test)
    
def brute(text: str, alphabet: list):
    modulo = len(alphabet)
    affines = []
    for multi in range(1, modulo):
        for offset in range(0, modulo):
            if gcd(modulo,multi) == 1:
                affines.append(deaffine(offset, multi, modulo, text, alphabet))
    return affines
        
def affine(offset: int, multiplier: int, modulo: int, text: str, alphabet: str):
    affined = ''    
    for ch in text:  
        num = alphabet.index(ch)
        affined += alphabet[((num * multiplier + offset) % modulo)]
    return Metadata(affined, alphabet, "Affine: " + str(multiplier) +', '+ str(offset) +', '+ str(modulo))

def deaffine(offset: int, multiplier: int, modulo: int, text: str, alphabet: str):
    affined = ''    
    for ch in text:  
        num = alphabet.index(ch)
        affined += alphabet[(multiplier * (num - offset) % modulo)]
    return Metadata(affined, alphabet, "Affine: " + str(multiplier) +', '+ str(offset) +', '+ str(modulo))



def cust_key(data: Metadata):
    return data.metadata["entropy"]

    
if __name__ == "__main__":
   main(sys.argv[1:])