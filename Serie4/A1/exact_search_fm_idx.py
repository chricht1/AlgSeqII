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
    counts = defaultdict(int)
    ranks = defaultdict(defaultdict(int))
    for i, char in enumerate(bwt):
        if i > 0:    
            ranks[i] = ranks[i-1].copy()
        ranks[i][ord(char)] += 1
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
    itertext = f'pattern search\n###############\nstart with empty pattern\nL: {left}\t R: {right}\n'
    for i in range(len(pattern)-1, -1, -1):        
        char = pattern[i]
        itertext += f'Iteration: {len(pattern)-1-i}\n---------------------\ncurrent pattern suffix: {pattern[i:]}\n'
        try:
            left = first[char] + (ranks[ord(char), left-1] if left > 0 else 0)
            right = first[char] + ranks[ord(char), right] - 1
            #print(first[char], (ranks[ord(char), left-1] if left > 0 else 0), ranks[ord(char), right])
            #print(f'After processing char "{char}": left={left}, right={right}')
            itertext += f'L+: {left}\t R+: {right}\n'
        except KeyError:
            return -1, itertext
        if left > right:
            return -1, itertext
    itertext += '\n'    
    return (left, right), itertext



def main():
    pattern = sys.argv[1]
    if len(sys.argv) == 3:
        text = sys.argv[2]
    else:
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
        '| sorted BWT (F)': np.sort(bwt),
        '| ranks: '+str([str(char) for char in bwt]): [ranks_vis[i,:] for i in range(ranks_vis.shape[0])]
    })
    #print(df.to_string(index=False))
    #print('first: ', first)   
    result, itertext = fm_idx_search(pattern, first, ranks, text)    
    result_text = ''
    org_text = text    
    if result == -1:
        result_text = f'Pattern "{pattern}" not found in text: '
        print(result_text)
        print(org_text)
    else:
        positions = suffixArray[result[0]:result[1]+1]
        result_text = f'Pattern found at positions {np.sort(positions).tolist()} in text: '
        print(result_text)            
        for pos in sorted(positions, reverse=True):
                text = text[:pos] + color.RED + text[pos:pos+len(pattern)] + color.END + text[pos+len(pattern):]
        print(text.replace('_', ' '))    

    with open('output.txt', 'w') as f:
        f.write(df.to_string(index=False))
        f.write('\nfirst: ' + str(first) + '\n')
        f.write(itertext)
        f.write(result_text + f'{org_text}')


if __name__ == "__main__":
    main()