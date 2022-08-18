"""
views.py - views needed by the wordtrek application.
"""

from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from wordtrek.forms import AnimalDQForm, AnimalPuzzleFormSet, \
    AnswerAnswerLetterFormSet, PuzzleAnswerFormSet, WordSolveForm
# from .forms import WordSearchForm
from wordtrek.models import Animal, Answer, AnswerLetter, Puzzle
from wordtrek.models import WordSearch, SOLVE_STATUS_SOLVED
from wordtrek.support.GetAWord import GetAWordClass
from wordtrek.support.constants import CELL_POSITION, CELL_UNIMPORTANT, \
    FLIP_VOWEL_CHECK, END_QUEUE_MARKER, FOUND_WORD, RESET_PUZZLE, \
    RESET_SOLVED_STATUS, ROW_MARKER, FLIP_DICTIONARY_CHECK, \
    TURN_DICTIONARY_ON, \
    WORD_SELECTION

__author__ = 'Travis Risner'
__project__ = "WordTrekSolver"
__creation_date__ = "01/06/2017"
# "${CopyRight.py}"

# initialize the lookup class here so it is only done once
gaw = GetAWordClass()


# Create your views here.


class AnimalDQListView(ListView):
    """
    Main view (list) of animals and DQ's using a generic ListView.
    """
    model = Animal
    template_name = 'wordtrek/animal_list.html'
    context_object_name = 'animal_list_context'

    def get_context_data(self, **kwargs):
        """
        Add additional content to the context.

        :param kwargs:
        :return: context
        """
        context = super(AnimalDQListView, self).get_context_data()

        # provide additional information
        reset_options = gaw.get_reset_options()
        context['reset_options'] = reset_options

        return context


class AnimalDQDetailView(DetailView):
    """
    Show details of an animal or daily quest using a generic DetailView.
    """
    model = Animal
    template_name = 'wordtrek/animal_detail.html'
    context_object_name = 'animal_detail_context'

    def get_context_data(self, **kwargs):
        """
        Add additional content to the context.

        :param kwargs:
        :return: context
        """
        context = super(AnimalDQDetailView, self).get_context_data()

        # provide additional information
        # animal_id = context['id']
        animal = context['object']

        # add puzzles
        puzzle_set = Puzzle.objects.filter(
            animal_id__exact=animal.id)

        # add stuff back to context
        context['animal'] = animal
        context['puzzle_set'] = puzzle_set

        return context


class AnimalDQCreateView(CreateView):
    """
    Create an animal or daily quest using a generic CreateView.
    """
    model = Animal
    template_name = 'wordtrek/animal_edit.html'
    context_object_name = 'animal_edit_context'

    formClass = AnimalDQForm

    # Future Why are fields required here in the create - 1/18/17
    fields = ['category', 'animal_order', 'animal_name', 'date_started', ]

    def get_context_data(self, **kwargs):
        """
        Modify the context before rendering the template.

        :param kwargs:
        :return:
        """

        context = super(AnimalDQCreateView, self).get_context_data(**kwargs)
        context['action'] = reverse('wordtrek:animal_new')
        return context

    def get_success_url(self):
        """
        Run once form is successfully validated.

        :return:
        """
        results = reverse('wordtrek:animal_view')
        return results


class AnimalDQUpdateView(UpdateView):
    """
    Update an animal or daily quest using a generic UpdateView.
    """

    model = Animal
    template_name = 'wordtrek/animal_edit.html'
    context_object_name = 'animal_edit_context'

    form_class = AnimalDQForm

    # Future Why are fields forbidden here in the update - 1/18/17
    # fields = ['category', 'animal_order', 'animal_name', 'date_started', ]

    def get_context_data(self, **kwargs):
        """
        Modify the context before rendering the template.

        :param kwargs:
        :return:
        """

        context = super(AnimalDQUpdateView, self).get_context_data(**kwargs)
        context['action'] = reverse('wordtrek:animal_update',
                                    kwargs={'pk': self.get_object().id})
        return context

    def get_success_url(self):
        """
        Set the next URL to use once the edit is successful.
        :return:
        """

        results = reverse('wordtrek:animal_view')
        return results


