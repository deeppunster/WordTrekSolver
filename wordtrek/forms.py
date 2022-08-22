"""
forms.py - provide details validation of an animal or DQ.
"""

from logging import getLogger, debug, error

from django import forms
from django.core.exceptions import ValidationError
# from django.forms import inlineformset_factory
from django.forms import inlineformset_factory, BaseInlineFormSet
from django.shortcuts import get_object_or_404

# from support.Puzzlebox import PuzzleBoxClass
from wordtrek.models import Animal, Puzzle, Answer, AnswerLetter
from wordtrek.models import WordSearch
from wordtrek.support.GetAWord import GetAWordClass

__author__ = 'Travis Risner'
__project__ = "WordTrekSolver"
__creation_date__ = "01/18/2017"
# "${CopyRight.py}"

# log = getLogger(__name__)

gaw = GetAWordClass()


class AnimalDQForm(forms.ModelForm):
    """
    Manage Animal/DQ details with a generic form.
    """

    class Meta:
        """
        Additional info to help Django provide intelligent defaults.
        """
        model = Animal
        fields = ['category', 'animal_order', 'animal_name', 'date_started',
                  'animal_solved']

    def clean(self):
        """
        Additional form validation logic.

        **Important Note:**
        Currently a new animal does not go through this method for
        validation.  If I ever figure out why, I will implement the new
        portion of the comments below.

        :return:
        """

        # items not yet validated:
        # - animal:
        #   - name is not (case insensitive) "Daily Quest"
        #   - new:
        #     - name is unique amongst animals
        #     - order is unique amonst animals
        # - daily quest:
        #   - name = 'Daily Quest'
        #   - order = 1
        #   - date-started is unique

        # determine if new or edit
        # TODO Determine how to validate new entries - 1/19/17

        # animal validation

        # get the id of the existing record
        animal_id = self.instance.id

        # find out if it is now an animal or a daily quest
        category = self.cleaned_data.get('category')

        # retrieve other cleaned data for our use
        order = self.cleaned_data.get('animal_order')
        name = self.cleaned_data.get('animal_name')
        date_started = self.cleaned_data.get('date_started')

        # daily quest validation
        if category == Animal.DAILY_QUEST_IND:
            if order != 1:
                raise ValidationError('The order for daily quests must be 1.')
            if name != 'Daily Quest':
                raise ValidationError('The name must be "Daily Quest" for '
                                      'daily quests.')
            dq_set_same_date = Animal.objects.filter(
                date_started__exact=date_started).exclude(
                id__exact=animal_id).exclude(category__exact='D')
            if len(dq_set_same_date) > 0:
                raise ValidationError(
                    'The date started for daily quests must be unique.'
                )

        # Other category validation
        elif category == Animal.OTHER_IND:
            if order != 1:
                raise ValidationError('The order for other categories must be '
                                      '1.')
            if name.casefold() == 'daily quest':
                raise ValidationError('The name must not be "Daily Quest" for '
                                      'other category.')
            dq_set_same_date = Animal.objects.filter(
                date_started__exact=date_started).exclude(
                id__exact=animal_id).exclude(category__exact='Z')
            if len(dq_set_same_date) > 0:
                raise ValidationError(
                    'The date started for other quests must be unique.'
                )

        # animal validation
        elif category == Animal.ANIMAL_IND:
            # check animal order
            animal_set_order = Animal.objects.filter(
                animal_order__exact=order).exclude(
                id__exact=animal_id).exclude(category__exact='D')
            if len(animal_set_order) > 0:
                raise ValidationError(
                    'The order for animals must be unique.'
                )

            # check animal name
            if name.casefold() == 'daily quest':
                raise ValidationError('Animal name cannot be "Daily Quest')
            animal_set_name = Animal.objects.filter(
                animal_name__exact=name).exclude(id__exact=animal_id)
            if len(animal_set_name) > 0:
                raise ValidationError('The name of the animal must be unique.')


        return self.cleaned_data


