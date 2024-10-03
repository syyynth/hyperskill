#!/usr/bin/bash

menu() {
    echo
    echo "Select an option"
    echo "0. Type '0' or 'quit' to end program"
    echo "1. Convert units"
    echo "2. Add a definition"
    echo "3. Delete a definition"
}

is_valid_number() {
    [[ $1 =~ ^-?[0-9]+(\.[0-9]+)?$ ]]
}

is_valid_name() {
    [[ $1 =~ ^[a-zA-Z]+_to_[a-zA-Z]+$ ]]
}

is_valid_definition() {
    local arr=("$@")
    [[ ${#arr[@]} -eq 2 ]] && is_valid_name "${arr[0]}" && is_valid_number "${arr[1]}"
}

add_definition() {
    while true; do
        echo "Enter a definition:"
        read -a definition

        is_valid_definition "${definition[@]}" && break

        echo "The definition is incorrect!"
    done

    echo "${definition[@]}" >>definitions.txt

}

remove_definition() {
    local file=definitions.txt def_count

    if [ ! -s "$file" ]; then
        echo "Please add a definition first!"
    else
        echo "Type the line number to delete or '0' to return"

        nl -s ". " -w 1 "$file"

        def_count=$(wc -l <"$file")

        read -r ltod

        until [[ $ltod =~ ^[0-9]+$ && $ltod -ge 0 && $ltod -le $def_count ]]; do
            echo "Enter a valid line number!"
            read -r ltod
        done

        [[ $ltod -eq 0 ]] && return 0

        sed -i "${ltod}d" "$file"

    fi
}

convert() {
    local file=definitions.txt def_count

    if [ ! -s "$file" ]; then
        echo "Please add a definition first!"
    else
        echo "Type the line number to convert units or '0' to return"

        nl -s ". " -w 1 "$file"
        def_count=$(wc -l <"$file")

        read -r ltod

        until [[ $ltod =~ ^[0-9]+$ && $ltod -ge 0 && $ltod -le $def_count ]]; do
            echo "Enter a valid line number!"
            read -r ltod
        done

        [[ $ltod -eq 0 ]] && return 0

        line=$(sed "${ltod}!d" "$file")
        read -a def <<<"$line"

        echo "Enter a value to convert:"

        read -r value

        until is_valid_number "$value"; do
            echo "Enter a float or integer value!"
            read -r value
        done

        result=$(echo "scale=2; ${def[1]} * $value" | bc -l)
        echo "Result: $result"

    fi
}

echo "Welcome to the Simple converter!"

while true; do
    menu
    read -r option

    case "${option}" in
    0 | quit)
        echo "Goodbye!"
        break
        ;;
    1)
        convert
        ;;
    2)
        add_definition
        ;;
    3)
        remove_definition
        ;;
    *)
        echo "Invalid option!"
        ;;
    esac
done