class AnimalDQDeleteView(DeleteView):
    """
    Delete an animal or daily quest using a generic DeleteView.
    """
    model = Animal
    template_name = 'wordtrek/animal_delete.html'
    context_object_name = 'animal_delete_context'

    def get_success_url(self):
        """
        Set the next URL to use once the delete is successful.
        :return:
        """

        results = reverse('wordtrek:animal_view')
        return results


class PuzzleDetailView(DetailView):
    """
    Show details of a puzzle using a generic DetailView.
    """
    model = Puzzle
    template_name = 'wordtrek/puzzle_detail.html'
    context_object_name = 'puzzle_detail_context'

    def get_context_data(self, **kwargs):
        """
        Add additional content to the context.

        :param kwargs:
        :return: context
        """
        context = super(PuzzleDetailView, self).get_context_data()

        # provide additional information
        context_puzzle = context['object']

        # try to get all related records
        this_puzzle = Puzzle.objects.select_related().get(id=context_puzzle.id)

        # get associated animal
        this_animal = get_object_or_404(Animal, pk=this_puzzle.animal_id)

        # add answers
        answer_set = Answer.objects.filter(
            puzzle_id__exact=this_puzzle.id).order_by('answer_sequence', )

        # get current working table
        working_table = gaw.get_working_box_letters()
        letter_location_table = flatten_table_for_display(working_table)

        # add stuff back to context
        context['this_animal'] = this_animal
        context['this_puzzle'] = this_puzzle
        context['answer_set'] = answer_set
        context['letter_location_table'] = letter_location_table

        return context


class AnimalPuzzleEditView(UpdateView):
    """
    Edit the Puzzles under a given animal or daily quest.
    """

    model = Animal
    template_name = 'wordtrek/puzzle_edit.html'
    form_class = AnimalPuzzleFormSet

    # def save(self):
    #     """
    #     Try modifying the same to force the puzzle letters to upper case
    #
    #     Note: there is no save method to override in UpdateView
    #     :return:
    #     """
    #     super(AnimalPuzzleEditView, self).save()

    # def post(self, request, *args, **kwargs):
    #     """
    #     Stash the selected word in the answer.
    #
    #     Note: adding a post method to UpdateView causes the clean method
    #     in the form to be ignored.
    #
    #     :param request: HTTPRequest info
    #     :param args:
    #     :param kwargs:
    #     :return:
    #     """
    #
    #     # get access to the incoming data
    #     post_info = request.POST
    #
    #     # allow POST to be modified
    #     if not request.POST._mutable:
    #         request.POST._mutable = True
    #
    #     # set form fields prefix
    #     pfx = 'puzzle_set-'
    #
    #     # get value of max-forms from post data
    #     max_forms_key = pfx + 'TOTAL_FORMS'
    #     max_forms = int(post_info[max_forms_key])
    #
    #     # force all puzzle letters to upper case and strip spaces
    #     for ndx in range(max_forms):
    #         # build name of this set of puzzle letters
    #         puzzle_letters_name = pfx + str(ndx) + '-puzzle_characters'
    #
    #         # get puzzle letters and mangle them into the proper format
    #         letters = post_info[puzzle_letters_name]
    #         fixed_letters = letters.strip().upper()
    #         post_info[puzzle_letters_name] = fixed_letters
    #
    #         # leave all validation to the clean method
    #
    #     # allow request to be modified
    #     if request.POST._mutable:
    #         request.POST._mutable = False
    #
    #     # declare where to go from here
    #     target = HttpResponseRedirect(
    #         reverse('wordtrek:animal_detail',
    #                 kwargs={'pk': self.get_object().id}))
    #     return target

    # this method was never invoked
    # def clean_puzzle_characters(self):
    #     """
    #     Capture changes to the data and respond accordingly.
    #
    #     :return:
    #     """
    #
    #     # obtain the field to examine and modify
    #     puzzle_chars = self.cleaned_data['puzzle_characters']
    #
    #     # remove leading and trailing white space and force all letters to
    #     # upper case
    #     clean_chars = puzzle_chars.strip().upper()
    #
    #     # check that the string only contains letters
    #     if not clean_chars.isalpha():
    #         raise ValidationError(
    #             f'The puzzle letters "{puzzle_chars}" must only contain '
    #             f'letters',
    #             params={'puzzle_chars': puzzle_chars})
    #
    #     return clean_chars

    def get_success_url(self, **kwargs):
        """
        Run once form is successfully validated.

        :return:
        """

        # return to animal detail
        # Tried get object - failed (something about URLConf)
        # Tried to get context - failed (no context in list item)
        # Tried commenting out this method - failed (no URL to redirect to)

        # workaround to force the puzzle letters to upper case
        # extract the amimal id from the containing object
        animal_key = self.get_object().id

        # get the puzzles for this animal, if any
        puzzles = Puzzle.objects.filter(animal_id=animal_key)
        for puzzle in puzzles:
            puzzle.puzzle_characters = puzzle.puzzle_characters.upper()
            puzzle.save()

        results = reverse('wordtrek:animal_detail',
                          kwargs={'pk': self.get_object().id})
        return results


