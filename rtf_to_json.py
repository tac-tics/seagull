import json
import sys

dictionary = {}
filename = sys.argv[1]
with open(filename, 'rb') as infile:
    for line in infile:
        try:
            line = line.decode('ascii')
        except:
            continue
        # {\*\cxs REUS/KEU/ER}riskier
        if not line.startswith('{\*\cxs '):
            continue

        line = line[len('{\*\cxs '):].strip()
        idx = line.index('}')
        outline = line[:idx]
        word = line[idx+1:]

        if '\\' in word:
            continue

        dictionary[outline] = word

json.dump(dictionary, sys.stdout, indent=4)
print(file=sys.stdout)
