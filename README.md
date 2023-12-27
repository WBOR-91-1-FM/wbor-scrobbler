# wbor-scrobbler

This is a program that uses the Spinitron and Last.fm APIs to take now-playing songs from a radio station on Spinitron and "scrobble" them to a Last.fm account. It was originally written by WKNC for [their station's Last.fm account](https://www.last.fm/user/wknc881). This fork adds a Docker image for easy use within our streaming server.

## Requirements

* A Last.fm account and API application. Create an API app [here](https://www.last.fm/api/account/create) if necessary.
* Admin access to the [Spinitron](https://spinitron.com/) web app corresponding to the scrobbling station.
* [Docker](https://www.docker.com/) version 24.0.7 (mileage may vary on newer versions)

## Installation

1. Navigate to the directory you want to setup in, and then run:

    ```text
    git clone https://github.com/mdrxy/wbor-scrobbler.git && cd wbor-scrobbler && cd env && nano .env
    ```

2. Enter the following values (in the format `KEY=VAL` seperated by newline):
    * LASTFM_API_KEY: Found on your [Last.fm API accounts page](https://www.last.fm/api/accounts) under "API Key"
    * LASTFM_API_SECRET: Found on your [Last.fm API accounts page](https://www.last.fm/api/accounts) under "Shared Secret"
    * SPINITRON_API_KEY: Found on the [Spinitron automation and API page](https://spinitron.com/station/automation/panel) under "API Key"
    * The resulting `.env` file shoud look similar to the following:

        ```text
        LASTFM_API_KEY=fndvnbufhjbkcxghudf
        LASTFM_API_SECRET=vbhcxjbvdkslgnmkjdsn
        SPINITRON_API_KEY=eriugdfnjkgbdfjk
        ```

    * Once you've entered these, press `ctrl + x` and then enter `y` then `enter` to save.

3. Build the docker image. Run:

    ```text
    cd .. && docker build --no-cache -t scrobbler .
    ```

4. Assuming the image was built successfully, you can now spin up a container to complete setup. Run:

    ```text
    docker run -v "$(pwd)"/env:/env -p 4000:80 -it --name scrobbler scrobbler
    ```

5. Navigate to the Last.fm url presented (in some terminals you can cmd + click the URL) and authorize the application by pressing "allow access." Return to the terminal and enter `y` followed by `enter`

## Usage

* To stop scrobbling, run `docker stop scrobbler`
