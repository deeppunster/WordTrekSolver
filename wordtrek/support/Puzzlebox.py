"""
Puzzlebox.py - Identify touching letters in a box.
"""

from collections import deque
from logging import getLogger, debug, error
from copy import deepcopy

from .constants import AVAILABILITY, ADJ_LIST, FOUND_WORD, LETTER_LOC, \
    VOWEL_CHECK, DICTIONARY_CHECK, WORD_SELECTION
from .constants import FLIP_VOWEL_CHECK, FLIP_DICTIONARY_CHECK
from .constants import CELL_VACANT, END_QUEUE_WORD
from .constants import CELL, CELL_STATUS, CELL_POSITION
from .SpellChecker import SpellCheckerClass


__author__ = 'Travis Risner'
__project__ = "WordTS-Box"
__creation_date__ = "01/22/2017"
# "${CopyRight.py}"

log = None


class PuzzleBoxClass:
    """
    Create a representation of the puzzle and try to find words in it.
    """

    def __init__(self, box_size: int, box_letters: str, reset_options: dict):
        """
        Initialize the box size and the letter contained in each box.
        :param box_size:
        :param box_letters:
        """
        # capture initial parameters
        self.side = box_size
        self.letters = box_letters.strip().upper()

        # create a pipeline to receive words
        self.word_queue = deque()

        # create an array of side X side and populate with letters and a
        # place to add found words
        self.my_box = Box(self.side, self.letters, self.word_queue,
                          reset_options)

        # maintain a cache of previously retrieved words so only unique
        # words are returned by default
        self.word_cache = set()

        # last word returned - in case a variant of the same word is desired
        self.last_word_returned = None

    def build_word_list_from_box(self, word_length: int, word_hint: str):
        """
        Get the next available word from the box.

        :param word_length:
        :param word_hint:
        :return:
        """

        # force hints to upper case
        my_word_hint = word_hint.upper()

        # walk through the box, picking each available position in turn as
        # the starting point for a word
        for cell_count, cell in enumerate(
                self.my_box.get_next_starting_point()):
            # box_count = cell_count
            row_pos = cell.pos.row
            col_pos = cell.pos.col
            letter = cell.letter
            debug(f'Starting position for next group of words - '
                  f'Row: {row_pos}, '
                  f'Column: {col_pos}, '
                  f'Letter: {letter}'
                  )

            # if any hint provided, launch search only if first letter matches
            if len(my_word_hint) > 0 and letter != my_word_hint[0]:
                continue
            self.my_box.find_words_from_here(cell, word_length, my_word_hint)
            debug(f'BWFB - returned from finding words from here')

        return

    def get_a_word(self, kind: WORD_SELECTION)-> FOUND_WORD:
        """
        Return one word from the queue.

        The word returned depends on the kind flag.  A cache of previously
        returned words is kept so that only unique words are returned by
        default.  However, if the kind desired is a variant of the same
        word (using different boxes in the puzzle), then return only those
        variants.  If requested to flush the queue, clear the queue and
        treat it as request for the next (first) unique word.

        :param kind: kind of word desired
        :return: a found word tuple
        """

        request_type = kind
        next_word = None

        # request is for the cache to be flushed before retrieving a word
        if request_type == WORD_SELECTION.flush_cache:
            self.word_cache = set()
            request_type = WORD_SELECTION.unique_word

        # request is for the next unique word
        if request_type == WORD_SELECTION.unique_word:
            while True:
                self.last_word_returned = self._next_word()
                if self.last_word_returned.found_word in self.word_cache:
                    continue
                else:
                    self.word_cache.add(self.last_word_returned.found_word)
                    break
        # request for a variant of the same word
        elif request_type == WORD_SELECTION.same_word:
            while True:
                next_word = self._next_word()
                if next_word.found_word == self.last_word_returned.found_word:
                    self.last_word_returned = next_word
                    break
                else:
                    continue
        else:
            raise ValueError(f'Unable to handle request of "{kind}" in '
                             f'get_a_word')

        # clear cache if end of queue encountered (probably redundant)
        if self.last_word_returned == END_QUEUE_WORD:
            self.word_cache = set()

        return self.last_word_returned

    def _next_word(self) -> FOUND_WORD:
        # extract the words from the queue and send them back
        try:
            next_queued_word = self.word_queue.popleft()
        except IndexError:
            next_queued_word = END_QUEUE_WORD

        return next_queued_word

    def remove_an_answer(self, answer_word: FOUND_WORD):
        """
        Remove the last word from the puzzle box.
        :param answer_word:
        :return:
        """

        self.my_box.remove_word_letters(answer_word)

        return

    def get_working_box_letters(self) -> list:
        """
        Return a list of lists containing the working box at the moment.
        :return:
        """
        working_box = self.my_box.get_working_box_letters()
        return working_box

    def __str__(self) -> str:
        """
        Prepare a string of essential info about this class.
        :return:
        """

        text = str(self.my_box)
        return text


