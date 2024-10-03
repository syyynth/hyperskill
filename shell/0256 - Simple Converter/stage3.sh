#!/usr/bin/bash

menu() {
    echo "Select an option"
    echo "0. Type '0' or 'quit' to end program"
    echo "1. Convert units"
    echo "2. Add a definition"
    echo "3. Delete a definition"
}

echo "Welcome to the Simple converter!"

while true; do
    menu
    read -r option

    case "${option}" in
    0 | "quit")
        echo "Goodbye!"
        break
        ;;
    1)
        echo "Not implemented!"
        ;;
    2)
        echo "Not implemented!"
        ;;
    3)
        echo "Not implemented!"
        ;;
    *)
        echo "Invalid option!"
        ;;
    esac
done
