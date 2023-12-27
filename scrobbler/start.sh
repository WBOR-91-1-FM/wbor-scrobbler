#!/bin/bash

# If setup hasn't been completed
if [ ! -e /env/setup_done ]; then
    printf "\e[34mstart.sh: Running initial setup...\e[0m\n"
    python scrobbler.py --setup
    
    if [ -e /env/setup_done ]; then
        printf "\e[34mstart.sh: Setup completed successfully. Reboot the container to begin running scrobbler.\e[0m\n"
        exit 0
    else
        printf "\e[91mstart.sh: Setup failed.\e[0m\n"
        exit 1
    fi
fi

# Assuming setup has been done, start the scrobbler
exec python scrobbler.py