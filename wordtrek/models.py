"""
Database tables and fields for WordTrek
"""

from django import forms
from django.db import models
from django.urls import reverse
from django.utils.timezone import now

__author__ = 'Travis Risner'
__project__ = "WordTrekSolver"
__creation_date__ = "01/06/2017"
# "${CopyRight.py}"


# Create your models here.

# cross-table choice possibilities
# solution status constants
SOLVE_STATUS_SOLVED = 'S'
SOLVE_STATUS_OPEN = 'O'

# solution status choices
SOLVE_STATUS = [
    (SOLVE_STATUS_SOLVED, 'Solved'),
    (SOLVE_STATUS_OPEN, 'Still Open'),
]


class Animal(models.Model):
    """
    Table holding the label for groups of puzzles or that it is a daily quest.
    """
    # define constants for the category field
    ANIMAL_IND = 'A'
    DAILY_QUEST_IND = 'D'
    OTHER_IND = 'Z'

    CATEGORY_CHOICES = [
        (ANIMAL_IND, 'Animal'),
        (DAILY_QUEST_IND, 'Daily&nbsp;Quest'),
        (OTHER_IND, 'Other')
    ]
    category = models.CharField(
        max_length=1, choices=CATEGORY_CHOICES, default=ANIMAL_IND,
        help_text='Choose either "Animal" or "Daily Quest".'
    )
    animal_order = models.IntegerField(
        default=0,
        help_text='The sequence number of the animal or "1" for daily quests.'
    )

    animal_name = models.CharField(
        max_length=30,
        help_text='Animal name or "Daily Quest".',
    )

    date_started = models.DateField(
        null=True, blank=True, default=now,
        help_text="Please use the following format: "
                  "<strong>YYYY-MM-DD</strong>.",
    )
    animal_solved = models.CharField(
        max_length=1, choices=SOLVE_STATUS, default=SOLVE_STATUS_OPEN,
        null=True, blank=True,
        help_text='Has all the puzzles for this animal/daily quest been '
                  'solved?'
    )

    class Meta:
        """
        Extra info for Animal model.
        """
        ordering = ['animal_solved', 'category', 'animal_order', 'date_started']

        # associate with a particular app
        app_label = 'wordtrek'

    def get_absolute_url(self):
        """
        Get the absolute url to the views.py class.
        :return: a reverse URL to get back to our animal detail view
        """
        abs_url = reverse('wordtrek:animal_detail', kwargs={'pk': self.pk})
        return abs_url

    def __str__(self) -> str:
        """
        Provide a sensible string for each animal or daily quest.

        :return: string holding the animal name and date
        """
        # # didn't work
        # year = ExtractYear(self.date_started)
        # month = ExtractMonth(self.date_started)
        # day = ExtractDay(self.date_started)
        # if self.category == 'A':
        #     text = '{}({}/{}/{})'.format(self.animal_name, month, day, year)
        # else:
        #     text = 'Daily Quest for {}/{}/{}'.format(month, day, year)
        if self.category == self.ANIMAL_IND:
            text = f'# {self.animal_order} - {self.animal_name} ' \
                   f'({self.date_started})'
        else:
            text = f'Daily Quest for {self.date_started}'
        return text


class Puzzle(models.Model):
    """
    One of the puzzles for the given animal.
    """
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    puzzle_sequence = models.IntegerField(
        default=0,
        # help_text='Puzzle number or sequence of this puzzle.',
    )
    puzzle_size = models.IntegerField(
        default=0,
        # help_text='The number of letters on one side of the puzzle.',
    )
    puzzle_characters = models.CharField(
        max_length=255,
        # help_text='The letters in the puzzle - left to right, top to bottom.',
        null=True, blank=True,
    )
    puzzle_solved = models.CharField(
        max_length=1, choices=SOLVE_STATUS, default=SOLVE_STATUS_OPEN,
        null=True, blank=True,
        # help_text='Have all the answers for this puzzle been solved?'
    )

    class Meta:
        """
        Provide additional info about Puzzle
        """
        ordering = ['animal', 'puzzle_solved', 'puzzle_sequence']

        # associate with a particular app
        app_label = 'wordtrek'

    def get_absolute_url(self):
        """
        Get the absolute url to the views.py class.
        :return: a reverse URL to get back to our puzzle detail view
        """
        abs_url = reverse('wordtrek:puzzle_detail', kwargs={'pk': self.pk})
        return abs_url

    def __str__(self) -> str:
        """
        Provide a sensible string for each puzzle.

        :return:
        """
        text = f'Puzzle # {self.puzzle_sequence} ' \
               f'({self.puzzle_size} x {self.puzzle_size})\n' \
               f'{self.puzzle_characters}'
        return text


# class PuzzleForm(forms.ModelForm):
#     """
#     Supply business logic to data before saving.
#     """
#
#     class Meta:
#         """
#         Identify the base table this logic is to apply.
#         """
#         model = Puzzle
#
#     def save(self, commit=True):
#         """
#         Apply business logic before saving a record.
#
#         :param commit:
#         :return:
#         """
#         super(PuzzleForm, self).save()
#
#         self.puzzle_characters = self.puzzle_characters.strip().upper()


