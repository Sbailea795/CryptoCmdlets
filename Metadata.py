from statistics import mean, median, stdev
from Crypto_Utilities import sanitizeText

from Language import Alphabet, Language, LanguageScrawl

from Entropy import entropy

class Metadata():

    def __init__(self, text: str, alphabet: str, note: str):
        keyFreqPair = []
        AlphaLength = 0
        self.string = text
        self.languageReducedString = sanitizeText(text, Alphabet)
        self.note = note

        for c in alphabet:
            keyFreqPair.append((c, 0))
        Frequency = dict(keyFreqPair)
        for c in self.languageReducedString:
            if c in alphabet:
                Frequency[c] += 1
                AlphaLength += 1
        
        self.metadata = dict()
        self.metadata["alphabet"] = alphabet
        self.metadata["alphabetLength"] = len(self.metadata['alphabet'])
        self.metadata["average"] = mean(Frequency.values())
        self.metadata["length"] = sum(Frequency.values())
        self.metadata["entropy"] = entropy(self.languageReducedString)
        self.metadata['frequencies'] = list(Frequency.items())
        self.metadata["maximum"] = max(Frequency.values())
        self.metadata["medianVal"] = median(Frequency.values())
        self.metadata["minimum"] = min(Frequency.values())
        self.metadata["totalLength"] = len(text)
        self.metadata['stdDeviation'] = (stdev(Frequency.values()) / max(self.metadata['maximum'], 1) )
        self.metadata['relConcavity'] = (self.metadata['medianVal'] - ((self.metadata['maximum'] - self.metadata['minimum']) / 2)) / max(self.metadata['maximum'] - self.metadata['minimum'], 1)
    
    def statisticsToString(self):
        return "Concavity: {0:-5.5f} | ".format(self.metadata['relConcavity']) + \
            "Entropy: {0:-5.5f} ({1}) | ".format(self.metadata['entropy'], Language) + \
            "Median: {0:03}, {1:05.2f}% | ".format(self.metadata['medianVal'], 100*(self.metadata['medianVal']/self.metadata['length'])) + \
            "Average: {0:05.2f}, {1:05.2f}% | ".format(self.metadata['average'], 100*(self.metadata['average']/self.metadata['length'])) + \
            "Max-Min Slope: {0:-1.3f}, {1:-2.3f}% | ".format(self.metadata['minimum'] - self.metadata['maximum']/self.metadata['alphabetLength'], 100*(self.metadata['minimum'] - self.metadata['maximum'])/self.metadata['alphabetLength']/self.metadata['length']) + \
            "Note:{0: >17}".format(self.note)
