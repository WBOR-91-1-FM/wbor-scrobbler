# wbor-scrobbler

This is a script that uses the Spinitron and Last.fm APIs to take now-playing songs from WBOR 91.1 FM on Spinitron and "scrobble" them to our Last.fm account. It was originally written by WKNC for [their station's Last.fm account](https://www.last.fm/user/wknc881). This fork creates a Docker image and streamlined setup process for easy use within our streaming server and installation in other Docker environments.

## Requirements

* A Last.fm account and API application. Create an API app [here](https://www.last.fm/api/account/create) if you haven't already done so.
* Admin access to the [Spinitron](https://spinitron.com/) web app corresponding to the scrobbling station.
* [Docker](https://www.docker.com/) version 24.0.7 (mileage may vary on newer versions)

## Installation & Setup

After you've gone through this setup process once, you theoretically shouldn't need to ever repeat it! Neat.

1. In terminal, navigate to the directory you want to set this up in, and then run:

    ```text
    git clone https://github.com/mdrxy/wbor-scrobbler.git && cd wbor-scrobbler && cd env && nano .env
    ```

    * Clones the repository, navigates to its folder, and opens the .env for editing in step 2.

2. Enter the following values after the `=` (without a space):
    * LASTFM_API_KEY: Found on your [Last.fm API accounts page](https://www.last.fm/api/accounts) under "API Key"
    * LASTFM_API_SECRET: Found on your [Last.fm API accounts page](https://www.last.fm/api/accounts) under "Shared Secret"
    * SPINITRON_API_KEY: Found on the [Spinitron automation and API page](https://spinitron.com/station/automation/panel) under "API Key"
    * The resulting `.env` file shoud look something like the following:

        ```text
        LASTFM_API_KEY=fndvnbufhjbkcxghudfdiyt
        LASTFM_API_SECRET=vbhcxjbvdkslgnmkjdsnvpxc
        SPINITRON_API_KEY=eriugdfnjkgbdfjkrewm
        ```

    * Once entered, press `ctrl + x` and then enter `y` then `enter` to save and exit.

3. Build the docker image. Run:

    ```text
    cd .. && docker build --no-cache -t scrobbler .
    ```

    * Navigates to the repo's root folder and creates a Docker image titled `scrobbler`

4. Assuming the image was built successfully, you can now spin up a container to complete setup. Run:

    ```text
    docker run -v "$(pwd)"/env:/env -p 4000:80 -it --name scrobbler --restart unless-stopped scrobbler
    ```

    * Creates and starts a container titled `scrobbler` in interactive terminal mode for the initial setup process.
    * In the case of a server reboot or a script failure, `scrobbler` will immediately restart, and will continue to do so unless you explicitly stop the container (more below).
    * Maps to external port 4000 by default, however you can change this as needed depending on your installation environment.

5. Navigate to the Last.fm url presented on screen (in some terminals you can cmd + click the URL) and authorize the application by pressing "allow access." Return to the terminal and enter `y` followed by `enter`.

6. Following setup, `scrobbler` will immediately begin running in the background, so no further action is required!

## Usage

* To stop/start scrobbling for any reason, run `docker stop scrobbler` and `docker start scrobbler` respectively.
  * Scrobbling is started in the background by default. If you want to run it in the foreground to see realtime output from the script (to see what's happening), add the `-i` flag between `start` and `scrobbler`. NOTE: once you've started `scrobbler` in the foreground, the only way to hide its output again is to stop the process and start it without the `-i` flag.
* Like mentioned in part 4 of "Installation & Setup," in the case of a server reboot or a script failure, `scrobbler` will immediately restart without needing to run through the setup process again.

## Troubleshooting

* If you accidentally removed the `scrobbler` docker container, create a new one by navigating to the location you cloned this repo to (important!) and running:

    ```text
    docker run -v "$(pwd)"/env:/env -p 4000:80 -d --name scrobbler --restart unless-stopped scrobbler
    ```

  * Runs the container in the background this time since you've already gone through the initial setup process.
