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
    -s, --start N       Start at output number N
    -e, --end N         End at output number N

Arguments:
    WORD    Word to be used present in the password
            1337dict generates all possible combinations of those words
"""

import sys
import docopt
import itertools
from math import factorial

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


def leet_word(word):
    if len(word) == 0:
        return ''

    if len(word) == 1:
        yield from leet_letter(word)

    for w in leet_word(word[:-1]):
        for l in leet_letter(word[-1]):
            yield w + l


def gen_passwords(wordset, minlen, maxlen, permute):
    for i in range(len(wordset)):
        for combination in itertools.combinations(wordset, i+1):
            if (len(''.join(combination)) < minlen
             or len(''.join(combination)) > maxlen):
                continue

            if permute:
                for permutation in itertools.permutations(combination):
                    yield from leet_word(''.join(permutation))

            else:
                yield from leet_word(''.join(combination))


def variations_number(word):
    weigh = 1
    for letter in word:
        weigh *= ((2 if letter.isalpha() else 1)
                + (letter in letter_num)
                + (letter in letter_sym))

    return weigh


def permutations_number(combination, permute):
    return factorial(len(combination)) if permute else 1


def possibilities_number(wordset, permute):
    result = 0

    for i in range(len(wordset)):
        for combination in itertools.combinations(wordset, i+1):
            result += (permutations_number(combination, permute)
                     * variations_number(''.join(combination)))

    return result


def main():
    args = docopt.docopt(__doc__)

    wordset = args["WORD"]

    numvar  = args["--number"]  or False
    permute = args["--permute"] or False

    minlen  = int(args["--min"]   or 0)
    maxlen  = int(args["--max"]   or 32)
    start   = int(args["--start"] or 0)
    end     = int(args["--end"]   or possibilities_number(wordset, permute))

    if end < start:
        print("--end must be more than --start", file=sys.stderr)
        return 1

    if numvar:
        print(end - start)
        return 0

    # Combinations are done from the front to the back, so putting shorter
    # elements first should iterate on more words in a shorter time
    if permute:
        wordset.sort(key=len)

    try:
        counter = 0
        for each in gen_passwords(wordset, int(minlen), int(maxlen), permute):
            print(each)
            counter += 1

            if counter == end - start:
                break

    except KeyboardInterrupt:
        print(counter, file=sys.stderr)


if __name__ == "__main__":
    main()
