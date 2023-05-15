#!/usr/bin/env python
import re
import sys

if len(sys.argv) > 1:
    filename = sys.argv[1]
    # Use the filename variable for further processing
    print("Filename:", filename)
    with open(filename, 'r') as file:
        content = file.read()

    # Use regular expressions to fix indentation
    fixed_content = ""
    for line in content.splitlines():
        heading = True
        newline = ''
        for char in line:
            if char != ' ' or not heading:
                heading = False
                newline = newline + char

        fixed_content = fixed_content + newline + '\n'

    with open(filename, 'w') as file:
        file.write(fixed_content)
else:
    print("Please provide a filename as an argument to this script")
    sys.exit(1)