class Box:
    """
    Container for a puzzle box.
    """

    def __init__(self, box_size: int, box_letters: str, word_queue: deque,
                 reset_option: dict):
        """
        Initialize the box size and the letter contained in each box.
        :param box_size: the size of one side of the puzzle
        :param box_letters: the letters contained in the puzzle (l-r, t-b)
        :param word_queue: a que to add found words
        """
        # capture initial parameters
        self.side = box_size
        self.letters = box_letters
        self.word_queue = word_queue
        self.reset_option = reset_option

        # validate size vs. letters
        if self.side * self.side != len(self.letters):
            raise ValueError(f'Incorrect number of letters for a box that '
                             f'is {self.side} letters on a side.')

        # set other variables
        self.box = None
        self.word_length = None
        self.hint = None

        # fill in the static information in the box
        self.fill_cells_in_box()

        # see documentation about why these deeply copied maps are necessary
        # stash of starter maps - maps of positions used at the previous level
        self.starter_map_stash = dict()
        # stash of try maps - maps of positions tried at the this level
        self.try_map_stash = dict()
        # stash of letter locations - locations in the order used
        self.letter_loc_stash = dict()

        # initialize the spell check api
        self.spell_check = SpellCheckerClass()

        return

    def __str__(self) -> str:
        """
        Provide nice representation of box.
        :return:
        """
        text = ''
        for row_count, row in enumerate(self.box):
            text += f'Row {row_count + 1}:\n'
            for col_count, cell in enumerate(row):
                text += f'\tColumn {col_count + 1}:\n'
                text += f'\t\tPosition: ({cell.pos[0] + 1}, ' \
                        f'{cell.pos[1] + 1})\n'
                text += f'\t\tLetter: {cell.letter}\n'
                text += f'\t\tNeighbors: {cell.neighbors}\n'
            text += '\n'

        return text

    def fill_cells_in_box(self):
        """
        Initialize a box with static information.

        :return:
        """
        # implement as a list of lists
        self.box = list()

        # prepare to fill the box.
        get_letter = letter_gen(self.letters)

        # fill initial box
        for row_pos in range(self.side):
            row = list()
            for col_pos in range(self.side):

                # determine neighbor status
                my_pos = CELL_POSITION(row=row_pos, col=col_pos)
                my_neighbors = fill_availability_box(my_pos, self.side)
                row.append(CELL(pos=my_pos,
                                letter=get_letter.__next__(),
                                my_availability=CELL_STATUS.AVAILABLE,
                                neighbors=my_neighbors))
            self.box.append(row)

        # shut down letter generator for future use.
        get_letter.close()

    def get_next_starting_point(self):
        """
        Walk through the box returning each valid starting point for a word.

        Note: this method is a generator returning a cell each time.
        :return:
        """

        for row in reversed(self.box):
            for cell in reversed(row):
                if cell.my_availability == CELL_STATUS.AVAILABLE:
                    yield cell

        return

    def find_words_from_here(
            self, cell: CELL, word_length: int, word_hint: str):
        """
        Given a starting point and a word length, find a series of words.

        Note: these strings are called "words", but until spell-checked,
        the strings produced here may just be nonsense.

        :param cell:
        :param word_length:
        :param word_hint:
        :return:
        """

        start_cell = cell
        self.word_length = word_length
        self.hint = word_hint.upper()

        # get the starting letter and its location to stash at this level
        start_letter = start_cell.letter
        pos = start_cell.pos
        letter_loc = LETTER_LOC(found_letter=start_letter, letter_loc=pos)
        loc_list = [letter_loc]
        self.letter_loc_stash[self.word_length] = loc_list

        # get the letter out of the starting cell, create a letter map with
        # that cell used, and adjust the letters needed accordingly
        start_word_letters = start_letter
        letters_needed = self.word_length - 1
        start_letter_map = self.init_letter_map(start_cell)

        # the first letter of the hint already filtered in
        # build_word_list_from_box

        debug(f'FWFH starting point: '
              f'first letter: {start_word_letters} '
              f'start map:\n\t{start_letter_map}')

        # look for all the possible remaining letters
        self.get_next_letter(
                letters_needed=letters_needed, prev_cell=start_cell,
                prev_letter_map=start_letter_map,
                prev_word_letters=start_word_letters,
                prev_letters_loc=loc_list
        )

        debug(f'FWFH Get next letter returned')

        return

    def init_letter_map(self, start_cell: CELL):
        """
        Initialize a used letter map and mark the starting cell as used.

        :param start_cell:
        :return:
        """
        # create a blank (empty) letter map with all letters available
        empty_letter_map = list()
        for row_pos in range(self.side):
            letter_row = list()
            for col_pos in range(self.side):
                letter_row.append(self.box[row_pos][col_pos].my_availability)
            empty_letter_map.append(letter_row)

        # mark the starting cell as used
        letter_map = mark_cell_used(empty_letter_map, start_cell)
        return letter_map

    def get_next_letter(self, *, letters_needed: int,
                        prev_cell: CELL,
                        prev_letter_map: list,
                        prev_word_letters: str,
                        prev_letters_loc: list):
        """
        Recursive function to get the next available letter or report the word.

        The letter (and its cell position are considered valid for the word
        so far.  letters_needed indicates how many **more** letters must be
        found before we have a word to try against the puzzle.

        If a hint has been provided, the letters in prev_word_letters match
        the hint so far.  If the hint runs out at this point, we are free
        to choose any available letter.  Otherwise, the letter chosen next
        must match the next letter in the hint.

        Note - with this many parameters and with recursion, all parameters
            must be provided using keywords.

        :param letters_needed:
        :param prev_cell:
        :param prev_letter_map:
        :param prev_word_letters:
        :param prev_letters_loc:
        :return: all the letters generated so far
        """
        # do we have a word yet?  If so report it, else get another letter
        if letters_needed == 0:

            # default to adding word to queue
            use_word = True

            # apply filters as needed
            # vowel check
            if self.reset_option[VOWEL_CHECK]:
                if not contains_vowel(prev_word_letters):
                    use_word = False
            # dictionary check
            if self.reset_option[DICTIONARY_CHECK]:
                if not self.spell_check.check_word(prev_word_letters):
                    use_word = False

            # if word passed the filters, add it to the queue
            if use_word:
                this_word = FOUND_WORD(found_word=prev_word_letters,
                                       letters_loc=prev_letters_loc)
                self.word_queue.append(this_word)

        else:

            # capture this position as an anchor for this iteration

            # capture all the previous letters in this word so far
            my_word_letters = prev_word_letters

            # capture the previous cell
            my_cell = prev_cell

            # capture the previous letter locations
            my_letter_locs = prev_letters_loc

            # Determine if there are any hint letters left and select the
            # next one.  Note that since Python indexes strings counting at
            # zero, the length of the previously accumulated letters
            # automatically points to the next letter needed in the hint.
            if len(self.hint) > len(my_word_letters):
                next_hint_letter = self.hint[len(my_word_letters)]
            else:
                next_hint_letter = None

            # initialize my letter map and locations to the previous info
            my_letter_map = prev_letter_map
            self.starter_map_stash[letters_needed] = deepcopy(my_letter_map)
            self.letter_loc_stash[letters_needed] = deepcopy(my_letter_locs)
            debug(f'GNL Starting next letter: still need: {letters_needed}, '
                  f'starting cell: {prev_cell.pos}, '
                  f'start map:\n\t{my_letter_map}')

            # initialize a search map (indicating which neighbors have been
            # tried and add to the try map stash
            my_search_map = my_letter_map
            self.try_map_stash[letters_needed] = deepcopy(my_search_map)

            # loop through all the possible neighbors of this cell
            while True:
                # try to get the next available neighbor and use it
                try:
                    # point to my search map in the try map stash
                    my_search_map = self.try_map_stash[letters_needed]
                    try_cell = self.find_next_available_cell(
                        prev_cell, my_search_map, next_hint_letter)

                    # mark that this cell has been tried (in the try map stash)
                    _ = mark_cell_used(my_search_map, try_cell)
                    # self.try_map_stash[letters_needed] = my_search_map

                    # get a deep copy of the original starter map for this
                    # level so that subsequent changes do not change the
                    # original
                    next_letter_map = deepcopy(
                        self.starter_map_stash[letters_needed]
                    )
                    # get a deep copy of the original letter locations
                    next_letters_loc = deepcopy(
                        self.letter_loc_stash[letters_needed])

                    # prepare variables for the next iteration
                    next_cell = try_cell
                    next_word_letters = my_word_letters + next_cell.letter
                    next_letter_map = mark_cell_used(
                        next_letter_map, next_cell)
                    letter_loc = LETTER_LOC(found_letter=next_cell.letter,
                                            letter_loc=next_cell.pos)
                    next_letters_loc.append(letter_loc)
                    next_letters_needed = letters_needed - 1
                    debug(
                        f'GNL recursing in, '
                        f'still need: {next_letters_needed}, '
                        f'next cell: {next_cell.pos}, '
                        f'letters so far: {next_word_letters}, '
                        f'next map:\n\t{next_letter_map}'
                        )

                    # call myself again if not enough letters found
                    self.get_next_letter(
                            letters_needed=next_letters_needed,
                            prev_cell=next_cell,
                            prev_letter_map=next_letter_map,
                            prev_word_letters=next_word_letters,
                            prev_letters_loc=next_letters_loc
                    )
                    debug('GNL returned for next try')
                except LookupError:
                    break

            # exhausted all possible neighbors
            debug(f'GNL exhausted all neighbors of {my_cell.pos}')
        return

    def find_next_available_cell(self, current_cell: CELL,
                                 current_letter_map: list,
                                 next_hint_letter: str) -> CELL:
        """
        Generate an available adjacent letter.

        :param current_cell:
        :param current_letter_map:
        :param next_hint_letter:
        :return:
        """
        # capture input
        my_letter_map = current_letter_map
        my_current_cell = current_cell
        debug(f'FNA start, start cell: {my_current_cell.pos}, '
              f'start map:\n\t{my_letter_map}')

        # get the neighbors of the current cell
        my_neighbors = my_current_cell.neighbors

        # set marker to default of failed to find an available cell
        found_cell = None

        # walk through the available neighbors for one that has not been used
        for pos, neighbor in enumerate(my_neighbors):
            if neighbor == CELL_STATUS.AVAILABLE:

                # get the relative position of this neighbor
                rel_pos = ADJ_LIST[pos]

                # compute the absolute location of this neighbor
                abs_pos = CELL_POSITION(
                    my_current_cell.pos.row + rel_pos.row,
                    my_current_cell.pos.col + rel_pos.col
                )

                # see if this position has been used
                if my_letter_map[abs_pos.row][abs_pos.col] == \
                        CELL_STATUS.AVAILABLE:
                    possible_cell = self.box[abs_pos.row][abs_pos.col]

                    # see if we are restricted to a certain letter by the hint
                    if next_hint_letter:
                        if next_hint_letter == possible_cell.letter:
                            found_cell = possible_cell
                            debug(
                                f'FNA returning, chosen cell: '
                                f'{found_cell.pos}')
                            break
                    else:
                        found_cell = possible_cell
                        debug(f'FNA returning, chosen cell: {found_cell.pos}')
                        break

        # check result of search
        if not found_cell:
            raise LookupError

        return found_cell

    def remove_word_letters(self, answer_word: FOUND_WORD):
        """
        Remove this word from the puzzle by marking these letters as used.
        :param answer_word:
        :return:
        """
        # presumably the caller verified that this word came from the puzzle.

        # possibly verify that the letters in accepted_word are in the
        # puzzle at the locations specified.  (presume it for now.)
        # TODO verify that these letters are located correctly - 1/26/17

        # sort the positions into top to bottom, left to right order
        unsorted_pos = answer_word.letters_loc
        sorted_pos = sorted(unsorted_pos,
                            key=lambda s_pos: ((s_pos.col * 100) + s_pos.row))

        # for each position, remove the letter and let the ones above fall
        for pos in sorted_pos:
            self.remove_a_letter(pos)

        return

    def remove_a_letter(self, pos: CELL_POSITION):
        """
        Remove a letter from the puzzle and move the letters above it down.

        :param pos:
        :return:
        """

        base_row = pos.row
        col = pos.col
        col_moves_done = False

        # validate before moving anything
        if base_row < 0 or base_row >= self.side:
            raise ValueError(f'row of {base_row} before removing a letter '
                             f'is invalid')
        if col < 0 or col >= self.side:
            raise ValueError(f'column of {col} before removing a letter is '
                             f'invalid')

        for curr_row in range(base_row, -1, -1):

            # unpack information originally in the cell
            orig_cell = self.box[curr_row][col]
            orig_letter = orig_cell.letter
            orig_neighbors = orig_cell.neighbors

            # placeholder to build cell info to put back in the cell
            new_cell = None

            # evaluate the situation for this cell

            # -- if cell is already used
            # --- don't change anything
            # --- bail out of loop
            if orig_letter == CELL_VACANT:
                new_cell = orig_cell
                col_moves_done = True

            # -- if the cell above is actually above the puzzle edge
            # --- mark this cell as unavailable
            # --- bail out of loop
            elif orig_neighbors.UP == CELL_STATUS.EDGE:
                new_cell = orig_cell._replace(my_availability=CELL_STATUS.USED,
                                              letter=CELL_VACANT)
                col_moves_done = True
            else:
                # extract above cell's letter for convenience
                above_cell_letter = self.box[curr_row - 1][col].letter

                # -- if the cell above has been marked unavailable
                # --- mark this cell as unavailable
                if above_cell_letter == CELL_VACANT:
                    new_cell = orig_cell._replace(my_availability=CELL_STATUS.USED,
                                                  letter=CELL_VACANT)
                    col_moves_done = True
                else:

                    # -- if the box above exists and has a letter
                    # --- move the letter into this cell
                    new_cell = orig_cell._replace(letter=above_cell_letter)

            # update the cell in box
            self.box[curr_row][col] = new_cell

            # check for "doneness"
            if col_moves_done:
                break

        return

    def get_working_box_letters(self) -> list:
        """
        Return just the current letter values in the current box.

        :return:
        """

        disp_box = list()
        for row in range(self.side):
            row_letters = list()
            for col in range(self.side):
                row_letters.append(self.box[row][col].letter)
            disp_box.append(row_letters)
        return disp_box


