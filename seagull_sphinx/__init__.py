import re
import json
from docutils import nodes


DICTIONARY = {}


with open('dictionaries/stened.json') as infile:
    dictionary = json.load(infile)
    for outline, word in dictionary.items():
        DICTIONARY[outline] = word

with open('dictionaries/basic_english_1000.json') as infile:
    dictionary = json.load(infile)
    for outline, word in dictionary.items():
        DICTIONARY[outline] = word

with open('seagull.json') as infile:
    dictionary = json.load(infile)
    for outline, word in dictionary.items():
        DICTIONARY[outline] = word

def doctree_resolved(app, doctree, fromdocname):
    pass


def steno_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    idx = text.index('<')
    idx2 = text.index('>')

    word = text[:idx].strip()
    outline = text[idx+1:idx2].strip()

    assert DICTIONARY[outline] == word, f'Outline {outline} does not correspond to word {word}'

    word_node = nodes.Text(' ' + word)
    outline_node = nodes.literal()
    outline_node += nodes.Text(outline)
    return [outline_node, word_node], []


def setup(app):
    app.add_role('steno', steno_role)
    app.connect('doctree-resolved', doctree_resolved)
