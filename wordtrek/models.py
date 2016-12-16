"""
Database tables and fields for WordTrek
"""

from django.db import models
from django.utils import timezone, datetime_safe
from django.db.models.functions import ExtractDay, ExtractMonth, ExtractYear


# Create your models here.


class Animal(models.Model):
    """
    Table holding the label for groups of puzzles or that it is a daily quest.
    """
    category = models.CharField(max_length=1, choices=(
        ('A', 'animal'),
        ('D', 'daily quest')
    ))
    animal_name = models.CharField(max_length=30)
    date_started = models.DateTimeField('date started')

    def __str__(self) -> str:
        """
        Provide a sensible string for each animal or daily quest.

        :return: string holding the animal name and date
        """
        year = ExtractYear(self.date_started)
        month = ExtractMonth(self.date_started)
        day = ExtractDay(self.date_started)
        if self.category == 'A':
            text = '{}({}/{}/{})'.format(self.animal_name, month, day, year)
        else:
            text = 'Daily Quest for {}/{}/{}'.format(month, day, year)
        return text


class Puzzle(models.Model):
    """
    One of the puzzles for the given animal.
    """
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    puzzle_sequence = models.IntegerField(default=0)
    puzzle_size = models.IntegerField(default=0)
    puzzle_characters = models.CharField(max_length=255)

    def __str__(self) -> str:
        """
        Provide a sensible string for each puzzle.

        :return:
        """
        text = 'Puzzle # {0} ({1} x {1})\n{2}'.format(self.puzzle_sequence,
                                                      self.puzzle_size,
                                                      self.puzzle_characters)
        return text


class Answers(models.Model):
    """
    One of the answers for a puzzle.
    """
    puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE)
    answer_sequence = models.IntegerField(default=0)
    answer_length = models.IntegerField(default=0)
    answer_text = models.CharField(max_length=255)

    def __str__(self) -> str:
        """
        Provide a sensible string for each answer.

        :return:
        """
        if len(self.answer_text.strip()) == 0:
            text = 'Answer # {} needs {} characters'.format(
                self.answer_sequence, self.answer_length)
        else:
            text = 'Answer # {} is {}'.format(self.answer_sequence,
                                              self.answer_text)
        return text


class WordCache(models.Model):
    """
    Cache of previously found words.

    This list of words were prevously found from the aspell library.  It is
    organized by length of the word and a "sorted" key of all the letters
    in the word by sorted order.
    """
    word_length = models.IntegerField(default=0)
    sorted_letters = models.CharField(max_length=255)
    valid_word = models.CharField(max_length=255)

    def __str__(self) -> str:
        """
        Provide a sensible string for each word.
        :return:
        """
        text = '{} ({}-{})'.format(self.valid_word, self.word_length,
                                   self.sorted_letters)
        return text

# EOF