class PuzzleAnswerEditView(UpdateView):
    """
    Edit the answers under a given puzzle.
    """

    model = Puzzle
    template_name = 'wordtrek/answer_edit.html'
    form_class = PuzzleAnswerFormSet

    def get_context_data(self, **kwargs):
        """
        Add additional content to the context.

        :param kwargs:
        :return: context
        """
        context = super(PuzzleAnswerEditView, self).get_context_data()

        # provide additional information
        this_puzzle = context['object']

        # get associated animal
        this_animal = get_object_or_404(Animal, pk=this_puzzle.animal_id)

        # make formset info explicitly available
        # formset = PuzzleAnswerFormSet(self.request.POST)

        # add stuff back to context
        context['this_animal'] = this_animal
        context['this_puzzle'] = this_puzzle
        # context['formset'] = formset

        return context

    def get_success_url(self, **kwargs):
        """
        Run once form is successfully validated.

        :return:
        """

        # return to puzzle detail
        results = reverse('wordtrek:puzzle_detail',
                          kwargs={'pk': self.get_object().id})
        return results


class AnswerLetterEditView(UpdateView):
    """
    Edit the answer letters for an answer of a puzzle.
    """

    model = Answer
    template_name = 'wordtrek/answer_letter_edit.html'
    form_class = AnswerAnswerLetterFormSet

    def post(self, request, *args, **kwargs):
        """
        Stash the selected letters for this word.

        :param request: HTTPRequest info
        :param args:
        :param kwargs:
        :return:
        """
        answer_key = {'pk': self.get_object().id}
        answer_id = answer_key['pk']
        this_answer = get_object_or_404(Answer, pk=answer_id)
        post_info = request.POST
        for ndx in range(int(post_info['answerletter_set-TOTAL_FORMS'])):
            prefix = 'answerletter_set-'
            order = int(post_info[prefix + str(ndx) + '-letter_order'])
            if order > 0:
                letter = post_info[prefix + str(ndx) + '-letter_text']
                row = int(post_info[prefix + str(ndx) + '-letter_row'])
                col = int(post_info[prefix + str(ndx) + '-letter_col'])
                this_answer_loc = AnswerLetter(
                    answer=this_answer,
                    letter_order=order,
                    letter_text=letter,
                    letter_row=row,
                    letter_col=col
                )
                this_answer_loc.save()

        # remove the letters of the answer from the puzzle
        # gaw.remove_answer_letters(this_answer.id)

        # get this puzzle id for the following url
        puzzle_id = post_info['this_puzzle_id']

        # declare where to go from here
        target = HttpResponseRedirect(
            reverse('wordtrek:puzzle_detail',
                    kwargs={'pk': puzzle_id}))
        return target

    def get_context_data(self, **kwargs):
        """
        Modify the context before rendering the template.

        :param kwargs:
        :return:
        """

        context = super(AnswerLetterEditView, self).get_context_data(**kwargs)

        # provide additional information
        this_answer = context['object']

        # get associated puzzle
        this_puzzle = get_object_or_404(Puzzle, pk=this_answer.puzzle_id)

        # get associated animal
        this_animal = get_object_or_404(Animal, pk=this_puzzle.animal_id)

        # add stuff back to context
        context['this_animal'] = this_animal
        context['this_puzzle'] = this_puzzle
        context['this_answer'] = this_answer
        return context

    def get_success_url(self, **kwargs):
        """
        Redirect back to the puzzle answer one the edit is finished.
        :param kwargs:
        :return:
        """

        # return to answer detail
        results = reverse('wordtrek:puzzle_detail',
                          kwargs={'pk': self.get_object().id})
        return results


