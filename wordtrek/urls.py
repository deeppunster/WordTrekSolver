"""
urls.py.py - urls needed for wordtrek application.
"""

from logging import getLogger, debug, error
from django.conf.urls import url

from wordtrek.views import AnimalDQListView, AnimalDQDetailView, \
    AnimalDQCreateView, AnimalDQUpdateView, AnimalDQDeleteView, \
    PuzzleDetailView, AnimalPuzzleEditView, PuzzleAnswerEditView, \
    WordSolveView, reset_puzzle, AnswerLetterEditView, word_solve_unique, \
    word_solve_same, reset_puzzle_box, reset_dictionary
# from .views import WordSearchView

# from .views import PuzzleCreateView

__author__ = 'Travis Risner'
__project__ = "WordTrekSolver"
__creation_date__ = "01/06/2017"
# "${CopyRight.py}"

app_name = 'wordtrek'


urlpatterns = [
    # e.g. /wordtrek/ = list of animals and daily quests
    url(r'^$', AnimalDQListView.as_view(), name='animal_view', ),

    # e.g. /wordtrek/animal/add/ = add and animal or daily quest
    url(r'^animal/add/$', AnimalDQCreateView.as_view(), name='animal_new', ),

    # e.g. /wordtrek/animal/edit/4/ = edit animal/daily quest # 4
    url(r'^animal/edit/(?P<pk>[0-9]+)/$', AnimalDQUpdateView.as_view(),
        name='animal_update', ),

    # # e.g. /wordtrek/animal/delete/4/ = delete animal/daily quest # 4
    url(r'^animal/delete/(?P<pk>[0-9]+)/$', AnimalDQDeleteView.as_view(),
        name='animal_delete', ),

    # e.g. /wordtrek/animal/4/ = show puzzles for animal/daily quest # 4
    url(r'^animal/(?P<pk>[0-9]+)/$', AnimalDQDetailView.as_view(),
        name='animal_detail', ),

    # e.g. /wordtrek/puzzle/4/ = show answers for puzzle # 4
    url(r'^puzzle/(?P<pk>[0-9]+)/$', PuzzleDetailView.as_view(),
        name='puzzle_detail', ),

    # e.g. /wordtrek/puzzle/edit/9/ = add/edit puzzles for animal/dq # 9
    url(r'^puzzle/edit/(?P<pk>[0-9]+)/$', AnimalPuzzleEditView.as_view(),
        name='puzzle_edit', ),

    # e.g. /wordtrek/answer/edit/9/ = add/edit answers for puzzle # 9
    url(r'^answer/edit/(?P<pk>[0-9]+)/$', PuzzleAnswerEditView.as_view(),
        name='answer_edit', ),

    # e.g. /wordtrek/answer/edit/letters/9/ = add/edit
    url(r'^answer/edit/letters/(?P<pk>[0-9]+)/$',
        AnswerLetterEditView.as_view(),
        name='letter_edit', ),

    # e.g. /wordtrek/word/solve/5
    url(r'^word/solve/(?P<pk>[0-9]+)/$', WordSolveView.as_view(),
        name='word_solve', ),

    # e.g. /wordtrek/word/solve/unique/5
    url(r'^word/solve/unique/(?P<pk>[0-9]+)/$', word_solve_unique,
        name='word_solve_unique', ),

    # e.g. /wordtrek/word/solve/same/5
    url(r'^word/solve/same/(?P<pk>[0-9]+)/$', word_solve_same,
        name='word_solve_same', ),

    # # e.g. /wordtrek/word/search/5
    # url(r'^word/search/(?P<pk>[0-9]+)/$', WordSearchView.as_view(),
    #     name='word_search'),

    # e.g. /wordtrek/reset/<opt>/ opt = { puzzle | vowels | dict }
    url(r'^reset/(?P<reset_option>[a-z]+)/$', reset_puzzle,
        name='reset_option', ),

    # e.g. /wordtrek/puzzle/reset/5/ = add reset puzzle for puzzle # 5
    url(r'^puzzle/reset/(?P<pk>[0-9]+)/$', reset_puzzle_box,
        name='puzzle_reset', ),

    # e.g. /wordtrek/puzzle/reset/dictionary/5/ = flip dictionary for
    # puzzle # 5
    url(r'^puzzle/reset/dictionary/(?P<pk>[0-9]+)/$', reset_dictionary,
        name='dictionary_reset', ),

]

# EOF
