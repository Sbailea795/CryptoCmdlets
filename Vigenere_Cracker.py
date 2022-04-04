#!/usr/bin/env python
import argparse
import sys
import numpy
import math
from matplotlib import pyplot

from numpy.core.fromnumeric import size
from numpy.lib.function_base import append, blackman

englishScrawl = numpy.asarray(
                [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094,
                 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929,
                 0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150,
                 0.01974, 0.00074])
englishSignature = numpy.sort(englishScrawl)

englishAlphabet = "abcdefghijklmnopqrstuvwxyz"
sanatizedText = ''
keyMaxLength = 16#int(len(englishAlphabet)/2) 

def main(argv):

    #parser
    parser = argparse.ArgumentParser(
        description='Performs analysis on suspected Vignere-enciphered texts.')
    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('Text', type=str,
                        help='text to analyze', metavar='Text')
    group.add_argument('-lf', '--lengthFind', action='store_true', default=False,
                       help='Calculates a list of averaged signatures, and takes them over the alphabets signature and then generates a value')
    group.add_argument('-kf', '--keyFind', type=int,
                       help='Finds most probable letter for each coset of the text; key must be relatively prime to the modulus. By default the modulus is the length of the alphabet: 26', metavar='KeyLength')
    group.add_argument('-d', '--decode', type=str, help='Uses the key passed to decode to decrypt a vigenere cipher')
    parser.add_argument('-g', '--graph', action='store_true', default=False,
                        help='Displays signatures when solving for length and scrawls when solving for a key')

    #parse args
    try:
        args = parser.parse_args()
    except:
        sys.exit('Error: ArgumentParser failed to parse the arguments')
    sanatizedText = ''.join(ch.lower() for ch in args.Text if ch.isalpha())
    #determine length/key finder
    if(args.lengthFind): 
        lengthFinder(sanatizedText, args.graph)
    elif(args.decode is not None):
        decode(sanatizedText, str(args.decode).lower())
    else:
        keyFinder(sanatizedText, args.keyFind, args.graph)


def lengthFinder(text, graph):
    cosetComposite = numpy.zeros([keyMaxLength,keyMaxLength])
    allScrawls = []
    x = range(0, 26)
    #engFig, axE = pyplot.subplots()
    #axE.plot(x, englishSignature)
    #axE.set_title("Signature of English")
    fig, ax = pyplot.subplots(4,4)

    for cosets in range(1, keyMaxLength+1):
        cosetStrings = []
        signatures = []
        sanitizedText = text
        for i in range(0, cosets - len(text) % cosets):
            sanitizedText +=' '
        for offset in range(0,cosets):
            cosetStrings.append(list(sanitizedText[offset::(cosets)]))
        cosetsMatrix = numpy.resize(cosetStrings, (cosets, len(cosetStrings[0])))
        scrawls = numpy.zeros([cosets, len(englishAlphabet)])

        for offset in range(0, cosetsMatrix.shape[0]):
            keyFreqPair = dict((ch,0) for ch in englishAlphabet)
            blankCount = 0
            for col in cosetsMatrix[offset]:
                for ch in col:
                    if ch.isalpha(): keyFreqPair[ch] += 1
                    else : blankCount += 1
            scrawls[offset] = [keyFreqPair[letter]/(cosetsMatrix.shape[1] - blankCount) for letter in keyFreqPair]
        allScrawls.append(scrawls)
        for sets in scrawls:
            signature = numpy.sort(sets)
            V = ((numpy.sum(signature[int(size(sets)/2):]) + numpy.sum(signature[int(size(sets)/2-1):size(sets)-1]) - numpy.sum(signature[1:int(size(sets)/2)]) - numpy.sum(signature[:int(size(sets)/2-1)]) ) / 2 )
            signatures.append(V)
        signatures = numpy.pad(signatures, (0,keyMaxLength-len(signatures)),'constant', constant_values=(0))
        cosetComposite[cosets-1] = signatures
    averages = []
    for index in range(0, keyMaxLength):
        averages.append(numpy.sum(cosetComposite[index]/(index+1)))

    print(' l   ',end='')
    for cosets in range (1, keyMaxLength + 1): 
        print(' V{:02d}  '.format(cosets),end='')
    print('Average')
    offset = 1
    for cosets in cosetComposite:
        row = 0
        print('{:2d} | '.format(offset), end='')
        for keyLength in range(0, keyMaxLength):
            print('{:0.3f} '.format(cosets[keyLength]), end='')
        print('| {:0.3f}'.format(averages[offset-1]), end='')
        if averages[max(offset-2,0)] < averages[offset-1] > averages[min(offset, len(averages)-1)]: print(' !',end='')
        print()
        offset += 1

    for index in range(0, min(keyMaxLength,size(ax))):
        ax[int(index/4), index % 4].plot(x, englishSignature, label='English')
        ax[int(index/4), index % 4].set_title("key length {:2}".format(index+1))
        for j in range (0, index+1):
            ax[int(index/4), index % 4].plot(x, numpy.sort(allScrawls[index][j]), label='key length{:02}'.format(j))
    if graph: pyplot.show()
    print()