class WordSolveView(DetailView):
    """
    Solve a puzzle one word at a time using a generic view.
    """

    model = Answer
    template_name = 'wordtrek/puzzle_solve_edit.html'
    context_object_name = 'puzzle_solve_context'

    form_class = WordSolveForm

    def post(self, request, *args, **kwargs):
        """
        Stash the selected word in the answer.

        :param request: HTTPRequest info
        :param args:
        :param kwargs:
        :return:
        """
        answer_key = kwargs = {'pk': self.get_object().id}
        answer_id = answer_key['pk']
        this_answer = get_object_or_404(Answer, pk=answer_id)
        desired_answer = request.POST.get('possible_answer')
        letter_locations_string = request.POST.get('letter_locations_string')
        word_loc = string_to_letter_locs(letter_locations_string)

        this_answer.answer_text = desired_answer
        this_answer.answer_status = Answer.SOLVED
        this_answer.save()
        if len(desired_answer) == len(word_loc):
            for order, zip_list in enumerate(zip(desired_answer, word_loc),
                                             start=1):
                letter, loc = zip_list
                this_answer_loc = AnswerLetter(
                    answer=this_answer,
                    letter_order=order,
                    letter_text=letter,
                    letter_row=loc.row,
                    letter_col=loc.col
                )
                this_answer_loc.save()

        # remove the letters of the answer from the puzzle
        gaw.remove_answer_letters(this_answer.id)

        # now restore dictionary use in case it was turned off momentarily
        gaw.reset_an_option(TURN_DICTIONARY_ON)

        # declare where to go from here by default
        target = HttpResponseRedirect(
            reverse('wordtrek:puzzle_detail',
                    kwargs={'pk': this_answer.puzzle_id}))

        # if all answers have been given for this puzzle, mark it solved
        answers_missing = Answer.objects.filter(
            puzzle_id__exact=this_answer.puzzle_id).exclude(
            answer_status__exact=Answer.SOLVED)
        if not answers_missing:
            this_puzzle = Puzzle.objects.get(id__exact=this_answer.puzzle_id)
            this_puzzle.puzzle_solved = SOLVE_STATUS_SOLVED
            this_puzzle.save()

            # declare where to go from here when the puzzle has been solved
            target = HttpResponseRedirect(
                reverse('wordtrek:animal_detail',
                        kwargs={'pk': this_puzzle.animal_id}))

            # if all puzzles for this animal have also been solved, mark the
            # animal solved
            puzzles_open = Puzzle.objects.filter(
                animal_id=this_puzzle.animal_id).exclude(
                puzzle_solved=SOLVE_STATUS_SOLVED)
            if not puzzles_open:
                this_animal = Animal.objects.get(
                    id__exact=this_puzzle.animal_id)
                this_animal.animal_solved = SOLVE_STATUS_SOLVED
                this_animal.save()

                # declare where to go from here when the animal has been solved
                target = HttpResponseRedirect(
                    reverse('wordtrek:animal_view'))

        return target

    def get_context_data(self, **kwargs):
        """
        Modify the context before rendering the template.

        :param kwargs:
        :return:
        """

        context = super(WordSolveView, self).get_context_data(**kwargs)

        # provide additional information
        this_answer = context['object']

        # get associated puzzle
        this_puzzle = get_object_or_404(Puzzle, pk=this_answer.puzzle_id)

        # get associated animal
        this_animal = get_object_or_404(Animal, pk=this_puzzle.animal_id)

        # get a proposed word
        possible_found_word = gaw.get_next_word(animal_id=this_animal.id,
                                                puzzle_id=this_puzzle.id,
                                                answer_id=this_answer.id)

        # prepare for display
        final_location_display_string = ''
        location_display_string = ''
        letter_locations_string = ''
        letter_location_table = ''
        if possible_found_word.found_word == END_QUEUE_MARKER:
            end_of_answers = True
            possible_answer = END_QUEUE_MARKER
            gaw.reset_an_option(RESET_PUZZLE)
        else:
            end_of_answers = False
            # extract word
            possible_answer = possible_found_word.found_word
            # prepare to display locations
            for loc in possible_found_word.letters_loc:
                location_display_string += \
                    f'{loc.found_letter} ' \
                    f'({loc.letter_loc.row}, {loc.letter_loc.col}), '
            final_location_display_string = location_display_string[:-2]

            # prepare for letter locations turnaround
            letter_locations_string = letter_locs_to_string(
                possible_found_word.letters_loc)

            # prepare to display the letters of this word in a table
            letter_location_table = build_possible_answer_table(
                puzzle_size=this_puzzle.puzzle_size,
                answer=possible_found_word
            )

        # add stuff back to context
        context['this_animal'] = this_animal
        context['this_puzzle'] = this_puzzle
        context['this_answer'] = this_answer
        context['possible_answer'] = possible_answer
        context['letter_locations'] = final_location_display_string
        context['letter_locations_string'] = letter_locations_string
        context['letter_location_table'] = letter_location_table
        context['end_of_answers'] = end_of_answers
        return context

    def get_success_url(self):
        """
        Set the next URL to use once the edit is successful.

        Note: never used.  Success comes through post method above.
        :return:
        """

        results = reverse('wordtrek:puzzle_detail',
                          kwargs={'pk': self.get_object().id})
        return results