class PuzzleInlineFormSet(BaseInlineFormSet):
    """
    Add custom logic to an inline form set.

    Note: Cannot add logic directly to AnimalPuzzleFormSet below.  Instead,
    this class has the additional logic and is incorporated into the form set
    below.

    Note: attempts to modify data here fail because the data has already
    been saved to the database.

    """

    def clean(self):
        """
        Capture changes to the data and respond accordingly.

        :return:
        """

        # get all fields from parent
        super(PuzzleInlineFormSet, self).clean()

        # # set data fields prefix
        # pfx = 'puzzle_set-'

        # walk through the cleaned data for each form and fix as needed
        for ndx, puzzle in enumerate(self.cleaned_data):

            # skip empty forms
            if not puzzle:
                continue

            # get the size of the puzzle
            puzzle_size = puzzle['puzzle_size']

            # get the characters in the puzzle
            puzzle_chars = puzzle['puzzle_characters']

            # validate the two fields individually, then together

            # check that the puzzle size is reasonable
            if puzzle_size < 1 or puzzle_size > 10:
                raise ValueError(
                    f'The puzzle size value "{puzzle_size}" must be numeric '
                    f'in the range of 1 - 10',
                    params={'puzzle_size': puzzle_size}
                )

            # remove leading and trailing white space and force all letters to
            # upper case
            clean_puzzle_chars = puzzle_chars.strip().upper()

            # check that the string only contains letters
            if not clean_puzzle_chars.isalpha():
                raise ValidationError(
                    f'The puzzle letters "{puzzle_chars}" for puzzle '
                    f'{ndx}must only contain letters',
                    params={'puzzle_chars': puzzle_chars})

            # check that the number of characters match the puzzle size
            if len(clean_puzzle_chars) != (puzzle_size * puzzle_size):
                raise ValidationError(
                    f'The number of characters in the puzzle letters "'
                    f'{puzzle_chars} must match the square of the puzzle size '
                    f'"{puzzle_size}"',
                    params={'puzzle_chars': puzzle_chars,
                            'puzzle_size': puzzle_size}
                )

            # this failed to work as well
            # # passed all the checks, store the (upper-cased) letters - NOT
            # # in self.cleaned_data but in self.data
            #
            # # # build name of this set of puzzle letters
            # #  puzzle_letters_name = pfx + str(ndx) + '-puzzle_characters'
            #
            # # allow self.cleaned_data to be modified
            # if self.cleaned_data[ndx]['puzzle_characters'] == False:
            #     self.cleaned_data[ndx]['puzzle_characters'] = True
            #
            # self.cleaned_data[ndx]['puzzle_characters'] = clean_puzzle_chars
            #
            # # restore immutability of self.cleaned_data
            # # if self.cleaned_data[ndx]['puzzle_characters'] == True:
            # #     self.cleaned_data[ndx]['puzzle_characters'] = False

        return self.cleaned_data

    def form_valid(self):
        """
        Validate the data.

        Note: not triggered.

        :return:
        """

        super(PuzzleInlineFormSet, self).form_valid()

        return

AnimalPuzzleFormSet = inlineformset_factory(
    Animal,
    Puzzle,
    formset=PuzzleInlineFormSet,  # see comments in class above
    extra=10,
    max_num=32,
    # labels='',   # didn't affect anything, labels still appeared

    fields=['puzzle_sequence', 'puzzle_size', 'puzzle_characters',
            'puzzle_solved']
)

AnswerAnswerLetterFormSet = inlineformset_factory(
    Answer,
    AnswerLetter,
    extra=15,
    max_num=20,

    fields=['letter_order', 'letter_text', 'letter_row', 'letter_col', ]
)