def decode(text, key):
    for index in range(0, len(text)):
        letterOffset = (ord(text[index]) - ord(englishAlphabet[0])) + (ord(englishAlphabet[0]) - ord(key[index % len(key)]))
        print( chr( ord(englishAlphabet[0]) + (letterOffset % len(englishAlphabet)) ).upper(), end='')

def keyFinder(text, keyLength, graph):
    print('Shift |', end='')
    for shift in range( 0, len(englishAlphabet)):
        print(' {:03d}  '.format(shift), end ='')
    print('\nletter|', end='')
    for ch in englishAlphabet:
        print('  {:1s}   '.format(ch), end ='')
    print()

    for cosets in range(keyLength, keyLength+1):
        cosetStrings = []
        sanitizedText = text
        for i in range(0, cosets - len(text) % cosets):
            sanitizedText +=' '
        for offset in range(0,cosets):
            cosetStrings.append(list(sanitizedText[offset::(cosets)]))
        cosetsMatrix = numpy.resize(cosetStrings, (cosets, len(cosetStrings[0])))
        scrawls = numpy.zeros([cosets, len(englishAlphabet)])

        for offset in range(0, cosetsMatrix.shape[0]):
            keyFreqPair = dict((ch,0) for ch in englishAlphabet)
            blankCount = 0
            for col in cosetsMatrix[offset]:
                for ch in col:
                    if ch.isalpha(): keyFreqPair[ch] += 1
                    else : blankCount += 1
            scrawls[offset] = [keyFreqPair[letter]/(cosetsMatrix.shape[1] - blankCount) for letter in keyFreqPair]
            #print('x')
        parallel = numpy.zeros([cosetsMatrix.shape[0], len(englishAlphabet)])
        for freqArrarys in range(0, scrawls.shape[0]):
            for offset in range(0,len(englishAlphabet)):
                shiftedScrawl =  numpy.concatenate( (scrawls[freqArrarys][offset:], scrawls[freqArrarys][:offset]) )
                parallel[freqArrarys][offset] = numpy.dot(shiftedScrawl, englishScrawl )

        for rows in range(0, parallel.shape[0]):
            print('i ={:02d} |'.format(rows+1),end='')
            for index in range(0, len(englishAlphabet)):
                if parallel[rows][index] == max(list(parallel[rows])):
                   print('{:1.3f}!'.format(parallel[rows][index]),end='')
                   print('',end='')
                else:
                    print('{:1.3f} '.format(parallel[rows][index]),end='')
            print()
        
        
        x = range(0, 26)
        engFig, axE = pyplot.subplots()
        axE.plot(x, englishScrawl)
        axE.set_title("Scrawl of English")
        fig, ax = pyplot.subplots()
        ax.set_title("Scrawls of Cosets")
        for j in range(0, scrawls.shape[0]):
            line = ax.plot(x, scrawls[j], label='Coset{:02}'.format(j+1))
            ax.legend()
        if graph: pyplot.show()
    
    for index in englishAlphabet:
        print('  {:2s} '.format(ch), end ='')

if __name__ == "__main__":
    main(sys.argv[1:])