# class WordSearchView(UpdateView):
#     """
#     Try to rapidly find non-dictionary answers.
#     """
#     model = WordSearch
#     template_name = 'wordtrek/answer_search.html'
#     form_class = WordSearchForm
#
#     def post(self, request, *args, **kwargs):
#         """
#         Adjust the selected prefix of words to include or exclude.
#         :param request:
#         :param args:
#         :param kwargs:
#         :return:
#         """
#         answer_key = {'pk': self.get_object().id}
#         answer_id = answer_key['pk']
#         this_answer = get_object_or_404(Answer, pk=answer_id)
#         this_puzzle = get_object_or_404(Puzzle, pk=this_answer.puzzle)
#         this_animal = get_object_or_404(Animal, pk=this_puzzle.animal)
#         post_info = request.POST
#
#         # declare where to go from here
#         target = HttpResponseRedirect(
#             reverse('wordtrek:puzzle_detail',
#                     kwargs={'pk': answer_id}))
#         return target


def word_solve_unique(request, pk) -> HttpResponseRedirect:
    """
    Force a unique possible answer (not previously presented).

    :param request: http request info
    :param pk: applicable answer id
    :return: a text response
    """

    answer_id = pk

    # take appropriate action
    gaw.set_word_selection_choice(WORD_SELECTION.unique_word)

    # go back to answer solving page
    response = HttpResponseRedirect(reverse('wordtrek:word_solve',
                                            kwargs={'pk': answer_id}))
    return response


def word_solve_same(request, pk) -> HttpResponseRedirect:
    """
    Force the same possible answer but with different letter choices.

    :param request: http request info
    :param pk: applicable answer id
    :return: a text response
    """

    answer_id = pk

    # take appropriate action
    gaw.set_word_selection_choice(WORD_SELECTION.same_word)

    # go back to answer solving page
    response = HttpResponseRedirect(reverse('wordtrek:word_solve',
                                            kwargs={'pk': answer_id}))
    return response


