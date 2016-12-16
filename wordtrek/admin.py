"""
Provide administration details for this app.
"""

from django.contrib import admin

from .models import Animal, WordCache, Puzzle, Answers

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
    fields = ['category', 'animal_name', 'date_started']
    # fieldsets = [
    #     ('Puzzle category', {'fields': ['category', ]}),
    #     ('Animal/DQ', {'fields': ['animal_name']}),
    #     ('Date', {'fields': ['date_started']})
    # ]
    list_display = ('category', 'animal_name', 'date_started')
    inlines = [PuzzleInLine]
    list_filter = ['category', 'animal_name', 'date_started']
    search_fields = ['category', 'animal_name', 'date_started']


class AnswersInLine(admin.TabularInline):
    """
    Administer the possible answers in tabular form below the puzzle.
    """
    model = Answers
    extra = 1


class PuzzleAdmin(admin.ModelAdmin):
    """
    Administer a puzzle.
    """
    fields = ['puzzle_sequence', 'puzzle_size', 'puzzle_characters']
    # fieldsets = [
    #     ('Puzzle #', {'fields': ['puzzle_sequence']}),
    #     ('Size', {'fields': ['puzzle_size']}),
    #     # ('Letters', {'fields', ['puzzle_characters']}),
    # ]
    list_display = ('puzzle_sequence', 'puzzle_size', 'puzzle_characters')
    inlines = [AnswersInLine]
    list_filter = ['puzzle_sequence']
    search_fields = ['puzzle_sequence']

admin.site.register(Animal, AnimalAdmin)
admin.site.register(Puzzle, PuzzleAdmin)
admin.site.register(WordCache)

# EOF
