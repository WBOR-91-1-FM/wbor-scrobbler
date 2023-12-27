"""
This is a script to get up-to-date track information from a Spinitron page for a radio station, 
and "scrobble" that information to a user's Last.fm profile (allowing the user to record the
songs they are listening to on the radio station).

This functionality requires prerequsites of an API key and API secret from Last.fm, as well as a Spinitron API 
key associated with the desired station. These should be entered into the .env file with the variable names 
LASTFM_API_KEY, LASTFM_API_SECRET, and SPINITRON_API_KEY.

Before starting scrobbling, there must also be a web service session established with an associated
session key. If one has not already been obtained, the script should be run with the --setup flag
to establish one. The session key should be entered into the .env file with the variable name 
LASTFM_SESSION_KEY.
"""
import argparse
from datetime import datetime
from dateutil import parser, tz
from dotenv import load_dotenv, set_key
import hashlib
import logging
import os
import requests as r
import signal
import sys
import time
import xml.etree.ElementTree as ET

LASTFM_API_URL = "https://ws.audioscrobbler.com/2.0/"

# Pull env variables
load_dotenv()
lastfm_api_key = os.getenv("LASTFM_API_KEY")
lastfm_api_secret = os.getenv("LASTFM_API_SECRET")
lastfm_session_key = os.getenv("LASTFM_SESSION_KEY")
spinitron_api_key = os.getenv("SPINITRON_API_KEY")

spinitron_headers={"Authorization": f"Bearer {spinitron_api_key}"}

logging.basicConfig(level=logging.INFO,
                    filename="error.log",
                    filemode='w',
                    format="%(asctime)s %(name)-4s %(levelname)s \n%(message)s\n")

def signal_handler(sig, frame):
    print("\nCtrl+C pressed, aborting application. Goodbye!")
    sys.exit(0)

def generate_signature(params):
    """Takes parameters for a request and generates an md5 hash signature as specified in the Last.fm authentication specs
    
    Args:
        params (library): Library of stringe representing the parameters for the request
    Returns:
        str: The generated signature, as a string
    """
    signature = ''
    for key in sorted(params):
        signature += key + str(params[key])
    signature += lastfm_api_secret
    return hashlib.md5(signature.encode("utf-8")).hexdigest()

def get_token():
    """Performs API call auth.getToken to fetch a request token
    
    Returns:
        str: Returned token, as a string
    """
    params = {
        "method": "auth.getToken",
        "api_key": lastfm_api_key
    }
    params["api_sig"] = generate_signature(params)

    response = r.post(LASTFM_API_URL, params=params)
    root = ET.fromstring(response.content)
    return root.find("./token").text

def get_session_key(token):
    """Performs API call to auth.getSession to create a web service session and fetch the associated session key

    Args:
        token (str): A request token, retrived from auth.getToken
    Returns:
        str: Returned session key, as a string
    """
    params = {
        "method": "auth.getSession",
        "api_key": lastfm_api_key,
        "token": token
    }
    params["api_sig"] = generate_signature(params)

    response = r.post(LASTFM_API_URL, params=params)
    root = ET.fromstring(response.content)
    session_key_element = root.find("./session/key")
    if session_key_element is None:
        print("\nSession key not returned from Last.fm. Did you open the link above and press \"yes, allow access?\" Aborting setup.")
        sys.exit(0)
    
    session_key = session_key_element.text
    return session_key

def update_np(session_key, artist, track, album=None, duration=None):
    """Performs API call to track.updateNowPlaying to indicate to Last.fm that the user has started listening to a new track
    
    Args:
        session_key (str): A session key for an associated web service session generated by auth.getSession
        artist (str): The artist name
        track (str): The track name
        album (str, optional): The album name
        duration (int, optional): The length of the track in seconds
    Returns:
        int: Status code of the response"""

    params = {
        "method": "track.updateNowPlaying",
        "artist": artist,
        "track": track,
        "api_key": lastfm_api_key,
        "sk": session_key
    }
    if (album):
        params["album"] = album
    if (duration):
        params["duration"] = duration
    params["api_sig"] = generate_signature(params)

    response = r.post(LASTFM_API_URL, params=params)

    # Handle http error if necessary
    if not response.ok:
        handle_lastfm_http_error(response=response, request_type="NP")

    return response.status_code

def request_scrobble(session_key, artist, track, timestamp, album=None, duration=None):
    """Performs API call to track.scrobble to indicate to Last.fm that the user has listened to a song
    
    Args:
        session_key (str): A session key for an associated web service session generated by auth.getSession
        artist (str): The artist name
        track (str): The track name
        timestamp (float): The time the track started playing (UTC), in UNIX timestamp format
        album (str, optional): The album name
        duration (int, optional): The length of the track in seconds
    Returns:
        int: Status code of the response
        """
    params = {
        "method": "track.scrobble",
        "artist": artist,
        "track": track,
        "timestamp": timestamp,
        "api_key": lastfm_api_key,
        "sk": session_key
    }
    if (album):
        params["album"] = album
    if (duration):
        params["duration"] = duration
    params["api_sig"] = generate_signature(params)

    response = r.post(LASTFM_API_URL, params=params)
    
    # Handle http error if necessary
    if not response.ok:
        handle_lastfm_http_error(response=response, request_type="scrobble")

    return response.status_code

