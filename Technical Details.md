# WordTrek Solver Technical Details

## Gui Interface
This tool uses Django to present a web site on the local host.

## Database
By default this tool uses Sqlite to store the levels (animals) the letters 
in each grid, and the answers chosen  -- all of which must be typed in.

## Methodology Used
For a given puzzle and a specific answer to solve, the tool finds all 
possible letter combinations from the available letters.  It runs each 
combination past a dictionary (aspell or hunspell).  Each combination 
of letters that pass the dictionary check are stored in a cache in the 
database and presented to the user, one at a time.  If the user indicates 
that the commbination is the correct word (by trying it out in the app), 
the solution is stored in the database.  That word is stored in the 
database and the letters of that puzzle are removed from the grid.  Any 
letters above the letter are dropped down to match the app.

In order to speed up the process of selecting possible words and get around 
the limitations of the GIL, the 
multiprocessing library is invoked so that multiple cores are used 
simultaneously.  The maximum number of cores used is set by a constant in 
the code.  I found that setting that limit to one less than the actual 
number of cores was optimal.

Each letter in the search is found by using recursion and deep copies.  The 
limitation of this was that when searching for 17 letter words or so, this 
technique used up a great deal of memory.  In fact, the tool could use up 
all of the available memmory on a 16 GB machine, which caused it to croak.

I better algorithm might be to replace the recursion with pushing each pass 
to a queue and pulling the next attempt to find a letter off the other end 
when a core is available to process it.