class AnswerInlineFormSet(BaseInlineFormSet):
    """
    Add custom logic to an inline form set.

    Note: Cannot add logic directly to PuzzleAnswerFormSet below.  Instead,
    this class has the additional logic and is incorporated into the form set
    below.
    """
    def clean(self):
        """
        Capture changes to the data and respond accordingly.

        :return:
        """

        # if the answer text has been invalidated for some reason, delete the
        # corresponding letters in the AnswerLetter table
        for answer in self.cleaned_data:
            # following if required because the cleaned data has an object
            # for each of the "extra" lines added to the form
            if answer == dict():
                continue
            if answer['answer_sequence'] != 0 and \
                    answer['answer_status'] != Answer.SOLVED:
                answer_id = answer['id']
                letters_deleted = AnswerLetter.objects.filter(
                    answer_id=answer_id).delete()
                debug(f'Answer letters deleted was: {letters_deleted}')

        return


PuzzleAnswerFormSet = inlineformset_factory(
    Puzzle,
    Answer,
    formset=AnswerInlineFormSet,  # see comments in class above
    extra=10,
    max_num=10,

    fields=['answer_sequence', 'answer_length', 'answer_status',
            'answer_text', ],
)


class WordSolveForm(forms.ModelForm):
    """
    Manage Animal/DQ details with a generic form.
    """

    # define additional (non-db) fields here
    possible_answer = forms.CharField(
        label='Possible answer',
        required=False,
    )

    # # create a Puzzle Solving Box on the fly as a class variable
    # pb = None

    class Meta:
        """
        Additional info to help Django provide intelligent defaults.
        """
        model = Answer
        fields = ['answer_sequence', 'answer_length', 'answer_status',
                  'possible_answer'
                  ]

    # def clean(self):
    #     """
    #     Additional form validation logic.
    #
    #     **Important Note:**
    #     Currently a new animal does not go through this method for
    #     validation.  If I ever figure out why, I will implement the new
    #     portion of the comments below.
    #
    #     :return:
    #     """
    #
    #     # extract some reccord id's
    #
    #     # get the answer id
    #     answer_id = self.instance.id
    #
    #     # get the puzzle id and puzzle for this answer
    #     puzzle_id = self.instance.puzzle_id
    #     puzzle = get_object_or_404(Puzzle, pk=puzzle_id)
    #
    #     # get the animal for this puzzle
    #     animal_id = get_object_or_404(Animal, pk=puzzle.animal_id).id
    #
    #     # # if the puzzle box for this puzzle has not yet been created, do it
    #     # if not WordSolveForm.pb:
    #     #     size = puzzle.puzzle_size
    #     #     letters = puzzle.puzzle_characters
    #     #     length = self.instance.answer_length
    #     #     WordSolveForm.pb = PuzzleBoxClass(size, letters)
    #     #     WordSolveForm.pb.build_word_list_from_box(length)
    #     #
    #     # # get a word from the possible solutions
    #     # next_word = WordSolveForm.pb.get_a_word()
    #
    #     # try to get the next valid word
    #     next_word = gaw.get_next_word(animal_id=animal_id,
    #                                   puzzle_id=puzzle_id,
    #                                   answer_id=answer_id)
    #     possible_answer = next_word
    #
    #     return self.cleaned_data


# class WordSearchForm(forms.ModelForm):
#     """
#     Manage attempt to find a rapid solution to non-dictionary words.
#     """
#
#     # define additional (non-db) fields for the template
#     trim_words = forms.CharField(
#         label='beginning of character string to trim or restore',
#         required=False,
#     )
#
#     show_all = forms.BooleanField(
#         label='Restore all character sequences?',
#         initial=False,
#     )
#
#     ACTION_TRIM = 'T'
#     ACTION_RESTORE = 'R'
#     ACTION_NONE = 'N'
#
#     ACTION_CHOICES = [
#         (ACTION_TRIM, 'Trim words with this prefix'),
#         (ACTION_RESTORE, 'Restore words with this prefix'),
#         (ACTION_NONE, 'No action'),
#     ]
#
#     action = forms.CharField(
#         label='Choose action to take:?',
#         choices=ACTION_CHOICES,
#         initial=ACTION_NONE,
#     )
#
#     class Meta:
#         """
#         Additional info to help drive this form.
#         """
#         model = WordSearch
#         fields = ['show_all', 'trim_words', 'action', 'word_text']

# EOF
