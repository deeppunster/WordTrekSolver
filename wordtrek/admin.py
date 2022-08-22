"""
admin.py - administrative views for wordtrek.
"""
from logging import getLogger, debug, error, info
from django.contrib import admin

from wordtrek.models import Animal, WordCache, Puzzle, Answer

__author__ = 'Travis Risner'
__project__ = "WordTrekSolver"
__creation_date__ = "01/06/2017"
# "${CopyRight.py}"

log = getLogger(__name__)

# Register your models here.


class PuzzleInLine(admin.TabularInline):
    """
    Administer the possible puzzles for an animal or daily quest.
    """
    model = Puzzle
    extra = 1


class AnimalAdmin(admin.ModelAdmin):
    """
    Administer the Animal table and its dependents.
    """
    info('Running AnimalAdmin class')
    fields = ['animal_solved', 'category', 'animal_order', 'animal_name',
              'date_started']
    # fieldsets = [
    #     ('Puzzle category', {'fields': ['category', ]}),
    #     ('Animal/DQ', {'fields': ['animal_name']}),
    #     ('Date', {'fields': ['date_started']})
    # ]
    list_display = ('animal_solved',  'category', 'animal_order',
                    'animal_name', 'date_started', 'id')
    inlines = [PuzzleInLine]
    list_filter = ['animal_solved',  'category', 'animal_order',
                   'animal_name', 'date_started']
    search_fields = ['animal_solved', 'category', 'animal_order',
                     'animal_name', 'date_started']


class AnswersInLine(admin.TabularInline):
    """
    Administer the possible answers in tabular form below the puzzle.
    """
    model = Answer
    extra = 1


class PuzzleAdmin(admin.ModelAdmin):
    """
    Administer a puzzle.
    """
    info('Running PuzzleAdmin class')
    fields = ['puzzle_sequence', 'puzzle_size', 'puzzle_characters',
              'puzzle_solved']
    # fieldsets = [
    #     ('Puzzle #', {'fields': ['puzzle_sequence']}),
    #     ('Size', {'fields': ['puzzle_size']}),
    #     # ('Letters', {'fields', ['puzzle_characters']}),
    # ]
    list_display = ('puzzle_sequence', 'puzzle_size', 'puzzle_characters',
                    'puzzle_solved')
    inlines = [AnswersInLine]
    list_filter = ['puzzle_sequence', 'puzzle_solved']
    search_fields = ['puzzle_sequence', 'puzzle_solved']

admin.site.register(Animal, AnimalAdmin)
admin.site.register(Puzzle, PuzzleAdmin)
admin.site.register(WordCache)

# EOF
