#! /usr/bin/env python
"""
autoEdit - A Python tool to automatically edit a set of files
           according to the specified user rules:

           1) Discard module files

           2) Rename module names in subroutines

Written by Andre C. Marta          Last updated: Apr 6, 2007

"""

# Import modules

import os
import sys

# Specify file extension

EXT = "_d.f90"

DIR_ORI = sys.argv[1]
DIR_MOD = sys.argv[2]

# Specifiy the list of LINE ID's to find, what to replace and with what

# First set: Find line with 'USE' and replace "_D" with ''
LINE_ID = ["USE"]
STR_OLD = ["_D"]
STR_NEW = [""]

STR_REPLACE_ALL = {"_CD": ""}
# Also, entirely ignore lines with these strings:
LINE_IGNORE = []
FILE_IGNORE = ["gridData_d.f90", "kd_tree_d.f90", "warpMesh_d.f90"]
# Some feedback

print("Directory of input source files  :", DIR_ORI)
print("Directory of output source files :", DIR_MOD)

for f in os.listdir(DIR_ORI):
    if f not in FILE_IGNORE:
        if f.endswith(EXT):
            # open original file in read mode
            file_object_ori = open(DIR_ORI + "/" + f, "r")
            print("\nParsing input file", file_object_ori.name)

            # read to whole file to string and reposition the pointer
            # at the first byte for future reading
            all_src = file_object_ori.read()
            file_object_ori.seek(0)

            # open modified file in write mode
            file_object_mod = open(DIR_MOD + "/" + f, "w")

            # read the original file, line-by-line
            nEdits = len(LINE_ID)
            nIgnores = len(LINE_IGNORE)

            for line in file_object_ori:
                # parse original line for relevante identifier
                # and replace the string
                line_mod = line.lstrip()  # Strip out Left-hand leading spaces

                found_ignore = False
                for i in range(nIgnores):
                    if line_mod.find(LINE_IGNORE[i]) >= 0:
                        found_ignore = True
                    # end if
                # end for

                if not found_ignore:
                    for i in range(nEdits):
                        if line_mod[0 : len(LINE_ID[i])] == LINE_ID[i]:
                            line_mod = line_mod.replace(STR_OLD[i], STR_NEW[i])
                        # end if
                    # end for
                # end if

                for key in STR_REPLACE_ALL:
                    line_mod = line_mod.replace(key, STR_REPLACE_ALL[key])
                # end for

                # write the modified line to new file
                file_object_mod.write("   " + line_mod)

            # close the files
            file_object_ori.close()
            file_object_mod.close()

            # success message
            print(" Modified file saved", file_object_mod.name)
