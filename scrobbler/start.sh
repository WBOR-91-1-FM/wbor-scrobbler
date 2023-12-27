#!/bin/bash

# If setup hasn't been completed
if [ ! -e /env/setup_done ]; then
    echo "start.sh: Running initial setup..."
    python scrobbler.py --setup
    
    if [ -e /env/setup_done ]; then
        echo "start.sh: Setup completed successfully. Reboot the container to begin runnning scrobbler."
    else
        echo "start.sh: Setup failed. Please check the logs for details."
        exit 1
    fi
fi

# Assuming setup has been done, start the scrobbler
exec python scrobbler.py