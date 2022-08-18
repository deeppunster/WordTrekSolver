"""
constants.py - Some constants used for managing words.

Note - many of the assumptions of this program are exposed here.
"""

from enum import Enum
from typing import NamedTuple
from multiprocessing import cpu_count
from os.path import join

__author__ = 'Travis Risner'
__project__ = "WordTrekSolver"
__creation_date__ = "01/01/2017"
# "${CopyRight.py}"

# Assumed maximum word size
MAX_WORD_SIZE = 15

# Maximum number of CPU cores to use for multiprocessing
# leave one core for other tasks
MAX_CORE_LIMIT = cpu_count() - 1

# manual recursion limit - default is 1000
RECURSION_LIMIT = 1500


class WordSetInfo(NamedTuple):
    """
    Return containing all the info about a list of valid words.
    """
    word_size: int
    sorted_letters: str
    word_list: list


# value to put in a cell that has been used by another answer
CELL_VACANT = '\u2588'  # full block

# value to put in a cell to show that it is unimportant (not used in the word)
CELL_UNIMPORTANT = '\u22c5'  # dot operator

# value to indicate the end of row for a flattened table
ROW_MARKER = '|'


class CELL_STATUS(Enum):
    """
    Constants used to populate the availability matrix.
    """
    AVAILABLE = 'usable'
    USED = 'used'
    EDGE = 'edge'


class CELL_POSITION(NamedTuple):
    """
    Position of cell in the box (0 based).
    """
    row: int
    col: int


class AVAILABILITY(NamedTuple):
    """
    Positions around the cell and their usefulness.
    """
    UL: CELL_STATUS  # UL - upper left
    UP: CELL_STATUS  # UP - upper (above)
    UR: CELL_STATUS  # UR - upper right
    RG: CELL_STATUS  # RG - right side
    LR: CELL_STATUS  # LR - lower right
    LW: CELL_STATUS  # LW - lower (below)
    LL: CELL_STATUS  # LL - lower left
    LF: CELL_STATUS  # LF - left side


# adjustments to current position (row, column)
ADJ_UL = CELL_POSITION(row=-1, col=-1)
ADJ_UP = CELL_POSITION(row=-1, col=0)
ADJ_UR = CELL_POSITION(row=-1, col=1)
ADJ_RG = CELL_POSITION(row=0, col=1)
ADJ_LR = CELL_POSITION(row=1, col=1)
ADJ_LW = CELL_POSITION(row=1, col=0)
ADJ_LL = CELL_POSITION(row=1, col=-1)
ADJ_LF = CELL_POSITION(row=0, col=-1)

# adjustment order list
ADJ_LIST = [ADJ_UL, ADJ_UP, ADJ_UR, ADJ_RG, ADJ_LR, ADJ_LW, ADJ_LL, ADJ_LF, ]


class CELL(NamedTuple):
    """
    Contents of a cell in the box.
    """
    pos: CELL_POSITION
    letter: str
    my_availability: CELL_STATUS
    neighbors: AVAILABILITY


class LETTER_LOC(NamedTuple):
    """
    Holds a letter chosen and its location.
    """
    found_letter: str
    letter_loc: CELL_POSITION


class FOUND_WORD(NamedTuple):
    """
    Report the found word and the locations of all letters used in it.
    """
    found_word: str
    letters_loc: list


class QUEUE_ENTRY(NamedTuple):
    found_word: str
    letter_seq: list


# value to put in the word queue to indicate that there are no more words
END_QUEUE_MARKER = '## END OF LIST ##'

# entry to put in the word queue to indicate that there are no more words
END_QUEUE_ENTRY = QUEUE_ENTRY(found_word=END_QUEUE_MARKER, letter_seq=list())

# (END_QUEUE_WORD is obsolete)
END_QUEUE_WORD = FOUND_WORD(found_word=END_QUEUE_MARKER, letters_loc=list())

# couldn't figure out how to use this tuple to set the dictionary key
# class RESET_OPTION(NamedTuple):
#     """
#     Constants used as indexes to the reset table.
#     """
#     RESET_PUZZLE = 'reset_puzzle'
#     FLIP_VOWEL_CHECK = 'check_vowels'
#     FLIP_DICTIONARY_CHECK = 'use_dictionary'


# reset option choices (actions)
RESET_PUZZLE = 'reset_puzzle'
RESET_SOLVED_STATUS = 'reset_solved_status'
FLIP_VOWEL_CHECK = 'flip_vowel_check'
FLIP_DICTIONARY_CHECK = 'flip_dictionary_check'
TURN_DICTIONARY_ON = 'force_dictionary_on'

# reset dictionary keys
VOWEL_CHECK = 'vowels'
DICTIONARY_CHECK = 'dict'

# flags for next word selection from queue
SAME_NEXT_WORD = 'SAME'
UNIQUE_NEXT_WORD = 'UNIQUE'
FLUSH_WORD_CACHE = 'FLUSH'


class WORD_SELECTION(Enum):
    unique_word = UNIQUE_NEXT_WORD
    same_word = SAME_NEXT_WORD
    flush_cache = FLUSH_WORD_CACHE


RAW_WORD_LIST = 'raw_word_list.txt'
# EOF
