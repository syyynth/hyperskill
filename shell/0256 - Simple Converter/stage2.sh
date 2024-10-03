#!/usr/bin/bash

is_valid_number() {
    [[ $1 =~ ^-?[0-9]+(\.[0-9]+)?$ ]]
}

echo "Enter a definition:"
read -a definition

if [[ ${#definition[@]} -eq 2 && ${definition[0]} =~ ^[a-zA-Z]+_to_[a-zA-Z]+$ ]] && is_valid_number "${definition[1]}"; then
    echo "Enter a value to convert:"
    read value

    until is_valid_number "$value"; do
        echo "Enter a float or integer value!"
        read value
    done

    result=$(echo "scale=2; ${definition[1]} * $value" | bc -l)
    echo "Result: $result"
else
    echo "The definition is incorrect!"
fi
