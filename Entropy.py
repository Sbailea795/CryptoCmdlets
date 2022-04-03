import math, sys
from Language import Alphabet, LanguageScrawl

def main(argv):
    print(entropy[argv])

def entropy(text: str):
    sum = 0
    for char in text:   
        sum += LanguageScrawl.get(char) * math.log2(LanguageScrawl.get(char))
    sum /= len(text)
    return -sum

if __name__ == "__main__":
    main(sys.argv[1:])