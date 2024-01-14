#!/bin/bash

N=$1
directory=$2

generate_random_filename() {
    echo $((RANDOM % 512)).txt
}

generate_random_permission() {
    echo $((RANDOM % 8))$((RANDOM % 8))$((RANDOM % 8))
}

mkdir -p "$directory"

for ((i=0; i<N; i++)); do
    filename=$(generate_random_filename)
    touch "$directory/$filename"
    perm=$(generate_random_permission)
    chmod "$perm" "$directory/$filename"
done
