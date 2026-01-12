import re

def readSequences(fpath):
    with open(fpath, 'r') as f:
        fcontent = f.read()
    seqs = re.split(r'>[ -~]*\n', fcontent) # matches any printable ASCII character (space through ~)
    seqs.pop(0)
    seqs = [t.strip().replace('\n', '') for t in seqs]
    return seqs