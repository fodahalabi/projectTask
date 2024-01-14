#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Error: Please provide a valid number for the number of files."
    exit 1
fi

if ! [[ $1 =~ ^[0-9]+$ ]]; then
    echo "Error: The provided argument is not a valid number."
    exit 1
fi

num_files=$1
for ((i = 0; i < num_files; i++)); do
    file_name="${i}.txt"
    touch "$file_name"
done

echo "Generated $num_files files with names like 0.txt, 1.txt, etc."


for ((i = 0; i < $1; i++)); do
    touch "${i}.txt"
    chmod +rwx "${i}.txt"
done

for ((i = 0; i < $1; i++)); do
    file_name="${i}.txt"
    if [ -e "$file_name" ]; then
        if [ -r "$file_name" ] && [ -w "$file_name" ] && [ -x "$file_name" ]; then
            echo "File $file_name has read, write, and execute permissions."
        else
            echo "Error: File $file_name does not have the expected permissions."
        fi
    else
        echo "Error: File $file_name does not exist."
    fi
done