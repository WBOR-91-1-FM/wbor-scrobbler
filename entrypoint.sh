#!/bin/bash

python scrobbler.py --setup

while [ ! -e "/scrobbler/setup_done" ]; do
    echo "Waiting for setup to complete..."
    sleep 5  # Adjust the sleep duration as needed
done

# Run the main application
exec python scrobbler.py
