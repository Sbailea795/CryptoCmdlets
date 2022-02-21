import math
import sys
from Crypto_Utilities import lettersOnly
from Language import LowerAlphabet, LanguageScrawl

def main(argv):
    print(entropy[argv])

def entropy(text: str):
    text = lettersOnly(text)
    sum = 0
    for char in text:
        index = ord(char.lower()) - ord(LowerAlphabet[0])
        sum += LanguageScrawl[index] * math.log2(LanguageScrawl[index])
    sum /= len(text)
    return -sum

if __name__ == "__main__":
    main(sys.argv[1:])