#!/bin/bash

# Get list of files to exclude from .gitignore
EXCLUDE=$(cat .gitignore | sed '/^$/d' | sed 's/\./\\\./g' | sed 's/\*/\.\*/g' | tr '\n' '|' | sed 's/|$/\n/')

# Print directory structure excluding files in .gitignore
tree -I "$EXCLUDE"

# Loop through all files in directory
for file in $(find . -type f | grep -Ev "$EXCLUDE")
do
    # Print file name
    echo "'$file'"
    # Print file contents enclosed by triple backticks
    echo '```'
    cat "$file"
    echo ''
    echo '```'
    echo ''
done