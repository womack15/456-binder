[UPDATED 11/22/16 1:30pm]

To run binder.py:

In terminal type "python binder.py Prog1 Prog2 ... ProgN"

The program will create an executable file that combines Prog1 Prog2 ... ProgN. It generates "codearray.h" in the proper form according to section 1(b) of the prompt.

***NOTES***
The code needs some error checking in some places.

[FIXED] The actual size of the file and the size given by the function and python appear to be different. 

To print out the actual binary hex you can do:

headerFile.write(str(temp))

However, it is very likely that your system will freeze when trying to open the header file to view the values.  Seems to work when displaying in the Terminal, however.
