# wbor-scrobbler

This is a program that uses the Spinitron and Last.fm APIs to take live songs from a radio station on Spinitron and "scrobble" it to a Last.fm account. It was originally written by WKNC for [their station's Last.fm account](https://www.last.fm/user/wknc881).

## Requirements

* Requires a Last.fm account and API application. Create an API app [here](https://www.last.fm/api/account/create) if necessary. For more information on authentication with the Last.fm API, look [here](https://www.last.fm/api/authentication). Also requires admin access to the Spinitron web app for WBOR.
* Python >=3.11: <https://www.python.org/>  
* .env file with the following values:

1. LASTFM_API_KEY: Found on your [Last.fm API accounts page](https://www.last.fm/api/accounts) under "API Key"
2. LASTFM_API_SECRET: Found on your [Last.fm API accounts page](https://www.last.fm/api/accounts) under "Shared Secret"
3. SPINITRON_API_KEY: Found on the [Spinitron automation and API page](https://spinitron.com/station/automation/panel) under "API Key"

## Installation

1. Clone the project from the repository
2. Navigate to cloned folder in a terminal
3. Execute 'pip install -r requirements.txt' to install packages
4. Execute 'python scrobbler.py --setup'
5. When prompted, authorize the application while logged into the wbor Last.fm account

## Usage

After initial setup, to begin scrobbling, simply:

1. Navigate to the project folder in a terminal
2. Execute 'python scrobbler.py'