def build_possible_answer_table(*,
                                puzzle_size: int,
                                answer: FOUND_WORD) -> list:
    """
    Build a table with the letters of this answer prominently displayed.

    :param puzzle_size:
    :param answer:
    :return:
    """
    # build default table
    table = list()
    for row in range(puzzle_size):
        table.append(list())
        for col in range(puzzle_size):
            table[row].append(CELL_UNIMPORTANT)

    # add the letters of the answer in the appropriate places
    for loc in answer.letters_loc:
        letter = loc.found_letter
        pos = loc.letter_loc
        table[pos.row][pos.col] = letter

    final_table = flatten_table_for_display(table)

    return final_table


def flatten_table_for_display(table: list) -> list:
    """
    Reformat the two-dimensional table so it can be displayed in the template.

    :param table:
    :return:
    """

    # flatten table and add a marker after each row
    flat_table = list()
    for row in table:
        for col in row:
            flat_table.append(col)
        flat_table.append(ROW_MARKER)

    # remove the last row marker
    final_table = flat_table[:-1]
    return final_table


def reset_puzzle(request, reset_option) -> HttpResponseRedirect:
    """
    Reset certain processing options.

    :param request: http request info
    :param reset_option: specifies which option to set or reset
    :return: a text response
    """

    # determine desired option
    if reset_option == 'puzzle':
        option_selected = RESET_PUZZLE
    elif reset_option == 'vowel':
        option_selected = FLIP_VOWEL_CHECK
    elif reset_option == 'dict':
        option_selected = FLIP_DICTIONARY_CHECK
    elif reset_option == 'solved':
        option_selected = RESET_SOLVED_STATUS
    else:
        option_selected = ''

    # take appropriate action
    gaw.reset_an_option(option_selected)

    # go back to main page
    response = HttpResponseRedirect(reverse('wordtrek:animal_view'))
    return response


def reset_puzzle_box(request, pk) -> HttpResponseRedirect:
    """
    Reset the puzzle box and return to the puzzle detail.

    :param request: http request info
    :param pk: applicable puzzle id
    :return: a text response
    """

    puzzle_id = pk

    # take appropriate action
    gaw.reset_an_option(RESET_PUZZLE)

    # go back to answer solving page
    response = HttpResponseRedirect(reverse('wordtrek:puzzle_detail',
                                            kwargs={'pk': puzzle_id}))
    return response


def reset_dictionary(request, pk) -> HttpResponseRedirect:
    """
    Flip the dictionary check and return to the puzzle detail.

    :param request: http request info
    :param pk: applicable puzzle id
    :return: a text response
    """

    puzzle_id = pk

    # take appropriate action
    gaw.reset_an_option(FLIP_DICTIONARY_CHECK)

    # go back to answer solving page
    response = HttpResponseRedirect(reverse('wordtrek:puzzle_detail',
                                            kwargs={'pk': puzzle_id}))
    return response


"""
The following two functions are used by WordSolveView.
"""


def letter_locs_to_string(letter_loc_list: list) -> str:
    """
    Convert a list of positions to a string for stashing is a web page.
    :param letter_loc_list:
    :return:
    """

    # walk through list of positions building a string to return
    # use '|' as separator between positions
    # use ',' as separator between row and column
    text = ''
    for letter_loc in letter_loc_list:
        pos = letter_loc.letter_loc
        text += f'{str(pos.row)},{str(pos.col)}|'

    # strip off trailing vertial bar
    final_text = text[:-1]

    return final_text


def string_to_letter_locs(letter_locations_string: str) -> list:
    """
    Convert string into a list of positions for storing in the db.
    :param letter_locations_string:
    :return:
    """

    # assume string was formatted by letter_locs_to_string
    pos_list = list()
    pos_string_list = letter_locations_string.split(sep='|')
    for pos_string in pos_string_list:
        pos_elements = pos_string.split(sep=',')
        pos = CELL_POSITION(row=int(pos_elements[0]),
                            col=int(pos_elements[1]))
        pos_list.append(pos)

    return pos_list

# EOF
