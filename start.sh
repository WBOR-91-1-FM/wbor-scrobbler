#!/bin/bash

if [ -e /env/setup_done ]; then
    echo "Starting scrobbler."
    exec python scrobbler.py
else
    echo "Setup needs to be completed."
fi