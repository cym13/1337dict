#!/usr/bin/env python3
#
# Copyright 2017 Cédric Picard
#
# LICENSE
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
# END_OF_LICENSE


"""
Generate 1337speak based password dictionary

Usage: 1337dict [-h] [options] WORD...

Options:
    -h, --help          Print this help and exit.
    -p, --permute       Enable permutations of words
    -n, --number        Outputs the number of variations
    -m, --min LEN       Do not generate passwords shorter than LEN
                        Defaults to 0
    -M, --max LEN       Do not generate passwords longer than LEN
                        Defaults to 32
    -s, --skip N        Skip the first N entries

Arguments:
    WORD    Word to be used present in the password
            1337dict generates all possible combinations of those words
"""

import sys
import docopt
import itertools
from math      import factorial
from itertools import chain

try:
    import pytest
except ImportError:
    pass


letter_num = {
            'a': '4',
            'e': '3',
            'g': '9',
            'i': '1',
            'l': '1',
            'o': '0',
            's': '5',
            't': '7'
        }


letter_sym = {
            'a': '@',
            'e': '€',
            'i': '!',
            's': '$',
            't': '+'
        }


def leet_letter(letter):
    yield letter.lower()

    if letter.isalpha():
        yield letter.upper()

    if letter in letter_num:
        yield letter_num[letter]

    if letter in letter_sym:
        yield letter_sym[letter]


def test_leet_letter():
    assert list(leet_letter('a')) == ['a', 'A', '4', '@']
    assert list(leet_letter('b')) == ['b', 'B']
    assert list(leet_letter('1')) == ['1']
    assert list(leet_letter('@')) == ['@']


def leet_word(word):
    if len(word) == 0:
        return ''

    if len(word) == 1:
        yield from leet_letter(word)

    for w in leet_word(word[:-1]):
        for l in leet_letter(word[-1]):
            yield w + l


def test_leet_word():
    assert (list(leet_word('ba1:')) ==
            ['ba1:', 'bA1:', 'b41:', 'b@1:',
             'Ba1:', 'BA1:', 'B41:', 'B@1:'])


def gen_passwords(wordset, minlen, maxlen, permute, skip):
    combinations, skip = drop_combinations(skip, wordset, permute)

    variations = []

    for combination in combinations:
        if (len(''.join(combination)) < minlen
         or len(''.join(combination)) > maxlen):
            continue

        if permute:
            permutations, skip = drop_permutations(skip, combination)

            for permutation in permutations:
                variations = chain(variations, leet_word(''.join(permutation)))
        else:
            variations = chain(variations, leet_word(''.join(combination)))

    try:
        drop(skip, variations)
    except AttributeError:
        return
    yield from variations


def test_gen_passwords():
    assert (list(gen_passwords(["ba1:"], 0, 4, False, 0)) ==
            list(leet_word('ba1:')))

    assert (list(gen_passwords(["ba1:"], 0, 4, True, 0)) ==
            list(leet_word('ba1:')))

    assert (list(gen_passwords(["b", "c"], 0, 2, False, 0)) ==
            ['b', 'B', 'c', 'C', 'bc', 'bC', 'Bc', 'BC'])

    assert (list(gen_passwords(["b", "c"], 0, 1, False, 0)) ==
            ['b', 'B', 'c', 'C'])

    assert (list(gen_passwords(["b", "c"], 2, 2, False, 0)) ==
            ['bc', 'bC', 'Bc', 'BC'])

    assert (list(gen_passwords(["b", "c"], 0, 2, True, 0)) ==
            ['b',  'B',  'c',  'C',
             'bc', 'bC', 'Bc', 'BC',
             'cb', 'cB', 'Cb', 'CB'])

    assert (list(gen_passwords(["b", "c"], 0, 2, True, 8)) ==
             ['cb', 'cB', 'Cb', 'CB'])



def variations_number(word):
    result = 1
    for letter in word:
        result *= ((2 if letter.isalpha() else 1)
                + (letter in letter_num)
                + (letter in letter_sym))

    return result


def test_variations_number():
    assert variations_number('a') == 4
    assert variations_number('b') == 2
    assert variations_number('1') == 1
    assert variations_number('@') == 1


def permutations_number(combination, permute):
    return factorial(len(combination)) if permute else 1


def test_permutation_number():
    assert permutations_number(['b', 'c'], False) == 1
    assert permutations_number(['b', 'c'], True)  == 2


