import math
import sys
from Crypto_Utilities import lettersOnly
from Language import Alphabet, LanguageScrawl

def main(argv):
    print(entropy[argv])

def entropy(text: str):
    text = lettersOnly(text)
    sum = 0
    for char in text.lower():
        sum += LanguageScrawl[char] * math.log2(LanguageScrawl[char])
    sum /= len(text)
    return -sum

if __name__ == "__main__":
    main(sys.argv[1:])