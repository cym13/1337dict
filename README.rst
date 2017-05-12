Description
===========

This is a 1337-speak dictionnary generator. It combines words and generates
all 1337-speak variations of those combinations.

Practical usage
===============

Generating word combinations in 1337-speak
------------------------------------------

This is the basic feature of 1337dict. For example:

::

    $ 1337dict a b
    a
    A
    4
    @
    b
    B
    ab
    aB
    Ab
    AB
    4b
    4B
    @b
    @B

Here the words were very small in order to keep the output small, you can of
course use real words:

::

    $ 1337dict password 123 '!'

    $ 1337dict Ijustwant1337speak

    $ 1337dict -p open guest welcome wifi

It is designed to be very efficient, you have no reason to worry about your
memory usage. You can also speed it up by setting length boundaries:
combinations that do not fit that boundary will never get generated.

Permutations
------------

By default 1337dict does not permute its elements, it keeps them in order.
This explains why in the previous example *ba* is never generated. In order
to enable the permutations use the --permute flag.

Skipping and recovering
-----------------------

On forced exit with Ctrl+C 1337dict will indicate the last iteration number
outputed. This number can be combined with the --skip option given the same
arguments to restart the command from where it stopped.

Skipping can also be useful to parallelize computation on different
computers. For example:

.. code:: sh

    # Getting the total number of variations of "password"
    $ 1337dict -n password
    3072

    # On the first computer
    $ 1337dict password | head -n 1536 | aircrack-ng --whatever

    # On the second computer
    $ 1337dict --skip 1536 password | aircrack-ng --whatever

Documentation
=============

::

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

Dependencies
============

::

    docopt  https://github.com/docopt/docopt or "pip install docopt"

Alternatively 1337dict embeds unittests that are to be used with pytest.

License
=======

This program is under the GPLv3 License.

You should have received a copy of the GNU General Public License
along with this program. If not, see http://www.gnu.org/licenses/.

Contact
=======

::

    Main developper: Cédric Picard
    Email:           cedric.picard@efrei.net
