from glob import glob
import json

def main():
    dictionary = {}
    for filename in glob('dictionaries/*.json'):
        if filename == 'dictionaries/main.json':
            continue

        print(filename)
        with open(filename) as infile:
            for outline, word in json.load(infile).items():
                if outline in dictionary:
                    assert dictionary[outline] == word, f'Words do not match for outline: {word}'
                dictionary[outline] = word

    with open('seagull.json', 'w') as outfile:
        json.dump(dictionary, outfile, indent=4)

    with open('dictionaries/main.json') as infile:
        for outline, word in json.load(infile).items():
            if outline not in dictionary:
                dictionary[outline] = f'[Type # for {word!r}]'
                dictionary[outline + '/#'] = word

    with open('main.bypass.json', 'w') as outfile:
        json.dump(dictionary, outfile, indent=4)


if __name__ == "__main__":
    main()
