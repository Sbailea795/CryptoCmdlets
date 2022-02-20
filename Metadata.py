from statistics import mean, median, stdev

class Metadata():
    
    def __init__(self, text, alphabet: str):
        keyFreqPair = []
        AlphaLength = 0
        for c in alphabet:
            keyFreqPair.append((c, 0))
        Frequency = dict(keyFreqPair)
        for c in text:
            if (c in alphabet):
                Frequency[c] += 1
                AlphaLength += 1
        self.string = text
        self.mdata = dict()
        self.mdata["alphabet"] = alphabet
        self.mdata["alphabetLength"] = len(alphabet)
        self.mdata["average"] = mean(Frequency.values())
        self.mdata["length"] = sum(Frequency.values())
        self.mdata['frequencies'] = list(Frequency.items())
        self.mdata["maximum"] = max(Frequency.values())
        self.mdata["medianVal"] = median(Frequency.values())
        self.mdata["minimum"] = min(Frequency.values())
        self.mdata["totalLength"] = len(text)
        self.mdata['stdDeviation'] = (stdev(Frequency.values()) / self.mdata['maximum'])
        self.mdata['relConcavity'] = (self.mdata['medianVal'] - ((self.mdata['maximum'] - self.mdata['minimum']) / 2)) / (self.mdata['maximum'] - self.mdata['minimum'])
        #return (list(Frequency.items()), mdata)