class Answer(models.Model):
    """
    One of the answers for a puzzle.
    """
    # define constants for the answer_status field
    UNSOLVED = 'U'
    HINT = 'H'
    SOLVED = 'S'

    ANSWER_STATUS_CHOICES = [
        (UNSOLVED, 'Unsolved'),
        (HINT, 'Hinted'),
        (SOLVED, 'Solved')
    ]
    puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE)
    answer_sequence = models.IntegerField(default=0)
    answer_length = models.IntegerField(default=0)
    answer_text = models.CharField(max_length=255, null=True, blank=True)
    answer_status = models.CharField(
        max_length=1, choices=ANSWER_STATUS_CHOICES, default='U',
        # help_text='Choose answer status.'
    )

    class Meta:
        """
        Provide additional info about Answer.
        """
        ordering = ['puzzle', 'answer_sequence']

        # associate with a particular app
        app_label = 'wordtrek'

    def get_absolute_url(self):
        """
        Get the absolute url to the views.py class.
        :return: a reverse URL to get back to our answer detail view
        """
        abs_url = reverse('wordtrek:answer', kwargs={'pk': self.pk})
        return abs_url

    def __str__(self) -> str:
        """
        Provide a sensible string for each answer.

        :return:
        """
        if self.answer_status == self.UNSOLVED:
            text = f'Answer # {self.answer_sequence} needs ' \
                   f'{self.answer_length} letters'
        elif self.answer_status == self.HINT:
            text = f'Answer # {self.answer_sequence} needs ' \
                   f'{self.answer_length} letters (hint: ' \
                   f'{self.answer_text})'
        else:
            text = f'Answer # {self.answer_sequence} is ' \
                   f'{self.answer_text}'
        return text


class AnswerLetter(models.Model):
    """
    The position of a letter in the answer.
    """
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    letter_order = models.IntegerField(default=0)
    letter_text = models.CharField(max_length=1)
    letter_row = models.IntegerField(default=-1)
    letter_col = models.IntegerField(default=-1)

    class Meta:
        """
        Provide additional constraints.
        """
        ordering = ['answer', 'letter_order', ]

    # associate with a particular app
    app_label = 'wordtrek'

    def get_absolute_url(self):
        """
        Get the absolute url to the views.py class.
        :return: a reverse URL to get back to our answer letter detail view
        """
        abs_url = reverse('wordtrek:answer', kwargs={'pk': self.pk})
        return abs_url

    def __str__(self) -> str:
        """
        Provide a sensible string for each letter of the answer.

        :return:
        """
        text = f'letter order {self.letter_order} ' \
               f'for {self.letter_text} ' \
               f'is at position {self.letter_row}. {self.letter_col}'
        return text


class WordSearch(models.Model):
    """
    Non-dictionary word search.
    
    When a word in the puzzle is not in the dictionary, Create a list if 
    letter combinations (one per record) to consider.  Start showing all 
    combinations, then whittle it down by the "impossible" word prefixes 
    until we have a more reasonable list of words to consider.
    """
    SHOW_IND = 'S'
    HIDE_IND = 'H'

    SHOW_HIDE_CHOICES = [
        (SHOW_IND, 'Show'),
        (HIDE_IND, 'Hide'),
    ]

    word_text = models.CharField(max_length=255)

    show_hide = models.CharField(
        max_length=1, choices=SHOW_HIDE_CHOICES, default=SHOW_IND,
        help_text='Choose to show or hide this word'
    )

    class Meta:
        """
        Extra info about WordSearch.
        """
        ordering = ['word_text']

        # assocate with WordTrek
        app_label = 'wordtrek'

    def __str__(self) -> str:
        """
        Provide a sensible string for each record.
        :return: 
        """
        if self.show_hide == self.SHOW_IND:
            text = f'{self.word_text} - shown'
        else:
            text = f'{self.word_text} - hidden'

        return text


class WordCache(models.Model):
    """
    Cache of previously found words.

    These lists of words were previously found from the aspell library.  It is
    organized by a "sorted" key of all the letters in the word by sorted
    order, the length of the word, and by the valid word.
    """
    word_length = models.IntegerField(default=0)
    sorted_letters = models.CharField(max_length=255)
    valid_word = models.CharField(max_length=255)

    # # associate with a particular app
    # app_label = 'wordtrek'

    class Meta:
        """
        Provide additional info about WordCache.
        """
        ordering = ['sorted_letters', 'word_length', 'valid_word']

        # associate with a particular app
        app_label = 'wordtrek'

    def __str__(self) -> str:
        """
        Provide a sensible string for each word.
        :return:
        """
        text = f'{self.valid_word} ({self.word_length}-{self.sorted_letters})'
        return text

# EOF
