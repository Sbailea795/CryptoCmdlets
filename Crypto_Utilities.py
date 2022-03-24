#!/usr/bin/env python
import sys
from tokenize import Whitespace
import numpy
import math
#import XOR
from Language import Alphabet
from dataclasses import dataclass, field

Scrawl = numpy.asarray(
                [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094,
                 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929,
                 0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150,
                 0.01974, 0.00074])
Signature = numpy.sort(Scrawl)
lowerAlphabet = "abcdefghijklmnopqrstuvwxyz"
upperAlphabet = lowerAlphabet.upper()

def main(argv):
    entropy("eeee")
    print("This script current has no main; as it stands, this is meant to serve as a collection of common fuctions and utilties for crypto")

def sanitizeText(text):
    for char in text.lower():
        if (char not in Alphabet) or (not char.isspace()):
            text = text.replace(char, '')
    return text.lower()

def lettersOnly(text):
    for char in text:
        if (not char.isalpha()):
            text = text.replace(char, '')
    return text

def sanitizeBinaryText(text):
    output = ''
    for char in text:
        if char == '0':
            output += char
        elif char == '1':
            output += char
    return output

def zeroizedIntToChar(num) -> chr:
    return chr(ord(lowerAlphabet[0]) + num).upper()

def charToZeroBasedInt(ch):
    return (ord(ch) - ord(lowerAlphabet[0]))

def charToBinary(ch):
    return bin(ord(ch))[2:]

def charTo7ASCII(ch):
    return charToBinary(ch)

def ASCII8to7(string):
    output = ''
    for n in range(0,len(string), 8):
        output.join(list(string)[n+1:n+7])
    return output

def charTo8ASCII(ch):
    return '0' + charToBinary(ch)

def entropy(text):
    sum = 0
    for char in text:
        index = ord(char) - ord(lowerAlphabet[0])
        sum += Scrawl[index] * math.log2(Scrawl[index])
    sum /= len(text)
    return -sum

def FeistelFunction(binary, key, blockSize) -> str:
    outString = ''
    if (blockSize == 2):
        return str((1 + int(key[0]) * int(binary[0])**2 + int(key[1]) * int(binary[0]) * int(binary[1])) % 2) + str((int(key[0])**2 * int(binary[0]) * int(binary[1]) + int(key[2]) * int(binary[1])**2) % 2)
    elif (blockSize == 4):
        for block in range(0, len(binary), 4):
            outString += str(binary[block + 2:block + 4]) + str(XOR.XOR(binary[block + 0:block + 2], FeistelFunction(binary[block + 2:block + 4], key, 2)))
    return outString

def sBox(binary):
    if (binary == '000'):
        return '11'
    elif (binary == '001'):
        return '01'
    elif (binary == '010'):
        return '00'
    elif (binary == '011'):
        return '10'
    elif (binary == '100'):
        return '01'
    elif (binary == '101'):
        return '00'
    elif (binary == '110'):
        return '11'
    elif (binary == '111'):
        return '10'

def enciphRound(binary, key, rounds):
    out = ''
    t = sBox(XOR.XOR(binary[2:4]+binary[2], key))
    u = XOR.XOR(t, binary[0:2])
    out = binary[2:4]+u
    if rounds > 1: 
        return (enciphRound(out, key, rounds-1))
    else:
        return out

def Leftmost(binary, size):
    return binary[:size]

def shiftRegister(binary, fill):
    return (binary[int(len(binary)/2):] + fill)

@dataclass
class BrutesBook:

    cipher: str
    BruteEntropies: dict = field(default_factory=dict)

    def __init__(self, cipher:str):
        self.cipher = cipher
        self.BruteEntropies = {}
    def print(self):
        print("String | Entropy")
        print(*sorted(self.BruteEntropies.items(), key=lambda x:x[1], reverse=True), sep='\n')

if __name__ == "__main__":
   main(sys.argv[1:])