def handle_lastfm_http_error(response, request_type):
    """Helper function for update_np and request_scrobble, which takes the returned response from an HTTP error, parses, and logs the information.

    Args:
        response (requests.Response): Response object that is returned by an HTTP request. Should only be responses where response.ok is false (status code >= 400)
        request_type (str): A string indicating the source of the HTTP error ('NP' if it comes from an NP request, 'scrobble' if it comes from a scrobble request)
    """
    http_error_str = f"An HTTP error occured while making a {request_type} request.\nHTTP error code {response.status_code}: {response.reason}"
    try:
        # Get error info sent from last.fm if available
        root = ET.fromstring(response.content)
        data = root.find('./error')
        http_error_str += f"\nLast.fm error code {data.get('code')}: {data.text}"
    except:
        http_error_str += "\nCould not parse response data for more information."
    
    print(http_error_str)
    logging.error(http_error_str)

def setup():
    """Execution to run when the user has not established a web service session
    
    Returns:
        str: Established session key
    """
    
    token = get_token()

    # Prompt user to authorize for their account
    link = f"http://www.last.fm/api/auth/?api_key={lastfm_api_key}&token={token}"
    print(f"You need to authorize this application with your Last.fm account. To do so, visit the following link. Click \"yes, allow access.\" \n\n{link}\n")
    
    # Wait for user to confirm that they have authorized before proceeding
    confirmation = ''
    print("Please enter 'y' to after you have authorized this application with your Last.fm account:")
    while confirmation != 'y':
        confirmation = input()
        if confirmation.lower() != 'y':
            print("Did not receive 'y' - aborting setup...")
            sys.exit(0)
    
    session_key = get_session_key(token)
    print("\nSuccess!")
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('/scrobbler/setup_done', 'w') as setup_done_file:
            setup_done_file.write(f'Setup completed at {current_time}')

    return session_key

def run():
    """Execution to run when the user has already established a web service session"""
    
    print("Last.fm Spinitron scrobbler now running. To stop, use `Ctrl+C`\n")

    # Loop - each iteration is a check to Spinitron for new song data. All paths have blocking of at least 5 seconds to avoid sending too many requests
    miss_count = 0
    last_spin_id = None
    while True:
        # Get most recent spin info from Spinitron
        current_spin = r.get("https://spinitron.com/api/spins?count=1", headers=spinitron_headers).json()["items"][0]
        
        # Parse song data, get time difference between song end and current time
        spin_id = current_spin["id"]
        song_end_datetime = parser.parse(current_spin["end"])
        current_datetime = datetime.utcnow().replace(tzinfo=tz.UTC)
        time_difference = (song_end_datetime - current_datetime).total_seconds()

        # Check if a new song is playing
        if (time_difference > 0) and (spin_id != last_spin_id):
            miss_count = 0

            print("Making Last.fm Now Playing request for new spin.")
            update_np(session_key=lastfm_session_key, artist=current_spin["artist"], track=current_spin["song"], album=current_spin["release"], duration=current_spin["duration"])

            # Last.fm asks that we only scrobbly songs longer than 30 seconds
            if current_spin["duration"] > 30:
                # Idle until end of song, then make scrobble request
                time.sleep(time_difference)
                print("Song finished playing. Making scrobble request.")
                request_scrobble(session_key=lastfm_session_key, artist=current_spin["artist"], track=current_spin["song"], timestamp=parser.parse(current_spin["end"]).timestamp(), album=current_spin["release"], duration=current_spin["duration"])
            else:
                too_short_str = f"Song length too short to scrobble. Waiting for {time_difference} seconds..."
                print(too_short_str)
                logging.info(too_short_str)
                time.sleep(time_difference) # Idle until end of current song
            
            time.sleep(5)

        else:
            miss_count += 1 # Miss - loop has run without a new spin

            # If miss occurs > 10 times in a row (approx 6 minutes), idle for 5 minutes before next loop
            if miss_count > 10:
                miss_str = f"{miss_count} requests since last spin. Currently {-1*time_difference} seconds overdue according to last spin's end time value. Waiting 5 minutes before next request."
                print(miss_str)
                logging.info(miss_str)
                time.sleep(270)

            time.sleep(30)
        
        last_spin_id = spin_id

if __name__ == '__main__':
    # Ctrl+C handler
    signal.signal(signal.SIGINT, signal_handler)

    # Parse CLI args for --setup flag
    cli_parser = argparse.ArgumentParser()
    cli_parser.add_argument("--setup", action="store_true", help="Run script in setup mode (when a web service session has not been established)")
    args = cli_parser.parse_args()

    # Check if necessary env vars are either not present or left as example value
    if (not (lastfm_api_key and lastfm_api_secret and spinitron_api_key)) or (any(all(char == 'x' for char in string.lower()) for string in [lastfm_api_key, lastfm_api_secret, spinitron_api_key])):
        print("Please make sure you have set your LASTFM_API_KEY, LASTFM_API_SECRET, and SPINITRON_API_KEY values in the \".env\" file.")
    else:
        if args.setup:
            # If setup flag was used, run setup, then set the obtained session key in the .env file and run()
            if not os.path.exists('/scrobbler/setup_done'):
                new_session_key = setup()
                set_key(".env", "LASTFM_SESSION_KEY", new_session_key)
                load_dotenv()
                lastfm_session_key = os.getenv("LASTFM_SESSION_KEY")
                print("LASTFM_SESSION_KEY automatically set in .env\n")
                sys.exit(0)
            else:
                print("Setup was done previously. Aborting...")
                sys.exit(0)
        else:
            # Check if session key variable is not present or left as example value
            if (not lastfm_session_key) or all(char == 'x' for char in lastfm_session_key.lower()):
                print("Please make sure you have set your LASTFM_SESSION_KEY value in the \".env\" file. If you have not yet established a web service session, please run the script in setup mode using the --setup argument.")
                sys.exit(0)
            else:
                run()
