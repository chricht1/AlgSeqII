import numpy as np
import sys
from collections import defaultdict
import pandas as pd

lenAlphabet = 256


class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'



def getSuffixArray(text):
    suffixes = [(text[i:], i) for i in range(len(text))] # tuple (suffix, suffix start index)
    suffixes.sort()
    #suffixArray = [suffix[1] for suffix in suffixes]
    return np.array(suffixes)



def getBWT(suffixArray, text):
    bwt = []
    textLen = len(text)
    for idx in suffixArray:
        if idx == 0:
            bwt.append('$')
        else:
            bwt.append(text[idx-1]) 
    return np.array(bwt)



def getFirstAndRanks(bwt):

    # calc ranks
    counts = np.zeros(lenAlphabet, dtype=int)
    ranks = np.zeros((lenAlphabet, len(bwt)), dtype=int)
    for i, char in enumerate(bwt):
        if i > 0:    
            ranks[:,i] = ranks[:,i-1].copy()
        ranks[ord(char),i] += 1
        counts[ord(char)] += 1

    # calc first
    first = defaultdict(int)
    sortedBWT = np.sort(bwt)
    
    sortedBWTIdx = 0
    letter = sortedBWT[sortedBWTIdx]
    first[letter] = 0
    for _ in range(1, np.sum(counts > 0)):
        sortedBWTIdx += counts[ord(letter)]
        letter = sortedBWT[sortedBWTIdx]
        first[letter] = sortedBWTIdx

    return dict(first), ranks



def fm_idx_search(pattern, first, ranks, len_text):
    left = 0
    right = len(len_text) - 1
    for i in range(len(pattern)-1, -1, -1):
        char = pattern[i]
        try:
            left = first[char] + (ranks[ord(char), left-1] if left > 0 else 0)
            right = first[char] + ranks[ord(char), right] - 1
            #print(first[char], (ranks[ord(char), left-1] if left > 0 else 0), ranks[ord(char), right])
            #print(f'After processing char "{char}": left={left}, right={right}')
        except KeyError:
            return -1
        if left > right:
            return -1
        
    return left, right



def main():
    pattern = sys.argv[1]
    textFpath = 'text2.txt'
    with open(textFpath, 'r') as f:
        lines = f.readlines()
        #text = ''.join(lines)
        text = ''
        for line in lines:
            text += line.replace('\n', '')
        text = text.replace(' ', '_')
    text+='$'

    suffixes = getSuffixArray(text)
    suffixArray = suffixes[:,1].astype(int)
    bwt = getBWT(suffixArray, text)
    first, ranks = getFirstAndRanks(bwt)
    ranks_vis = np.int32([ranks[ord(char)] for char in bwt]).T

    df = pd.DataFrame({
        'Index': range(len(suffixArray)),
        '| Suffix': suffixes[:,0],
        '| Suffix Array': suffixArray,
        '| BWT': bwt,
        '| sorted BWT': np.sort(bwt),
        '| ranks: '+str([str(char) for char in bwt]): [ranks_vis[i,:] for i in range(ranks_vis.shape[0])]
    })
    with open('control_table.txt', 'w') as f:
        f.write(df.to_string(index=False))
        f.write('first: ' + str(first) + '\n')
    #print(df.to_string(index=False))
    #print('first: ', first)
    
    result = fm_idx_search(pattern, first, ranks, text)
    positions = suffixArray[result[0]:result[1]+1]
    if result == -1:
        print(f'Pattern "{pattern}" not found in text.')
    else:
        print(f'Pattern found at positions {positions} in text.')

    for pos in sorted(positions, reverse=True):
            text = text[:pos] + color.RED + text[pos:pos+len(pattern)] + color.END + text[pos+len(pattern):]

    print(text.replace('_', ' '))


if __name__ == "__main__":
    main()