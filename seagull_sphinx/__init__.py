import re
import time
import sys
import json
from docutils import nodes


DICTIONARY = {}


def error_on_duplicate_keys(ordered_pairs):
    # eg:
    # json.loads(
    #     '{"x": 1, "x": 2}',
    #     object_pairs_hook=array_on_duplicate_keys,
    # )
    result = {}
    for k, v in ordered_pairs:
        if k not in result:
            result[k] = v
        else:
            raise Exception(f'Multiple entries with single key: {k!r}')
    return result


#with open('dictionaries/stened.json') as infile:
#    dictionary = json.load(infile)
#    for outline, word in dictionary.items():
#        DICTIONARY[outline] = word
#
#with open('dictionaries/basic_english_1000.json') as infile:
#    dictionary = json.load(infile)
#    for outline, word in dictionary.items():
#        DICTIONARY[outline] = word

with open('seagull.json') as infile:
    dictionary = json.load(infile, object_pairs_hook=error_on_duplicate_keys)
    for outline, word in dictionary.items():
        DICTIONARY[outline] = word


ERRORS = []


def doctree_resolved(app, doctree, fromdocname):
    if len(ERRORS) > 0:
        for error in ERRORS:
            print(error, file=sys.stderr)

        raise Exception('There were {len(ERRORS)} errors in the project.')


def steno_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    idx = text.index('<')
    idx2 = text.index('>')

    word = text[:idx].strip()
    outline = text[idx+1:idx2].strip()

    if outline != '' and DICTIONARY.get(outline) != word:
        ERRORS.append(f'Missing "{outline}": "{word}",')

    if outline == '':
        outline = '?????????'

    word_node = nodes.Text(' ' + word)
    outline_node = nodes.literal()
    outline_node += nodes.Text(outline)
    return [outline_node, word_node], []


def setup(app):
    app.add_role('steno', steno_role)
    app.connect('doctree-resolved', doctree_resolved)
