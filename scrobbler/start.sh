#!/bin/bash

# If setup hasn't been completed
if [ ! -e /env/setup_done ]; then
    echo "Running initial setup..."
    python scrobbler.py --setup
    
    if [ -e /env/setup_done ]; then
        echo "Setup completed successfully."
    else
        echo "Setup failed. Please check the logs for details."
        exit 1
    fi
fi

# Start the scrobbler
echo "Starting scrobbler."
exec python scrobbler.py