# wbor-scrobbler

This is a script that takes the now-playing song from a [Spinitron](https://spinitron.com/) station and scrobbles it to a [Last.fm](https://www.last.fm/) account. It was originally written by [WKNC](https://wknc.org/) for [their station's Last.fm account](https://www.last.fm/user/wknc881). I have since configured it at [WBOR 91.1 FM](https://www.wbor.org) ([WBOR on Spinitron](https://spinitron.com/WBOR/) - [Last.fm](https://www.last.fm/user/wbor)) with a few modifications.

In this fork, I Dockerized the original script and wrote a more streamlined setup process so that other station managers who may not be as technically inclined can hopefully implement it without much friction.

## Requirements

* A Last.fm account and API application. Create an API app [here](https://www.last.fm/api/account/create) if you haven't already done so. **Make sure to log in to Last.fm with the account you plan to scrobble to.**
* Admin login to the [Spinitron](https://spinitron.com/) account corresponding to the station that plans to scrobble.
* Some kind of Linux server environment (WBOR is running it on a Virtual Private Server (VPS) at Digital Ocean using Ubuntu 22.04.3 at the time of this writing)
  * [Docker](https://www.docker.com/) version 24.0.7 (at the time of this writing -- your mileage may vary on newer versions)
* `nano` or a similar command line text editor such as `vim`. If you choose to use something other than `nano`, you will need to modify the following commands accordingly.

## Installation & Setup

After you've gone through the following setup process once, you theoretically shouldn't need to ever repeat it! Neat.

1. In terminal, navigate to the directory you want to set this up in, and then run:

    ```text
    git clone https://github.com/mdrxy/wbor-scrobbler.git && cd wbor-scrobbler && cd env && nano .env
    ```

    * Clones the repository, navigates to its folder, and opens the .env needed for editing in step 2.

2. In .env, enter the following values after a `=` (without a space):
    * `LASTFM_API_KEY`: Found on your [Last.fm API accounts page](https://www.last.fm/api/accounts) under "API Key"
    * `LASTFM_API_SECRET`: Found on your [Last.fm API accounts page](https://www.last.fm/api/accounts) under "Shared Secret"
    * `SPINITRON_API_KEY`: Found on the [Spinitron automation and API page](https://spinitron.com/station/automation/panel) under "API Key"
    * The resulting `.env` file shoud look something like the following:

        ```text
        LASTFM_API_KEY=7AtTWxDq3ho9AEwjiuMjAdYPkoyUHgFH
        LASTFM_API_SECRET=nwZvxiCbx28dAAwswQETeBjjyhMz6LFf
        SPINITRON_API_KEY=HjeZczCFkQ87RghvJXMHvGVn
        ```

    * Once entered, press <kbd>ctrl</kbd> + <kbd>x</kbd> and then enter <kbd>y</kbd> then <kbd>enter</kbd> to save and exit.

3. Set a scrobbling schedule. By default, it is set to scrobble 24/7, but you can choose a block of time to start/stop scrobbling. Run:

    ```text
    cd .. && cd scrobbler && nano schedule.json
    ```

    * Navigates to the repo's assets folder and opens nano to modify the schdeule.
    * **NOTE:** times are 24-hour UTC. Use a [conversion tool](https://www.worldtimebuddy.com/) to find your time zone in UTC.
    * You are not locked in to this schedule and can [change it at a later date](#changing-the-scrobble-schedule) if you choose.
    * If you are content scrobbling 24 hours a day, press <kbd>ctrl</kbd> + <kbd>x</kbd> and move on to step #4.
    * If you are defining a custom schedule, change the start and end hour, press <kbd>ctrl</kbd> + <kbd>x</kbd> and then enter <kbd>y</kbd> then <kbd>enter</kbd> to save and exit.

4. Build the docker image. Run:

    ```text
    cd .. && docker build --no-cache -t scrobbler .
    ```

    * Navigates to the repo's root folder and creates a Docker image tagged/titled `scrobbler`.
        * You are free to give the image a tag/title other than `scrobbler` but note that you will need to adjust the code in the following steps accordingly.

5. Assuming the image was built successfully, you can now spin up a container to complete setup. Run:

    ```text
    docker run -v "$(pwd)"/env:/env -p 4000:80 -it --name scrobbler --restart unless-stopped scrobbler
    ```

    * Creates and starts a container titled `scrobbler` in interactive terminal mode for the initial setup process. Same as above: you are free to give the container a title other than `scrobbler` but note that you will need to adjust the code in the following steps accordingly.
    * In the case of a server reboot or a script failure, the container `scrobbler` will immediately restart, and will continue to do so unless you explicitly stop the container (more below).
    * Maps to external port 4000 by default, however you can change this as needed depending on your installation environment.

6. Navigate to the Last.fm url presented to you (in some terminals you can <kbd>cmd</kbd> + <kbd>click</kbd> the URL) and authorize the application by pressing "allow access." Return to the terminal and enter <kbd>y</kbd> followed by <kbd>enter</kbd>.

7. Following setup, the container `scrobbler` will immediately begin running in the background, so no further action is required!

## Usage

### Start/Stop

* To stop/start the script's container for any reason, run `docker stop scrobbler` and `docker start scrobbler` respectively.
  * **NOTE:** stopping the container may take 5-10 seconds.
* Like mentioned in part 5 of "Installation & Setup," in the case of a server reboot or a script failure, the container `scrobbler` will immediately restart without needing to run the setup process again.

### Changing the Scrobble Schedule

1. Enter the currently running wbor-scrobbler container. Run:

   ```text
   docker exec -it scrobbler /bin/bash
   ```

   * Opens the container's shell.

2. Edit `schedule.json`. Run:

   ```text
   nano schedule.json
   ```

   * Choose hours to START and STOP scrobbling. These should be in 24-hour UTC format. E.g. 1 PM EST should be entered as 15 for 15:00 UTC. No other integers other than 0-24 are permitted. Once done, press <kbd>ctrl</kbd> + <kbd>x</kbd> and then enter <kbd>y</kbd> then <kbd>enter</kbd> to save and exit.
   * You can now run `exit` to escape the container's CLI.

## Updating

1. `docker kill scrobbler` - stops the currently running `scrobbler` if there is one
2. `docker rm scrobbler` - deletes the previously built `scrobbler` container
3. `docker rmi scrobbler` - deletes the previously built `scrobbler` iamge
4. Navigate to the location of the `scrobbler` source files (e.g. the folder with the Dockerfile, wherever you cloned this repo to)
5. `git stash` to save any local changes
6. `git pull` to get the latest files
7. `git stash pop` to restore any changes you saved in step 4
8. `docker build --no-cache -t scrobbler .` to build the new scrobbler Docker image
9. `docker run -v "$(pwd)"/env:/env -p 4000:80 -d --name scrobbler --restart unless-stopped scrobbler` to create and run a new container in the background from the new image. Change `-d` to `-it` to see realtime logs, but remember, you will need to delete and recreate the container again in order to run the container in detached (background) mode.

## Troubleshooting

* If you accidentally removed the `scrobbler` docker container, create a new one by navigating to the location you cloned this repo to (important!) and running:

    ```text
    docker run -v "$(pwd)"/env:/env -p 4000:80 -d --name scrobbler --restart unless-stopped scrobbler
    ```

  * Runs the container in the background since it is assumed you've already gone through the initial setup process.
