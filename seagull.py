from pathlib import Path
import json
import urllib


DICTIONARY_URLS = [
    'https://raw.githubusercontent.com/tac-tics/seagull/master/seagull.json',
    'https://raw.githubusercontent.com/tac-tics/seagull/master/dictionaries/punctuation.json',
    'https://raw.githubusercontent.com/tac-tics/seagull/master/fingerspelling.json',
    'https://raw.githubusercontent.com/tac-tics/seagull/master/dictionaries/stened.json',
]


DICTIONARY = {}

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

load_dictionaries()

# Lookup function: return the translation for <key> (a tuple of strokes)
# or raise KeyError if no translation is available/possible.
def lookup(key):
    assert len(key) <= LONGEST_KEY
    outline = '/'.join(key)

    word = DICTIONARY.get(outline)
    if word is None:
        raise KeyError
    else:
        return word


# Optional: return an array of stroke tuples that would translate back
# to <text> (an empty array if not possible).
def reverse_lookup(text):
    return []
