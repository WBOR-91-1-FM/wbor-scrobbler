#!/bin/bash

# Check if the setup has been done
if [ ! -e /scrobbler/setup_done ]; then
    # Perform setup
    python scrobbler.py --setup
fi

while [ ! -e "/scrobbler/setup_done" ]; do
    echo "Waiting for setup to complete..."
    sleep 5  # Adjust the sleep duration as needed
done

# Run the main application
exec python scrobbler.py
