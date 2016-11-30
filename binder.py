'''
Micah Geertson
Joshua Womack
CPSC 456 - Assignment 2
Professor Gofman
Due: 25 November 2016
'''

import sys
from subprocess import Popen, PIPE

# The header file name
FILE_NAME = "codearray.h"


###########################################################
# Returns the hexidecimal dump of a particular binary file
# @execPath - the executable path
# @return - returns the hexidecimal string representing
# the bytes of the program. The string has format:
# byte1,byte2,byte3....byten,
# For example, 0x19,0x12,0x45,0xda,
##########################################################
def getHexDump(execPath):
    # The return value
    retVal = None

    # 1. Use popen() in order to run hexdump and grab the hexadecimal bytes of the program.
    # 2. If hexdump ran successfully, return the string retrieved. Otherwise, return None.
    # The command for hexdump to return the list of bytes in the program in C++ byte format
    # the command is hexdump -v -e '"0x" 1/1 "%02X" ","' progName

    process = Popen(["hexdump", "-v", "-e", '"0x" 1/1 "%02X" ","', execPath], stdout=PIPE)

    (output, err) = process.communicate()
    #print("Path: {}".format(execPath))
    #print("Size: {}\n".format(sys.getsizeof(output)))
    # print("Output: {}".format(output[len(output) - 1]))
    # print("Err: {}".format(err))
    if err is None:
        retVal = output[:-1]  # Removes last comma from the string of hex numbers

    return retVal


###################################################################
# Generates the header file containing an array of executable codes
# @param execList - the list of executables
# @param fileName - the header file to which to write data
###################################################################

def generateHeaderFile(execList, fileName):
    # The program array
    progNames = sys.argv

    # Open the header file -- THIS WILL CREATE A "codeArray.h" FILE and WRITE TO IT
    headerFile = open(fileName, "w")

    # The lengths of programs
    progLens = []

    # Write the array name to the header file
    headerFile.write("#include <string>\n\nusing namespace std;\n\n"
                     "unsigned char* codeArray[" + str(len(execList)) + "] = {")

    # For each program progName we should run getHexDump() and get the
    # the string of bytes formatted according to C++ conventions. That is, each
    # byte of the program will be a two-digit hexadecimal value prefixed with 0x.
    # For example, 0xab. Each such byte should be added to the array codeArray in
    # the C++ header file. After this loop executes, the header file should contain
    # an array of the following format:
    # 1. unsigned char* codeArray[] = {new char[<number of bytes in prog1>{prog1byte1, prog1byte2.....},
    # 				   new char[<number of bytes in prog2><{prog2byte1, progbyte2,....},
    #					........
    #				};

    for progName in range(len(execList)):
        temp = getHexDump(execList[progName])
        progLens.append(sys.getsizeof(temp))
        headerFile.write("new unsigned char[" + str(sys.getsizeof(temp)) + "]{" + temp)
        if progName < len(execList) - 1:
            headerFile.write("}, \n")
        else:
            headerFile.write("}")

    headerFile.write("};")

    # Add array to containing program lengths to the header file
    headerFile.write("\n\nunsigned programLengths[] = {")

    # Add to the array in the header file the sizes of each program.
    # That is the first element is the size of program 1, the second element
    # is the size of program 2, etc.
    for i in range(len(progLens)):
        if i < len(progLens) - 1:
            headerFile.write(str(progLens[i]) + ", ")
        else:
            headerFile.write(str(progLens[i]))
    headerFile.write("};")

    # Write the number of programs.
    headerFile.write("\n\n#define NUM_BINARIES " + str(len(progNames) - 1))

    # Close the header file
    headerFile.close()


############################################################
# Compiles the combined binaries
# @param binderCppFileName - the name of the C++ binder file
# @param execName - the executable file name
############################################################
def compileFile(binderCppFileName, execName):  # ***** START HERE ***** #
    print("Compiling...")

    # Run the process
    # Run the g++ compiler in order to compile backbinder.cpp
    # If the compilation succeeds, print "Compilation succeeded"
    # If compilation failed, then print "Compilation failed"
    # Do not forget to add -std=gnu++11 flag to your compilation line
    process = Popen(["g++", binderCppFileName, "-o", execName, "-std=gnu++11"], stdout=PIPE)

    (output, err) = process.communicate()

    #print ("Process output: {}".format(output))
    #print ("Process err: {}".format(err))

    if process.wait() != 0:
        print("Compilation failed")
    else:
        print("Compilation Succeeded")


generateHeaderFile(sys.argv[1:], FILE_NAME)
compileFile("binderbackend.cpp", "bound")
