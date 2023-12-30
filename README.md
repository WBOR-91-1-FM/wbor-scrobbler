# wbor-scrobbler

This is a script that takes the now-playing song from a [Spinitron](https://spinitron.com/) station and scrobbles it to a [Last.fm](https://www.last.fm/) account. It was originally written by [WKNC](https://wknc.org/) for [their station's Last.fm account](https://www.last.fm/user/wknc881). I have since configured it at [WBOR 91.1 FM](https://www.wbor.org) ([WBOR on Spinitron](https://spinitron.com/WBOR/) - [Last.fm](https://www.last.fm/user/wbor)) with a few modifications.

In this fork, I Dockerized the original script and wrote a more streamlined setup process so that other station managers who may not be as technically inclined can hopefully implement it without much friction.

## Requirements

* A Last.fm account and API application. Create an API app [here](https://www.last.fm/api/account/create) if you haven't already done so. **Make sure to log in to Last.fm with the account you plan to scrobble to.**
* Admin login to the [Spinitron](https://spinitron.com/) account corresponding to the station that plans to scrobble.
* Some kind of Linux server environment (WBOR is running it on a Virtual Private Server (VPS) at Digital Ocean using Ubuntu 22.04.3 at the time of this writing)
  * [Docker](https://www.docker.com/) version 24.0.7 (at the time of this writing -- your mileage may vary on newer versions)

## Installation & Setup

After you've gone through the following setup process once, you theoretically shouldn't need to ever repeat it! Neat.

1. In terminal, navigate to the directory you want to set this up in, and then run:

    ```text
    git clone https://github.com/mdrxy/wbor-scrobbler.git && cd wbor-scrobbler && cd env && nano .env
    ```

    * Clones the repository, navigates to its folder, and opens the .env needed for editing in step 2.

2. In .env, enter the following values after the `=` (without a space):
    * LASTFM_API_KEY: Found on your [Last.fm API accounts page](https://www.last.fm/api/accounts) under "API Key"
    * LASTFM_API_SECRET: Found on your [Last.fm API accounts page](https://www.last.fm/api/accounts) under "Shared Secret"
    * SPINITRON_API_KEY: Found on the [Spinitron automation and API page](https://spinitron.com/station/automation/panel) under "API Key"
    * The resulting `.env` file shoud look something like the following:

        ```text
        LASTFM_API_KEY=7AtTWxDq3ho9AEwjiuMjAdYPkoyUHgFH
        LASTFM_API_SECRET=nwZvxiCbx28dAAwswQETeBjjyhMz6LFf
        SPINITRON_API_KEY=HjeZczCFkQ87RghvJXMHvGVn
        ```

    * Once entered, press <kbd>ctrl</kbd> + <kbd>x</kbd> and then enter <kbd>y</kbd> then <kbd>enter</kbd> to save and exit.

3. Build the docker image. Run:

    ```text
    cd .. && docker build --no-cache -t scrobbler .
    ```

    * Navigates to the repo's root folder and creates a Docker image titled `scrobbler`
        * You are free to give the image a title other than `scrobbler` but note that you will need to adjust the code in the following steps accordingly.

4. Assuming the image was built successfully, you can now spin up a container to complete setup. Run:

    ```text
    docker run -v "$(pwd)"/env:/env -p 4000:80 -it --name scrobbler --restart unless-stopped scrobbler
    ```

    * Creates and starts a container titled `scrobbler` in interactive terminal mode for the initial setup process. Same as above: you are free to give the container a title other than `scrobbler` but note that you will need to adjust the code in the following steps accordingly.
    * In the case of a server reboot or a script failure, the container `scrobbler` will immediately restart, and will continue to do so unless you explicitly stop the container (more below).
    * Maps to external port 4000 by default, however you can change this as needed depending on your installation environment.

5. Navigate to the Last.fm url presented to you (in some terminals you can cmd + click the URL) and authorize the application by pressing "allow access." Return to the terminal and enter <kbd>y</kbd> followed by <kbd>enter</kbd>.

6. Following setup, the container `scrobbler` will immediately begin running in the background, so no further action is required!

## Usage

* To stop/start the script's container for any reason, run `docker stop scrobbler` and `docker start scrobbler` respectively.
  * Scrobbling is started in the background by default. If you want to run it in the foreground to see realtime output from the script (to see what's happening), add the `-i` flag between `start` and `scrobbler`. NOTE: once you've started `scrobbler` in the foreground, the only way to hide its output again is to stop the process and start it without the `-i` flag.
* Like mentioned in part 4 of "Installation & Setup," in the case of a server reboot or a script failure, the container `scrobbler` will immediately restart without needing to run through the setup process again.

## Troubleshooting

* If you accidentally removed the `scrobbler` docker container, create a new one by navigating to the location you cloned this repo to (important!) and running:

    ```text
    docker run -v "$(pwd)"/env:/env -p 4000:80 -d --name scrobbler --restart unless-stopped scrobbler
    ```

  * Runs the container in the background this time since you've already gone through the initial setup process.
