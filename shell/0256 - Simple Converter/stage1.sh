#!/usr/bin/bash

echo "Enter a definition:"
read -a u

if [[ ${#u[@]} -eq 2 && ${u[0]} =~ ^[a-zA-Z]+_to_[a-zA-Z]+$ && ${u[1]} =~ ^-?[0-9]+(\.[0-9]+)?$ ]]; then
    echo "The definition is correct!"
else
    echo "The definition is incorrect!"
fi
