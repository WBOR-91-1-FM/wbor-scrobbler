#!/bin/bash

while true; do
    if [ -e /env/setup_done ]; then
        echo "Starting scrobbler."
        exec python scrobbler.py
    else
        echo "Setup needs to be completed."
    fi

    # Optional: Add a sleep to avoid high CPU usage in the loop
    sleep 5
done