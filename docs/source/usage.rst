.. _`usage`

********************
WordTrekSolver Usage
********************

WordTrekSolver is written using Django - a web framework

Command Line Invocation
=======================

command line


Animal List
===========

The first screen that comes up is the Animal and Daily Quest List screen.
It shows the list of all `animal`_\ s and `daily quest`_\ s
that have
previously been
entered, as well as some special options.

Animal/Daily Quest Management
-----------------------------

You can add an animal or daily quest by choosing the "Add Animal or Daily
Quest" button.  To edit an animal or daily quest, choose the "Edit" button
across from the name of the animal or daily quest to be edited. To delete
an animal or daily quest, choose the "Delete" button.  Note - deleting an
animal or daily quest will delete all the puzzles, answers, and answer
letters associated with it.


Special Options
---------------

There are four special options available at the top of the screen.

-   Reset Puzzle - this resets internal markers and clears the :doc:`word
queue` of
    any remaining potential `answer`\ s.

        - animal/DQ add
        - animal edit
        - animal delete
        - reset puzzle
        - dictionary check on/off
        - vowel check on/off

    - animal detail
        - puzzle add/edit/delete

    - puzzle detail
        - answer add/edit/delete
        - solve this word
        - reset puzzle
        - flip dictionary check

    - answer detail
        - answer letter add/edit/delete

Section
=======


Sub-Section
-----------


Sub-Sub-Section
^^^^^^^^^^^^^^^


Paragraph
"""""""""

Official list of Python heading levels

    - # with overline, for parts
    - \* with overline, for chapters
    - = for sections
    - \- for subsections
    - ^ for subsubsections
    - " for paragraphs


Blah blah *italics*  **bold**

This is a numbered list

    1. Numbered items
    #. Numbered items
    #. Period can be replaced by a dash, right paren, etc., but is required.

This is a bulleted list
    - Bulleted items
    - Bulleted items
        - sublist items
    
Show an indented literal text block like this:

::

    literal text
    ...

Text indented the same as the "::" marker ends the literal text

A simple sample Table

============   ========================
Cell Title     Another Cell  Title
============   ========================
contents       more contents
item 1         item 2
green          purple
============   ========================

A grid table

+---------------+--------------+--------------+
| Header Col 1  | Header 2     |   Centered   |
| Extended      |              |   Header     |
+===============+==============+==============+
| Body 1        |   Body 2     |       Body 3 |
+---------------+--------------+--------------+
| Left Just     |   Centered   |   Right Just |
+---------------+--------------+--------------+
| This entry spans these cols  | This entry   |
+---------------+--------------+              +
| Blah          | Blah         | spans rows   |
+---------------+--------------+--------------+

Link to external URL: `Apple main web site <http://www.apple.com>`_ that way.

Reference to a reference elsewhere in the same document:  `Link to elsewhere`_

Blah blah

    _`Link to elsewhere`   <-- This is the target of the link above.
  
To reference another document use

    :doc:`title <doc name and location>`
    
    There must NOT be a space between the : and the backtick!
    
    Can also use :any: - it will try to do :doc:, :ref:, etc.
    
        If not found, will then try to find a Python object with that name 
        and link to it (e.g. class name, function name, module name, etc.)

To add a glossary, prefix it with the lines below.  To have the glossary
automatically sorted, use the :Sorted: Parameter as shown and indent the
terms so the beginning of the term lines up with the "G" in glossary.

..  glossary::
    :sorted:

    Glossary-type definition
        The definition for the term must be indented and immediately below
        the term.

        Blank lines may appear in the definition body, but must not
        come between the term and the first line of definition.

        Each term must have a blank line separating is from the previous
        definition.

    Glossary reference
        The term defined can be referenced elsewhere by :term:,
        e.g. :term:Glossary-type definition


145 * 23.98
