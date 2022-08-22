########
Overview
########

WordTrekSolver is a program to assist in solving the WordTrek app available
for IOS (and possibly for Android).

:doc:`Installation instructions <installation>`

:doc:`WordTrekSolver Usage <usage>`

Outline

   - Approach
   - What didn't work
      - modifying the data before saving it
      - django debugtoolbar
-   what causes other things to be skipped
-   places where a change will cause a "mystery" error page
-   performance
-   installation
-   requirements
-   project layout
-   app layout
-   template strategy
-   css
-   usage instructions
-   my inexperience with:
    -   Django
    -   html
    -   css
    -   debugtoolbar
    -   sphinx
-   Can be used only with a local web site - not ready for the internet
-   Populated database not included
-   Used sqlite db by default


*******
Purpose
*******

WordTrek Solver is designed to assist in solving the WordTrek game available
for iOS (and possibly Android).

The game presents a series of squares filled with letter blocks.  Below each
squares is several sets of empty blocks indicating the number of letters in
each answer.  Solving the puzzle involves passing a finger over each letter in
order.  If the word indicated matches one of the answers, the letter blocks
will drop into one of the sets of blank answer blocks.

Any blocks above the blocks that were removed from the puzzle will drop down
to fill any empty cells.  Thus new combinations of letters become possible.

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

Reference to an internal documentation:  `Link to elsewhere`_

Blah blah

  _`Link to elsewhere`   This is the target of the link above.
