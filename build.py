from glob import glob
import json

def main():
    dictionary = {}
    words = set()
    canonical_outlines = {}
    for filename in glob('dictionaries/*.json'):
        if filename == 'dictionaries/main.json':
            continue

        if filename == 'dictionaries/lapwing.json':
            continue

        print(filename)
        with open(filename) as infile:
            for outline, word in json.load(infile).items():
                if outline in dictionary:
                    assert dictionary[outline] == word, f'Outline used twice: {outline} for {word} and {dictionary[outline]}'
                dictionary[outline] = word
                words.add(word)
                assert word not in canonical_outlines or canonical_outlines[word] == outline, f'Word does not have a canonical outline: {word} as outlines {outline} and {canonical_outlines[word]}'
                canonical_outlines[word] = outline

    with open('seagull.json', 'w') as outfile:
        json.dump(dictionary, outfile, indent=4)

    with open('dictionaries/main.json') as infile:
        for outline, word in json.load(infile).items():
            if outline not in dictionary and word not in words:
                dictionary[outline] = f'[Type # for {word!r}]'
                dictionary[outline + '/#'] = word
            elif outline not in dictionary: # but word is in words
                canonical_outline = canonical_outlines[word]
                dictionary[outline] = f'[Type {canonical_outline} for {word!r}]'

    with open('main.bypass.json', 'w') as outfile:
        json.dump(dictionary, outfile, indent=4)


if __name__ == "__main__":
    main()
