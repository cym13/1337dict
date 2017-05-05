Description
===========

This is a 1337-speak dictionnary generator. It combines words and generates
all 1337-speak variations of those combinations.

For example:

::

    $ 1337speak.py a b
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
course use real words.

It is designed to be very efficient, you have no reason to worry about your
memory usage. You can also speed it up by setting length boundaries:
combinations that do not fit that boundary will never get generated.

Documentation
=============

::

    Usage: 1337dict [-h] [-p] [-m LEN] [-M LEN] WORD...

    Options:
        -h, --help          Print this help and exit.
        -p, --permute       Enable permutations of words
        -m, --min LEN       Do not generate passwords shorter than LEN
                            Defaults to 0
        -M, --max LEN       Do not generate passwords longer than LEN
                            Defaults to 32

    Arguments:
        WORD    Word to be used present in the password
                1337dict generates all possible combinations of those words

Dependencies
============

docopt  https://github.com/docopt/docopt or "pip install docopt"

License
=======

This program is under the GPLv3 License.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

Contact
=======

::

    Main developper: Cédric Picard
    Email:           cedric.picard@efrei.net
