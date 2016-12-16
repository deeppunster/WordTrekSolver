*****************************
Creation and Modification Log
*****************************

This is a log of what I did and in what order to put this project together.

Initial Setup
=============

Project Requirements
--------------------

Initial requirements are:

1.  PyCharm Professional (2016.3)
#.  Python 3.5
#.  Access to the internet

Initial Steps
-------------

1.  Create a new Django project named "WorkTrekDjango.

    *  Start by using the main Python 3.5 intrepreter for the project. 

#.  Enable the source control of your choice.
#.  Add some directories to it manually.

    a.  behave
    #.  docs
    #.  tests
    #.  venv
    #.  work

#.  Create the virtual environment for this project in venv.

    *   Based on Python 3.5
    *   Added these packages to it:

        #.  Django
        #.  pytest-django
        #.  Sphinx
        #.  django-sphinx
        #.  django-sphinx-autodoc
        #.  behave-django

#.  Run the sphinx-quickstart tool.
#.  Started this log in the docs/source directory as log.rst.
#.  Added entries for "log" and "modules" to the index.rst.
#.  Verify that the WordTrekDjango task works.
#.  Create a sphinx task and verify that it works.
#.  Run the tool "Run manage.py Task...".

    *   startapp wordtrek
    *   This will create the starter files for the Django app itself.

#.  Add a few more directories that will be needed later.

    1.  wordtrek/static
    #.  wordtrek/static/wordtrek
    #.  wordtrek/templates
    #.  wordtrek/templates/admin
    #.  wordtrek/templates/wordtrek

#.  Setup BDD (behave) as desired.
#.  Setup TDD(pytest) as desired.
#.  Modify the settings.py file of the main project by adding this app to 
    the INSTALLED_APPS attribute.  
    *   E.g. "'wordtrek.apps.WordtrekConfig',".
#.  Take a snapshot with the chosen source contol tool.


Setup the database tables and fields
====================================

WordTrek has a list of animals.  Each animal has ten puzzles.  Each puzzle 
has a square block of letters (3 x 3, 4 x 4, etc.).  Each puzzle also has 
one or more empty answer "word" blocks.  The length of each empty word 
block provides a clue about how many letters from the puzzle will be used
up. 

Each day there is a new daily quest of three puzzles.  Solving the three 
puzzles gives the user additonal points (coins) and spins. 

This puzzle solver uses aspell to determine if a sequence of letters is a 
valid word.  If so, the word is stored in a word cache so that it can be
found more quickly the next time.

Steps to create the database tables and fields
----------------------------------------------

1.  Run manage.py with the migrate option to set up the database and the tables
    needed for all Django projects.
    *   E.g. python manage.py migrate.
#.  Create or modify a file under wordtrek called models.py.

    a.  Add a class for each table to be created.
    #.  For each class, add a __str__ method to format a string representation 
        of the fields of one row in that table.
#.  Run manage.py with the makemigrations <app> option.
    *   E.g python manage.py makemigrations wordtrek.
#.  Optionally run manage.py with the sqlmigrate <app> <seq> to see the SQL 
    script that will be used to modify the database for the migration just 
    created.
    *   E.g. python manage.py sqlmigrate wordtrek 0001,
#.  Run manage.py with the migrate option to apply the latest migration to the
    database.
    *   E.g. python manage.py migrate.
#.  Take a snapshot with the chosen source contol tool.


Admin Establishment
===================

Now that we have an application defined (and the database minimally built) we
can set up minimal administration so we can manage the tables, etc. from the
web site.

Setup Admin
-----------

1.  Run manage.py with the createsuperuser option.
    a.  Choose a userid for the superuser.
    #.  Fill in an email address for the superuser.
    #.  Choose a password for the superuser and fill it in twice.

Test Admin
----------

1.  Start the server with the run configuration previously defined in 
    PyCharm.
#.  Open a browser and go to http://127.0.0.1:8000/admin/.
#.  Login using the userid and password created in the previous section.
#.  Optionally add more users and groups if desired.
#.  Take a snapshot with the chosen source contol tool.


Initial App Establishment
=========================

Note: as you make the following changes, it is not necessary to shutdown and 
    restart the server.  Django automatically notices when python code and 
    settings files are changed in PyCharm and restarts the server for you 
    as soon as you switch away from PyCharm.

Add App to Server
-----------------

1.  Modify wordtrek/admin.py by:
    a.  Add import(s) for your top table(s) from .model.
    b.  Register the top table(s) using admin.site.register(<table name>)
        *   E.g. admin.site.register(Animal).
#.  Switch to your browser.
#.  Return to the main admin page or refresh the page.
#.  Observe that the table(s) are not listed under the app setion.
#.  Optionally go to a table and add data if you like. 
#.  Take a snapshot with the chosen source contol tool.


Develop App Web Pages
=====================

Overview
--------

1.  Determine the initial desired layout of the web pages and flow.
2.  Put style sheets (*.css files) and images in the <app>/static/<app>
    directory as they are defined and needed.
3.  Put template html files in the <app>/templates/<app> directory as they are
    defined and needed.
4.  Modify the <app> views.py file to include the logic needed for each web
    page.  


Customzie Admin Pages
=====================

1.  Find the django package under the site-packages direcotry and copy the 
    file base_site.html from contrib/admin/templates/admin to the 
    <app/templates/admin directory.
2.  Add 



-----

Remove the following sample rst stuff when done.

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
