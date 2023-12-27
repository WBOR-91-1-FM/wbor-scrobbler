# wbor-scrobbler

This is a program that uses the Spinitron and Last.fm APIs to take now-playing songs from a radio station on Spinitron and "scrobble" them to a Last.fm account. It was originally written by WKNC for [their station's Last.fm account](https://www.last.fm/user/wknc881). This fork adds a Docker image for easy use within our streaming server.

## Requirements

* A Last.fm account and API application. Create an API app [here](https://www.last.fm/api/account/create) if necessary.
* Admin access to the [Spinitron](https://spinitron.com/) web app corresponding to the scrobbling station.
* [Docker](https://www.docker.com/) version 24.0.7 or greater

## Installation

1. Clone this repository to your desired destination
2. At this destination, make a folder called env
3. In this folder, create the file `.env` and enter the following values (in the format `KEY=VAL`):
    * LASTFM_API_KEY: Found on your [Last.fm API accounts page](https://www.last.fm/api/accounts) under "API Key"
    * LASTFM_API_SECRET: Found on your [Last.fm API accounts page](https://www.last.fm/api/accounts) under "Shared Secret"
    * SPINITRON_API_KEY: Found on the [Spinitron automation and API page](https://spinitron.com/station/automation/panel) under "API Key"
    * The resulting `.env` shoud look similar to the following:

        ```text
        LASTFM_API_KEY=ABCDEFG
        LASTFM_API_SECRET=HIJKLMN
        SPINITRON_API_KEY=OPQRSTU
        ```
      


Build the docker image by running `docker build -t scrobbler .`

Spin up a container from this new image by running `docker run -v /var/scrobbler/env:/env -p 4000:80 --name scrobbler_container scrobbler`


## Usage