def possibilities_number(wordset, permute):
    result = 0

    for i in range(len(wordset)):
        for combination in itertools.combinations(wordset, i+1):
            result += (permutations_number(combination, permute)
                     * variations_number(''.join(combination)))

    return result


def test_possibilities_number():
    assert possibilities_number(['haha'],     False) == 64
    assert possibilities_number(['bcbc'],     False) == 16
    assert possibilities_number(['ha', 'bc'], False) == 44
    assert possibilities_number(['ha', 'bc'], True)  == 76


def drop_combinations(skip, wordset, permute):
    if skip == 0:
        combinations = []
        for i in range(len(wordset)):
            combinations = chain(combinations,
                                 itertools.combinations(wordset, i+1))
        return combinations, 0

    tmp       = 0
    result    = []
    last_skip = skip

    for i in range(len(wordset)):
        combinations = itertools.combinations(wordset, i+1)

        for combination in combinations:
            tmp += (permutations_number(combination, permute)
                  * variations_number(''.join(combination)))

            if tmp > skip:
                result = chain(result, [combination], combinations)
            else:
                last_skip = tmp

    return result, last_skip


def test_drop_combinations():
    wordset = ["ha", "bc"]

    combinations, iteration = drop_combinations(0, wordset, False)
    assert list(combinations) == [('ha',), ('bc',), ('ha', 'bc')]
    assert iteration == 0

    combinations, iteration = drop_combinations(0, wordset, True)
    assert list(combinations) == [('ha',), ('bc',), ('ha', 'bc')]
    assert iteration == 0

    combinations, iteration = drop_combinations(2, wordset, False)
    assert list(combinations) == [('ha',), ('bc',), ('ha', 'bc')]
    assert iteration == 2

    combinations, iteration = drop_combinations(13, wordset, True)
    assert list(combinations) == [('ha', 'bc')]
    assert iteration == 12


def drop_permutations(skip, combination):
    varnum       = variations_number(''.join(combination))
    permutations = itertools.permutations(combination)

    for i in range(skip // varnum):
        permutations.__next__()

    return permutations, skip % varnum


def test_drop_permutations():
    combination = ('ha', 'bc', 'de')
    varnum      = variations_number(''.join(combination))

    permutations, iteration = drop_permutations(0, combination)
    assert (list(permutations) ==
            [('ha', 'bc', 'de'), ('ha', 'de', 'bc'), ('bc', 'ha', 'de'),
             ('bc', 'de', 'ha'), ('de', 'ha', 'bc'), ('de', 'bc', 'ha')])
    assert iteration == 0

    permutations, iteration = drop_permutations(varnum-1, combination)
    assert (list(permutations) ==
            [('ha', 'bc', 'de'), ('ha', 'de', 'bc'), ('bc', 'ha', 'de'),
             ('bc', 'de', 'ha'), ('de', 'ha', 'bc'), ('de', 'bc', 'ha')])
    assert iteration == varnum-1

    permutations, iteration = drop_permutations(varnum+1, combination)
    assert (list(permutations) ==
            [                    ('ha', 'de', 'bc'), ('bc', 'ha', 'de'),
             ('bc', 'de', 'ha'), ('de', 'ha', 'bc'), ('de', 'bc', 'ha')])
    assert iteration == 1



def drop(n, generator):
    for i in range(n):
        generator.__next__()


def test_drop():
    generator = ( x for x in range(10) )

    drop(5, generator)
    assert generator.__next__() == 5

    drop(4, generator)

    with pytest.raises(StopIteration):
        generator.__next__()


def main():
    args = docopt.docopt(__doc__)

    wordset = args["WORD"]

    numvar  = args["--number"]  or False
    permute = args["--permute"] or False

    minlen  = int(args["--min"]   or 0)
    maxlen  = int(args["--max"]   or 32)
    skip    = int(args["--skip"]  or 0)

    if numvar:
        print(possibilities_number(wordset, permute) - skip)
        return 0

    # Combinations are done from the front to the back, so putting shorter
    # elements first should iterate on more words in a shorter time
    if permute:
        wordset.sort(key=len)
        
    counter = 0

    try:
        for each in gen_passwords(wordset, minlen, maxlen, permute, skip):
            print(each)
            counter += 1

    except KeyboardInterrupt:
        print(counter, file=sys.stderr)


if __name__ == "__main__":
    main()
