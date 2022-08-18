"""
GetAWord.py - Look for words in the database or create a new list.
"""
from itertools import permutations
from logging import getLogger, debug, error

from django.shortcuts import get_object_or_404

from wordtrek.support.PuzzleboxParallel import PuzzleBoxParallelClass
# from . import Puzzlebox
from wordtrek.models import Puzzle, Answer, AnswerLetter, \
    SOLVE_STATUS_SOLVED, \
    SOLVE_STATUS_OPEN, Animal
from wordtrek.support.constants import FOUND_WORD, CELL_POSITION, \
    RESET_SOLVED_STATUS, TURN_DICTIONARY_ON, VOWEL_CHECK, DICTIONARY_CHECK,\
    WORD_SELECTION, RESET_PUZZLE, FLIP_VOWEL_CHECK, FLIP_DICTIONARY_CHECK, \
    MAX_CORE_LIMIT

__author__ = 'Travis Risner'
__project__ = "WordTrekSolver"
__creation_date__ = "01/06/2017"
# "${CopyRight.py}"

log = getLogger(__name__)


class GetAWordClass:
    """
    GetAWordClass - Look for words in dictionary or make new list.
    """

    def __init__(self):
        """
        Set up for looking in the dictionary or creating a new list.

        (Used by views.py - module initialization)
        """
        # self.ewc = ExtractWords.ExtractWordsClass()
        # self.spell_checker = SpellChecker.SpellCheckerClass()
        self.pb = None

        # Current request info
        self.curr_animal_id = None
        self.curr_puzzle_id = None
        self.curr_answer_id = None

        # puzzle and answer info retrieved from database
        self.puzzle_letters = None
        self.other_answer_letters = None
        self.word_length = None
        self.word_hint = None

        # puzzle reset options
        self.reset_options = dict()

        # set defaults for startup
        self.reset_options[RESET_PUZZLE] = False
        self.reset_options[VOWEL_CHECK] = True
        self.reset_options[DICTIONARY_CHECK] = True

        # internal source of words and valid values for indicator
        self.word_source = None
        self.word_source_cache = 'CACHE'
        self.word_source_dictionary = 'DICTIONARY'
        self.word_source_puzzle_box = 'PUZZLE BOX'

        # handling of kind of work selection desired (set to default)
        self.word_selection_kind = WORD_SELECTION.unique_word

        # other internal variables
        self.retrieve_word = None
        self.core_limit = MAX_CORE_LIMIT

        return

    def get_next_word(self, animal_id=None, puzzle_id=None, answer_id=None) \
            -> FOUND_WORD:
        """
        Get the next word as a possible answer.

        (Called by WordSolveView.get_context_data)

        :param animal_id: internal id of an animal or daily quest
        :param puzzle_id: internal id of a puzzle for an animal or DQ
        :param answer_id: internal id of an answer for a puzzle
        :return: the next possible word
        """

        if animal_id == self.curr_animal_id and \
                puzzle_id == self.curr_puzzle_id and \
                answer_id == self.curr_answer_id:
            next_word = self.get_next_word_from_box(self.word_selection_kind)
        elif animal_id == self.curr_animal_id and \
                puzzle_id == self.curr_puzzle_id:
            self.curr_answer_id = answer_id
            next_word = self.start_new_word_search()
        else:
            self.curr_animal_id = animal_id
            self.curr_puzzle_id = puzzle_id
            self.curr_answer_id = answer_id
            next_word = self.start_new_puzzle_search()
        return next_word

    def get_next_word_from_box(self, kind: WORD_SELECTION) -> FOUND_WORD:
        """
        Get next word from a (already initialized) source.

        (Internal call from get_next_word)
        :return:
        """
        next_word = self.pb.get_a_word(kind)
        return next_word

    def start_new_word_search(self) -> FOUND_WORD:
        """
        Initialize internals for a new word search and return the first word.

        (Internal call from get_next_word)

        :return: the first word found
        """

        # for now, treat it like a new puzzle
        first_word = self.start_new_puzzle_search()

        return first_word

    def start_new_puzzle_search(self) -> FOUND_WORD:
        """
        Initialize internals for a new puzzle search and return the first word.

        (Internal call from get_next_word and start_new_word_search)

        :return: the first word found
        """

        # retrieve puzzle and answer info from database
        puzzle = get_object_or_404(Puzzle, pk=self.curr_puzzle_id)

        # set up a new puzzle box
        self.word_source = self.word_source_puzzle_box
        self.pb = PuzzleBoxParallelClass(
            box_size=puzzle.puzzle_size,
            box_letters=puzzle.puzzle_characters.strip().upper(),
            reset_options=self.reset_options,
        )

        # remove any previous answers
        answer_set = Answer.objects.filter(
            puzzle_id__exact=self.curr_puzzle_id)
        for answer in answer_set:
            if answer.id == self.curr_answer_id:
                self.word_length = answer.answer_length
                if answer.answer_status == Answer.HINT:
                    self.word_hint = answer.answer_text.upper()
                else:
                    self.word_hint = ''
            elif answer.answer_status == Answer.SOLVED:
                self.remove_answer_letters(answer.id)

        self.pb.build_word_list_from_box(self.word_length, self.word_hint)

        # get the first found word and return it
        next_word = self.pb.get_a_word(WORD_SELECTION.flush_cache)
        return next_word

    def remove_answer_letters(self, answer_id: int):
        """
        Remove the last word received from the puzzle.

        (called from WordSolveView.post and internally by
        start_new_puzzle_search)

        :param answer_id:
        :return:
        """

        # get the answer positions for this answer
        answer_letter_set = AnswerLetter.objects.filter(
            answer_id=answer_id)

        # if there are locations to back up this word, remove them from puzzle
        if answer_letter_set:

            # build a "found' word from the db for this answer
            word = ''
            letter_loc = list()
            for answer_letter in answer_letter_set:
                word += answer_letter.letter_text
                cell_pos = CELL_POSITION(row=answer_letter.letter_row,
                                         col=answer_letter.letter_col)
                letter_loc.append(cell_pos)

            answer_info = FOUND_WORD(found_word=word, letters_loc=letter_loc)

            # pass in the answer chosen to the box as verification
            self.pb.remove_an_answer(answer_info)

        # else must be a hint, use it later
        else:
            pass

        return

    def get_working_box_letters(self) -> list:
        """
        Return a list of lists containing the working box at the moment.

        (Called from PuzzleDetailView.get_context_data)
        :return:
        """

        if self.pb:
            working_box = self.pb.get_working_box_letters()
        else:
            # have to set message as text in a 1 X 1 box
            col_text = ['Puzzle not initialized']
            working_box = [col_text]
        return working_box

    def reset_an_option(self, reset_option: str):
        """
        Reset a puzzle processing option.

        (Called from WorldSolveView.get_context_data and post, and from
        reset_puzzle)

        :return:
        """
        # reset the puzzle box?
        if reset_option == RESET_PUZZLE:
            self.curr_animal_id = 0
            self.curr_puzzle_id = 0
            self.curr_answer_id = 0
            self.kill_word_searches()

        # turn on or off the check for vowels?
        elif reset_option == FLIP_VOWEL_CHECK:
            previous_setting = self.reset_options[VOWEL_CHECK]
            self.reset_options[VOWEL_CHECK] = not previous_setting

        # turn on or off using the dictionary as a word filter?
        elif reset_option == FLIP_DICTIONARY_CHECK:
            previous_setting = self.reset_options[DICTIONARY_CHECK]
            self.reset_options[DICTIONARY_CHECK] = not previous_setting

        # restore using the dictionary as a word filter
        elif reset_option == TURN_DICTIONARY_ON:
            self.reset_options[DICTIONARY_CHECK] = True

        elif reset_option == RESET_SOLVED_STATUS:
            self.reset_solved_status()

        # problem - yell!
        else:
            raise ValueError(f'Reset puzzle option {reset_option} invalid!')

        return

    def get_reset_options(self) -> dict:
        """
        Return the reset options as a dictionary.

        (Called from AnimalDQListView.get_context_data)

        :return:
        """
        options_dict = self.reset_options
        return options_dict

    def kill_word_searches(self):
        """
        Look for asynchronous word searches and kill them as needed.
        
        :return: 
        """
        if self.pb:
            self.pb.kill_any_word_searches()
        return

    def reset_solved_status(self):
        """
        Reset the solved status for animals and puzzles.

        Rather than try to reset everything at once, first reset the puzzle
        solve status, then reset the animal solved status once we are
        certain that the puzzles have been properly marked.

        (Called internally from reset_an_option)

        :return:
        """

        # reset the solved status of puzzles

        # get a list of all the puzzles in the table
        puzzle_list = Puzzle.objects.all()

        # for each puzzle find out if there are any answers
        for puzzle in puzzle_list:
            solved = SOLVE_STATUS_SOLVED
            answer_list = Answer.objects.filter(puzzle_id__exact=puzzle.id)

            # if there are answers, verify that they all have been solved
            if answer_list:
                for answer in answer_list:
                    if answer.answer_status != Answer.SOLVED:
                        solved = SOLVE_STATUS_OPEN

            # else, if no answers at all, mark the puzzle as unsolved
            else:
                solved = SOLVE_STATUS_OPEN

            # update puzzle with results
            puzzle.puzzle_solved = solved
            puzzle.save()

        # now do similar processing for setting the animal solved status

        # get a list of all animals and daily quests in the table
        critter_list = Animal.objects.all()

        # for each animal or daily quest find out if there are any puzzles
        for critter in critter_list:
            solved = SOLVE_STATUS_SOLVED
            puzzle_list = Puzzle.objects.filter(animal_id__exact=critter.id)

            # if there are any puzzles, verify that they have all been solved
            if puzzle_list:
                for puzzle in puzzle_list:
                    if puzzle.puzzle_solved != SOLVE_STATUS_SOLVED:
                        solved = SOLVE_STATUS_OPEN

            # else, if no puzzles at all, mark as unsolved
            else:
                solved = SOLVE_STATUS_OPEN

            # update animal or daily quest with results
            critter.animal_solved = solved
            critter.save()

        return

    def set_word_selection_choice(self, kind: WORD_SELECTION):
        """
        Set the word selection choice desired.

        :param kind:
        :return:
        """
        if kind in WORD_SELECTION:
            self.word_selection_kind = kind

        return

# EOF