def contains_vowel(word: str) ->bool:
    """
    Check a word to see if it contains a vowel.

    :param word:
    :return: true if a vowel found, else false
    """

    for letter in word:
        if letter in 'AEIOUY':
            return True
    return False


def letter_gen(letters: str):
    """
    Generate one letter at a time from an initial string.
    :param letters:
    :return:
    """
    for letter in letters:
        yield letter

    return


def fill_availability_box(my_pos: CELL_POSITION, side: int) -> AVAILABILITY:
    """
    Fill in an availability box for this position.

    :param my_pos:
    :param side:
    :return:
    """
    my_adj_list = list()
    for adjustment in ADJ_LIST:
        neighbor_pos = (my_pos.row + adjustment[0], my_pos.col + adjustment[1])
        if neighbor_pos[0] < 0 or neighbor_pos[0] >= side or \
                neighbor_pos[1] < 0 or neighbor_pos[1] >= side:
            my_adj_list.append(CELL_STATUS.EDGE)
        else:
            my_adj_list.append(CELL_STATUS.AVAILABLE)

    # convert the list to a tuple
    my_availability = AVAILABILITY._make(my_adj_list)

    return my_availability


def mark_cell_used(current_letter_map: list, current_cell: CELL) -> list:
    """
    Mark the given cell as used in the letter map.

    :param current_letter_map:
    :param current_cell:
    :return:
    """

    # capture input parms
    my_letter_map = current_letter_map
    my_cell = current_cell

    # extract the location to be marked
    my_row = my_cell.pos.row
    my_col = my_cell.pos.col

    # mark it in my letter map
    my_letter_map[my_row][my_col] = CELL_STATUS.USED

    return my_letter_map

# EOF
