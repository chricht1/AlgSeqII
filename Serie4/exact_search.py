import numpy as np
import sys
from collections import defaultdict

lenAlphabet = 256

def getSuffixArray(text):
    suffixes = [(text[i:], i) for i in range(len(text))]
    suffixes.sort()
    suffixArray = [suffix[1] for suffix in suffixes]
    return np.array(suffixArray)


def getBWT(suffixArray, text):
    bwt = []
    textLen = len(text)
    for arr in suffixArray:
        pos = textLen - len(arr) - 1
        if pos < 0:
            bwt.append('$')
        else:
            bwt.append(text[pos]) 


def getFirstAndRanks(sortedBWT):
    sortedBWT = np.sort(sortedBWT)
    counts = defaultdict(int)
    first = defaultdict(int)
    ranks = defaultdict(np.zeros(len(sortedBWT)))
    for i, char in enumerate(sortedBWT):
        if first[char] == 0:
            first[char] = i
        counts[char] += 1
        ranks[]


def main():
    pattern = sys.argv[1]
    textFpath = 'text.txt'
    with open(textFpath, 'r') as f:
        lines = f.readlines()
        text = ''.join(lines)
    text+='$'
    print(text)

if __name__ == "__main__":
    main()