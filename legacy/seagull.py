from pathlib import Path
import json
import urllib


DICTIONARY_URLS = [
    'https://raw.githubusercontent.com/tac-tics/seagull/master/seagull.json',
    'https://raw.githubusercontent.com/tac-tics/seagull/master/dictionaries/commands.json',
    'https://raw.githubusercontent.com/tac-tics/seagull/master/dictionaries/punctuation.json',
    'https://raw.githubusercontent.com/tac-tics/seagull/master/dictionaries/stened.json',
]

FINGERSPELL_URL = 'https://raw.githubusercontent.com/tac-tics/seagull/master/fingerspelling.json'


DICTIONARY = {}
FINGERSPELLING = {}

# Length of the longest supported key (number of strokes).
LONGEST_KEY = 1


def load_dictionary(dictionary_url):
    global LONGEST_KEY
    with urllib.request.urlopen(dictionary_url) as infile:
        dictionary = json.load(infile)
        for outline, word in dictionary.items():
            LONGEST_KEY = max(LONGEST_KEY, len(outline.split('/')))
            DICTIONARY[outline] = word


def load_dictionaries():
    for dictionary_json in reversed(DICTIONARY_URLS):
        load_dictionary(dictionary_json)

    with urllib.request.urlopen(FINGERSPELL_URL) as infile:
        dictionary = json.load(infile)
        for letter, stroke in dictionary.items():
            FINGERSPELLING[stroke] = '{>}{&' + letter + '}'
            FINGERSPELLING[f'{stroke}*'] = '{&' + letter.upper() + '}'


load_dictionaries()

MODE = 'dictionary'

def outline_from_key(key):
    strokes = []
    for k in key:
        if k == '*' and strokes:
            strokes.pop()
        else:
            strokes.append(k)
    return '/'.join(strokes)


# Lookup function: return the translation for <key> (a tuple of strokes)
# or raise KeyError if no translation is available/possible.
def lookup(key):
    global MODE
    assert len(key) <= LONGEST_KEY
    assert '#' not in key
    outline = outline_from_key(key)


    if outline == '#*':
        MODE = 'dictionary'
        raise KeyError

    if MODE == 'dictionary':
        if outline == '#':
            MODE = 'fingerspelling'
            raise KeyError

        elif outline == 'TPH':
            try:
                load_dictionaries()
                return '[Success loading dictionaries]'
            except:
                return '[Error loading dictionaries]'

        return DICTIONARY[outline]

    elif MODE == 'fingerspelling':
        return FINGERSPELLING[outline]

    raise KeyError


# Optional: return an array of stroke tuples that would translate back
# to <text> (an empty array if not possible).
def reverse_lookup(text):
    return []
