from datetime import datetime
import json
import os


BUILD_DIR = os.path.dirname(os.path.abspath(__file__))

def dump(dictionary):
    dt = datetime.now()
    created_datetime_string = dt.strftime('%Y-%m-%d_%H_%M_%S')
    dictionary["#K-T"] = created_datetime_string

    dictionary_name = 'seagull.json'
    with open(BUILD_DIR + "/" + dictionary_name, 'w') as outfile:
        json.dump(dictionary, outfile, indent=4)


def load(dictionary_name):
    with open(f'data/{dictionary_name}.json', 'r') as infile:
        return json.load(infile)


def merge(dictionary1, dictionary2):
    dictionary = dict(dictionary1)
    for outline, word in dictionary2.items():
        if outline not in dictionary:
            dictionary[outline] = word

    return dictionary


def filter(dictionary, pred):
    new_dictionary = {}
    for outline, word in dictionary.items():
        if pred(word):
            new_dictionary[outline] = word

    return new_dictionary


def filter_outline(dictionary, pred):
    new_dictionary = {}
    for outline, word in dictionary.items():
        if pred(outline):
            new_dictionary[outline] = word

    return new_dictionary


def make_stened_dict():
    stened_dict = load('stened')
    stened_dict = filter(stened_dict, lambda word: ' ' not in word)
    stened_dict = filter(stened_dict, lambda word: '{,}' not in word)
    stened_dict = filter_outline(stened_dict, lambda outline: not any(ch in outline for ch in '1234567890#'))

    # replace /-PB with /-EN
    new_dictionary = {}
    for outline, word in stened_dict.items():
        if outline.endswith('/-PB') and word.endswith('en'):
            new_outline = outline[:-3] + 'EPB'
        elif outline.endswith('/-PB') and word.endswith('in'):
            new_outline = outline[:-3] + 'EUPB'
        elif outline.endswith('/-PB') and word.endswith('ine'):
            new_outline = outline[:-3] + 'EUPB'
        elif outline.endswith('/-PB'):
            pass
            # print('Removing ', outline, word)
        else:
            new_dictionary[outline] = word

    return stened_dict


def main():
    dictionary = {}

    seagull_base_dict = load('seagull_base')
    stened_dict = make_stened_dict()

    dictionary = merge(dictionary, seagull_base_dict)
    dictionary = merge(dictionary, load('fingerspell'))
    dictionary = merge(dictionary, load('commands'))
    dictionary = merge(dictionary, load('punctuation'))
    dictionary = merge(dictionary, stened_dict)

    dump(dictionary)


if __name__ == '__main__':
    main()
