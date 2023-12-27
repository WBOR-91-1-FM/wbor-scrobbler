# wbor-scrobbler

This is a program that uses the Spinitron and Last.fm APIs to take now-playing songs from a radio station on Spinitron and "scrobble" them to a Last.fm account. It was originally written by WKNC for [their station's Last.fm account](https://www.last.fm/user/wknc881). This fork adds a Docker image for easy use within our streaming server.

## Requirements

* A Last.fm account and API application. Create an API app [here](https://www.last.fm/api/account/create) if necessary.
* Admin access to the [Spinitron](https://spinitron.com/) web app corresponding to the scrobbling station.
* [Docker](https://www.docker.com/) version 24.0.7 or greater

## Installation

Execute 'pip install -r requirements.txt' to install packages
Execute 'python scrobbler.py --setup'
When prompted, authorize the application while logged into the wbor Last.fm account

* .env file with the following values:
  * LASTFM_API_KEY: Found on your [Last.fm API accounts page](https://www.last.fm/api/accounts) under "API Key"
  * LASTFM_API_SECRET: Found on your [Last.fm API accounts page](https://www.last.fm/api/accounts) under "Shared Secret"
  * SPINITRON_API_KEY: Found on the [Spinitron automation and API page](https://spinitron.com/station/automation/panel) under "API Key"

## Usage

After initial setup, to begin scrobbling, simply:

1. Navigate to the project folder in a terminal
2. Execute 'python scrobbler.py'
