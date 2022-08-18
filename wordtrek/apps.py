"""
apps.py - Define the wordtrek app to Django.
"""
from logging import getLogger, debug, error
from django.apps import AppConfig

__author__ = 'Travis Risner'
__project__ = "WordTrekSolver"
__creation_date__ = "01/06/2017"
# "${CopyRight.py}"

log = getLogger(__name__)


class WordTrekConfig(AppConfig):
    """
    Declare that "wordtrek" is a registered namespace to Django.
    """
    debug('Running WordTrekConfig class')
    name = 'wordtrek'
    verbose_name = 'WordTrek Solver'

# EOF
