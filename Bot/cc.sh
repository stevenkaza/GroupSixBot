#!/bin/bash
find . -type d -exec bash -c "pushd {} ; gcc -Wall -pedantic -std=c99 program7.c -o run > compile.log 2>&1 ; styleCheck <<< "program7.c" ; popd" \;